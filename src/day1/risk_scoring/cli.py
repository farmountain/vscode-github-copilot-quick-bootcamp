"""Command-line interface for risk scoring."""

import argparse
import json
import sys
from pathlib import Path

from .models import CreditApplication
from .risk_engine import assess_risk


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Risk Scoring Service - Assess credit risk"
    )
    
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Path to input JSON file with applications'
    )
    
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('out/day1/lab2/risk_assessments.json'),
        help='Path to output JSON file (default: out/day1/lab2/risk_assessments.json)'
    )
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1
    
    print(f"Risk Scoring Service")
    print(f"=" * 50)
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print()
    
    try:
        # Load applications
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        applications = [CreditApplication(**app) for app in data]
        print(f"Loaded {len(applications)} applications")
        print()
        
        # Assess each application
        results = []
        decisions_count = {"APPROVED": 0, "MANUAL_REVIEW": 0, "DECLINED": 0}
        
        for app in applications:
            assessment = assess_risk(app)
            results.append(assessment.model_dump(mode='json'))
            decisions_count[assessment.decision.value] += 1
            
            print(f"Application {app.application_id}:")
            print(f"  Total Score: {assessment.total_score}/100")
            print(f"  Risk Level: {assessment.risk_level.value}")
            print(f"  Decision: {assessment.decision.value}")
            print()
        
        # Write results
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"✓ Assessment completed!")
        print()
        print("Decision Summary:")
        print(f"  Approved: {decisions_count['APPROVED']}")
        print(f"  Manual Review: {decisions_count['MANUAL_REVIEW']}")
        print(f"  Declined: {decisions_count['DECLINED']}")
        print()
        print(f"Results written to: {args.output}")
        
        return 0
        
    except Exception as e:
        print(f"Error: Assessment failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
