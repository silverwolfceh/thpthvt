import json
import os
from constants import *


class configcls:
	def __init__(self, cpath = CONFIG_FILE):
		self.conf = None
		self.cpath = cpath
		with open(cpath, "r") as f:
			self.conf = json.loads(f.read())
		
	def __save__(self):
		with open(self.cpath, "w") as f:
			print(json.dumps(self.conf))
			f.write(json.dumps(self.conf, indent=4))

	def get(self, cname, dvalue = ""):
		if self.conf and cname in self.conf:
			return self.conf[cname]
		return dvalue
	
	def set(self, cname, cvalue):
		if self.conf is not None:
			self.conf[cname] = cvalue
			self.__save__()
	
	def refresh(self):
		with open(self.cpath, "r") as f:
			self.conf = json.loads(f.read())
			

def generate_init_config_file(filename = CONFIG_FILE):
	if not os.path.isfile(filename):
		with open(filename, "w") as f:
			f.write("{}")
	cfobj = configcls(filename)
	cfobj.set(CONFIGSTR.MYSQL_DB.value, CONFIGVAL.MYSQL_DB.value)
	cfobj.set(CONFIGSTR.MYSQL_HOST.value, CONFIGVAL.MYSQL_HOST.value)
	cfobj.set(CONFIGSTR.MYSQL_PASS.value, CONFIGVAL.MYSQL_PASS.value)
	cfobj.set(CONFIGSTR.MYSQL_PORT.value, CONFIGVAL.MYSQL_PORT.value)
	cfobj.set(CONFIGSTR.MYSQL_USER.value, CONFIGVAL.MYSQL_USER.value)

if __name__ == "__main__":
	generate_init_config_file()
	