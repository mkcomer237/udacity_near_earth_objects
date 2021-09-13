import extract as ex
import database as db

# Create the database
neo_db = db.NEODatabase(ex.load_neos('data/neos.csv'), ex.load_approaches('data/cad.json'))
print('creation_success')

# Print out the first few elements from each collection

for neo in neo_db._neos[0:3]:
    print(neo) 



for approach in neo_db._approaches[0:3]:
    print(approach) 


counter = 0
for key, value in neo_db.name_dict.items():
    print(key, value)
    counter += 1 
    if counter >= 3:
        break


# Test the methods for the DB 

print(neo_db.get_neo_by_designation(887))
print(neo_db.get_neo_by_name('Eros'))
print(neo_db.get_neo_by_designation('2020 BS'))
print(neo_db.get_neo_by_designation('2101'))
print(neo_db.get_neo_by_designation('2102'))

