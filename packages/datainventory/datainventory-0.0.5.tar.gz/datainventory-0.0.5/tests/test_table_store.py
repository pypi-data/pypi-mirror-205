"""Unit test for table_store."""

import sqlalchemy

from datetime import date

from datainventory import _internal_store
from datainventory import common
from datainventory import table_store

from sqlalchemy.orm import sessionmaker


def test_simple_case():
    """Test the basic functionalities of table_store."""
    engine = sqlalchemy.create_engine("sqlite:///:memory:", echo=True, future=True)
    metadata = sqlalchemy.MetaData()
    Session = sessionmaker(bind=engine)
    store = table_store.TableStore(
        create_key=_internal_store.CREATE_KEY,
        device_id="test_device",
        metadata=metadata,
        session=Session(),
        connection=engine.connect(),
    )

    TABLE = "temperature"

    schema = {"scale": common.ColumnType.String, "value": common.ColumnType.Float}
    store.create_table(table_name=TABLE, columns=schema)

    assert store.query_data(table_name=TABLE).empty

    data = [{"scale": "F", "value": 97.9}, {"scale": "C", "value": 23.7}]
    store.insert(table_name=TABLE, values=data)

    range = common.Range(date.today())
    output = store.query_data(TABLE, range=range)
    assert output["value"].count() == 2
