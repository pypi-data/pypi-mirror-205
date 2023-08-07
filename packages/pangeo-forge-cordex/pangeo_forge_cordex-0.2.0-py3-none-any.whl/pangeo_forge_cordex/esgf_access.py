import os
import ssl

import requests
from pangeo_forge_recipes.patterns import pattern_from_file_sequence
from pangeo_forge_recipes.recipes import XarrayZarrRecipe
from pyesgf.logon import LogonManager

from .utils import combine_response, parse_dataset_response, sort_files_by_dataset_id


def logon():
    lm = LogonManager(verify=True)
    if not lm.is_logged_on():
        myproxy_host = "esgf-data.dkrz.de"
        # if we find those in environment, use them.
        if "ESGF_USER" in os.environ and "ESGF_PASSWORD" in os.environ:
            lm.logon(
                hostname=myproxy_host,
                username=os.environ["ESGF_USER"],
                password=os.environ["ESGF_PASSWORD"],
                interactive=False,
                bootstrap=True,
            )
        else:
            lm.logon(
                hostname=myproxy_host,
                interactive=True,
                bootstrap=True,
            )

    print(f"logged on: {lm.is_logged_on()}")

    # create SSL context
    sslcontext = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
    sslcontext.load_verify_locations(capath=lm.esgf_certs_dir)
    sslcontext.load_cert_chain(lm.esgf_credentials)
    return sslcontext


def create_recipe(urls, recipe_kwargs=None, pattern_kwargs=None):
    if recipe_kwargs is None:
        recipe_kwargs = {}
    if pattern_kwargs is None:
        pattern_kwargs = {}
    pattern = pattern_from_file_sequence(urls, "time", **pattern_kwargs)
    if urls is not None:
        return XarrayZarrRecipe(
            pattern, xarray_concat_kwargs={"join": "exact"}, **recipe_kwargs
        )


def request(
    url="https://esgf-node.llnl.gov/esg-search/search",
    project="CORDEX",
    type="File",
    **search,
):
    version = search.get("version", None)
    if type == "File" and version:
        # this does not work for File searches since version denotes here rcm_version
        del search["version"]
    elif version and version.startswith("v"):
        search["version"] = version[1:]
    params = dict(project=project, type=type, format="application/solr+json", limit=500)
    params.update(search)
    return requests.get(url, params)


def esgf_search(
    url="https://esgf-node.llnl.gov/esg-search/search",
    files_type="OPENDAP",
    project="CORDEX",
    **search,
):
    response = request(url, project, "Dataset", **search)
    # return response.json()["response"]
    dset_info = parse_dataset_response(response)
    response = request(url, project, "File", **search)
    # return response.json()["response"]
    files_by_id = sort_files_by_dataset_id(response)
    responses = combine_response(dset_info, files_by_id)
    return responses
