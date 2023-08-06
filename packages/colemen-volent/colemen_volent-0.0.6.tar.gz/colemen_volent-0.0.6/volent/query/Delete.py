# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    The query delete module.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 04-28-2023 07:24:17
    `name`: delete
    * @xxx [04-28-2023 07:24:33]: documentation for delete
'''



from dataclasses import dataclass
from typing import Iterable, Union


import colemen_utils as c


import volent.settings.types as _t
# import volent.settings as _settings
# from volent.Field import Field as _field
# from volent.Relationship import Relationship as _relationship
# from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint
from volent.query.Query import Query
from volent.query.WhereMixin import WhereMixin


@dataclass
class Delete(Query,WhereMixin):
    def __init__(self,model:_t.model_type) -> None:
        '''
            Create a delete query instance.

            ----------

            Arguments
            -------------------------
            `model` {model}
                The model instance to execute a delete operation on.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:24:53
            `memberOf`: Delete
            `version`: 1.0
            `method_name`: Delete
            * @xxx [04-28-2023 07:26:55]: documentation for Delete
        '''
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
    def query(self)->tuple:
        '''
            Generate this delete query's SQL.

            ----------

            Return {tuple}
            ----------------------
            A tuple containing the query string and a dictionary of query params.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:27:18
            `memberOf`: Delete
            `version`: 1.0
            `method_name`: query
            * @xxx [04-28-2023 07:33:51]: documentation for query
        '''

        value = f"DELETE {self.model.quoted_name} {self.where_string}"

        value = self._paginate_select_query(value)
        value = self._format_query_params(value,self._params)
        return value,self._params
        # return value,self._params

    def execute(self,foreign_key_checks:bool=True)->Union[bool,dict,int]:
        '''
            Execute the delete operation on the model.

            ----------

            Arguments
            -------------------------
            [`foreign_key_checks`=True] {bool}
                If False, the query will not perform foreign key checks before executing the deletion.
                Be careful, this can cause integrity issues and will NOT warn you about it.


            Return {bool}
            ----------------------
            True if execution was successful,False otherwise.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:34:05
            `memberOf`: Delete
            `version`: 1.0
            `method_name`: execute
            * @xxx [04-28-2023 07:40:57]: documentation for execute
        '''

        sql,args= self.query

        if sql is False:
            return False
        # @Mstep [] execute the delete query.
        result = self.database.run(sql,args,foreign_key_checks=foreign_key_checks)
        return result




def format_null(value):
    if value is None:
        return "NULL"
    return value

