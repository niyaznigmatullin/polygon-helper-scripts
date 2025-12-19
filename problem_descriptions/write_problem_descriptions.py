#!/usr/bin/env python3
"""
Script to automatically generate formal problem descriptions for Polygon problems.

This script:
1. Takes a list of contest IDs as input
2. Gets all problems from those contests
3. For each problem, gets the problem statement and uses OpenAI API to generate a formal description
4. Outputs all problem descriptions to a CSV file

Requirements:
- polygon_api library
- openai library
- API credentials for Polygon and OpenAI
"""

import argparse
import csv
import os
import sys
from typing import Dict, List
import logging

try:
    from polygon_api import Polygon, Problem
except ImportError:
    print("Error: polygon_api library not found. Install with: pip install polygon_api")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("Error: openai library not found. Install with: pip install openai")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class DescriptionGenerator:
    """Handles the generation of problem descriptions using OpenAI API."""

    def __init__(self, model: str = "gpt-4", api_key: str = None, base_url: str = None, language: str = "English"):
        self.model = model
        self.language = language
        client_kwargs = {"api_key": api_key or os.environ.get('OPENAI_API_KEY')}
        if base_url:
            client_kwargs["base_url"] = base_url
        self.client = OpenAI(**client_kwargs)

    def ask_llm(self, prompt: str) -> str:
        """Send a prompt to the LLM and get a response."""
        try:
            logger.debug(f"Sending prompt to LLM (length: {len(prompt)} chars)")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )

            description = response.choices[0].message.content.strip()
            logger.debug(f"Received response from LLM (length: {len(description)} chars)")

            return description

        except Exception as e:
            logger.error(f"Error generating description: {e}")
            raise

    def generate_description(self, problem_statement: str, problem_name: str) -> str:
        """
        Generate a formal 3-sentence problem description.

        Args:
            problem_statement: The full problem statement text
            problem_name: Name of the problem for context

        Returns:
            Generated formal description (3 sentences)
        """

        prompt = f"""You are an expert in competitive programming. Given the following problem statement, write a short formal description of the problem in exactly three sentences in {self.language}.

Problem Name: {problem_name}

Problem Statement:
{problem_statement}

Requirements:
1. Write exactly THREE sentences in {self.language}
2. The description should be formal and concise
3. Include the most important details about what needs to be solved
4. Include key constraints at the end (e.g., array size limits, value ranges, time/memory limits if mentioned)
5. Do not include example inputs/outputs
6. Focus on the core problem, not implementation details
7. Use mathematical or technical terminology where appropriate

Generate only the three-sentence description in {self.language} without any additional text, explanations, or formatting."""

        return self.ask_llm(prompt)


