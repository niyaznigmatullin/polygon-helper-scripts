# Polygon Validator Writer

This script automatically generates and adds validators to Polygon problems in a contest that don't already have validators.

## Features

- Fetches all problems from a specified contest
- Identifies problems without validators
- Generates C++ validators using testlib.h via LiteLLM
- Automatically adds the generated validators to the problems
- Supports dry-run mode to preview changes
- Comprehensive logging and error handling

## Requirements

- Python 3.7+
- polygon_api library
- litellm library
- Polygon API credentials
- LiteLLM-compatible API access (OpenAI, Anthropic, etc.)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python write_validators.py <contest_id>
```

### With API Credentials

```bash
python write_validators.py 12345 --api-key YOUR_API_KEY --api-secret YOUR_API_SECRET
```

### Using Environment Variables

```bash
export POLYGON_API_KEY="your_api_key"
export POLYGON_API_SECRET="your_api_secret"
python write_validators.py 12345
```

### Dry Run (Preview Mode)

```bash
python write_validators.py 12345 --dry-run
```

### Using Different LLM Model

```bash
python write_validators.py 12345 --model gpt-3.5-turbo
```

### Verbose Logging

```bash
python write_validators.py 12345 --verbose
```

## Command Line Options

- `contest_id`: The Polygon contest ID to process (required)
- `--api-url`: Polygon API URL (default: https://polygon.codeforces.com/api)
- `--api-key`: Polygon API key (or set POLYGON_API_KEY env var)
- `--api-secret`: Polygon API secret (or set POLYGON_API_SECRET env var)
- `--model`: LiteLLM model to use (default: gpt-4)
- `--dry-run`: Show what would be done without making changes
- `--verbose, -v`: Enable verbose logging

## How It Works

1. **Contest Analysis**: Fetches all problems from the specified contest
2. **Validator Check**: Determines which problems don't have validators
3. **Statement Extraction**: Gets the problem statement for each problem
4. **Test Case Retrieval**: Downloads the first test case to help understand input/output format
5. **Validator Generation**: Uses LiteLLM to generate a C++ validator with testlib.h, including the test case for better format understanding
6. **Validator Integration**: Adds the generated validator to the problem and commits changes

## Generated Validators

The generated validators:
- Use `#include "testlib.h"`
- Call `registerValidation()` in main
- Validate all input constraints from the problem statement
- Use appropriate testlib functions (`inf.readInt()`, `inf.readSpace()`, etc.)
- Include bounds checking with descriptive error messages
- End with `inf.readEof()` to ensure no extra input

## Error Handling

The script includes comprehensive error handling:
- Network errors when communicating with Polygon API
- LLM generation failures
- File upload errors
- Invalid contest IDs
- Missing API credentials

## Logging

The script provides detailed logging:
- Contest processing status
- Problem validation checks
- Validator generation progress
- Success/failure notifications
- Error details for troubleshooting

## Example Output

```
2024-01-15 10:30:00 - INFO - Processing contest 12345
2024-01-15 10:30:01 - INFO - Found 5 problems in contest
2024-01-15 10:30:02 - INFO - Checking problem: Problem A (ID: 67890)
2024-01-15 10:30:02 - INFO -   ✓ Already has validator
2024-01-15 10:30:03 - INFO - Checking problem: Problem B (ID: 67891)
2024-01-15 10:30:03 - INFO -   ✗ No validator found
2024-01-15 10:30:04 - INFO - Found 1 problems without validators
2024-01-15 10:30:04 - INFO - Processing problem: Problem B
2024-01-15 10:30:05 - INFO -   Got problem statement (1250 characters)
2024-01-15 10:30:05 - INFO -   Retrieved first test case for format understanding
2024-01-15 10:30:05 - INFO -   Generating validator...
2024-01-15 10:30:08 - INFO -   Generated validator (850 characters)
2024-01-15 10:30:10 - INFO -   ✓ Successfully added validator
2024-01-15 10:30:10 - INFO - Completed processing. Successfully added validators to 1/1 problems
```

## Security Notes

- Store API credentials securely using environment variables
- The script only adds validators to problems without existing ones
- All changes are committed with descriptive messages
- Use dry-run mode to preview changes before execution

## Troubleshooting

### Common Issues

1. **Import Error**: Install required packages with `pip install -r requirements.txt`
2. **API Authentication**: Verify your Polygon API credentials
3. **Contest Not Found**: Check that the contest ID is correct and accessible
4. **LLM Errors**: Ensure you have proper API access for the chosen model
5. **Permission Errors**: Verify you have write access to the contest problems

### Debug Mode

Use `--verbose` flag for detailed debugging information:

```bash
python write_validators.py 12345 --verbose
```