"""
upload or update model file | log file | metafile
"""
import re

from openxlab.model.clients.openapi_client import OpenapiClient
from openxlab.model.common.constants import endpoint, token


def upload(model_repo, file_type, source, target) -> None:
    """
    upload model file | readme file | logfile | meta file
    """
    try:
        # split params
        username, repository = _split_repo(model_repo)
        client = OpenapiClient(endpoint, token)
        """
        1. 查询哪些待上传
        2. 上传oss
        """
        print(f"file upload successfully.")
    except ValueError as e:
        print(f"Error: {e}")
        return


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


def _parse_check():

    pass