class ProblemDescriptionWriter:
    """Main class for generating problem descriptions."""

    def __init__(self, api_url: str, api_key: str, api_secret: str, model: str = "gpt-4",
                 openai_api_key: str = None, openai_base_url: str = None, language: str = "English"):
        """
        Initialize the description writer.

        Args:
            api_url: Polygon API URL
            api_key: Polygon API key
            api_secret: Polygon API secret
            model: OpenAI model to use for generation
            openai_api_key: OpenAI API key (optional, will use env var if not provided)
            openai_base_url: OpenAI API base URL (optional, for custom deployments)
            language: Language for generated descriptions (default: English)
        """
        self.api = Polygon(api_url, api_key, api_secret)
        self.generator = DescriptionGenerator(model, openai_api_key, openai_base_url, language)

    def get_contest_problems(self, contest_id: int) -> Dict[str, Problem]:
        """Get all problems in a contest."""
        try:
            return self.api.contest_problems(contest_id)
        except Exception as e:
            logger.error(f"Error getting contest problems for contest {contest_id}: {e}")
            raise

    def get_problem_statement(self, problem: Problem) -> str:
        """Get the problem statement text."""
        try:
            statements = self.api.problem_statements(problem.id)

            def collect_statement(statement):
                parts = []
                if hasattr(statement, 'legend') and statement.legend:
                    parts.append(f"Legend: {statement.legend}")
                if hasattr(statement, 'input') and statement.input:
                    parts.append(f"Input: {statement.input}")
                if hasattr(statement, 'scoring') and statement.scoring:
                    parts.append(f"Scoring: {statement.scoring}")
                if hasattr(statement, 'output') and statement.output:
                    parts.append(f"Output: {statement.output}")
                if hasattr(statement, 'notes') and statement.notes:
                    parts.append(f"Notes: {statement.notes}")
                return "\n\n".join(parts)

            # Try to get English statement first, then any available language
            for lang in ['english', 'en']:
                if lang in statements:
                    return collect_statement(statements[lang])

            # If no English statement, use the first available
            if statements:
                first_lang = next(iter(statements))
                logger.warning(f"Using {first_lang} statement for problem {problem.name}")
                return collect_statement(statements[first_lang])

            raise ValueError("No statements found")

        except Exception as e:
            logger.error(f"Error getting statement for problem {problem.name}: {e}")
            raise

    def process_contests(self, contest_ids: List[int], output_file: str) -> None:
        """
        Process all problems in the given contests and generate descriptions.

        Args:
            contest_ids: List of contest IDs to process
            output_file: Path to output CSV file
        """
        logger.info(f"Processing {len(contest_ids)} contest(s)")

        all_descriptions = []

        for contest_id in contest_ids:
            logger.info(f"Processing contest {contest_id}")

            try:
                problems = self.get_contest_problems(contest_id)
                logger.info(f"  Found {len(problems)} problems in contest")
            except Exception as e:
                logger.error(f"  Failed to get contest problems: {e}")
                continue

            for name, problem in problems.items():
                logger.info(f"  Processing problem: {problem.name} (ID: {problem.id})")

                try:
                    # Get problem statement
                    statement = self.get_problem_statement(problem)
                    logger.info(f"    Got problem statement ({len(statement)} characters)")

                    # Generate description
                    logger.info("    Generating description...")
                    description = self.generator.generate_description(statement, problem.name)
                    logger.info(f"    Generated description ({len(description)} characters)")
                    logger.info(f" Description: \n {description}")

                    all_descriptions.append({
                        'contest_id': contest_id,
                        'problem_id': problem.id,
                        'problem_name': problem.name,
                        'description': description
                    })

                    logger.info(f"    ✓ Successfully generated description")

                except Exception as e:
                    logger.error(f"    ✗ Error processing problem {problem.name}: {e}")

        # Write to CSV
        if all_descriptions:
            logger.info(f"Writing {len(all_descriptions)} descriptions to {output_file}")
            try:
                with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['contest_id', 'problem_id', 'problem_name', 'description']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for desc in all_descriptions:
                        writer.writerow(desc)

                logger.info(f"✓ Successfully wrote descriptions to {output_file}")
            except Exception as e:
                logger.error(f"✗ Error writing CSV file: {e}")
                raise
        else:
            logger.warning("No descriptions were generated")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate formal problem descriptions for Polygon contest problems"
    )
    parser.add_argument(
        "contest_ids",
        type=int,
        nargs='+',
        help="Contest ID(s) to process (space-separated)"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="problem_descriptions.csv",
        help="Output CSV file path (default: problem_descriptions.csv)"
    )
    parser.add_argument(
        "--api-url",
        default="https://polygon.codeforces.com/api",
        help="Polygon API URL"
    )
    parser.add_argument(
        "--api-key",
        help="Polygon API key (or set POLYGON_API_KEY env var)"
    )
    parser.add_argument(
        "--api-secret",
        help="Polygon API secret (or set POLYGON_API_SECRET env var)"
    )
    parser.add_argument(
        "--model",
        default="gpt-4",
        help="OpenAI model to use (default: gpt-4)"
    )
    parser.add_argument(
        "--openai-api-key",
        help="OpenAI API key (or set OPENAI_API_KEY env var)"
    )
    parser.add_argument(
        "--openai-base-url",
        help="OpenAI API base URL (or set OPENAI_BASE_URL env var) - for custom deployments"
    )
    parser.add_argument(
        "--language",
        "-l",
        default="English",
        help="Language for generated descriptions (default: English)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Get API credentials
    api_key = args.api_key or os.getenv("POLYGON_API_KEY")
    api_secret = args.api_secret or os.getenv("POLYGON_API_SECRET")
    openai_api_key = args.openai_api_key or os.getenv("OPENAI_API_KEY")
    openai_base_url = args.openai_base_url or os.getenv("OPENAI_BASE_URL")

    if not api_key or not api_secret:
        logger.error(
            "API key and secret are required. Provide via --api-key/--api-secret "
            "or POLYGON_API_KEY/POLYGON_API_SECRET environment variables"
        )
        sys.exit(1)

    if not openai_api_key:
        logger.error(
            "OpenAI API key is required. Provide via --openai-api-key "
            "or OPENAI_API_KEY environment variable"
        )
        sys.exit(1)

    try:
        # Initialize the description writer
        writer = ProblemDescriptionWriter(args.api_url, api_key, api_secret, args.model,
                                         openai_api_key, openai_base_url, args.language)

        # Process the contests
        writer.process_contests(args.contest_ids, args.output)

    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
