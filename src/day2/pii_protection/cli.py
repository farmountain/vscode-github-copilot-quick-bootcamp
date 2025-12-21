"""Command-line interface for PII protection."""

import argparse
import csv
import json
import sys
from pathlib import Path

from .config import ProtectionMode
from .masking import mask_field
from .tokenization import tokenize_field
from .redaction import redact_fields
from .audit import AuditEntry, write_audit_entry


def load_csv(csv_path: Path) -> list:
    """Load records from CSV file.
    
    Args:
        csv_path: Path to CSV file
        
    Returns:
        List of records (dicts)
    """
    records = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records


def write_csv(records: list, csv_path: Path) -> None:
    """Write records to CSV file.
    
    Args:
        records: List of records (dicts)
        csv_path: Path to output CSV file
    """
    if not records:
        return
    
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = records[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def protect_records(
    records: list,
    mode: ProtectionMode,
    fields_to_protect: set,
    secret_key: str,
    audit_log_path: Path,
    id_field: str = "customer_id"
) -> list:
    """Apply PII protection to records.
    
    Args:
        records: List of records to protect
        mode: Protection mode (MASK, TOKENIZE, REDACT)
        fields_to_protect: Set of field names to protect
        secret_key: Secret key for tokenization
        audit_log_path: Path to audit log file
        id_field: Field name to use as record ID for audit
        
    Returns:
        List of protected records
    """
    protected = []
    
    for record in records:
        record_id = record.get(id_field, "unknown")
        protected_record = record.copy()
        
        if mode == ProtectionMode.MASK:
            for field in fields_to_protect:
                if field in protected_record:
                    protected_record[field] = mask_field(field, protected_record[field])
        
        elif mode == ProtectionMode.TOKENIZE:
            for field in fields_to_protect:
                if field in protected_record:
                    protected_record[field] = tokenize_field(field, protected_record[field], secret_key)
        
        elif mode == ProtectionMode.REDACT:
            protected_record = redact_fields(protected_record, fields_to_protect)
        
        protected.append(protected_record)
        
        # Write audit entry
        audit_entry = AuditEntry(
            operation=mode.value,
            record_id=str(record_id),
            fields_protected=list(fields_to_protect)
        )
        write_audit_entry(audit_entry, audit_log_path)
    
    return protected


def main():
    """Main CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="PII Protection - Mask, tokenize, or redact sensitive data"
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
        default=Path('out/day2/lab4/protected_data.csv'),
        help='Path to output CSV file (default: out/day2/lab4/protected_data.csv)'
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['MASK', 'TOKENIZE', 'REDACT'],
        required=True,
        help='Protection mode: MASK, TOKENIZE, or REDACT'
    )
    
    parser.add_argument(
        '--fields',
        type=str,
        required=True,
        help='Comma-separated list of fields to protect'
    )
    
    parser.add_argument(
        '--secret-key',
        type=str,
        default='default-secret-key-change-in-production',
        help='Secret key for tokenization (default: default-secret-key-change-in-production)'
    )
    
    parser.add_argument(
        '--audit-log',
        type=Path,
        default=Path('out/day2/lab4/audit.jsonl'),
        help='Path to audit log file (default: out/day2/lab4/audit.jsonl)'
    )
    
    args = parser.parse_args()
    
    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        return 1
    
    print(f"PII Protection Service")
    print(f"=" * 50)
    print(f"Mode: {args.mode}")
    print(f"Input: {args.input}")
    print(f"Output: {args.output}")
    print(f"Fields: {args.fields}")
    print(f"Audit Log: {args.audit_log}")
    print()
    
    try:
        # Parse fields
        fields_to_protect = set(f.strip() for f in args.fields.split(','))
        
        # Load records
        records = load_csv(args.input)
        print(f"Loaded {len(records)} records")
        print()
        
        # Apply protection
        protected_records = protect_records(
            records=records,
            mode=ProtectionMode(args.mode),
            fields_to_protect=fields_to_protect,
            secret_key=args.secret_key,
            audit_log_path=args.audit_log
        )
        
        # Write protected records
        write_csv(protected_records, args.output)
        
        print(f"✓ Protection completed!")
        print(f"Protected {len(protected_records)} records")
        print(f"Output written to: {args.output}")
        print(f"Audit log written to: {args.audit_log}")
        
        return 0
        
    except Exception as e:
        print(f"Error: Protection failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
