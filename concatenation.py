import glob
import os
import pandas as pd



def startConcatenation(filename='result'):
    try:
        all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]
        combine_csv = pd.concat([pd.read_csv(file) for file in all_filenames])
        combine_csv.to_csv(f'{filename}.csv', index=False, encoding='utf-8-sig')

        return 'success'

    except Exception:
        return 'error'

