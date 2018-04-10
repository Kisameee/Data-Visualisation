#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Class for handling the reading of a Dataset (CSV for the moment)
TODO: Implement Row class for comparing rows
"""


import csv
from pprint import pprint
from functools import partial
from datetime import datetime


class DatasetReader:
    """
    Class for reading a Dataset
    TODO: Handle Kwargs properly
    TODO: Implement [], >, < operator OR Row Class
    """

    def __init__(self, file_path: str, cols_types: dict=None, **kwargs):
        """
        Initiate the Dataset Reader class with the file to read and
        the dict mapping columns to theirs types
        :param file_path: The file_path of the file to read as dataset
        :param cols_types: The optional columns type of the data in the dataset
        :param kwargs: Allow others arguments like the separator of the file, its encoding, etc
        """
        sep = kwargs['sep'] if 'sep' in kwargs else ','
        encoding = kwargs['encoding'] if 'encoding' in kwargs else ','
        with open(file=file_path, encoding=encoding) as dataset:
            csv_reader = csv.DictReader(dataset, delimiter=sep)
            self.columns = csv_reader.fieldnames
            self.values = list()
            for row in csv_reader:
                if cols_types:
                    typed_row = self._typed_parser(row, cols_types)
                    self.values.append(typed_row)
                else:
                    self.values.append(row)

    def _typed_parser(self, row: dict, data_types) -> dict:
        """
        Parse a untyped row and transform it ro a typed one
        :param row: The row to type
        :param data_types: The type of data to use
        :return: A typed row as dict
        """
        typed_row = dict()
        for col, typed in data_types.items():
            typed_row[col] = typed(row[col])
        self.values.append(typed_row)
        return typed_row

    def sort(self, sort_func: dict):
        """
        Sort the Dataset by a one multiple columns
        TODO: To implement
        :param sort_func: A dict mapping the columns name and the function to use to sort
        """
        pass

    def __get__(self, instance, owner):
        pass


def date_parser(date: str, parser: str) -> datetime:
    """
    Wrapper around datetime.strptime to use with partial
    :param date: The date as string to parser
    :param parser: The date parser to use
    :return: The Date as datetime object
    """
    return datetime.strptime(date, parser)


if __name__ == '__main__':
    date_parser = partial(date_parser, parser='%d/%m/%Y')
    columns_types = {'ID': str, 'Sexe': str, 'Date de naissance': date_parser, 'Taille (cm)': int,
                  'Pointure': int, 'Note exam': str}
    dr = DatasetReader(file_path='./ressources/test_data.csv', cols_types=columns_types,
                       sep=';', encoding='utf-8-sig')
    pprint(dr.values)
