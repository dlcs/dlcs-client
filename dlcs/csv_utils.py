import os
import csv
from dlcs.images import Image, Collection
from dlcs.settings import csv_excludes, master_mappings


def csv_to_json(csv_file, mappings=master_mappings, excludes=(csv_excludes,)):
    """
    Helper function to transform a CSV that has been formatted in the way expected by the
    Portal UI into Collection JSON that can be used via the DLCS APIs.

    :param csv_file:
    :param mappings: list of mappings for keys. Mappings are dicts with {"old_key: "new_key"} pairs.
    :param excludes: list of lists for excludes for keys, e.g. ["exclude_me", "exclude_me_too"]
    :return:
    """
    if os.path.exists(csv_file):
        if os.path.isfile(csv_file):
            if os.access(csv_file, os.R_OK):  # we have a readable file
                with open(csv_file) as f:
                    csv_doc = csv.DictReader(f)
                    # convert to tuples, and run through the dict transformation
                    csv_rows = [
                        Image(mappings=mappings, excludes=excludes, **dict(d)).jsonld_friendly()
                        for d in csv_doc
                    ]
                    if csv_rows:
                        collection = Collection(member=csv_rows, excludes=None, mappings=mappings)
                        if collection:
                            # this bit is sort of redundant, but we might want to also transform this before returning
                            return collection
    return
