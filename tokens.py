import os
import click
import requests
from unsub_database import make_cursor

def fetch_token(email):
    base_url = 'https://unpaywall-jump-api.herokuapp.com'
    data = {"password": os.getenv("UNSUB_SECRET_PWD"), "email": email}
    res = requests.post(base_url + "/user/login", json=data)
    if not res.ok:
        click.echo(f'not able to get token for {email}')
        raise click.Abort()
    if res.ok:
        json = res.json()
        return json["access_token"]

@click.group()
def cli():
    """Get Unsub JWT Tokens"""
    
@cli.command('e', short_help='get a JWT token by email address')
@click.argument('email')
def by_email(email):
    """Examples

    tokens e hello@world.org
    """
    out = fetch_token(email = email)
    click.echo(out)
