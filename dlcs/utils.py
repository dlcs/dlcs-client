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
    Delete empty keys and replace keys with their appropriate equivalent, e.g.
    'context' with '@context'.
    
    Works recursively.

    :param source: input dict
    :param mappings: list of mappings for keys
    :param excludes: list of lists for excludes for keys
    :param lower_case: Boolean, change the key to lower case form of key
    :return: dict
    """
    if excludes:  # merge the list fo excludes into a single list
        exclude = list(itertools.chain.from_iterable(excludes))
    else:
        exclude = None
    if mappings:  # merge the list of dicts into a single dict
        mapping = merge_dicts(*mappings)
    else:
        mapping = None
    if type(source) == list:
        return [dict_to_jsonld_friendly(x, mappings=mappings, excludes=excludes) for x in source]
    elif type(source) == dict:
        new_dict = {}
        for k, v in source.items():
            if lower_case:
                new_key = k.lower()
            else:
                new_key = k
            mapped_key = new_key
            if mapping:
                if new_key in mapping.keys():
                    mapped_key = mapping[new_key]
            if v is not None:  # exclude empty keys
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
