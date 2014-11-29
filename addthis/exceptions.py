# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class AddthisValidationError(Exception):
    """Raised if incorrect parameters are provided."""
    pass


class AddthisError(Exception):
    """Raised if Addthis service returns anything
    with status code other than 200.
    """
    def __init__(self, status_code, error_data):
        self.status_code = status_code
        self.error = error_data
        Exception.__init__(self, str(self))

    @property
    def code(self):
        return self.error["code"]

    @property
    def message(self):
        return self.error["message"]

    @property
    def attachment(self):
        return self.error["attachment"]

    def __str__(self):
        return "{error.status_code} Error (code = '{error.code}'," \
               " message='{error.message}', attachment='{error.attachment})'.".\
            format(error=self)