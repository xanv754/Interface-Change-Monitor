import traceback
import asyncio
import click
from updater.utils.file import read_file_snmp, read_files_snmp
from updater.libs.operator import get_operators, get_all_operators, get_operator

@click.group()
def cli():
    pass

@cli.command(help='Update the database')
@click.option('-f', '--file', type=click.Path(exists=True), required=False, help='Update the database from a specific file')
@click.option('-d', '--date', type=str, required=False, help='Update the database from a specific date in format YYYY-MM-DD')
def database(file: str, date: str):
    if file: 
        click.echo(f'|_ Updating the database with the file: {file}... Please wait...')
        asyncio.run(read_file_snmp(date))
        click.echo(f'|_ Database updated with the file {file}!')
    elif date: 
        click.echo(f'|_ Updating the database with the date {date}... Please wait...')
        asyncio.run(read_files_snmp(date))
        click.echo(f'|_ Database updated with the date {date}!')
    else: 
        click.echo(f'|_ Updating the database... Please wait...')
        asyncio.run(read_files_snmp())
        click.echo(f'|_ Database updated!')

@cli.command(help='View the info with containt the database.')
@click.option('-o', '--operator', type=click.Choice(['all', 'only-permanent', 'specific']), required=False, help='View the status of the operators in the database.')

def info(operator: str):
    if operator == 'all':
        click.echo(f'ALL OPERATORS')
        get_all_operators()
    elif operator == 'only-permanent':
        click.echo(f'OPERATORS WITH NOT DELETED ACCOUNT')
        get_operators()
    elif operator == 'specific':
        username = input("Username: ")
        if username: get_operator(username)
        else: print('The username is required')

if __name__ == '__main__':
    try:
        cli()
    except SystemExit as e:
        pass
    except:
        traceback.print_exc()