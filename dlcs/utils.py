import itertools


def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.

    From: https://stackoverflow.com/a/26853961
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def dict_to_jsonld_friendly(source, mappings=None, excludes=None, lower_case=True):
    """
    Helper function.

    Delete empty keys and replace keys with their appropriate equivalent, e.g.
    'context' with '@context'.

    Exclude keys that you don't want to appear in the output.
    
    Works recursively on shallow copies of the original source.

    :param source: input
    :param mappings: list of mappings for keys. Mappings are dicts with {"old_key: "new_key"} pairs.
    :param excludes: list of lists for excludes for keys, e.g. ["exclude_me", "exclude_me_too"]
    :param lower_case: Boolean, change the key to lower case form of key
    :return: transformed input.
    """
    if excludes:  # merge the list fo excludes into a single list
        exclude = list(itertools.chain.from_iterable(excludes))
    else:
        exclude = None
    if mappings:  # merge the list of dicts into a single dict
        mapping = merge_dicts(*mappings)  # this assumes that the same key isn't repeated
    else:
        mapping = None
    if type(source) == list:
        return [dict_to_jsonld_friendly(x, mappings=mappings, excludes=excludes) for x in source]
    elif type(source) == dict:
        new_dict = {}  # empty dict to add the transformed keys and values to
        for k, v in source.items():
            if lower_case:  # transform to lower case, this defaults to True.
                new_key = k.lower()
            else:
                new_key = k
            mapped_key = new_key
            if mapping:
                if new_key in mapping.keys():
                    mapped_key = mapping[new_key]
            if v is not None and v is not "":  # exclude empty keys and empty strings
                if exclude:
                    if new_key not in exclude:  # if the key isn't explicitly excluded
                        new_dict[mapped_key] = dict_to_jsonld_friendly(
                            v, mappings=mappings, excludes=excludes
                        )
                else:
                    new_dict[mapped_key] = dict_to_jsonld_friendly(
                        v, mappings=mappings, excludes=excludes
                    )
    else:
        return source
    return new_dict



