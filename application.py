import tkinter
from tkinter import BOTH, HORIZONTAL, CURRENT, END
from matplotlib import pyplot

# PART I ***
# define root window
root = tkinter.Tk()
root.title('Gravity Simulator')
root.iconbitmap('earth.ico')
root.geometry('500x650')
root.resizable(0, 0)
""" 
1. define fonts and colors
2. the system default
"""
ime = 0
data = {}
for i in range(1,5):
	data['data_%d' % i] = []
# END PART I ***

# PART III ****

# defining functions 
def move(event):
	if "BALL" in main_canvas.gettags(CURRENT):
		x1 = main_canvas.coords(CURRENT)[0]
		x2 = main_canvas.coords(CURRENT)[2]
		main_canvas.coords(CURRENT, x1, event.y, x2, event.y+10)
		if main_canvas.coords(CURRENT)[3] < 15:
			main_canvas.coords(CURRENT, x1, 5, x2, 15)
		#Below the bottom of the screen
		elif main_canvas.coords(CURRENT)[3] > 415:
			main_canvas.coords(CURRENT, x1, 405, x2, 415)
	update_height()


def update_height():
	for i in range(1,5):
		heights['height_%d' % i].config(text="Height: " + str(round(415 - main_canvas.coords(balls['ball_%d' % i])[3], 2)))
 
 
def step(t):
	"""Advance the ball one 'step' based on time_slider value of t"""
	global time
	#loop through all 4 balls
	for i in range(1,5):
		a = -1*float(accelerations['a_%d' % i].get())
		v = -1*float(velocities['v_%d' % i].get())
		d = v*t + .5*a*t**2
		x1 = main_canvas.coords(balls['ball_%d' % i])[0]
		x2 = main_canvas.coords(balls['ball_%d' % i])[2]

		if main_canvas.coords(balls['ball_%d' % i])[3] + d <= 415:
			main_canvas.move(balls['ball_%d' % i], 0, d)
			y2 = main_canvas.coords(balls['ball_%d' % i])[3]
			#Draw dash line at bottom of ball
			main_canvas.create_line(x1, y2, x2, y2, tag="DASH")
		else:
			main_canvas.coords(balls['ball_%d' % i], x1, 405, x2, 415)
		#Do MORE PHYSICS
		vf = v + a*t
		#update velocity values for each ball
		velocities['v_%d' % i].delete(0, END)
		velocities['v_%d' % i].insert(0, str(round(-1*vf, 2)))
		data['data_%d' % i].append((time, 415 - main_canvas.coords(balls['ball_%d' %i])[3]))

	update_height()
	time += t

def run():
	step(t_slider.get())
	while 15 < main_canvas.coords(balls['ball_1'])[3] < 415 or 15 < main_canvas.coords(balls['ball_2'])[3] < 415 or 15 < main_canvas.coords(balls['ball_3'])[3] < 415 or 15 < main_canvas.coords(balls['ball_4'])[3] < 415:
		step(t_slider.get())

def graph():
	colors = ['red', 'green', 'blue', 'yellow']
	for i in range(1,5):
		x = []
		y = []
	for data_list in data['data_%d' % i]:
		x.append(data_list[0])
		y.append(data_list[1])
		pyplot.plot(x, y, color=colors[i-1])
	# format the graph
	pyplot.title('Distance Vs. Time')
	pyplot.xlabel('Time')
	pyplot.ylabel('Distance')
	pyplot.show()

def reset():
	global time
	time = 0
	main_canvas.delete("DASH")
	for i in range(1,5):
		velocities['v_%d' % i].delete(0, END)
		velocities['v_%d' % i].insert(0, '0')
		accelerations['a_%d' % i].delete(0, END)
		accelerations['a_%d' % i].insert(0, '0')
		main_canvas.coords(balls['ball_%d' % i], 45+(i-1)*100, 405, 55+(i-1)*100, 415)
		data['data_%d' % i].clear()
	update_height()
	t_slider.set(1)

