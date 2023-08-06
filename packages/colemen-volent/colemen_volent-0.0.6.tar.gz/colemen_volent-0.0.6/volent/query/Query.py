# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    The Query module

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 04-28-2023 07:04:20
    `name`: query
    * @xxx [04-28-2023 07:04:34]: documentation for query
'''



from dataclasses import dataclass
import re
from typing import Iterable, Union
from datetime import datetime
from datetime import timezone

import colemen_utils as c


import volent.settings.types as _t
# import volent.settings as _settings
# from volent.Field import Field as _field
from volent.mixins import OrderedClass


@dataclass
class Query(metaclass=OrderedClass):
    main = None
    # database:_t.database_type = None
    model:_t.model_type = None
    '''A reference to the model instance this query is referencing.'''

    query_crud_type:str = None
    data:dict = None
    database:_t.database_type = None
    '''A reference to the database instance used to execute this query.'''

    _selects:Iterable[str] = None
    _wheres:Iterable[str] = None
    _count:bool = False
    _average:bool = False
    _sum:bool = False

    def __init__(
        self,
        model:_t.model_type,
        data:dict=None,
        select_columns=None,
        update_columns=None
        ):
        '''
            Create a new query instance.

            ----------

            Arguments
            -------------------------
            `model` {model}
                The model instance that this query will act on.
            `data` {dict}
                A dictionary of data that is used in the query operation.
            `select_columns` {list}
                A list of column names or column instances that should be "selected" in a select query
            `update_columns` {list}
                A list of column names or column instances that should be updated in an update query


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:04:55
            `memberOf`: Query
            `version`: 1.0
            `method_name`: query
            * @xxx [04-28-2023 07:07:59]: documentation for query
        '''
        self.model = model
        self.data = data
        self.database = model.database
        self._wheres = []
        self._selects = []
        self._updates = {}

        self.__parse_col_data(select_columns,update_columns)
        # else:
        #     for col in update_columns:
        #         if isinstance(col,(list,tuple)):
        #             if len(col) == 2:
        #                 name,value = col
        #                 self.add_update(name,value)
            #     if len(col) == 1:
            #         col = col[0]
            # if isinstance(col,(str)):
            #     self.add_select(col)

    def __parse_col_data(
        self,
        select_columns:Iterable[Union[str,_t.column_type]],
        update_columns:Iterable[Union[str,_t.column_type]]
        ):
        '''
            Parse the select and update columns into this query for later use.

            Essentially take a bunch of column names/instances and store them in a useful way.
            ----------

            Arguments
            -------------------------
            `select_columns` {list}
                A list of column names or column instances that should be "selected" in a select query

            `update_columns` {list}
                A list of column names or column instances that should be updated in an update query

            Return
            ----------------------
            Doesn't return shit.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:08:04
            `memberOf`: Query
            `version`: 1.0
            `method_name`: __parse_col_data
            * @xxx [04-28-2023 07:10:20]: documentation for __parse_col_data
        '''
        if isinstance(select_columns,(list)):
            for col in select_columns:
                if isinstance(col,(list,tuple)):
                    if len(col) >= 2:
                        name,alias = col
                        self.add_select(name,alias)
                    if len(col) == 1:
                        col = col[0]
                if isinstance(col,(str)):
                    self.add_select(col)

        if isinstance(update_columns,(dict)):
            mt_col = self.model.get_column("modified_timestamp")
            if mt_col is not None:
                self.add_update("modified_timestamp",round(datetime.now(tz=timezone.utc).timestamp()))


            for k,v in update_columns.items():
                col = self.model.get_column(k)
                # @Mstep [IF] if the column is the primary key of the table
                if col.is_primary is True:
                    # @Mstep [] skip
                    continue
                # @Mstep [] add a new update clause to this query.
                self.add_update(k,v)

            for col in self.model.columns:
                # @Mstep [IF] if the column has an "on_update" value set.
                if col.on_update != _t.undefined:
                    # @Mstep [IF] if the column is not already being updated.
                    if col.name not in self._updates:
                        # @Mstep [] add a new update clause to this query.
                        self.add_update(col.name,col.on_update)

    def filter_dict_by_columns(self,data:dict)->dict:
        '''
            Iterate a dictionary to remove key's that do not have a corresponding column in this query's model
            ----------

            Arguments
            -------------------------
            `data` {dict}
                The dictionary to filter.

            Return {dict}
            ----------------------
            The dictionary with only keys that match a column.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:10:41
            `memberOf`: Query
            `version`: 1.0
            `method_name`: filter_dict_by_columns
            * @xxx [04-28-2023 07:11:51]: documentation for filter_dict_by_columns
        '''
        output = {}
        for k,v in data.items():
            col = self.model.get_column(k)
            if col is not None:
                if v is None and col.nullable is False:
                    continue
                output[k] = v
        return output

    def sort_dict_by_columns(self,data:dict)->dict:
        '''
            Sort the keys of dictionary to match the order of columns in this query's model.
            
            This is primarily useful for parameterized insert statements, where the order of the columns
            is critical to inserting the correct data.
            
            This will sort them into the same order that the columns were declared in.
            
            ----------

            Arguments
            -------------------------
            `data` {dict}
                The dictionary to sort.


            Return {dict}
            ----------------------
            The dictionary with all keys reordered to match the model's columns.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:11:58
            `memberOf`: Query
            `version`: 1.0
            `method_name`: sort_dict_by_columns
            * @xxx [04-28-2023 07:13:57]: documentation for sort_dict_by_columns
        '''
        output = {}
        for col in self.model.columns:
            if col.name in data:
                output[col.name] = data[col.name]
        return output


    def add_where(self,column_name,value,comparison):
        '''
            Add a where clause to this query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column that this clause applies to.
            `value` {any}
                The value that the column is compared to
            `comparison` {str}
                The comparison/operator to use.

            Return {type}
            ----------------------
            no returned value

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-28-2023 07:14:41
            `memberOf`: Query
            `version`: 1.0
            `method_name`: add_where
            * @xxx [04-28-2023 07:19:24]: documentation for add_where
        '''
        if value is None:
            value = "NULL"
        # self.wheres.append(f"{column_name} {comparison} {value}")

        if c.string.to_snake_case(comparison) in ["!","!=","isnt","isnot","is_not","<>"]:
            comparison = "is not"

        data = {
            "column_name":column_name,
            "comparison":comparison,
            "value":value,
            "max_value":None,
        }

        if c.string.to_snake_case(comparison) in ["between"]:
            if isinstance(value,(list,tuple)):
                data['value'] = value[0]
                data['max_value'] = value[1]
            else:
                data['value'] = 0
                data['max_value'] = value

        if c.string.to_snake_case(comparison) in ["in"]:
            value = c.arr.force_list(value)
            if isinstance(value,(list,tuple)):
                items = []
                for idx,x in enumerate(value):
                    if isinstance(x,(str)):
                        # key = f"{column_name}_{idx}"
                        # items[key] = f"'{x}'"
                        items.append(x)


                    if isinstance(x,(int,float)):
                        # key = f"{column_name}_{idx}"
                        items.append(f"{x}")
                        # items[key] = f"{x}"

                # str_list = ', '.join(items)

                data['value'] = items

        self._wheres.append(data)


    @property
    def where_string(self)->str:
        '''
            Generate this query's where string.

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 12-09-2022 15:45:29
            `@memberOf`: UpdateQuery
            `@property`: where_string
        '''
        value = self._wheres
        # self._params = {}
        if len(self._wheres) > 0:
            wheres = []
            for where in self._wheres:
                wcol = where['column_name']
                wcomp = where['comparison']
                wval = str(where['value'])

                if c.string.to_snake_case(wcomp) in ["between"]:
                    min_key =f"{wcol}_minimum"
                    max_key =f"{wcol}_maximum"

                    single_where = f"{wcol} {where['comparison'].upper()} :{min_key} AND :{max_key}"
                    self._params[min_key] = where['value']
                    self._params[max_key] = where['max_value']


                elif c.string.to_snake_case(wcomp) in ["in","not_in"]:
                    in_list = []
                    for idx,val in enumerate(where['value']):
                        key = f"{where['column_name']}_{idx}"
                        self._params[key] = val
                        in_list.append(f":{key}")
                    in_list_string = ', '.join(in_list)
                    single_where = f"{where['column_name']} {where['comparison'].upper()} ({in_list_string})"


                # @Mstep [IF] if comparison matches [is,is not]
                elif c.string.to_snake_case(wcomp) in ["is","is_not"]:
                    # @Mstep [] generate the where string without applying a parameterized value.
                    # This can cause issues with "IS NULL" type clauses, because those cannot be parameterized
                    # single_where = f"{where['column_name']} {where['comparison'].upper()} {str(where['value'])}"
                    single_where = f"{wcol} {wcomp} {wval}"
                    # if wval.upper() == "NULL":
                        # single_where = f"{wcol} {wcomp} {wval}"
                    # params[where['column_name']] = where['value']
                else:
                    single_where = f"{where['column_name']} {where['comparison']} :{where['column_name']}"
                    self._params[where['column_name']] = where['value']

                wheres.append(single_where)
            wheres = ' AND '.join(wheres)
            value = f" WHERE {wheres}"
        else:
            value = ""
        return value

    def _format_query_params(self,sql:str,args:dict)->str:
        '''
            Format an SQL query's parameters to use the python named template format.

            This will only replace matches that have a corresponding key in the args dictionary.

            Parameters can begin with a dollar sign or colon.


            SELECT * from blackholes WHERE hash_id=$hash_id

            SELECT * from blackholes WHERE hash_id=%(hash_id)s

            ----------

            Arguments
            -------------------------
            `sql` {str}
                The sql string to format.

            `args` {dict}
                The dictionary of parameter values.


            Return {str}
            ----------------------
            The sql statement with parameters replaced.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2022 10:39:24
            `memberOf`: MySQLDatabase
            `version`: 1.0
            `method_name`: _format_query_params
            * @xxx [12-09-2022 10:43:23]: documentation for _format_query_params
        '''
        return _format_query_params(sql,args)

    def _paginate_select_query(self,sql)->str:
        '''
            Apply a limit and offset value to a select query statement.


            Arguments
            -------------------------
            `sql` {str}
                The sql statement to modify

            Return {str}
            ----------------------
            The sql statement with a limit and offset value applied.

            If the limit/offset if invalid no pagination is added.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-14-2022 11:45:47
            `memberOf`: QueryBase
            `version`: 1.0
            `method_name`: __paginate_select_query
            * @xxx [12-14-2022 11:46:12]: documentation for __paginate_select_query
        '''
        return _paginate_select_query(sql,self.limit,self.offset)

    def add_where_from_wheres(self,wheres:Iterable[dict]):
        for w in wheres:
            column_name = w["column_name"]
            value = w["value"]
            max_value = w["max_value"]
            comparison = w["comparison"]

            if max_value is not None:
                value = [value,max_value]

            self.add_where(column_name,value,comparison)
        return self

    def add_where_from_where(self,**kwargs):
        column_name = c.obj.get_kwarg(["column_name"],None,(str),**kwargs)
        value = c.obj.get_kwarg(["value"],None,None,**kwargs)
        max_value = c.obj.get_kwarg(["max_value"],None,None,**kwargs)
        comparison = c.obj.get_kwarg(["comparison"],None,None,**kwargs)

        if max_value is not None:
            value = [value,max_value]

        self.add_where(column_name,value,comparison)

        return self






def format_null(value):
    '''
        convert a None value to a "null" string.

        ----------

        Arguments
        -------------------------
        `value` {any}
            The value to test.

        Return {any}
        ----------------------
        "NULL" if the value is None, the original value otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-28-2023 07:20:50
        `memberOf`: Query
        `version`: 1.0
        `method_name`: format_null
        * @xxx [04-28-2023 07:22:36]: documentation for format_null
    '''
    if value is None:
        return "NULL"
    return value




def _paginate_select_query(sql:str,limit:int=None,offset:int=None)->str:
    '''
        Apply a limit and offset value to a select query statement.
        ----------

        Arguments
        -------------------------
        `sql` {str}
            The sql statement to modify

        [`limit`=None] {int}
            The limit to apply to the results.

        [`offset`=None] {int}
            The offset to apply to the results.


        Return {str}
        ----------------------
        The sql statement with a limit and offset value applied.

        If the limit/offset if invalid no pagination is added.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2022 11:09:53
        `memberOf`: MySQLDatabase
        `version`: 1.0
        `method_name`: _paginate_select_query
        * @xxx [12-09-2022 11:11:52]: documentation for _paginate_select_query
    '''
    if limit is None and offset is None:
        return sql
    if isinstance(limit,(str)):
        limit = re.sub(r'[^0-9]',"",limit)
        if len(limit) == 0:
            return sql
        limit = int(limit)

    if isinstance(offset,(str)):
        offset = re.sub(r'[^0-9]',"",offset)
        if len(offset) == 0:
            offset = None
        else:
            offset = int(offset)

    if limit == 0:
        limit = 1

    if offset is not None:
        if offset < 1:
            offset = None

    sql = c.string.strip(sql,[";"],"right")
    sql = re.sub(r'limit\s*[0-9]*\s*(,|offset)\s*(:?[0-9\s]*)?',"",sql,re.MULTILINE | re.IGNORECASE)

    limit_string = f"LIMIT {limit}"
    offset_string = ""
    if offset is not None:
        offset_string = f"OFFSET {offset}"
    paginate = f"{limit_string} {offset_string}"
    sql = f"{sql} {paginate}"
    return sql




def _format_query_params(sql:str,args:dict)->str:
    '''
        Format an SQL query's parameters to use the python named template format.

        This will only replace matches that have a corresponding key in the args dictionary.

        Parameters can begin with a dollar sign or colon.


        SELECT * from blackholes WHERE hash_id=$hash_id

        SELECT * from blackholes WHERE hash_id=%(hash_id)s

        ----------

        Arguments
        -------------------------
        `sql` {str}
            The sql string to format.

        `args` {dict}
            The dictionary of parameter values.


        Return {str}
        ----------------------
        The sql statement with parameters replaced.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2022 10:39:24
        `memberOf`: MySQLDatabase
        `version`: 1.0
        `method_name`: _format_query_params
        * @xxx [12-09-2022 10:43:23]: documentation for _format_query_params
    '''
    if isinstance(args,(dict)) is False:
        return sql
    # args = sorted(args.items(), key=lambda x: x[1], reverse=True)
    # @Mstep [] get a list of the argument keys
    arg_keys = list(args.keys())
    # @Mstep [] sort the keys from largest to smallest.
    arg_keys.sort(key=len, reverse=True)
    # @Mstep [] iterate the argument keys.
    for k in arg_keys:
    # for k,v in args.items():
        # @Mstep [] replace the key with the parameterized version.
        sql = re.sub(fr'[$:]{k}',f"%({k})s",sql)

    # matches = re.findall(r'[$:]([a-z_0-9]*)',sql,re.IGNORECASE)
    # if isinstance(matches,(list)):
    #     for match in matches:
    #         if match in args:
    #             sql = sql.replace(f"${match}",f"%({match})s")

    return sql

