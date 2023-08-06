"""Command line interface for katlas."""

import click

from katlas.motif import SequenceMotif

@click.group()
def cli():
    pass

@cli.command()
@click.option('--motif', '-m', help='Motif to search for.')
def search(motif):
    """Search for a motif in the database."""
    print(motif)

@cli.command()
def main():
    """Main entry point."""
    example_motif = "PSVEPPLS*QETFSDL"
    s = SequenceMotif(example_motif)
    print(s)

if __name__ == '__main__':
    cli()

