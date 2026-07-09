from pathlib import Path

root = Path(__file__).resolve().parent.parent
sample_dir = root / "data" / "uploads"
sample_dir.mkdir(parents=True, exist_ok=True)

(sample_dir / "sample-policy.txt").write_text(
    "Employees receive 20 working days of annual leave each year. The policy applies to full-time employees.",
    encoding="utf-8",
)

(sample_dir / "sample-report.txt").write_text(
    "The report highlights three key risks: vendor concentration, regulatory change, and data retention compliance.",
    encoding="utf-8",
)
