"""Explicit corrections to masters/master_town_village.csv.

The village table was first built by scripts/creating_master_admin.py from inputs that are not in
this repo, so it cannot be regenerated. From now on the CSV is the source of truth and every change
to it is listed here, with its reason. Running this script again changes nothing.

Run from the repo root:  python3 scripts/correct_town_village.py
"""
import csv
from pathlib import Path

MASTER = Path(__file__).resolve().parent.parent / "masters" / "master_town_village.csv"

# 2026-10-31 — phantom rows. Each village name shared by two communes was copied into both
# communes (with the other commune's coordinates), so each of these communes listed the name twice.
# The row kept is the one the INSEED population files use; these IDs were never used by any dataset.
PHANTOM_ROWS = [
    "KM112_0002",  # DOMONI, twin of KM112_0001
    "KM115_0004",  # SALAMANI, twin of KM115_0003
    "KM121_0005",  # KANGANI, twin of KM121_0004
    "KM131_0005",  # MAWENI, twin of KM131_0004
    "KM143_0002",  # BARAKANI, twin of KM143_0003
    "KM151_0007",  # MAWENI, twin of KM151_0006
    "KM152_0006",  # MILEMBENI, twin of KM152_0007
    "KM153_0013",  # SALAMANI, twin of KM153_0014
    "KM234_0004",  # MILEMBENI, twin of KM234_0003
    "KM241_0006",  # PIDJANI, twin of KM241_0005
    "KM252_0007",  # DOMONI, twin of KM252_0006
    "KM262_0003",  # KOUA, twin of KM262_0002
    "KM264_0003",  # PIDJANI, twin of KM264_0004
    "KM265_0009",  # KOUA, twin of KM265_0008
    "KM271_0009",  # DZAHANI, twin of KM271_0008
    "KM283_0002",  # DZAHANI, twin of KM283_0003
    "KM311_0004",  # KANGANI, twin of KM311_0005
    "KM323_0004",  # DOMONI, twin of KM323_0003
    "KM332_0003",  # BARAKANI, twin of KM332_0002
]

# 2026-10-31 — commune Moya (KM151) belongs to prefecture Sima (KM15), as in master_commune.csv
# and law 11-006/AU of 2 May 2011 (art. 7). Its villages pointed to KM16, which does not exist.
PREFECTURE_FIXES = {"KM151": "KM15"}

# 2026-10-31 — coordinates cleared rather than guessed: checked against the OCHA COD-AB commune
# boundaries (v01, 2019-12-05), they fall in another commune, or two villages share one point.
WRONG_COORDINATES = [
    "KM152_0001",  # SIMA (Anjouan): point of SIMA in Grande Comore (KM232_0003), 115 km away
    "KM131_0008",  # BANDRADJOU: inside Mirontsi (KM133), 5.3 km from its commune
    "KM211_0008",  # BANDAMADJI LA MBOIKOU: inside Nyuma Mro (KM212), 3.5 km from its commune
    "KM265_0008",  # KOUA: point of KOUA in KM262 (same coordinates as KM262_0002)
    "KM251_0008",  # TSINI MOICHONGO: same point as KANDZILE (KM251_0009); which one is right is unknown
    "KM251_0009",  # KANDZILE: same point as TSINI MOICHONGO (KM251_0008)
]


def main():
    with MASTER.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        rows = list(reader)

    ids = {r["town_village_id"] for r in rows}
    unknown = [i for i in WRONG_COORDINATES if i not in ids]
    if unknown:
        raise SystemExit(f"Unknown IDs in WRONG_COORDINATES: {unknown}")

    before = len(rows)
    rows = [r for r in rows if r["town_village_id"] not in PHANTOM_ROWS]
    for r in rows:
        if r["commune_id"] in PREFECTURE_FIXES:
            r["prefecture_id"] = PREFECTURE_FIXES[r["commune_id"]]
        if r["town_village_id"] in WRONG_COORDINATES:
            r["latitude"] = r["longitude"] = ""

    with MASTER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{MASTER.name}: {before} rows -> {len(rows)} rows")


if __name__ == "__main__":
    main()
