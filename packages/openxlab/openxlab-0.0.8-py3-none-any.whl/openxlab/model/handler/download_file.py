"""
Download function for related files in the reality model library
"""
import logging
import re
from tqdm import tqdm
import requests
import os

from openxlab.model.clients.openapi_client import OpenapiClient
from openxlab.model.common.constants import endpoint, token, default_metafile_template_name

logger = logging.getLogger("openxlab.model")


def download(model_repo, file, path=None) -> None:
    """
    download model file|meta file|log filee|readme file
    usage: cli & sdk
    """
    try:
        # split params
        username, repository = _split_repo(model_repo)
        client = OpenapiClient(endpoint, token)
        url, file_name = client.get_download_url(repository, file)
    except ValueError as e:
        print(f"Error: {e}")
        return
    path_file = _download_to_local(url, file_name, path)
    print("download model repo:{}, file_name:{}".format(model_repo, file_name))
    return path_file


def download_metafile_template(path=None) -> None:
    """
    download metafile template file
    """
    try:
        # split params
        client = OpenapiClient(endpoint, token)
        url = client.get_metafile_template_download_url()
    except ValueError as e:
        print(f"Error: {e}")
        return
    _download_to_local(url, file_name=default_metafile_template_name, path=path)


def _split_repo(model_repo) -> (str, str):
    """
    Split a full repository name into two separate strings: the username and the repository name.
    """
    # username/repository format check
    pattern = r'^[a-zA-Z0-9]+\/[a-zA-Z0-9\-_]+$'
    if not re.match(pattern, model_repo):
        raise ValueError("The input string must be in the format 'didi12/test-d-1'")

    values = model_repo.split('/')
    return values[0], values[1]


def _download_to_local(url, file_name, path=None) -> str:
    """
    download file to local with progress_bar
    """
    response = requests.get(url, stream=True)

    total_size_in_bytes = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    path_file = file_name
    if path is not None:
        if not os.path.exists(path):
            os.makedirs(path)
        path_file = f"{path}/{file_name}"
    with open(path_file, 'wb') as f:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            f.write(data)
    progress_bar.close()
    return path_file
