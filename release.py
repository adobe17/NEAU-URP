#! py -3.5
#-*- coding:utf-8 -*-

from random import sample
from requests import get, post, session, exceptions
from re import compile

kbname = './选课结果.html'
yzmname = './yzm.jpg'
cjbname = './成绩总表.html'


def setCookie(ori_cookie):
	cookie_tmp = session()
	for key, value in ori_cookie.items():
		cookie_tmp.cookies.set(key, value)
	return cookie_tmp.cookies


proxy = {
	"http": "http://127.0.0.1:8080"
}
url_port = ['',
            'http://jws1.vpn.neau.edu.cn/',
            'http://jws2.vpn.neau.edu.cn/',
            'http://jws3.vpn.neau.edu.cn/',
            'http://jws4.vpn.neau.edu.cn/',
            'http://jwt1.vpn.neau.edu.cn/',
            'http://jwt2.vpn.neau.edu.cn/',
            'http://jwt3.vpn.neau.edu.cn/'
            ]
header = {
	'Accept': 'image/gif, image/jpeg, image/pjpeg, application/x-ms-application, application/xaml+xml, application/x-ms-xbap, */*',
	'Accept-Language': 'zh-Hans-CN,zh-Hans;q=0.8,en-US;q=0.5,en;q=0.3',
	'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729)',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Accept-Encoding': 'gzip, deflate'
}
login_params = {
	"zjh1": "",
	"tips": "",
	"lx": "",
	"evalue": "",
	"eflag": "",
	"fs": "",
	"dzslh": "",
	"zjh": "",
	"mm": "",
	"v_yzm": ""
}
xkcx_params = {
	'kch': '',		# 课程号
	'cxkxh': '',	# 课序号
	'kcm': '',		# 课程名
	'skjs': '',		# 上课教师
	'kkxsjc': '',	# 开课系
	'skxq': '',		# 上课星期
	'skjc': '',		# 上课节次
	'pageNumber': '-2',
	'preActionType': '2',
	'actionType': '5'
}
xkqr_params = {
	'kcId': '',
	'preActionType': '5',
	'actionType': '9'
}
vpn_params = {
	'auth_type': 'local',
	'username': '',
	'sms_code': '',
	'password': '',
	'captcha': '',
	'needCaptcha': 'false'
	# 'captcha_id': 'pnNauNa3WE6uG07'
}

vpn_url = 'http://vpn.neau.edu.cn/do-login/'
lg_in = 'loginAction.do'
lg_out = 'logout.do'
xk = 'xkAction.do'
tk = 'xkAction.do?actionType=10&kcId='
kb = 'xkAction.do?actionType=6'
yzm = 'validateCodeAction.do'


def randomSession(x):
	return ''.join(sample('1234567890zyxwvutsrqponmlkjihgfedcbaABCDEFGHIGKLMOPQRSTUVWXYZ', x))


def filewrite(fname, content):
	with open(fname, 'w') as f:
		f.write(content)


def POST(url, cookie, debug, data={}):
	if(debug == 1):
		return post(url, headers=header, data=data, cookies=cookie, timeout=(2, 4), proxies=proxy)
	else:
		return post(url, headers=header, data=data, cookies=cookie, timeout=(2, 4))


def GET(url, cookie, debug, data={}):
	if(debug == 1):
		return get(url, headers=header, data=data, cookies=cookie, timeout=(2, 4), proxies=proxy)
	else:
		return get(url, headers=header, data=data, cookies=cookie, timeout=(2, 4))


def port1():
	choice = input(
		'选择端口：\n1.jws1学生入口1\n2.jws2学生入口2\n3.jws3学生入口3\n4.jws4学生入口4\n\n5.jwt1教师入口1\n6.jwt2教师入口2\n7.jwt3教师入口3\n请输入序号：')
	return url_port[int(choice)]


def port2(choice):
	return url_port[int(choice)]


