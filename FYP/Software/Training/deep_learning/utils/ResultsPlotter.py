from sklearn import metrics
import matplotlib.pyplot as plt
import pandas as pd
import os.path as path
import numpy as np

class ResultsPlotter:
    def __init__(self, test_matrix, labels, guesses, filename=''):
        self.names = ['Standing', 'Walking', 'Lying_F', 'Lying_L', 'Lying_R', 'Fall_F', 'Fall_L', 'Fall_R']
        self.fall_head = 5  # index of first fall action
        self.test_matrix = test_matrix
        self.labels = labels
        self.guesses = guesses
        self.df = pd.DataFrame(metrics.classification_report(self.labels, self.guesses, target_names=self.names, digits=4, output_dict=True))
        self.supports = self.df.iloc[3, :-3]
        self.df = self.df.drop(['f1-score', 'support'])
        self.df = self.df.drop(['macro avg', 'weighted avg'], axis=1)

        self.filename = filename
        if self.filename != '':
            self.write_to_file()

    def print_test_matrix(self):
        print('Confusion Matrix:')
        for row in self.test_matrix:
            print(row)
        print('\n')

    def print_test_report(self):
        print('Test Report:')
        print(metrics.classification_report(self.labels, self.guesses, target_names=self.names, digits=4))
        print('\n')

    def concatenate_report(self):
        placeholder = self.df.copy(deep=False)
        recalls = self.df.iloc[1, :-1].values
        accuracy = self.df.iloc[0, -1]
        self.df = self.df.drop('recall')
        self.df = self.df.drop('accuracy', axis=1)
        total_added = 0
        for i, col_name in enumerate(self.df.columns):  # TODO: Row still named precision technically
            self.df.rename(columns={col_name: col_name + '_PR'}, inplace=True)
            self.df.insert(i + 1 + total_added, column=col_name + '_SE', value=recalls[i])
            total_added += 1

        [self.df['global_PR'], self.df['global_SE'], self.df['global_SP']] = self.calculate_global_metrics()
        self.df['global_ACC'] = accuracy

    def calculate_global_metrics(self):
        r_fall_head = len(self.names) - self.fall_head  # reverse index of first fall index
        falls = self.test_matrix[self.fall_head:, self.fall_head:]
        adls = self.test_matrix[:-r_fall_head, :-r_fall_head]
        tp = np.sum(falls)  # np.sum(np.dot(falls, np.identity(3)))  For inter-fall stats
        tn = np.sum(adls)  # np.sum(np.dot(adls, np.identity(5)))  For inter-adl stats
        fp = np.sum(self.test_matrix[:self.fall_head, self.fall_head:])  # (np.tril(self.test_matrix, k=-1))
        fn = np.sum(self.test_matrix[self.fall_head:, :self.fall_head])  # (np.triu(self.test_matrix, k=1))
        assert (tp + tn + fp + fn == self.supports.sum())
        pr = tp / (tp + fp)
        se = tp / (tp + fn)
        sp = tn / (tn + fp)
        print('GLOBAL STATS:\tPrecision = %.4f, Sensitivity = %.4f, Specificity = %.4f\n' % (pr, se, sp))
        return [pr, se, sp]

    def write_to_file(self):
        if path.exists(self.filename):
            with open(self.filename) as f:
                self.test_report.to_csv(f, 'a', header=False)
        else:
            try:
                with open(self.filename) as f:
                    self.test_report.to_csv(f, 'w', header=True)
            except Exception as e:
                print(e)




