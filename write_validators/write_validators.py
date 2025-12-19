#!/usr/bin/env python3
"""
Script to automatically generate and add validators to Polygon problems in a contest.

This script:
1. Takes a contest ID as input
2. Gets all problems from that contest that don't have validators
3. For each problem, gets the problem statement and uses OpenAI to generate a C++ validator
4. Adds the generated validator to the problem

Requirements:
- polygon_api library
- openai library
- API credentials for Polygon
"""

import argparse
import os
import sys
from typing import Dict, List, Optional
import logging

try:
    from polygon_api import Polygon, Problem, FileType
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


class ValidatorGenerator:
    """Handles the generation of validators using OpenAI."""

    def __init__(self, model: str = "gpt-4", polygon_api=None):
        self.model = model
        self.api = polygon_api

        # Initialize OpenAI client
        api_key = os.environ.get('OPENAI_API_KEY')
        base_url = os.environ.get('OPENAI_BASE_URL')

        if base_url:
            self.client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            self.client = OpenAI(api_key=api_key)
    
    def get_first_test_case(self, problem_id: int) -> Optional[Dict[str, str]]:
        """
        Get the first test case (input and output) for a problem.
        
        Args:
            problem_id: The problem ID
            
        Returns:
            Dictionary with 'input' and 'output' keys, or None if not available
        """
        if not self.api:
            return None
            
        try:
            # Try different testset names
            for testset in ['tests', 'samples']:
                try:
                    # Get input
                    test_input = self.api.problem_test_input(problem_id, testset, 1)
                    
                    return {
                        'input': test_input.strip() if test_input else '',
                    }
                except Exception as e:
                    logger.debug(f"Could not get tests from testset '{testset}': {e}")
                    continue
                    
            return None
            
        except Exception as e:
            logger.warning(f"Error getting test case for problem {problem_id}: {e}")
            return None

    def ask_llm(self, prompt):
        try:
            print(prompt)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=1  # Low temperature for consistent code generation
            )
            print(len(response.choices))
            for c in response.choices:
                print("=====================================")
                print(c.message.content)

            validator_code = response.choices[0].message.content.strip()

            # Clean up any markdown formatting that might have been added
            if validator_code.startswith("```cpp"):
                validator_code = validator_code[6:]
            if validator_code.startswith("```"):
                validator_code = validator_code[3:]
            if validator_code.endswith("```"):
                validator_code = validator_code[:-3]

            return validator_code.strip()

        except Exception as e:
            logger.error(f"Error generating validator: {e}")
            raise

    def generate_validator(self, problem_statement: str, test_case: str, problem_name: str, problem_id: int = None) -> str:
        """
        Generate a C++ validator using testlib.h based on the problem statement.
        
        Args:
            problem_statement: The problem statement text
            problem_name: Name of the problem for context
            problem_id: Problem ID for getting test cases
            
        Returns:
            Generated C++ validator code
        """
        
        # Build the prompt with optional test case information
        prompt_parts = [
            "You are an expert competitive programming judge. Generate a C++ validator using testlib.h for the following problem.",
            "Detect the type of problem ICPC or IOI, according to the problem statement whether there subtasks and scoring mentioned.",
            f"\nProblem Name: {problem_name}",
            f"\nProblem Statement:\n{problem_statement}"
        ]
        
        if test_case:
            prompt_parts.extend([
                f"\nExample Test Case:",
                f"Input:\n{test_case['input']}",
            ])
        
        prompt_parts.extend([
            "\nRequirements:",
            "1. Use #include \"testlib.h\" at the top",
            "2. Use registerValidation(argc, argv) in main function",
            "3. Validate all input constraints mentioned in the problem",
            "4. Use appropriate testlib functions like inf.readInt(), inf.readSpace(), inf.readEoln(), etc.",
            "5. Ensure the validator checks all bounds and format requirements",
            "6. End with inf.readEof() to ensure no extra input",
            "7. Use ensuref() for constraint validation with descriptive error messages",
            "8. Don't forget to #include the standard libraries used",
            "9. Don't forget to use constants like 1'000'000 instead of 1000000",
            "10. For IOI type problems use `validator.group()` to get `std::string` denoting a group of the current validated test. The group names are always a number with no leading zeros, i.e. \"1\", \"2\", ..., \"10\"",
            "11. If the problem has test cases `setTestCase` has to be called",
            "",
            "Generate only the C++ code without any explanations or markdown formatting."
        ])

        prompt = "\n".join(prompt_parts)

        return self.ask_llm(prompt)

    def fix_validator(self, problem_statement: str, test_case: str, problem_name: str, validator_code: str, error: str) -> str:
        prompt_parts = [
            "You are an expert competitive programming judge. Fix a C++ validator for the following problem.",
            f"\nProblem Name: {problem_name}",
            f"\nProblem Statement:\n{problem_statement}"
        ]
        if test_case:
            prompt_parts.extend([
                f"\nExample Test Case:",
                f"Input:\n{test_case['input']}",
            ])
        prompt_parts.append(f"Validator code:\n{validator_code}")
        prompt_parts.append(f"Error: \n{error}")
        prompt_parts.append("Generate only the C++ code without any explanations or markdown formatting.")
        return self.ask_llm("\n".join(prompt_parts))

