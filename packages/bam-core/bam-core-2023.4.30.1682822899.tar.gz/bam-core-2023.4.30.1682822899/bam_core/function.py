import argparse
import time
from typing import Any, Dict, Optional

from bam_core.lib.airtable import Airtable
from bam_core.lib.listmonk import ListMonk
from bam_core.lib.s3 import S3


class Function(object):
    """
    A reusable class for building Digital Ocean Functions
    """

    listmonk = ListMonk()
    airtable = Airtable()
    s3 = S3()

    def get_parser(self) -> Optional[argparse.ArgumentParser]:
        """
        Add argparse params here.
        """
        return None

    def run(self, event, context, **params):
        """
        The core logic of your function.
        """
        raise NotImplementedError

    def main(self, event, context) -> Dict[str, Any]:
        """
        The Digital Ocean Function Handler.
        """
        parser = self.get_parser()
        if parser:
            params = vars(parser.parse_args())
        else:
            params = {}
        output = self.main(event, context, **params)
        return {"body": output}
