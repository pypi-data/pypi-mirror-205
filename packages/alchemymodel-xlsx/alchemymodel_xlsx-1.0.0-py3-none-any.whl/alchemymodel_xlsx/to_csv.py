# lib
from typing import Dict
from io import BytesIO
import pandas as pd

# sqlalchemy
from sqlalchemy.orm import Query

# own lib
from alchemymodel_xlsx.exceptions import FieldModelNotFound
from alchemymodel_xlsx import utils


def query_to_csv(
    query: Query,
    fields: Dict,
    expr_bool: Dict = None,
):
    """Convert model from sqlalchemy to excel file.

    :param db_session:
        A :class:`Session` instance.
    :param model:
        A :class:`object` instance, example: Model User.
    :param query:
        A :class:`sqlalchemy.orm.Query` instance in case it is a custom query.
    :param fields:
        A :Dict:`Dict` instance in case it is custom fields list
    :param expr_bool:
        A :Dict:`Dict` instance in case it is custom bool expresions
    :returns:
        The :bytes:`bytes` instance of excel file
    """

    data = {}

    for key, label in fields.items():
        data[label] = []

    for row in query:
        for key, label in fields.items():
            try:
                raw_value = getattr(row, key)
            except AttributeError:
                raise FieldModelNotFound(
                    "Not found the field `{}` in query.".format(key)
                )

            value_serialize = utils.serialize_value(raw_value)

            if expr_bool and isinstance(raw_value, bool):
                value_serialize = expr_bool[raw_value]

            data[label].append(value_serialize)

    df = pd.DataFrame(data)
    csv_bytes = BytesIO()
    df.to_csv(csv_bytes, index=False)
    csv_bytes.seek(0)

    return csv_bytes.read()
