#!/usr/bin/env python3
"""
Database Operations Module

This module handles all database operations for retrieving problems,
solutions, and test cases from the TopCoder SQLite database.
"""

import sqlite3
import subprocess
import os
import sys
from typing import List, Optional
from dataclasses import dataclass

# Import the entities from the provided schema
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'all'))
from entities import Problem, Solution, System_test_case, Round_component


@dataclass
class SampleCase:
    """Container for a sample test case from the problem description"""
    case_id: str
    annotation: str


@dataclass
class ProblemData:
    """Container for complete problem data with statement, solutions, and tests"""
    problem: Problem
    problem_statement: Optional[str]
    components: List[Round_component]
    solutions: List[Solution]
    test_cases: List[System_test_case]
    sample_cases: List[SampleCase]


def decode_java_object(base64_string: str, script_dir: str) -> Optional[str]:
    """Decode a base64 encoded Java serialized object using the JavaObjectDecoder"""
    try:
        # Run the Java decoder
        result = subprocess.run(
            ['java', 'JavaObjectDecoder', base64_string],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Java decoder error: {result.stderr}")
            return None

    except subprocess.TimeoutExpired:
        print("Java decoder timed out")
        return None
    except Exception as e:
        print(f"Error running Java decoder: {e}")
        return None


class DatabaseOperations:
    """Handles all database operations for TopCoder problems"""

    def __init__(self, db_path: str):
        """Initialize with database path"""
        self.db_path = db_path
        self.connection = None

    def connect(self) -> None:
        """Connect to the SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Enable column access by name
        except sqlite3.Error as e:
            raise Exception(f"Failed to connect to database: {e}")

    def close(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

    def find_problem_by_name(self, problem_name: str) -> Optional[Problem]:
        """Find a problem by its name"""
        if not self.connection:
            raise Exception("Database not connected")

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM problems WHERE name = ? COLLATE NOCASE",
            (problem_name,)
        )

        row = cursor.fetchone()
        if row:
            return Problem.from_dict(dict(row))
        return None

    def find_components_by_problem_id(self, problem_id: int) -> List[Round_component]:
        """Find all components associated with a problem"""
        if not self.connection:
            raise Exception("Database not connected")

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM round_component WHERE problem_id = ?",
            (str(problem_id),)
        )

        components = []
        for row in cursor.fetchall():
            components.append(Round_component.from_dict(dict(row)))

        return components

    def find_solutions_by_component_id(self, component_id: int) -> List[Solution]:
        """Find all solutions for a given component"""
        if not self.connection:
            raise Exception("Database not connected")

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM solutions WHERE component_id = ?",
            (str(component_id),)
        )

        solutions = []
        for row in cursor.fetchall():
            solutions.append(Solution.from_dict(dict(row)))

        return solutions

    def find_test_cases_by_component_id(self, component_id: int) -> List[System_test_case]:
        """Find all test cases for a given component"""
        if not self.connection:
            raise Exception("Database not connected")

        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM system_test_cases WHERE component_id = ?",
            (str(component_id),)
        )

        test_cases = []
        for row in cursor.fetchall():
            test_cases.append(System_test_case.from_dict(dict(row)))

        return test_cases

    @staticmethod
    def _extract_problem_description_from_xml(xml_text: str) -> Optional[str]:
        """Extract problem description from XML component text"""
        try:
            import xml.etree.ElementTree as ET
            import html
            import re

            # Parse the XML
            root = ET.fromstring(xml_text)
            # Find the intro element which contains the problem description
            # Handle XML namespace if present
            namespace = {'tc': 'http://topcoder.com'}
            parent = root.find('.//tc:test-cases', namespace)
            for testcase in parent.findall('tc:test-case', namespace):
                if testcase.get('example') != '1':
                    parent.remove(testcase)

            def extract_text_from_element(elem):
                """Recursively extract text from an element and its children"""
                text_parts = []
                if elem.text:
                    text_parts.append(elem.text)

                for child in elem:
                    text_parts.append(extract_text_from_element(child))
                    if child.tail:
                        text_parts.append(child.tail)

                result = ''.join(text_parts)

                if elem.tag.endswith("test-cases"):
                    return ""
                elif elem.tag.endswith("test-case"):
                    return f"\n Test case: \n{result}"
                elif elem.tag.endswith("notes"):
                    return f"\n Constraints: \n{result}"
                elif elem.tag.endswith("output"):
                    return f"\n\n Output: \n{result}\n\n"

                return result

            intro_text = extract_text_from_element(root)

            # Check if the content is HTML escaped
            if root.get('escaped') == '1':
                intro_text = html.unescape(intro_text)

            # Clean up the text
            clean_text = intro_text
            # Remove leading/trailing whitespace
            clean_text = clean_text.strip()

            return clean_text if clean_text else None

        except Exception as e:
            # If XML parsing fails, return None
            print(f"XML parsing failed: {e}")
            return None

    def extract_sample_cases(self, xml_description: str) -> List[SampleCase]:
        """Extract sample test cases from XML description"""
        try:
            import xml.etree.ElementTree as ET
            import html

            # Parse the XML
            root = ET.fromstring(xml_description)

            # Find the test-cases element
            namespace = {'tc': 'http://topcoder.com'}
            test_cases_elem = root.find('.//tc:test-cases', namespace)

            use_namespace = test_cases_elem is not None
            if test_cases_elem is None:
                # Try without namespace
                test_cases_elem = root.find('.//test-cases')

            if test_cases_elem is None:
                return []

            sample_cases = []

            # Find all test-case elements with example="1"
            test_case_list = (test_cases_elem.findall('tc:test-case', namespace)
                             if use_namespace
                             else test_cases_elem.findall('test-case'))

            for test_case in test_case_list:
                if test_case.get('example') == '1':
                    case_id = test_case.get('id', '')

                    # Extract annotation text
                    annotation_elem = (test_case.find('tc:annotation', namespace)
                                      if use_namespace
                                      else test_case.find('annotation'))
                    annotation_text = ''

                    if annotation_elem is not None:
                        annotation_text = ''.join(annotation_elem.itertext()) or ''

                        # Check if the annotation is HTML escaped
                        if annotation_elem.get('escaped') == '1':
                            annotation_text = html.unescape(annotation_text)

                    sample_cases.append(SampleCase(
                        case_id=case_id,
                        annotation=annotation_text
                    ))

            return sample_cases

        except Exception as e:
            print(f"Error extracting sample cases: {e}")
            return []

    def get_problem_data(self, problem_name: str) -> Optional[ProblemData]:
        """
        Single entry function to retrieve all data for a problem.

        Args:
            problem_name: Name of the problem to retrieve

        Returns:
            ProblemData object containing:
                - problem: Problem entity
                - problem_statement: Extracted problem description from XML
                - components: List of Round_component entities
                - solutions: List of Solution entities
                - test_cases: List of System_test_case entities

            Returns None if problem not found.
        """
        if not self.connection:
            raise Exception("Database not connected. Call connect() first or use context manager.")

        # Find the problem
        problem = self.find_problem_by_name(problem_name)
        if not problem:
            return None

        # Find components for this problem
        components = self.find_components_by_problem_id(problem.problem_id)

        # Extract problem statement and sample cases from component XML
        problem_statement = None
        sample_cases = []
        for component in components:
            if component.component_text:
                problem_statement = self._extract_problem_description_from_xml(component.component_text)
                sample_cases = self.extract_sample_cases(component.component_text)
                if problem_statement:
                    break

        # Find solutions and test cases for all components
        all_solutions = []
        all_test_cases = []

        used_component = set()

        for component in components:
            if component.component_id in used_component:
                continue
            used_component.add(component.component_id)
            solutions = self.find_solutions_by_component_id(component.component_id)
            test_cases = self.find_test_cases_by_component_id(component.component_id)

            all_solutions.extend(solutions)
            all_test_cases.extend(test_cases)

        return ProblemData(
            problem=problem,
            problem_statement=problem_statement,
            components=components,
            solutions=all_solutions,
            test_cases=all_test_cases,
            sample_cases=sample_cases
        )
