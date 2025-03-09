# Based Rollup Evaluation

Submitted to [CAAW 2025](https://caaw.io/2025/); data is from Taiko and Scroll rollups. 
Taiko is a based rollup, Scroll is not -- but it serves as a good reference for a lot things.

The main data collection is done as follows
`python3 main-v2.py` (or change for Scroll data)
`python3 process-tx.py`

and then other checks (`checkdata` or `duplicates`) and generate charts.
To avoid collecting data yourself, it's included in `data-*` directories within `data.zip`. This prevents the need to get a premium RPC endpoint.