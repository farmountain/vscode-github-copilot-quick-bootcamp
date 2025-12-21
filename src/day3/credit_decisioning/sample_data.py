"""Synthetic sample data generator for credit applications."""
import json
from pathlib import Path

from . import config


def generate_samples() -> list[dict]:
    """Generate synthetic sample applications with variety.
    
    Returns:
        List of 10 sample application dicts (some safe, some risky, some borderline, some edge cases)
    """
    samples = [
        # Safe applicants (expect APPROVE)
        {
            "full_name": "Alice Safe",
            "annual_income": 80000,
            "monthly_debt_payments": 800,
            "requested_amount": 10000,
            "employment_years": 8,
            "missed_payments_12m": 0,
            "address": "456 Oak St, Testville",
            "email": "alice.safe@example.com"
        },
        {
            "full_name": "Bob Secure",
            "annual_income": 90000,
            "monthly_debt_payments": 1500,
            "requested_amount": 12000,
            "employment_years": 10,
            "missed_payments_12m": 0,
            "address": "789 Pine Ave, Testville",
            "email": "bob.secure@example.com"
        },
        {
            "full_name": "Carol Trusted",
            "annual_income": 70000,
            "monthly_debt_payments": 1200,
            "requested_amount": 15000,
            "employment_years": 6,
            "missed_payments_12m": 0,
            "address": "321 Maple Dr, Testville",
            "email": "carol.trusted@example.com"
        },
        # Risky applicants (expect DECLINE)
        {
            "full_name": "David Risky",
            "annual_income": 30000,
            "monthly_debt_payments": 1200,
            "requested_amount": 20000,
            "employment_years": 1,
            "missed_payments_12m": 5,
            "address": "111 Danger Rd, Testville",
            "email": "david.risky@example.com"
        },
        {
            "full_name": "Eve Unstable",
            "annual_income": 35000,
            "monthly_debt_payments": 1500,
            "requested_amount": 18000,
            "employment_years": 0,
            "missed_payments_12m": 4,
            "address": "222 Risk Blvd, Testville",
            "email": "eve.unstable@example.com"
        },
        {
            "full_name": "Frank Shaky",
            "annual_income": 40000,
            "monthly_debt_payments": 2000,
            "requested_amount": 25000,
            "employment_years": 1,
            "missed_payments_12m": 3,
            "address": "333 Worry Ln, Testville",
            "email": "frank.shaky@example.com"
        },
        # Borderline applicants (expect REFER)
        {
            "full_name": "Grace Borderline",
            "annual_income": 50000,
            "monthly_debt_payments": 1400,
            "requested_amount": 15000,
            "employment_years": 3,
            "missed_payments_12m": 1,
            "address": "444 Middle St, Testville",
            "email": "grace.borderline@example.com"
        },
        {
            "full_name": "Henry Moderate",
            "annual_income": 55000,
            "monthly_debt_payments": 1600,
            "requested_amount": 14000,
            "employment_years": 4,
            "missed_payments_12m": 2,
            "address": "555 Average Ave, Testville",
            "email": "henry.moderate@example.com"
        },
        # Edge cases
        {
            "full_name": "Ivy Edge1",
            "annual_income": 60000,
            "monthly_debt_payments": 1800,  # DTI = 0.36 exactly
            "requested_amount": 12000,
            "employment_years": 5,  # exactly 5 years
            "missed_payments_12m": 0,
            "address": "666 Edge Case Rd, Testville",
            "email": "ivy.edge1@example.com"
        },
        {
            "full_name": "Jack Edge2",
            "annual_income": 50000,
            "monthly_debt_payments": 1000,
            "requested_amount": 15000,  # 30% of income exactly
            "employment_years": 2,  # exactly 2 years
            "missed_payments_12m": 0,
            "address": "777 Boundary St, Testville",
            "email": "jack.edge2@example.com"
        }
    ]
    
    return samples


def save_samples(samples: list[dict], output_path: Path) -> None:
    """Save samples to JSON file.
    
    Args:
        samples: List of sample application dicts
        output_path: Path to save JSON file
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(samples, f, indent=2)


if __name__ == "__main__":
    print("=== Generating Sample Applications ===\n")
    
    samples = generate_samples()
    
    # Print summary
    print(f"Generated {len(samples)} sample applications:")
    print(f"  - 3 safe (expect APPROVE)")
    print(f"  - 3 risky (expect DECLINE)")
    print(f"  - 2 borderline (expect REFER)")
    print(f"  - 2 edge cases")
    print()
    
    # Save to file
    output_path = config.BASE_OUTPUT_DIR / "sample_requests.json"
    save_samples(samples, output_path)
    print(f"Saved samples to: {output_path}")
    print("\nSample names:")
    for sample in samples:
        print(f"  - {sample['full_name']}")
