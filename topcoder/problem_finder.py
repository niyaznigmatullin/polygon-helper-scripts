#!/usr/bin/env python3
"""
Problem Finder Script

This script queries an SQLite database to find a problem by name and retrieve
its associated solutions and test cases.

Usage:
    python3 problem_finder.py description --db <db-file> <problem-name>
    python3 problem_finder.py problem --db <db-file> <problem-name>
    python3 problem_finder.py short_description --db <db-file> <problem-name>
    python3 problem_finder.py convert --db <db-file> <problem-name>
"""

import argparse
import sys

# Import command handlers
from commands import (
    handle_description_command,
    handle_short_description_command,
    handle_problem_command,
    handle_convert_command
)


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Find problems in TopCoder database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 problem_finder.py description --db all/all.db CatRescue
  python3 problem_finder.py problem --db all/all.db CatRescue
  python3 problem_finder.py short_description --db all/all.db --api-key YOUR_API_KEY CatRescue
  python3 problem_finder.py short_description --db all/all.db CatRescue  # Uses OPENAI_API_KEY env var
  python3 problem_finder.py convert --db all/all.db --api-key YOUR_API_KEY CatRescue
  python3 problem_finder.py convert --db all/all.db CatRescue  # Uses OPENAI_API_KEY env var
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Description subcommand
    desc_parser = subparsers.add_parser('description', help='Show only problem description')
    desc_parser.add_argument('--db', required=True, help='Path to SQLite database file')
    desc_parser.add_argument('problem_name', help='Name of the problem to find')
    desc_parser.set_defaults(func=handle_description_command)

    # Problem subcommand
    prob_parser = subparsers.add_parser('problem', help='Show problem description, solutions, and test cases')
    prob_parser.add_argument('--db', required=True, help='Path to SQLite database file')
    prob_parser.add_argument('problem_name', help='Name of the problem to find')
    prob_parser.set_defaults(func=handle_problem_command)

    # Short description subcommand (GPT-4o explanation)
    short_desc_parser = subparsers.add_parser('short_description', help='Get GPT-4o formal explanation of problem with constraints')
    short_desc_parser.add_argument('--db', required=True, help='Path to SQLite database file')
    short_desc_parser.add_argument('--api-key', help='OpenAI API key (or set OPENAI_API_KEY environment variable)')
    short_desc_parser.add_argument('problem_name', help='Name of the problem to find')
    short_desc_parser.set_defaults(func=handle_short_description_command)

    # Convert subcommand (TopCoder to ICPC format conversion)
    convert_parser = subparsers.add_parser('convert', help='Convert TopCoder problem to ICPC format with LaTeX output')
    convert_parser.add_argument('--db', required=True, help='Path to SQLite database file')
    convert_parser.add_argument('--api-key', help='OpenAI API key (or set OPENAI_API_KEY environment variable)')
    convert_parser.add_argument('problem_name', help='Name of the problem to convert')
    convert_parser.set_defaults(func=handle_convert_command)

    args = parser.parse_args()

    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
