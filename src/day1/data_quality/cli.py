"""Command-line interface for data quality validation."""

import argparse
import sys
from pathlib import Path

from .validator import run_validation


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Data Quality Rules Engine - Validate transaction data"
    )
    
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Path to input CSV file'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('out/day1/lab1/validation_report.json'),
        help='Path to output JSON report (default: out/day1/lab1/validation_report.json)'
    )
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1
    
    print(f"Data Quality Validation")
    print(f"=" * 50)
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print()
    
    try:
        report = run_validation(args.input, args.output)
        
        print(f"✓ Validation completed!")
        print()
        print(f"Total transactions: {report.total_transactions}")
        print(f"Valid transactions: {report.valid_transactions}")
        print(f"Invalid transactions: {report.invalid_transactions}")
        print()
        
        if report.issues:
            print("Issues by severity:")
            for severity, count in sorted(report.issues_by_severity.items()):
                print(f"  {severity}: {count}")
            print()
            
            print("Issues by rule:")
            for rule, count in sorted(report.issues_by_rule.items()):
                print(f"  {rule}: {count}")
            print()
        
        print(f"Report written to: {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"Error: Validation failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
