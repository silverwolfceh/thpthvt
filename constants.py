from enum import Enum
import os

SERVER_VERSION = "1.0"
CONFIG_FILE = "config.json"
DEVELOPMENT_ENV = os.environ.get('DEVMODE')
APP_PORT_PRODUCTION = 80

class CONFIGSTR(Enum):
	MYSQL_HOST = "MYSQL_HOST"
	MYSQL_PORT = "MYSQL_PORT"
	MYSQL_USER = "MYSQL_USER"
	MYSQL_PASS = "MYSQL_PASS"
	MYSQL_DB = "MYSQL_DB"

class CONFIGVAL(Enum):
	MYSQL_HOST = "127.0.0.1"
	MYSQL_PORT = "3306"
	MYSQL_USER = "root"
	MYSQL_PASS = "root"
	MYSQL_DB = "quanli_hs"

class DATATABLE(Enum):
	NOIQUY = "noi_quy"
	THIDUA = "quanli_thidua"


class DATAFIELDS(Enum):
	ID = "id"
	LOP = "lop"
	TENHS = "ten_hs"
	MANQ = "ma_nq"
	TUAN = "tuan"
	NGAY = "ngay"
	TENNQ = "ten_nq"
	DIEMTRU = "diem_tru"
	DIEMCONG = "diem_cong"