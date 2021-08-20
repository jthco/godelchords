

testDecode = [
	"00 00 01 11 00 11 10 01 11"
]

def p(s):
	print(s)
def s(s):
	print(s)

"""
Get a bit from the stream
"""
def getBit(inStream):
	stream = inStream
	while stream[0] == " ":
		stream = stream[1:]
	bit = stream[0]
	s("    [" + bit + "]")
	return bit, stream[1:]

"""
Strip spaces and line feeds from the stream
"""
def stripSpaces(inStream):
	return inStream
	while inStream[0] != " ":
		inStream = inStream[1:]
	return inStream


"""
Get a nybble (two bits) from the stream
"""
def getNybble(inStream):
	while inStream[0] == " ":
		inStream = inStream[1:]
	bit1 = inStream[0]
	bit2 = inStream[1]
	s("    [" + bit1 + bit2 + "]")
	return bit1 + bit2, inStream[2:]

"""
Decode a whole message
"""
def decodeBits(inputStream):

	output = ""
	stream = inputStream

	# decode version and functionality
	nybble, stream = getNybble(stream)
	if nybble == "00": # plain
		pass
	elif nybble == "01": # special modes
		pass
	elif nybble == "10": # chord length
		nybble, stream = getNybble(stream)
	elif nybble == "11":
		pass

	bitsRemaining = True
	while bitsRemaining:
		nybble, stream = getNybble(stream)
		print(f"{nybble = }")
		bitsRemaining = len(stream) > 1

"""
Decode a regular number
"""
def decodeNumber(inStream):
	stream = inStream
	accum = 0
	while True:
		nybble,stream = getNybble(stream)
		if nybble == "00": # special
			return accum + 0, stream
		elif nybble == "01":
			return accum + 1, stream
		elif nybble == "10":
			return accum + 2, stream
		elif nybble == "11":
			accum += 3

"""
Decode an 8 bit number
"""
def decode8bitNumber(inStream):
	stream = inStream
	accum = 0
	multiplier = 128;
	for bitCount in range(8):
		bit,stream = getBit(stream)
		if bit == "1":
			accum += multiplier
		multiplier /= 2
	accum = int(accum)
	print("  8BIT: ", accum)
	return accum, stream

"""
Decode a 4 bit number
Number returned is multiplied by 4.
"""
def decode4bitNumber(inStream):
	stream = inStream
	accum = 0
	multiplier = 8;
	for bitCount in range(4):
		bit,stream = getBit(stream)
		if bit == "1":
			accum += multiplier
		multiplier /= 2
	accum = int(accum)
	print("  4BIT: ", accum)
	return 4 * accum, stream

"""
Decode a musical number
"""
def decodeMusicNumber(inStream):
	stream = stripSpaces(inStream)
	print("decodeMusicNumber ", inStream )
	convert = [0,1,2,4,8,16,3,7,15,32,6,14,64,128,256]
	stream = inStream
	#if stream[]
	number, stream = decodeNumber(stream)
	print(f"{number = }")
	if number == 0:		# special
		nextNumber, stream = decodeNumber(stream)
		print(f"{nextNumber = }")
		if nextNumber == 0:
			return 0, stream;		# actual 0
		elif nextNumber == 1:			# 4 bit number times four follows
			print("  4 bit follows")
			return decode4bitNumber(stream)
		elif nextNumber == 2:			# 8 bit number follows
			print("  8 bit follows")
			return decode8bitNumber(stream)

	p("  Music number: " + str(convert[number]))
	return convert[number], stream

"""
Decode a chord
"""
def decodeChord(inStream):
	p("decodeChord")
	stream = inStream
	accum = 0
	while True:
		nybble,stream = getNybble(stream)
		if nybble == "00":
			return 1, stream
		elif nybble == "01":
			return 4, stream
		elif nybble == "10":
			return 5, stream
		elif nybble == "11":
			nybble, stream = getNybble(stream)
			if nybble == "00":
				return 6, stream
			elif nybble == "01":
				return 2, stream
			elif nybble == "10":
				return 3, stream
			elif nybble == "11":
					return 7

