# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Sep  8 2010)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx

###########################################################################
## Class GBIFQueryLayout
###########################################################################

class GBIFQueryLayout ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"GBIF Query", pos = wx.DefaultPosition, size = wx.Size( 790,620 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
		
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		
		bSizer3.AddSpacer( ( 0, 0), 0, 0, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Query" ), wx.HORIZONTAL )
		
		self.m_TaxonName = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer2.Add( self.m_TaxonName, 1, wx.ALL, 5 )
		
		self.m_Search = wx.Button( self, wx.ID_ANY, u"Search", wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer2.Add( self.m_Search, 0, wx.ALL, 5 )
		
		bSizer3.Add( sbSizer2, 0, wx.EXPAND, 5 )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Boundries" ), wx.VERTICAL )
		
		gSizer3 = wx.GridSizer( 2, 2, 0, 0 )
		
		self.m_MinLonLabel = wx.StaticText( self, wx.ID_ANY, u"Min Longitude", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_MinLonLabel.Wrap( -1 )
		gSizer3.Add( self.m_MinLonLabel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_MinLon = wx.SpinCtrl( self, wx.ID_ANY, u"-180", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.TAB_TRAVERSAL, -180, 180, -180 )
		gSizer3.Add( self.m_MinLon, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_MaxLonLabel = wx.StaticText( self, wx.ID_ANY, u"Max Longitude", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_MaxLonLabel.Wrap( -1 )
		gSizer3.Add( self.m_MaxLonLabel, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_MaxLon = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.TAB_TRAVERSAL, -180, 180, 180 )
		gSizer3.Add( self.m_MaxLon, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"Min Latitude", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		gSizer3.Add( self.m_staticText7, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_MinLat = wx.SpinCtrl( self, wx.ID_ANY, u"-90", wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.TAB_TRAVERSAL, -90, 90, 90 )
		gSizer3.Add( self.m_MinLat, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"Max Latitude", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText8.Wrap( -1 )
		gSizer3.Add( self.m_staticText8, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		self.m_MaxLat = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS|wx.TAB_TRAVERSAL, -90, 90, 90 )
		gSizer3.Add( self.m_MaxLat, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		sbSizer4.Add( gSizer3, 1, wx.EXPAND, 5 )
		
		bSizer3.Add( sbSizer4, 0, wx.EXPAND, 5 )
		
		sbSizer8 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Progress" ), wx.HORIZONTAL )
		
		self.m_Progress = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_DONTWRAP|wx.TE_MULTILINE|wx.TE_READONLY|wx.CLIP_CHILDREN )
		sbSizer8.Add( self.m_Progress, 1, wx.ALL|wx.EXPAND, 5 )
		
		bSizer3.Add( sbSizer8, 1, wx.EXPAND, 5 )
		
		sbSizer11 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Summary" ), wx.VERTICAL )
		
		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )
		sbSizer11.Add( self.m_staticText6, 0, wx.ALL, 5 )
		
		bSizer3.Add( sbSizer11, 0, wx.EXPAND, 5 )
		
		bSizer12 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_Help = wx.Button( self, wx.ID_ANY, u"?", wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )
		bSizer12.Add( self.m_Help, 0, wx.ALL, 5 )
		
		self.m_AddData = wx.Button( self, wx.ID_ANY, u"Add Data to Map", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_AddData, 0, wx.ALL, 5 )
		
		self.m_ExportData = wx.Button( self, wx.ID_ANY, u"Export Data...", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_ExportData, 0, wx.ALL, 5 )
		
		
		bSizer12.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		bSizer3.Add( bSizer12, 0, wx.EXPAND, 5 )
		
		bSizer2.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer8 = wx.BoxSizer( wx.VERTICAL )
		
		sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Results Table" ), wx.VERTICAL )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		m_ResultChoices = []
		self.m_Result = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_ResultChoices, wx.LB_EXTENDED|wx.LB_HSCROLL )
		bSizer10.Add( self.m_Result, 1, wx.ALL|wx.EXPAND, 5 )
		
		sbSizer5.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		bSizer8.Add( sbSizer5, 1, wx.EXPAND, 5 )
		
		sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, wx.EmptyString ), wx.VERTICAL )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		
		bSizer9.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_Add = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.m_Add, 0, wx.ALL, 5 )
		
		
		bSizer9.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_Remove = wx.Button( self, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer9.Add( self.m_Remove, 0, wx.ALL, 5 )
		
		
		bSizer9.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		sbSizer6.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		bSizer8.Add( sbSizer6, 0, wx.EXPAND, 5 )
		
		sbSizer7 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"ID List" ), wx.VERTICAL )
		
		bSizer11 = wx.BoxSizer( wx.VERTICAL )
		
		m_IDListChoices = []
		self.m_IDList = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_IDListChoices, wx.LB_EXTENDED|wx.LB_HSCROLL )
		bSizer11.Add( self.m_IDList, 1, wx.ALL|wx.EXPAND, 5 )
		
		gSizer2 = wx.GridSizer( 1, 2, 0, 0 )
		
		self.m_Calc = wx.Button( self, wx.ID_ANY, u"Calc", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_Calc, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )
		
		self.m_button13 = wx.Button( self, wx.ID_ANY, u"PreCalc", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer2.Add( self.m_button13, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL, 5 )
		
		bSizer11.Add( gSizer2, 0, wx.EXPAND, 5 )
		
		sbSizer7.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		bSizer8.Add( sbSizer7, 1, wx.EXPAND, 5 )
		
		bSizer5.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		bSizer14 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button15 = wx.Button( self, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer14.Add( self.m_button15, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
		
		bSizer5.Add( bSizer14, 0, wx.EXPAND, 5 )
		
		bSizer2.Add( bSizer5, 1, wx.EXPAND, 5 )
		
		bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
		
		self.SetSizer( bSizer1 )
		self.Layout()
		self.m_statusBar1 = self.CreateStatusBar( 1, wx.ST_SIZEGRIP, wx.ID_ANY )
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.m_Search.Bind( wx.EVT_BUTTON, self.OnSearch )
		self.m_Help.Bind( wx.EVT_BUTTON, self.OnHelp )
		self.m_AddData.Bind( wx.EVT_BUTTON, self.OnAddData )
		self.m_ExportData.Bind( wx.EVT_BUTTON, self.OnExportData )
		self.m_Result.Bind( wx.EVT_LEFT_DCLICK, self.OnAdd )
		self.m_Add.Bind( wx.EVT_BUTTON, self.OnAdd )
		self.m_Remove.Bind( wx.EVT_BUTTON, self.OnRemove )
		self.m_IDList.Bind( wx.EVT_LEFT_DCLICK, self.OnRemove )
		self.m_Calc.Bind( wx.EVT_BUTTON, self.OnCalculate )
		self.m_button13.Bind( wx.EVT_BUTTON, self.OnPreCalculate )
		self.m_button15.Bind( wx.EVT_BUTTON, self.OnOK )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()
	
	def OnSearch( self, event ):
		event.Skip()
	
	def OnHelp( self, event ):
		event.Skip()
	
	def OnAddData( self, event ):
		event.Skip()
	
	def OnExportData( self, event ):
		event.Skip()
	
	def OnAdd( self, event ):
		event.Skip()
	
	
	def OnRemove( self, event ):
		event.Skip()
	
	
	def OnCalculate( self, event ):
		event.Skip()
	
	def OnPreCalculate( self, event ):
		event.Skip()
	
	def OnOK( self, event ):
		event.Skip()
	

