import os


def check_is_directory(path: str) -> bool:
    return os.path.isdir(path)


def check_projects_exist(projects: list[str]) -> list[str] | None:
    """
    Check that each project exists (is a directory). Return list of
    projects that don't exist (or None if they all exist).
    """
    # TODO: Check that projects are Poetry projects
    not_directories = []
    for project in projects:
        if not check_is_directory(project):
            not_directories.append(project)

    return not_directories or None
