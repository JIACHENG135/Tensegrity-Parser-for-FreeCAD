import scipy.io as scio
import numpy as np
import math
import random

import collections
import FreeCADGui
import FreeCAD
class MyList(list):
	'''
	data structure used to simplify Matrix manipulation. All build-in functions
	
	'''
	def __init__(self,*args):
		list.__init__(self,*args)
	def __sub__(self,other):
		for ind,i in enumerate(other):
			self[ind] -= i
		return self
	def _norm(self):
		ans = 0
		for i in self:
			ans += i**2
		return ans**0.5
	def _cross(self,other):
		return MyList(np.cross(self,other))

	def _dot(self,other):
		return sum([i*j for i,j in zip(self,other)])

	def _euler_angle(self):
		norm = self._norm()
		normalized = MyList([self[0]/norm,self[1]/norm,self[2]/norm])
		wait = MyList([0,0,1])
		x1,y1,z1 = normalized
		v = wait._cross(normalized)
		a = math.atan2(normalized._cross(wait)._norm(),normalized._dot(wait))
		return [a,v]





class Buffer:
	ROOT = "C:\\Users\\ljc14\\AppData\\Roaming\\FreeCAD\\Macro\\"
	def __init__(self,filename,root=""):
		'''
		The input file should have MATLAB variable N(n*3) C_b C_s ,optional BAR_RADIUS(beta*1)
		The filename should be a .mat file that save MATLAB variables.
		'''
		if root:
			self.ROOT = root
		self.data = scio.loadmat(self.ROOT+filename)
		self.doc = FreeCAD.newDocument()
		try:
			assert 'N' in self.data
			self.N = self.data["N"]
		except:
			print("N should be included")

		try:
			assert "C_b" in self.data
			assert "C_s" in self.data
			self.cb = self.data["C_b"]
			self.cs = self.data["C_s"]
		except:
			print("C_b,C_s should be included")
		try:
			assert "BAR_RADIUS" in self.data
			self.bar_radius = self.data["BAR_RADIUS"]
		except:
			self.bar_radius = []
			for i in range(len(self.cb)):
				self.bar_radius.append(random.random()*0.1+0.05)
#			self.bar_radius = []
	def _draw_bar(self,slice=0):
		for ind,row in enumerate(self.cb):
			row = list(row)
			start,end = row.index(-1),row.index(1)
			startN,endN = MyList(self.N[start]),MyList(self.N[end])
			name = "Bar_{}".format(str(ind))
			vec_ori = endN-startN
			angle,vector = vec_ori._euler_angle()
			vec = tuple(vec_ori)
			pos = tuple(startN)
			try:
				box = self.doc.getObject(name)
				assert box is not None
			except:
				box = self.doc.addObject("Part::Cylinder",name)
			box.Placement = App.Placement(App.Vector(pos),App.Rotation(App.Vector(tuple(vector)),angle/(math.pi/180)))
			box.Height = vec_ori._norm()
			if self.bar_radius:
				box.Radius = self.bar_radius[ind]
			else:
				box.Radius = 0.1
			self.doc.recompute()
		for ind,row in enumerate(self.cs):
			row = list(row)
			start,end = row.index(-1),row.index(1)
			startN,endN = MyList(self.N[start]),MyList(self.N[end])
			name = "String_" + str(ind)
			vec_ori = endN-startN
			angle,vector = vec_ori._euler_angle()
			vec = tuple(vec_ori)
			pos = tuple(startN)
			try:
				box = self.doc.getObject(name)
				assert box is not None
			except:
				box = self.doc.addObject("Part::Cylinder",name)
			box.Placement = App.Placement(App.Vector(tuple(startN)),App.Rotation(App.Vector(tuple(vector)),angle/(math.pi/180)))
			box.Height = vec_ori._norm()
			box.Radius = 0.05
			box.ViewObject.ShapeColor = (1.0,0.0,0.0)
			self.doc.recompute()
	def _draw_joint(self,pattern="linear",decay_factor = 1,slice=0):
		
		g = collections.defaultdict(int)
		base_radius = 0.05
		uniform_radius = 0.3
		for row in self.cb:
			row = list(row)
			start,end = row.index(-1),row.index(1)
			g[start] += 1
			g[end] += 1
		for n in g:
			name = "Sphere at nodes{}".format(str(n))
			try:
				sphere = self.doc.getObject(name)
				assert sphere is not None
			except:
				sphere = self.doc.addObject("Part::Sphere",name)
			if pattern == "linear":
				sphere.Radius = base_radius * g[n]
			else:
				sphere.Radius = uniform_radius
			pos = tuple(self.N[n])
			sphere.Placement = App.Placement(App.Vector(pos),App.Rotation(App.Vector(0,0,0),1))
			self.doc.recompute()


	


	
if __name__ == "__main__":
	b = Buffer("N_out_cell.mat","C:\\Users\\ljc14\\Desktop\\")
	b._draw_bar()
	b._draw_joint('non-linear')

		
	


		


