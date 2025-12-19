#!/usr/bin/env python3
"""
Convert Command Handler

Handles the 'convert' subcommand to convert TopCoder problems to ICPC format.
"""

import os
import sys
import re
import subprocess
from typing import List, Dict, Optional

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common import DatabaseOperations, LLMHelper, decode_java_object
from all.entities import System_test_case


def handle_convert_command(args):
    """Handle the 'convert' subcommand"""
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
        print(f"Converting problem: '{args.problem_name}' from TopCoder to ICPC format...")

        # Get all problem data in one call
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

        xml_description = problem_data.problem_statement + f"\nExplanations:" + "\n".join(f"  Example #{i + 1}: {s.annotation}" for i, s in enumerate(problem_data.sample_cases) if s.annotation != "")

        if problem_data.sample_cases[0].case_id == '':
            is_sample_case = None
        else:
            is_sample_case = { int(s.case_id) : i for i, s in enumerate(problem_data.sample_cases) }

        if not xml_description:
            print(f"No XML description found for problem '{args.problem_name}'")
            return

        print(f"Found problem: {problem_data.problem.name}")
        print(f"Problem ID: {problem_data.problem.problem_id}")

        # Create directory with problem name in lowercase
        problem_dir = problem_data.problem.name.lower().replace(' ', '_')
        if not os.path.exists(problem_dir):
            os.makedirs(problem_dir)
            print(f"Created directory: {problem_dir}")

        # Step 1: Process test cases from problem_data
        print("\nStep 1: Processing test cases...")
        
        if is_sample_case is None:
            all_test_cases = problem_data.test_cases
            for test_case in all_test_cases:
                test_case.extension = ".sample" if test_case.example_flag == '1' else ".in"
        else:
            all_test_cases = []
            for test_case in problem_data.test_cases:
                if test_case.test_case_id in is_sample_case:
                    all_test_cases.append(test_case)
                    test_case.extension = ".sample"
            all_test_cases.sort(key=lambda x: is_sample_case[x.test_case_id])
            for test_case in problem_data.test_cases:
                if test_case.test_case_id not in is_sample_case:
                    all_test_cases.append(test_case)
                    test_case.extension = ".in"

        if not all_test_cases:
            print("No test cases found for this problem")
        else:
            print(f"Found {len(all_test_cases)} test cases")

            # Create original_tests directory
            original_tests_dir = os.path.join(problem_dir, "original_tests")
            if not os.path.exists(original_tests_dir):
                os.makedirs(original_tests_dir)
                print(f"Created original_tests directory: {original_tests_dir}")

            # Save each test case to a separate file
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            decoded_test_cases = []

            for i, test_case in enumerate(all_test_cases):
                test_case.path = os.path.join(original_tests_dir, f"{i+1:03d}{test_case.extension}")
                test_file = test_case.path

                # Decode the base64 encoded args
                decoded_args = decode_java_object(test_case.args, script_dir)
                if decoded_args is None:
                    print(f"Warning: Failed to decode args for test case {i+1}, using raw base64")
                    decoded_args = test_case.args

                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write(decoded_args)
                decoded_test_cases.append(decoded_args)
                print(f"Saved test case {i+1} to: {test_file}")

        # Step 2: Generate ICPC format documentation
        print("\nStep 2: Generating ICPC format documentation...")
        icpc_documentation = get_icpc_format_documentation(xml_description, problem_data.problem.name, decoded_test_cases[:3], llm_helper)

        if icpc_documentation:
            # Save documentation to file
            doc_file = os.path.join(problem_dir, "icpc_format_documentation.md")
            with open(doc_file, 'w', encoding='utf-8') as f:
                f.write(icpc_documentation)
            print(f"Saved ICPC format documentation to: {doc_file}")
        else:
            print("Failed to generate ICPC format documentation")
            return

        # Step 3: Generate test conversion script using LLM
        print("\nStep 3: Generating test conversion script...")
        if all_test_cases and icpc_documentation:
            error = ""
            tries = 0
            MAX_TRIES = 10
            while tries < MAX_TRIES:
                conversion_script = generate_test_conversion_script(
                    icpc_documentation, decoded_test_cases[:3], problem_data.problem.name, error, llm_helper
                )
                if conversion_script:
                    script_file = os.path.join(problem_dir, "convert_tests.py")
                    with open(script_file, 'w', encoding='utf-8') as f:
                        f.write(conversion_script)
                    print(f"Saved test conversion script to: {script_file}")

                    # Step 4: Run conversion script on all test cases
                    print("\nStep 4: Converting test cases to ICPC format...")
                    tests_dir = os.path.join(problem_dir, "tests")
                    if not os.path.exists(tests_dir):
                        os.makedirs(tests_dir)
                        print(f"Created tests directory: {tests_dir}")

                    # Run conversion script for each test case
                    try:
                        convert_all_test_cases(script_file, original_tests_dir, tests_dir, all_test_cases)
                    except Exception as e:
                        error = f"The script:\n{conversion_script}\n" + str(e)
                        tries += 1
                        continue
                    break
                else:
                    print("Failed to generate test conversion script")
            if tries == MAX_TRIES:
                print("Failed to generate working test conversion script")

        # Step 4.5: Convert solutions to ICPC format
        print("\nStep 4.5: Converting solutions to ICPC format...")
        if problem_data.solutions and icpc_documentation:
            solutions_dir = os.path.join(problem_dir, "solutions")
            if not os.path.exists(solutions_dir):
                os.makedirs(solutions_dir)
                print(f"Created solutions directory: {solutions_dir}")

            # Get file extensions based on language
            language_extensions = {
                1: ".java",    # Java
                3: ".cpp",     # C++
                4: ".cs",      # C#
                5: ".vb",      # VB
                6: ".py",      # Python
                7: ".py"       # Python 3
            }

            for i, solution in enumerate(problem_data.solutions, 1):
                print(f"\nConverting solution {i}/{len(problem_data.solutions)} (Language ID: {solution.language_id})...")

                converted_code = convert_solution_to_icpc_format(
                    solution.solution_text,
                    solution.language_id,
                    icpc_documentation,
                    problem_data.problem.name,
                    llm_helper
                )

                if converted_code:
                    # Get file extension
                    extension = language_extensions.get(solution.language_id, ".txt")
                    solution_file = os.path.join(solutions_dir, f"s{i:02d}{extension}")

                    with open(solution_file, 'w', encoding='utf-8') as f:
                        f.write(converted_code)

                    print(f"Saved converted solution to: {solution_file}")
                else:
                    print(f"Failed to convert solution {i}")
        else:
            if not problem_data.solutions:
                print("No solutions found for this problem")
            if not icpc_documentation:
                print("No ICPC documentation available for solution conversion")

        # Step 5: Generate LaTeX problem statement (two-step process)
        print("\nStep 5: Converting to olymp.sty LaTeX format...")
        statements_dir = os.path.join(problem_dir, "statements")
        os.makedirs(statements_dir)

        # Step 5a: Convert to LaTeX with documentation
        latex_content = convert_to_latex(xml_description, icpc_documentation, problem_data.problem.name, llm_helper)

        with open(os.path.join(statements_dir, "problem.tex"), "w", encoding='utf-8') as stf:
            stf.write(latex_content)

        if not latex_content:
            print("Failed to convert to LaTeX format")
            return

        # Step 5b: Split LaTeX into sections
        latex_sections = split_latex_into_sections(latex_content, llm_helper)

        if latex_sections:
            # Create subdirectory for LaTeX files
            latex_dir = os.path.join(statements_dir, "latex")
            if not os.path.exists(latex_dir):
                os.makedirs(latex_dir)
                print(f"Created LaTeX directory: {latex_dir}")

            # Save each section to separate files
            sections = ['name', 'legend', 'input-format', 'output-format', 'notes']
            for section in sections:
                if section in latex_sections:
                    section_file = os.path.join(latex_dir, f"{section}.tex")
                    with open(section_file, 'w', encoding='utf-8') as f:
                        f.write(latex_sections[section])
                    print(f"Saved {section} to: {section_file}")

            print(f"\nConversion completed successfully!")
            print(f"Output directory: {problem_dir}")
            print(f"- ICPC documentation: icpc_format_documentation.md")
            print(f"- Original test cases: original_tests/")
            if all_test_cases:
                print(f"- Test conversion script: convert_tests.py")
                print(f"- Converted test cases: tests/")
            if problem_data.solutions:
                print(f"- Converted solutions: solutions/ ({len(problem_data.solutions)} solutions)")
            print(f"- LaTeX sections: latex/")
        else:
            print("Failed to convert to LaTeX format")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    finally:
        db_ops.close()


