# Problem Description Generator

This script automatically generates formal problem descriptions for Polygon problems using an LLM.

## Overview

The script:
1. Takes a list of contest IDs as input
2. Iterates through all problems in those contests
3. Gets the problem statement for each problem
4. Uses an LLM to generate a short formal description (3 sentences)
5. Outputs all problem descriptions to a CSV file

## Requirements

Install the required packages:
```bash
pip install polygon_api openai
```

## Environment Setup

Set up your Polygon API credentials as environment variables:
```bash
export POLYGON_API_KEY="your_api_key"
export POLYGON_API_SECRET="your_api_secret"
export OPENAI_API_KEY="your_openai_api_key"
```

For custom OpenAI-compatible APIs (optional):
```bash
export OPENAI_BASE_URL="https://your-custom-api.com/v1"
```

Alternatively, you can provide them as command-line arguments.

## Usage

### Basic Usage

Process a single contest:
```bash
./write_problem_descriptions.py 12345
```

Process multiple contests:
```bash
./write_problem_descriptions.py 12345 12346 12347
```

### Custom Output File

Specify a custom output CSV file:
```bash
./write_problem_descriptions.py 12345 --output my_descriptions.csv
```

### Using Different OpenAI Model

Specify a different OpenAI model:
```bash
./write_problem_descriptions.py 12345 --model gpt-4-turbo
```

Or use a different model like GPT-3.5:
```bash
./write_problem_descriptions.py 12345 --model gpt-3.5-turbo
```

### Using Custom OpenAI API Endpoint

Use a custom OpenAI-compatible API endpoint:
```bash
./write_problem_descriptions.py 12345 --openai-base-url https://your-api.com/v1
```

This is useful for:
- Azure OpenAI deployments
- Local LLM servers (like LiteLLM proxy, vLLM, etc.)
- Other OpenAI-compatible APIs

### Specifying Description Language

Generate descriptions in a specific language:
```bash
./write_problem_descriptions.py 12345 --language Russian
```

Or use the short form:
```bash
./write_problem_descriptions.py 12345 -l Spanish
```

The LLM will generate descriptions in the specified language. Examples:
- English (default)
- Russian
- Spanish
- Chinese
- French
- Any other language supported by the LLM

### Verbose Output

Enable verbose logging to see more details:
```bash
./write_problem_descriptions.py 12345 --verbose
```

### All Options

```bash
./write_problem_descriptions.py --help
```

Output:
```
usage: write_problem_descriptions.py [-h] [--output OUTPUT] [--api-url API_URL]
                                      [--api-key API_KEY] [--api-secret API_SECRET]
                                      [--model MODEL] [--openai-api-key OPENAI_API_KEY]
                                      [--openai-base-url OPENAI_BASE_URL]
                                      [--language LANGUAGE] [--verbose]
                                      contest_ids [contest_ids ...]

Generate formal problem descriptions for Polygon contest problems

positional arguments:
  contest_ids           Contest ID(s) to process (space-separated)

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT, -o OUTPUT
                        Output CSV file path (default: problem_descriptions.csv)
  --api-url API_URL     Polygon API URL
  --api-key API_KEY     Polygon API key (or set POLYGON_API_KEY env var)
  --api-secret API_SECRET
                        Polygon API secret (or set POLYGON_API_SECRET env var)
  --model MODEL         OpenAI model to use (default: gpt-4)
  --openai-api-key OPENAI_API_KEY
                        OpenAI API key (or set OPENAI_API_KEY env var)
  --openai-base-url OPENAI_BASE_URL
                        OpenAI API base URL (or set OPENAI_BASE_URL env var)
  --language LANGUAGE, -l LANGUAGE
                        Language for generated descriptions (default: English)
  --verbose, -v         Enable verbose logging
```

## Output Format

The script generates a CSV file with the following columns:
- `contest_id`: The Polygon contest ID
- `problem_id`: The Polygon problem ID
- `problem_name`: The problem name/letter
- `description`: The generated 3-sentence formal description

## Description Format

Each generated description:
- Contains exactly 3 sentences
- Is formal and concise
- Is written in the specified language (default: English)
- Includes the most important details about the problem
- Includes key constraints at the end (e.g., array size limits, value ranges)
- Uses mathematical or technical terminology where appropriate
- Does not include example inputs/outputs

## Example

```bash
$ ./write_problem_descriptions.py 12345 12346 -o descriptions.csv

2024-01-01 12:00:00 - INFO - Processing 2 contest(s)
2024-01-01 12:00:01 - INFO - Processing contest 12345
2024-01-01 12:00:02 - INFO -   Found 5 problems in contest
2024-01-01 12:00:03 - INFO -   Processing problem: A (ID: 123)
2024-01-01 12:00:04 - INFO -     Got problem statement (1500 characters)
2024-01-01 12:00:05 - INFO -     Generating description...
2024-01-01 12:00:08 - INFO -     Generated description (285 characters)
2024-01-01 12:00:08 - INFO -     ✓ Successfully generated description
...
2024-01-01 12:05:00 - INFO - Writing 10 descriptions to descriptions.csv
2024-01-01 12:05:00 - INFO - ✓ Successfully wrote descriptions to descriptions.csv
```

## Error Handling

The script will:
- Continue processing other problems if one fails
- Log all errors with details
- Skip contests that cannot be accessed
- Still generate the CSV file with successfully processed problems

## Notes

- The script uses the same Polygon API library as `write_validators`
- OpenAI API is used for generating descriptions
- The script processes contests sequentially to avoid rate limiting
- Problem statements are retrieved in English when available, otherwise the first available language is used
- Generated descriptions can be in any language supported by the LLM (use `--language` parameter)
- Supports any OpenAI model (gpt-4, gpt-4-turbo, gpt-3.5-turbo, etc.)
- Compatible with OpenAI-compatible APIs through the `--openai-base-url` parameter
