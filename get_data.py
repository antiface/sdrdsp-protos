import sys

from rtlsdr import RtlSdr

class Config:
	matlab_flag = False
	sample_rate = 2.4e5
	center_freq = 100e6
	sample_num = 1024

	def __init__(self):
		pass

config = Config()

#check system arguments
if len(sys.argv) < 2:
	print "Arguments needed"
	print """ ./get_data.py [OPTIONS]
		-m               ... output in matlab compatible format
		-s [SAMPLE_NUM]  ... number of samples
		-c [FREQUENCY]   ... center frequency
		-r [SAMPLE_RATE] ... sample_rate
	"""
	sys.exit(0)

#parse arguments
for i in range(0,len(sys.argv)):
	arg = sys.argv[i]
	if (arg == "-m"):
		config.matlab_flag = True
	elif (arg == "-s"):
		config.sample_num = int(sys.argv[i+1])
	elif (arg == "-c"):
		config.center_freq = int(sys.argv[i+1])
	elif (arg == "-r"):
		config.sample_rate = int(sys.argv[i+1])

#init RTLSDR and if no then go out
try:
	sdr = RtlSdr()
except IOError:
	print "Probably RTLSDR device not attached"
	sys.exit(0)

# configure device
sdr.sample_rate = config.sample_rate  # Hz
sdr.center_freq = config.center_freq     # Hz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'


samples = sdr.read_samples( config.sample_num )
if config.matlab_flag == False:
	print( samples )
else:
	print "samples = [",
	for s in samples:
		if s.imag < 0.0:
			print "%s%si "%(str(s.real), str(s.imag)),
		else:
			print "%s+%s "%(str(s.real), str(s.imag)),
	print "];"
