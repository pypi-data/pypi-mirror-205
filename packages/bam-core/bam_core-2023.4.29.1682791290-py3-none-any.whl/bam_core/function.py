import sys
import time

from bam_core.lib.airtable import Airtable
from bam_core.lib.listmonk import ListMonk
from bam_core.lib.s3 import S3
from bam_core.utils.serde import obj_to_json


class Function(object):
    """
    A reusable class for building Digital Ocean Functions
    """

    listmonk = ListMonk()
    airtable = Airtable()
    s3 = S3()

    def get_params(self):
        """
        Add argparse params here.
        """
        return {}

    def main(self):
        """
        The main function that will be called by Digital Ocean Functions
        """
        raise NotImplementedError


    def run(self):
        start = time.time()
        params = self.get_params()
        output = self.main(**params)
        end = time.time()
        json_data = obj_to_json({"results": output, "params": params, "execution_time": end - start})
        sys.stdout.write(json_data)
