import mysql.connector
from util import configcls
from constants import CONFIGSTR, DATATABLE, DATAFIELDS
import datetime

class MySQLDB:
	_instance = None
	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super(MySQLDB, cls).__new__(cls, *args, **kwargs)
			cls._instance._connection = None
		return cls._instance
	
	def __init__(self):
		cfg = configcls()
		self.host = cfg.get(CONFIGSTR.MYSQL_HOST.value)
		self.database = cfg.get(CONFIGSTR.MYSQL_DB.value)
		self.user = cfg.get(CONFIGSTR.MYSQL_USER.value)
		self.password = cfg.get(CONFIGSTR.MYSQL_PASS.value)

	def connect(self):
		if not self._connection:
			self._connection = mysql.connector.connect(
				host=self.host,
				database=self.database,
				user=self.user,
				password=self.password
			)
			print("Connected to MySQL database")

	def execute_query(self, query):
		if not self._connection:
			self.connect()
		cursor = self._connection.cursor()
		cursor.execute(query)
		result = cursor.fetchall()
		cursor.close()
		return result
	
	def execute_query_safe(self, query, input):
		if not self._connection:
			self.connect()
		cursor = self._connection.cursor()
		cursor.execute(query, (input, ))
		result = cursor.fetchall()
		cursor.close()
		return result
	
	def get_table(self, tablename):
		q = f"SELECT * FROM {tablename}"
		return self.execute_query(q)

	def get_all_class(self):
		q = f"SELECT DISTINCT {DATAFIELDS.LOP.value} FROM {DATATABLE.THIDUA.value}"
		return self.execute_query(q)
	
	def get_top_x_vipham(self, topx = 10):
		q = f"SELECT lop, ten_hs, ten_nq, diem_tru, diem_cong, tuan, ngay FROM {DATATABLE.THIDUA.value}, {DATATABLE.NOIQUY.value} WHERE {DATATABLE.THIDUA.value}.{DATAFIELDS.MANQ.value} = {DATATABLE.NOIQUY.value}.{DATAFIELDS.MANQ.value}  ORDER BY {DATAFIELDS.NGAY.value} DESC LIMIT 0, {topx}"
		return self.execute_query(q)

	def get_yearly_stats(self):
		current_date = datetime.datetime.now()
		first_day_of_year = datetime.datetime(current_date.year, 1, 1)
		last_day_of_year = datetime.datetime(current_date.year, 12, 31)
		sql_first_date = str(first_day_of_year.year).zfill(2) + "." + str(first_day_of_year.month).zfill(2) + "." + str(first_day_of_year.day).zfill(2)
		sql_last_date = str(last_day_of_year.year).zfill(2) + "." + str(last_day_of_year.month).zfill(2) + "." + str(last_day_of_year.day).zfill(2)
		q = f'''
			SELECT {DATATABLE.NOIQUY.value}.{DATAFIELDS.MANQ.value}, {DATAFIELDS.TENNQ.value}, count({DATAFIELDS.TENNQ.value}) 
			FROM {DATATABLE.NOIQUY.value} 
			INNER JOIN {DATATABLE.THIDUA.value} 
			ON {DATATABLE.THIDUA.value}.{DATAFIELDS.MANQ.value} = {DATATABLE.NOIQUY.value}.{DATAFIELDS.MANQ.value}
			WHERE {DATAFIELDS.NGAY.value} >= '{sql_first_date}' AND {DATAFIELDS.NGAY.value} <= '{sql_last_date}'
			GROUP BY {DATATABLE.THIDUA.value}.{DATAFIELDS.MANQ.value}
		'''
		return self.execute_query(q)
	
	def get_weekly_detail(self, weeknum, lop):
		try:
			weeknum = int(weeknum)
			q = f'''
				SELECT {DATAFIELDS.TENHS.value}, {DATAFIELDS.TENNQ.value}, {DATAFIELDS.NGAY.value}, {DATAFIELDS.LOP.value}
				FROM {DATATABLE.THIDUA.value}
				INNER JOIN {DATATABLE.NOIQUY.value}
				ON {DATATABLE.NOIQUY.value}.{DATAFIELDS.MANQ.value}  = {DATATABLE.THIDUA.value}.{DATAFIELDS.MANQ.value}
				WHERE {DATAFIELDS.TUAN.value} = {weeknum} AND {DATATABLE.NOIQUY.value}.{DATAFIELDS.MANQ.value} <> 'null'
			'''
			if lop != "":
				q = q + f" AND {DATAFIELDS.LOP.value} = %s"
				return self.execute_query_safe(q, lop)
			else:
				return self.execute_query(q)
		except Exception as e:
			print(e)
			return None
		
	def get_hs_vipham_trong_tuan(self, weeknum, lop):
		try:
			weeknum = int(weeknum)
			q = f'''
				SELECT {DATAFIELDS.TENHS.value}, count({DATAFIELDS.MANQ.value}) as SOLANVIPHAM, {DATAFIELDS.LOP.value}
				FROM {DATATABLE.THIDUA.value}
				WHERE {DATAFIELDS.TUAN.value} = {weeknum} AND {DATAFIELDS.LOP.value} = %s AND {DATAFIELDS.MANQ.value} <> 'null'
				GROUP BY {DATAFIELDS.TENHS.value}
			'''
		
			return self.execute_query_safe(q, lop)
		except Exception as e:
			print(e)
			return None
	
	def get_weekly_stats(self, weeknum):
		try:
			# Sanitize input
			weeknum = int(weeknum)
			q = f'''
			SELECT {DATAFIELDS.TUAN.value}, {DATAFIELDS.LOP.value}, SUM({DATAFIELDS.DIEMTRU.value}), SUM({DATAFIELDS.DIEMCONG.value}), SUM({DATAFIELDS.DIEMTRU.value}) - SUM({DATAFIELDS.DIEMCONG.value}) AS TONG_DIEM
			FROM {DATATABLE.NOIQUY.value} 
			INNER JOIN {DATATABLE.THIDUA.value}
			ON {DATATABLE.THIDUA.value}.{DATAFIELDS.MANQ.value} = {DATATABLE.NOIQUY.value}.{DATAFIELDS.MANQ.value}
			WHERE {DATAFIELDS.TUAN.value} = {weeknum}  AND {DATATABLE.THIDUA.value}.{DATAFIELDS.MANQ.value} <> 'null'
			GROUP BY {DATATABLE.THIDUA.value}.{DATAFIELDS.LOP.value} 
			ORDER BY TONG_DIEM
		'''
			print(q)
			return self.execute_query(q)
		except Exception as e:
			print(e)
			return None
		

if __name__ == "__main__":
	db = MySQLDB()
	d = "26 or '1=1'"
	rows = db.get_hs_vipham_trong_tuan(23, "11c2")
	print(rows)