from typing import Any, List, Union

from pyairtable import Table, formulas as fx, Api

from bam_core import settings


class Airtable(object):
    def __init__(
        self,
        base_id: str = settings.AIRTABLE_BASE_ID,
        token: str = settings.AIRTABLE_TOKEN,
    ):
        self.base_id = base_id
        self.token = token
        self.api = Api(token)

    def get_table(self, table_name: str) -> Table:
        """
        Get a table object from the Airtable API
        :param table_name: The name of the table to get
        :return Table
        """
        return Table(self.token, self.base_id, table_name)

    def get_view(
        self, table_name: str, view_name: str, fields: List[str] = []
    ) -> Table:
        """
        Get a table object from the Airtable API
        :param table_name: The name of the table to get
        :return Table
        """
        return self.api.all(
            self.base_id, table_name, view=view_name, fields=fields
        )

    def get_view_count(
        self, table: str, view: str, fields: List[str] = [], unique=False
    ) -> int:
        """
        Get a table object from the Airtable API
        :param table_name: The name of the table to get
        :return Table
        """
        records = self.get_view(
            table_name=table, view_name=view, fields=fields
        )
        if unique and len(fields) and len(records):
            return len(set([r.get(fields[0]) for r in records]))
        return len(records)

    # core table objects

    @property
    def assistance_requests(self) -> Table:
        return self.get_table(settings.AIRTABLE_ASSISTANCE_REQUESTS_TABLE_NAME)

    @property
    def essential_goods(self) -> Table:
        return self.get_table(settings.AIRTABLE_ESSENTIAL_GOODS_TABLE_NAME)

    @property
    def volunteers(self) -> Table:
        return self.get_table(settings.AIRTABLE_VOLUNTEERS_TABLE_NAME)

    @property
    def mesh_requests(self):
        return self.get_view(
            settings.AIRTABLE_ASSISTANCE_REQUESTS_TABLE_NAME,
            settings.AIRTABLE_MESH_VIEW_NAME,
        )

    def filter_table(
        self,
        table: Union[str, Table],
        expressions: List[Any],
        match_any: bool = False,
        sort: List[str] = ["-Date Submitted"],
        fields=[],
    ):
        if isinstance(table, str):
            table = self.get_table(table)
        if not match_any:
            formula = fx.AND(*expressions)
        else:
            formula = fx.OR(*expressions)
        return table.all(formula=formula, sort=sort, fields=fields)
