from .comms import PulseGenerator
from . import transcode
from .transcode import encode_instruction   #Frequently called by end user, and it is tedious to have to call it with ndpulsegen.transcode.encode_instruction
from . import console_read