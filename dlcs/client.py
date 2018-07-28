from dlcs.queue_response import Batch
from requests import get, post, auth
import settings


def register_collection(image_collection):

    url = get_customer_url() + 'queue'
    json = image_collection.as_json()
    response = post(url, data=json, auth=get_authorisation())
    batch = Batch(response.json())

    return batch

def get_image(image_slug, space=None):

    if space == None:
        space = settings.DLCS_SPACE
    
    url = get_customer_url + "spaces/" + str(space) + "/images/" + image_slug
    response = get(url, auth=get_authorisation())
    # just do this? Or use the Image class somehow?
    return response.json()
    
def get_authorisation():

    return auth.HTTPBasicAuth(settings.DLCS_API_KEY, settings.DLCS_API_SECRET)

def get_customer_url():

    cust_id = str(settings.DLCS_CUSTOMER_ID)
    return settings.DLCS_ENTRY + 'customers/' + cust_id + "/"
