
from godelchords import *

import os
path = 'C:\\Users\\j\\Documents\\Godel Chords\\McGill-Billboard'


def trimTime(inp):
	pass

def cleanChord(chord):
	#print(chord[-4:])
	if chord[-4:] == ":maj":
		return chord[:-4]
	if chord[-4:] == ":min":
		return chord[:-4] + "m"
	return chord + "!"

songs = 0
for root,d_names,f_names in os.walk(path):
	if len(f_names):
		#if root[-4:] == "0029":
		if True:
			print("--------")
			file = open(root + "\\" + f_names[0], "r")
			title = file.readline()[9:-1]
			artist = file.readline()[10:-1]
			metre = file.readline()[9:-1]
			tonic = file.readline()[9:-1]
	#		print(file.readline())
			print(root[-4:] + ": " + artist.ljust(40) + title.ljust(40) + metre.ljust(10) + tonic)
			n = file.readline()
			#print(n)

			for i in range(10):
				n = file.readline().split()
				#print(n)
				index = 0
				line = ""
				seq = ""
				type = ""
				component = ""
				for elem in n:
					if index == 0: # time
						pass
					elif elem == "|":
						pass
					elif "(" in elem:  # for example "(voice"
						component = "- BEGIN " + elem[1:]
					elif ")" in elem:  # for example "voice)"
						component = "- END " + elem[:-1]
					elif elem.islower():
						type = elem.replace(",", "")
					elif not ":" in elem: # A or B
						seq = elem.replace(",", "")
					else:
						line += cleanChord(elem) + " / "
					index += 1
				outp = ""
				if seq:
					outp += seq + ": "
				if type:
					outp += "[" + type + "] "
				outp = outp.ljust(15)
				outp += line + component

				print(outp)
			songs += 1


print(songs, "songs.")