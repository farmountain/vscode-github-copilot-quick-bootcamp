#!/usr/bin/env python3
"""
Evidence Bundle Collection Script for Day 3 Capstone

This script collects artifacts from the capstone project and packages them
into an evidence bundle for review and submission.

Evidence collected:
- Test output (pytest results)
- Coverage report
- Audit log sample
- Database schema
- Configuration snapshot
- Evidence manifest

Usage:
    python scripts/day3_collect_evidence.py
"""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def run_command(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    """Run a shell command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out after 5 minutes"
    except Exception as e:
        return -1, "", str(e)


def main():
    """Main evidence collection workflow."""
    print("=" * 70)
    print("Day 3 Capstone Evidence Bundle Collection")
    print("=" * 70)
    print()

    # Determine workspace root (parent of scripts/)
    workspace_root = Path(__file__).parent.parent.resolve()
    print(f"Workspace Root: {workspace_root}")
    print()

    # Setup evidence directory
    evidence_dir = workspace_root / "out" / "day3" / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)
    print(f"Evidence Directory: {evidence_dir}")
    print()

    # Timestamp for this run
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    evidence_manifest = {
        "collection_timestamp": timestamp,
        "workspace_root": str(workspace_root),
        "artifacts": []
    }

    # ========================================
    # 1. Run pytest and capture output
    # ========================================
    print("[1/7] Running pytest for Day 3 capstone...")
    test_output_file = evidence_dir / "test_output.txt"
    
    exit_code, stdout, stderr = run_command(
        ["pytest", "tests/day3/", "-v", "--tb=short"],
        cwd=workspace_root
    )
    
    with open(test_output_file, "w", encoding="utf-8") as f:
        f.write(f"=== pytest exit code: {exit_code} ===\n\n")
        f.write("=== STDOUT ===\n")
        f.write(stdout)
        f.write("\n\n=== STDERR ===\n")
        f.write(stderr)
    
    print(f"   ✓ Test output saved to {test_output_file.name}")
    evidence_manifest["artifacts"].append({
        "name": "test_output.txt",
        "description": "Pytest test results for Day 3",
        "exit_code": exit_code,
        "passed": exit_code == 0
    })
    print()

    # ========================================
    # 2. Generate coverage report
    # ========================================
    print("[2/7] Generating test coverage report...")
    coverage_file = evidence_dir / "coverage_report.txt"
    
    exit_code, stdout, stderr = run_command(
        [
            "pytest", "tests/day3/", "-v",
            "--cov=src.day3.credit_decisioning",
            "--cov-report=term-missing"
        ],
        cwd=workspace_root
    )
    
    with open(coverage_file, "w", encoding="utf-8") as f:
        f.write(f"=== pytest --cov exit code: {exit_code} ===\n\n")
        f.write("=== COVERAGE REPORT ===\n")
        f.write(stdout)
        if stderr:
            f.write("\n\n=== STDERR ===\n")
            f.write(stderr)
    
    print(f"   ✓ Coverage report saved to {coverage_file.name}")
    evidence_manifest["artifacts"].append({
        "name": "coverage_report.txt",
        "description": "Test coverage analysis",
        "exit_code": exit_code
    })
    print()

    # ========================================
    # 3. Copy audit log (if exists)
    # ========================================
    print("[3/7] Collecting audit log sample...")
    audit_log_src = workspace_root / "out" / "day3" / "audit_log.jsonl"
    audit_log_dst = evidence_dir / "audit_log_sample.jsonl"
    
    if audit_log_src.exists():
        # Copy only first 50 lines (or entire file if smaller)
        with open(audit_log_src, "r", encoding="utf-8") as src:
            lines = src.readlines()[:50]
        
        with open(audit_log_dst, "w", encoding="utf-8") as dst:
            dst.writelines(lines)
        
        print(f"   ✓ Audit log sample saved to {audit_log_dst.name} ({len(lines)} entries)")
        evidence_manifest["artifacts"].append({
            "name": "audit_log_sample.jsonl",
            "description": "First 50 audit log entries",
            "entries": len(lines)
        })
    else:
        print(f"   ⚠ Audit log not found at {audit_log_src}")
        evidence_manifest["artifacts"].append({
            "name": "audit_log_sample.jsonl",
            "description": "Audit log not found",
            "status": "missing"
        })
    print()

    # ========================================
    # 4. Extract database schema
    # ========================================
    print("[4/7] Extracting database schema...")
    db_file = workspace_root / "out" / "day3" / "credit_decisioning.db"
    schema_file = evidence_dir / "db_schema.sql"
    
    if db_file.exists():
        exit_code, stdout, stderr = run_command(
            ["sqlite3", str(db_file), ".schema"],
            cwd=workspace_root
        )
        
        with open(schema_file, "w", encoding="utf-8") as f:
            f.write("-- Database Schema for Credit Decisioning Service\n")
            f.write(f"-- Extracted: {timestamp}\n\n")
            f.write(stdout)
        
        print(f"   ✓ Database schema saved to {schema_file.name}")
        evidence_manifest["artifacts"].append({
            "name": "db_schema.sql",
            "description": "SQLite database schema",
            "exit_code": exit_code
        })
    else:
        print(f"   ⚠ Database not found at {db_file}")
        with open(schema_file, "w", encoding="utf-8") as f:
            f.write("-- Database not found\n")
        evidence_manifest["artifacts"].append({
            "name": "db_schema.sql",
            "description": "Database not found",
            "status": "missing"
        })
    print()

    # ========================================
    # 5. Capture configuration snapshot
    # ========================================
    print("[5/7] Capturing configuration snapshot...")
    config_snapshot_file = evidence_dir / "config_snapshot.json"
    
    config_snapshot = {
        "timestamp": timestamp,
        "python_version": sys.version,
        "environment_variables": {
            key: value for key, value in os.environ.items()
            if key.startswith("CREDIT_") or key in ["PYTHONPATH", "PATH"]
        },
        "workspace_structure": {
            "src": str(workspace_root / "src" / "day3"),
            "tests": str(workspace_root / "tests" / "day3"),
            "out": str(workspace_root / "out" / "day3")
        }
    }
    
    with open(config_snapshot_file, "w", encoding="utf-8") as f:
        json.dump(config_snapshot, f, indent=2)
    
    print(f"   ✓ Configuration snapshot saved to {config_snapshot_file.name}")
    evidence_manifest["artifacts"].append({
        "name": "config_snapshot.json",
        "description": "Environment and configuration at collection time"
    })
    print()

    # ========================================
    # 6. Generate evidence manifest
    # ========================================
    print("[6/7] Generating evidence manifest...")
    manifest_file = evidence_dir / "evidence_manifest.md"
    
    with open(manifest_file, "w", encoding="utf-8") as f:
        f.write("# Evidence Bundle Manifest\n\n")
        f.write(f"**Collection Timestamp:** {timestamp}\n\n")
        f.write(f"**Workspace Root:** `{workspace_root}`\n\n")
        f.write("---\n\n")
        f.write("## Artifacts Included\n\n")
        
        for idx, artifact in enumerate(evidence_manifest["artifacts"], start=1):
            f.write(f"### {idx}. {artifact['name']}\n\n")
            f.write(f"**Description:** {artifact['description']}\n\n")
            
            if "exit_code" in artifact:
                status = "✅ Pass" if artifact["exit_code"] == 0 else "❌ Fail"
                f.write(f"**Exit Code:** {artifact['exit_code']} ({status})\n\n")
            
            if "entries" in artifact:
                f.write(f"**Entries:** {artifact['entries']}\n\n")
            
            if "status" in artifact:
                f.write(f"**Status:** {artifact['status']}\n\n")
            
            f.write("---\n\n")
        
        f.write("## Verification Steps\n\n")
        f.write("1. Review `test_output.txt` for test results\n")
        f.write("2. Check `coverage_report.txt` for code coverage percentage\n")
        f.write("3. Inspect `audit_log_sample.jsonl` for PII exclusion\n")
        f.write("4. Review `db_schema.sql` for data model correctness\n")
        f.write("5. Verify `config_snapshot.json` for environment consistency\n\n")
        f.write("---\n\n")
        f.write("## Next Steps\n\n")
        f.write("- Verify all tests pass (exit code 0)\n")
        f.write("- Confirm audit log does NOT contain PII (full_name, address, email)\n")
        f.write("- Review coverage report (target: >80%)\n")
        f.write("- Submit evidence bundle for review\n\n")
    
    print(f"   ✓ Evidence manifest saved to {manifest_file.name}")
    print()

    # ========================================
    # 7. Create ZIP archive
    # ========================================
    print("[7/7] Creating evidence bundle ZIP archive...")
    zip_file = workspace_root / "out" / "day3" / f"evidence_bundle_{timestamp}.zip"
    
    with ZipFile(zip_file, "w", ZIP_DEFLATED) as zipf:
        for artifact_file in evidence_dir.glob("*"):
            if artifact_file.is_file():
                zipf.write(artifact_file, arcname=artifact_file.name)
    
    print(f"   ✓ Evidence bundle created: {zip_file.name}")
    print()

    # ========================================
    # Summary
    # ========================================
    print("=" * 70)
    print("Evidence Collection Complete")
    print("=" * 70)
    print()
    print(f"Evidence Bundle: {zip_file}")
    print(f"Evidence Directory: {evidence_dir}")
    print()
    print("Artifacts collected:")
    for artifact in evidence_manifest["artifacts"]:
        status_icon = "✅" if artifact.get("exit_code") == 0 or "exit_code" not in artifact else "⚠️"
        print(f"  {status_icon} {artifact['name']}")
    print()
    print("Review the evidence_manifest.md for details.")
    print()

    # Exit with test status
    test_artifact = evidence_manifest["artifacts"][0]  # First artifact is test output
    return 0 if test_artifact.get("passed", False) else 1


if __name__ == "__main__":
    sys.exit(main())
