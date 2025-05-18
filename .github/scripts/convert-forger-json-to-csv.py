#!/usr/bin/env python3

"""
This script generates a coin_ledger.csv in the root of the repo with rows for each of
the 400 coins.

If a coin is found in any daily-scrape JSON file, its details and discovery date are
included; otherwise, the row is left blank except for the id.

Run the script to produce the updated CSV.
"""

import json
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

def get_all_json_files():
    folder = ROOT / 'daily-scrape'
    files = sorted([f for f in folder.iterdir() if f.suffix == '.json'])
    return files

def build_coin_ledger():
    coin_info = {}  # id (int) -> dict with details and discovered_on
    for jsonfile in get_all_json_files():
        date = jsonfile.stem
        with jsonfile.open('r') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f'Error reading {jsonfile}: {e}', file=sys.stderr)
                continue
            for coin in data:
                cid = coin.get('id')
                if not isinstance(cid, int):
                    continue
                if cid not in coin_info:
                    coin_info[cid] = {
                        'id': cid,
                        'name': coin.get('name', ''),
                        'location': coin.get('location', ''),
                        'image': coin.get('image', ''),
                        'discovered_on': date
                    }
    # Prepare rows for ids 1-400
    rows = []
    for cid in range(1, 401):
        if cid in coin_info:
            rows.append(coin_info[cid])
        else:
            rows.append({'id': cid, 'name': '', 'location': '', 'image': '', 'discovered_on': ''})
    return rows

def write_coin_ledger_csv(rows, csv_file):
    fieldnames = ['id', 'name', 'location', 'image', 'discovered_on']
    with open(ROOT / csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f'Wrote CSV to {csv_file}')

if __name__ == '__main__':
    rows = build_coin_ledger()
    write_coin_ledger_csv(rows, 'coin_ledger.csv')
