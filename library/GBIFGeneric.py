#=======================================================================
# Author: Alexander Keddy
#
# Copyright 2013 Alexander Keddy
#
# This file is part of GenGIS.
#
# GenGIS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GenGIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GenGIS.  If not, see <http://www.gnu.org/licenses/>.
#=======================================================================


import re
import wx
import GenGIS
from decimal import Decimal
from operator import itemgetter
class GBIFGeneric:
	
	def roundCoord(self,num):
		return round(Decimal(str(num)),1)
	
	def GETTEXT (self,obs_list, masterKeys):
		OUTL=""
		OUTS=""
		for obs in obs_list:
			locs, seqs = self.MAKEOUTS(obs, masterKeys)
			OUTL+=locs
			OUTS+=seqs
		return(OUTL,OUTS)
		
	#	Transforms the mined data into text to be output
	def MAKEOUTS (self,obs, masterKeys):
		uniqueSiteID = set()
		OUTLTEXT="Site ID, Latitude, Longitude\n"
		OUTSTEXT="Site ID, Sequence ID," + ",".join(masterKeys) + '\n'
		seqFileAgg = {}
		for location in obs:
			#location text
			OUTLTEXT += ("%s,%f,%f\n" % (location.id, location.lat, location.lon))
			for id,metadata in location.metadata.items():
				OUTSTEXT+="%s,%s" %(location.id,metadata['key'])
				for key in masterKeys:
					if str(key) in metadata.keys():
						text = ('%s' % metadata[key])#.replace(',','')
						OUTSTEXT += ',' + text.replace(',','')
					else:
						OUTSTEXT +=(',')
				OUTSTEXT += ('\n')
			
		return(OUTLTEXT.encode('utf-8'),OUTSTEXT.encode('utf-8'))
				
	# Populate the Results Table using Taxa and Geographic boundaries
	def CPPOUT (self,input):
		input = input.decode('utf-8')
		array = input.split("\n")
		return (array)
		
	def drange(self,start,stop,step):
		r = self.roundCoord(start)
		list = []
		while (r + step) <= (stop):
			list.append(self.roundCoord(r))
			r+= self.roundCoord(step)
		if r < stop:
			r -= self.roundCoord(step)
			r += (stop-step-r)
			tempR = self.roundCoord(r)	#quick rounding to try and account for the innacuracy of floats
			list.append(tempR)
		return(list)
	
	
	#subdivide a given range by longitude
	def SUBDIVIDECOL(self,minlatitude,maxlatitude,minlongitude,maxlongitude,numSubs,step):
		new_coords = []
		tem = self.drange(minlongitude, maxlongitude,step)
		#protecting for rounding errors
		minlongitude = self.roundCoord(minlongitude)
		maxlongitude = self.roundCoord(maxlongitude)
		step = self.roundCoord(step)
		for i in tem:
			minl = i
			maxl = i+step
			new_coords.append((minlatitude,maxlatitude,minl,maxl))
		return(new_coords)
	
	#subdivide a given range by latitude
	def SUBDIVIDEROW(self,minlatitude,maxlatitude,minlongitude,maxlongitude,numSubs,step):
		new_coords = []
		tem = self.drange(minlatitude,maxlatitude,step)
		#protecting for rounding errors
		minlatitude = self.roundCoord(minlatitude)
		maxlatitude = self.roundCoord(maxlatitude)
		step = self.roundCoord(step)
		for i in tem:
			minl = i
			maxl = i+step
			new_coords.append((minl,maxl,minlongitude,maxlongitude))
		return(new_coords)	
		
	def WRITEEXPORT(self,outfile,outtext,header=""):
		try:
			OUTL=open(outfile,'w')
			if(len(header)>0):
				OUTL.write(header)
			OUTL.write(outtext)
			OUTL.close()
		except IOError:
			wx.MessageBox("File could not be written. Perhaps another program is using it.")
	
	# tests if a value falls within the default space of a map
	# if it violates on either side, it is still assumed to belong to
	# the bound it is being tested against
	# ex val = 4200, bound = -180 (lower bound) func = max
	# the bound will be returned, as the val is not within the default borders
	def BorderTest(self,bound,val,func):
		res = func(bound,val)
		if func == "max":
			res = res if (-1*bound > res) else bound
		if func == "min":
			res = res if (-1*bound < res) else bound
		
		return res
		
	def	SpecialUTMConversion(self, x, y):
		convPoint=GenGIS.Point3D()
		convCoord=GenGIS.GeoCoord(x,y)
		GenGIS.MapController.GeoToGrid(GenGIS.layerTree.GetMapLayer(0).GetController(),convCoord,convPoint)
		GenGIS.MapController.GridToGeo(GenGIS.layerTree.GetMapLayer(0).GetController(),convPoint,convCoord)
		return convCoord

