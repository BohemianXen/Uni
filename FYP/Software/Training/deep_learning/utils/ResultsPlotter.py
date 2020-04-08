from sklearn import metrics
import matplotlib.pyplot as plt
import pandas as pd
import os.path as path
import numpy as np


# TODO: Add load file and plot functions in future
class ResultsPlotter:
    def __init__(self, labels, guesses, test_matrix, filename='', history=None):
        self.names = ['Standing', 'Walking', 'Lying_F', 'Lying_L', 'Lying_R', 'Fall_F', 'Fall_L', 'Fall_R']
        self.fall_head = 5  # index of first fall action
        self.labels = labels
        self.guesses = guesses
        self.test_matrix = test_matrix
        self.filename = filename
        self.history = history

        self.df = pd.DataFrame(metrics.classification_report(self.labels, self.guesses, target_names=self.names,
                                                             digits=4, output_dict=True, zero_division=0.0))
        self.supports = self.df.iloc[3, :-3]
        self.df = self.df.drop(['f1-score', 'support'])
        self.df = self.df.drop(['macro avg', 'weighted avg'], axis=1)

        self.concatenate_report()
        if self.history is not None:
            self.add_history()

        if self.filename != '':
            self.write_to_file()

    def print_test_matrix(self):
        print('Confusion Matrix:')
        for row in self.test_matrix:
            print(row)
        print('\n')

    def print_test_report(self):
        print('Test Report:')
        print(metrics.classification_report(self.labels, self.guesses, target_names=self.names,
                                            digits=4, zero_division=0.0))
        print('\n')

    def concatenate_report(self):
        recalls = self.df.iloc[1, :-1].values
        accuracy = self.df.iloc[0, -1]
        self.df = self.df.drop('recall')
        self.df = self.df.drop('accuracy', axis=1)
        # self.df.columns.add_suffix('_PR')

        total_added = 0
        for i, col_name in enumerate(self.df.columns):
            self.df.rename(columns={col_name: col_name + '_PR'}, inplace=True)
            self.df.insert(i + 1 + total_added, column=col_name + '_SE', value=recalls[i])
            total_added += 1

        [self.df['global_PR'], self.df['global_SE'], self.df['global_SP']] = self.calculate_global_metrics()
        self.df['test_ACC'] = accuracy

    def calculate_global_metrics(self):
        r_fall_head = len(self.names) - self.fall_head  # reverse index of first fall index
        falls = self.test_matrix[self.fall_head:, self.fall_head:]
        adls = self.test_matrix[:-r_fall_head, :-r_fall_head]

        tp = np.sum(falls)  # np.sum(np.dot(falls, np.identity(3)))  For inter-fall stats
        tn = np.sum(adls)  # np.sum(np.dot(adls, np.identity(5)))  For inter-adl stats
        fp = np.sum(self.test_matrix[:self.fall_head, self.fall_head:])  # (np.tril(self.test_matrix, k=-1))
        fn = np.sum(self.test_matrix[self.fall_head:, :self.fall_head])  # (np.triu(self.test_matrix, k=1))
        assert (tp + tn + fp + fn == self.supports.sum())

        pr = 0.0
        se = 0.0
        sp = 0.0

        # Zero divisions and NaNs are expected during learning rate testing for final year report
        try:
            pr = tp / (tp + fp)
        except Exception as e:
            print('Precision zero division')
            pass

        try:
            se = tp / (tp + fn)
        except Exception as e:
            print('Sensitivity zero division')

        try:
            sp = tn / (tn + fp)
        except Exception as e:
            print('Sensitivity zero division')

        print('GLOBAL STATS:\tPrecision = %.4f, Sensitivity = %.4f, Specificity = %.4f\n' % (pr, se, sp))

        return [pr, se, sp]

    def add_history(self):
        self.df['train_ACC'] = self.history.history['accuracy'][-1]
        self.df['val_ACC'] = self.history.history['val_accuracy'][-1]
        self.df['train_LOSS'] = self.history.history['loss'][-1]
        self.df['val_LOSS'] = self.history.history['val_loss'][-1]

    def write_to_file(self):
        full_path = path.abspath(self.filename)

        try:
            if path.exists(full_path):
                self.df.to_csv(full_path, sep=',', mode='a', header=False, index=False)
            else:
                self.df.to_csv(full_path, sep=',', mode='w', header=True, index=False)
            return True
        except Exception as e:
            print(e)
            return False