def kyl(cont):
	pattern = compile(r'(<td.*>.*\n\t\t[0-9]*</td>)')
	result = pattern.findall(cont)
	# print(result)
	i = 0
	while i < len(result):
		print('  课序号：', end='')
		print(((compile(r'<td.*>.*\n\t\t([0-9]*)</td>')).findall(result[i]))[0])
		print('  课余量：', end='')
		print(((compile(r'<td.*>.*\n\t\t([0-9]*)</td>')).findall(result[i+1]))[0])
		i += 2


def xkjg(cont):
	pattern = compile(r'<strong><font color="#990000">(.*)</font></strong>')
	result = pattern.findall(cont)
	# print(result)
	if(result):
		return '  选/退课结果：' + result[0]
	else:
		return '  请检查代码是否出错！'


def valid(debug=0):
	try:
		response = GET(url_selected + kb, cookie, debug)
		print('   课表核对结果：', end='')
		print(bool((response.text.find(kcId)) > 0))
		# with open(kbname, 'w') as f:
		# 	f.write(response.text)
		# f.write(response.text.replace('charset=GBK', 'charset=utf-8'))
	except exceptions.Timeout:
		print('\n     【课表】请求超时！请重试或更换端口！\n')


def xk_do(debug=0):
	try:
		response = POST(url_selected + xk, cookie, debug, xkcx_params)
		print(response.status_code)
		if(response.status_code == 200):
			# with open('./xk.html', 'w') as f:
			# 	f.write(response.text)
			if int(len(response.text)) > 2600:
				if '<h1>500' not in response.text:
					kyl(response.text)
					try:
						response = POST(url_selected + xk, cookie, debug, xkqr_params)
						print(response.status_code)
						if(response.status_code == 200):
							# with open('./xkjg.html', 'w') as f:
							# 	f.write(response.text)
							if '<h1>500' not in response.text:
								print(xkjg(response.text))
							else:
								print('  500 Servlet Exception')
							print('  选课已执行！')
						else:
							print('\nxkAction.do连接失败！\n')
					except exceptions.Timeout:
						print('\n     【选课确认】请求超时！请重试或更换端口！\n')
				else:
					print('  500 Servlet Exception')
			valid(debug)
	except exceptions.Timeout:
		print('\n     【选课】请求超时！请重试或更换端口！\n')


def tk_do(debug=0):
	try:
		response = GET(url_selected + tk + kcId, cookie, debug)
		print(response.status_code)
		if (response.status_code == 200):
			print('\n  退课已执行！')
			print(xkjg(response.text))
			valid()
		else:
			print('\n  连接失败！')
	except exceptions.Timeout:
		print('\n     【退课】请求超时！请重试或更换端口！\n')


def kb_do(debug=0):
	try:
		response = GET(url_selected + kb, cookie, debug)
		with open(kbname, 'w') as f:
			f.write(response.text)
		print('\n  课表已生成！\n')
	except exceptions.Timeout:
		print('\n     【课表】请求超时！请重试或更换端口！\n')


def cj_do(debug=0):
	try:
		response = GET(url_selected + cj, cookie, debug)
		with open(cjbname, 'w') as f:
			f.write(response.text)
		print('\n  成绩总表已生成！\n')
	except exceptions.Timeout:
		print('\n     【成绩总表】请求超时！请重试或更换端口！\n')


def login(cookie, debug=0):
	try:
		response = GET(url_selected + yzm, cookie, debug)
		with open(yzmname, 'wb') as f:
			f.write(response.content)

		jwc_password = input('请输入教务处密码：')

		login_params['zjh'] = jwc_username
		login_params['mm'] = jwc_password

		login_params['v_yzm'] = input("请打开yzm.jpg查看并输入验证码：")
		try:
			response = POST(url_selected + lg_in, cookie, debug, login_params)
			# print(len(response.text))  8289  484
			# success:content-lenth = 491  fail:~~content-lenth~~
			if len(response.text) > 1000:
				print('\n登录失败！请检查账号密码或验证码是否输入错误！')
				return 0
			else:
				print('\n登录成功！开始执行！\n')
				return 1
		except exceptions.Timeout:
			print('\n    【教务处登录】 请求超时！请重试或更换端口！\n')
	except exceptions.Timeout:
		print('\n    【验证码】 请求超时！请重试或更换端口！\n')


