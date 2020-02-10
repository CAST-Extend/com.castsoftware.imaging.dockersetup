#!/bin/sh
# Run to delete user roles from database.

curl -X POST -H "Content-type: application/json" http://neo4j:imaging@localhost:7474/db/data/transaction/commit -d "{\"statements\": [{\"statement\": \"MATCH (n:Role) DETACH DELETE n\"}]}"
echo
echo "All users have been successfully deleted."
