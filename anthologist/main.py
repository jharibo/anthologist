import logging
import subprocess

import click

from anthologist.helpers import check_projects_exist

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")


@click.group()
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
def add(dependency: str, version: str | None, projects: tuple[str]) -> None:
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

    with click.progressbar(
        projects, label=f"Adding {dep}", length=len(projects)
    ) as bar:
        for project in bar:
            click.secho(
                f"\nAnthologist adding {dependency} to {project}:", fg="magenta"
            )
            subprocess.run(["poetry", "add", dep], cwd=project, shell=True)


@cli.command()
@click.option(
    "--projects",
    type=str,
    required=True,
    multiple=True,
    help="paths to poetry-managed projects",
)
def update(projects: tuple[str]) -> None:
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

    with click.progressbar(
        projects, label="Updating dependencies", length=len(projects)
    ) as bar:
        for project in bar:
            click.secho(
                f"\nAnthologist updating dependencies for {project}:", fg="magenta"
            )
            subprocess.run(["poetry", "update"], cwd=project, shell=True)


@cli.command()
@click.argument("dependency")
@click.option(
    "--projects",
    type=str,
    required=True,
    multiple=True,
    help="paths to poetry-managed projects",
)
def remove(dependency: str, projects: tuple[str]) -> None:
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

    with click.progressbar(
        projects, label=f"Removing {dependency}", length=len(projects)
    ) as bar:
        for project in bar:
            click.secho(
                f"\nAnthologist removing {dependency} from {project}:", fg="magenta"
            )
            subprocess.run(["poetry", "remove", dependency], cwd=project, shell=True)


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


if __name__ == "__main__":
    cli()
