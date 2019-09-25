from dlcs.queue_response import Batch
import requests
from requests import auth
import dlcs.settings as settings
import json


def register_collection(image_collection):
    """
    Register an image collectio with the DLCS.

    :param image_collection: expects a clean JSON-LD friendly dict.
    :return:
    """
    authorisation = auth.HTTPBasicAuth(settings.DLCS_API_KEY, settings.DLCS_API_SECRET)
    url = settings.DLCS_ENTRY + 'customers/' + str(settings.DLCS_CUSTOMER_ID) + '/queue'
    json_data = json.dumps(image_collection)
    response = requests.post(url, data=json_data, auth=authorisation)
    batch = Batch(response.json())
    return batch
