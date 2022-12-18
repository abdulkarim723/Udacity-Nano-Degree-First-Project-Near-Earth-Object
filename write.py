"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    with open(filename, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames)
        writer.writeheader()
        rows = []
        for elem in results:
            if elem.neo.name is None:
                elem.neo.name = ''
            row = {fieldnames[0]: elem.time_str, fieldnames[1]: elem.distance, fieldnames[2]: elem.velocity,
                   fieldnames[3]: elem.designation,
                   fieldnames[4]: elem.neo.name, fieldnames[5]: elem.neo.diameter, fieldnames[6]: elem.neo.hazardous}
            writer.writerow(row)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    with open(filename, 'w', newline='\n') as outfile:
        data = []
        for result in results:
            approach_dict = {}
            approach_neo = {}
            approach_dict['datetime_utc'] = result.time_str
            approach_dict['distance_au'] = result.distance
            approach_dict['velocity_km_s'] = result.velocity

            approach_neo['designation'] = result.neo.designation
            approach_neo['name'] = result.neo.name
            if approach_neo['name'] is None:
                approach_neo['name'] = ''
            approach_neo['diameter_km'] = result.neo.diameter
            approach_neo['potentially_hazardous'] = result.neo.hazardous

            approach_dict['neo'] = approach_neo
            data.append(approach_dict)
        json.dump(data, outfile, default=str, indent=2)
