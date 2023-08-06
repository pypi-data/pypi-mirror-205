# authenticate.py


import click


@click.command()
@click.option("--username", prompt=True, help="Provide username")
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
def auth(username, password):
    """Provides user authentication"""
    click.echo(f"{username} {password}")

