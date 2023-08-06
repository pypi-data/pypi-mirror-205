# cli.py


import click


@click.group()
def main():
    """CLI main application"""
    click.echo("main")


@main.command()
def shows():
    """Shows notes"""
    pass


@main.command()
def add():
    """Adds info"""


@main.command()
def update():
    """Updates database"""