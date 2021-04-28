

import streamlit as st
from pyproj import Proj, transform
from zipfile import ZipFile

def MyInput(string, color):
	if color == 'red':
		color = '#f63366'
	elif color == 'green':
		color = '#09ab3b'
	elif clor == 'grey':
		color = ''

	st.markdown('<font color='+color+'>{}</font>'.format(string), unsafe_allow_html=True)



def MengLa_range(latitude, longitude):
	max_lon = 22.4072520341805
	min_lon = 21.15243901732123
	min_lat = 101.07477381339304
	max_lat = 101.85927697308027
	# st.write("I am here!")
	if latitude >= min_lat and latitude <= max_lat:
		if longitude >= min_lon and longitude <= max_lon:
			return True
		else:
			return False
	else:
		return False


def checking_decimal(latitude, longitude):
	'''
	checking the lon and lat when input decimal
	'''
	lat_flag = 0
	lon_flag = 0
	# if not latitude:
	# 	st.write("请输入经度!")

	if not longitude or not latitude: ## Step 1, 判断是否完整输入的经纬度
		MyInput('请输入经度、纬度!！', 'red')
	else:
		try:
			if MengLa_range(float(latitude), float(longitude)): # Step 3, 判断是否在勐腊县范围
				MyInput('数据导入成功', 'green')
			else:
				MyInput('您输入的经纬度不在勐腊县范围，请重新输入！', 'red')
		except ValueError: ## Step 2, 判断是否正确经纬度的形式，小数（浮点数）
			MyInput('格式错误，请输入正确的经度、纬度!！', 'red')

def check_tmp(one, two):
	'''
	check if users entered the number
	'''
	if not one and not two:
		return False
	else:
		return True


def dms_to_dec(d, m, s):
	'''
	convert degree min second to decimal
	'''
	ans = float(d) + (float(m) / 60) + (float(s) / 3600)
	return ans

def checking_dms(latitude_d, latitude_m, latitude_s, longitude_d, longitude_m, longitude_s):
	if check_tmp(latitude_d, latitude_m) and check_tmp(longitude_d, longitude_m):
		if not check_tmp(latitude_s, longitude_s):
			pass
			# MyInput('请输入经度、纬度没有秒!！', 'red')
		try:
			latitude = dms_to_dec(int(latitude_d), int(latitude_m), float(latitude_s))
			longitude = dms_to_dec(int(longitude_d), int(longitude_m), float(longitude_s))

			if MengLa_range(float(latitude), float(longitude)): # Step 3, 判断是否在勐腊县范围
				MyInput('数据导入成功', 'green')
				return latitude, longitude
			else:
				MyInput('您输入的经纬度不在数据库范围内，请重新输入！', 'red')

		except ValueError: ## Step 2, 判断是否正确经纬度的形式，小数（浮点数）
			MyInput('格式错误，请输入正确的经度、纬度!！', 'red')		

	else:
		MyInput('请输入经度、纬度!！', 'red')

def get_indices(x, y):#, ox, oy, pw, ph):
    """
    Gets the row (i) and column (j) indices in an array for a given set of coordinates.
    Based on https://gis.stackexchange.com/a/92015/86131

    :param x:   array of x coordinates (longitude)
    :param y:   array of y coordinates (latitude)
    :param ox:  raster x origin
    :param oy:  raster y origin
    :param pw:  raster pixel width
    :param ph:  raster pixel height
    :return:    row (i) and column (j) indices
    """
    # for Mengla,  ox = 715444.1473863411 oy = 2480706.663435716, pw = 30, ph = 30
    ox = 715444.1473863411
    oy = 2480706.663435716
    pw = 30
    ph = 30

    i = int((oy-y) / ph)
    j = int((x-ox) / pw)

    return i, j

def to_coordinate(latitude, longitude):
	inProj = Proj('epsg:32647')
	outProj = Proj('epsg:4326')
	x, y = transform(outProj, inProj, longitude, latitude)
	# st.write(x,y)

	return get_indices(x, y)

def ToID(x, y, row_number=4676):
	return (y-1)*row_number + x


	# 不适宜 1
	# 中适宜 2
	# 高适宜 3
	# 最适宜 4


