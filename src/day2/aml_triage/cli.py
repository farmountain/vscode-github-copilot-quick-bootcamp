"""Command-line interface for AML Triage Pipeline.

Usage:
    python -m src.day2.aml_triage.cli --input <csv_path> --outdir <output_directory>
"""

import argparse
import sys
from pathlib import Path

from . import pipeline


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="AML Alert Triage Pipeline - Process transactions and generate alert triage queue"
    )
    
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Path to input CSV file containing transactions'
    )
    
    parser.add_argument(
        '--outdir',
        type=Path,
        default=Path('out/day2/lab3'),
        help='Output directory for results (default: out/day2/lab3)'
    )
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1
    
    print(f"AML Alert Triage Pipeline")
    print(f"=" * 50)
    print(f"Input file: {args.input}")
    print(f"Output directory: {args.outdir}")
    print()
    
    try:
        # Run pipeline
        summary = pipeline.run_pipeline(args.input, args.outdir)
        
        # Print summary
        print(f"✓ Pipeline completed successfully!")
        print()
        print(f"Processed {summary['total_transactions']} transactions")
        print(f"Generated {summary['total_alerts']} alerts")
        print()
        
        if summary['total_alerts'] > 0:
            print("Priority breakdown:")
            by_priority = summary.get('by_priority', {})
            print(f"  P1 (Critical): {by_priority.get('P1', 0)}")
            print(f"  P2 (High):     {by_priority.get('P2', 0)}")
            print(f"  P3 (Medium):   {by_priority.get('P3', 0)}")
            print()
        
        print(f"Outputs written to: {args.outdir}/")
        print(f"  - aml_alerts.json")
        print(f"  - triage_queue.csv")
        print(f"  - summary.json")
        
        return 0
        
    except Exception as e:
        print(f"Error: Pipeline failed: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
