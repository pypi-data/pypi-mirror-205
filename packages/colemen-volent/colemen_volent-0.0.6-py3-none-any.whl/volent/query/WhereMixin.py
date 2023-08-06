# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import


from dataclasses import dataclass
from typing import Iterable, Union


# import colemen_utils as c


import volent.settings.types as _t
# import volent.settings as _settings
# from volent.Field import Field as _field
# from volent.Relationship import Relationship as _relationship
# from volent.UniqueConstraint import UniqueConstraint as _uniqueConstraint
# from volent.query.Query import Query


@dataclass
class WhereMixin:

    def equals(self,column_name:str,value,ignore_nulls:bool=False)->_t.query_type:
        '''
            Add an equals where clause to the query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to test.

            `value` {any}
                The value to test for.

            [`ignore_nulls`=False] {bool}
                If True, the clause will not be added if the value is None.

            Return {Query}
            ----------------------
            returns this Query Instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 11:16:43
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: equals
            * @xxx [04-25-2023 11:18:26]: documentation for equals
        '''
        if value is None and ignore_nulls is True:
            return self
        if value == _t.no_default:
            return self
        value = format_null(value)
        self.add_where(column_name=column_name,value=value,comparison="=")
        return self
    is_ = equals

    def is_not(self,column_name:str,value)->_t.query_type:
        '''
            Add an "IS NOT" where clause to the query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to test.

            `value` {any}
                The value to test for.

            Return {Query}
            ----------------------
            returns this Query Instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 11:16:43
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: equals
            * @xxx [04-25-2023 11:18:26]: documentation for equals
        '''
        value = format_null(value)
        self.add_where(column_name=column_name,value=value,comparison="!=")
        return self
    not_ = is_not

    def null(self,column_name:str)->_t.query_type:
        '''
            Add a "IS NULL" where clause to the query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to test.

            Return {Query}
            ----------------------
            returns this Query Instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 11:16:43
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: equals
            * @xxx [04-25-2023 11:18:26]: documentation for equals
        '''
        self.add_where(column_name=column_name,value="NULL",comparison="IS")
        return self

    def not_null(self,column_name:str)->_t.query_type:
        '''
            Add an "IS NOT NULL" where clause to the query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to test.

            Return {Query}
            ----------------------
            returns this Query Instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 11:16:43
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: equals
            * @xxx [04-25-2023 11:18:26]: documentation for equals
        '''
        self.add_where(column_name=column_name,value="NULL",comparison="IS NOT")
        return self

    def in_(self,column_name:str,options:Iterable[str])->_t.query_type:
        '''
            Add an "IN" where clause to the query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to test.

            `options` {list}
                The value to test for.

            Return {Query}
            ----------------------
            returns this Query Instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 11:16:43
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: in_
            * @xxx [04-25-2023 11:18:26]: documentation for in_
        '''
        self.add_where(column_name,options,"in")
        return self

    def not_in(self,column_name:str,options:list)->_t.query_type:
        '''
            Add a "NOT IN" where clause to the query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to test.

            `options` {any}
                A list of options to compare against.

            Return {Query}
            ----------------------
            returns this Query Instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 11:16:43
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: not_in
            * @xxx [04-25-2023 11:18:26]: documentation for not_in
        '''
        # options = f"({','.join(c.arr.values_to_strings(options))})"
        self.add_where(column_name,options,"not in")
        return self

    def between(self,column_name:str,minimum:Union[int,float],maximum:Union[int,float])->_t.query_type:
        '''
            Add a "BETWEEN" where clause to the query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to test.

            `minimum` {int,float}
                The minimum value
            `maximum` {int,float}
                The maximum value

            Return {Query}
            ----------------------
            returns this Query Instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 11:16:43
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: between
            * @xxx [04-25-2023 11:18:26]: documentation for between
        '''
        self.add_where(column_name,(minimum,maximum),"between")
        return self

    def greater_than(
        self,
        column_name:str,
        value:Union[int,float],
        inclusive:bool=False
        )->_t.query_type:
        '''
            Add a ">" where clause to the query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to test.

            `value` {any}
                The value to test for.

            [`inclusive`=False] {bool}
                If True, the value can be less than or equal to, this is the same as calling
                greater_than_equal()



            Return {Query}
            ----------------------
            returns this Query Instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 11:16:43
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: greater_than
            * @xxx [04-25-2023 11:18:26]: documentation for greater_than
        '''
        if inclusive is True:
            self.greater_than_equal(column_name,value)
        else:
            self.add_where(column_name,value,">")
        return self

    def greater_than_equal(self,column_name:str,value:Union[int,float])->_t.query_type:
        '''
            Add a ">=" where clause to the query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to test.

            `value` {any}
                The value to test for.

            Return {Query}
            ----------------------
            returns this Query Instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 11:16:43
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: greater_than_equal
            * @xxx [04-25-2023 11:18:26]: documentation for greater_than_equal
        '''
        self.add_where(column_name,value,">=")
        return self

    def less_than(self,column_name:str,value:Union[int,float],inclusive:bool=False)->_t.query_type:
        '''
            Add a "<" where clause to the query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to test.

            `value` {int,float}
                The value that the column must be less than.

            [`inclusive`=False] {bool}
                If True, the value can be less than or equal to, this is the same as calling
                less_than_equal()

            Return {Query}
            ----------------------
            returns this Query Instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 11:16:43
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: less_than
            * @xxx [04-25-2023 11:18:26]: documentation for less_than
        '''
        if inclusive is True:
            self.less_than_equal(column_name,value)
        else:
            self.add_where(column_name,value,">")
        return self

    def less_than_equal(self,column_name:str,value:Union[int,float])->_t.query_type:
        '''
            Add a "<=" where clause to the query.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to test.

            `value` {int,float}
                The value that the column must be less than or equal to.

            Return {Query}
            ----------------------
            returns this Query Instance.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 11:16:43
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: less_than
            * @xxx [04-25-2023 11:18:26]: documentation for less_than
        '''
        self.add_where(column_name,value,">=")
        return self

    def timestamps(self,column_name:str,start_timestamp:int=None,end_timestamp:int=None):
        '''
            Add a where clause used for filtering rows by dates.

            If both timestamps are provided only rows that are between will be returned.

            If only start is provided, the row timestamp must be greater.
            If only end is provided, the row timestamp must be less.

            ----------

            Arguments
            -------------------------
            `column_name` {str}
                The name of the column to filter

            [`start_timestamp`=None] {int}
                The start_timestamp to filter by

            [`end_timestamp`=None] {int}
                The end_timestamp to filter by

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-25-2023 08:58:25
            `memberOf`: WhereMixin
            `version`: 1.0
            `method_name`: where_timestamps
            * @xxx [04-25-2023 09:02:31]: documentation for where_timestamps
        '''
        # if self.model.get_column(column_name) is None:
        #     return None
        if start_timestamp is not None and end_timestamp is not None:
            self.between(column_name,start_timestamp,end_timestamp)
        if start_timestamp is None and end_timestamp is not None:
            self.less_than_equal(column_name,end_timestamp)
        if start_timestamp is not None and end_timestamp is None:
            self.greater_than_equal(column_name,start_timestamp)




def format_null(value):
    if value is None:
        return "NULL"
    return value


