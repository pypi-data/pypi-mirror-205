"""Unit test for media_store."""

import pathlib
import pytest
import sqlalchemy

from datainventory import _internal_store
from datainventory import media_store

from sqlalchemy.orm import sessionmaker


def test_simple_case(tmp_path):
    """Test the basic functionalities of media_store."""
    testinventory = tmp_path / pathlib.Path("testinventory")
    datainventory = testinventory / pathlib.Path("data")
    engine = sqlalchemy.create_engine("sqlite:///:memory:", echo=True, future=True)
    Session = sessionmaker(bind=engine)
    store = media_store.MediaStore(
        create_key=_internal_store.CREATE_KEY,
        device_id="test_device",
        session=Session(),
        connection=engine.connect(),
        data_inventory=datainventory,
    )

    with pytest.raises(FileNotFoundError):
        fake_file = pathlib.Path("nonexist_file.txt")
        store.insert_media(file_path=fake_file, media_type=media_store.MediaType.Image)

    # Random test file
    test_binary_name = pathlib.Path("binary.mp4")
    test_binary: pathlib.Path = testinventory / test_binary_name
    test_binary.write_bytes(b"Binary file contents")

    dest = store.insert_media(
        file_path=test_binary, media_type=media_store.MediaType.Video
    )
    query_result = store.query_data()
    assert len(query_result) == 1

    assert query_result[0][0].filename == test_binary_name.name
    assert query_result[0][0].fullpath == str(dest.absolute())
    assert query_result[0][0].media_type == media_store.MediaType.Video.name
    assert query_result[0][0].format == test_binary_name.suffix
    assert query_result[0][0].device_id == "test_device"
    assert query_result[0][0].created_at is not None
    assert query_result[0][0].size > 0
    # assert query_result[0][0].duration > 0