def generate_test_conversion_script(icpc_documentation: str, example_test_cases: List[str], problem_name: str, error: str, llm_helper: LLMHelper) -> Optional[str]:
    """Generate a Python script to convert test cases from TopCoder format to ICPC format"""
    context = "You are a competitive programming expert who specializes in converting test cases between different contest formats."

    # Prepare example test cases for the prompt
    examples_text = ""
    for i, test_case in enumerate(example_test_cases[:3]):  # Use up to 3 examples
        examples_text += f"\nExample Test Case {i+1}:\n"
        examples_text += f"{test_case}\n"

    prompt = [f"""
I need you to generate a Python script that converts test cases from TopCoder format according to the documentation.

Problem Name: {problem_name}

ICPC Format Documentation:
{icpc_documentation}

Example TopCoder Test Cases:
{examples_text}

Please generate a complete Python script that:
1. Reads a TopCoder test case file
2. Parses it, you can always use python's eval(text) and it will correctly get a python list of arguments
3. Converts them to ICPC input format according to the documentation
4. Writes the converted input to a provided file
5. Exits with non-zero exit code is something failed

The script should:
- Take input file path and output file path as command line arguments
- Parse the TopCoder test case format from the input file
- Convert according to the ICPC format specification
- Handle any necessary data transformations (string parsing, format changes, etc.)
- Include error handling for malformed input
- Add comments explaining the conversion logic

Please provide a complete, runnable Python script with proper imports and error handling. Please don't include anything else in the reply, just the source code.
"""]
    if len(error) > 0:
        prompt.append(f"There is an error happened, please fix:\n{error}")

    try:
        text = llm_helper.ask_llm(context, prompt, max_tokens=4000)
        match = re.search(r"```(python3?|py)?\n?(.*?)```", text, re.DOTALL)
        return match.group(2).strip() if match else text
    except Exception as e:
        print(f"Error generating test conversion script: {e}")
        return None


