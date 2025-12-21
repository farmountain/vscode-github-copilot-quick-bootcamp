"""End-to-end demo script for the credit decisioning API."""
import httpx


API_BASE_URL = "http://127.0.0.1:8000"


def run_demo() -> None:
    """Run end-to-end demo of the credit decisioning service."""
    print("=== Credit Decisioning E2E Demo ===\n")
    
    # Define sample applications
    samples = [
        {
            "name": "Safe Applicant (expect APPROVE)",
            "data": {
                "full_name": "Demo Safe",
                "annual_income": 70000,
                "monthly_debt_payments": 1000,
                "requested_amount": 12000,
                "employment_years": 7,
                "missed_payments_12m": 0,
                "address": "123 Demo St, Testville",
                "email": "demo.safe@example.com"
            }
        },
        {
            "name": "Risky Applicant (expect DECLINE)",
            "data": {
                "full_name": "Demo Risky",
                "annual_income": 35000,
                "monthly_debt_payments": 1500,
                "requested_amount": 20000,
                "employment_years": 1,
                "missed_payments_12m": 4,
                "address": "456 Demo Ave, Testville",
                "email": "demo.risky@example.com"
            }
        },
        {
            "name": "Borderline Applicant (expect REFER)",
            "data": {
                "full_name": "Demo Borderline",
                "annual_income": 50000,
                "monthly_debt_payments": 1400,
                "requested_amount": 15000,
                "employment_years": 3,
                "missed_payments_12m": 1,
                "address": "789 Demo Blvd, Testville",
                "email": "demo.borderline@example.com"
            }
        }
    ]
    
    # Process each sample
    for i, sample in enumerate(samples, 1):
        print(f"Application {i}: {sample['name']}")
        print("-" * 60)
        
        try:
            # Submit application
            response = httpx.post(f"{API_BASE_URL}/applications", json=sample['data'], timeout=10.0)
            response.raise_for_status()
            app_id = response.json()['application_id']
            print(f"  Application ID: {app_id}")
            
            # Compute decision
            response = httpx.post(f"{API_BASE_URL}/applications/{app_id}/decision", timeout=10.0)
            response.raise_for_status()
            decision = response.json()
            
            print(f"  Decision: {decision['outcome']} (score: {decision['score']})")
            print(f"  Reason codes: {decision['reason_codes']}")
            print()
            
        except httpx.HTTPError as e:
            print(f"  ERROR: {e}")
            print()
    
    print("=== Demo Complete ===")
    print("\nTo view audit log:")
    print("  Get-Content out\\day3\\audit_log.jsonl")
    print("\nTo retrieve decision by ID:")
    print("  Invoke-RestMethod -Uri http://127.0.0.1:8000/decisions/{decision_id}")


if __name__ == "__main__":
    run_demo()
