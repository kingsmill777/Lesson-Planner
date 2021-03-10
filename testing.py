import sharepy as sp
import os
import sys
import csv
import json
import PySimpleGUI as sg


def Import_Files(): #This function will examine all game files in the current directory and extract the useful information from them. It returns a dictionary of indexable data.
	Folder = sys.path[0]
	Final_Folder = os.path.join(Folder, 'Game Files')
	print(Final_Folder)
	entries = os.listdir(Final_Folder)
	data = {"file":[], "name":[], "level":[], "target":[], "goal":[], "engagement":[], "age":[], "description":[], "note":[]}	#Initilizes a dictionary that is stores all the data.
	for entry in entries:
		if "_game.txt" in entry:				#Determines what local files are game files
			data['file'].append(entry)
	for entry in data['file']:
		for header in list(dict.keys(data)):
			if header == 'file':
				continue
			data[header].append('')		#This creates a new list entry for each valid file. Making sure that data isn't entered twice
		File_Name = os.path.join(Final_Folder, entry)
		with open(File_Name) as f:			#Go through each game file and extract the relevant data from the lines. If there are duplicates they will be overwritten
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

def Sharepoint_Login(username, password):
	return sp.connect("english1com.sharepoint.com", username=username, password=password)

def Sharepoint_Import(s):
	
	
	URL_B = "https://english1com.sharepoint.com/sites/EF_XZS3/_api/web\/GetFolderByServerRelativeUrl('Shared Documents/Kingsley/Activity Finder/Game Files')/Files"
	URL_C = "https://english1com.sharepoint.com/sites/EF_XZS3/Shared Documents/Kingsley/Activity Finder/Game Files/"
	r = s.get(URL_B)
	q = json.loads(r.text)
	Names_of_Files = q['d']['results']
	Folder = sys.path[0]
	Final_Folder = os.path.join(Folder, 'Game Files')
	if not os.path.exists(Final_Folder):
		os.makedirs(Final_Folder)
	for i in range(len(Names_of_Files)):
		step1 = Names_of_Files[i]['Name']
		name = URL_C + step1
		Saved_file = os.path.join(Final_Folder, step1)
		s.getfile(name, filename=Saved_file)
	return(Final_Folder)

def LBox(values, key, size):			#This function defines the Listboxes that will be used to display the different data. Since the only thing that will chang is the key, the parameters will be set within this function.
	return sg.Listbox(values, enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE , size=(size,len(values)), pad=(0,0), no_scrollbar=True, key=key)
def TBox(values, size):					#This function defines the Text boxes above the Listboxes. Since their parameters won't change except the actual Text in them I can define it all here in this function.
	return sg.Text(values, justification='center', size=(size, 1), pad=(0,0))
def CBox(values, key, seeya):			#Combo boxes used for choosing what to sort the data set by. Some boxes will be invisible at the start. But other than that and the values they are the same so into this function they go.
	return sg.Combo(values, default_value='ALL', readonly=True, size =(12,len(values)), pad=(0,0), key=key, enable_events=True, visible=seeya)

def find(lst, value):		#Simple little Find function. I tried it in list syntax and it didn't work. Still I want to get this down to one line at some point.
	result = []
	for i, x in enumerate(lst):
		print(x)
		if value in x or x == 'ALL':
			result.append(i)
	return result

def CreateNumbers(value):			#Creates a numeric list of numbers of a custom size. This is useful for creating indexes of all my data sets.
	return list(range(0, len(value)))


Index = []			#Defining the data that will go in the listboxes. Appending to empty lists is the easiest way to ensure the program works properly.
Names = []
Level = []
Target = []
Goal = []
Engagement = []
Age = []
Description = []
Note = []
The_details = {"file":[], "name":[], "level":[], "target":[], "goal":[], "engagement":[], "age":[], "description":[], "note":[]}


