from GBIFQueryLayout import GBIFQueryLayout

import GenGIS
import wx
import math
import pickle
import urllib2
import re
import sys
from xml.dom import minidom
from dataHelper import isNumber
from GBIFGeneric import GBIFGeneric
from GBIFSpecific import GBIFSpecific

class GBIFQuery(GBIFQueryLayout):
	#	Global variables to store queried information
	__obs__ = []
	__conversions__ = []
	__selectedTaxon__= []
	__description__=""
	
	def __init__(self,parent=None):
#		import pdb; pdb.set_trace()
		self.GBIFSPECIFIC = GBIFSpecific()
		self.GBIFGENERIC = GBIFGeneric()
		GBIFQueryLayout.__init__(self,parent)
		self.SetIcon(wx.Icon(GenGIS.mainWindow.GetExeDir() + "images/CrazyEye.ico",wx.BITMAP_TYPE_ICO))
		self.m_bitmap3.SetIcon(wx.Icon(GenGIS.mainWindow.GetExeDir() + "images/GBIF_compass_small.png",wx.BITMAP_TYPE_PNG))
		self.graphicalElementIds=[]
		self.__selectedTaxon__=[]
		self.__obs__ = []
		self.__conversions__ = []
		self.m_IDList.Clear()
		#No Map Data
		self.m_AddData.Disable()
		#Map Data
		if GenGIS.layerTree.GetNumMapLayers() > 0 :
			self.m_AddData.Enable()
			borders = GenGIS.layerTree.GetMapLayer(0).GetController().GetMapBorders()
			self.m_MinLat.SetValue(borders.y1)
			self.m_MaxLat.SetValue(borders.dy)
			self.m_MinLon.SetValue(borders.x1)
			self.m_MaxLon.SetValue(borders.dx)
		
	#	Query GBIF for Taxa in Lat/Lon Boundary
	def OnSearch(self,event):
		wx.BeginBusyCursor()
		#	Clear the results list
		self.m_Result.Clear()
		
		taxon = self.m_TaxonName.GetLineText(0)
		#TEST  CASES REMOVE BEFORE LAUNCH
		if(taxon=="TEST"):
			taxon="Liolaemus darwinii"
		#	self.m_MinLat.SetValue(-34)
		#	self.m_MaxLat.SetValue(-31)
		#	self.m_MinLon.SetValue(-72)
		#	self.m_MaxLon.SetValue(-66)
		elif(taxon=="TE"):
			taxon="Apolochiton"
			self.m_MinLat.SetValue(-34)
			self.m_MaxLat.SetValue(-31)
			self.m_MinLon.SetValue(-72)
			self.m_MaxLon.SetValue(-66)
		elif(taxon=="Galaxiidae"):
			taxon="Galaxiidae"
			self.m_MinLat.SetValue(-42)
			self.m_MaxLat.SetValue(-26)
			self.m_MinLon.SetValue(127)
			self.m_MaxLon.SetValue(167)
		taxon=taxon.split()
		if(len(taxon)==0):
			wx.MessageBox("You did not enter a taxon name.")
		else:
			minLatitude= self.m_MinLat.GetValue()
			maxLatitude= self.m_MaxLat.GetValue()
			minLongitude= self.m_MinLon.GetValue()
			maxLongitude= self.m_MaxLon.GetValue()
			self.GBIFSPECIFIC.GETTAXRESULT(taxon,self.m_Result)
		wx.EndBusyCursor()
		
	#	Create Sequence and Location files for selected Taxa 		
	def OnCalculate(self,event):
		self.m_staticText6.SetLabel("\n")
		records,distLocations = 0,0
		self.__obs__=[]
		self.__conversions__=[]
		wx.BeginBusyCursor()
		if(self.__selectedTaxon__):
			minLatitude= self.m_MinLat.GetValue()
			maxLatitude= self.m_MaxLat.GetValue()
			minLongitude= self.m_MinLon.GetValue()
			maxLongitude= self.m_MaxLon.GetValue()
			self.m_Progress.WriteText("Starting...\n")
			for tax in self.__selectedTaxon__:
				obs,con,recs,distLocs,description= self.GBIFSPECIFIC.GETOBSENTIRERANGE(tax.split(),minLatitude,maxLatitude,minLongitude,maxLongitude,self.m_Progress)
				self.__obs__.append(obs)
				self.__conversions__.append(con)
				self.__description__+="%s\n" % description
				records += recs
				distLocations +=distLocs
			self.m_Progress.WriteText("Done.\n")
		else:
			wx.MessageBox("Please select some Taxa.")
		
		self.m_staticText6.SetLabel("%d records retrieved.\n%d distinct locations." %(records,distLocations))
		wx.EndBusyCursor()
	
	#	Present the number of locations a user is about to query
	#	Used as a check by the user to know they aren't going to produce way too much data.
	def OnPreCalculate(self,event):
		self.m_staticText6.SetLabel("\n")
		if(self.__selectedTaxon__):
			minLatitude= self.m_MinLat.GetValue()
			maxLatitude= self.m_MaxLat.GetValue()
			minLongitude= self.m_MinLon.GetValue()
			maxLongitude= self.m_MaxLon.GetValue()
			count=0
			for tax in self.__selectedTaxon__:
				count+=self.GBIFSPECIFIC.GETCOUNT(tax.split(),minLatitude,maxLatitude,minLongitude,maxLongitude,self.m_Progress)
		else:
			wx.MessageBox("Please select some Taxa.")
		self.m_staticText6.SetLabel("There were %d records for the given location." % count) 
	
	#	Redirects User to Wiki page for this plugin
	def OnHelp(self, event):
		wx.LaunchDefaultBrowser( 'http://kiwi.cs.dal.ca/GenGIS/Description_of_GenGIS_plugins#Linear_Regression' )
	
	#	Adds Data to GenGIS
	def OnAddData(self,event):
		if (len(self.__obs__) > 0):
			OUTLText, OUTSText = self.GBIFGENERIC.GETTEXT(self.__obs__,self.__conversions__)
			OUTLArray=self.GBIFGENERIC.CPPOUT(OUTLText)
			OUTSArray=self.GBIFGENERIC.CPPOUT(OUTSText)
			OUTLArray.insert(0,"Site ID,Latitude,Longitude,Richness,Cell ID")
			OUTSArray.insert(0,"Sequence ID,Site ID,CellLat,CellLong,Taxon,Genus,TrueLat,TrueLong,Count,AllRecords")					
			OUTLArray.pop()
			OUTSArray.pop()
			layerName = "GBIFLayer_%d" % GenGIS.layerTree.GetNumLocationLayers()
			GenGIS.mainWindow.OpenLocationsCSVFile(OUTLArray, layerName)
			GenGIS.mainWindow.OpenSequenceCSVFile(OUTSArray, layerName)
			
			#Get the number of last location layer added (the gbif one)
			numLocationLayers=GenGIS.layerTree.GetNumLocationSetLayers()
			locationSetLayer = GenGIS.layerTree.GetLocationSetLayer(numLocationLayers-1)
			locationSetLayer.SetDescription(self.__description__)
			
		else:
			wx.MessageBox("Please make a successful GBIF Query first.")
		

	#	Exports Location and Sequence Data to a location of the users choice
	def OnExportData(self,event):
		if (len(self.__obs__) > 0):
			fileTypes = 'Loc and Seq Files (*.csv)|*.csv'
			dlg = wx.FileDialog(self, "Save plot", "", "", fileTypes, wx.SAVE)
			if dlg.ShowModal()==wx.ID_OK:
				filename =	dlg.GetFilename()
				dir = dlg.GetDirectory()
				file_split = filename.split(".",1)
				#creates the directories
				OUTLfile = ("%s/%s_locs.csv" % (dir,file_split[0]))				
				OUTSfile = ("%s/%s_seqs.csv" % (dir,file_split[0]))
				OUTDfile = ("%s/%s_source.txt" % (dir,file_split[0]))
				OUTLText, OUTSText = self.GBIFGENERIC.GETTEXT(self.__obs__,self.__conversions__)
				self.GBIFGENERIC.WRITEEXPORT(OUTLfile,OUTLText,"Site ID,Latitude,Longitude,Richness,Cell ID\n")
				self.GBIFGENERIC.WRITEEXPORT(OUTSfile,OUTSText,"Sequence ID,Site ID,CellLat,CellLong,Taxon,Genus,TrueLat,TrueLong,Count,AllRecords\n")
				description = self.__description__.encode('utf-8')
				self.GBIFGENERIC.WRITEEXPORT(OUTDfile,description,"")
			dlg.Destroy()
		else:
			wx.MessageBox("Please make a successful GBIF Query first.")
	
	#	Add Data from Results Table to ID List
	def OnAdd(self,event):
		i=0
		IDCount = self.m_IDList.GetCount()
		for index in self.m_Result.GetSelections():
			selected = self.m_Result.GetString(index)
			self.m_IDList.InsertItems(["%s" % selected],IDCount+i)
			split = selected.split(" | ")
			self.__selectedTaxon__.append(split[1])
			i+=1
			
	#	Remove Data from ID List
	def OnRemove(self,event):
		for index in self.m_IDList.GetSelections():
			selected = self.m_IDList.GetString(index)
			split = selected.split(" | ")
			self.__selectedTaxon__.remove(split[1])
			self.m_IDList.Delete(index)
	
	#	Close the Plugin
	def OnClose(self, event):
		# remove plotted lines
		for id in self.graphicalElementIds:
			GenGIS.graphics.RemoveLine(id)

		GenGIS.viewport.Refresh()
		event.Skip()
	
	#	Close the Plugin
	def OnOK( self, event ):
		self.Close()
		
		
