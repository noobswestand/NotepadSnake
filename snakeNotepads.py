import ctypes,subprocess,win32gui,time,win32api,pywintypes
user32 = ctypes.windll.user32

class Snake:
	def __init__(self):
		self.handles=[]
		self.processes=[]

		self.proc=None
		self.proc_handle=None

		self.x=[]
		self.y=[]
		self.xStart=1000
		self.yStart=300
		self.w=100
		self.h=100

		self.pellet_process=None
		self.pellet_handle=None
		self.pellet_x=100
		self.pellet_y=100

	def pellet(self):
		self.pellet_process=subprocess.Popen(['cmd.exe'],creationflags=subprocess.CREATE_NEW_CONSOLE)
		self.proc=self.pellet_process.pid
		time.sleep(.5)
		self.proc_handle=None
		win32gui.EnumWindows(self.enumHandler, None)
		self.pellet_handle=self.proc_handle
		self.show_window(self.proc_handle)

		self.pellet_move()

	def pellet_move(self):
		self.window_move(self.pellet_handle,self.pellet_x,self.pellet_y,self.w,self.h)
	def pellet_close(self):
		self.pellet_process.kill()

	def new(self):

		p=subprocess.Popen(['notepad.exe'])
		self.processes.append(p)
		self.proc=p.pid
		
		time.sleep(0.25)
		self.proc_handle=None
		win32gui.EnumWindows(self.enumHandler, None)
		self.handles.append(self.proc_handle)

		if len(self.x)==0:
			self.x.append(self.xStart)
			self.y.append(self.yStart)
		else:
			self.x.append(self.x[-1]-self.w)
			self.y.append(self.y[-1])

		self.show_window(self.proc_handle)
		self.window_move(self.proc_handle,self.x[-1],self.y[-1],self.w,self.h)


	def enumHandler(self,hwnd, lParam):
		lpdw_process_id = ctypes.c_ulong()
		result = user32.GetWindowThreadProcessId(hwnd, ctypes.byref(lpdw_process_id))
		if lpdw_process_id.value==self.proc and self.proc_handle==None:
			self.proc_handle=hwnd

	def show_window(self,handle):
		user32.ShowWindow(handle, 6)
		user32.ShowWindow(handle, 9)
	def window_move(self,handle,x,y,w,h):
		user32.MoveWindow(handle, x,y,w,h, True)

	def move(self,relx,rely):
		self.x.pop(len(self.x)-1)
		self.y.pop(len(self.y)-1)

		self.x.insert(0,self.x[0]+relx)
		self.y.insert(0,self.y[0]+rely)

		for i,h in enumerate(self.handles):
			self.window_move(h,self.x[i],self.y[i],self.w,self.h)

	def close(self,i):
		self.processes[i].kill()
		
		self.processes.pop(i)
		self.handles.pop(i)




import sys,time

s=Snake()
s.pellet()
for i in range(3):
	s.new()




import keyboard,threading,math,random

left=False
right=False
up=False
down=False
Running=True

def listen(key):
	global left,right,up,down,Running
	while True:
		keyboard.wait(key)
		if key=="left":
			left=True
		elif key=="right":
			right=True
		elif key=="up":
			up=True
		elif key=="down":
			down=True
		elif key=="escape":
			Running=False
			print("close")

#Start the threads
threads=[]
keys=["left","right","up","down","escape"]
for key in keys:
	t=threading.Thread(target=listen,args=(key,))
	t.setDaemon(True)
	t.start()
	threads.append(t)

direction=0
while Running==True:
	time.sleep(0.25)

	moved=False

	if left==True and direction!=0:
		s.move(s.w*-1,0)
		direction=180
		moved=True
	if moved==False and right==True and direction!=180:
		s.move(s.w,0)
		direction=0
		moved=True
	if moved==False and up==True and direction!=90:
		s.move(0,s.h*-1)
		direction=270
		moved=True
	if moved==False and down==True and direction!=270:
		s.move(0,s.h)
		direction=90
		moved=True

	if moved==False:
		#print(round(s.w*math.cos(math.radians(direction))),round(s.h*math.sin(math.radians(direction))))
		s.move(round(s.w*math.cos(math.radians(direction))),round(s.h*math.sin(math.radians(direction))))
	
	#Grow
	if s.x[0]==s.pellet_x and s.y[0]==s.pellet_y:
		s.new()
		finding=True
		while finding==True:
			s.pellet_x=random.randint(0,20)*s.w
			s.pellet_y=random.randint(0,7)*s.h
			c=0
			for i,x in enumerate(s.x):
				if s.pellet_x!=s.x[i] or s.pellet_y!=s.y[i]:
					c+=1
			if c==len(s.x):
				finding=False
		s.pellet_move()

	#Self collision
	for i in range(len(s.x)):
		for j in range(len(s.x)):
			if i!=j:
				if s.x[i]==s.x[j] and s.y[i]==s.y[j]:
					Running=False


	#Edge collisions


	left=False
	right=False
	up=False
	down=False


#Display game over
with open("gameover.txt","r") as f:
	f.write("Game Over!")
p=subprocess.Popen(['notepad.exe','gameover.txt'])


for i in range(len(s.x)):
	s.close(0)
s.pellet_close()
