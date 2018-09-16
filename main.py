#!/usr/local/bin/python
from Tkinter import Canvas, Tk, Frame, Button, RAISED, TOP, BOTTOM, StringVar, Label, RIGHT, RIDGE, LEFT
import random
import math
import sys
from UnionFind import UnionFind

tk = Tk()
tk.wm_title("Steiner MST")

global oPoints
oPoints = []
global rsPoints
rsPoints = []
global gsPoints
gsPoints = []
global MST
MST = []

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.deg = 0
		self.edges = []
		self.MSTedges = []
	def update(self, edge):
		self.edges.append(edge)
	def reset(self):
		self.edges = []
		self.deg = 0
		self.MSTedges = []
	def MSTupdate(self, edge):
		self.deg += 1
		self.MSTedges.append(edge)

class Line:
	def __init__(self, p1, p2, w):
		self.points = []
		self.points.append(ref(p1))
		self.points.append(ref(p2))
		self.w = w
	def getOther(self, pt):
		if pt == self.points[0].get():
			return self.points[1]
		elif pt == self.points[1].get():
			return self.points[0]
		else:
			print "Error"
	def getFirst(self):
		return self.points[0]
	def getLast(self):
		return self.points[1]

class ref:
	def __init__(self, obj):
		self.obj = obj
	def get(self):
		return self.obj
	def set(self, obj):
		self.obj = obj

def addMousePoint(event):
	addpt = True
	if oPoints == []:
		if (event.x < 10) and (event.x >= 500) and (event.y < 10) and (event.y >= 500):
				addpt = False
	else:
		for pt in oPoints:
			dist = math.sqrt(pow((event.x - pt.x),2) + pow((event.y - pt.y),2))
			if dist < 11:
				addpt = False
			if (event.x < 10) and (event.x >= 500) and (event.y < 10) and (event.y >= 500):
				addpt = False
	if addpt ==  True:
			addPoint(event.x, event.y)

def addPoint(x, y):
	global MST
	del MST[:]
	canvas.create_oval(x-5,y-5,x+5,y+5, outline="black", fill="white", width=1)
	point = Point(x, y)
	global oPoints
	oPoints.append(point)

def Kruskal(SetOfPoints, type):
	for i in xrange(0,len(SetOfPoints)):
		SetOfPoints[i].reset()
	for i in xrange(0,len(SetOfPoints)):
		for j in xrange(i,len(SetOfPoints)):
			if i != j:
				if type == "R":
					dist = (abs(SetOfPoints[i].x-SetOfPoints[j].x)
						+ abs(SetOfPoints[i].y - SetOfPoints[j].y))
				elif type == "G":
					dist = math.sqrt(pow((SetOfPoints[i].x-SetOfPoints[j].x),2) +
					pow((SetOfPoints[i].y - SetOfPoints[j].y),2))
				else:
					"All of the Errors!"
				line = Line(SetOfPoints[i], SetOfPoints[j], dist)
				SetOfPoints[i].update(line)
				SetOfPoints[j].update(line)
			else:
				dist = 100000
				line = Line(SetOfPoints[i], SetOfPoints[j], dist)
				SetOfPoints[i].update(line)

	G = {}
	for i in xrange(0,len(SetOfPoints)):
		off = 0
		subset = {}
		for j in xrange(0,len(SetOfPoints[i].edges)):
			subset[j] = SetOfPoints[i].edges[j].w
		G[i] = subset

	subtrees = UnionFind()
	tree = []
	for W,u,v in sorted((G[u][v],u,v) for u in G for v in G[u]):
		if subtrees[u] != subtrees[v]:
			tree.append([u,v])
			subtrees.union(u,v)

	MST = []
	for i in xrange(0,len(tree)):
		point1 = SetOfPoints[tree[i][0]]
		point2 = SetOfPoints[tree[i][1]]
		for j in xrange(0,len(point1.edges)):
			if point2 == point1.edges[j].getOther(point1).get():
				point1.MSTupdate(point1.edges[j])
				point2.MSTupdate(point1.edges[j])
				MST.append(point1.edges[j])
	return MST

def DeltaMST(SetOfPoints, TestPoint, type):
	if type == "R":
		MST = Kruskal(SetOfPoints, "R")
	else:
		MST = Kruskal(SetOfPoints, "G")

	cost1 = 0
	for i in xrange(0,len(MST)):
		cost1 += MST[i].w

	combo = SetOfPoints + [TestPoint]

	if type == "R":
		MST = Kruskal(combo, "R")
	else:
		MST = Kruskal(combo, "G")

	cost2 = 0
	for i in xrange(0,len(MST)):
		cost2 += MST[i].w
	return cost1 - cost2

