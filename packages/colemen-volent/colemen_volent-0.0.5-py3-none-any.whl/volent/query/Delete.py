# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
from typing import Iterable,OrderedDict, Union


import colemen_utils as c


import volent.settings.types as _t
import volent.settings as _settings
from volent.Field import Field as _field
# from volent.Relationship import Relationship as _relationship
# from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint
from volent.query.Query import Query
from volent.query.WhereMixin import WhereMixin


@dataclass
class Delete(Query,WhereMixin):
    def __init__(self,model:_t.model_type) -> None:
        self._params = {}

        self.query_crud_type = "delete"
        super().__init__(model)

    @property
    def select_string(self)->str:
        '''
            Get the compiled select string for this query.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:56:15
            `@memberOf`: SelectQuery
            `@property`: select_string
        '''
        if len(self._selects) == 0:
            value = "*"
        else:
            selects = []
            for sel in self._selects:
                value = None
                if sel['alias'] is not None:
                    value = f"{sel['column_name']} as {sel['alias']}"
                else:
                    value = f"{sel['column_name']}"
                if value is not None:
                    selects.append(value)
            value = ', '.join(selects)

        if self._count is True:
            value = f"COUNT({value})"
        if self._average is True:
            value = f"AVG({value})"
        if self.sum_ is True:
            value = f"SUM({value})"
        return value


    @property
    def query(self):


        value = f"DELETE {self.model.quoted_name} {self.where_string}"

        value = self._paginate_select_query(value)
        value = self._format_query_params(value,self._params)
        return value,self._params
        # return value,self._params

    def execute(self)->Union[bool,dict,int]:

        sql,args= self.query

        if sql is False:
            return False
        # @Mstep [] execute the delete query.
        result = self.database.run(sql,args)
        return result




def format_null(value):
    if value is None:
        return "NULL"
    return value

