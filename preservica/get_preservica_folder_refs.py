#/usr/bin/python3

import csv
import json
import pprint
import warnings
import xml.etree.ElementTree as ET
import requests


# suppress warnings during testing
warnings.filterwarnings("ignore")

class PreservicaDownloader():
    def __init__(self, username, pw, api_url):
        self.username = username
        self.pw = pw
        self.api_url = api_url
        self.session = requests.Session()
        self.token = self.__token__()
        self.session.headers.update(self.token)

    def __token__(self):
        response = self.session.post(f'https://{self.api_url}accesstoken/login', data=f'username={self.username}&password={self.pw}', headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}, verify=False)
        if response.status_code == 200:
            print('Connected.')
            return {'Preservica-Access-Token': response.json()['token']}
        else:
            print(f"Get new token failed with error code: {response.status_code}")
            print(response.request.url)
            raise SystemExit

    def send_request(self, ref, object_type):
        # Changed this from hardcoded structural-object endpoint to user-defined, since
        # the structure 2 object DU IDs correspond to info objects, while structure 1
        # DU IDs correspond to structural objects
        req = self.session.get(f'https://{self.api_url}entity/{object_type}/{ref}', verify=False)
        if req.status_code == 200:
            return ET.fromstring(req.text)
        elif req.status_code == 401:
            self.token = self.__token__()
            self.session.headers.update(self.token)
            return self.send_request(ref)
        else:
            return req.status_code
            
    def get_structural_object(self, ref):
        req = self.send_request(ref, 'structural-objects')
        if isinstance(req, ET.Element):
            obj_data = req.iter("{http://preservica.com/XIP/v6.5}StructuralObject")
            for element in obj_data:
                deliverable_unit_title = element.find('{http://preservica.com/XIP/v6.5}Title').text
                deliverable_unit_security_tag = element.find('{http://preservica.com/XIP/v6.5}SecurityTag').text
                return {'du_title': deliverable_unit_title, 'du_security_tag': deliverable_unit_security_tag}
        elif isinstance(req, int):
            # If the repsonse is a 404 that will be returned as an int
            return {'du_title': f'ERROR: {req}', 'du_security_tag': f'ERROR: {req}'}

    def get_target_folder(self, ref, folder_titles, match=0):
        req = self.send_request(f"{ref}/children", 'structural-objects')
        if isinstance(req, ET.Element):
            child_data = req.iter("{http://preservica.com/EntityAPI/v6.5}Child")
            for element in child_data:
                child_title = element.attrib.get('title')
                if child_title in folder_titles:
                    match = 1
                    return {'target_folder_ref': element.attrib.get('ref'), 'target_folder_title': child_title}
            if match == 0:
                return {'target_folder_ref': 'NOT FOUND', 'target_folder_title': 'NOT FOUND'}
        elif isinstance(req, int):
            return {'target_folder_ref': f'ERROR: {req}'}

    def get_object_data(self, ref, target_folder):
        print(f'Getting the deliverable unit: {ref}')
        # Retrieves basic info on the parent object - title, security tag.
        deliverable_unit_data = self.get_structural_object(ref)
        # Retrieves the identifier for the target folder below the deliverable unit - i.e. the 'processed' folder
        structural_object_ref = self.get_target_folder(ref, target_folder)
        return deliverable_unit_data, structural_object_ref

def main():
    with open('config.json', encoding='utf8') as config_file:
        settings = json.load(config_file)
        username = settings.get('preservica_username')
        password = settings.get('preservica_password')
        api_url = settings.get('preservica_api_url')
        input_file_path = settings.get('input_csv')
        output_file_path = settings.get('output_csv')
        target_folders = settings.get('target_folder_titles')
        fieldnames = settings.get('fieldnames')
        client = PreservicaDownloader(username, password, api_url)
        with open(input_file_path, encoding='utf8') as input_file, open(output_file_path, 'a', encoding='utf8', newline='') as output_file:
            reader = csv.DictReader(input_file)
            writer = csv.DictWriter(output_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in reader:
                ref = row.get('digital_object_id')
                # this passes in the user-supplied target folder title and the DU identifier
                deliverable_unit_data, target_folder_data = client.get_object_data(ref, target_folders)
                row.update(deliverable_unit_data)
                row.update(target_folder_data)
                writer.writerow(row)

if __name__ == "__main__":
    main()