def extract_information(file, x, y):
	myzip = ZipFile(file)
	# st.write(myzip)
	# st.write(myzip.namelist()[0])
	for record in myzip.open(myzip.namelist()[0]):
		record = record.strip().decode("utf-8")
		record_id, elev_type, slope_type, aspect_type, result = record.split('\t')
		# st.write(ToID(x, y))
		if ToID(x, y) == int(record_id):
			# st.write(record_id, result)
			if result == "1":
				st.write("不适宜")
			elif result == "2":
				st.write("中适宜")
			elif result == "3":
				st.write("高适宜")			
			elif result == "4":
				st.write("最适宜")

			myzip.close()
			break
		else:
			st.write("数据库没有收录该地区信息")





def GUI():
	# 第一部分，数据导入部分：
	st.header('用户输入数据或文件')

	# 首先把界面呈现出来，用户可以看到需要输入哪一种形式的经纬度
	## 1.1 小数点形式的经纬度
	st.subheader('1. 请输入经纬度')
	st.write('1.1 十进制形式的经纬度')
	col1, col2 = st.beta_columns(2) # 分成两列
	for i in range(1):
		latitude = col1.text_input("经度", '')
		longitude = col2.text_input("纬度", '')


	st.write('') # 空一行

	## 1.2 度分秒形式的经纬度
	st.write('1.2 度分秒形式的经纬度')

	col1_lat, col2_lat, col3_lat, blank, col1_lon, col2_lon, col3_lon= st.beta_columns(7) # 输入分为7列
	latitude_d = col1_lat.text_input("经度", '度')
	latitude_m = col2_lat.text_input("", '分')
	latitude_s = col3_lat.text_input("", '秒')

	longitude_d = col1_lon.text_input("纬度", '度')
	longitude_m = col2_lon.text_input(" ", '分')
	longitude_s = col3_lon.text_input(" ", '秒')


	# 然后确认他们输入了哪一个，是十进制还是度分秒
	st.write('') # 空一行
	st.write('') # 空一行

	if latitude or longitude:
		checking_decimal(latitude, longitude)
	elif check_tmp(latitude_d, latitude_m) and check_tmp(longitude_d, longitude_m):
		if check_tmp(latitude_s, longitude_s):
			MyInput('输入的经度、纬度没有秒!！', 'red')
			try:
				latitude = dms_to_dec(int(latitude_d), int(latitude_m), float(latitude_s))
				longitude = dms_to_dec(int(longitude_d), int(longitude_m), float(longitude_s))

				if MengLa_range(float(latitude), float(longitude)): # Step 3, 判断是否在勐腊县范围
					MyInput('数据导入成功', 'green')
					return latitude, longitude
				else:
					pass
					MyInput('您输入的经纬度不在数据库范围内，请重新输入！', 'red')

			except ValueError: ## Step 2, 判断是否正确经纬度的形式，小数（浮点数）
				pass
				# MyInput('格式错误，请输入正确的经度、纬度!！', 'red')
		else:
			try:
				latitude = dms_to_dec(int(latitude_d), int(latitude_m), float(0))
				longitude = dms_to_dec(int(longitude_d), int(longitude_m), float(0))

				if MengLa_range(float(latitude), float(longitude)): # Step 3, 判断是否在勐腊县范围
					MyInput('数据导入成功', 'green')
					return latitude, longitude
				else:
					pass
					MyInput('您输入的经纬度不在数据库范围内，请重新输入！', 'red')

			except ValueError: ## Step 2, 判断是否正确经纬度的形式，小数（浮点数）
				MyInput('格式错误，请输入正确的经度、纬度!！', 'red')	


	else:
		MyInput('请输入十进制或者度分秒形式的经度、纬度!！', 'red')



	# 第二部分，结果分析和输出

	result = st.button('开始分析!')
	# result_show = 'This land is suitable for planting'

	if result:
	# st.write(result_show)
		st.header('结果：')

		# 第一步讲经纬度转换为raster的对应的横列
		x, y = to_coordinate(latitude, longitude)
		# st.write(x, y)

		# 第二步，将坐标位置关系，去数据库中各种信息
		file = '/app/streamlit-app-mengla/result_simple_table.zip'
		extract_information(file, x, y)

		# 第三步，将找到的信息，进行建模，输出结果


		st.write( # 分析结束
		'''
		***
		'''
		)





if __name__ == '__main__':
	# print("I am here!!")
	GUI()
# 界面设置

