from enum import Enum

class elev_button_type_t(Enum):
	_order_ = 'BUTTON_CALL_UP BUTTON_CALL_DOWN BUTTON_COMMAND'
	BUTTON_CALL_UP = 0
	BUTTON_CALL_DOWN = 1
	BUTTON_COMMAND = 2 