def get_icpc_format_documentation(xml_description: str, problem_name: str, test_cases: List[str], llm_helper: LLMHelper) -> Optional[str]:
    """Get GPT-4o to generate ICPC format documentation for the problem"""
    test_cases_text = '\n'.join(f"Test Case {i}:\n{f}" for i, f in enumerate(test_cases))

    context = "You are a competitive programming expert who specializes in converting problems between different contest formats."
    prompt = f"""
You are a competitive programming expert. I need to convert a TopCoder problem to ICPC format.

Given the following TopCoder problem XML description, please write detailed documentation explaining:

1. How the input format should look like in an ICPC-style competition
2. How the output format should look like in an ICPC-style competition
3. How to convert test cases from TopCoder format to ICPC format (don't take examples from xml, take them from examples)
4. How to modify solutions that work with TopCoder format to work with ICPC format
5. Any important considerations for the conversion process
6. How the variables from the original statement should be called in a new ICPC format, include how old naming corresponds to the new naming in the documentation
   - Usually in ICPC format they use single-letter named variables, they don't use words like 'array', they use mathematical notations.
7. Sometimes in topcoder they split the input into an array that needs to be concatenated in order to get the real input data. We should avoid this in ICPC,
    if Topcoder gives an array of strings that need to be concatenated, the ICPC problem has to include the concatenation in the input. If this concatenated string is a list of numbers,
    then ICPC problem has to include numbers and not strings.

The documentation should be practical and actionable, helping someone to:
- Rewrite the problem statement from TopCoder format to ICPC format
- Write a script to convert test cases
- Include several examples in the documentation for conversion
- Adapt existing solutions to the new format

Problem Name: {problem_name}

TopCoder Problem XML:
{xml_description}

TopCoder formatted testcase examples for tests and solutions conversion:
{test_cases_text}

Please provide comprehensive documentation in Markdown format.
"""
    return llm_helper.ask_llm(context, [prompt], max_tokens=3000)


