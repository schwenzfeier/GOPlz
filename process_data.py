import yaml
import pandas as pd
from pandas.io.json import json_normalize


## Reading in data from ProPublica
## Source: https://github.com/unitedstates/congress-legislators

with open('data/legislators-current.yaml', 'r') as f:
	leg = yaml.load(f)
	f.close()

with open('data/legislators-social-media.yaml', 'r') as f:
	soc = yaml.load(f)
	f.close()

print('Data read')

## Putting together a list of all of the legislators
headers = ['id', 'first_name', 'last_name', 'type', 'state', 'district', 'party']
rows = []

for person in leg:
	id = person['id']['bioguide']
	first = person['name']['first']
	last = person['name']['last']
	current_term = person['terms'][-1]
	type = current_term['type']
	state = current_term['state']
	if type == 'rep':
		district = current_term['district']
	else:
		district = None
	party = current_term['party']
	row = [id, first, last, type, state, district, party]
	rows.append(row)

# convert to pandas df
leg_df = pd.DataFrame(rows, columns = headers)


## Putting together a list of all twitter handles and twitter IDs
headers = ['id', 'twitter_handle']
rows = []
for s in soc:
	id = s['id']['bioguide']
	if 'twitter' in s['social'].keys():
		twitter_handle = s['social']['twitter']
	else:
		print(id)
		twitter_handle = None
		twitter_id = None
	row = [id, twitter_handle]
	rows.append(row)

# convert to df
soc_df = pd.DataFrame(rows, columns = headers)


### Merging social and leg data together
df = leg_df.merge(soc_df, left_on = 'id', right_on = 'id', how = 'outer')

## Putting together a list of people losing care by CD
sen_cap = pd.read_csv('data/cap_state_data.csv')
house_cap = pd.read_csv('data/cap_house_data.csv')
cap_data = sen_cap.append(house_cap, ignore_index = True)


df = df.merge(cap_data, left_on = ['state', 'district'], right_on = ['state', 'district'], how = 'left')

## savin'
df.to_csv('data/cong_data_full_merged.csv', encoding = 'utf-8', index = False)
