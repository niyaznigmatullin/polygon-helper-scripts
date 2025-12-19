#!/usr/bin/env python3
"""
Problem Command Handler

Handles the 'problem' subcommand to display complete problem information.
"""

import os
import sys
from common import DatabaseOperations, ProblemData


def handle_problem_command(args):
    """Handle the 'problem' subcommand"""
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
        result = db_ops.get_problem_data(args.problem_name)

        if result:
            display_results(result, include_description=True)
        else:
            print(f"Problem '{args.problem_name}' not found in the database.")
            print("\nTip: Problem names are case-insensitive. Try checking the exact spelling.")

            # Show some example problem names
            cursor = db_ops.connection.cursor()
            cursor.execute("SELECT name FROM problems LIMIT 10")
            examples = [row[0] for row in cursor.fetchall()]
            print(f"\nSome example problem names:")
            for example in examples:
                print(f"  - {example}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    finally:
        db_ops.close()


def display_results(result: ProblemData, include_description: bool = True) -> None:
    """Display the search results in a user-friendly format"""
    print(f"\n{'='*60}")
    print(f"PROBLEM FOUND: {result.problem.name}")
    print(f"{'='*60}")

    print(f"\nProblem Details:")
    print(f"  ID: {result.problem.problem_id}")
    print(f"  Name: {result.problem.name}")
    print(f"  Created: {result.problem.create_date}")
    print(f"  Modified: {result.problem.modify_date}")
    print(f"  Status ID: {result.problem.status_id}")
    print(f"  Problem Type ID: {result.problem.problem_type_id}")

    if result.problem.problem_text:
        print(f"\nProblem Text:")
        # Truncate long problem text for display
        text = result.problem.problem_text
        if len(text) > 500:
            text = text[:500] + "..."
        print(f"  {text}")

    # Add problem description if requested
    if include_description and result.problem_statement:
        print(f"\nPROBLEM DESCRIPTION:")
        print(f"{'-'*20}")
        print(result.problem_statement)

    print(f"\nComponents ({len(result.components)}):")
    for i, component in enumerate(result.components, 1):
        print(f"  {i}. Component ID: {component.component_id}")
        print(f"     Class Name: {component.class_name}")
        print(f"     Method Name: {component.method_name}")
        print(f"     Points: {component.points}")
        print(f"     Difficulty ID: {component.difficulty_id}")

    print(f"\nSolutions ({len(result.solutions)}):")
    for i, solution in enumerate(result.solutions, 1):
        print(f"  {i}. Solution ID: {solution.solution_id}")
        print(f"     Coder ID: {solution.coder_id}")
        print(f"     Language ID: {solution.language_id}")
        print(f"     Modified: {solution.modify_date}")
        print(f"     Primary: {solution.primary_solution}")

        # Show first few lines of solution code
        if solution.solution_text:
            lines = solution.solution_text.split('\n')
            print(f"     Code Preview:")
            for line in lines:
                print(f"       {line}")
        print()

    print(f"Test Cases ({len(result.test_cases)}):")
