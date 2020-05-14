import csv
from datetime import datetime
from os import path, listdir, mkdir
import numpy as np
from shutil import move, copy2
from processing.DataProcessors import DataProcessors


class CSVConverters:

    @staticmethod
    def write_data(data, root='General', suffix=None):
        """Writes the values in data into a timestamped csv file."""

        print('Saving as csv')

        filename = 'Training Data\\{0}\\{1}'.format(root, datetime.now().strftime("%Y-%m-%d %H_%M_%S"))

        if suffix is not None and type(suffix) is int:
            # Add a label to the end of filename - used for simulated files
            filename = '..\\' + filename
            filename += '_' + str(suffix)

        filename += '.csv'

        written = 0
        with open(filename, 'w', newline='') as f:
            col_headers = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']
            if len(data[0]) == 9:
                col_headers.extend(['mx', 'my', 'mz'])
            try:
                f_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                f_writer.writerow(col_headers)
                for line in data:
                    f_writer.writerow(line)
                    written += 1
            except Exception as e:
                print(str(e))
                return -1

        return written

    @staticmethod
    def csv_to_list(filename, remove_mag=True):
        """Reads a csv file and saves the values as a list type."""

        data = []
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                if row[0] != 'ax':
                    if remove_mag and len(row) == 9:
                        data.append([float(val) for val in row[:-3]])
                    else:
                        data.append([float(val) for val in row])
        return data

    @staticmethod
    def get_data_files(root=r'..\Training Data'):
        """Finds all csv data files in a root directory - returns found files along with their class labels."""

        print('Parsing data in root directory \'%s\'\n' % root[root.rfind('\\') + 1:])

        root = path.normpath(root)
        dirs = [path.join(root, d) for d in listdir(root) if path.isdir(path.join(root, d)) and 'General' not in d]
        all_files = []
        all_labels = []

        if dirs != 0:
            for directory in dirs:
                label = int(directory[directory.rfind('_') + 1:])  # Label should be after final underscore of dirname
                files = [path.join(directory, f) for f in listdir(directory) if
                         (path.isfile(path.join(directory, f)) and ('.csv' in f))]
                if len(files) != 0:
                    for file in files:
                        all_files.append(file)
                        all_labels.append(label)

        return [all_files, all_labels]

    @staticmethod
    def split_data(root=r'..\Training Data', target=r'..\Validation Data',
                     split_size=42, dir_prefix='06Apr_Generated_Validation_WalkingDynamic_', copy=True):
        """Randomly moves a given number of files from one root directory to another - used for dataset splitting.

        Args:
            root (str): The directory holding the files to be randomly moved elsewhere.
            target (str): The directory where a new directory filled with the randomly selected files will be created.
            split_size (str): The number of files to be randomly selected.
            dir_prefix (str): The major part of the new directory name. The minor part will be the class label.
            copy (bool): Whether to just copy the files or actually move them. For testing and anti-idiocy.

        Return:
            (list): A list with the total number of files moved for each activity/action.
        """

        files, labels = CSVConverters.get_data_files(root)
        unique_labels, counts = np.unique(labels, return_counts=True)  # No. of different classes present in root dir

        if len(unique_labels) != 0:
            for label in unique_labels:
                # Create new directory for each class in root that will hold the randomly selected files

                dir_name = dir_prefix + str(label)
                dir_path = path.join(target, dir_name)
                if not path.exists(dir_path):
                    try:
                        mkdir(dir_path)
                    except OSError as e:
                        print('Could not create dir: ' + dir_name)
                        print(e)
                        return -1

            dir_counts = np.zeros(8)  # Scale this up if more classes added in future
            chosen = np.random.choice(files, size=split_size, replace=False)

            for file in chosen:
                # Move (or copy) each of the randomly chosen files into the relevant target directory child

                label = labels[files.index(file)]
                dir_name = dir_prefix + str(label)
                full_dir_name = path.join(target, dir_name)
                filename = file[file.rfind('\\')+1:]

                # Check destination directory exists and there isn't already a copy of this file present in there
                if path.exists(full_dir_name) and not path.exists(path.join(full_dir_name, filename)):

                    try:
                        if copy:
                            print('Copying ' + file + ' to ' + full_dir_name)
                            copy2(file, full_dir_name)
                        else:
                            print('Moving ' + file + ' to ' + full_dir_name)
                            move(file, full_dir_name)
                        dir_counts[label] += 1
                    except Exception as e:
                        print('Error copying/moving ' + file + ' to ' + full_dir_name)
                        print(e)
                        return False
                else:
                    return False

            return dir_counts

    @staticmethod
    def mirror_data(root=r'..\Training Data', target=r'..\Training Data',
               output_dir='23Mar_Train_LeftFallMirrored_4', mask=(1, 1, 1, 1, 1, 1)):
        """Alters all the values of the data files in a director depending on a multiplication mask.
           Used for simulating data files (e.g. left falls) from real ones (e.g. right falls) by flipping axial values.
        """

        files, labels = CSVConverters.get_data_files(root)

        dir_path = path.join(target, output_dir)
        if not path.exists(dir_path):
            try:
                mkdir(dir_path)
            except OSError as e:
                print('Could not create dir: ' + dir_path)
                print(e)
                return -1

        success_counts = 0
        for file in files:
            data = CSVConverters.csv_to_list(file)
            mirrored_data = DataProcessors.mirror(data, mask=mask)
            success = CSVConverters.write_data(mirrored_data, root=output_dir, suffix=success_counts)
            if success == -1:
                print('Failed to save data for', file)
                return -1
            else:
                success_counts += 1

        return success_counts


class Tests:
    def __init__(self):
        pass

    @staticmethod
    def test_directories():
        pass


if __name__ == '__main__':
    """Uncomment line below when ready to run train/test/validation splitting."""
    # print(CSVConverters.split_data(copy=True)) NEVER SET COPY=FALSE AND RUN UNLESS READY TO SPLIT TEST/VAL/TRAIN

    """Uncomment line below when ready to simulate some actions. mask is in ax, ay, az, gx, gy, gz order."""
    # CSVConverters.mirror_data(mask=(1, -1, 1, 1, 1, -1))
