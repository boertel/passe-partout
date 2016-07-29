import sys
from functools import update_wrapper
import click
from . import __version__

from passepartout.strategies.github import GithubLocking


class Config(object):
    def __init__(self, verbose, token):
        self.verbose = verbose
        self.token = token

    def log(self, *args):
        if self.verbose:
            for arg in args:
                click.echo(arg)


def locking(f):
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        config = ctx.obj
        locking = GithubLocking(kwargs.pop('owner'),
                                kwargs.pop('repo'),
                                log=config.log,
                                token=config.token)
        return ctx.invoke(f, ctx, locking, *args, **kwargs)
    return update_wrapper(new_func, f)


def get_version(ctx, value):
    message = 'Passe-partout {version}\nPython {python_version}'
    click.echo(message.format(version=__version__, python_version=sys.version),
               color=ctx.color)
    ctx.exit()


@click.group()
@click.option('-v', '--verbose', count=True)
@click.option('--token', envvar='GITHUB_TOKEN')
@click.pass_context
def cli(ctx, verbose, token):
    ctx.obj = Config(verbose, token)


@cli.command()
@click.argument('owner')
@click.argument('repo')
@locking
def status(ctx, locking):
    message = 'locked' if locking.is_locked() else 'unlocked'
    click.echo(message)


@cli.command()
@click.argument('owner')
@click.argument('repo')
@locking
def lock(ctx, locking):
    message = 'locked' if locking.lock() else 'already locked'
    click.echo(message)


@cli.command()
@click.argument('owner')
@click.argument('repo')
@locking
def unlock(ctx, locking):
    message = 'unlocked' if locking.unlock() else 'already unlocked'
    click.echo(message)
