#!/usr/bin/env python
import pkg_resources
import click
from scinode.profile import ScinodeProfile


class CLIContext:
    """Context Object for the CLI."""

    def __init__(self, app=None):
        """Initialize the CLI context."""
        self.profile = ScinodeProfile()
        self.activate_profile = self.profile.load_activate_profile()
        self.app = app
        if self.activate_profile is not None and self.activate_profile["celery"]:
            from scinode.engine.celery.tasks import app

            self.app = app
            self.use_celery = True
        else:
            self.use_celery = False


@click.group(help="CLI tool to manage SciNode")
@click.pass_context
def scinode(ctx):
    ctx.obj = CLIContext()


@scinode.command(help="Start the services.")
@click.option("--web", is_flag=True, default=False, help="Start web service")
@click.pass_context
def start(ctx, web):
    """Start scinode services.

    Examples
    --------

    scinode start
    """
    import os
    from scinode.profile.profile import init_configuration
    from scinode.daemon.worker_config import init_worker
    from scinode.daemon.scheduler_config import init_scheduler
    from scinode.utils.emoji import logo

    print(logo)
    print("Starting Scinode Services")
    print("Initializing configuration")
    init_configuration()
    print("Initializing scheduler")
    init_scheduler()
    print("Initializing worker")
    init_worker()
    os.system("scinode scheduler start")
    os.system("scinode worker start localhost")
    if web:
        os.system(
            "nohup scinode web start > ~/.scinode/web.log & echo $! > ~/.scinode/web.pid &"
        )
        print("Please visit the web app at: http://127.0.0.1:5000/")
    print("Scinode status:")
    os.system("scinode status")


@scinode.command(help="Stop the services.")
@click.pass_context
def stop(ctx):
    """Stop scinode services.

    Examples
    --------

    scinode stop
    """
    import os

    print("Sotp Scheduler...")
    os.system("scinode scheduler stop")
    print("Stop Workers...")
    os.system("scinode worker stop-all")
    print("Stop Web...")
    os.system("kill $(cat ~/.scinode/web.pid)")


@scinode.command(help="Start the services.")
@click.pass_context
def restart(ctx):
    """Restart scinode services.

    Examples
    --------

    scinode restart
    """
    import os

    os.system("scinode stop")
    os.system("scinode start")


@scinode.command(help="Show the status of scinode.")
@click.pass_context
def status(ctx):
    """Show the status of scinode.
    - database
    - rabbitmq if needed
    - scheduler
    - workers

    Args:
        ctx (_type_): _description_
    """
    from scinode.database.client import get_db_status
    from scinode.utils.daemon import (
        inspect_daemon_status_celery,
        inspect_daemon_status_builtin,
    )
    from scinode.utils.formater import print_key_value, green, red
    import os

    db_active = get_db_status()
    if ctx.obj.activate_profile is not None and ctx.obj.activate_profile["celery"]:
        scheduler_activate = inspect_daemon_status_celery("scheduler@worker")
    else:
        scheduler_activate = inspect_daemon_status_builtin(
            "scheduler", sleep=2, daemon_type="scheduler"
        )
    if db_active:
        print_key_value("Database", green("Connected"))
    else:
        print_key_value("Database", red("Can not connect."))
    if scheduler_activate:
        print_key_value("Scheduler", green("running"))
    else:
        print_key_value("Scheduler", red("is not active."))
    print("-" * 30)
    if db_active:
        print("Workers: ")
        os.system("scinode worker status")
    else:
        print_key_value("Workers", red("Can not connect."))


def load_entry_point():
    for entry_point in pkg_resources.iter_entry_points("scinode_cli"):
        scinode.add_command(entry_point.load())


load_entry_point()

if __name__ == "__main__":
    scinode()
