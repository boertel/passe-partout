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
        owner = kwargs.pop('owner')
        repo = kwargs.pop('repo')
        if repo is None:
            splitted = owner.split('/')
            owner = splitted[0]
            repo = splitted[1]
        locking = GithubLocking(owner,
                                repo,
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
@click.option('--token', envvar=('PASSEPARTOUT_GITHUB_TOKEN', 'GITHUB_TOKEN',))
@click.pass_context
def cli(ctx, verbose, token):
    if not token:
        click.echo('no github token found.', err=True)
        sys.exit(1)
    ctx.obj = Config(verbose, token)


@cli.command()
@click.argument('owner')
@click.argument('repo', required=False)
@locking
def status(ctx, locking):
    message = 'locked' if locking.is_locked() else 'unlocked'
    click.echo(message)


@cli.command()
@click.argument('owner')
@click.argument('repo', required=False)
@click.option('-r', '--reason', required=False)
@locking
def lock(ctx, locking, reason):
    message = 'locked' if locking.lock(reason) else 'already locked'
    click.echo(message)


@cli.command()
@click.argument('owner')
@click.argument('repo', required=False)
@locking
def unlock(ctx, locking):
    message = 'unlocked' if locking.unlock() else 'already unlocked'
    click.echo(message)
