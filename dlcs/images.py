import json
import requests
from dlcs.settings import key_mapping


def image_dict(
    identifier=None,
    at_id=None,
    space=None,
    origin=None,
    tags=None,
    string_1=None,
    string_2=None,
    number_1=None,
    number_2=None,
):
    """ This is redudant, just here while I check stuff."""
    # Do stuff here if there's any validation that needs to happen, or transformation.
    # Otherwise, just return whatever parameters get passed in.
    return locals()


def dict_to_jsonld_friendly(source, mapping, lower_case=True):
    """
    Delete empty keys and replace keys with their appropriate equivalent, e.g.
    'context' with '@context'.

    :param source: input dict
    :param mapping: mapping for keys
    :param: lower_case: Boolean, change the key to lower case form of key
    :return: dict
    """
    if type(source) == list:
        return [dict_to_jsonld_friendly(x, mapping=mapping) for x in source]
    elif type(source) == dict:
        new_dict = {}
        for k, v in source.items():
            if lower_case:
                new_key = k.lower()
            else:
                new_key = k
            if v is not None and v is not "":
                if k in mapping.keys():
                    new_dict[mapping[new_key]] = dict_to_jsonld_friendly(v, mapping=mapping)
                else:
                    new_dict[new_key] = dict_to_jsonld_friendly(v, mapping=mapping)
    else:
        return source
    return new_dict


def make_collection(
    members,
    context="http://www.w3.org/ns/hydra/context.jsonld",
    to_jsonld_friendly=True,
):
    """

    :param members:
    :param context:
    :param to_jsonld_friendly: Boolean, if true transform to json-ld friendly form.
    :return:
    """
    collection_dict = dict(type="Collection", context=context, members=members)
    if members:
        if len(members) > 0:
            collection_dict["total_items"] = len(members)
    if to_jsonld_friendly:
        return dict_to_jsonld_friendly(source=collection_dict, mapping=key_mapping)
    else:
        return collection_dict


r = requests.get(
    "https://presley.dlcs-ida.org/iiif/idatest01/_roll_M-1011_174_cvs-948-1001/manifest"
)
if r.status_code == requests.codes.ok:
    j = r.json()
    print(json.dumps(dict_to_jsonld_friendly(j, mapping=key_mapping), indent=2))
