# XRPL Validation Tracker
Three modules are provided:
1. The `aggregator` combines multiple websocket subscription streams into a single outgoing websocket stream.
2. `db_writer` stores XRP Ledger data in relational databases. Since this code is in testing, only sqlite3 is supported now. Better database support is needed for production.
3. `ws_client` is used to connect to remote websocket servers and is used by both the `aggregator` and `db_writer` modules.

The `aggregator` is designed for more flexible use with a wide range of streams. The `db_writer` is currently specific to the validation stream, though support for additional streams would be beneficial (e.g., the ledger stream).

The `aggregator` code is structured to provide multiple layers of redundancy. For example, four servers could use the `aggregator` code to subscribe to 5-10 XRP Ledger nodes. Two additional servers could then use the `db_writer`, which already depends on the `aggregator` to subscribe to the previously mentioned four servers. This schema provides redundancy at both the data aggregation and database ingestion stages.

## Installing & Running the Software
After installing dependencies, adjust the settings in `settings_aggregator.py` and/or `settings_db_writer.py`, then run `run_tracker.py` using either an '-a' or '-d' flag to specify which module to run. Both modules can be run on the same system, though they must be started separately.

All modules depend on the python `websockets` module. `db_writer` also requires sqlite3.

The `supplemental_data` depends on the `xrpl_unl_parser` and `pytomlpp`

This has been tested on Python 3.7 and 3.8.

## To Do Items
1. Transition to Postgres or another production database
2. Improve database structure & index the database
3. Improve the websocket server `ws_server` in the `aggregator` - accept headers, subscribe messages, etc.
4. API access - mimic Data API v2 + live validation stream subscription (notify missing) - consider developing a `db_reader` package to retrieve requests.
5. Multiple "To-do" items are noted in comments throughout the code.
6. Change logging to % format
7. Daemonize
8. Fix errors with multiprocessing when exiting using keyboard interrupt
9. Support multiple UNLs
10. Verify UNLs authenticity against a provided signature
11. Check attestations in TOMLs
12. Write ledgerClosed stream data to DB

## Thoughts
1. Identify main chain through an aggregated ledger subscription stream - use this to verify hash, index, and time
2. Trie or rrdtool?
