
def test():
	print("start write")
	# with open('abc.txt','a+') as f:
	# 	f.write("haha")
	f = open("abc.txt", "a+")
	f.write("\r\nHellow World")
	a = open("abc.txt","r")
	a.read()
	print("end write")

def test1():
	print("haah")

def my_scheduled_job():
	pass
