# Comoros Admin Master

This repository contains the canonical administrative reference tables for the Comoros.

## Contents

The master tables are published in both Excel and CSV formats under the `masters/` directory:

- `master_country.csv` / `master_country.xlsx`
- `master_island.csv` / `master_island.xlsx`
- `master_prefecture.csv` / `master_prefecture.xlsx`
- `master_commune.csv` / `master_commune.xlsx`
- `master_town_village.csv` / `master_town_village.xlsx`

## Purpose

These tables provide a reusable, stable administrative hierarchy that can be joined in other projects:

- country
- island
- prefecture
- commune
- town_village

Each row contains the official administrative IDs and the related names so downstream datasets can remain consistent across projects.

## Source and maintenance

The source script is available in `scripts/creating_master_admin.py`.

This repository is intended as the authoritative admin-reference layer. It should be reused by analysis and publication projects rather than recreated in each project.

## Example usage

```python
import pandas as pd

country = pd.read_csv('masters/master_country.csv')
commune = pd.read_csv('masters/master_commune.csv')
```
