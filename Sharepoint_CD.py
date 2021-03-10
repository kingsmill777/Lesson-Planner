import sharepy as sp
import json
import os
import sys
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

#Sharepoint_Import('kingsley.baxter@ef.cn', 'Toffee777')