class PolygonValidatorWriter:
    """Main class for writing validators to Polygon problems."""
    
    def __init__(self, api_url: str, api_key: str, api_secret: str, model: str = "gpt-4"):
        """
        Initialize the validator writer.

        Args:
            api_url: Polygon API URL
            api_key: Polygon API key
            api_secret: Polygon API secret
            model: OpenAI model to use for generation
        """
        self.api = Polygon(api_url, api_key, api_secret)
        self.generator = ValidatorGenerator(model, self.api)
    
    def get_contest_problems(self, contest_id: int) -> Dict[str, Problem]:
        """Get all problems in a contest."""
        try:
            return self.api.contest_problems(contest_id)
        except Exception as e:
            logger.error(f"Error getting contest problems: {e}")
            raise
    
    def has_validator(self, problem: Problem) -> bool:
        """Check if a problem already has a validator."""
        try:
            validator = self.api.problem_validator(problem.id)
            return validator is not None and validator.strip() != ""
        except Exception as e:
            # If there's an error getting the validator, assume it doesn't exist
            logger.warning(f"Could not check validator for problem {problem.name}: {e}")
            return False
    
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
                if hasattr(statement,'scoring') and statement.scoring:
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
    
    def add_validator_to_problem(self, problem: Problem, validator_code: str) -> bool:
        """
        Add a validator to a problem.
        
        Args:
            problem: The problem to add validator to
            validator_code: The C++ validator code
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Update working copy first
            self.api.problem_update_working_copy(problem.id)
            
            # Save the validator file
            validator_filename = "validator.cpp"
            self.api.problem_save_file(
                problem_id=problem.id,
                type=FileType.SOURCE,
                name=validator_filename,
                file=validator_code.encode('utf-8'),
            )
            
            # Set the validator
            self.api.problem_set_validator(problem.id, validator_filename)
            
            # Commit changes
            self.api.problem_commit_changes(
                problem.id,
                minor_changes=True,
                message="Added auto-generated validator"
            )
            
            logger.info(f"Successfully added validator to problem {problem.name}")
            return True, ""
            
        except Exception as e:
            logger.error(f"Error adding validator to problem {problem.name}: {e}")
            return False, str(e)
    
    def process_contest(self, contest_id: int, dry_run: bool = False) -> None:
        """
        Process all problems in a contest and add validators where needed.
        
        Args:
            contest_id: The contest ID to process
            dry_run: If True, only show what would be done without making changes
        """
        logger.info(f"Processing contest {contest_id}")
        
        # Get all problems in the contest
        try:
            problems = self.get_contest_problems(contest_id)
            logger.info(f"Found {len(problems)} problems in contest")
        except Exception as e:
            logger.error(f"Failed to get contest problems: {e}")
            return
        
        problems_without_validators = []
        
        # Check which problems need validators
        for name, problem in problems.items():
            logger.info(f"Checking problem: {problem.name} (ID: {problem.id})")
            
            if self.has_validator(problem):
                logger.info(f"  ✓ Already has validator")
            else:
                logger.info(f"  ✗ No validator found")
                problems_without_validators.append(problem)
        
        if not problems_without_validators:
            logger.info("All problems already have validators!")
            return
        
        logger.info(f"Found {len(problems_without_validators)} problems without validators")
        
        if dry_run:
            logger.info("DRY RUN - Would process the following problems:")
            for problem in problems_without_validators:
                logger.info(f"  - {problem.name} (ID: {problem.id})")
            return
        
        # Process each problem without a validator
        success_count = 0
        for problem in problems_without_validators:
            logger.info(f"Processing problem: {problem.name}")
            
            try:
                # Get problem statement
                statement = self.get_problem_statement(problem)
                logger.info(f"  Got problem statement ({len(statement)} characters)")
                
                # Try to get first test case for better format understanding
                test_case = self.generator.get_first_test_case(problem.id)
                if test_case:
                    logger.info("  Retrieved first test case for format understanding")
                else:
                    logger.info("  No test case available, proceeding with statement only")


                # Generate validator
                logger.info("  Generating validator...")
                validator_code = self.generator.generate_validator(statement, test_case, problem.name, problem.id)
                logger.info(f"  Generated validator ({len(validator_code)} characters)")
                
                RETRIES = 5
                for retry in range(5):
                    # Add validator to problem
                    success, error = self.add_validator_to_problem(problem, validator_code)
                    if success:
                        success_count += 1
                        logger.info(f"  ✓ Successfully added validator")
                        break
                    else:
                        logger.error(f"  ✗ Failed to add validator")
                        logger.info(f"  Regenerating validator {retry + 1}/{RETRIES - 1}")
                        validator_code = self.generator.fix_validator(statement, test_case, problem.name, validator_code, error)
                if not success:
                    logger.info(f"  ✗ Failed to add validator in {RETRIES} tries")
                    
            except Exception as e:
                logger.error(f"  ✗ Error processing problem {problem.name}: {e}")
        
        logger.info(f"Completed processing. Successfully added validators to {success_count}/{len(problems_without_validators)} problems")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate and add validators to Polygon contest problems")
    parser.add_argument("contest_id", type=int, help="Contest ID to process")
    parser.add_argument("--api-url", default="https://polygon.codeforces.com/api", 
                       help="Polygon API URL")
    parser.add_argument("--api-key", help="Polygon API key (or set POLYGON_API_KEY env var)")
    parser.add_argument("--api-secret", help="Polygon API secret (or set POLYGON_API_SECRET env var)")
    parser.add_argument("--model", default="gpt-4", help="OpenAI model to use")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Show what would be done without making changes")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Get API credentials
    api_key = args.api_key or os.getenv("POLYGON_API_KEY")
    api_secret = args.api_secret or os.getenv("POLYGON_API_SECRET")
    
    if not api_key or not api_secret:
        logger.error("API key and secret are required. Provide via --api-key/--api-secret or POLYGON_API_KEY/POLYGON_API_SECRET environment variables")
        sys.exit(1)
    
    try:
        # Initialize the validator writer
        writer = PolygonValidatorWriter(args.api_url, api_key, api_secret, args.model)
        
        # Process the contest
        writer.process_contest(args.contest_id, args.dry_run)
        
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()