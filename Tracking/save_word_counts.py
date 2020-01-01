import json, datetime 

with open('data.json') as json_file:
	old_data = json.load(json_file)


today = datetime.date.today().strftime("%Y-%m-%d")
time = datetime.datetime.now().strftime("%H:%M:%S")

# Add time to list
if today in old_data.keys():
	times = old_data[today]['times']
else:
	times = []
times.append(time)


# Read in files
word_counts = {}
try: 
	with open('word_counts.out', 'r') as f:
		for i, line in enumerate(f): 
			if i % 2 == 0:
				temp_name = line.rstrip()
			else:
				word_counts[temp_name] = int(line.rstrip())
except:
	print("Critical Failure on word_counts")

latex_counts = {}
try: 
	with open('latex_counts.out', 'r') as f:
		for line in f:
			count, temp_name = line.split()
			latex_counts[temp_name] = count
except:
	print("Critical Failure on latex_counts")


# Save data
new_data ={'word_counts':word_counts, 
			'latex_counts':latex_counts,
			'times': times
			}

old_data[today] = new_data

with open('data.json', 'w') as json_file:
	json.dump(old_data, json_file, indent=4, sort_keys=True)