#END PART III ****


# PART II ***
# -> assigning global variable and main frame
canvas_frame = tkinter.Frame(root)
input_frame = tkinter.Frame(root)
canvas_frame.pack(pady = 10)
input_frame.pack(fill = BOTH, expand = True)

# frame layouts
main_canvas = tkinter.Canvas(canvas_frame, width = 400, height = 420, bg = 'white')
main_canvas.grid(row=0, column=0, padx=5, pady=5)

line_0 = main_canvas.create_line(2, 0, 2, 415)
line_1 = main_canvas.create_line(100, 0, 100, 415)
line_2 = main_canvas.create_line(200, 0, 200, 415)
line_3 = main_canvas.create_line(300, 0, 300, 415)
line_4 = main_canvas.create_line(400, 0, 400, 415)

balls = {}
balls['ball_1'] = main_canvas.create_oval(45, 405, 55, 415, fill = 'red', tag = "BALL")
balls['ball_2'] = main_canvas.create_oval(145, 405, 155, 415, fill = 'green', tag = "BALL")
balls['ball_3'] = main_canvas.create_oval(245, 405, 255, 415, fill = 'yellow', tag = "BALL")
balls['ball_4'] = main_canvas.create_oval(345, 405, 355, 415, fill = 'blue', tag = "BALL")

# input frame, row labels
tkinter.Label(input_frame, text = 'd').grid(row=0, column=0) #displacement
tkinter.Label(input_frame, text = 'v').grid(row=1, column=0) #velocity
tkinter.Label(input_frame, text = 'a').grid(row=2, column=0, ipadx = 22) #acceleration
tkinter.Label(input_frame, text = 't').grid(row=3, column=0) #time

# distance / heights labels
heights = {}
for i in range(1, 5):
	heights['height_%d' % i] = tkinter.Label(input_frame, text = "Height: " + str(415 - main_canvas.coords(balls['ball_%d' % i])[3]))
	heights['height_%d' % i].grid(row=0, column=i)

# velocity labels entries
velocities = {}
for i in range(1, 5):
	velocities['v_%d' % i] = tkinter.Entry(input_frame, width = 15)
	velocities['v_%d' % i].grid(row=1, column=i, padx=1)
	velocities['v_%d' % i].insert(0, '0')

# accelerations labels entries
accelerations = {}
for i in range (1, 5):
	accelerations['a_%d' % i] = tkinter.Entry(input_frame, width = 15)
	accelerations['a_%d' % i].grid(row=2, column=i, padx=1)
	accelerations['a_%d' % i].insert(0, '0')

# time sliders
t_slider = tkinter.Scale(input_frame, from_ = 0, to = 1, tickinterval = .1, resolution = .01, orient = HORIZONTAL)
t_slider.grid(row=3, column=1, columnspan=4, sticky='WE')
t_slider.set(1)

# buttons
step_button = tkinter.Button(input_frame, text = "Step", command=lambda:step(t_slider.get()), bg='#f4853a')
run_button = tkinter.Button(input_frame, text = "Play", command = run, bg = '#27f96d')
graph_button = tkinter.Button(input_frame, text = "Graph", command = graph, bg = '#6ddaf0')
reset_button = tkinter.Button(input_frame, text = "Reset", command = reset, bg = '#d3ecf2')
quit_buttton = tkinter.Button(input_frame, text = "QUIT", command = root.destroy, bg = '#eb5050')
# put buttons on main window
step_button.grid(row=4, column=1, pady=(10, 0), sticky="WE")
run_button.grid(row=4, column=2, pady=(10, 0), sticky="WE")
graph_button.grid(row=4, column=3, pady=(10, 0), sticky="WE")
reset_button.grid(row=4, column=4, pady=(10, 0), sticky="WE")
quit_buttton.grid(row=5, column=1, columnspan=4, sticky="WE")
#END PART II ***


# make each ball to move vertically
root.bind('<B1-Motion>', move)

# this should be last, means running the application
root.mainloop()