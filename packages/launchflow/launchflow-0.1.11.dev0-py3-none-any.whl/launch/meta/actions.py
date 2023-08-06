from typing import Optional
from launch import constants
from launch.auth import cache
from pprint import pprint
import requests
from websocket import create_connection
from websocket import WebSocketConnectionClosedException

import typer

from launch.config import LaunchFlowConfig

app = typer.Typer()


@app.command()
def upgrade(server_address: str = constants.SERVER_ADDRESS_OPTION):
    creds = cache.get_user_creds(server_address)
    response = requests.get(
        f'{server_address}/billing/checkout',
        headers={'Authorization': f'Bearer {creds.id_token}'})
    response_json = response.json()
    return f'Sign up for a premium account at {response_json["url"]}'


@app.command()
def stream_job_info(job_id: int,
                    server_address: str = constants.SERVER_ADDRESS_OPTION):
    creds = cache.get_user_creds(server_address)
    ws_endpoint = server_address.replace('http://', 'ws://').replace(
        'https://', 'wss://')
    if ws_endpoint.endswith('/'):
        ws_endpoint = ws_endpoint[:-1]
    ws = create_connection(
        f'{ws_endpoint}/jobs/info?job_id={job_id}',
        timeout=600,
        header={'Authorization': f'Bearer {creds.id_token}'})
    while True:
        try:
            print(ws.recv())
        except WebSocketConnectionClosedException:
            print('Web socket close.')
            break


@app.command()
def drain_job(job_id: int,
              server_address: str = constants.SERVER_ADDRESS_OPTION):
    creds = cache.get_user_creds(server_address)
    response = requests.post(
        f'{server_address}/jobs/drain',
        headers={'Authorization': f'Bearer {creds.id_token}'},
        json={'job_id': job_id})
    if response.status_code != 200:
        print(f'Failed to drain job error: {response.content.decode()}')
        return
    print('Job is now draining')


@app.command()
def stop_job(job_id: int,
             server_address: str = constants.SERVER_ADDRESS_OPTION):
    creds = cache.get_user_creds(server_address)
    response = requests.post(
        f'{server_address}/jobs/stop',
        headers={'Authorization': f'Bearer {creds.id_token}'},
        json={'job_id': job_id})
    if response.status_code != 200:
        print(f'Failed to stop job: {response.content.decode()}')
        return
    print('Job is now stopped.')


@app.command()
def set_default_team(
    team_id: Optional[int] = typer.Argument(
        default=None, help='The team ID to set as default'),
    server_address: str = constants.SERVER_ADDRESS_OPTION,
):
    config = LaunchFlowConfig.load(server_address)
    config.default_team_id = team_id
    config.write()


@app.command()
def get_config():
    config = LaunchFlowConfig.load()
    print('Launchflow Config')
    print('-----------------')
    print(f'    default team ID: {config.default_team_id}')


@app.command()
def list_teams(server_address: str = constants.SERVER_ADDRESS_OPTION):
    creds = cache.get_user_creds(server_address)
    response = requests.post(
        f'{server_address}/teams/list',
        headers={'Authorization': f'Bearer {creds.id_token}'})
    if response.status_code != 200:
        print(f'Failed to list teams: {response.content.decode()}')
        return

    print('List Teams')
    print('-----------')
    pprint(response.json())


@app.command()
def list_flows(server_address: str = constants.SERVER_ADDRESS_OPTION):
    creds = cache.get_user_creds(server_address)
    response = requests.post(
        f'{server_address}/flows/list',
        headers={'Authorization': f'Bearer {creds.id_token}'})
    if response.status_code != 200:
        print(f'Failed to list flows: {response.content.decode()}')
        return

    print('List Flows')
    print('-----------')
    pprint(response.json())


@app.command()
def list_jobs(running: bool = typer.Option(
    default=False,
    help='If true will only return running jobs. Otherwise returns all jobs'),
              server_address: str = constants.SERVER_ADDRESS_OPTION):
    creds = cache.get_user_creds(server_address)
    response = requests.post(
        f'{server_address}/jobs/list',
        json={'running_only': running},
        headers={'Authorization': f'Bearer {creds.id_token}'})
    if response.status_code != 200:
        print(f'Failed to list jobs: {response.content.decode()}')
        return

    print('List Jobs')
    print('-----------')
    pprint(response.json())


if __name__ == "__main__":
    app()
