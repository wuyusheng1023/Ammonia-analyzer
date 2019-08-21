
import os
import pandas as pd
from datetime import datetime, timedelta
from pymongo import MongoClient

# data output folder
data_folder = 'data'

# Mongo DB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["NH3"]
col = db["raw_data"]

# Create target Directory
dir_path = os.path.dirname(os.path.realpath(__file__))
data_dir = dir_path + os.sep + data_folder
try:
    os.mkdir(data_dir)
    print("Directory " , data_dir ,  " Created ") 
except FileExistsError:
    print("Directory " , data_dir ,  " already exists")

# get date
print('date input formate: %Y-%m-%d, like "2010-03-21"')
start = input('input start date: ')
end = input('input end date: ')

start = datetime.strptime(start, '%Y-%m-%d')
end = datetime.strptime(end, '%Y-%m-%d')
days = [start + timedelta(i) for i in range((end-start).days + 1)]

for day in days:
	day_str = day.strftime('%Y-%m-%d')
	next_day_str = (day + timedelta(1)).strftime('%Y-%m-%d')
	file_name = data_dir + os.sep + day_str
	print(file_name, flush=True)
	query = {'date_time': {'$gte': day_str, '$lte': next_day_str}}

	# load data
	cursor = col.find(query)
	df =  pd.DataFrame(list(cursor))

	# Delete the _id
	if '_id' in df: del df['_id']

	# save data
	df.to_pickle(file_name + '.pkl')
	df.to_pickle(file_name + '.csv', index=False)

