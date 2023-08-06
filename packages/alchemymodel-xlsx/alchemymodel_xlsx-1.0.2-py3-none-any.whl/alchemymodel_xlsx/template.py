# lib
from openpyxl.utils import get_column_letter
from typing import Dict
from io import BytesIO
import pandas as pd


def create_template(
    fields: Dict,
):
    """Generate excel file format from sqlalchemy model.

    :param model:
        A :class:`object` instance, example: User Model.
    :param fields:
        A :Dict:`Dict` instance in case it is custom fields list
    :returns:
        The :bytes:`bytes` instance of excel file
    """

    data = {}

    for _, label in fields.items():
        data[label] = [""]

    df = pd.DataFrame(data)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="openpyxl")
    df.to_excel(writer, sheet_name="hoja1", index=False)

    book = writer.book
    worksheet1 = writer.sheets["hoja1"]  # Set the format headers.

    for i, col in enumerate(df.columns, 1):
        column_len = max(df[col].astype(str).str.len().max(), len(col) + 2)
        worksheet1.column_dimensions[get_column_letter(i)].width = column_len + 5

    output = BytesIO()

    book.save(output)
    output.seek(0)

    return output.read()
