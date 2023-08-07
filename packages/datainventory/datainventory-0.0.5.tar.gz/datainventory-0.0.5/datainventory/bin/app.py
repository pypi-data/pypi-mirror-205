"""A CLI tool for exporting data."""
import click
import pathlib

from datainventory import inventory


@click.group()
def cli() -> None:
    """CLI group."""
    pass


@cli.command()
@click.option("--device_id")
@click.option("--inventory_path")
@click.option("--export_path")
def inventory_export(device_id: str, inventory_path: str, export_path: str) -> None:
    """Export the entire inventory data."""
    store = inventory.Inventory(
        device_id=device_id, inventory=pathlib.Path(inventory_path)
    )
    store.export(dest_filename=pathlib.Path(export_path))


@cli.command()
@click.option("--device_id")
@click.option("--source_path")
@click.option("--inventory_path")
def inventory_import(device_id: str, source_path: str, inventory_path: str) -> None:
    """Import data into the inventory."""
    store = inventory.Inventory(
        device_id=device_id, inventory=pathlib.Path(inventory_path)
    )
    store.import_data(source_data=pathlib.Path(source_path))


@cli.command()
@click.option("--device_id")
@click.option("--inventory_path")
def destroy(device_id: str, inventory_path: str) -> None:
    """Destroy the inventory data."""
    store = inventory.Inventory(
        device_id=device_id, inventory=pathlib.Path(inventory_path)
    )
    store.destroy()


def main() -> None:
    """Entry point."""
    cli()