def HananPoints(SetOfPoints):
	totalSet = SetOfPoints
	SomePoints = []
	for i in xrange(0,len(totalSet)):
		for j in xrange(i,len(totalSet)):
			if i != j:
				SomePoints.append(Point(totalSet[i].x, totalSet[j].y))
				SomePoints.append(Point(totalSet[j].x, totalSet[i].y))
	return SomePoints

def BrutePoints(SetOfPoints):
	if SetOfPoints != []:
		SomePoints = []
		xmax = (max(SetOfPoints,key=lambda x: x.x)).x
		xmin = (min(SetOfPoints,key=lambda x: x.x)).x
		ymax = (max(SetOfPoints,key=lambda x: x.y)).y
		ymin = (min(SetOfPoints,key=lambda x: x.y)).y

		rangex = range(xmin,xmax)
		rangey = range(ymin,ymax)
		for i in rangex[::10]:
			for j in rangey[::10]:
				SomePoints.append(Point(i,j))
		return SomePoints
	else:
		return []

def compute():
	canvas.delete("all")
	global MST
	if MST == []:
		global gsPoints
		del gsPoints[:]
		Candidate_Set = [0]

		while Candidate_Set != []:
			maxPoint = Point(0,0)
			Candidate_Set = [x for x in BrutePoints(oPoints + gsPoints) if DeltaMST(oPoints + gsPoints, x, "G") > 0]
			cost = 0
			for pt in Candidate_Set:
				DeltaCost = DeltaMST(oPoints + gsPoints, pt, "G")
				if DeltaCost > cost:
					maxPoint = pt
					cost = DeltaCost

			if (maxPoint.x != 0 and maxPoint.y != 0):
				gsPoints.append(maxPoint)
			for pt in gsPoints:
				if pt.deg <= 2:
					gsPoints.remove(pt)
				else:
					pass

		MST = Kruskal(oPoints+gsPoints, "G")

	MSTminDist = 0
	for i in xrange(0,len(MST)):
		MSTminDist += MST[i].w
		canvas.create_line(MST[i].points[0].get().x, MST[i].points[0].get().y,
			MST[i].points[1].get().x, MST[i].points[1].get().y, width=2)

	for i in xrange(0,len(gsPoints)):
		canvas.create_oval(gsPoints[i].x-5,gsPoints[i].y-5,
			gsPoints[i].x+5,gsPoints[i].y+5, outline="black", fill="black", width=1)

	for i in xrange(0,len(oPoints)):
		canvas.create_oval(oPoints[i].x-5,oPoints[i].y-5,
			oPoints[i].x+5,oPoints[i].y+5, outline="black", fill="white", width=1)

	MSTtext.set(str(round(MSTminDist, 2)))

def clear():
	global oPoints
	del oPoints[:]
	global rsPoints
	del rsPoints[:]
	global gsPoints
	del gsPoints[:]
	global MST
	del MST[:]
	MSTtext.set("0")
	canvas.delete("all")

master = Canvas(tk)
but_frame = Frame(master)
var = StringVar()
var.set("Distance:")
button = Button(but_frame, text = "Draw", command = compute)
button.configure(width=9, activebackground = "blue", relief = RIDGE)
button.pack(side=LEFT)
Label(but_frame, textvariable=var).pack(side=LEFT)
MSTtext = StringVar()
label = Label(but_frame, textvariable=MSTtext)
label.pack(side=LEFT)
Label(but_frame, textvariable="").pack(side=LEFT)
resetButton = Button(but_frame, text = "Clear", command = clear)
resetButton.configure(width=9, activebackground = "blue", relief = RAISED)
resetButton.pack(side=LEFT)
but_frame.pack(side=BOTTOM, expand=0)
canvas = Canvas(master, width = 700, height = 500, bd=5, relief=RIDGE, bg='#FFF')
canvas.bind("<Button-1>", addMousePoint)
canvas.pack(expand=0)
master.pack(expand=0)

MSTtext.set("0")

addPoint(200, 200)
addPoint(200, 400)
addPoint(400, 200)
addPoint(400, 400)

tk.mainloop()
