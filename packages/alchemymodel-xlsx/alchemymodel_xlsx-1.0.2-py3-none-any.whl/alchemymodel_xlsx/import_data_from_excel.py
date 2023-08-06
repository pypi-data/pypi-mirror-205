# lib
from typing import Dict
import pandas as pd

#  sqlalchemy
from sqlalchemy.orm import Session

# own lib
from alchemymodel_xlsx.exceptions import SqlAlchemyError
from alchemymodel_xlsx.exceptions import FieldsNotEqual
from alchemymodel_xlsx import utils


def import_data(
    file: bytes,
    model: object,
    fields: Dict,
    db_session: Session,
    expr_bool: Dict,
) -> None:
    """Import data from excel to sqlalchemy model.

    :param file:
        A :bytes:`bytes` instance.
    :param model:
       A :class:`object` instance, example: User Model.
    :param fields:
       A :Dict:`Dict` instance, to import data depends of fields.
    :param db_session:
       A :Session:`Session` instance, to generate query to import data with db session.
    :param expr_bool:
       A :Dict:`Dict` instance in case it is custom bool expresions
    :returns:
        None
    """

    excel_file = pd.read_excel(file, na_filter=None)

    # fields keys from dict
    fields_names = list(fields.values())

    # Get the column names
    column_names = list(excel_file.columns)

    if set(column_names) != set(fields_names):
        raise FieldsNotEqual("Fields are not equal that excel file")

    objs = []

    for _, row in excel_file.iterrows():
        data = {}
        row_dict = row.to_dict()

        for key, value in row_dict.items():
            model_key = list(fields.keys())[list(fields.values()).index(key)]
            data[model_key] = utils.serialize_value(value)

            if expr_bool:
                expr_bool_values = list(expr_bool.values())
                if value in expr_bool_values:
                    value = True if value == expr_bool[True] else False
                    data[model_key] = value

        obj = model(**data)

        objs.append(obj)

    try:
        db_session.bulk_save_objects(objs)
        db_session.commit()
    except Exception as e:
        raise SqlAlchemyError(
            "Error from sqlalchemy when try import bulk data: `{}`".format(e)
        )
    finally:
        db_session.close()
