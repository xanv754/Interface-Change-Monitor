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
        click.echo(f'|_ Updating the database with the file: {file}... Please wait...')
        asyncio.run(read_file(date))
        click.echo(f'|_ Database updated with the file {file}!')
    elif date: 
        click.echo(f'|_ Updating the database with the date {date}... Please wait...')
        asyncio.run(read_files(date))
        click.echo(f'|_ Database updated with the date {date}!')
    else: 
        click.echo(f'|_ Updating the database... Please wait...')
        asyncio.run(read_files())
        click.echo(f'|_ Database updated!')

@cli.command(help='View the status of the consults SNMP, the updater, etc...')
def status():
    pass

if __name__ == '__main__':
    try:
        cli()
    except SystemExit as e:
        pass
    except:
        traceback.print_exc()