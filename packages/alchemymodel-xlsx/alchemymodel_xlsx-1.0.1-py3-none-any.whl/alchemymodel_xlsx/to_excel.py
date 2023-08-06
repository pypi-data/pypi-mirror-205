# lib
from openpyxl.utils import get_column_letter
from typing import Dict
from io import BytesIO
import pandas as pd

# sqlalchemy
from sqlalchemy.orm import Query

# own lib
from alchemymodel_xlsx.exceptions import FieldModelNotFound
from alchemymodel_xlsx.exceptions import FieldsSizeExceeded
from alchemymodel_xlsx.exceptions import FieldAreNotBoolean
from alchemymodel_xlsx import utils


def query_to_excel(
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

    expr_bool_values = list(expr_bool.keys())

    if len(expr_bool_values) > 2:
        raise FieldsSizeExceeded("The boolean fields must be only two")

    for key in expr_bool_values:
        if not isinstance(key, bool):
            raise FieldAreNotBoolean(f"The key: {key} is not boolean")

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
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="openpyxl")
    df.to_excel(writer, sheet_name="hoja1", index=False)

    book = writer.book
    worksheet1 = writer.sheets["hoja1"]

    # Set the format headers.
    for i, col in enumerate(df.columns, 1):
        column_len = max(df[col].astype(str).str.len().max(), len(col) + 2)
        worksheet1.column_dimensions[get_column_letter(i)].width = column_len + 5

    output = BytesIO()

    book.save(output)
    output.seek(0)

    return output.read()
