import os
import sys
import csv

def Import_Files(): #This function will examine all game files in the current directory and extract the useful information from them. It returns a dictionary of indexable data.
	Folder = sys.path[0]
	entries = os.listdir(Folder)
	data = {"file":[], "name":[], "level":[], "target":[], "goal":[], "engagement":[], "age":[], "description":[], "note":[]}	#Initilizes a dictionary that is stores all the data.
	for entry in entries:
		if "_game.txt" in entry:				#Determines what local files are game files
			data['file'].append(entry)
	for entry in data['file']:
		for header in list(dict.keys(data)):
			if header == 'file':
				continue
			data[header].append('')		#This creates a new list entry for each valid file. Making sure that data isn't entered twice

		with open(entry) as f:			#Go through each game file and extract the relevant data from the lines. If there are duplicates they will be overwritten
			line = f.readline()
			while line:
				split = line.split(":", 1)
				if len(split) > 1:
					if split[0] == "Name ":
						data['name'][-1] = (split[1].strip())
					elif split[0] == "Level ":
						data['level'][-1] = (split[1].strip())
					elif split[0] == "Target ":
						data['target'][-1] = (split[1].strip())
					elif split[0] == "Goal ":
						data['goal'][-1] = (split[1].strip())
					elif split[0] == "Engagement ":
						data['engagement'][-1] = (split[1].strip())
					elif split[0] == "Age ":
						data['age'][-1] = (split[1].strip())
					elif split[0] == "Description ":
						data['description'][-1] = (split[1].strip())
					elif split[0] == "Note ":
						data['note'][-1] = (split[1].strip())
					else:
						print("There was an exception. Please sanitize the files ", entry, "Since it has a line called ", split[0]) #Lets user know there wasn't a parsed line.
				line = f.readline()
	return data

def Sort_Data(Info, Reference):
	Info2 = {"name":[], "level":[], "target":[], "goal":[], "engagement":[], "age":[], "description":[], "note":[]}
	for i in range(len(Info['file'])):
		#name
		if Info['name'][i] == '':
			print("The file: ", Info['file'][i], " is not formatted correctly. Please add a name.")
			continue
		elif len(Info['name'][i]) > 32:
			print("The file: ", Info['file'][i], "has a name that is too long. Please shorten it.")
		#Description
		if Info['description'][i] == '':							#If there is no description let the user know and discard the game.
			print("The file: ", Info['file'][i], " is not formatted correctly. Please add a Description.")
			continue
		#Note; notes don't need to be sanitized at the moment
		
		Info2['name'].append(Info['name'][i])
		Info2['description'].append(Info['description'][i])
		Info2['note'].append(Info['note'][i])
	
		#level #target #goal #engagement #Age
		Electables = ['level', 'target', 'goal', 'engagement', 'age'] #Define the Definable Characteristics of the game.
		for section in Electables:									#Iterate over all the different Electables
			if Info[section][i] == '':								#If there is no Value, then set the value to all and continue
				Info2[section].append('ALL')
			else:
				cut_down = Info[section][i].split(',')				#Split the potential multiple entries into seperates.
				Complete_and_True = []								#Create an empty list to dump valid values into.
				for j in range(len(cut_down)):
					cut_down[j] = cut_down[j].strip()				#Strip whitespace off the inputs.
					if cut_down[j] in Reference[section]:			 #Look at the reference of valid values for that section. If it doesn't exist let the user no and discard that result.
						Complete_and_True.append(cut_down[j])
					else:
						print("There is a value called ", cut_down[j], "in file ", Info['file'][i], 'which is not supported please change and import again if you want to update this.')			#If it does exist Append it as a discreet value to that section.
				if Complete_and_True == []:
					Complete_and_True.append('ALL')
				Info2[section].append(Complete_and_True)

	return Info2

def Write_Directory(Info2):
	with open('directory.csv', 'w') as csv_file:
			fieldnames = list(dict.keys(Info2))
			writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
			writer.writeheader()
			for i in range(len(Info2['name'])):
				Info3 = {	"name":Info2['name'][i],
							"level":Info2['level'][i],
							"target":Info2['target'][i],
							"goal":Info2['goal'][i],
							"engagement":Info2['engagement'][i],
							"age":Info2['age'][i],
							"description":Info2['description'][i],
							"note":Info2['note'][i]}
				writer.writerow(Info3)
	return

Reference = {"level": ['ALL','SS1', 'SS2', 'SS3', 'SS4', 'HFC', 'HFD', 'HFE', 'HFF', 'HFG', 'HFH', 'HFI', 'HFJ', 'TB1', 'TB2', 'TB3', 'TB4', 'TB5', 'TB6'],
			"target":['ALL', 'Vocabulary', 'Grammar', 'Dialogue', 'Reading','Writing', 'Reset'], 
			"goal":['ALL', 'Introduction', 'Practice', 'Test', 'Consolidate', 'Fun'],
			"engagement":['ALL', 'Individual', 'Pairs', 'Small Groups', 'Whole Class'],
			"age":['3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15'],}

Info = Import_Files()
Info2 = Sort_Data(Info, Reference)
Write_Directory(Info2)
