#!/usr/bin/env python

import sys

sampleResp = '/home/local/GS/tstorm/RESP.IU.LCO.60.BHZ'
respPath = sampleResp
sensorKey = 'ZP_M2166_GEN'
getstainfoValue = 'STS1M2166'
legend = [['STS1M2166','ZP_M2166_GEN']]

def readResp():
	fob = open(respPath, 'r')
	contents = fob.read()
	fob.close()
	return contents


def main():
	args = sys.argv[1:]
	print args
	contents = readResp().split('\n')
	for line in contents:
		if 'B053F10-13' in line or 'B053F15-18' in line:
			blockette, index, real, imag, realError, imagError = line.split()
			sqlstatement = "INSERT INTO seed_pz_data (key, rowkey, r_value, r_error, i_value, i_error) VALUES (\'" + 'ZP_M2166_GEN' + "\', \'"
			if   'B053F10-13' == blockette:
				sqlstatement += "Z"
			elif 'B053F15-18' == blockette:
				sqlstatement += "P"
			if '+' == real[0]:
				real = real[1:]
			if '+' == imag[0]:
				imag = imag[1:]
			if '+' == realError[0]:
				realError = realError[1:]
			if '+' == imagError[0]:
				imagError = imagError[1:]
			sqlstatement += index.zfill(3) + "\', " + real + ", " + imag + ", " + realError + ", " + imagError + ") ;"
			print sqlstatement

# def sensorValue(sensorKey):
# 	for item in legend:
# 		key, value = item
# 		if key == sensorKey:
# 			return value

main()