"""
Data Interpretation
===================

Multiple functions for entering data into python code.


"""

from collections import defaultdict
import csv

def readCSV(fileName, DISPLAY_OUTPUT=None):
    """Reads and turns .csv file types into lists for interpretation with
    other functions.

    Parameters
    ----------
    fileName : str
        Relative filepath to .csv
    DISPLAY_OUTPUT : bool
        Whether to display function reading details

    Returns
    -------
    CSVasList : list
        The .csv columns as lists outputs

    Notes
    -----
    Reworked from Kerri-Ann Norton's code.

    IN THE WORKS

    Examples
    --------

    """

    with open(fileName, newline='') as csvfile:
        _reader = csv.reader(csvfile, delimiter = ',')
        line_count = 0
        _data = defaultdict(list)
        for row in _reader:
            if line_count == 0:
                if DISPLAY_OUTPUT == True:
                    print(f'Column names are {", ".join(row)}')
                    print
                    print("===============")
                    print("")
                print(row)
                # FIX THIS
                #
                for row in range(len(row)):
                    print(row)
                    _data[row] = []
                line_count += 1
                print(_data)
            else:
                # and is {row[2]}
                if DISPLAY_OUTPUT == True:
                    #for i in range()
                    print(f'Revenue from Arcades (in billions): \t{row[0]} and CS doctorates in US: {row[1]}.')
                #arcadeRevenues.append(float(row[0]))
                #csPhDs.append(int(row[1]))
                line_count += 1
        print(f'Processed {line_count} lines.')
    return None #csPhDs, arcadeRevenues

a, b = readCSV("/Users/hew_/Documents/GitHub/hewpy/src/statpy/test.csv", True)