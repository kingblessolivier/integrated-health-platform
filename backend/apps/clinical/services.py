"""Pure clinical helpers (no DB) — unit-tested in tests.py."""
import re

# ICD-10 form: a letter, two digits, optional dotted subdivision (e.g. B54, J18.9, A15.0).
_ICD10 = re.compile(r"^[A-Z][0-9]{2}(?:\.[0-9A-Za-z]{1,4})?$")


def is_valid_icd(code: str) -> bool:
    """True if `code` is a well-formed ICD-10 code (validated before a diagnosis is saved)."""
    return bool(code) and bool(_ICD10.match(code))
