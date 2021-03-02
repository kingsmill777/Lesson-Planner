import PySimpleGUI as sg
import csv



def LBox(values, key, size):
	return sg.Listbox(values, enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE , size=(size,len(values)), pad=(0,0), no_scrollbar=True, key=key)
def TBox(values, size):
	return sg.Text(values, justification='center', size=(size, 1), pad=(0,0))
def CBox(values, key, seeya):
	return sg.Combo(values, default_value='ALL', readonly=True, size =(12,len(values)), pad=(0,0), key=key, enable_events=True, visible=seeya)

def find(lst, value):
	result = []
	for i, x in enumerate(lst):
		if value in x or x == 'ALL':
			result.append(i)
	return result

def CreateNumbers(value):
	return list(range(0, len(value)))

Index = []
Names = []
Level = []
Target = []
Goal = []
Engagement = []
Age = []
Description = []
Note = []

def Reading():
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


Reading()

Options1 = ['ALL','SS1', 'SS2', 'SS3', 'SS4', 'HFC', 'HFD', 'HFE', 'HFF', 'HFG', 'HFH', 'HFI', 'HFJ', 'TB1', 'TB2', 'TB3', 'TB4', 'TB5', 'TB6']
Options2 = ['ALL', 'Vocabulary', 'Grammar', 'Dialogue', 'Reading','Writing', 'Reset']
Options3 = ['ALL', 'Introduction', 'Practice', 'Test', 'Consolidate', 'Fun']
Options4 = ['ALL', 'Individual', 'Pairs', 'Small Groups', 'Whole Class']
Options5 = ['ALL', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
Step = {21:[], 22:[], 23:[], 24:[], 25:[]}
Sort_Ref = {21:'Level', 22:'Target', 23:'Goal', 24:'Engagement', 25:'Age'}
size_name = 20
size_description = 25
size_default = 15
size_age = 6
#col = [[sg.Text('                      '), CBox(Options1, 21), CBox(Options2, 22), CBox(Options3, 23), CBox(Options4, 24), CBox(Options5, 25), sg.Button('Sort')],
#	   [sg.Text('                      '), CBox(Options1, 31),sg.Text(' '), CBox(Options2, 32), CBox(Options3, 33), CBox(Options4, 34), CBox(Options5, 35)],
#	   [TBox('Name', size_name), TBox('Level', size_default), TBox('Target', size_default),  TBox('Goal', size_default), TBox('Engagement', size_default), TBox('Age', size_default), TBox('Description', size_description)],
#	   [LBox(Names, 10, size_name),LBox(Level, 11, size_default), LBox(Target, 12, size_default), LBox(Goal, 13, size_default), LBox(Engagement, 14, size_default), LBox(Age, 15, size_default), LBox(Description, 16, size_description)],
#	  ]
col1 = [[sg.In(key=99,size=(size_name,1))],[sg.Text(' ')]]#,[TBox('Name', size_default)],[LBox(Names, 10, size_name)]]
col2 = [[CBox(Options1, 21, True)],[CBox(Options1, 31, False)]]#,[TBox('Level', size_default)],[LBox(Level, 11, size_default)]]
col3 = [[CBox(Options2, 22, True)],[CBox(Options2, 32, False)]]#,[TBox('Target', size_default)],[LBox(Target, 12, size_default)]]
col4 = [[CBox(Options3, 23, True)],[CBox(Options3, 33, False)]]#,[TBox('Goal', size_default)],[LBox(Goal, 13, size_default)]]
col5 = [[CBox(Options4, 24, True)],[CBox(Options4, 34, False)]]#,[TBox('Engagement', size_default)],[LBox(Engagement, 14, size_default)]]
col6 = [[CBox(Options5, 25, True)],[CBox(Options5, 35, False)]]#,[TBox('Age', size_default)],[LBox(Age, 15, size_default)]]
col7 = [[sg.Text("-Activity Name-",enable_events=True, size=(50,1), pad=(0,1), key=41,background_color=('white'), text_color=('black'))],[sg.Multiline("-Description-",enable_events=True, size=(50,4), pad=(0,1), key=42,background_color=('white'), text_color=('black'))],[sg.Multiline("-Notes-",enable_events=True, size=(50,4), pad=(0,1), key=43,background_color=('white'), text_color=('black'))]]

layout = [[sg.Column(col1), sg.Column(col2), sg.Column(col3), sg.Column(col4), sg.Column(col5), sg.Column(col6), sg.Button('Sort'),sg.Column(col7)],
			[TBox('Name', size_name), TBox('Level', size_default), TBox('Target', size_default),  TBox('Goal', size_default), TBox('Engagement', size_default), TBox('Age', size_default), TBox('Description', size_description)],
			[LBox(Names, 10, size_name),LBox(Level, 11, size_default), LBox(Target, 12, size_default), LBox(Goal, 13, size_default), LBox(Engagement, 14, size_default), LBox(Age, 15, size_default), LBox(Description, 16, size_description)],
			[sg.Button('Do Something'), sg.Button('Exit')]]


window = sg.Window('Activity Finder', layout)

while True:
	events, values = window.read()
	print(events)
	if events in (None, 'Exit'):
		break
	if events in (10,11,12,13,14,15,16):
		indexes = window[events].GetIndexes()
		window[41].Update(Names[indexes[0]])
		window[42].Update(Description[indexes[0]])
		window[43].Update(Note[indexes[0]])
		for key in (10,11,12,13,14,15,16):
			window[key].Update(set_to_index=indexes)
	if events in (None, 'Sort'):
		Every = CreateNumbers(Index)
		for key in (21, 22, 23, 24, 25):
			if key == 21:
				if values[key] == 'ALL':
					Step[key] = Every
				else:
					Step[key] = find(Level, values[key])
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
		Combo = set(Step[21]) & set(Step[22]) & set(Step[23]) & set(Step[24]) & set(Step[25])
		window[10].update([Names[i] for i in Combo])
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
window.Close()