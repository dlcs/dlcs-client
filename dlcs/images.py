import json
from dlcs.utils import dict_to_jsonld_friendly
from dlcs.settings import master_excludes, master_mappings


class JsonObject(object):
    """
    Generic JSON object class, with methods for returning a transformed jsonld friendly dict, or
    json as a string.

    Will set the mappings to settings.master_mappings and the excludes to settings.master_excludes if not otherwise set.
    """
    def __init__(self, *args, **kwargs):
        vars(self).update(kwargs)
        if not hasattr(self, "mappings"): # this can be set to None
            self.mappings = master_mappings
        if not hasattr(self, "excludes"):  # this can be set to None
            self.excludes = master_excludes
        self.clean_dict = {k:v for k,v in self.__dict__.items() if k not in ["excludes", "mappings"]}


    def jsonld_friendly(self):
        """
        Method will delete empty keys and replace keys with their appropriate equivalent, e.g.
        'context' with '@context' using the self.mappings parameter.

        Exclude keys that you don't want to appear in the output using the self.excludes parameter.
        """
        return dict_to_jsonld_friendly(source=self.clean_dict, mappings=self.mappings, excludes=self.excludes)

    def to_json(self):
        """
        Dump the json_ld_friendly output to a string using json.dumps
        """
        return json.dumps(self.jsonld_friendly(), indent=2, sort_keys=True)


class Image(JsonObject):
    """
    Image object
    """
    def __init__(self, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        # Do some stuff here if there's any image specific stuff. e.g. validation or normalisation of values.


class Collection(JsonObject):
    """
    Collection object.

    Will set the context and the type.
    """
    def __init__(self, *args, **kwargs):
        super(Collection, self).__init__(*args, **kwargs)
        # Do some stuff here if there's any collection specific stuff, e.g. validation or normalisation of values.
        self.clean_dict["type"] = "Collection"
        self.clean_dict["context"] = "http://www.w3.org/ns/hydra/context.jsonld"
        if hasattr(self, "member"):
            if self.member is None:
                self.clean_dict["total_items"] = 0
            else:
                self.clean_dict["total_items"] = len(self.member)
        else:
            self.clean_dict["total_items"] = 0










