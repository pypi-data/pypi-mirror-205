"""Unit test for inventory."""
import pathlib

from datainventory import inventory


def test_simple_case(tmp_path):
    """Test the basic functionalities of inventory."""
    inventorydir = tmp_path / pathlib.Path("inventorydir")
    my_inventory = inventory.Inventory(device_id="device_id", inventory=inventorydir)
    assert my_inventory.get_media_store() is not None
    assert my_inventory.get_model_store() is not None
    assert my_inventory.get_table_store() is not None

    dest_filename: pathlib.Path = tmp_path / pathlib.Path("archive")

    archive_path = my_inventory.export(dest_filename=dest_filename)
    assert archive_path.exists()

    my_inventory.destroy()
    assert not inventorydir.exists()
