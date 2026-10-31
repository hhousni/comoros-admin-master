# CLAUDE.md — Comoros Admin Master

The canonical IDs and names (country / island / prefecture / commune / village) used by every dataset of Comores Open Data. Workspace map and shared rules: `../CLAUDE.md`; dataset rules: `../docs/DATA_CONTRACT.md`. Sources, rules and commands: `README.md`.

- `masters/*.csv` are the source of truth. Country → commune must stay identical to the OCHA COD-AB copy in `raw/ocha_cod_ab/` (tests check it). Never edit `raw/`.
- IDs are never changed, reused or renumbered. A removal is a deliberate edit of `tests/known_ids.txt`, noted in `CHANGELOG.md`.
- Village changes go in `scripts/correct_town_village.py` (one list per kind of change, each entry with its reason), then run it, run the tests and add a `CHANGELOG.md` entry.
- Coordinates: leave empty rather than guess; a new coordinate must fall in its commune (test).
- After a change, the repos that use these tables must be updated (e.g. `Comoros-demographics` submodule `external/comoros-admin-master`) and the reference tables republished on the site.
- Run `PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider` before every commit.
