import qrcode
import os
import random
import pdfkit

# 测试
# CWD = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
# TEMP_URL = os.path.join(CWD, 'collected_static', 'smallparts', 'temp')
# REPORT = os.path.join(CWD, 'collected_static', 'smallparts', 'reports')
# PATH_WK = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
# ADM_GROUPS = ['foreman']


# 正式
CWD = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
TEMP_URL = os.path.join(CWD, 'static', 'smallparts', 'temp')
REPORT = os.path.join(CWD, 'static', 'smallparts', 'reports')
PATH_WK = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
ADM_GROUPS = ['报工平台-主管', '报工平台-班组长']


def parse_str(group_id):
	config_str = SheetConfig.objects.get(group_id = group_id)
	config_string = config_str.config_string.replace('\n','').replace('\r','').replace(' ','')
	config_list = config_string.split('$')[1:]
	result = {}
	item_list =[]
	for config_unit in config_list:
		config_unit_list = config_unit.split('|')
		result[config_unit_list[0].replace('.','_')] = config_unit_list[1:3]
		item_list.append(config_unit_list[0])
	return result

class Additional(object):
	def make_code_easy(self, text):
	    image = qrcode.make(text)
	    ss = ''.join(random.sample(list('abcdefgklmnopqrstuvwxyz1234567890'), 10))
	    link = os.path.join(TEMP_URL, '%s.png' % ss)
	    image.save(link)
	    return '%s.png' % ss

	def make_code(self, text):
		qr = qrcode.QRCode(     
		    version=1,     
		    error_correction=qrcode.constants.ERROR_CORRECT_L,     
		    box_size=10,     
		    border=1, 
		) 
		qr.add_data(text) 
		ss = ''.join(random.sample(list('abcdefgklmnopqrstuvwxyz1234567890'), 10))
		link = os.path.join(TEMP_URL, '%s.png' % ss)
		qr.make(fit=True)  
		img = qr.make_image()
		img.save(link)
		return '%s.png' % ss

	def export_pdf(self, host, serial_no):
		path_wk = PATH_WK
		link = os.path.join(REPORT, '%s.pdf' % serial_no)
		config = pdfkit.configuration(wkhtmltopdf=path_wk)
		url = 'http://'+host+'/smallpart/template/'+serial_no+'/'
		pdfkit.from_url(url, link, configuration=config)
		return link


