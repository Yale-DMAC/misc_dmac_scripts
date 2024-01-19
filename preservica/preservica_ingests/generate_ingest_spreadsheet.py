#!/usr/bin/python3

import csv
import json
import os
import sys

# only for testing
#from rich import print

def check_config(file_name='config.json') -> dict:
    '''Checks whether a configration file exists, and if so opens and returns
       the file. Can handle either .json or .yml files.

       Parameters:
        file_name: The configuration file name. Default value 'config.json'

       Returns:
        The loaded configuration data

       Raises:
        FileNotFoundError - if the condiguration file is not found at the specified path
    '''
    # not sure about this - works if I run from file, doesn't work if I run from repl
    path_to_this_file = os.path.dirname(os.path.realpath(sys.argv[0]))
    config_path = os.path.join(path_to_this_file, file_name)
    if os.path.exists(config_path):
        with open(config_path, encoding='utf8') as config_file:
            if file_name.endswith('yml'):
                return yaml.safe_load(config_file)
            elif file_name.endswith('json'):
                return json.load(config_file)
    else:
        raise FileNotFoundError(f"File {config_path} not found")

def get_file_list(file_location):
	# returns the list of folders in the file location
	return [dirpath for dirpath in os.listdir(file_location)]
	#return [os.path.join(file_location, dirpath) for dirpath in os.listdir(file_location)]

def get_files_not_ingested(digitized_folder_list, previous_file_list):
	'''returns all folders in the TempLimbOutputs directory which have not already been
		ingested, using the list of folders in the directory and the list of files
		already sent to DPS as input
	'''
	digitized_folder_list_set = set(digitized_folder_list)
	with open(previous_file_list, encoding='utf8') as infile:
		reader = csv.reader(infile)
		header = next(reader)
		previous_file_list_set = set([row[4] for row in reader])
		in_new_list_not_previous_list = digitized_folder_list_set - previous_file_list_set
		return in_new_list_not_previous_list

def separate_uris(digitization_tracking_sheet):
	'''returns lists of records from the digitization tracking spreadsheet which have
		a single URI and muliple uris, respectively.
	'''
	with open(digitization_tracking_sheet, encoding='utf8') as infile:
		reader = csv.reader(infile)
		header = next(reader)
		data = list(reader)
		single_uris = [row for row in data if ',' not in row[15]]
		multiple_uris = [row for row in data if ',' in row[15]]
		return single_uris, multiple_uris, header

def match_files(single_uris, files_not_ingested, output_file_path, header):
	'''returns a list of files, with full directory paths and a single ArchivesSpace URI,
		which are ready to be ingested into Preservica.
	'''
	data = [row for row in single_uris if row[4] in files_not_ingested]
	print(len(data))
	with open(output_file_path, 'w', encoding='utf8') as ofile:
		writer = csv.writer(ofile)
		writer.writerow(header)
		writer.writerows(data)


def main():
	config = check_config()
	file_location = config.get('file_location')
	previous_file_list = config.get('previous_file_list')
	digitization_tracking_sheet = config.get('digitization_tracking_sheet_path')
	output_path = config.get('output_file_path')
	single_uris, multiple_uris, header = separate_uris(digitization_tracking_sheet)
	digitized_folder_list = get_file_list(file_location)
	files_not_ingested = get_files_not_ingested(digitized_folder_list, previous_file_list)
	match_files(single_uris, files_not_ingested, output_path, header)

if __name__ == '__main__':
	main()