def logout(cookie, debug=0):
	try:
		response = GET(url_selected + lg_out, cookie, debug)
		if(response.status_code == 200):
			print('\n已经登出当前账号！\n')
	except exceptions.Timeout:
		print('\n    【教务处登出】 请求超时！请重试或更换端口！\n')


def vpn(debug=0):
	global cookie
	vpn_params['username'] = input('请输入VPN账号：')
	vpn_params['password'] = input('请输入VPN密码：')
	try:
		response = POST(vpn_url, cookie, debug,  vpn_params)
		# print(response.headers['Set-Cookie'])
		if response.headers['Content-Length'] != '35':
			print('\nVPN登录失败！请检查账号密码或验证码是否输入错误！')
			return 0
		else:
			pattern = compile(r'cn=(.*); P')
			result = pattern.findall(response.headers['Set-Cookie'])
			cookie = setCookie({"wengine_vpn_ticketvpn_neau_edu_cn": result[0]})
			# print(cookie.items())
			print('\n\nVPN登录成功！')
			return 1
	except exceptions.Timeout:
		print('\n    【VPN登录】 请求超时！请重试或更换端口！\n')


if __name__ == '__main__':

	debug_mod = int(input("127.0.0.1:8080代理模式(0/1)【不清楚有什么用的请选0】："))
	# debug_mod = 1
	vpncookie = {"wengine_vpn_ticketvpn_neau_edu_cn": randomSession(25)}
	cookie = setCookie(vpncookie)
	vpncl = -1
	vpn_tries = 0
	jwc_tries = 0

	while(vpncl):
		if(vpn_tries >= 3):
			print('\n警告：VPN已连续 3 次尝试失败，为防止账户被封锁（连续五次登陆失败），脚本即将退出！\n为防止账户被锁，请仔细核对密码后重新登录！\n')
			break
		vpn_tries += 1

		if vpn(debug_mod) == 1:
			tmp = setCookie({"JSESSIONID": randomSession(16)})
			cookie.update(tmp)
			vpn_tries = 0

			print('\n当前账户cookie：', cookie.items(), end='\n\n')
			url_selected = port2(7)

			while vpncl:
				if vpncl == -1:
					url_selected = port1()
					vpncl = 1
				if(jwc_tries >= 5):
					print('\n教务处账号已连续 5 次尝试错误，请仔细核对后重新尝试！\n')
					break

				jwc_username = input('请输入教务处账号：')

				if(login(cookie, debug_mod)):
					jwc_tries = 0
					choose = 1
					while(choose):
						print('===================================')
						choose = int(
							input('1、选课  2、退课  3、查课表  4、成绩总表(暂未完善)\n0、退出当前教务系统账号（退出后可更换端口）\n\n请输入选项：'))
						if choose == 1 or choose == 2:

							kcId = input("请输入课程号：")
							
							if choose == 1:
								lkId = '_'
								kxId = input("请输入课序号：")
								xkcx_params['kch'] = kcId
								xkcx_params['cxkxh'] = kxId
								xkqr_params["kcId"] = kcId + lkId + kxId
								xk_do(debug_mod)
							else:
								tk_do(debug_mod)
						elif choose == 3:
							kb_do(debug_mod)
						elif choose == 4:
							cj_do(debug_mod)

						print(' \n执行完毕！请登录教务处核对课表！')
						print('***********************************')
					logout(cookie, debug_mod)
					print('-----------------------------------')
				vpncl = int(input(
					'当前账号%s已登出/停止尝试，是否继续处理其他账号？\n(0 退出/ 1 处理其他账号/ -1 更换端口)\n' % (jwc_username)))
	print('选课脚本已退出！感谢您的支持与使用！\n')
	print('如有任何修改建议或bug反馈请发送至：a17github@126.com 或 https://github.com/adobe17/NEAU-URP 的issue处提出')