"""
Decode a chord sequence
"""
def decodeChords(num, inStream):
	p("decodeChords")
	chords = ""
	stream = inStream
	for index in range(0, num):
		chord, stream = decodeChord(stream)
		chords += str(chord)
	p("  -->" + chords)
	return chords, stream

"""
Decode a note
"""
def decodeNote(inStream):
	p("decodeNote")
	convert = [1,5,2,6,4,0,0,0,0,0,0,0,0]
	number, stream = decodeNumber(inStream)
	return convert[number] - 1, stream

"""
Chord Progression
	Arguments:
		number of chords
		chord 1, chord 2, ... chord N
"""
def decodeProgression(inStream):
	p("decodeProgression")
	num, stream = decodeMusicNumber(inStream)
	print("  playing", num, "chords")
	return decodeChords(num, stream)

"""
Chord Progressions
	Arguments:
		number of loops
		Chord Progression
"""
def decodeProgressions(inStream):
	p("decodeProgressions")
	num, stream = decodeMusicNumber(inStream)
	print("  looping", num, "times")
	chords = ""
	newChords, stream = decodeProgression(stream)
	for loop in range(num):
		chords += newChords
	p("  -->" + chords)
	return chords + " ", stream

def commaChords(chords, key):
	chordC = {"C", "Dm", "Em", "F", "G", "Am", "Bm"}
	ret = ""
	for c in chords:
		ret += "[" + chordC[chords[c]-1] + "]"
		#print("HEY!")
	print ("ret = ", ret)
	return ret


	print(chords)


"""
Song
	Arguments:
		Function
		Key
		Chord Progressions 1, Chord Progressions 2, ....
"""
def decodeSong(inStream):
	p("decodeSong")
	stream = inStream
	function, stream = getNybble(stream)
	key, stream = getNybble(stream)
	chords = ""
	while len(stream) > 0:
		print("======== LOOPING =========")
		#print("LEN:", len(stream))
		#num, stream = decodeMusicNumber(stream)
		print("LEN:", len(stream))
		newChords, stream = decodeProgressions(stream)
		print("LEN:", len(stream))
		chords += newChords
		p("  -->" + chords)
	print ("WTFFFFFF!!!!!!!!!!")
	return commaChords(chords, key), stream


def namedChords(key, chords, stream):
	print(chords)
	return chords, stream



if __name__ == '__main__':
	#print(decodeNumber("1111111110"))
	#print(decodeMusicNumber("1110"))
	#print(decodeChords(4, "0001110010"))
	#print(decodeProgression("100001110010"))
	#print(decodeProgressions("10100001110010"))
	#song: 0000
	# progressions
	#print(decodeSong("0000 10100001110010"))  # one verse
	#print(decodeSong("0000 1100   100001110010"))  # one verse
# with or without you

	U2 = ("THIS!", decodeSong( \
		# standard:
		"00" \
		# key of D
		+ "10" \
		# 1st progression, 8 loops:
		+ "1101" \
		# one bar:
		+ "01" \
		# tonal chord (now in D):
		+ "00" \
		# 2nd progression, 24 4-bar loops:
		# 4 bit binary times four:
		+ "0001" \
		# 24 loops is 6 x 4:
		+ "0110" \
		# 4 bars:
		+ "1100"
		# I, V, vi, IV
		+ "0010110001"
		# 3rd progression, 24 1-bar loops:
		# 4 bit binary times four:
		+ "0001" \
		# 24 loops:
		+ "0110" \
		# 1 bar:
		+ "01"
		# I
		+ "00"
		# 4th progression, 7 4-bar loops:
		+ "111101" \
		# 4 bars:
		+ "1100"
		# I, V, vi, IV
		+ "0010110001"
	))
	#print(decodeMusicNumber("16: " + "1110"))

	#print(decodeMusicNumber("16: " + "00010010"))
	print(U2)
	print(namedChords("C", commaChords(U2, 1))

#	print(decodeMusicNumber("0010111011111111X"))

#decodeBits(testDecode[0])