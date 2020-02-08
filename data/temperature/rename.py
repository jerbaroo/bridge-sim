import os

months = ["jan", "feb", "march", "april", "may", "june", "july", "aug", "sep", "oct", "nov", "dec"]
files = [f for f in os.listdir('.') if os.path.isfile(f)]

for i, month in enumerate(months):
	month_i = i + 1
	month_id = "0" + str(month_i) if month_i <= 9 else str(month_i)
	print(files)
	month_files = [f for f in files if f.endswith(month_id + ".dat")]
	print(month_files)
	assert len(month_files) == 1	
	print(month_files)
	os.rename(month_files[0], month + ".txt")
