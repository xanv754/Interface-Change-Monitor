import traceback
import asyncio
import click
from updater.utils.file import read_file, read_files

@click.group()
def cli():
    pass

@cli.command(help='Update the database')
@click.option('-f', '--file', type=click.Path(exists=True), required=False, help='Update the database from a specific file')
@click.option('-d', '--date', type=str, required=False, help='Update the database from a specific date in format YYYY-MM-DD')
def database(file: str, date: str):
    if file: 
        click.echo(f'|_ Updating the database with the file: {file}...')
        asyncio.run(read_file(date))
    elif date: 
        click.echo(f'|_ Updating the database with the file: {file}...')
        asyncio.run(read_files(date))
    else: 
        click.echo(f'|_ Updating the database...')
        asyncio.run(read_files())

@cli.command(help='View the status of the consults SNMP, the updater, etc...')
def status():
    pass

if __name__ == '__main__':
    try:
        cli()
    except SystemExit as e:
        if e.code == 0: pass
        else: print(e)
    except:
        traceback.print_exc()