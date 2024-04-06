import logging
import subprocess

import click

from anthologist.helpers import check_projects_exist

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


@click.group()
@click.version_option()
def cli() -> None:
    pass


@cli.command()
@click.argument("dependency")
@click.option(
    "--version", type=str, default="", help="version constraint of the dependency"
)
@click.option(
    "--projects",
    type=str,
    required=True,
    multiple=True,
    help="paths to poetry-managed projects",
)
@click.option(
    "--group", "-G", type=str, required=False, help="the group to add the dependency to"
)
@click.option(
    "--optional",
    is_flag=True,
    default=False,
    required=False,
    help="add as an optional dependency",
)
@click.option(
    "--lock",
    is_flag=True,
    default=False,
    required=False,
    help="do not perform install (only update the lockfile)",
)
def add(
    dependency: str,
    version: str | None,
    projects: tuple[str],
    group: str | None = None,
    optional: bool = False,
    lock: bool = False,
) -> None:
    """
    Add a dependency to multiple projects
    """
    not_projects = check_projects_exist(list(projects))
    if not_projects:
        click.secho(
            f"The following projects do not exist: {not_projects}",
            err=True,
            fg="magenta",
        )
        return

    click.secho(
        f"\U0001f4d6 Anthologist trying to add {dependency} to the following projects:\n",
        fg="magenta",
    )
    for project in projects:
        click.secho(project, fg="magenta")
    click.secho("----------------", fg="magenta")

    dep = dependency
    if version:
        dep = f"{dependency}={version}"

    extra_args = []
    if group:
        extra_args += ["--group", group]
    if optional:
        extra_args += ["--optional"]
    if lock:
        extra_args += ["--lock"]

    with click.progressbar(
        projects, label=f"Adding {dep}", length=len(projects)
    ) as bar:
        for project in bar:
            click.secho(
                f"\nAnthologist adding {dependency} to {project}:", fg="magenta"
            )
            subprocess.run(["poetry", "add", dep, *extra_args], cwd=project, shell=True)


@cli.command()
@click.option(
    "--projects",
    type=str,
    required=True,
    multiple=True,
    help="paths to poetry-managed projects",
)
@click.option(
    "--lock",
    is_flag=True,
    default=False,
    required=False,
    help="do not perform install (only update the lockfile)",
)
@click.option(
    "--sync",
    is_flag=True,
    default=False,
    required=False,
    help="synchronize the environment with the locked packages",
)
def update(projects: tuple[str], lock: bool = False, sync: bool = False) -> None:
    """
    Update dependencies for multiple projects
    """
    not_projects = check_projects_exist(list(projects))
    if not_projects:
        click.secho(
            f"The following projects do not exist: {not_projects}",
            err=True,
            fg="magenta",
        )
        return

    click.secho(
        "\U0001f4d6 Anthologist trying to update dependencies for the following projects:\n",
        fg="magenta",
    )
    for project in projects:
        click.secho(project, fg="magenta")
    click.secho("----------------", fg="magenta")

    extra_args = []
    if lock:
        extra_args += ["--lock"]
    if sync:
        extra_args += ["--sync"]

    with click.progressbar(
        projects, label="Updating dependencies", length=len(projects)
    ) as bar:
        for project in bar:
            click.secho(
                f"\nAnthologist updating dependencies for {project}:", fg="magenta"
            )
            subprocess.run(["poetry", "update", *extra_args], cwd=project, shell=True)


@cli.command()
@click.argument("dependency")
@click.option(
    "--projects",
    type=str,
    required=True,
    multiple=True,
    help="paths to poetry-managed projects",
)
@click.option(
    "--group",
    "-G",
    type=str,
    required=False,
    help="the group to remove the dependency from",
)
@click.option(
    "--lock",
    is_flag=True,
    default=False,
    required=False,
    help="do not perform operations (only update the lockfile)",
)
def remove(
    dependency: str, projects: tuple[str], group: str | None = None, lock: bool = False
) -> None:
    """
    Remove a dependency from multiple projects
    """
    not_projects = check_projects_exist(list(projects))
    if not_projects:
        click.secho(
            f"The following projects do not exist: {not_projects}",
            err=True,
            fg="magenta",
        )
        return

    click.secho(
        f"\U0001f4d6 Anthologist trying to remove {dependency} from the following projects:\n",
        fg="magenta",
    )
    for project in projects:
        click.secho(project, fg="magenta")
    click.secho("----------------", fg="magenta")

    extra_args = []
    if group:
        extra_args += ["--group", group]
    if lock:
        extra_args += ["--lock"]

    with click.progressbar(
        projects, label=f"Removing {dependency}", length=len(projects)
    ) as bar:
        for project in bar:
            click.secho(
                f"\nAnthologist removing {dependency} from {project}:", fg="magenta"
            )
            subprocess.run(
                ["poetry", "remove", dependency, *extra_args], cwd=project, shell=True
            )


@cli.command()
@click.option(
    "--projects",
    type=str,
    required=True,
    multiple=True,
    help="paths to poetry-managed projects",
)
@click.option(
    "--no-update",
    default=False,
    is_flag=True,
    help="only refresh the lock file - do not update dependencies to latest available compatible versions",
)
def lock(projects: tuple[str], no_update: bool) -> None:
    """
    Lock dependencies for multiple projects
    """
    not_projects = check_projects_exist(list(projects))
    if not_projects:
        click.secho(
            f"The following projects do not exist: {not_projects}",
            err=True,
            fg="magenta",
        )
        return

    click.secho(
        "\U0001f4d6 Anthologist trying to lock dependencies for the following projects:\n",
        fg="magenta",
    )
    for project in projects:
        click.secho(project, fg="magenta")
    click.secho("----------------", fg="magenta")

    cmd = ["poetry", "lock"]
    if no_update:
        cmd.append("--no-update")
    with click.progressbar(
        projects, label="Locking dependencies", length=len(projects)
    ) as bar:
        for project in bar:
            click.secho(
                f"\nAnthologist locking dependencies for {project}:", fg="magenta"
            )
            subprocess.run(["poetry", "lock"], cwd=project, shell=True)
