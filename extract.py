"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neos_dict = {}

    with open(neo_csv_path, mode='r') as incsv:
        neos = csv.reader(incsv)
        # Skip the header 
        next(neos)
        # Add each neo to the output dictionary as a NearEarthObject object with 
        # the designation as the key (for easy lookup later)
        for line in neos:
            neos_dict[line[3]] = NearEarthObject(designation=line[3], 
                                                name=line[4],
                                                diameter=line[15], 
                                                hazardous=line[7])

    return neos_dict


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    cad_list = [] 
    with open(cad_json_path, mode='r') as infile:
        cad = json.load(infile) 
    # Add each close approach to a list as a CloseApproach object 
    for approach in cad['data']:
        cad_list.append(CloseApproach(designation=approach[0],
                                    distance=approach[4],
                                    velocity=approach[8],
                                    time=approach[3]))
    return cad_list
