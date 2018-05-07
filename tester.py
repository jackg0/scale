import mass_finder as mf
import time

mf.setup()

print(mf.get_mass())

nCaps = 0

tStart = time.time()

while(True):
	print(mf.get_mass())
	time.sleep(.01)


#while(nCaps < 1000):
#	mf.get_mass()
#	nCaps += 1

#print(time.time() - tStart)