def convert_to_latex(xml_description: str, icpc_documentation: str, problem_name: str, llm_helper: LLMHelper) -> Optional[str]:
    """
    Step 1: Convert TopCoder problem to LaTeX format using ICPC documentation.
    Returns the complete LaTeX problem statement.
    """
    prompt = f"""
You are a competitive programming expert. I need to convert a TopCoder problem to olymp.sty LaTeX format.

Given the TopCoder problem XML description and ICPC format documentation, please rewrite the problem statement in olymp.sty LaTeX format.

Important requirements:
- Use olymp.sty LaTeX formatting
- Use proper LaTeX formatting for mathematical expressions, code, etc.
- All LaTeX formulas have to be inside '$'
- Usually in ICPC format they use single-letter named variables, they don't use words like 'array', they use mathematical notations.
- The naming must be consistent throughout the problem statement
- The input, output formats and the notes section usually don't use itemize. Just write text as `The first line of the input consists of two integers`, or `In the first example ...`.
- The constraints have to be integrated into the input format, don't make extra constraints section
- Don't include examples in the statement
- use U+0060 backtick and ' for single-quotes
- use double (U+0060 backtick) and '' for double-quotes
- include anything inside quotes into \\texttt command, don't include quotes themselves: for instance `\\texttt{{hello}}'
- Don't forget to write example explanations in the notes section
- Sometimes in topcoder they split the input into an array that needs to be concatenated in order to get the real input data. We should avoid this in ICPC,
    if Topcoder gives an array of strings that need to be concatenated, the ICPC problem has to include the concatenation in the input. If this concatenated string is a list of numbers,
    then ICPC problem has to include numbers and not strings.

Problem Name: {problem_name}

ICPC Format Documentation:
{icpc_documentation}

TopCoder Problem XML:
{xml_description}

Please provide the complete LaTeX problem statement. Don't divide it into sections yet, just provide the full statement.
"""

    print("=" * 60)
    print("STEP 1: Converting to LaTeX format")
    print("=" * 60)
    context = "You are a competitive programming expert who specializes in LaTeX formatting and problem statement conversion."
    latex_content = llm_helper.ask_llm(context, [prompt], max_tokens=16000, temperature=0.4)

    print("\nGenerated LaTeX content:")
    print(latex_content)
    return latex_content


def split_latex_into_sections(latex_content: str, llm_helper: LLMHelper) -> Optional[Dict[str, str]]:
    """
    Step 2: Split the LaTeX problem statement into required sections.
    Takes complete LaTeX statement and divides it into: name, legend, input-format, output-format, notes.
    """
    prompt = f"""
I have a LaTeX problem statement that needs to be divided into exactly 5 sections for the olymp.sty format.

Please divide the following LaTeX content into these sections:
1. name - The problem title
2. legend - The problem story/description
3. input-format - Input format specification (include constraints here)
4. output-format - Output format specification
5. notes - Additional notes, sample case explanations

Important:
- Don't modify the LaTeX content, just divide it appropriately
- Constraints should be part of the input-format section
- Keep all LaTeX formatting intact
- Don't include examples

Please provide the output in the following format:

=== NAME ===
[content for name section]

=== LEGEND ===
[content for legend section]

=== INPUT-FORMAT ===
[content for input-format section including constraints]

=== OUTPUT-FORMAT ===
[content for output-format section]

=== NOTES ===
[content for notes section]

Here is the LaTeX content to divide:

{latex_content}
"""

    print("\n" + "=" * 60)
    print("STEP 2: Dividing LaTeX into sections")
    print("=" * 60)
    context = "You are a competitive programming expert who specializes in LaTeX formatting and problem statement organization."
    sectioned_content = llm_helper.ask_llm(context, [prompt], max_tokens=16000, temperature=0.2)

    try:
        print("\nSectioned content:")
        print(sectioned_content)

        # Helper function to remove ```latex wrapper
        def strip_latex_wrapper(content: str) -> str:
            content = content.strip()
            if content.startswith('```latex'):
                content = content[8:].lstrip('\n')
            if content.endswith('```'):
                content = content[:-3].rstrip('\n')
            return content

        # Parse the response to extract sections
        sections = {}
        current_section = None
        current_content = []

        for line in sectioned_content.split('\n'):
            if line.startswith('=== ') and line.endswith(' ==='):
                # Save previous section
                if current_section:
                    sections[current_section] = strip_latex_wrapper('\n'.join(current_content))

                # Start new section
                current_section = line[4:-4].lower()
                current_content = []
            else:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = strip_latex_wrapper('\n'.join(current_content))

        return sections

    except Exception as e:
        raise Exception(f"Failed to split LaTeX into sections: {e}")


