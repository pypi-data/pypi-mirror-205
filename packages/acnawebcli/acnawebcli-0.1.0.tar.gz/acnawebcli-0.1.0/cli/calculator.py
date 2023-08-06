# calculator.py

import click


@click.command()
@click.argument("xs", type=int, nargs=-1)
@click.option("-v", "--verbose", help="Show info", is_flag=True)
def add(xs, verbose):
    """Adds numbers"""
    if verbose:
        click.echo(f"{' + '.join(str(x) for x in xs)} = {sum(xs)}")
    else:
        click.echo(sum(xs))
    

@click.command()
@click.argument("xs", type=int, nargs=-1)
@click.option("-v", "--verbose", help="Show info", is_flag=True)
def subtract(xs, verbose):
    """Substracts numbers"""
    result = xs[0]
    for x in xs[1:]:
        result -= x

    if verbose:
        click.echo(f"{' - '.join(str(x) for x in xs)} = {result}")
    else: 
        click.echo(result)

