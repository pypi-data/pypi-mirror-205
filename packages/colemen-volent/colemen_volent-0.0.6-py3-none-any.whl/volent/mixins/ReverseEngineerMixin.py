# # pylint: disable=missing-function-docstring
# # pylint: disable=missing-class-docstring
# # pylint: disable=line-too-long
# # pylint: disable=unused-import

# from dataclasses import dataclass
# from string import Template
# from typing import Iterable, Union
# # from typing import Iterable

# import colemen_utils as c
# import sqlite3
# import mysql.connector as _mysqlConnnector


# import volent.settings as _settings
# import volent.settings.types as _t

# qc:str = _settings.control.sql_quote_char
# '''The quote character to use.'''
# indent:str = " " * _settings.control.mysql.create_table_indent
# '''The indentation string used for the table contents'''


# @dataclass
# class ReverseEngineerMixin:
    
    
#     def gen_python_create(self,data:dict):
        
#     def gen_create(self):
#         from volent.Database import Database as _database
#         from volent.Model import Model as _model
#         from volent.Column import Column as _column
#         from volent.UniqueConstraint import UniqueConstraint as _unique_constraint
#         from volent.Relationship import Relationship as _relationship
        
#         if isinstance(self,_column):
#             value = self._gen_column_create()





# COLUMN_CREATE_TEMPLATE = """self.$name = Column($data_type()$args)"""
# def _gen_column_create(self,col:_t.column_type):
#     s = Template(COLUMN_CREATE_TEMPLATE)
#     args = []
#     if col.is_foreign_key is True:
#         args.append("is_foreign_key=True")
#     if col.is_primary is True:
#         args.append("is_primary=True")
#     if col.is_primary is True:
#         args.append("is_primary=True")
#     val = s.substitute(
#         indent=indent,
#         name=col.name,
#         data_type=col.data_type.__class__.__name__,
#     )