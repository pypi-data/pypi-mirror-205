# cli.py

import logging
import click
import os
from dhuolib.auth.login import do_login
from dotenv import load_dotenv

load_dotenv() 


@click.group()
def main():
    """Library for data science on DHuO Data"""


@main.command()
@click.option('--email', prompt=True, help='Your DHuO Data email')
@click.option('--password', prompt=True, help='Your DHuO Data password', 
            hide_input=True, confirmation_prompt=True)
def login(email, password):
    """Provides user authentication"""

    click.echo("Efetuando login...")

    try: 
        do_login(email, password)

        click.echo(f"Seja bem-vindo ao DHuO Data {email}")

    except Exception as e:
        logging.exception("Logon error")        


@main.command()
def create_project():
    """Create Machine Learning project"""


@main.command()
def list_projects():
    """List Machine Learning """


@main.command()
def status():
    """Show current status"""    


@main.command()
def get_project():
    """Get project"""    


@main.command()
def show_info():
    """Show environment info"""

    click.echo("IAM_URI\t" + os.getenv("IAM_URI"))
