# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
import re
from typing import Iterable, OrderedDict, Sized, Union
from collections import OrderedDict

import colemen_utils as c


class VolentError(Exception):
    '''Base Class for Volent exceptions'''



class ValidationError(VolentError):
    _errors = {}
    def __init__(
        self,
        message:Union[str,list,dict],
        field_name:str=None,
        ):
        if field_name is not None:
            self._errors[field_name] = message
        super().__init__(message)

    @property
    def errors(self):
        '''Get a dictionary of errors

        {
            field_name : error_message
        }
        '''
        if len(list(self._errors.keys())) == 0:
            data = {}
            for idx,k in enumerate(self.args):
                data[f"v{idx}"] = k
            return data
        return self._errors

class DuplicateEntryError(VolentError):
    _error = None
    _constraint_name = None
    _value = None
    _message = None
    _errno = None
    _sql_state = None
    _args = None
    def __init__(
        self,
        error,
        ):
        self._error = error
        message=self._message = error.msg
        self._errno = error.errno
        self._args = error.args
        self._sql_state = error.sqlstate

        match = re.findall(r"key\s*'([a-zA-Z0-9_]*)",message)
        if len(match) == 1:
            self._constraint_name = match[0]
        val = message.replace("Duplicate entry ","")
        val = re.sub(r"for key .*","",val)
        self._value = c.string.strip(val,["'"])
        super().__init__(self._message)

    @property
    def constraint_name(self):
        '''
            Get this exceptions's constraint_name

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-27-2023 14:37:30
            `@memberOf`: exceptions
            `@property`: constraint_name
        '''
        return self._constraint_name

    @property
    def value(self):
        '''
            Get this exceptions's value

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-27-2023 14:43:42
            `@memberOf`: exceptions
            `@property`: value
        '''
        return self._value

    @property
    def error_number(self):
        '''
            Get this exceptions's error_number

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-27-2023 15:54:29
            `@memberOf`: exceptions
            `@property`: error_number
        '''
        return self._errno

    @property
    def sql_state(self):
        '''
            Get this exceptions's sql_state

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 04-27-2023 15:54:52
            `@memberOf`: exceptions
            `@property`: sql_state
        '''
        return self._sql_state


