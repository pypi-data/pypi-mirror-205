import os
import sys,time

def write(str):
	for i in str:
		sys.stdout.write(i)
		sys.stdout.flush()

		time.sleep(3/90)