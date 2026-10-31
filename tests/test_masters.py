"""Checks every master table must pass before it is published or used by another repo."""
import json
import math
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
MASTERS = ROOT / "masters"
OCHA = ROOT / "raw" / "ocha_cod_ab"


def master(name):
    return pd.read_csv(MASTERS / f"master_{name}.csv", dtype=str, keep_default_na=False)


country, island, prefecture, commune, village = (
    master(n) for n in ["country", "island", "prefecture", "commune", "town_village"]
)
LEVELS = [
    (country, "country_id"),
    (island, "island_id"),
    (prefecture, "prefecture_id"),
    (commune, "commune_id"),
    (village, "town_village_id"),
]


@pytest.mark.parametrize("table, id_col", LEVELS)
def test_ids_unique_and_no_empty_cell(table, id_col):
    assert not table[id_col].duplicated().any()
    filled = table.drop(columns=[c for c in ["latitude", "longitude"] if c in table])
    assert not (filled.apply(lambda col: col.str.strip()) == "").any().any()
    assert (table == table.apply(lambda col: col.str.strip())).all().all()


def test_parents_exist_and_ids_nest():
    # child table, child id, parent table, parent id
    for child, cid, parent, pid in [
        (island, "island_id", country, "country_id"),
        (prefecture, "prefecture_id", island, "island_id"),
        (commune, "commune_id", prefecture, "prefecture_id"),
        (village, "commune_id", commune, "commune_id"),
    ]:
        assert set(child[pid]) <= set(parent[pid]), f"{cid}: unknown {pid}"
    assert all(p.startswith(i) for p, i in zip(prefecture.prefecture_id, prefecture.island_id))
    assert all(c.startswith(p) for c, p in zip(commune.commune_id, commune.prefecture_id))
    assert all(v.startswith(c + "_") for v, c in zip(village.town_village_id, village.commune_id))


def test_every_row_repeats_the_parents_of_its_commune():
    by_prefecture = prefecture.set_index("prefecture_id")
    for row in commune.itertuples():
        assert row.island_id == by_prefecture.loc[row.prefecture_id, "island_id"], row.commune_id
    by_commune = commune.set_index("commune_id")
    wrong = [
        row.town_village_id
        for row in village.itertuples()
        if (row.prefecture_id, row.island_id, row.country_id)
        != tuple(by_commune.loc[row.commune_id, ["prefecture_id", "island_id", "country_id"]])
    ]
    assert not wrong, f"villages whose parents differ from their commune: {wrong[:10]}"


def test_no_village_listed_twice_in_a_commune():
    twice = village[village.duplicated(["commune_id", "town_village_name"], keep=False)]
    assert twice.empty, twice[["town_village_id", "town_village_name"]].values.tolist()


def test_ids_never_disappear():
    """An ID, once published, keeps its meaning. Removing one must be a deliberate edit of known_ids.txt."""
    known = (Path(__file__).parent / "known_ids.txt").read_text().split()
    current = set().union(*(set(t[c]) for t, c in LEVELS))
    missing = [i for i in known if i not in current]
    assert not missing, f"IDs removed from the masters: {missing}"


def test_country_to_commune_match_ocha_cod_ab():
    """Codes, names and parents of the first four levels are those of the OCHA COD-AB (v01, 2019-12-05)."""
    ocha = pd.read_excel(OCHA / "com_admin_boundaries.xlsx", sheet_name=None)
    a0, a1, a2, a3 = (ocha[f"com_admin{i}"] for i in range(4))
    assert dict(zip(a0.adm0_pcode, a0.adm0_name)) == dict(zip(country.country_id, country.country_name))
    # OCHA writes "Anjouan (Ndzouani)": French name, then local name in brackets
    assert dict(zip(a1.adm1_pcode, a1.adm1_name)) == {
        i: f"{fr} ({local})" for i, fr, local in zip(island.island_id, island.island_name_fr, island.island_name_local)
    }
    assert dict(zip(a2.adm2_pcode, zip(a2.adm2_name, a2.adm1_pcode))) == dict(
        zip(prefecture.prefecture_id, zip(prefecture.prefecture_name, prefecture.island_id))
    )
    assert dict(zip(a3.adm3_pcode, zip(a3.adm3_name, a3.adm2_pcode))) == dict(
        zip(commune.commune_id, zip(commune.commune_name, commune.prefecture_id))
    )


# --- village coordinates ------------------------------------------------------------------

def _in_ring(x, y, ring):
    inside = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            inside = not inside
    return inside


def _km(x1, y1, x2, y2):
    return math.hypot((x2 - x1) * 111.32 * math.cos(math.radians(y1)), (y2 - y1) * 110.57)


def _km_outside(x, y, polygons):
    """0 if the point is inside the commune, else its distance to the commune border in km."""
    if any(_in_ring(x, y, p[0]) and not any(_in_ring(x, y, h) for h in p[1:]) for p in polygons):
        return 0.0
    best = math.inf
    for ring in (r for p in polygons for r in p):
        for (x1, y1), (x2, y2) in zip(ring, ring[1:]):
            dx, dy = x2 - x1, y2 - y1
            t = 0 if dx == dy == 0 else max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
            best = min(best, _km(x, y, x1 + t * dx, y1 + t * dy))
    return best


def test_latitude_and_longitude_filled_together():
    assert ((village.latitude == "") == (village.longitude == "")).all()


def test_village_coordinates_fall_in_their_commune():
    """Within 1 km of the OCHA commune boundary (borders and coastlines are drawn roughly)."""
    shapes = {}
    for f in json.loads((OCHA / "com_admin3.geojson").read_text())["features"]:
        g = f["geometry"]
        shapes[f["properties"]["adm3_pcode"]] = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
    located = village[village.latitude != ""]
    far = [
        (r.town_village_id, r.town_village_name, round(d, 1))
        for r in located.itertuples()
        if (d := _km_outside(float(r.longitude), float(r.latitude), shapes[r.commune_id])) > 1
    ]
    assert not far, f"villages more than 1 km outside their commune: {far}"


def test_no_two_villages_share_a_point():
    located = village[village.latitude != ""]
    shared = located[located.duplicated(["latitude", "longitude"], keep=False)]
    assert shared.empty, shared[["town_village_id", "town_village_name"]].values.tolist()
