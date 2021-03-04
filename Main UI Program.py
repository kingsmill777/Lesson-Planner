import PySimpleGUI as sg
import csv
import os
import sys
from Data_Manip import *


def LBox(values, key, size):			#This function defines the Listboxes that will be used to display the different data. Since the only thing that will chang is the key, the parameters will be set within this function.
	return sg.Listbox(values, enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE , size=(size,len(values)), pad=(0,0), no_scrollbar=True, key=key)
def TBox(values, size):				#This function defines the Text boxes above the Listboxes. Since their parameters won't change except the actual Text in them I can define it all here in this function.
	return sg.Text(values, justification='center', size=(size, 1), pad=(0,0))
def CBox(values, key, seeya):			#Combo boxes used for choosing what to sort the data set by. Some boxes will be invisible at the start. But other than that and the values they are the same so into this function they go.
	return sg.Combo(values, default_value='ALL', readonly=True, size =(12,len(values)), pad=(0,0), key=key, enable_events=True, visible=seeya)

def find(lst, value):				#Simple little Find function. I tried it in list syntax and it didn't work. Still I want to get this down to one line at some point.
	result = []
	for i, x in enumerate(lst):
		if value in x or x == 'ALL':
			result.append(i)
	return result

def CreateNumbers(value):			#Creates a numeric list of numbers of a custom size. This is useful for creating indexes of all my data sets.
	return list(range(0, len(value)))

Index = []					#Defining the data that will go in the listboxes. Appending to empty lists is the easiest way to ensure the program works properly.
Names = []
Level = []
Target = []
Goal = []
Engagement = []
Age = []
Description = []
Note = []
The_details = {"file":[], "name":[], "level":[], "target":[], "goal":[], "engagement":[], "age":[], "description":[], "note":[]}

def Reading():					#Reads the directory list. Due to how the directory is created there are some issues with list formatting carrying over. Once I tidy up the other code I might be able to reduce the resources this section uses.
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

	return


