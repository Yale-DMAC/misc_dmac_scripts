#!/usr/bin/python3


import os
from pathlib import Path
import subprocess

import requests
import yaml

def yml_to_list(yaml_file):
    return [[item.get('name'), item.get('url'), item.get('branch')] for item in list(yaml_file.values())[0]]

def get_github_file(fp, sesh):
    plugin_data = sesh.get(fp).text
    if fp.endswith('yml'):
        return yaml.safe_load(plugin_data)
    return plugin_data

def get_plugin_report(instance, sesh):
    fp = f"https://api.github.com/repos/YaleArchivesSpace/aspace-deployment/contents/{instance}/plugins.yml"
    plugin_list = get_github_file(fp, sesh)
    return yml_to_list(plugin_list)

def clone_repo(repo_data, output_location):
    output_location = Path(output_location, repo_data[0])
    repo_uri = repo_data[1]
    branch = repo_data[2]
    subprocess.run(['git', 'clone', '-b', branch, repo_uri, output_location])

def main():
    output_location = input('Please enter path to output directory (e.g. /Users/alicia/archivesspace/plugins): ')
    with requests.Session() as sesh:
        headers = {'Accept': 'application/vnd.github.v4.raw'}
        sesh.headers.update(headers)
        plugin_data = get_plugin_report('test', sesh)
        for plugin_row in plugin_data:
            clone_repo(plugin_row, output_location)

if __name__ == '__main__':
    main()