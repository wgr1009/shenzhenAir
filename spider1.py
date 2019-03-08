# coding=gbk

'''
反爬机制： 检测当前IP + 请求头 + cookie
	判断cookie：有过期时间, 过期后更新  self.AlteonP  self.sign_flight
	判断sessionid：sessionid过期 更新 整个cookies 或者 JSsessionid
	每请求一次  cookie中 PV值 加 1
'''
import requests, time, random, json,logging

class ShenZhenAir:
	def __init__(self):

		self.url = 'http://www.shenzhenair.com/szair_B2C/flightSearch.action'

		# 日期的请求时添加  并且方便下一次更新调用
		self.form_data = {
			'condition.orgCityCode': 'PEK',
			'condition.dstCityCode': 'SZX',
			'condition.hcType': 'DC',
		}
		# referer 信息也在请求时添加，需要更新 post 传递参数，User-Agent不能修改，因为User-agent绑定cookie+IP
		self.headers = {
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Accept-Encoding': 'gzip, deflate',
			'Accept-Language': 'zh-CN,zh;q=0.9',
			'Content-Length': '129',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'Host': 'www.shenzhenair.com',
			'Origin': 'http://www.shenzhenair.com',
			'Proxy-Connection': 'keep-alive',
			'X-Requested-With': 'XMLHttpRequest',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
		}
		# cookie值 值取到 PV: 因为每次请求需要 加1 操作
		self.cookie = '自己的cookie值pv:'

		# refer值 也需要拼接，所以只取到中间一部分 日期后面的部分在请求时拼接进去
		self.refer = 'http://www.shenzhenair.com/szair_B2C/flightsearch.action?orgCityCode=PEK&dstCityCode=SZX&orgDate='


	def getJson(self):
		# print(self.headers)
		n = 1
		p = 18
		n_time = time.localtime()
		base_time = int(time.strftime('%Y%m%d', n_time))
		try:
			while n<=7:
				# 时间更新用
				date = str(base_time)[0:4] + '-' + str(base_time)[4:6] + '-' + str(base_time)[6:]

				dstDate = base_time + 1
				conditiondstDate = str(dstDate)[0:4] + '-' + str(dstDate)[4:6] + '-' + str(dstDate)[6:]
				# 更新 传递的 data
				self.form_data['condition.orgDate'] = date
				self.form_data['condition.dstDate'] = conditiondstDate
				# 更新 请求头  信息
				self.headers['Referer'] = self.refer + date + '&hcType=DC'
				self.headers['Cookie'] = self.cookie + str(p)

				print('正在获取%s号信息' % date)
				# 发起请求获取数据
				res = requests.post(self.url, headers=self.headers, data=self.form_data)
				time.sleep(5)
				print(res.request.headers['Cookie'])
				# print(res.cookies)
				# res.encoding = 'utf-8'
				html = json.loads(res.text)
				print('==' * 30)

				# 对获取的数据进行解析
				self.parseJson(html)

				# 数值更新
				n += 1
				p += 1
				base_time += 1
				time.sleep(0.5)
		except json.decoder.JSONDecodeError:
			print('后续处理')



	def parseJson(self, html):
		'''
		对获取的 Json数据进行解析
		:param html:
		:return:
		'''
		if len(html):
			info = html['flightSearchResult']['flightInfoList']
			for i in info:
				flightno = i['flightNo']
				orgdate = i['orgDate']
				orgtime = i['orgTime']
				dsttime = i['dstTime']
				orgcitych = i['orgCityCH']
				dstcitych = i['dstCityCH']

				print('去程: '+orgcitych +'-'+dstcitych + ' '+'机型: {}, 起飞日期: {}, 起飞时间: {}, 落地时间: {}'.format(flightno, orgdate, orgtime, dsttime))
				classinfolist = i['classInfoList']
				for j in classinfolist:
					class_type = j['classCode']
					class_price = j['classPrice']
					print(class_type + '舱' + ': ' + class_price + '元')
				print()
			time.sleep(0.5)
		else:
			print('抱歉，该日期无座位或航班')

	def main(self):
		self.getJson()

if __name__ == '__main__':
	app = ShenZhenAir()
	app.main()


	'https://pan.baidu.com/s/1n2NubUiUspnCj0CzknnFXg 提取码: hww4'
