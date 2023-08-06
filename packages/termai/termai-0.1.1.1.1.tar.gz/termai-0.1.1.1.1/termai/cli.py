import click
from .termchat import main

@click.command()
@click.argument("prompt")
def cli(prompt):
    main(prompt)

if __name__ == "__main__":
    cli()
