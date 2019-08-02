# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from PyQt5 import QtCore as QtC
from PyQt5 import QtGui as QtG
from PyQt5 import QtWidgets as QtW
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
import os, sys

def simncoins( coins, sims ):
    icoins = int(float(coins))
    isims = int(float(sims))
    
    outcome = random.rand( icoins, isims )
    tally = np.sum( outcome > 0.5 , axis = 0 ) 
    return(tally)
    
class PlotCanvas( FigureCanvas ):
    def __init__( self, parent= None ):
        self.fig = Figure( )
        
        self.axes = self.fig.add_subplot(111)
        
        FigureCanvas.__init__( self, self.fig )
        self.parent = parent
        
        FigureCanvas.updateGeometry( self )
        
    def plot( self ):
        self.icoins = int(float(self.parent.coinsEdit.text()))
        self.isims = int(float(self.parent.simsEdit.text()))
        
        self.axes.cla( )
        
        if self.icoins and self.isims != ( '' or None ):
            self.tally = simncoins( self.icoins, self.isims )
            
        self.axes.hist( self.tally, bins = self.icoins + 1, range = ( -0.5, self.icoins + 0.5 ) , rwidth = 0.75 )
        self.axes.set_title( '%a Coins and %a Simulations; O. Fox' % (self.icoins, self.isims) )
        self.axes.set_xlabel( '# of Heads' )
        self.draw( )
        
class CentralWidget( QtW.QWidget ):
    def __init__( self, parent ):
        super( CentralWidget, self).__init__( parent )
        self.initUI( )
        
    def plotHist( self ):
        if self.coinsEdit.text() and self.simsEdit.text() != ( '' or None ):
            self.tally = simncoins( self.coinsEdit.text() , self.simsEdit.text( ) )              
        self.plotWindow.plot( )
        return( self.tally )
        
    def savePlot( self ):
        namePicker = QtW.QFileDialog.getSaveFileName( self, 'Save Plot Image', filter = "*.png" )
        self.plotWindow.fig.savefig( namePicker[0] )
    
    def initUI( self ):
        
        self.coins = QtW.QLabel( 'Number of Coins' )
        self.sims = QtW.QLabel( 'Number of Simulations' )
        
        self.coinsEdit = QtW.QLineEdit( )
        self.simsEdit = QtW.QLineEdit( )
        self.intValidator = QtG.QDoubleValidator( )
        self.intValidator.setDecimals( 0 )
        self.coinsEdit.setValidator( self.intValidator )
        self.simsEdit.setValidator( self.intValidator )
        
        self.plotButton = QtW.QPushButton( 'Plot Histogram' )
        self.plotButton.clicked.connect( self.plotHist )
        
        self.saveButton = QtW.QPushButton( 'Save Plot Image' )
        self.saveButton.clicked.connect( self.savePlot )
        
        self.firstRow = QtW.QHBoxLayout( )
        self.firstRow.addWidget( self.coins )
        self.firstRow.addWidget( self.coinsEdit )
        self.firstRow.addWidget( self.plotButton )
        
        self.secondRow = QtW.QHBoxLayout( )
        self.secondRow.addWidget( self.sims )
        self.secondRow.addWidget( self.simsEdit )
        self.secondRow.addWidget( self.saveButton )
        
        self.plotWindow = PlotCanvas( self )
        
        self.mainLayout = QtW.QVBoxLayout( )
        self.mainLayout.addLayout( self.firstRow )
        self.mainLayout.addLayout( self.secondRow )
        #self.mainLayout.addStretch( 1 )
        
        self.mainLayout.addWidget( self.plotWindow )
        
        self.setLayout( self.mainLayout )
        self.show()
        
class MainGUI( QtW.QMainWindow ):
    def __init__( self ):
        super( MainGUI, self ).__init__( )
        self.initUI( )
        
    def fileQuit( self ):
        self.close( )
        
    def fileMenu( self ):
        self.fileMenu = QtW.QMenu( '&File', self)
        self.fileMenu.addAction( '&Quit', self.fileQuit, QtC.Qt.CTRL + QtC.Qt.Key_Q)
        self.menuBar( ).addMenu( self.fileMenu )
   
    def initUI( self ):
        self.setMinimumSize( 500, 500 )
        self.fileMenu( )
        
        self.mainWidget = CentralWidget( self )
        self.setCentralWidget( self.mainWidget )      
        self.show( )
        
if __name__=='__main__':
    app = 0
    app = QtW.QApplication( sys.argv )
    mg = MainGUI( )
    app.exec_( )  