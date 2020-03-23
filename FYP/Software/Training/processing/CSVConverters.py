import csv
from datetime import datetime
from os import path, listdir, mkdir
import numpy as np
from shutil import move, copy2
from processing.DataProcessors import DataProcessors


class CSVConverters:
    def __init__(self):
       None

    @staticmethod
    def write_data(data, root='General', suffix=None): # TODO: only works because only method to call this (gui) currently shares same parent directory as 'Training Data'
        print('Saving as csv')
        filename = 'Training Data\\{0}\\{1}'.format(root, datetime.now().strftime("%Y-%m-%d %H_%M_%S"))

        if suffix is not None and type(suffix) is int:
            filename = '..\\' + filename
            filename += '_' + str(suffix)

        filename += '.csv'

        written = 0
        with open(filename, 'w', newline='') as f:
            col_headers = ['ax', 'ay', 'az', 'gx', 'gy', 'gz']  #  'mx', 'my', 'mz']
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
    def get_data_files(root=r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data'): # TODO: See write_data
        print('Parsing data in root directory \'%s\'\n' % root[root.rfind('\\') + 1:])
        root = path.normpath(root)
        dirs = [path.join(root, d) for d in listdir(root) if path.isdir(path.join(root, d)) and 'General' not in d]
        all_files = []
        all_labels = []

        if dirs != 0:
            for directory in dirs:
                label = int(directory[directory.rfind('_') + 1:])  # TODO: Regex practice!
                files = [path.join(directory, f) for f in listdir(directory) if
                         (path.isfile(path.join(directory, f)) and ('.csv' in f))]
                if len(files) != 0:
                    for file in files:
                        all_files.append(file)
                        all_labels.append(label)

        return [all_files, all_labels]

    @staticmethod
    def get_test_set(root=r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data',
                     target=r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Validation Data',
                     test_size=42, dir_prefix='23Mar_Generated_Validation_RightFall_', copy=True):

        files, labels = CSVConverters.get_data_files(root)

        unique_labels, counts = np.unique(labels, return_counts=True)
        if len(unique_labels) != 0:
            for label in unique_labels:
                dir_name = dir_prefix + str(label)
                dir_path = path.join(target, dir_name)
                if not path.exists(dir_path):
                    try:
                        mkdir(dir_path)
                    except OSError as e:
                        print('Could not create dir: ' + dir_name)
                        print(e)
                        return -1

            dir_counts = np.zeros(8)
            chosen = np.random.choice(files, size=test_size, replace=False)
            for file in chosen:
                label = labels[files.index(file)]
                dir_name = dir_prefix + str(label)
                full_dir_name = path.join(target, dir_name)
                filename = file[file.rfind('\\')+1:]

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

            return dir_counts #  == test_size

    @staticmethod
    def mirror(root=r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data',
               target=r'C:\\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data',
               output_dir='23Mar_Train_LeftFallMirrored_4', mask=(1, 1, 1, 1, 1, 1)):

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
    test = r'C:\Users\blaze\Desktop\Programming\Uni\trunk\FYP\Software\Training\Training Data'
    #print(CSVConverters.get_test_set(copy=True))

    #CSVConverters.mirror(mask=(1, -1, 1, 1, 1, -1))
