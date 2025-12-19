#!/usr/bin/env python3
"""
Short Description Command Handler

Handles the 'short_description' subcommand to get GPT-4o formal explanation of problems.
"""

import os
import sys
from common import DatabaseOperations, LLMHelper


def handle_short_description_command(args):
    """Handle the 'short_description' subcommand"""
    # Check if database file exists
    if not os.path.exists(args.db):
        print(f"Error: Database file '{args.db}' not found")
        sys.exit(1)

    # Check if API key is provided
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OpenAI API key is required. Provide it via --api-key argument or OPENAI_API_KEY environment variable")
        sys.exit(1)

    # Create LLM helper
    llm_helper = LLMHelper(api_key, os.getenv('OPENAI_BASE_URL'))

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

        if not problem_data.problem_statement:
            print(f"No description found for problem '{args.problem_name}'")
            return

        print(f"\n{'='*60}")
        print(f"PROBLEM: {problem_data.problem.name}")
        print(f"{'='*60}")

        print(f"\nOriginal Description:")
        print(f"{'-'*20}")
        print(problem_data.problem_statement)

        print(f"\n{'='*60}")
        print(f"GPT-4o FORMAL EXPLANATION:")
        print(f"{'='*60}")

        # Get GPT-4o explanation
        print("Requesting formal explanation from GPT-4o...")
        gpt_explanation = get_gpt4o_explanation(
            problem_data.problem_statement,
            problem_data.problem.name,
            llm_helper
        )

        if gpt_explanation:
            print(gpt_explanation)
        else:
            print("Failed to get explanation from GPT-4o")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    finally:
        db_ops.close()


def get_gpt4o_explanation(problem_description: str, problem_name: str, llm_helper: LLMHelper) -> str:
    """Get GPT-4o explanation of the problem with constraints"""
    prompt = f"""
You are a competitive programming expert. Please analyze the following TopCoder problem and provide a formal explanation that includes:

1. A clear problem statement summary
2. All input constraints and limitations
3. Output format requirements
4. Key algorithmic insights or approaches
5. Time/space complexity considerations if relevant

Problem Name: {problem_name}

Problem Description:
{problem_description}

Please provide a structured, formal explanation that would help a competitive programmer understand exactly what needs to be solved and what the constraints are.
"""
    return llm_helper.ask_llm(
        "You are a competitive programming expert who explains problems clearly and formally.",
        [prompt]
    )
