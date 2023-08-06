import os
import shutil
import tempfile
import time
from urllib.parse import urljoin
import logging
from typing import Any, Dict, Optional
import zipfile
import requests

from bam_core import settings
from bam_core.utils import serde

log = logging.getLogger(__name__)


class ListMonk(object):
    """
    See API documentation here: https://listmonk.app/docs/apis/apis/
    """

    def __init__(
        self,
        username=settings.LISTMONK_USERNAME,
        password=settings.LISTMONK_PASSWORD,
        base_url=settings.LISTMONK_BASE_URL,
    ):
        self.username = username
        self.password = password
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

    def make_request(
        self,
        path: str,
        method: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        files: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        """
        Make a request to the ListMonk API.
        """
        url = urljoin(self.base_url, path)
        if method == "GET":
            response = self.session.get(url, params=params, files=files)
        elif method == "POST":
            response = self.session.post(
                url, json=data, params=params, files=files
            )
        elif method == "PUT":
            response = self.session.put(
                url, json=data, params=params, files=files
            )
        elif method == "DELETE":
            response = self.session.delete(url, params=params, files=files)
        else:
            raise ValueError("Invalid method")
        return response

    def get_lists(self, **params):
        """
        Get all lists.
        """
        r = self.make_request("api/lists", "GET", params=params)
        return r.json()

    def get_list_by_name(self, name, **params):
        """
        Get a list by name.
        """
        lists = self.get_lists(**params)
        for l in lists.get("data", {}).get("results", []):
            if name.lower().strip() == l["name"].lower().strip():
                return l
        return None

    def start_import(self, params, file):
        """
        Import subscribers from a CSV file.
        """
        default_params = {
            "mode": "subscribe",  # subscribe or blocklist
            "delim": ",",  # delimiter in the uploaded file
            "lists": [1],  # array of list IDs to import into
            "overwrite": True,  # overwrite existing entries or skip them?
        }

        if isinstance(params["lists"][0], str):
            # lookup list ids using list names
            ids = []
            for name in params["lists"]:
                l = self.get_list_by_name(name)
                if not l:
                    raise ValueError(f"Invalid list name: {name}")
                ids.append(l["id"])
            params["lists"] = ids
        default_params.update(params)
        with open(file, "rb") as f:
            log.info(
                f"Importing subscribers from {file} using params: {default_params}"
            )
            file = f.read()
            r = self.make_request(
                "api/import/subscribers",
                "POST",
                params={"params": serde.obj_to_json(default_params)},
                files={"file": file},
            )
        return r.json()

    def get_import_status(self):
        """
        Get the status of an import.
        """
        r = self.make_request("api/import/subscribers", "GET")
        return r.json().get("data", {})

    def stop_imports(self):
        """
        Stop all imports.
        """
        r = self.make_request("api/import/subscribers", "DELETE")
        return r.json()

    def get_import_logs(self):
        """
        Get import logs.
        """
        r = self.make_request("api/import/subscribers/logs", "GET")
        return [l for l in r.json().get("data", "").split("\n") if l]

    def run_import(self, params, subscribers, **kwargs):
        """
        Run an import.
        """
        self.stop_imports()
        try:
            tempdir, file = self.write_subscriber_list_to_csv(
                subscribers, **kwargs
            )
            self.start_import(params, file)
            while True:
                status = self.get_import_status()
                log.info(f"got import status: {status}")
                logs = self.get_import_logs()
                for line in logs:
                    log.info(line)
                if status["status"] == "finished":
                    break
                elif status["status"] == "failed":
                    raise ValueError(f"Import failed: {logs}")
                elif status["status"] == "importing":
                    log.info("Waiting 10 seconds before checking status again")
                    time.sleep(10)
                    continue
        except Exception as e:
            self.stop_imports()
            log.error(e)
            raise e
        finally:
            shutil.rmtree(tempdir)

        return True

    @classmethod
    def write_subscriber_list_to_csv(
        cls, subscribers, name_field="First Name", email_field="Email"
    ):
        """
        Write a list of subscribers to a CSV file.
        """
        data = []
        for subscriber in subscribers:
            if "fields" in subscriber:
                subscriber = subscriber.get("fields", {})
            attributes = serde.obj_to_json(
                {
                    key: value
                    for key, value in subscriber.items()
                    if key not in [name_field, email_field]
                }
            )
            name = subscriber.get(name_field)
            data.append(
                {
                    "email": subscriber.get(email_field),
                    "name": name,
                    "attributes": attributes,
                }
            )
        tempdir = tempfile.mkdtemp()
        file = os.path.join(tempdir, "subscribers.csv")
        file_zip = os.path.join(tempdir, "subscribers.csv.zip")
        log.info(f"Writing {len(data)} subscribers to {file}")
        with open(file, "w") as f:
            f.write(serde.obj_to_csv(data))
        with zipfile.ZipFile(file_zip, mode="w") as f:
            f.write(file)
        return tempdir, file_zip
