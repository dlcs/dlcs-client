from requests import get, auth
import dlcs.settings_local as settings
from tqdm import tqdm
import time


mapping = {
    '@context': 'context',
    '@id': 'id',
    '@type': 'type',
    'errorImages': 'error_images',
    'completedImages': 'completed_images',
}


def batch_progress(dlcs_batch, sleep_interval=10):
    """
    Provide a TQDM progress bar for a batch ingest.

    To Do: Add logging.

    :param dlcs_batch: Batch object
    :param sleep_interval: time to sleep between updates
    :return: Batch
    """
    t = tqdm(total=dlcs_batch.count)
    while dlcs_batch.finished == "0001-01-01T00:00:00" or not dlcs_batch.is_completed():
        dlcs_batch.update()
        processed = dlcs_batch.completed + dlcs_batch.errors
        t.update(dlcs_batch.completed + dlcs_batch.errors)
        time.sleep(sleep_interval)
    t.close()
    print(f"Processed {processed} of {dlcs_batch.count}, with {dlcs_batch.errors} errors.")
    return dlcs_batch


class Batch:

    @staticmethod
    def get_attribute_name(json_name):
        if json_name in mapping:
            return mapping.get(json_name)
        return json_name

    def __init__(self, batch_data=None, batch_id=None):

        self.count = 0
        self.completed = 0
        self.id = batch_id
        if batch_data is not None:
            self.update_data(batch_data)
        else:
            self.update()

    def update(self):
        url = self.id
        a = auth.HTTPBasicAuth(settings.DLCS_API_KEY, settings.DLCS_API_SECRET)
        response = get(url, auth=a)
        self.update_data(response.json())

    def update_data(self, batch_data):

        for element in batch_data:
            value = batch_data.get(element)
            setattr(self, self.get_attribute_name(element), value)

    def is_completed(self):
        # TODO check for errors count. e.g. errors + completed == count and return number of errors
        return self.count > 0 and self.count == int(self.completed)
