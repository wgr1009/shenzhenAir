# coding=gbk

'''
�������ƣ� ��⵱ǰIP + ����ͷ + cookie
	�ж�cookie���й���ʱ��, ���ں����  self.AlteonP  self.sign_flight
	�ж�sessionid��sessionid���� ���� ����cookies ���� JSsessionid
	ÿ����һ��  cookie�� PVֵ �� 1
'''
import requests, time, random, json,logging

class ShenZhenAir:
	def __init__(self):

		self.url = 'http://www.shenzhenair.com/szair_B2C/flightSearch.action'

		# ���ڵ�����ʱ���  ���ҷ�����һ�θ��µ���
		self.form_data = {
			'condition.orgCityCode': 'PEK',
			'condition.dstCityCode': 'SZX',
			'condition.hcType': 'DC',
		}
		# referer ��ϢҲ������ʱ��ӣ���Ҫ���� post ���ݲ�����User-Agent�����޸ģ���ΪUser-agent��cookie+IP
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
		# cookieֵ ֵȡ�� PV: ��Ϊÿ��������Ҫ ��1 ����
		self.cookie = '�Լ���cookieֵpv:'

		# referֵ Ҳ��Ҫƴ�ӣ�����ֻȡ���м�һ���� ���ں���Ĳ���������ʱƴ�ӽ�ȥ
		self.refer = 'http://www.shenzhenair.com/szair_B2C/flightsearch.action?orgCityCode=PEK&dstCityCode=SZX&orgDate='


	def getJson(self):
		# print(self.headers)
		n = 1
		p = 18
		n_time = time.localtime()
		base_time = int(time.strftime('%Y%m%d', n_time))
		try:
			while n<=7:
				# ʱ�������
				date = str(base_time)[0:4] + '-' + str(base_time)[4:6] + '-' + str(base_time)[6:]

				dstDate = base_time + 1
				conditiondstDate = str(dstDate)[0:4] + '-' + str(dstDate)[4:6] + '-' + str(dstDate)[6:]
				# ���� ���ݵ� data
				self.form_data['condition.orgDate'] = date
				self.form_data['condition.dstDate'] = conditiondstDate
				# ���� ����ͷ  ��Ϣ
				self.headers['Referer'] = self.refer + date + '&hcType=DC'
				self.headers['Cookie'] = self.cookie + str(p)

				print('���ڻ�ȡ%s����Ϣ' % date)
				# ���������ȡ����
				res = requests.post(self.url, headers=self.headers, data=self.form_data)
				time.sleep(5)
				print(res.request.headers['Cookie'])
				# print(res.cookies)
				# res.encoding = 'utf-8'
				html = json.loads(res.text)
				print('==' * 30)

				# �Ի�ȡ�����ݽ��н���
				self.parseJson(html)

				# ��ֵ����
				n += 1
				p += 1
				base_time += 1
				time.sleep(0.5)
		except json.decoder.JSONDecodeError:
			print('��������')



	def parseJson(self, html):
		'''
		�Ի�ȡ�� Json���ݽ��н���
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

				print('ȥ��: '+orgcitych +'-'+dstcitych + ' '+'����: {}, �������: {}, ���ʱ��: {}, ���ʱ��: {}'.format(flightno, orgdate, orgtime, dsttime))
				classinfolist = i['classInfoList']
				for j in classinfolist:
					class_type = j['classCode']
					class_price = j['classPrice']
					print(class_type + '��' + ': ' + class_price + 'Ԫ')
				print()
			time.sleep(0.5)
		else:
			print('��Ǹ������������λ�򺽰�')

	def main(self):
		self.getJson()

if __name__ == '__main__':
	app = ShenZhenAir()
	app.main()


	'https://pan.baidu.com/s/1n2NubUiUspnCj0CzknnFXg ��ȡ��: hww4'
