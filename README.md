# Comoros Admin Master

Canonical administrative reference tables for the Comoros: one stable ID and one name per country, island, prefecture, commune and town / village. Every dataset published on [Comores Open Data](https://comoresopendata.org) uses these IDs.

## Tables (`masters/`)

| File | Rows | Columns |
|---|---|---|
| `master_country.csv` | 1 | `country_name`, `country_id` |
| `master_island.csv` | 3 | `country_id`, `island_id`, `island_name_fr`, `island_name_local` |
| `master_prefecture.csv` | 17 | `prefecture_name`, `prefecture_id`, `island_id`, `country_id` |
| `master_commune.csv` | 55 | `commune_name`, `commune_id`, `prefecture_id`, `island_id`, `country_id` |
| `master_town_village.csv` | 319 | `country_id`, `island_id`, `prefecture_id`, `commune_id`, `town_village_id`, `town_village_name`, `latitude`, `longitude` |

IDs nest: `KM` → island `KM1` → prefecture `KM15` → commune `KM151` → village `KM151_0001`.

## Sources

- **Country → commune**: OCHA COD-AB for the Comoros, provided by COSEP (Centre des opérations de secours et de la protection civile), version v01, valid from 2019-12-05 — [HDX `cod-ab-com`](https://data.humdata.org/dataset/cod-ab-com), licence CC BY-IGO. Copy in `raw/ocha_cod_ab/` (downloaded 2026-10-31). The tests check that codes, names and parents match it.
- **Towns / villages**: the village list of the INSEED population projections (2017–2042, medium hypothesis), one row per village, under its commune. Not an official list: villages have no OCHA code.
- **Village coordinates**: geocoded by name (origin not recorded). 205 of 319 villages have coordinates; each one is checked against the OCHA commune boundaries. Missing coordinates are left empty rather than guessed.

Notes:
- Prefecture `KM29` Kartala has one commune, `KM291` Cratère du Karthala, the uninhabited crater zone: it has no village.
- The 2011 law (loi 11-006/AU) lists 16 prefectures and INSEED 18 (Moya and Mboudé separate). These tables follow OCHA (17): commune Moya `KM151` is in prefecture Sima `KM15`; Mboudé and Mitsamiouli form one prefecture, Mitsamiouli-Mboudé `KM26`.

## Rules

- **An ID never changes meaning and is never reused.** New units get a new ID; a removed unit's ID is not given to another one. `tests/known_ids.txt` lists every ID; removing one from the tables makes the tests fail until it is removed from that list on purpose (and noted in `CHANGELOG.md`).
- Every change to `master_town_village.csv` goes through `scripts/correct_town_village.py`, with its reason, and is noted in `CHANGELOG.md`.
- Run the tests before publishing or before updating another repo that uses these tables.

## Commands

```bash
pip install -r requirements.txt
python3 scripts/correct_town_village.py   # applies the listed corrections (running it twice changes nothing)
python3 -m pytest -q                      # checks the tables
```

`scripts/creating_master_admin.py` built the first version (2026-09) from inputs that are not in this repo; it is kept for history and cannot be re-run.

## Example

```python
import pandas as pd

commune = pd.read_csv("masters/master_commune.csv", dtype=str)
village = pd.read_csv("masters/master_town_village.csv", dtype=str)
```
