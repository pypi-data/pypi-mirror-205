from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import gitlab
from gitlab.const import SearchScope
from gitlab.exceptions import GitlabSearchError
from rich import print
from rich.progress import track

from .arguments import parse_arguments
from .config import Config


@dataclass
class SearchMatch:
    """A match of the search term in a file."""

    project_path: str
    file_path: str
    start_line: str
    ref: str
    data: str

    @property
    def sort_key(self) -> str:
        return f"{self.project_path}-{self.file_path}-{self.start_line:09d}"

    def gitlab_link(self, gitlab_url: str) -> str:
        return (
            f"{gitlab_url}/{self.project_path}/-/blob/"
            f"{self.ref}/{self.file_path}#L{self.start_line}"
        )

    @classmethod
    def from_search_item(cls, project, item):
        return cls(
            project_path=project.path_with_namespace,
            file_path=item["path"],
            start_line=item["startline"],
            ref=item["ref"],
            data=item["data"],
        )


def main():
    args = parse_arguments()
    config = Config.load()

    if args.setup:
        _run_setup(config)
        exit(0)

    elif not config.is_valid():
        print("No valid configuration found. Need to run setup.")
        _run_setup(config)

    if not config.is_valid():
        raise RuntimeError("Invalid configuration. Can not proceed.")

    gl = _connect_gitlab(config)

    projects = _fetch_projects(args, gl)
    if not projects:
        print("No projects found. Aborting.")
        exit(1)

    if args.show_projects_only:
        names = [p.path_with_namespace for p in projects]
        print(f"The following {len(names)} projects would searched:")
        for name in sorted(names):
            print(name)
        exit(0)

    for num, search_term in enumerate(args.search_term, start=1):
        print()
        matches = _search_projects(
            args, gl, projects, search_term, num, len(args.search_term)
        )
        _show_search_results(args, matches, config)


def _run_setup(config):
    """Request setup information from user and store them."""
    print("Setting up gitlab-search")
    try:
        while True:
            config.token = _input_with_default(
                "Please enter the GitLab token", config.token
            )
            if config.token:
                break
        config.url = _input_with_default("Please enter the GitLab URL", config.url)
    except KeyboardInterrupt:
        print()
        exit(1)
    path = config.save()
    print(f"Setup complete. Config stored at {path}")


def _input_with_default(question, default: Optional[str] = None) -> Optional[str]:
    response = input(f"{question} [{default if default else ''}]: ")
    return response or default


def _connect_gitlab(config) -> gitlab.Gitlab:
    print(f"Connecting to {config.url}...")
    gl = gitlab.Gitlab(config.url, private_token=config.token)
    gl.auth()
    username = gl.user.username if gl.user else "?"
    print(f"Connected as {username}")
    return gl


def _fetch_projects(args, gl):
    """Fetch projects to search in."""
    projects = []
    exclude_projects = set(args.exclude_projects) if args.exclude_projects else set()
    projects += _fetch_group_projects(args, gl, exclude_projects)
    projects += _fetch_user_projects(args, gl, exclude_projects)
    return projects


def _fetch_group_projects(args, gl, exclude_projects):
    projects = []
    if not args.exclude_groups:
        print(f"Fetching group projects from {gl.user.username}...")
        for group in gl.groups.list(order_by="name", sort="asc", iterator=True):
            for project in group.projects.list(
                order_by="name", sort="asc", iterator=True
            ):
                if (
                    not exclude_projects
                    or project.path_with_namespace not in exclude_projects
                ):
                    projects.append(project)
    return projects


def _fetch_user_projects(args, gl, exclude_projects):
    projects = []
    users = _determine_users(args, gl)
    for user in users:
        print(f"Fetching personal projects from {user.username}...")
        for project in user.projects.list(
            owned=True, order_by="name", sort="asc", iterator=True
        ):
            if (
                not exclude_projects
                or project.path_with_namespace not in exclude_projects
            ):
                projects.append(project)
    return projects


def _determine_users(args, gl):
    users = []
    if not args.exclude_personal_projects:
        user = gl.users.get(id=gl.user.id)
        users.append(user)
    if args.include_users:
        for user_id in args.include_users:
            user = gl.users.get(id=user_id)
            users.append(user)
    return users


def _search_projects(args, gl, projects, search_term, num, total):
    """Search files in projects."""
    if total > 1:
        search_text = f"{search_term} ({num}/{total})"
    else:
        search_text = search_term
    matches = []
    print(f"Searching {len(projects)} projects for: {search_text}")
    require_extensions = (
        set(args.require_extensions) if args.require_extensions else set()
    )
    for project in track(projects, description=search_text):
        project = gl.projects.get(id=project.id)
        for _ in range(2):
            new_matches = []
            try:
                for item in project.search(
                    SearchScope.BLOBS, search_term, iterator=True
                ):
                    item_suffix = Path(item["path"]).suffix[1:]
                    if not require_extensions or item_suffix in require_extensions:
                        new_matches.append(SearchMatch.from_search_item(project, item))
            except GitlabSearchError:
                pass
            else:
                matches += new_matches
                break
        else:
            print(f"ERROR: Failed to search project {project.path_with_namespace}")
    return matches


def _show_search_results(args, matches, config):
    """Show search results."""
    if not len(matches):
        print("Found no matches.")
        return

    print(f"Found {len(matches)} matches:")
    for detail in sorted(matches, key=lambda o: o.sort_key):
        print(detail.gitlab_link(config.url))
        if args.show_details:
            print(detail.data)
            print("---")


if __name__ == "__main__":
    main()