##########################################		
#	HERES LIES THE CORE FUNCTIONS OF THE GBIF QUERY		
#	WITH GREAT POWER COMES GREAT RESPONSIBILITY
##########################################
'''
######################
#	GENERIC FUNCTIONS
######################
	
	
	def GBIFGENERIC.GETTEXT (self,obs_list,conversions_list):
		OUTL=""
		OUTS=""
		for obs,convs in zip(obs_list,conversions_list):
	#		import pdb; pdb.set_trace()
			locs, seqs = self.MAKEOUTS(obs,convs)
			OUTL+=locs
			OUTS+=seqs
		return(OUTL,OUTS)
		
	#	Transforms the mined data into text to be output
	def MAKEOUTS (self,obs,conversions):
		uniqueSiteID = set()
		OUTLTEXT=""
		OUTSTEXT=""
		seqFileAgg = {}
		for cellOut in sorted(obs.keys()):
			if len(obs[cellOut].keys()) > 0:
				for taxOut in sorted(obs[cellOut].keys()):
					thisList=obs[cellOut][taxOut]
					for ent in thisList:
						fullLat = float(re.sub(r'\<.*?\>','',ent[1]))
						fullLon = float(re.sub(r'\<.*?\>','',ent[2]))
						siteID = "%s_%f_%f" %(taxOut,fullLat,fullLon)
						if siteID not in uniqueSiteID:
							uniqueSiteID.add(siteID)
							OUTLTEXT += ("%s,%f,%f,%d,%d\n" % (siteID, fullLat, fullLon, len(obs[cellOut].keys()), cellOut ))
						toKey = "%s,%f,%f,%s,%s,%s,%s" %(siteID, conversions[cellOut][0],conversions[cellOut][1],ent[3],taxOut,ent[1],ent[2])
						toKey = re.sub(r'\<.*?\>','',toKey)
						try:
							seqFileAgg[toKey].extend([ent[0]])
						except KeyError:
							seqFileAgg[toKey]=[ent[0]]
		seqFileAgg_items = seqFileAgg.items()
		seqFileAgg_items.sort(key=lambda x: x)
		for outME,IDlist in seqFileAgg_items:
			OUTSTEXT += ("%d,%s,%d,%s\n" %(IDlist[0],outME,len(IDlist),'|'.join(str(i) for i in IDlist)))
		return(OUTLTEXT,OUTSTEXT)
				
	# Populate the Results Table using Taxa and Geographic boundaries
	def CPPOUT (self,input):
		array = input.split("\n")
		return (array)
	
	#subdivide a given range by longitude
	def SUBDIVIDECOL(self,minlatitude,maxlatitude,minlongitude,maxlongitude):
		longitudeRange = maxlongitude - minlongitude
		new_coords = []
		longitudeBase= float(longitudeRange)/float(10)
		for i in range(0,10):
			new_coords.append(( minlatitude,maxlatitude,minlongitude+longitudeBase * i,minlongitude+longitudeBase* (i+1)))
		return(new_coords)
	
	#subdivide a given range by latitude
	def SUBDIVIDEROW(self,minlatitude,maxlatitude,minlongitude,maxlongitude):
		latitudeRange = maxlatitude - minlatitude
		new_coords = []
		latitudeBase= float(latitudeRange)/float(10)
		for i in range(0,10):
			new_coords.append((minlatitude + latitudeBase*i,minlatitude + latitudeBase *(i+1),minlongitude,maxlongitude))
		return(new_coords)	
		
	def GBIFGENERIC.WRITEEXPORT(self,outfile,outtext,header):
		try:
			OUTL=open(outfile,'w')
			if(len(header)>0):
				OUTL.write(header)
			OUTL.write(outtext)
			OUTL.close()
		except IOError:
			wx.MessageBox("File could not be written. Perhaps another program is using it.")
###########################
#	GBIF SPECIFIC SPECIFIC
###########################

	# get source of data sets as well as rights and citation
	def GETRIGHTS(self,fh):
		desc=""
		resource=fh.getElementsByTagName("gbif:dataResources")
		for node in resource:
			name = node.getElementsByTagName("gbif:name")
			rights = node.getElementsByTagName("gbif:rights")
			citation = node.getElementsByTagName("gbif:citation")
			desc+="##########################\n"
			for tem in name:
				desc+= "Name\n"
				desc+= re.sub(r'<.*?\>','',tem.toprettyxml(' '))
			for tem in rights:
				desc+= "\nRights\n"
				desc+= re.sub(r'<.*?\>','',tem.toprettyxml(' '))
			for tem in citation:
				desc+= "\nCitation\n"
				desc+= re.sub(r'<.*?\>','',tem.toprettyxml(' '))
			desc+="\n"
		return(desc)

	#	Queries GBIF to find the number of results for given boundary 
	def GBIFSPECIFIC.GETCOUNT(self,taxon_name,minLat,maxLat,minLon,maxLon):
		taxonReq = '+'.join(taxon_name)			
		cID = self.GETTAXID(taxonReq)
		url= " http://data.gbif.org/ws/rest/occurrence/count?taxonconceptkey=%d&maxlatitude=%d&minlatitude=%d&maxlongitude=%d&minlongitude=%d" % (cID,maxLat,minLat,maxLon,minLon) 
		try:	
			response=urllib2.urlopen(url).read()
		except urllib2.HTTPError as e:
			wx.MessageBox("The server is temporarily unreachable.\nPlease try again later.")
			self.Close()
		key_string = re.search('gbif:summary totalMatched="(\d+)"',response)
		count_string=re.search('\d+',key_string.group())
		count = int(count_string.group())
		return(count)
			
	def GBIFSPECIFIC.GETTAXRESULT(self,taxon_name):
		taxonReq = '+'.join(taxon_name)

		taxonList=()
		FAIL = 0
		try:
			taxonList = [line.strip() for line in open(taxonReq)]
		except IOError:
			FAIL=1
		if(FAIL==1):
			taxonReq_2 = taxonReq+".txt"
			FAIL=0
			try:
				taxonList = [line.strip() for line in open(taxonReq_2)]
			except IOError:
				FAIL=1
		if(FAIL==1):
			taxonList=[taxonReq]
		obs={}
				
		for taxonName in taxonList:	
			pos=0
			url="http://data.gbif.org/ws/rest/taxon/list?scientificname="+taxonName+"*&dataproviderkey=1&dataresourcekey=1"
			try:	
				html=urllib2.urlopen(url)
			except urllib2.HTTPError as e:
				wx.MessageBox("The server is temporarily unreachable.\nPlease try again later.")
				self.Close()
			taxResponse=html.read()
			taxxmldoc=minidom.parseString(taxResponse)
			taxNodeList=taxxmldoc.getElementsByTagName("tc:TaxonConcept")
		
			if (len(taxNodeList) > 0):
				for taxResult in taxNodeList:
					string = taxResult.toxml()
					key_string = re.search('gbifKey="(\d+)"',string)
					id_string=re.search('\d+',key_string.group())
					id = int(id_string.group())
					name=self.Strip(string,"<tn:nameComplete>.*")
					rank=self.Strip(string,"<tn:rankString>.*")
					according=self.Strip(string,"<tc:accordingToString>.*")
					self.m_Result.InsertItems(["%d | %s | %s | %s"%(id,name,rank,according)],pos)
					pos+=1
			else:
				wx.MessageBox("No Tax Found.")
				return(-1)
			return(1)
	
	#	Get smallest TAX ID. 
	def	Strip (self,Node,tag):
		name = re.search(('%s' % tag),Node)
		name=name.group()
		name = re.sub(r'<.*?\>','',name)
		name = re.sub(r'[^A-Za-z ]+','',name)
		name = re.sub(r' *$','',name)
		return name
	
	#	Convert TaxonName to a Concept ID for GBIF
	def GETTAXID (self,taxonName):
		taxConceptID=100000000
		url="http://data.gbif.org/ws/rest/taxon/list?scientificname="+taxonName+"*&dataproviderkey=1&dataresourcekey=1"
		try:	
			html=urllib2.urlopen(url)
		except urllib2.HTTPError as e:
			self.m_Progress.WriteText("%s\n" % e.code)
			wx.MessageBox("The server is temporarily unreachable.\nPlease try again later.")
			self.Close()
		taxResponse=html.read()
		taxxmldoc=minidom.parseString(taxResponse)
		taxNodeList=taxxmldoc.getElementsByTagName("tc:TaxonConcept")
		for taxResult in taxNodeList:
			string = taxResult.toprettyxml(indent=' ')
			key_string = re.search('gbifKey="(\d+)"',string)
			if key_string:
				id_string=re.search('\d+',key_string.group())
				id = int(id_string.group())
				if id < taxConceptID:
					taxConceptID = id
		if taxConceptID == 100000000:
	#		sys.exit("No frigging taxon concept found")
			return(-1)
		return(taxConceptID)
		
	# Search for a Taxon Name in a Geographic boundary
	def GBIFSPECIFIC.GETOBSENTIRERANGE(self,taxon_name,minLatitude,maxLatitude,minLongitude,maxLongitude):
		records=0
		distLocations=set()
		
		conversions = {}
		taxonReq = '+'.join(taxon_name)
		####################################
		#	check if text file or command input
		#	if (ends in .txt) then text
		#	if ! then append .txt and check
		####################################
		taxonList=()
		FAIL = 0
		try:
			taxonList = [line.strip() for line in open(taxonReq)]
		except IOError:
			FAIL=1
		if(FAIL==1):
			taxonReq_2 = taxonReq+".txt"
			FAIL=0
			try:
				taxonList = [line.strip() for line in open(taxonReq_2)]
			except IOError:
				FAIL=1
		if(FAIL==1):
			taxonList=[taxonReq]
		obs={}
		description=""
		for taxonName in taxonList:
			self.m_Progress.WriteText("########### Querying GBIF for %s ######\n" % taxonName)
			cID = self.GETTAXID(taxonName)
			if(cID == -1):
				self.m_Progress.WriteText("No concept ID found for %s. Skipping...\n" % taxonName)
				continue
			self.m_Progress.WriteText("Concept ID: %d\n" % cID)
			### The set of observations
			### hash key #1 = grid cell
			### hash #2 = scientific name
			### value = list of GBIF key + list of lat/longs of genus observations in that grid cell

			fullTaxonomy={}
			resultCount =self.GBIFSPECIFIC.GETCOUNT(taxon_name,minLatitude,maxLatitude,minLongitude,maxLongitude)
			#chek if whole window fits: if not divide into columns
			nodeList=[]
			if resultCount>1000 :
				newCoords = self.SUBDIVIDECOL(minLatitude,maxLatitude,minLongitude,maxLongitude)
				for coords in newCoords:
					colMinLongitude = coords[2]
					colMaxLongitude = coords[3]
					colMinLatitude = coords[0]
					colMaxLatitude = coords[1]
					
					resultCount =self.GBIFSPECIFIC.GETCOUNT(taxon_name,colMinLatitude,colMaxLatitude,colMinLongitude,colMaxLongitude)
					#check if col fits: if not divide into cells
					if resultCount > 1000:
						newCoords = self.SUBDIVIDEROW(colMinLatitude,colMaxLatitude,colMinLongitude,colMaxLongitude)
						for coords in newCoords:
							cellMinLongitude = coords[2]
							cellMaxLongitude = coords[3]
							cellMinLatitude = coords[0]
							cellMaxLatitude = coords[1]
							resultCount =self.GBIFSPECIFIC.GETCOUNT(taxon_name,cellMinLatitude,cellMaxLatitude,cellMinLongitude,cellMaxLongitude)
							#check if cell fits: if not divide into centicells
							print "stage 3"
							if resultCount >1000:
								newCoords = self.SUBDIVIDECOL(cellMinLatitude,cellMaxLatitude,cellMinLongitude,cellMaxLongitude)
								for coords in newCoords:
									ccellMinLongitude = coords[2]
									ccellMaxLongitude = coords[3]
									ccellMinLatitude = coords[0]
									ccellMaxLatitude = coords[1]
									resultCount =self.GBIFSPECIFIC.GETCOUNT(taxon_name,ccellMinLatitude,ccellMaxLatitude,ccellMinLongitude,ccellMaxLongitude)
									print "stage 4"
									if resultCount>1000:
										wx.MessageBox("Smallest Gradient not sufficient.")
									#centicells worked
									else:
										self.m_Progress.WriteText("Latitude: %0.2f : %0.2f\tLongitude: %0.2f : %0.2f\t |" % (ccellMinLatitude,ccellMaxLatitude,ccellMinLongitude,ccellMaxLongitude))
										url="http://data.gbif.org/ws/rest/occurrence/list?taxonconceptkey=%d&maxlatitude=%d&minlatitude=%d&maxlongitude=%d&minlongitude=%d" %(cID,ccellMaxLatitude,ccellMinLatitude,ccellMaxLongitude,ccellMinLongitude)
										try:
											response=urllib2.urlopen(url).read()
										except urllob2.URLError:
											self.m_Progress.WriteText("%s\n" % e.code)
											wx.MessageBox("The server is temporarily unreachable.\nPlease try again later.")
											self.Close()
										parser=minidom.parseString(response)
										description+=self.GETRIGHTS(parser)
										temper=parser.getElementsByTagName("to:TaxonOccurrence")
										nodeList.extend(temper)
										self.m_Progress.WriteText("%d records found\n" % len(temper))
							
							#cells worked
							else:
								self.m_Progress.WriteText("Latitude: %0.2f : %0.2f\tLongitude: %0.2f : %0.2f\t |" % (cellMinLatitude,cellMaxLatitude,cellMinLongitude,cellMaxLongitude))
								url="http://data.gbif.org/ws/rest/occurrence/list?taxonconceptkey=%d&maxlatitude=%d&minlatitude=%d&maxlongitude=%d&minlongitude=%d" %(cID,cellMaxLatitude,cellMinLatitude,cellMaxLongitude,cellMinLongitude)
								try:
									response=urllib2.urlopen(url).read()
								except urllob2.URLError:
									self.m_Progress.WriteText("%s\n" % e.code)
									wx.MessageBox("The server is temporarily unreachable.\nPlease try again later.")
									self.Close()
								parser=minidom.parseString(response)
								description+=self.GETRIGHTS(parser)
								temper=parser.getElementsByTagName("to:TaxonOccurrence")
								nodeList.extend(temper)
								self.m_Progress.WriteText("%d records found\n" % len(temper))
					#cols worked
					else:
						self.m_Progress.WriteText("Latitude: %0.2f : %0.2f\tLongitude: %0.2f : %0.2f\t |" % (colMinLatitude,colMaxLatitude,colMinLongitude,colMaxLongitude))
						url="http://data.gbif.org/ws/rest/occurrence/list?taxonconceptkey=%d&maxlatitude=%d&minlatitude=%d&maxlongitude=%d&minlongitude=%d" %(cID,colMaxLatitude,colMinLatitude,colMaxLongitude,colMinLongitude)
						try:
							response=urllib2.urlopen(url).read()
						except urllob2.URLError:
							self.m_Progress.WriteText("%s\n" % e.code)
							wx.MessageBox("The server is temporarily unreachable.\nPlease try again later.")
							self.Close()
						parser=minidom.parseString(response)
						description+=self.GETRIGHTS(parser)
						temp=parser.getElementsByTagName("to:TaxonOccurrence")
						self.m_Progress.WriteText("%d records found\n" % len(temp))
						nodeList.extend(temp)
						
			#whole thing worked
			else:
				self.m_Progress.WriteText("Latitude: %0.2f : %0.2f\tLongitude: %0.2f : %0.2f\t |" % (minLatitude,maxLatitude,minLongitude,maxLongitude))
				url="http://data.gbif.org/ws/rest/occurrence/list?taxonconceptkey=%d&maxlatitude=%d&minlatitude=%d&maxlongitude=%d&minlongitude=%d" %(cID,maxLatitude,minLatitude,maxLongitude,minLongitude)
				try:
					response=urllib2.urlopen(url).read()
				except urllob2.URLError:
					self.m_Progress.WriteText("%s\n" % e.code)
					wx.MessageBox("The server is temporarily unreachable.\nPlease try again later.")
					self.Close()
				parser=minidom.parseString(response)
				description+=self.GETRIGHTS(parser)
				nodeList=parser.getElementsByTagName("to:TaxonOccurrence")
				self.m_Progress.WriteText("%d records found\n" % len(nodeList))
			if len(nodeList) > 0:
				records += len(nodeList)
			for node in nodeList:
				string = node.toprettyxml(indent=' ')
				rID=-1
				key_string = re.search('gbifKey="(\d+)"',string)
				if key_string:
					id_string=re.search('\d+',key_string.group())
					id = int(id_string.group())
					rID=id
				else:
					sys.exit("Could not find a friggin GBIF key")
				name=node.getElementsByTagName("tn:nameComplete")[0].toxml()
				name = re.sub(r'<.*?\>','',name)
				name = re.sub(r'[^A-Za-z ]+','',name)
				name = re.sub(r' *$','',name)
				genus = re.sub(r' .*','',name.lower())
				lat_tem = node.getElementsByTagName("to:decimalLatitude")[0].toxml()
				long_tem=node.getElementsByTagName("to:decimalLongitude")[0].toxml()
				fullLat = float(re.sub(r'\<.*?\>','',lat_tem))
				fullLon = float(re.sub(r'\<.*?\>','',long_tem))
				currGrid = (int(fullLat)+90)*360 + (int(fullLon) +180)
				conversions[currGrid]=	[fullLat,fullLon]
				distLocations.add((fullLat,fullLon))
				try:
					obs[currGrid][genus].extend([(rID,lat_tem,long_tem,name)])
				except KeyError:
					try:
						obs[currGrid].update({genus: [(rID,lat_tem,long_tem,name)] })
					except KeyError:
						obs[currGrid] = {genus: [(rID,lat_tem,long_tem,name)] }
		return(obs,conversions,records,len(distLocations),description)
'''
