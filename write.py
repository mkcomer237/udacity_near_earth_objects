"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output
    row corresponds to the information in a single close approach from the
    `results` stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
    saved.
    """
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s',
                  'designation', 'name', 'diameter_km',
                  'potentially_hazardous')
    with open(filename, 'w') as outfile:
        approach_writer = csv.writer(outfile)
        # Write the header
        approach_writer.writerow(fieldnames)

        # Write each approach as a row
        for approach in results:
            outlist = (approach.time.strftime("%Y-%m-%d %H:%M"),
                       approach.distance,
                       approach.velocity,
                       approach.neo.designation,
                       approach.neo.name,
                       approach.neo.diameter,
                       approach.neo.hazardous)
            approach_writer.writerow(outlist)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is
    a list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be
    saved.
    """
    # Format as a json like dictionary/list collection first
    json_out = []
    # Add each returned approach to the list as a nested dictionary object
    for approach in results:
        approach_dict = {"datetime_utc": approach.time.strftime(("%Y-%m-%d"
                                                                " %H:%M")),
                         "distance_au": approach.distance,
                         "velocity_km_s": approach.velocity,
                         "neo": {
                             "designation": approach.neo.designation,
                             "name": approach.neo.name,
                             "diameter_km": approach.neo.diameter,
                             "potentially_hazardous": approach.neo.hazardous}
                         }

        json_out.append(approach_dict)

    # Write list of dictionaries to the file as a json object
    with open(filename, mode='w') as outfile:
        json.dump(json_out, outfile)