Options1 = ['ALL','SS1', 'SS2', 'SS3', 'SS4', 'HFC', 'HFD', 'HFE', 'HFF', 'HFG', 'HFH', 'HFI', 'HFJ', 'TB1', 'TB2', 'TB3', 'TB4', 'TB5', 'TB6']  #Yes, yes, I should have better variable names. Anyway this defines what are appropriate options. I should have this code reference the other file at somepoint so I don't have to change two things if I want to change what is acceptable or not.
Options2 = ['ALL', 'Vocabulary', 'Grammar', 'Dialogue', 'Reading','Writing', 'Reset']
Options3 = ['ALL', 'Introduction', 'Practice', 'Test', 'Consolidate', 'Fun']
Options4 = ['ALL', 'Individual', 'Pairs', 'Small Groups', 'Whole Class']
Options5 = ['ALL', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
Reference = {"level": Options1, "target": Options2, "goal": Options3, "engagement": Options4, "age":Options5}
Step = {21:[], 22:[], 23:[], 24:[], 25:[]} 	# Vital part of the sort function to pre-define this dictionary of empty lists. Again I know I should have better variable names.a
Sort_Ref = {21:'Level', 22:'Target', 23:'Goal', 24:'Engagement', 25:'Age'} #Not used but is actually useful for just remembering what each of the labels mean. Yes, yes, I know I should have better variable names. Shut up.
size_name = 20					#How else am I meant to tinker with over 30 different UI elements.
size_description = 60
size_default = 15
size_age = 6
col1 = [[sg.In(key=99,size=(size_name,1))]]	#Now I know I'm not a smart man or a good programmer but this UI was a real pain in the ass to program. I don't even know why I chose python for this I think this project would have been better in most other languages.
col2 = [[CBox(Options1, 21, True)],[CBox(Options1, 31, False)]]
col3 = [[CBox(Options2, 22, True)],[CBox(Options2, 32, False)]]
col4 = [[CBox(Options3, 23, True)],[CBox(Options3, 33, False)]]
col5 = [[CBox(Options4, 24, True)],[CBox(Options4, 34, False)]]
col6 = [[CBox(Options5, 25, True)],[CBox(Options5, 35, False)]]
col7 = [[sg.Text("-Activity Name-",enable_events=True, size=(50,1), pad=(0,1), key=41,background_color=('white'), text_color=('black'))],[sg.Multiline("-Description-",enable_events=True, size=(50,4), pad=(0,1), key=42,background_color=('white'), text_color=('black'))],[sg.Multiline("-Notes-",enable_events=True, size=(50,4), pad=(0,1), key=43,background_color=('white'), text_color=('black'))]] #3 is that really awkward number where its just easier to do each variable than make a function but if I have to add another multiline for whatever reason I'm going to kick myself.

layout = [[sg.Column(col1), sg.Column(col2), sg.Column(col3), sg.Column(col4), sg.Column(col5), sg.Column(col6), sg.Button('Sort'),sg.Column(col7)], # Beautiful but a real pain to figure out how to use. Creates a bunch of vertically aligned columns. Doing it any other way meant the combo boxes appeared in the wrong place.
			[TBox('Name', size_name), TBox('Level', size_default), TBox('Target', size_default),  TBox('Goal', size_default), TBox('Engagement', size_default), TBox('Age', size_default), TBox('Description', size_description)],
			[LBox(Names, 10, size_name),LBox(Level, 11, size_default), LBox(Target, 12, size_default), LBox(Goal, 13, size_default), LBox(Engagement, 14, size_default), LBox(Age, 15, size_default), LBox(Description, 16, size_description)],
			[sg.Button('Read'), sg.Button('Import'), sg.Button('Exit')]]


window = sg.Window('Activity Finder', layout) 	# What a deceptively and annoying line of code. You'd be forgiven for forgetting that the last 30 lines of code all go smushed into 'layout' and then called.

while True: 					# So this keeps the window alive and kicking. Also means there is a nice constant loop for events to trigger.
	events, values = window.read() 		# Makes the window.
	print(events) 				# Debugging tool that lets me know the key of UI element pressed.
	if events in (None, 'Exit'):		# Standard Exit loop.
		break
	if events in (10,11,12,13,14,15,16): 	# This is what passes for a multi-columned listbox. What a mess. Whenever the index of one box is selected this function makes the other list elements highlight.
		indexes = window[events].GetIndexes()
		window[41].Update(Names[indexes[0]]) # This part updates the info box with useful information.
		window[42].Update(Description[indexes[0]])
		window[43].Update(Note[indexes[0]])
		for key in (10,11,12,13,14,15,16):
			window[key].Update(set_to_index=indexes)
	if events in (None, 'Sort'):		#I knew I went to University for something. Handling data is interesting. especially trying to sort a whole bunch. And Yes, I know this is technically a filter. Fuck off.
		Every = CreateNumbers(Index)	#Makes sure I'll go through every data entry.
		for key in (21, 22, 23, 24, 25):#Need to find what they actually what to filter by. 
			if key == 21:				#This was difficult to think up. If all is picked I don't need to search the results but I need every result to show up. Thanks 'Every'
				if values[key] == 'ALL':
					Step[key] = Every
				else:
					Step[key] = find(Level, values[key]) # If the Combo box has something in it the feature must sort for it.
			elif key == 22:
				if values[key] == 'ALL':
					Step[key] = Every
				else:
					Step[key] = find(Target, values[key])
			elif key == 23:
				if values[key] == 'ALL':
					Step[key] = Every
				else:
					Step[key] = find(Goal, values[key])
			elif key == 24:
				if values[key] == 'ALL':
					Step[key] = Every
				else:
					Step[key] = find(Engagement, values[key])
			elif key == 25:
				if values[key] == 'ALL':
					Step[key] = Every
				else:
					Step[key] = find(Age, values[key])
		Combo = set(Step[21]) & set(Step[22]) & set(Step[23]) & set(Step[24]) & set(Step[25]) # Simple than thought code to find the common indexes.
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
		Reading()
		window[10].update(Names)	#Update all the listboxes to only show the indexes that have the correct values.
		window[11].update(Level)
		window[12].update(Target)
		window[13].update(Goal)
		window[14].update(Engagement)
		window[15].update(Age)
		window[16].update(Description)
	if events in (None, 'Read'):
		Reading()
		window[10].update(Names)	#Update all the listboxes to only show the indexes that have the correct values.
		window[11].update(Level)
		window[12].update(Target)
		window[13].update(Goal)
		window[14].update(Engagement)
		window[15].update(Age)
		window[16].update(Description)
window.Close()
