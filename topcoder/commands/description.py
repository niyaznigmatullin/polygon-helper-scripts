#!/usr/bin/env python3
"""
Description Command Handler

Handles the 'description' subcommand to display problem descriptions.
"""

import os
import sys
from common import DatabaseOperations


def handle_description_command(args):
    """Handle the 'description' subcommand"""
    # Check if database file exists
    if not os.path.exists(args.db):
        print(f"Error: Database file '{args.db}' not found")
        sys.exit(1)

    # Create database operations
    db_ops = DatabaseOperations(args.db)

    try:
        db_ops.connect()
        print(f"Searching for problem: '{args.problem_name}'...")

        # Get problem data
        problem_data = db_ops.get_problem_data(args.problem_name)

        if not problem_data:
            print(f"Problem '{args.problem_name}' not found in the database.")
            print("\nTip: Problem names are case-insensitive. Try checking the exact spelling.")

            # Show some example problem names
            cursor = db_ops.connection.cursor()
            cursor.execute("SELECT name FROM problems LIMIT 10")
            examples = [row[0] for row in cursor.fetchall()]
            print(f"\nSome example problem names:")
            for example in examples:
                print(f"  - {example}")
            return

        print(f"\n{'='*60}")
        print(f"PROBLEM: {problem_data.problem.name}")
        print(f"{'='*60}")
        print(f"Problem ID: {problem_data.problem.problem_id}")

        if problem_data.problem_statement:
            print(f"\nPROBLEM DESCRIPTION:")
            print(f"{'-'*20}")
            print(problem_data.problem_statement)
        else:
            print("\nNo problem description available for this problem.")

        print(f"\n{'='*60}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    finally:
        db_ops.close()
