#!/usr/bin/python3

import csv
import os


def main():
    target_path = input('Please enter target file list path: ')
    out_fp = input('Please enter path to output CSV: ')
    with open(out_fp, 'w', encoding='utf8') as ofile:
        writer = csv.writer(ofile)
        writer.writerow(['filepath'])
        for dirpath in os.listdir(target_path):
            full_path = os.path.join(target_path, dirpath)
            writer.writerow([full_path])
        # for dirpath, dirnames, filenames in os.walk(target_path):
        #     for dirname in dirnames:
        #         full_path = os.path.join(dirpath, dirname)
        #         writer.writerow([full_path])
            # for filename in filenames:
            #    full_path = os.path.join(dirpath, filename)
            #    writer.writerow([full_path])


if __name__ == "__main__":
    main()