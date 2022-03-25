import click
import json
from unsub_database import make_cursor
import pandas as pd

def get1(x):
    if x is None:
        return None
    return x[0] if x.any() else None

def none_abort(x, type):
    if x is None:
        click.echo(f'{type} not found')
        raise click.Abort()

def walk_up(scenario_id=None, package_id=None, institution_id=None):
    scenario_name = None
    package_name = None
    cursor = make_cursor()
    if scenario_id:
        cursor.execute(f"select * from jump_package_scenario where scenario_id = '{scenario_id}'")
        out: pd.DataFrame = cursor.fetch_dataframe()
        none_abort(out, 'scenario')
        if out.empty:
            cursor.execute(f"select * from jump_scenario_computed where scenario_id = '{scenario_id}' limit 1")
            out: pd.DataFrame = cursor.fetch_dataframe()
        if len(out) > 1:
            raise Exception(f"more than one result found for scenario_id {scenario_id}")
        package_id = get1(out.get('package_id'))
        scenario_name = get1(out.get('scenario_name'))
        if not scenario_name:
            cursor.execute(f"select * from jump_scenario_details_paid where scenario_id = '{scenario_id}' order by updated desc limit 1")
            out_name: pd.DataFrame = cursor.fetch_dataframe()
            if not out_name.empty:
                try:
                    scenario_name = json.loads(out_name.scenario_json[0])['name']
                except:
                    pass

    if package_id:
        cursor.execute(f"select * from jump_account_package where package_id = '{package_id}'")
        jap: pd.DataFrame = cursor.fetch_dataframe()
        none_abort(jap, 'package')
        if len(jap) > 1:
            raise Exception(f"more than one result found for package_id {package_id}")
        package_name = get1(jap.get('package_name'))
        institution_id = get1(jap.get('institution_id'))

    cursor.execute(f"select * from jump_debug_admin_combo_view where institution_id = '{institution_id}'")
    jdacv: pd.DataFrame = cursor.fetch_dataframe()
    none_abort(jdacv, 'institution')
    return {
        'scenario_id': scenario_id,
        'scenario_name': scenario_name,
        'package_id': package_id,
        'package_name': package_name,
        'institution_id': institution_id,
        'users': jdacv,}

def echo_users(x):
    if x['users'] is not None:
        if not x['users'].empty:
            click.echo('users')
            click.echo(x['users'].to_string())
        else:
            click.echo('users not found')
    else:
        click.echo('users not found')

@click.group()
def cli():
    """Lookup Unsub identifiers"""
    
@cli.command('s', short_help='lookup a scenario id')
@click.argument('id')
def scenario(id):
    """Examples

    ids s Jrofb6CY
    """
    out = walk_up(scenario_id=id)
    click.echo(f"scenario (id/name):   {out['scenario_id']} / {out['scenario_name']}")
    click.echo(f"package (id/name):    {out['package_id']} / {out['package_name']}")
    click.echo(f"institution (id):    {out['institution_id']}")
    echo_users(out)

@cli.command('p', short_help='lookup a package id')
@click.argument('id')
def package(id):
    """Examples

    ids p package-iQF8sFiRY99t
    """
    out = walk_up(package_id=id)
    click.echo(f"package (id/name):   {out['package_id']} / {out['package_name']}")
    click.echo(f"institution (id):    {out['institution_id']}")
    echo_users(out)


@cli.command('i', short_help='lookup a institution id')
@click.argument('id')
def institution(id):
    """Examples

    ids i institution-jiscrhu
    """
    out = walk_up(institution_id=id)
    click.echo(f"institution (id/name):   {out['users']['institution_id'][0]} / {out['users']['institution_display_name'][0]}")
    echo_users(out)
