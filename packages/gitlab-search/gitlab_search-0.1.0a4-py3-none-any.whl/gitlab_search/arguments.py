""""Define command line arguments."""

import argparse
import sys

from rich_argparse import RichHelpFormatter

from . import __version__


def parse_arguments():
    """Define and parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Search files of gitlab groups and projects for matching text.",
        epilog="To setup run this command without arguments.",
        formatter_class=RichHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + __version__
    )
    parser.add_argument(
        "search_term", nargs="*", help="Text to search for in project files"
    )
    parser.add_argument(
        "--show-details", action="store_true", help="Option to file snippets in result"
    )
    parser.add_argument(
        "--exclude-groups",
        action="store_true",
        help="Option to exclude groups of current user",
    )
    parser.add_argument(
        "--exclude-personal-projects",
        action="store_true",
        help="Option to exclude personal projects of current user",
    )
    parser.add_argument(
        "--show-projects-only",
        action="store_true",
        help="Option to only show the list of project which would be searched",
    )
    parser.add_argument(
        "--exclude-projects",
        nargs="+",
        help="Option to exclude projects specified by path with namespace",
    )
    parser.add_argument(
        "--require-extensions",
        nargs="+",
        help="Option to restrict matches to files with specified extensions",
    )
    parser.add_argument(
        "--include-users",
        nargs="+",
        help="Search public projects of others users, given by user IDs",
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Run setup to configure this app, e.g. the token",
    )

    if len(sys.argv) == 1:
        parser.print_usage()
        exit(0)

    return parser.parse_args()
