key_mapping = {"context": "@context", "at_id": "@id", "identifier": "id"}
csv_mapping = {
    "reference1": "string_1",
    "reference2": "string_2",
    "numberreference1": "number_1",
    "numberreference2": "number_2",
}
csv_excludes = ["line", "maxunauthorised", "type"]
master_excludes = [csv_excludes]
master_mappings = [key_mapping, csv_mapping]

DLCS_ENTRY = None  # DLCS API entry point e.g. "https://api.dlcs.io/"
DLCS_API_KEY = None  # API key for DLCS system supplied by a DLCS adminstrator
DLCS_API_SECRET = None  # Secret associated with API KEY supplied by a DLCS adminstrator
DLCS_CUSTOMER_ID = None  # Customer ID for key (integer)
DLCS_SPACE = None  # Default space within customer for operations (integer)
