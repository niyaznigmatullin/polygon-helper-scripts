#!/usr/bin/env python3
"""
Example usage of the Polygon Validator Writer script.

This demonstrates how to use the script programmatically.
"""

import os
from write_validators import PolygonValidatorWriter

def main():
    # Example configuration
    api_url = "https://polygon.codeforces.com/api"
    api_key = os.getenv("POLYGON_API_KEY", "your_api_key_here")
    api_secret = os.getenv("POLYGON_API_SECRET", "your_api_secret_here")
    contest_id = 12345  # Replace with your contest ID
    model = "gpt-4"  # or "gpt-3.5-turbo", "claude-3-sonnet-20240229", etc.
    
    # Initialize the validator writer
    writer = PolygonValidatorWriter(api_url, api_key, api_secret, model)
    
    # First, do a dry run to see what would be processed
    print("=== DRY RUN ===")
    writer.process_contest(contest_id, dry_run=True)
    
    # Ask for confirmation before proceeding
    response = input("\nProceed with adding validators? (y/N): ")
    if response.lower() == 'y':
        print("\n=== PROCESSING ===")
        writer.process_contest(contest_id, dry_run=False)
    else:
        print("Cancelled.")

if __name__ == "__main__":
    main()