def Reading():		#Reads the directory list. Due to how the directory is created there are some issues with list formatting carrying over. Once I tidy up the other code I might be able to reduce the resources this section uses.
	Index = []			#Defining the data that will go in the listboxes. Appending to empty lists is the easiest way to ensure the program works properly.
	Names = []
	Level = []
	Target = []
	Goal = []
	Engagement = []
	Age = []
	Description = []
	Note = []
	with open('directory.csv', mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		line_count = 0
		
		for row in csv_reader:
			Index.append(line_count)																#Reading in all the data from the CSV file but since I just want the strings I need to get rid of the list formatting.
			Names.append(row['name'].replace("'", ""))
			Level.append(row['level'].replace("'", "").replace("[", "").replace("]", ""))
			Target.append(row['target'].replace("'", "").replace("[", "").replace("]", ""))
			Goal.append(row['goal'].replace("'", "").replace("[", "").replace("]", ""))
			Engagement.append(row['engagement'].replace("'", "").replace("[", "").replace("]", ""))
			Age.append(row['age'].replace("'", "").replace("[", "").replace("]", ""))
			Description.append(row['description'].replace("'", "").replace("[", "").replace("]", ""))
			Note.append(row['note'].replace("'", "").replace("[", "").replace("]", ""))
			line_count += 1
	print(Names)
	return Index, Names, Level, Target, Goal, Engagement, Age, Description, Note


#Reading()  #TBH it seems weird to define a function only to just call it without any real need. It will be better when I tidy the code up.

Options1 = ['ALL','SS1', 'SS2', 'SS3', 'SS4', 'HFC', 'HFD', 'HFE', 'HFF', 'HFG', 'HFH', 'HFI', 'HFJ', 'TB1', 'TB2', 'TB3', 'TB4', 'TB5', 'TB6']  #Yes, yes, I should have better variable names. Anyway this defines what are appropriate options. I should have this code reference the other file at somepoint so I don't have to change two things if I want to change what is acceptable or not.
Options2 = ['ALL', 'Vocabulary', 'Grammar', 'Dialogue', 'Reading','Writing', 'Reset']
Options3 = ['ALL', 'Introduction', 'Practice', 'Test', 'Consolidate', 'Fun']
Options4 = ['ALL', 'Individual', 'Pairs', 'Small Groups', 'Whole Class']
Options5 = ['ALL', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
Reference = {"level": Options1, "target": Options2, "goal": Options3, "engagement": Options4, "age":Options5}
Step = {'Level':[], 'Target':[], 'Goal':[], 'Engagement':[], 'Age':[]} # Vital part of the sort function to pre-define this dictionary of empty lists. Again I know I should have better variable names.a
Name_Step = []
Sort_Ref = {21:'Level', 22:'Target', 23:'Goal', 24:'Engagement', 25:'Age'} #Not used but is actually useful for just remembering what each of the labels mean. Yes, yes, I know I should have better variable names. Shut up.
size_name = 20			#How else am I meant to tinker with over 30 different UI elements.
size_description = 60
size_default = 15
size_age = 6
col1 = [[sg.In(key=99,size=(size_name,1))]]		#Now I know I'm not a smart man or a good programmer but this UI was a real pain in the ass to program. I don't even know why I chose python for this I think this project would have been better in most other languages.
col2 = [[CBox(Options1, 21, True)],[CBox(Options1, 31, False)]]
col3 = [[CBox(Options2, 22, True)],[CBox(Options2, 32, False)]]
col4 = [[CBox(Options3, 23, True)],[CBox(Options3, 33, False)]]
col5 = [[CBox(Options4, 24, True)],[CBox(Options4, 34, False)]]
col6 = [[CBox(Options5, 25, True)],[CBox(Options5, 35, False)]]
col7 = [[sg.Text("-Activity Name-",enable_events=True, size=(50,1), pad=(0,1), key=41,background_color=('white'), text_color=('black'))],[sg.Multiline("-Description-",enable_events=True, size=(50,4), pad=(0,1), key=42,background_color=('white'), text_color=('black'))],[sg.Multiline("-Notes-",enable_events=True, size=(50,4), pad=(0,1), key=43,background_color=('white'), text_color=('black'))]] #3 is that really awkward number where its just easier to do each variable than make a function but if I have to add another multiline for whatever reason I'm going to kick myself.

layout = [[sg.Column(col1), sg.Column(col2), sg.Column(col3), sg.Column(col4), sg.Column(col5), sg.Column(col6), sg.Button('Sort'),sg.Column(col7)], # Beautiful but a real pain to figure out how to use. Creates a bunch of vertically aligned columns. Doing it any other way meant the combo boxes appeared in the wrong place.
			[TBox('Name', size_name), TBox('Level', size_default), TBox('Target', size_default),  TBox('Goal', size_default), TBox('Engagement', size_default), TBox('Age', size_default), TBox('Description', size_description)],
			[LBox(Names, 10, size_name),LBox(Level, 11, size_default), LBox(Target, 12, size_default), LBox(Goal, 13, size_default), LBox(Engagement, 14, size_default), LBox(Age, 15, size_default), LBox(Description, 16, size_description)],
			[sg.Button('Read'), sg.Button('Import'), sg.Button('SP Import'), sg.Button('Exit')]]


window = sg.Window('Activity Finder', layout) # What a deceptively and annoying line of code. You'd be forgiven for forgetting that the last 30 lines of code all go smushed into 'layout' and then called.

while True: # So this keeps the window alive and kicking. Also means there is a nice constant loop for events to trigger.
	events, values = window.read() # Makes the window.
	print(events) # Debugging tool that lets me know the key of UI element pressed.
	if events in (None, 'Exit'): # Standard Exit loop.
		break
	if events in (10,11,12,13,14,15,16): # This is what passes for a multi-columned listbox. What a mess. Whenever the index of one box is selected this function makes the other list elements highlight.
		indexes = window[events].GetIndexes()
		window[41].Update(Names[indexes[0]]) # This part updates the info box with useful information.
		window[42].Update(Description[indexes[0]])
		window[43].Update(Note[indexes[0]])
		for key in (10,11,12,13,14,15,16):
			window[key].Update(set_to_index=indexes)
	if events in (None, 'Sort'):		#I knew I went to University for something. Handling data is interesting. especially trying to sort a whole bunch. And Yes, I know this is technically a filter. Fuck off.
		Every = CreateNumbers(Index)	#Makes sure I'll go through every data entry.
		
		if values[21] == 'ALL':						#Start of Segment
			Step['Level'] = Every
		else:
			Step['Level'] = find(Level, values[21])
			if values[31] != 'ALL':
				Step['Level'] = list(set(Step['Level'] + find(Level, values[31])))
		if values[22] == 'ALL':						#Start of Segment
			Step['Target'] = Every
		else:
			Step['Target'] = find(Target, values[22])
			if values[32] != 'ALL':
				Step['Target'] = list(set(Step['Target'] + find(Target, values[32])))
		if values[23] == 'ALL':						#Start of Segment
			Step['Goal'] = Every
		else:
			Step['Goal'] = find(Goal, values[23])
			if values[33] != 'ALL':
				Step['Goal'] = list(set(Step['Goal'] + find(Goal, values[33])))
		if values[24] == 'ALL':						#Start of Segment
			Step['Engagement'] = Every
		else:
			Step['Engagement'] = find(Engagement, values[24])
			if values[34] != 'ALL':
				Step['Engagement'] = list(set(Step['Engagement'] + find(Engagement, values[34])))
		if values[25] == 'ALL':						#Start of Segment
			Step['Age'] = Every
		else:
			Step['Age'] = find(Age, values[25])
			if values[35] != 'ALL':
				Step['Age'] = list(set(Step['Age'] + find(Age, values[35])))
		Combo1 = list(set(Step['Level']) & set(Step['Target']) & set(Step['Goal']) & set(Step['Engagement']) & set(Step['Age']))
		Potential_Names = [Names[i] for i in Combo1]
		if not values[99] == '':
			Combo = []
			for i in Combo1:
				if values[99] in Names[i]:
					Combo.append(i)
		else:
			Combo = Combo1
		print(Combo)
		window[10].update([Names[i] for i in Combo])	#Update all the listboxes to only show the indexes that have the correct values.
		window[11].update([Level[i] for i in Combo])
		window[12].update([Target[i] for i in Combo])
		window[13].update([Goal[i] for i in Combo])
		window[14].update([Engagement[i] for i in Combo])
		window[15].update([Age[i] for i in Combo])
		window[16].update([Description[i] for i in Combo])
	if events in [21]:
		if values[21] == 'ALL':
			window[31].update(visible=False)
		else:
			window[31].update(visible=True)																			#If the CBox is selected, make visible another to allow for two selections.
	if events in [22]:
		if values[22] == 'ALL':
			window[32].update(visible=False)
		else:
			window[32].update(visible=True)
	if events in [23]:
		if values[23] == 'ALL':
			window[33].update(visible=False)
		else:
			window[33].update(visible=True)
	if events in [24]:
		if values[24] == 'ALL':
			window[34].update(visible=False)
		else:
			window[34].update(visible=True)
	if events in [25]:
		if values[25] == 'ALL':
			window[35].update(visible=False)
		else:
			window[35].update(visible=True)
	if events in (None, 'Import'):
		Info = Import_Files()
		Info2 = Sort_Data(Info, Reference)
		Write_Directory(Info2)
		Index, Names, Level, Target, Goal, Engagement, Age, Description, Note = Reading()
		window[10].update(Names)	#Update all the listboxes to only show the indexes that have the correct values.
		window[11].update(Level)
		window[12].update(Target)
		window[13].update(Goal)
		window[14].update(Engagement)
		window[15].update(Age)
		window[16].update(Description)
	if events in (None, 'Read'):
		Index, Names, Level, Target, Goal, Engagement, Age, Description, Note = Reading()
		print(Names)
		window[10].update(Names)	#Update all the listboxes to only show the indexes that have the correct values.
		window[11].update(Level)
		window[12].update(Target)
		window[13].update(Goal)
		window[14].update(Engagement)
		window[15].update(Age)
		window[16].update(Description)
	if events in (None, 'SP Import'):
		con_Mey = ''
		attempts = 0
		while con_Mey == '':
			try:
				Username = sg.popup_get_text('Please enter your EF email.', title='Sharepoint Login')
				Password = sg.popup_get_text('Please enter your EF password.', title='Sharepoint Login', password_char= '*')
				s = Sharepoint_Login(Username, Password)
				con_Mey = s.cookie
			except Exception as e:
				sg.popup('Sorry. Details have been entered incorrectly. Try again')
				print(e)
				attempts = attempts+1
				if attempts >= 3:
					break
		if not attempts >=3:
			Sharepoint_Import(s)
			Info = Import_Files()
			Info2 = Sort_Data(Info, Reference)
			Write_Directory(Info2)
			Index, Names, Level, Target, Goal, Engagement, Age, Description, Note = Reading()
			window[10].update(Names)	#Update all the listboxes to only show the indexes that have the correct values.
			window[11].update(Level)
			window[12].update(Target)
			window[13].update(Goal)
			window[14].update(Engagement)
			window[15].update(Age)
			window[16].update(Description)
window.Close()