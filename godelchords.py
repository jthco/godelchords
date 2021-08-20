

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
Return the nybble and the stream
"""
def getNybble(inStream):
	while inStream[0] != "0" and inStream[0] != "1":
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
	print("COMMACHORDS:", chords)
	chordC = ["C", "Dm", "Em", "F", "G", "Am", "Bm"]
	print(chordC)
	print(chords)
	print(chordC[3])
	ret = ""
	print(len(chords))
	print("----------")
	for c in range(len(chords)):
		#print(c)
		char = chords[c]
		#print(char)
		if char >= "0" and char <= "9":
			c = ord(char) - ord("1")
			ret += chordC[c]

		#	ret += "[" + chordC[c-"1"] + "]"
		#else:
		#	ret += char
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
	print("   size is: ", len(stream))
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
	return commaChords(chords, key), stream


def namedChords(key, chords, stream):
	print(chords)
	return chords, stream

#
# FUNCTION DEFINES
#

fPlain = "00"
fsLoop = "0100" # XX - number
fsStandard_ = "0101"  # not used
fssVc = "010100" # verse, chorus
fssVvc = "010101" # verse, verse, chorus

# 10 : fLength
flHalf = "1000"
fl2 = "1001"
fl4 = "1010"
flQuarter = "101100"
fl8 = "101101"
# 11 - future switches / options / modes
	# 00 - ?
	# 01 - ?
	# 10 - ?
		 # 1100 - ?


#
# KEY DEFINES
#

kC = "00"
kG = "01"
kD = "10"
kA = "1100"

#
# important number defines until a function is written
#
n1 = "01"
n2 = "10"
n4 = "1100"
n8 = "1101"
n16 = "1110"
n3 = "111100"
n7 = "111101"

#
# number encoding special defines
#

ns0			= "0000"		# 0
ns4x4b		= "0001"		# 4-bit number multiplied by 4
ns8b		= "0010"		# 8 bit number
ns16b		= "001100"		# 16 bit number
nsd3		= "001101"		# decimal number with 3 decimal points: integer followed by 10 bits (1000 to 1023 are reserved)
nsd6		= "001110"		# decimal number with 6 decimal points: integer followed by 20 bits (1000000 to 1048576 are reserved)
nsf			= "001111"		# fraction: numerator followed by denominator

ns0			= "[ns0 0000]"		# 0
ns4x4b		= "[ns4x4b 0001]"		# 4-bit number multiplied by 4
ns8b		= "[ns8b 0010]"		# 8 bit number
ns16b		= "[nsl6b 001100]"		# 16 bit number
nsd3		= "[nsd3 001101]"		# decimal number with 3 decimal points: integer followed by 10 bits (1000 to 1023 are reserved)
nsd6		= "[nsd6 001110]"		# decimal number with 6 decimal points: integer followed by 20 bits (1000000 to 1048576 are reserved)
nsf			= "[nsf 001111]"		# fraction: numerator followed by denominator

#
# Number encoders
#

# integer to terminating base 3 encoding
#    for non-zero numbers
def intToTBase3(num):
	ret = ""
	while True:
		if num >= 3:
			ret += "11"
			num -= 3
		if num == 2:
			ret += "10"
			return "<" + ret + ">"
		if num == 1:
			ret += "01"
			return "<" + ret + ">"
		if num == 0:
			ret += "00"
			return "<" + ret + ">"

# integer to 4 bit times 4 encoding
def intTo4x4b(num):
	assert (num & 3 == 0 and num <= 60 and num >= 0)
	ret = ns4x4b
	ret += ("000" + bin(num // 4)[2:])[-4:]
	return ret

# integer to 8 bit encoding
def intTo8b(num):
	assert (num <= 255 and num >= 0)
	ret = ns8b
	ret += ("0000000" + bin(num)[2:])[-8:]
	return ret

# integer to 16 bit encoding
def intTo16b(num):
	assert (num <= 65535 and num >= 0)
	ret = ns16b
	ret += ("000000000000000" + bin(num)[2:])[-16:]
	return ret

# number to X.XXX with 3 decimal precision
def numToDec3(num):
	assert(num >= 0 and num < 16)
	whole = int(num)
	frac = round((num - whole) * 1000)
	print(whole, frac)
	ret = nsd3
	ret += gNum(whole)
	ret += ("000000000" + bin(frac)[2:])[-10:]
	return ret

# number to X.XXX with 3 decimal precision
def numToDec6(num):
	assert(num >= 0 and num < 16)
	whole = int(num)
	frac = round((num - whole) * 1000000)
	print(whole, frac)
	ret = nsd6
	ret += gNum(whole)
	ret += ("0000000000000000000" + bin(frac)[2:])[-20:]
	return ret

def numToFraction(numerator, denominator):
	assert(numerator >= 0 and numerator < 16)
	assert(denominator >= 0 and denominator < 16)
	ret = nsf + gNum(numerator) + gNum(denominator)
	return ret

# godel number encoding
def gNum(num):
	if num == 0:
		return ns0
	return intToTBase3(num)

def rNum(gnum):
	pass


def gsBitsToJson(inStream):
	pass


"""
Convert a GodelSong bit stream to a Python list structure
"""

def gsBitsToList(inStream):
	p("-------------------------\ngBitsToList")
	stream = inStream
	print("   size is: ", len(stream))
	specials, stream = getNybble(stream)
	if specials:
		# not yet
		# pull in more data blocks
		pass


	key, stream = getNybble(stream)
	print(f"{function=} {key=}")
	return
	chords = ""
	while len(stream) > 0:
		print("======== LOOPING =========")
		# print("LEN:", len(stream))
		# num, stream = decodeMusicNumber(stream)
		print("LEN:", len(stream))
		newChords, stream = decodeProgressions(stream)
		print("LEN:", len(stream))
		chords += newChords
		p("  -->" + chords)
	return commaChords(chords, key), stream



if __name__ == '__main__':

	print("hey")
	bits = "100000" # simplest
	print(gsBitsToList(bits))
	#print rNum("0000")

	#	for i in range(0, 400, 1):
	#		#print(i, intToTBase3(i))
	#		#print(i, intTo4x4b(i*4))
	#		#print(i, intTo8b(i))
	#		#print(i, intTo16b(i))
	#		#print(i / 100, intToDec3(i / 100))
	#		print(i / 10000, intToDec6(i / 10000))
	#print(intToDec3(3.142))
	#print(intToFraction(5, 7))
	#print(decodeNumber("1111111110"))
	#print(decodeMusicNumber("1110"))
	#print(decodeChords(4, "0001110010"))
	#print(decodeProgression("100001110010"))
	#print(decodeProgressions("10100001110010"))
	#song: 0000
	# progressions
	#print(decodeSong("0000 10100001110010"))  # one verse
	#print(decodeSong("0000 1100   100001110010"))  # one verse
	#print(decodeMusicNumber("16: " + "1110"))

	#print(decodeMusicNumber("16: " + "00010010"))
	#print(namedChords("C", commaChords(U2, 1))

	#	print(decodeMusicNumber("0010111011111111X"))

	#decodeBits(testDecode[0])
	pass