def convert_test_case_with_llm(test_case: str, icpc_documentation: str, problem_name: str, llm_helper: LLMHelper) -> Optional[str]:
    """Get GPT-4o to convert test case to ICPC format"""
    context = "You are a competitive programming expert who specializes in converting test cases between different contest formats."
    prompt = f"""
You are a competitive programming expert. I need to convert a TopCoder test case to ICPC format.
    """
    prompt += f"Problem Name: {problem_name}\n"
    prompt += f"TopCoder Test Case:\n{test_case}\n"
    prompt += f"\nICPC Format Documentation:\n{icpc_documentation}\n"
    prompt += f"\nPlease convert the test case to ICPC format and provide the output as is with no text included\n"
    result = llm_helper.ask_llm(context, [prompt], max_tokens=3000)
    # if LLM answers with extra text, strip everything
    match = re.match(r"```(\S)*\n?(.*?)```", result, re.DOTALL)
    if match:
        result = match.group(2).strip()
    result = '\n'.join(line.strip() for line in result.splitlines())
    return result


def convert_solution_to_icpc_format(solution_code: str, language_id: int, icpc_documentation: str, problem_name: str, llm_helper: LLMHelper) -> Optional[str]:
    """
    Convert a TopCoder solution to ICPC format by adding stdin/stdout handling.

    Args:
        solution_code: Original TopCoder solution code
        language_id: Language ID (1=Java, 3=C++, 4=C#, 5=VB, 6=Python)
        icpc_documentation: ICPC format documentation
        problem_name: Name of the problem
        llm_helper: LLM helper instance

    Returns:
        Converted solution code with main function for stdin/stdout
    """
    # Map language IDs to language names
    language_map = {
        1: "Java",
        3: "C++",
        4: "C#",
        5: "VB",
        6: "Python",
        7: "Python 3"
    }

    language = language_map.get(language_id, "Unknown")

    context = "You are a competitive programming expert who specializes in converting solutions between different contest formats."
    prompt = f"""
You are a competitive programming expert. I need to convert a TopCoder solution to ICPC format.

The TopCoder solution is a class method that takes parameters and returns a result.
I need you to add a main function that:
1. Reads input from stdin according to the ICPC format
2. Calls the original solution method with the parsed input
3. Prints the result to stdout according to the ICPC format

Language: {language}
Problem Name: {problem_name}

ICPC Format Documentation:
{icpc_documentation}

TopCoder Solution Code:
{solution_code}

Please provide the complete converted solution with:
- The original solution code (keep it as is)
- A main function that reads from stdin, calls the solution, and writes to stdout
- Proper input/output formatting according to ICPC documentation
- No additional explanations, just the code

Make sure the solution is ready to compile and run for ICPC-style testing.
"""

    try:
        converted_code = llm_helper.ask_llm(context, [prompt], max_tokens=4000, temperature=0.3)

        # Try to extract code from markdown code blocks if present
        match = re.search(r"```(?:\w+)?\n(.*?)```", converted_code, re.DOTALL)
        if match:
            converted_code = match.group(1).strip()

        return converted_code
    except Exception as e:
        print(f"Error converting solution: {e}")
        return None


def convert_all_test_cases(script_file: str, original_tests_dir: str, tests_dir: str, all_test_cases: List[System_test_case]) -> None:
    """Run the conversion script on all test cases"""
    for i, test_case in enumerate(all_test_cases):
        test_file = test_case.path

        # Run the conversion script
        result = subprocess.run([
            sys.executable, script_file, test_file, os.path.join(tests_dir, os.path.basename(test_file))
        ], capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print(f"Successfully converted test case {i+1}")
        else:
            print(f"Error converting test case {i+1}: {result.stderr}")
            raise Exception(f"Error converting test case {i+1}:\nstdout: {result.stdout}\nstderr: {result.stderr}")
