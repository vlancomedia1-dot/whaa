from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple

@dataclass(frozen=True)
class Contact:
    phone: str

def _clean_phone(s: str) -> str:
    # keep digits and plus
    s = (s or "").strip()
    out = []
    for ch in s:
        if ch.isdigit() or ch == "+":
            out.append(ch)
    return "".join(out)

def load_contacts_from_csv(csv_path: str) -> Tuple[List[Contact], List[str]]:
    """Loads contacts from CSV.
    Accepts header: phone, number, mobile.
    Returns (contacts, errors).
    """
    p = Path(csv_path)
    if not p.exists():
        return [], [f"File not found: {csv_path}"]

    contacts: List[Contact] = []
    errors: List[str] = []

    with p.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return [], ["CSV has no header row."]
        fields = [h.strip().lower() for h in reader.fieldnames]
        candidates = ["phone", "number", "mobile", "msisdn"]
        col = None
        for c in candidates:
            if c in fields:
                col = reader.fieldnames[fields.index(c)]
                break
        if col is None:
            return [], [f"CSV header must include one of: {', '.join(candidates)}"]

        for i, row in enumerate(reader, start=2):
            raw = row.get(col, "")
            phone = _clean_phone(raw)
            if not phone:
                errors.append(f"Row {i}: empty phone value")
                continue
            contacts.append(Contact(phone=phone))

    # de-dup while preserving order
    seen = set()
    uniq = []
    for c in contacts:
        if c.phone in seen:
            continue
        seen.add(c.phone)
        uniq.append(c)
    return uniq, errors
