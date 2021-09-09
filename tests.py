import extract as ex
import database as db

# Create the database
neo_db = db.NEODatabase(ex.load_neos('data/neos.csv'), ex.load_approaches('data/cad.json'))
print('creation_success')

# Print out the first few elements from each collection
counter = 0
for key, value in neo_db._neos.items():
    print(key, value)
    counter += 1 
    if counter >= 3:
        break

for approach in neo_db._approaches[0:3]:
    print(approach) 
