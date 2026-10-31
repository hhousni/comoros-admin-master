# Changelog

## 2026-10-31 — village table corrected

`master_town_village.csv`: 338 → 319 rows. Country, island, prefecture and commune tables unchanged (checked identical to OCHA COD-AB v01).

- **19 phantom rows removed.** Each village name shared by two communes had been copied into both, so these communes listed it twice (the copy carried the other commune's coordinates). Removed IDs, never used by any published dataset: KM112_0002, KM115_0004, KM121_0005, KM131_0005, KM143_0002, KM151_0007, KM152_0006, KM153_0013, KM234_0004, KM241_0006, KM252_0007, KM262_0003, KM264_0003, KM265_0009, KM271_0009, KM283_0002, KM311_0004, KM323_0004, KM332_0003. These IDs will not be reused.
- **Moya**: the 6 villages of commune Moya (KM151) now have `prefecture_id` KM15 (Sima), like the commune itself; they had KM16, which does not exist.
- **6 coordinates cleared**: SIMA KM152_0001 (point of the Grande Comore Sima), BANDRADJOU KM131_0008, BANDAMADJI LA MBOIKOU KM211_0008, KOUA KM265_0008 (points in another commune), TSINI MOICHONGO KM251_0008 and KANDZILE KM251_0009 (same point for both).
- Added: tests (`tests/`), OCHA source in `raw/ocha_cod_ab/`, correction script, this changelog.

Every published village ID that was kept has the same name and commune as before.

## 2026-09 — first version
