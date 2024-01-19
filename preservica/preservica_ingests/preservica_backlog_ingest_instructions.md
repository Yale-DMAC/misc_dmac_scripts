# Preservica Backlog Ingest Preparation Instructions

This document describes how to generate an ingest spreadsheet for non-AV Preservica backlog materials

1. Download a copy of this spreadsheet: https://docs.google.com/spreadsheets/d/1x5yD1f6K1a2AGeRvhkwfhB3P-9CJIwEHrUVhQBTG_ss
2. If desired, delete any tabs that you don't need
3. Sort the spreadsheet by column Q - ASpace ID
4. Move anything with an Aspace ID to a new tab
5. Anything which is already in Preservica will have a value in column R. Sort by column R and remove these (to a new tab if desired, but not necessary). NOTE: this only applies to materials which were ingested prior to Kevin's departure. Anything which has already been ingested as part of the backlog project will not be noted here.
6. Copy the tab with the ASpace IDs to a new spreadsheet and save as a CSV
7. Fill out the `config.json` file
8. Run the `generate_ingest_spreadsheet.py` script
9. Review output
