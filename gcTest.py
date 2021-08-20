from godelchords import *

print("hi")

U2 = ("", decodeSong( \
	# standard:
	"00" \
	# key of D:
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
	# I, V, vi, IV:
	+ "0010110001"
	# 3rd progression, 24 1-bar loops:
	# 4 bit binary times four:
	+ "0001" \
	# 24 loops:
	+ "0110" \
	# 1 bar:
	+ "01"
	# I:
	+ "00"
	# 4th progression, 7 4-bar loops:
	+ "111101" \
	# 4 bars:
	+ "1100"
	# I, V, vi, IV:
	+ "0010110001"
))
# print(decodeMusicNumber("16: " + "1110"))

# print(decodeMusicNumber("16: " + "00010010"))
print(U2)
