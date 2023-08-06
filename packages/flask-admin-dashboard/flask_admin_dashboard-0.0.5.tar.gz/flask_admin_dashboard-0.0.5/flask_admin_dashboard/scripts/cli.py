import json
import os

import click as click
from click import prompt
from pathlib import Path

from flask_admin_dashboard.admin_dashboard import AdminDashboard

def link(uri, label=None):
    if label is None:
        label = uri
    parameters = ''

    # OSC 8 ; params ; URI ST <name> OSC 8 ;; ST
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'

    return escape_mask.format(parameters, uri, label)

@click.group()
def cli():
    """
    Simple CLI for managing Netsuite API Access
    """
    pass



