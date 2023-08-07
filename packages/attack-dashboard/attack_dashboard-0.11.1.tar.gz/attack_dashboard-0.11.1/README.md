# Update Mitre Dashboard

> Goal: Update the Mitre Dashboard from the [HELK](https://github.com/Cyb3rWard0g/HELK) with the latest data.

### Challenge

- [x] The [old data](https://raw.githubusercontent.com/Cyb3rWard0g/HELK/master/docker/helk-logstash/enrichments/cti/mitre_attack.csv) does not match with newer data, both in column names and count.
- [ ] Different sources with varying data formats.
- [ ] Sub-techniques not included in the old data. 

<!-- ## Mitre script

> Mitre provides python scripts to parse the data as csv.

The script is in the [allCsv]{./allCsv} folder together with the pulled csv files.
With a tad of column renaming and 2 table joins the resulting csv looks a lot like the original table.
We miss the `data_source` or `log_source` intel. -->

## Set up

Get started:
```bash
poetry install
```

## Mitreattack-py

Mitre offers a [python lib](https://github.com/mitre-attack/mitreattack-python/tree/master) to parse their data.
The returned data is very rich and in json format. Surely it contains all the columns we need, yet renaming and joining will require patience.

<!-- The concerning can be found in the [mitreattack_python](./mitreattack_python.ipynb) notebook. -->

### Challenge
- [x] The data is split into different tables which reference between each other.
- [x] Table joining results in a `60GB` and `130M` row table.
- [x] (Optionally) Exclude `sub-techniques` from the table.


The following sript exports the data as csv and the headers as txt.
```bash
poetry run python run.py --matrix_name <matrix> --include_subtechniques  --output_dir ./output
```
Options for `matrix_name` are `enterprise-attack`, `mobile-attack` and `ics-attack`.
Optional flags are:
- `--include_sub_techniques` to include sub_techniques.
- `--include_detection` to include detection methods.
- `--include_descriptions` to include descriptions of techniques, software, groups, etc.

> Note: setting all flags will result in a `60GB` csv file and might take a while.
### Send 2 Logstash

Now that we got the more or les lean data as `csv, lets use logstash to import it into elasticsearch.
First set your creds in the `.env` file. Then run:
```bash
export $(grep -v '^#' .env | xargs -d '\n')
export HEADERS=$(grep -v '^#' output/<pick1>.txt)
logstash -f logstash.conf
```

then in a separate shell:
```bash
nc <logstash-host> 32173 -q 11 < output/<the-same1>.csv
```


## OTRF [attackcti](https://attackcti.com/playground/1-Collect_All_Functions.html#get-all-relationships)


> From the dude who wrote the HELK. Yet columns do not match.


Work can be found in the [mitre_tables](./mitre_tables.ipynb) notebook.

He also introduces the `openhunt` library to visualize pivoting. Experiments are in the [openhunt](./openhunt.ipynb) notebook. 

