import os

import shutil
import random

from google_drive_downloader import GoogleDriveDownloader as gdd

from common.utils import get_txt_files

parent_dir = '../datasets/email-EuAll'

files = (
    ('email-EuAll', '1HNw17l-PtdVgcMcWnCsZndGEWVjin3Oz'),
)

if __name__ == '__main__':
    os.makedirs(parent_dir, exist_ok=True)

    for file_base, drive_id in files:
        gdd.download_file_from_google_drive(file_id=drive_id,
                                            dest_path='{}/{}.zip'.format(parent_dir, file_base),
                                            unzip=True, showsize=True)

        data_files = get_txt_files('{}/{}/'.format(parent_dir, file_base))

        # read lines
        lines = []
        for data_file in data_files:
            with open(data_file) as file:
                lines += file.readlines()

        shutil.rmtree('{}/{}/'.format(parent_dir, file_base))

        subsets = [
            (100.0, '100'),
            (75.0, '75'),
            (50.0, '50'),
            (25.0, '25'),
            (10.0, '10'),
            (5.0, '5'),
            (1.0, '1'),
            (0.1, '01'),
            (0.01, '001'),
        ]

        num_lines = len(lines)

        for percent, suffix in subsets:
            k = int(num_lines * percent / 100.0)

            i = 0
            reservoir = ['x'] * k

            for line in lines:
                if i < k:
                    reservoir[i] = line
                else:
                    j = random.randrange(i + 1)
                    if j < k:
                        reservoir[j] = line

                i += 1

            os.makedirs('{}/{}_{}/'.format(parent_dir, file_base, suffix), exist_ok=True)
            with open('{}/{}_{}/data.txt'.format(parent_dir, file_base, suffix), 'w') as new_f:
                for line in reservoir:
                    try:
                        source_id, target_id = line.split()
                        new_f.write('{},{}\n'.format(source_id, target_id))
                    except:
                        print('Error in line > {}'.format(line))