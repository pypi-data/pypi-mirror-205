from pathlib import Path

import click
from .core import NZB, parser


def nzb_printer(nzb: NZB):
    print("Name:", nzb.name)
    print("Header:", nzb.header)
    print("Passwort:", nzb.password)
    print("Groups:", ', '.join(nzb.groups))
    print("NZBLNK:", nzb.nzblnk)
    print("Uploaded at:", nzb.get_date_string())
    print("===================================")


def parse_nzb_path(path: Path | str):
    path = Path(path)
    if path.is_file():
        nzb_data = parser(path)
        nzb_printer(nzb_data)
    else:
        for p in path.glob('**/*.nzb'):
            parse_nzb_path(p)


@click.command(help="parse and print Nzb-Files")
@click.argument('paths', type=click.Path(exists=True, file_okay=True, resolve_path=False), nargs=-1)
def parse_nzb(paths):
    print("============================================")
    if len(paths) == 0:
        parse_nzb_path(Path('.'))
    for p in paths:
        parse_nzb_path(p)


@click.group(help="LordNzb Cli-Tool v0.1.0")
def cli():
    pass


cli.add_command(parse_nzb, name='parse')


def main():
    cli()


if __name__ == '__main__':
    main()