import click

from ckanext.datapackage_creator.model import create_tables


@click.command(u"datapackage-creator-init-db")
def init_db():
    """Create tables command.
    """
    create_tables()


def get_commands():
    return [init_db]
