# JSON to SQLite Schema Generator

This script analyzes JSON files and automatically generates SQLite database schemas and corresponding Python entity classes.

## Features

- **Automatic Schema Detection**: Analyzes the first 10KB of the first JSON file in a directory to infer data types and structure
- **SQLite Schema Generation**: Creates `CREATE TABLE` statements with appropriate data types
- **Python Entity Classes**: Generates dataclass-based entities with type annotations and conversion methods
- **Type Inference**: Intelligently detects numeric strings and converts them to appropriate Python types
- **Null Handling**: Properly handles nullable fields with `Optional` type annotations

## Usage

### Basic Usage

```bash
# Analyze a single JSON file
python3 json_to_sqlite.py <json_file>

# Analyze a directory containing JSON files
python3 json_to_sqlite.py <directory>

# Analyze multiple JSON files and/or directories (NEW!)
python3 json_to_sqlite.py <file1> <directory1> <file2> <directory2>
```

This will:
1. For each JSON file provided, analyze that file directly
2. For each directory provided, find all JSON files in that directory
3. Analyze the structure of all found JSON files using the first 10KB of each
4. **Merge all schemas into a unified schema** that accommodates all data structures
5. Generate `schema.sql` with SQLite CREATE TABLE statements for the unified schema
6. Generate `entities.py` with Python dataclass entities for the unified schema
7. **Create SQLite database** and insert all JSON data into the appropriate tables

### Multiple Input Paths (Enhanced Feature)

The tool now supports analyzing multiple JSON files and directories simultaneously:

```bash
# Analyze multiple directories
python3 json_to_sqlite.py challenges users products

# Mix files and directories
python3 json_to_sqlite.py data/users.json data/products/ logs/

# Analyze all JSON files in multiple locations
python3 json_to_sqlite.py ./data1/ ./data2/ specific_file.json
```

**Schema Merging**: When multiple JSON files are analyzed, the tool intelligently merges their schemas:
- **Field Union**: All fields from all files are included in the final schema
- **Type Promotion**: When the same field has different types across files, the most permissive type is chosen
- **Null Handling**: Fields that are null in some files become `Optional` in the Python classes

### Custom Output Files

```bash
# Using multiple inputs with custom output files
python3 json_to_sqlite.py challenges users products --output-sql unified_schema.sql --output-py unified_entities.py --output-db unified_data.db

# Using specific files
python3 json_to_sqlite.py data/users.json data/products.json --output-sql custom_schema.sql --output-py custom_entities.py --output-db custom_data.db
```

### Examples

```bash
# Analyze a specific JSON file (single input)
python3 json_to_sqlite.py challenges/challenges_1.json

# Analyze multiple directories (multiple inputs)
python3 json_to_sqlite.py challenges users products

# Mix files and directories
python3 json_to_sqlite.py challenges/challenges_1.json users/ products/products.json

# All generate:
# - schema.sql: Unified SQLite schema
# - entities.py: Unified Python entities
# - database.db: SQLite database with all JSON data inserted
```

## Generated Files

### schema.sql
Contains SQLite CREATE TABLE statements:
```sql
CREATE TABLE challenges (
    challenge_id TEXT,
    defendant_id TEXT,
    component_id TEXT,
    round_id TEXT,
    succeeded TEXT,
    submit_time TEXT,
    challenger_id TEXT,
    args TEXT,
    message TEXT,
    challenger_points TEXT,
    defendant_points TEXT,
    expected TEXT,
    received TEXT,
    status_id TEXT,
    check_answer_response TEXT
);
```

### entities.py
Contains Python dataclass entities with conversion methods:
```python
@dataclass
class Challenge:
    challenge_id: int
    defendant_id: int
    component_id: int
    round_id: int
    succeeded: int
    submit_time: int
    challenger_id: int
    args: str
    message: str
    challenger_points: float
    defendant_points: float
    expected: str
    received: str
    status_id: int
    check_answer_response: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> 'Challenge':
        # Automatic type conversion from JSON data
        return cls(...)
```

### database.db
Contains the actual SQLite database with tables created and all JSON data inserted:
```sql
-- Tables are created based on the generated schema
-- All JSON records are inserted with appropriate type conversions
-- Complex objects (arrays, nested objects) are stored as JSON strings
-- Numeric strings are converted to appropriate numeric types where detected
```

## Type Inference Rules

The script uses intelligent type inference:

1. **Strings that look like integers** (e.g., "12345") → `int` in Python, `TEXT` in SQLite
2. **Strings that look like floats** (e.g., "123.45") → `float` in Python, `TEXT` in SQLite  
3. **Null values** → `Optional[str]` in Python, `TEXT` in SQLite
4. **Regular strings** → `str` in Python, `TEXT` in SQLite
5. **Native numbers** → `int`/`float` in Python, `INTEGER`/`REAL` in SQLite

## Schema Merging Rules (Multiple Files)

When analyzing multiple JSON files, the tool merges schemas using these rules:

1. **Field Union**: All unique fields from all files are included in the final schema
2. **Type Promotion Hierarchy** (most to least permissive):
   - `Optional[str]` (most permissive - accommodates nulls)
   - `str` (string values)
   - `float` (numeric with decimals)
   - `int` (whole numbers)
   - `bool` (least permissive)
3. **Conflict Resolution**: When the same field has different types across files, the more permissive type is chosen
4. **Null Propagation**: If a field is null in any file, it becomes `Optional` in the final schema

**Example**: If `user_id` appears as `int` in one file and `"123"` (string) in another, the merged schema will use `int` with string-to-int conversion.

## Testing

Use the included test script to verify the generated entities work correctly:

```bash
python3 test_usage.py
```

This will load the JSON data and demonstrate the entity conversion process.

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Project Structure

```
to_sqlite/
├── json_to_sqlite.py    # Main script
├── test_usage.py        # Test/demo script
├── README.md           # This file
├── challenges/         # Sample data directory
│   └── challenges_1.json
├── schema.sql          # Generated SQLite schema
└── entities.py         # Generated Python entities
```