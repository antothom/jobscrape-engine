import numpy as np

from fetcher import DataFetcher
from extractor import Extractor
import os
import pandas as pd

data = pd.read_excel('JobBoards.xlsx')


data = data.dropna(subset=['Implemented'])
data = data[data['Platform'] == 'Dover']

data_dict = data[['Name', 'Job Feed', 'Platform', 'Source']]

jobs_list = []

for job_board in data_dict.iterrows():
    # if link is not None
    if job_board[1]['Job Feed'] is not None:
        try:
            data_fetcher = DataFetcher.create([job_board[1]['Job Feed']], job_board[1]['Source'], job_board[1]['Name'], job_board[1]['Platform'])

            data_fetcher.get_data()

            data_extractor = Extractor.create(data_fetcher)

            data_extractor.extract_job_list()

            jobs_list.append(data_extractor.jobs_list)
            print(f"SUCCESS: Data fetched for {job_board[1]['Name']}")
        except Exception as e:
            if e.args[0] == 'Invalid source type':
                print(f"ERROR: Invalid source type for {job_board[1]['Name']}")
            elif e.args[0] == 'There is no extractor for the given Job Board':
                print(f"ERROR: There is no extractor for the given Job Board {job_board[1]['Name']}")
            elif e.args[0] == 'Invalid XML data':
                print(f"ERROR: Invalid XML data for {job_board[1]['Name']}")
            else:
                print(f"ERROR: {e} for {job_board[1]['Name']}")
    else:
        print(f"NO data for {job_board[1]['Name']}")



# flatten the list of dictionaries jobs_list
jobs_list = [job for jobs in jobs_list for job in jobs]

jobs_frame = (pd.DataFrame(jobs_list))
jobs_frame.to_excel('jobs_list.xlsx', index=False)