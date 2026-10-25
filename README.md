# SYNDEPLOY-240

Synthetic Multi-Site Industrial IoT Deployment Planning Dataset for Rollout Sequencing Research

## Synthetic by construction

This dataset is synthetic by construction. It was generated programmatically and does not contain real site, operator, or deployment records.

## Files

- `syndeploy240_sites.csv` — the dataset in CSV format
- `syndeploy240_sites.json` — the dataset in JSON format
- `generate_dataset.py` — the script used to generate the dataset
- `DATA-DICTIONARY-AND-VALIDATION.md` — data dictionary and validation notes

## Regeneration

Regenerate the dataset with:

```bash
python3 generate_dataset.py
```

## Expected checksum

Expected SHA-256 for `syndeploy240_sites.csv`:

```
a55592a8cefa01f467041ec8fa2e0f5838b46a51b84338cf301961ecf7c1a872
```

## Citation

Please cite this dataset using its Zenodo DOI:

https://doi.org/10.5281/zenodo.23648012

## License

- Data: CC BY 4.0
- Script (`generate_dataset.py`): MIT
