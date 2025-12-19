# Polygon API Python Wrapper Documentation

A Python wrapper for the Polygon API (polygon.codeforces.com) that provides a convenient interface for managing competitive programming problems.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Core Classes](#core-classes)
- [API Methods](#api-methods)
- [Examples](#examples)
- [Error Handling](#error-handling)
- [Data Models](#data-models)

## Installation

```bash
pip install polygon_api
```

## Quick Start

```python
from polygon_api import Polygon

# Initialize the API client
api = Polygon(
    api_url="https://polygon.codeforces.com/api",
    api_key="your_api_key",
    api_secret="your_api_secret"
)

# List all problems
problems = api.problems_list()
print(f"Found {len(problems)} problems")

# Get problem info
if problems:
    problem = problems[0]
    info = problem.info()
    print(f"Problem: {problem.name}, Time Limit: {info.time_limit}ms")
```

## Authentication

To use the Polygon API, you need to generate an API key from your Polygon settings page. Each API key consists of:

- **key**: Your public API key
- **secret**: Your private API secret

The wrapper automatically handles the required authentication parameters:
- `apiKey`: Your public key
- `time`: Current UNIX timestamp
- `apiSig`: SHA-512 signature for request verification

## Core Classes

### Polygon

The main API client class that provides access to all Polygon API methods.

```python
class Polygon:
    def __init__(self, api_url, api_key, api_secret):
        """
        Initialize the Polygon API client.
        
        Args:
            api_url (str): The Polygon API base URL
            api_key (str): Your API key
            api_secret (str): Your API secret
        """
```

### Problem

Represents a Polygon problem with its metadata and provides convenient methods for problem operations.

```python
class Problem:
    def __init__(self, polygon, problem_id, owner, name, deleted, favorite, 
                 access_type, revision, latest_package, modified):
        """
        Problem object with metadata and operation methods.
        
        Attributes:
            id (int): Problem ID
            owner (str): Problem owner username
            name (str): Problem name
            deleted (bool): Whether the problem is deleted
            favorite (bool): Whether the problem is marked as favorite
            access_type (str): Access level (READ, WRITE, etc.)
            revision (int): Current revision number
            latest_package (int): Latest package revision
            modified (bool): Whether the problem has uncommitted changes
        """
```

## API Methods

### Problem Management

#### List Problems

```python
def problems_list(self, show_deleted=None, id=None, name=None, owner=None):
    """
    Get a list of problems available to the user.
    
    Args:
        show_deleted (bool, optional): Include deleted problems
        id (int, optional): Filter by problem ID
        name (str, optional): Filter by problem name
        owner (str, optional): Filter by owner username
    
    Returns:
        List[Problem]: List of Problem objects
    """
```

#### Create Problem

```python
def problem_create(self, name):
    """
    Create a new empty problem.
    
    Args:
        name (str): Name of the new problem
    
    Returns:
        Problem: The created Problem object
    """
```

### Problem Information

#### Get Problem Info

```python
def problem_info(self, problem_id):
    """
    Get detailed information about a problem.
    
    Args:
        problem_id (int): Problem ID
    
    Returns:
        ProblemInfo: Problem information object
    """
```

#### Update Problem Info

```python
def problem_update_info(self, problem_id, problem_info):
    """
    Update problem information.
    
    Args:
        problem_id (int): Problem ID
        problem_info (ProblemInfo): Updated problem information
    
    Returns:
        dict: API response result
    """
```

### Working Copy Management

```python
def problem_update_working_copy(self, problem_id):
    """Update the working copy of a problem."""

def problem_discard_working_copy(self, problem_id):
    """Discard the working copy of a problem."""

def problem_commit_changes(self, problem_id, minor_changes=None, message=None):
    """
    Commit changes to a problem.
    
    Args:
        problem_id (int): Problem ID
        minor_changes (bool, optional): If True, no email notification sent
        message (str, optional): Commit message
    """
```

### Problem Statements

```python
def problem_statements(self, problem_id):
    """
    Get problem statements in all languages.
    
    Args:
        problem_id (int): Problem ID
    
    Returns:
        Dict[str, Statement]: Map from language code to Statement object
    """

def problem_save_statement(self, problem_id, lang, problem_statement):
    """
    Save or update a problem statement.
    
    Args:
        problem_id (int): Problem ID
        lang (str): Language code (e.g., 'english', 'russian')
        problem_statement (Statement): Statement object with content
    """
```

### Problem Resources

```python
def problem_statement_resources(self, problem_id):
    """Get list of statement resources (images, etc.)."""

def problem_save_statement_resource(self, problem_id, name, file, check_existing=None):
    """
    Save a statement resource file.
    
    Args:
        problem_id (int): Problem ID
        name (str): Resource filename
        file: File content
        check_existing (bool, optional): Only allow adding new files
    """
```

### Tests Management

```python
def problem_save_test(self, problem_id, testset, test_index, test_input, 
                     test_group=None, test_points=None, test_description=None,
                     test_use_in_statements=None, test_input_for_statements=None,
                     test_output_for_statements=None, verify_input_output_for_statements=None,
                     check_existing=None):
    """
    Save a test case for a problem.
    
    Args:
        problem_id (int): Problem ID
        testset (str): Testset name (e.g., 'tests', 'samples')
        test_index (int): Test number
        test_input (str): Test input data
        test_group (str, optional): Test group name
        test_points (int, optional): Points for this test
        test_description (str, optional): Test description
        test_use_in_statements (bool, optional): Use test in statements
        test_input_for_statements (str, optional): Input for statements
        test_output_for_statements (str, optional): Output for statements
        verify_input_output_for_statements (bool, optional): Verify I/O for statements
        check_existing (bool, optional): Only allow adding new tests
    """
```

### Files and Solutions Management

```python
def problem_files(self, problem_id):
    """
    Get all files (resource, source, aux) for a problem.
    
    Args:
        problem_id (int): Problem ID
    
    Returns:
        Dict[FileType, List[File]]: Dictionary mapping file types to lists of File objects
    """

def problem_view_file(self, problem_id, type, name):
    """
    Get the content of a specific file.
    
    Args:
        problem_id (int): Problem ID
        type (str): File type ('resource', 'source', 'aux')
        name (str): File name
    
    Returns:
        bytes: Raw file content
    """

def problem_save_file(self, problem_id, type, name, file, source_type=None, 
                     resource_advanced_properties=None):
    """
    Save or update a file.
    
    Args:
        problem_id (int): Problem ID
        type (str): File type ('resource', 'source', 'aux')
        name (str): File name
        file: File content
        source_type (str, optional): Source type for source files
        resource_advanced_properties (ResourceAdvancedProperties, optional): Advanced properties for resource files
    
    Returns:
        dict: API response result
    """

def problem_solutions(self, problem_id):
    """
    Get all solutions for a problem.
    
    Args:
        problem_id (int): Problem ID
    
    Returns:
        List[Solution]: List of Solution objects
    """

def problem_view_solution(self, problem_id, name):
    """
    Get the content of a specific solution.
    
    Args:
        problem_id (int): Problem ID
        name (str): Solution name
    
    Returns:
        bytes: Raw solution content
    """

def problem_save_solution(self, problem_id, name, file, source_type, tag, check_existing=None):
    """
    Save or update a solution.
    
    Args:
        problem_id (int): Problem ID
        name (str): Solution name
        file: Solution content
        source_type (str): Source type
        tag (SolutionTag): Solution tag (MA, OK, RJ, TL, TO, WA, PE, ML, RE)
        check_existing (bool, optional): Only allow adding new solutions
    
    Returns:
        dict: API response result
    """

def problem_edit_solution_extra_tags(self, problem_id, name, remove, testset=None, 
                                   test_group=None, tag=None):
    """
    Add or remove extra tags for a solution.
    
    Args:
        problem_id (int): Problem ID
        name (str): Solution name
        remove (bool): If True, remove tag; if False, add tag
        testset (str, optional): Testset name (mutually exclusive with test_group)
        test_group (str, optional): Test group name (mutually exclusive with testset)
        tag (SolutionTag, optional): Extra tag to add (required when remove=False)
    
    Returns:
        dict: API response result
    """
```

### Checker, Validator, and Interactor Management

```python
def problem_checker(self, problem_id):
    """
    Get the current checker for a problem.
    
    Args:
        problem_id (int): Problem ID
    
    Returns:
        str: Name of the current checker
    """

def problem_set_checker(self, problem_id, checker):
    """
    Set the checker for a problem.
    
    Args:
        problem_id (int): Problem ID
        checker (str): Name of the checker (must be one of the source files)
    
    Returns:
        dict: API response result
    """

def problem_validator(self, problem_id):
    """
    Get the current validator for a problem.
    
    Args:
        problem_id (int): Problem ID
    
    Returns:
        str: Name of the current validator
    """

def problem_set_validator(self, problem_id, validator):
    """
    Set the validator for a problem.
    
    Args:
        problem_id (int): Problem ID
        validator (str): Name of the validator (must be one of the source files)
    
    Returns:
        dict: API response result
    """

def problem_interactor(self, problem_id):
    """
    Get the current interactor for a problem.
    
    Args:
        problem_id (int): Problem ID
    
    Returns:
        str: Name of the current interactor
    """

def problem_set_interactor(self, problem_id, interactor):
    """
    Set the interactor for a problem.
    
    Args:
        problem_id (int): Problem ID
        interactor (str): Name of the interactor (must be one of the source files)
    
    Returns:
        dict: API response result
    """
```

### Test Script Management

```python
def problem_script(self, problem_id, testset):
    """
    Get the test generation script for a testset.
    
    Args:
        problem_id (int): Problem ID
        testset (str): Testset name
    
    Returns:
        str: Script content
    """

def problem_save_script(self, problem_id, testset, source):
    """
    Save the test generation script for a testset.
    
    Args:
        problem_id (int): Problem ID
        testset (str): Testset name
        source (str): Script source code
    
    Returns:
        dict: API response result
    """
```

### Advanced Test Management

```python
def problem_tests(self, problem_id, testset, no_inputs=None):
    """
    Get all tests for a specific testset.
    
    Args:
        problem_id (int): Problem ID
        testset (str): Testset name
        no_inputs (bool, optional): If True, return tests without input data
    
    Returns:
        List[Test]: List of Test objects (ManualTest or GeneratedTest)
    """

def problem_test_input(self, problem_id, testset, test_index):
    """
    Get the input for a specific test.
    
    Args:
        problem_id (int): Problem ID
        testset (str): Testset name
        test_index (int): Test index
    
    Returns:
        str: Test input content
    """

def problem_test_answer(self, problem_id, testset, test_index):
    """
    Get the expected answer for a specific test.
    
    Args:
        problem_id (int): Problem ID
        testset (str): Testset name
        test_index (int): Test index
    
    Returns:
        str: Test answer content
    """

def problem_set_test_group(self, problem_id, testset, test_group, test_indices):
    """
    Set the test group for one or more tests.
    
    Args:
        problem_id (int): Problem ID
        testset (str): Testset name
        test_group (str): Test group name
        test_indices (List[int] or str): List of test indices or comma-separated string
    
    Returns:
        dict: API response result
    """

def problem_view_test_group(self, problem_id, testset, group=None):
    """
    Get test group information.
    
    Args:
        problem_id (int): Problem ID
        testset (str): Testset name
        group (str, optional): Specific group name
    
    Returns:
        List[TestGroup] or TestGroup: Test group(s) information
    """

def problem_save_test_group(self, problem_id, testset, group, points_policy=None, 
                          feedback_policy=None, dependencies=None):
    """
    Save test group configuration.
    
    Args:
        problem_id (int): Problem ID
        testset (str): Testset name
        group (str): Test group name
        points_policy (PointsPolicy, optional): COMPLETE_GROUP or EACH_TEST
        feedback_policy (FeedbackPolicy, optional): NONE, POINTS, ICPC, or COMPLETE
        dependencies (List[str] or str, optional): List of dependent group names
    
    Returns:
        dict: API response result
    """
```

### Problem Configuration

```python
def problem_enable_groups(self, problem_id, testset, enable):
    """Enable or disable test groups for a problem."""

def problem_enable_points(self, problem_id, enable):
    """Enable or disable points-based scoring for a problem."""
```

### Tags and Metadata

```python
def problem_view_tags(self, problem_id):
    """Get problem tags."""

def problem_save_tags(self, problem_id, tags):
    """
    Save problem tags.
    
    Args:
        problem_id (int): Problem ID
        tags (List[str]): List of tag strings
    """

def problem_view_general_description(self, problem_id):
    """Get problem general description."""

def problem_save_general_description(self, problem_id, description):
    """Save problem general description."""

def problem_view_general_tutorial(self, problem_id):
    """Get problem tutorial."""

def problem_save_general_tutorial(self, problem_id, tutorial):
    """Save problem tutorial."""
```

### Package Management

```python
def problem_packages(self, problem_id):
    """
    Get all packages for a problem.
    
    Args:
        problem_id (int): Problem ID
    
    Returns:
        List[Package]: List of Package objects
    """

def problem_package(self, problem_id, package_id, type=None):
    """
    Download a specific package as a zip archive.
    
    Args:
        problem_id (int): Problem ID
        package_id (int): Package ID
        type (str, optional): Package type ('standard', 'linux', 'windows')
                             Defaults to 'standard' if not specified
    
    Returns:
        bytes: Package content as zip archive
    """

def problem_build_package(self, problem_id, full=None, verify=None):
    """
    Start building a new package for the problem.
    
    Args:
        problem_id (int): Problem ID
        full (bool, optional): If True, build full package with all types
        verify (bool, optional): If True, verify all solutions on all tests
    
    Returns:
        dict: API response result with package build information
    """
```

### Contest Methods

```python
def contest_problems(self, contest_id):
    """
    Get all problems in a contest.
    
    Args:
        contest_id (int): Contest ID
    
    Returns:
        Dict[str, Problem]: Dictionary mapping problem names to Problem objects
    """
```

## Examples

### Basic Problem Operations

```python
from polygon_api import Polygon, ProblemInfo, Statement

# Initialize API
api = Polygon("https://polygon.codeforces.com/api", "your_key", "your_secret")

# Create a new problem
new_problem = api.problem_create("My New Problem")
print(f"Created problem: {new_problem.name} (ID: {new_problem.id})")

# Update problem information
problem_info = ProblemInfo(
    input_file="input.txt",
    output_file="output.txt",
    interactive=False,
    time_limit=2000,  # 2 seconds
    memory_limit=256  # 256 MB
)
new_problem.update_info(problem_info)

# Add a statement
statement = Statement(
    encoding="UTF-8",
    name="My Problem",
    legend="This is a sample problem...",
    input="The first line contains an integer n...",
    output="Output a single integer...",
    notes="Note that n can be very large."
)
new_problem.save_statement("english", statement)

# Add tags
new_problem.save_tags(["math", "implementation", "easy"])

# Commit changes
new_problem.commit_changes(message="Initial problem setup")
```

### Working with Existing Problems

```python
# List problems by owner
my_problems = api.problems_list(owner="myusername")

# Find a specific problem
target_problem = None
for problem in my_problems:
    if "A+B" in problem.name:
        target_problem = problem
        break

if target_problem:
    # Get detailed info
    info = target_problem.info()
    print(f"Time limit: {info.time_limit}ms")
    print(f"Memory limit: {info.memory_limit}MB")
    
    # Get statements
    statements = target_problem.statements()
    if "english" in statements:
        eng_statement = statements["english"]
        print(f"Problem name: {eng_statement.name}")
        print(f"Legend: {eng_statement.legend[:100]}...")
    
    # Add a test case
    target_problem.save_test(
        testset="tests",
        test_index=1,
        test_input="5 3\n",
        test_description="Sample test case"
    )
```

### Working with Files and Solutions

```python
# Get all files for a problem
files = target_problem.files()
print(f"Resource files: {len(files[FileType.RESOURCE])}")
print(f"Source files: {len(files[FileType.SOURCE])}")
print(f"Aux files: {len(files[FileType.AUX])}")

# Upload a checker
with open("checker.cpp", "r") as f:
    checker_content = f.read()

target_problem.save_file(
    type="source",
    name="checker.cpp",
    file=checker_content,
    source_type="cpp.g++17"
)

# Set the checker
target_problem.set_checker("checker.cpp")

# Upload and configure a solution
with open("solution.cpp", "r") as f:
    solution_content = f.read()

target_problem.save_solution(
    name="main.cpp",
    file=solution_content,
    source_type="cpp.g++17",
    tag=SolutionTag.MA  # Main solution
)

# Get all solutions
solutions = target_problem.solutions()
for solution in solutions:
    print(f"Solution: {solution.name}, Tag: {solution.tag}")
```

### Advanced Test Management

```python
# Enable test groups
target_problem.enable_groups("tests", True)

# Create test groups with different policies
target_problem.save_test_group(
    testset="tests",
    group="samples",
    points_policy=PointsPolicy.COMPLETE_GROUP,
    feedback_policy=FeedbackPolicy.COMPLETE
)

target_problem.save_test_group(
    testset="tests", 
    group="main",
    points_policy=PointsPolicy.EACH_TEST,
    feedback_policy=FeedbackPolicy.ICPC,
    dependencies=["samples"]  # Depends on samples group
)

# Add tests to specific groups
target_problem.save_test(
    testset="tests",
    test_index=1,
    test_input="1 2\n",
    test_group="samples",
    test_points=0,
    test_use_in_statements=True
)

target_problem.save_test(
    testset="tests",
    test_index=2,
    test_input="1000000 999999\n", 
    test_group="main",
    test_points=10
)

# Get all tests
tests = target_problem.tests("tests")
for test in tests:
    if isinstance(test, ManualTest):
        print(f"Manual test {test.index}: group={test.group}, points={test.points}")
    else:
        print(f"Generated test {test.index}: script={test.script_line}")
```

### Package Management

```python
# Get all packages
packages = target_problem.packages()
for package in packages:
    print(f"Package {package.id}: revision={package.revision}, state={package.state}")

# Download the latest package
if packages:
    latest_package = packages[-1]
    if latest_package.state == "READY":
        package_content = target_problem.package(latest_package.id, type="linux")
        with open(f"package_{latest_package.id}.zip", "wb") as f:
            f.write(package_content)
        print(f"Downloaded package {latest_package.id}")

# Build a new package
build_result = api.problem_build_package(
    target_problem.id,
    full=True,
    verify=True
)
print(f"Package build started: {build_result}")
```

### Batch Operations

```python
# Process multiple problems
problems = api.problems_list(owner="contest_author")

for problem in problems:
    try:
        # Update working copy
        problem.update_working_copy()
        
        # Add common tags
        existing_tags = problem.tags()
        new_tags = existing_tags + ["contest2024"]
        problem.save_tags(new_tags)
        
        # Commit changes
        problem.commit_changes(
            minor_changes=True,
            message="Added contest tag"
        )
        
        print(f"Updated problem: {problem.name}")
        
    except Exception as e:
        print(f"Failed to update {problem.name}: {e}")
```

## Error Handling

The wrapper raises `PolygonRequestFailedException` when API requests fail:

```python
from polygon_api import PolygonRequestFailedException

try:
    problem = api.problem_create("Test Problem")
    info = problem.info()
except PolygonRequestFailedException as e:
    print(f"API request failed: {e}")
    # Handle the error appropriately
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Data Models

### ProblemInfo

```python
class ProblemInfo:
    def __init__(self, input_file=None, output_file=None, interactive=None, 
                 time_limit=None, memory_limit=None):
        """
        Problem configuration information.
        
        Attributes:
            input_file (str): Input file name
            output_file (str): Output file name
            interactive (bool): Whether problem is interactive
            time_limit (int): Time limit in milliseconds
            memory_limit (int): Memory limit in MB
        """
```

### Statement

```python
class Statement:
    def __init__(self, encoding=None, name=None, legend=None, input=None, 
                 output=None, scoring=None, interaction=None, notes=None, tutorial=None):
        """
        Problem statement in a specific language.
        
        Attributes:
            encoding (str): Text encoding (e.g., "UTF-8")
            name (str): Problem name
            legend (str): Problem description
            input (str): Input format description
            output (str): Output format description
            scoring (str): Scoring information
            interaction (str): Interaction protocol (for interactive problems)
            notes (str): Additional notes
            tutorial (str): Problem tutorial/editorial
        """
```

### Solution

```python
class Solution:
    def __init__(self, name, modification_time_seconds, length, source_type, tag):
        """
        Solution object representing a problem solution.
        
        Attributes:
            name (str): Solution name
            modification_time_seconds (int): Modification time in UNIX format
            length (int): Solution file size in bytes
            source_type (str): Source type
            tag (SolutionTag): Solution tag (MA, OK, RJ, TL, TO, WA, PE, ML, RE)
        """
```

### Test

```python
class Test:
    def __init__(self, polygon, problem_id, testset, index, group, points, description, 
                 use_in_statements, input_for_statements, output_for_statements, 
                 verify_input_output_for_statements):
        """
        Base test object. Use ManualTest or GeneratedTest subclasses.
        
        Attributes:
            testset (str): Testset name
            index (int): Test index
            group (str): Test group name
            points (int): Test points
            description (str): Test description
            use_in_statements (bool): Whether test is used in statements
            input_for_statements (str): Input for statements
            output_for_statements (str): Output for statements
            verify_input_output_for_statements (bool): Whether to verify I/O for statements
        """

class ManualTest(Test):
    def __init__(self, polygon, problem_id, testset, index, input, group=None, 
                 points=None, description=None, use_in_statements=None, 
                 input_for_statements=None, output_for_statements=None, 
                 verify_input_output_for_statements=None):
        """
        Manual test with explicit input.
        
        Additional Attributes:
            input (str): Test input data
        """

class GeneratedTest(Test):
    def __init__(self, polygon, problem_id, testset, index, group, points, description, 
                 use_in_statements, script_line, input_for_statements, output_for_statements, 
                 verify_input_output_for_statements):
        """
        Generated test created by script.
        
        Additional Attributes:
            script_line (str): Script line that generates this test
        """
```

### TestGroup

```python
class TestGroup:
    def __init__(self, name, points_policy=None, feedback_policy=None, dependencies=None):
        """
        Test group configuration.
        
        Attributes:
            name (str): Test group name
            points_policy (PointsPolicy): COMPLETE_GROUP or EACH_TEST
            feedback_policy (FeedbackPolicy): NONE, POINTS, ICPC, or COMPLETE
            dependencies (List[str]): List of dependent group names
        """
```

### Package

```python
class Package:
    def __init__(self, id, revision, creation_time_seconds, state, comment, type):
        """
        Package object representing a problem package.
        
        Attributes:
            id (int): Package ID
            revision (int): Problem revision for this package
            creation_time_seconds (int): Creation time in UNIX format
            state (str): Package state (PENDING, RUNNING, READY, FAILED)
            comment (str): Package comment
            type (str): Package type (standard, linux, windows)
        """
```

### ResourceAdvancedProperties

```python
class ResourceAdvancedProperties:
    def __init__(self, for_types=None, main=None, stages=None, assets=None):
        """
        Advanced properties for resource files.
        
        Attributes:
            for_types (str): Semicolon-separated list of applicable file types
            main (bool): Currently reserved to be False
            stages (List[Stage]): List of stages (COMPILE, RUN)
            assets (List[Asset]): List of assets (VALIDATOR, INTERACTOR, CHECKER, SOLUTION)
        """
```

### Enums

The library provides several enums for type safety:

- `PointsPolicy`: Scoring policies (COMPLETE_GROUP, EACH_TEST)
- `FeedbackPolicy`: Feedback policies (NONE, POINTS, ICPC, COMPLETE)
- `FileType`: File types (RESOURCE, SOURCE, AUX)
- `SolutionTag`: Solution tags (MA, OK, RJ, TL, TO, WA, PE, ML, RE)
- `Stage`: Problem stages (COMPILE, RUN)
- `Asset`: Asset types (VALIDATOR, INTERACTOR, CHECKER, SOLUTION)

## Advanced Usage

### Custom Request Configuration

The wrapper handles authentication automatically, but you can access lower-level functionality if needed:

```python
# The Polygon class uses RequestConfig internally
# You typically don't need to interact with this directly
```

### Working with Test Groups

```python
# Enable test groups
problem.enable_groups("tests", True)

# Create test groups with policies
problem.save_test_group(
    testset="tests",
    group="small",
    points_policy=PointsPolicy.COMPLETE_GROUP,
    feedback_policy=FeedbackPolicy.COMPLETE
)

problem.save_test_group(
    testset="tests",
    group="large", 
    points_policy=PointsPolicy.EACH_TEST,
    feedback_policy=FeedbackPolicy.ICPC,
    dependencies=["small"]
)

# Save tests with groups
problem.save_test(
    testset="tests",
    test_index=1,
    test_input="1 2\n",
    test_group="small"
)

problem.save_test(
    testset="tests", 
    test_index=2,
    test_input="1000000 999999\n",
    test_group="large"
)

# Set test group for multiple tests at once
problem.set_test_group(
    testset="tests",
    test_group="large",
    test_indices=[3, 4, 5]
)
```

### Points-based Scoring

```python
# Enable points
problem.enable_points(True)

# Add tests with points
problem.save_test(
    testset="tests",
    test_index=1,
    test_input="1 2\n",
    test_points=10
)
```

### Working with Contest Problems

```python
# Get all problems in a contest
contest_problems = api.contest_problems(contest_id=12345)

for name, problem in contest_problems.items():
    print(f"Problem {name}: {problem.name} (ID: {problem.id})")
    
    # You can work with contest problems just like regular problems
    info = problem.info()
    print(f"  Time limit: {info.time_limit}ms")
    print(f"  Memory limit: {info.memory_limit}MB")
```

### Working with Scripts and Generated Tests

```python
# Set up a test generation script
script_content = """
gen 1 2
gen 1000000 999999
gen_random 1 1000000 5
"""

problem.save_script(testset="tests", source=script_content)

# Get the current script
current_script = problem.script("tests")
print("Current script:", current_script)

# Get all tests (including generated ones)
tests = problem.tests("tests")
for test in tests:
    if isinstance(test, GeneratedTest):
        print(f"Generated test {test.index}: {test.script_line}")
        
        # Get the actual input for generated tests
        test_input = api.problem_test_input(problem.id, "tests", test.index)
        test_answer = api.problem_test_answer(problem.id, "tests", test.index)
        print(f"  Input: {test_input[:50]}...")
        print(f"  Answer: {test_answer[:50]}...")
```

## Notes

- This wrapper requires at least WRITE access to problems for most operations
- Some problems may require a PIN code - add it as a parameter when needed
- The API has rate limiting - be mindful of request frequency
- Always commit changes after making modifications
- Use `minor_changes=True` to avoid email notifications for small updates
- When working with files, the wrapper handles both text and binary content
- Test groups must be enabled before you can assign tests to groups
- Package building is asynchronous - check the package state before downloading
- Generated tests require a script to be set up first

## Contributing

This library is a work in progress and doesn't cover the entire Polygon API yet. Contributions are welcome!

## License

MIT License - see LICENSE file for details.