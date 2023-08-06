# lib
from datetime import datetime
from typing import Any
import numpy

# exceptions
from alchemymodel_xlsx.exceptions import FieldAreNotTypeRequired
from alchemymodel_xlsx.const import DEFAULT_BOOL_VALUES


def datetime_to_str(value: datetime) -> str:
    if not isinstance(value, datetime):
        raise FieldAreNotTypeRequired(
            "The value `{}` must be datetime type.".format(value)
        )

    str_date = value.strftime("%Y-%m-%d")
    return str_date


def bool_to_str(value: bool) -> str:
    if not isinstance(value, bool):
        raise FieldAreNotTypeRequired("The value `{}` must be bool type.".format(value))

    return DEFAULT_BOOL_VALUES[value]


def none_to_str(value) -> str:
    if value is not None:
        raise FieldAreNotTypeRequired("The value `{}` must be None type.".format(value))

    return ""


def serialize_value(value) -> Any:
    """
    Convert each value from excel file to python type

    :param value:
        A :Any:`Any` value from each row - column from excel.
    """

    types = [str, datetime, int, float, bool, None]

    proccess_types = {
        datetime: datetime_to_str,
        bool: bool_to_str,
        None: none_to_str,
    }

    value_type = type(value)

    if isinstance(value, numpy.generic):
        if value.item() in proccess_types:
            value = proccess_types[value.item()](value)
            return value

    for python_type in types:
        if python_type == value_type:
            if value_type in proccess_types:
                value = proccess_types[value_type](value)
                return value

    return str(value)
