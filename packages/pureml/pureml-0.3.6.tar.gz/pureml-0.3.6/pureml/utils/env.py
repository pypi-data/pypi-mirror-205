from dotenv import load_dotenv
import os
from pureml.schema import Env
from rich import print


def generate_env_dict(env_path):
    load_dotenv(dotenv_path=env_path)

    org_id = os.getenv(Env.ORG_ID.value)
    access_token = os.getenv(Env.ACCESS_TOKEN.value)
    api_id = os.getenv(Env.API_ID.value)
    api_key = os.getenv(Env.API_KEY.value)

    env_dict = {}

    if org_id is None:
        print("[red]", Env.ORG_ID.value, "is not set in .env")
    else:
        env_dict[Env.ORG_ID.value] = org_id

    if access_token is None:
        print("[red]", Env.ACCESS_TOKEN.value, "is not set in .env")
    else:
        env_dict[Env.ACCESS_TOKEN.value] = access_token

    if api_id is None:
        print("[red]", Env.API_ID.value, "is not set in .env")
    else:
        env_dict[Env.API_ID.value] = api_id

    if api_key is None:
        print("[red]", Env.API_KEY.value, "is not set in .env")
    else:
        env_dict[Env.API_KEY.value] = api_key

    return env_dict


def validate_env_docker(env_dict):
    env_dict_set = set(list(env_dict.keys()))
    env_dict_docker = set([Env.ORG_ID.value, Env.API_ID.value, Env.API_KEY.value])

    if env_dict_docker.issubset(env_dict_set):
        return True

    return False
