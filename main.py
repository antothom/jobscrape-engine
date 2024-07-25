import numpy as np

from fetcher import DataFetcher
from extractor import Extractor
import os
import pandas as pd

data = pd.read_excel('JobBoards.xlsx', skiprows=1)

data_dict = data[['name', 'Link', 'source']]

jobs_list = []

for job_board in data_dict.iterrows():
    # if link is not None
    if job_board[1]['Link'] is not None:
        try:
            data_fetcher = DataFetcher.create([job_board[1]['Link']], job_board[1]['source'], job_board[1]['name'])

            data_fetcher.get_data()

            data_extractor = Extractor.create(data_fetcher)

            data_extractor.extract_job_list()

            jobs_list.append(data_extractor.jobs_list)
            print(f"SUCCESS: Data fetched for {job_board[1]['name']}")
        except Exception as e:
            if e.args[0] == 'Invalid source type':
                print(f"ERROR: Invalid source type for {job_board[1]['name']}")
            elif e.args[0] == 'There is no extractor for the given Job Board':
                print(f"ERROR: There is no extractor for the given Job Board {job_board[1]['name']}")
            elif e.args[0] == 'Invalid XML data':
                print(f"ERROR: Invalid XML data for {job_board[1]['name']}")
            else:
                raise e
    else:
        print(f"NO data for {job_board[1]['name']}")



# flatten the list of dictionaries jobs_list
jobs_list = [job for jobs in jobs_list for job in jobs]

jobs_frame = (pd.DataFrame(jobs_list))
jobs_frame.to_excel('jobs_list.xlsx', index=False)