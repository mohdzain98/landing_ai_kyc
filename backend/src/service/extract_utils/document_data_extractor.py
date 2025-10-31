import os

from src.service.extract_utils.identity_document_extractor import identity_extract
from src.service.extract_utils.bank_data_extractor import bank_extractor


def extract(folder_id):

    folder_path = os.getcwd() + f"/resources/{folder_id}"

    identity_extract(folder_path)
    bank_extractor(folder_path)




