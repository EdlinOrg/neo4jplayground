# Some code for trying out neo4j with python

`api.py`: a simple flask api

`n4j.py`: the cypher queries (that the api uses)

`createdb.py`: the file that generated `fullset.csv`, see that python file for the rules how the users are connected

A user has one property, _"ourid"_, not to be confused with the internal id of the node.

## Neo4j url

The url with username/password for Neo4j is hard coded in `n4j.py`

## Starting the api
### Dev environment

```bash
export FLASK_APP=`pwd`/api.py
export FLASK_DEBUG=1
flask run
```

### Using gunicorn
```bash
gunicorn -w 2 api:app
```

## Loadtest
```bash
npm install loadtest
node node_modules/loadtest/bin/loadtest.js -c 10 --rps 1000 "http://127.0.0.1:8000/2nd3rd/?ourid=3"
```

## Importing test data (about 2 million rows)

Remove the `WITH row LIMIT 30` to import the full 2 million entries
also adjust the path to wherever this directory is.

Comment out `dbms.directories.import` in `.neo4j.conf`
so neo4j will allow importing from files outside its own dir.

If it can't handle the full import at once, or you don't want to import all test data,
use the chunks `initdata/xa*` instead (100k in each)

(notice that you have to bunzip2 the `initdata/*` files first)

### Cypher code for import

```
CREATE CONSTRAINT ON (u:User) ASSERT u.ourid IS UNIQUE;

USING PERIODIC COMMIT
LOAD CSV WITH HEADERS FROM "file:///some/path/neo4jplayground/initdata/fullset.csv" AS row
WITH row LIMIT 30

MERGE(u:User {ourid:row.user})

FOREACH (f IN split(row.friends, ",") |
  MERGE(u2:User {ourid:f})
  MERGE(u)-[:FRIEND]->(u2))

```
