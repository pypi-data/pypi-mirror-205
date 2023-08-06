import os

import typer

DEFAULT_SERVER = 'https://apis.launchflow.com'

ADD_READER_HELP_TEXT = 'Adds a reader to a{}'
REMOVE_READER_HELP_TEXT = 'Removes a reader from a{}'
ADD_WRITER_HELP_TEXT = 'Adds a writer to a{}'
REMOVE_WRITER_HELP_TEXT = 'Removes a writer from a{}'
GET_HELP_TEXT = 'Prints details about a{}'
CREATE_HELP_TEXT = 'Create a{}'
NAME_HELP_TEXT = 'The name of the {}'
PERMISSION_HELP_TEST = 'The permission to perform operations on. Should be of the format: (user|serviceAccount|domain):(email|domain)'  # noqa: E501

BEARER_TOKEN_OPTION = typer.Option(default=None, hidden=True)

SERVER_ADDRESS_OPTION = typer.Option(default=DEFAULT_SERVER, hidden=True)
PERMISSION_ARG = typer.Argument(...,
                                help=PERMISSION_HELP_TEST,
                                show_default=False)

_TEAM_HELP = (
    'The name of the team to apply the operation on. If this is unset we will '
    'use the default team set in the config.')
TEAM_OPTION = typer.Option(default=None, help=_TEAM_HELP)

_FLOW_HELP = (
    'The name of the existing flow to apply the operation on. If this is unset'
    ' we will create an ad hoc flow for you.')
FLOW_OPTION = typer.Option(default=None, help=_FLOW_HELP)

CONFIG_DIR = os.path.join(os.path.expanduser('~'), '.config', 'launchflow')
