import channels.py
import ctypes

#Initialize libComedi in "Sanntidssalen"
#@return Non-zero on success and 0 on failure

def io_init(): 
	status = 0

	it_g = comedi_open("/dev/comedi0")
		
	if (it_g == NULL):
		return 0
		
	i = 0	
	for i in range(0,8):
		status |= comedi_dio_config(it_g, PORT1, i, COMEDI_INPUT)
		status |= comedi_dio_config(it_g, PORT2, i, COMEDI_OUTPUT)
		status |= comedi_dio_config(it_g, PORT3, i+8, COMEDI_OUTPUT)
		status |= comedi_dio_config(it_g, PORT4, i+16, COMEDI_INPUT)
		i += 1

	return (status == 0)



#Sets a digital channel bit.
#@param channel Channel bit to set.

def io_set_bit(channel): 				#int channel
	comedi_dio_write(it_g, channel >> 8, channel & 0xff, 1)



#Clears a digital channel bit.
#@param channel Channel bit to set.

def io_clear_bit(channel): 			#int channel
	comedi_dio_write(it_g, channel >> 8, channel & 0xff, 0)



#Writes a value to an analog channel.
#@param channel Channel to write to.
#@param value Value to write.

def io_write_analog(channel, value):			#int channel, int value
	comedi_data_write(it_g, channel >> 8, channel & 0xff, 0, AREF_GROUND, value)



#Reads a bit value from a digital channel.
#@param channel Channel to read from.
#@return Value read.

def io_read_bit(channel):					#int channel
	data = c_uint(0)								#unsigned int data = 0
	comedi_dio_read(it_g, channel >> 8, channel & 0xff, &data)

	return (int)data


#Reads a bit value from an analog channel.
#@param channel Channel to read from.
#@return Value read.

def io_read_analog(channel): 			#int channel
	lsampl_t data = 0
	comedi_data_read(it_g, channel >> 8, channel & 0xff, 0, AREF_GROUND, &data)

	return (int)data
	




