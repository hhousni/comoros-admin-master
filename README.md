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

## Fiches du catalogue / Catalog records

Textes du champ « Description » des tables de référence sur Comores Open Data (français, puis anglais). Licence : CC BY 4.0 (source OCHA : CC BY-IGO). Fréquence : `once`, mise à jour à chaque correction (voir `CHANGELOG.md`).
Description field of the reference tables on Comores Open Data (French, then English). Licence: CC BY 4.0 (OCHA source: CC BY-IGO). Frequency: `once`, updated with each correction (see `CHANGELOG.md`).

### Table de référence du pays (`master_country.csv`)

Table de référence du pays : identifiant administratif (KM) et nom officiel des Comores. Point de départ de la hiérarchie pays → île → préfecture → commune → village utilisée par tous les jeux de données de Comores Open Data.
Niveau géographique : pays
Colonnes : country_name, country_id
Source : OCHA COD-AB Comores (COSEP), version v01 du 5 décembre 2019, via HDX.

EN: Country reference table: administrative ID (KM) and official name of the Comoros. Top of the country → island → prefecture → commune → village hierarchy used by every Comores Open Data dataset.
Source: OCHA COD-AB Comoros (COSEP), version v01, 5 December 2019, via HDX.

### Table de référence des îles (`master_island.csv`)

Table de référence des trois îles des Comores : identifiant (KM1 Anjouan, KM2 Grande Comore, KM3 Mohéli), nom français et nom comorien (Ndzouani, Ngazidja, Mwali).
Niveau géographique : île
Colonnes : country_id, island_id, island_name_fr, island_name_local
Source : OCHA COD-AB Comores (COSEP), version v01 du 5 décembre 2019, via HDX.

EN: Reference table of the three islands of the Comoros: ID (KM1 Anjouan, KM2 Grande Comore, KM3 Mohéli), French name and Comorian name (Ndzouani, Ngazidja, Mwali).
Source: OCHA COD-AB Comoros (COSEP), version v01, 5 December 2019, via HDX.

### Table de référence des préfectures (`master_prefecture.csv`)

Table de référence des 17 préfectures des Comores, avec leur identifiant et leur île. Suit la liste de l'OCHA : la commune de Moya fait partie de la préfecture de Sima, et Mboudé forme une seule préfecture avec Mitsamiouli (Mitsamiouli-Mboudé). Kartala (KM29) correspond à la zone inhabitée du cratère du Karthala.
Niveau géographique : préfecture
Colonnes : prefecture_name, prefecture_id, island_id, country_id
Source : OCHA COD-AB Comores (COSEP), version v01 du 5 décembre 2019, via HDX.

EN: Reference table of the 17 prefectures of the Comoros, with their ID and island. Follows the OCHA list: the commune of Moya is part of Sima prefecture, and Mboudé forms one prefecture with Mitsamiouli (Mitsamiouli-Mboudé). Kartala (KM29) is the uninhabited Karthala crater zone.
Source: OCHA COD-AB Comoros (COSEP), version v01, 5 December 2019, via HDX.

### Table de référence des communes (`master_commune.csv`)

Table de référence des 55 communes des Comores, avec leur identifiant, leur préfecture et leur île. La commune KM291 « Cratère du Karthala » est inhabitée.
Niveau géographique : commune
Colonnes : commune_name, commune_id, prefecture_id, island_id, country_id
Source : OCHA COD-AB Comores (COSEP), version v01 du 5 décembre 2019, via HDX.

EN: Reference table of the 55 communes of the Comoros, with their ID, prefecture and island. Commune KM291 "Cratère du Karthala" is uninhabited.
Source: OCHA COD-AB Comoros (COSEP), version v01, 5 December 2019, via HDX.

### Table de référence des villages et localités (`master_town_village.csv`)

Table de référence des 319 villages et localités des Comores, avec leur identifiant, leur commune et, pour 205 d'entre eux, leurs coordonnées GPS. Chaque coordonnée a été vérifiée : elle tombe dans le contour officiel de sa commune. Les coordonnées manquantes sont laissées vides plutôt que devinées.
Mise à jour du 31 octobre 2026 : 19 doublons supprimés, villages de Moya rattachés à la préfecture de Sima, 6 coordonnées fausses effacées. Les identifiants conservés n'ont pas changé.
Niveau géographique : village / localité
Colonnes : country_id, island_id, prefecture_id, commune_id, town_village_id, town_village_name, latitude, longitude
Sources : liste des villages des projections démographiques de l'INSEED (2017–2042) ; communes OCHA COD-AB Comores (COSEP), v01.

EN: Reference table of the 319 towns and villages of the Comoros, with their ID, commune and, for 205 of them, GPS coordinates. Every coordinate was checked to fall within the official boundary of its commune; missing coordinates are left empty rather than guessed.
Update of 31 October 2026: 19 duplicates removed, Moya villages attached to Sima prefecture, 6 wrong coordinates cleared. IDs that were kept are unchanged.
Sources: village list of the INSEED population projections (2017–2042); communes from OCHA COD-AB Comoros (COSEP), v01.
