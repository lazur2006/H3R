'''
Created on 18.07.2021

@author: kai
'''

import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QWidget, QLineEdit, QTableWidgetItem, QPushButton, QAbstractScrollArea, QCheckBox, QMenu, QMenuBar, qApp
from TableModel import TableModel_
from numpy import array, ones, zeros
from Init import LoadData
from Correlation import GetCorrelation
from CreateShoppingCart import CreateShoppingCart
import re
from Search import SearchRecipes
from picnic import searchPicnicItem, putOrder, doLogin, setPicnicItem
from pandas.core import index
from future.builtins.misc import round
from pdf import create
from popup import TranslucentWidget
from ReweApi import put_order
from GetNewRecipes import Update
from PyQt5.uic.Compiler.qtproxies import QtCore, QtWidgets
import subprocess
import platform


IMG_FOLDER_LOCALE=["img/de-DE/","img/de-DE/","img/en-US/"]

# class WorkerThread_FindCallback(QtCore.QThread):
#     def run(self):
#         Find_Callback()
class WorkerThread_searchPicnicCallback(QThread):    
    def __init__(self):
        super(WorkerThread_searchPicnicCallback, self).__init__()
        
    def run(self):
        global picnicResult
        global items
        items = searchPicnicItem(shoppingCart)
        picnicResult = setPicnicItem(items)        
        
# class WorkerThread_putOrderCallback(QtCore.QThread):
#     def run(self):
#         putOrder_Callback()
# class WorkerThread_CreatePdfFileCallback(QtCore.QThread):
#     def run(self):
#         CreatePdfFile_Callback()
# class WorkerThread_SimplifyIngredientsCallback(QtCore.QThread):
#     def run(self):
#         SimplifyIngredients_Callback()     
# class WorkerThread_searchREWE_Callback(QtCore.QThread):
#     def run(self):
#         searchREWE_Callback()   
# class WorkerThread_ShowRecipes_Callback(QtCore.QThread):
#     def run(self):
#         ShowRecipes_Callback()  
        
     
class MainH3R(QWidget):
    def __init__(self):
        super(MainH3R, self).__init__()
        
        loadUi("bin/form.ui",self)
        self.setWindowIcon(QIcon('app.ico'))
        
        
        global results
        global MarkedToBasket
        global CntRecipe
        global iList
        global LOCALE_IDX
        global correlationFactor
        global DataPackage
        global shoppingCart
        global picnicResult
        global orderSelected
        global actItemIndex
        global items
        global status
        global Recipe_ActualNum
        
        # self.myQMenuBar = QMenuBar(self)
        #
        # Menu_Search = self.myQMenuBar.addMenu('Search')
        # Menu_Session = self.myQMenuBar.addMenu('Session')
        #
        # Action_IngredientSearch = QAction('Ingredient Search', self)        
        # Action_IngredientSearch.triggered.connect(qApp.quit)
        # Menu_Search.addAction(Action_IngredientSearch)
        #
        # Action_SaveSession = QAction('Save Session', self)        
        # Action_SaveSession.triggered.connect(qApp.quit)
        # Menu_Session.addAction(Action_SaveSession)
        
        
        
        
        
        # pixmap = QPixmap("H3RMockup.png")
        # self.LOGO.setPixmap(pixmap.scaled(100, 50, Qt.KeepAspectRatio))
        
        
        self.thread=WorkerThread_searchPicnicCallback()
        self.thread.finished.connect(self.StopWaitState)
        self.thread.finished.connect(self.updatePicnicTable)
        
        #Connect UI objects to function defs
        self.SearchInput.textChanged.connect(self.SearchInput_Callback)
        self.Clear.clicked.connect(self.Clear_Callback)
        self.SelectIngredientsList.itemClicked.connect(self.SelectIngredientsList_Callback)
        self.SelectedItemsList.itemClicked.connect(self.SelectedItemsList_Callback)
        self.Find.clicked.connect(self.Find_Callback)#(lambda: handleThreads(Find_Callback))
        self.DeleteSelection.clicked.connect(self.DeleteSelection_Callback)
        self.ShowRecipes.clicked.connect(lambda: self.ShowRecipes_Callback(0))#(lambda: self.handleThreads(self.ShowRecipes_Callback))
        self.GenShoppingList.clicked.connect(self.GenShoppingList_Callback)
        self.Next.clicked.connect(self.Next_Callback)
        self.Previous.clicked.connect(self.Previous_Callback)
        self.AddToBasket.stateChanged.connect(self.AddToBasket_Callback)
        #-----
        self.searchPicnic.clicked.connect(self.handleThreads)
        #-----
        self.clearPicnic.clicked.connect(self.clearPicnic_Callback)
        self.putOrder.clicked.connect(self.putOrder_Callback)#(lambda: self.handleThreads(self.putOrder_Callback))
        self.saveLoginData.clicked.connect(self.saveLoginData_Callback)
        self.numCorrelation.valueChanged.connect(self.numCorrelation_Callback)
        self.ShowRndSeed.stateChanged.connect(self.ShowRndSeed_Callback)
        self.ShowRecipeNum.stateChanged.connect(self.ShowRecipeNum_Callback)
        #self.SimplifyIngredients.stateChanged.connect(self.SimplifyIngredients_Callback)#(lambda: self.handleThreads(self.SimplifyIngredients_Callback))
        self.CreatePdfFile.clicked.connect(self.CreatePdfFile_Callback)#(lambda: handleThreads(CreatePdfFile_Callback))
        self.searchREWE.clicked.connect(self.searchREWE_Callback)#(lambda: self.handleThreads(self.searchREWE_Callback))
        self.CallUpdater.clicked.connect(self.updater_Callback)
        self.rbGerman.toggled.connect(lambda: self.LOCALE_Callback(0))
        self.rbGermanS.toggled.connect(lambda: self.LOCALE_Callback(1))
        self.rbUsa.toggled.connect(lambda: self.LOCALE_Callback(2))
        self.SetActToSeed.clicked.connect(self.SetActToSeed_Callback)
        self.picnicPassword.returnPressed.connect(self.saveLoginData_Callback)
        self.Help.clicked.connect(self.Help_Callback)
        
        self.RecipeGroupType.setStyleSheet("background-color: black;"
                                           "color: white;"
                                           "padding: 2px;"
                                           "font-weight: bold;"
                                           "border-radius : 5px")
        
        
        self.NameContainer.setStyleSheet("background-color: #f2f2f2;"
                                          "border-radius : 5px")
        self.IwantThisBanner.setStyleSheet("background-color: #f2f2f2;"
                                           "border-radius : 5px")
        self.RecipeModeContainer.setStyleSheet("background-color: #f2f2f2;"
                                           "border-radius : 5px")
        
        
        LOCALE_IDX = 1
        Recipe_ActualNum = 0
        
        DataPackage = LoadData(LOCALE_IDX)
        iList=DataPackage[5]
        self.SelectIngredientsList.addItems(iList)
        
        results = GetCorrelation([DataPackage,9,Recipe_ActualNum],LOCALE_IDX)
        self.RecipeName.setText(results[0][0])
        self.RandomSeed.setText("RandSeed = " + str(results[4]))
        self.RecipeCount.setText("Recipe 1 of " + str(len(results[0])))
        self.RecipeNumber.setText("Recipe Number = " + str(results[1][0]))
        
        self.modeStatus.setText("- RANDOM RECIPE MODE -")
        
        # Load image
        pixmap = QPixmap(IMG_FOLDER_LOCALE[LOCALE_IDX] + str(results[1][0]) + ".jpg")
        self.ImageLabel.setPixmap(pixmap.scaled(1000, 500, Qt.KeepAspectRatio))
        
        # Set inital recipe counter value to one
        CntRecipe = 1
        
        MarkedToBasket = []
        shoppingCart = []
        #picnicResult = []
        self.SumCosts.setText("")
        self.searchPicnic.setEnabled(False)
        self.CreatePdfFile.setEnabled(False)
        self.searchREWE.setEnabled(False)
        
        self.picnicPassword.setEchoMode(QLineEdit.Password)
        self.picnicLoginStatus.setText("")
        
        correlationFactor = 9
        
        status = False
        self.RandomSeed.setVisible(False)
        self.RecipeNumber.setVisible(False)
        self.putOrder.setEnabled(False)
        
        self.mode.setVisible(False)
        
        self.picnicGroup.setEnabled(False)
        self.picnicHint.setEnabled(False)
        self.picnicNoMatchList.setEnabled(False)
        self.clearPicnic.setEnabled(False)
        self.picnicMakeYourOrder.setEnabled(False)
                
        self._popframe = None
        self._popflag = False
        
        self.setTags()
        
        self.resize(int(QApplication.desktop().size().width()*0.75),int(QApplication.desktop().size().height()*0.8))
    def setTags(self):
        global results
        global DataPackage
        
        tags=DataPackage[7][results[1][CntRecipe - 1]]
        if any(tags):
            for item in tags:
                self.RecipeGroupType.setVisible(True)
                self.RecipeGroupType.setText(item)
        else:
            self.RecipeGroupType.setVisible(False)
            self.RecipeGroupType.setText("")
            
        self.headline.setText(DataPackage[8][results[1][CntRecipe - 1]][0])
        
    def Help_Callback(self):
        #os.system(os.getcwd()+"/"+path)
        
        path = 'Help.pdf'
        
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', path))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(path)
        else:                                   # linux variants
            subprocess.call(('xdg-open', path))
        
    def _createMenuBar(self):
        menuBar = self.menuBar()
        
    def SetActToSeed_Callback(self):
        self.mode.setText(results[0][CntRecipe - 1])
        self.ShowRecipes_Callback(results[1][CntRecipe - 1])
        self.modeStatus.setText("- SPECIFIC RECIPE MODE -")
        self.mode.setVisible(True)
        
        
    def updatePicnicTable(self):
        global actItemIndex
        global orderSelected
        
        self.picnicGroup.setEnabled(True)
        self.picnicHint.setEnabled(True)
        self.picnicNoMatchList.setEnabled(True)
        self.clearPicnic.setEnabled(True)
        self.picnicMakeYourOrder.setEnabled(True)
        
        var = picnicResult[0]
        
        orderSelected = ones(len(var), dtype=bool)
        actItemIndex = zeros(len(var), dtype=int)
    
        self.picnicTable.setColumnCount(6)
        self.picnicTable.setRowCount(len(var))
        
        self.picnicTable.setHorizontalHeaderLabels(['Ingredient (original)', 'Price', 'Amount (necessary)', 'Order', 'Previous', 'Next'])
        
        for row in range(len(var)):
            self.chkBoxItem = QTableWidgetItem(row)
            self.chkBoxItem.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            self.chkBoxItem.setCheckState(Qt.Checked)
            
            self.NextBtnItem = QPushButton('>>')
            self.NextBtnItem.clicked.connect(self.handleButtonClicked)
            self.picnicTable.setCellWidget(row, 5, self.NextBtnItem)
    
            self.PreviousBtnItem = QPushButton('<<')
            self.PreviousBtnItem.clicked.connect(self.handleButtonClicked)
            self.picnicTable.setCellWidget(row, 4, self.PreviousBtnItem)
            
            self.chkBox = QCheckBox("")
            self.chkBox.setChecked(True)
            self.chkBox.stateChanged.connect(self.handleCheckbox)
            self.picnicTable.setCellWidget(row, 3, self.chkBox)
            
            self.picnicTable.setItem(row, 0, QTableWidgetItem(str(var[row][0])))
            self.picnicTable.setItem(row, 1, QTableWidgetItem(str(var[row][1])))
            self.picnicTable.setItem(row, 2, QTableWidgetItem(str(var[row][2])))
            
            if picnicResult[4][row]:
                self.picnicTable.item(row, 2).setBackground(QColor(214, 117, 117))
        
    
        self.picnicTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.picnicTable.resizeColumnsToContents()
        
        
        self.picnicNoMatchList.addItems(items[1])
        
        self.SumCosts.setText("summarized costs " + picnicResult[2] + " €")
        
        self.tabWidget.setCurrentIndex(2)
        self.putOrder.setEnabled(True)
           
    def ResetGui(self):
        global results
        global MarkedToBasket
        global CntRecipe
        # reset all settings
        results = []
        MarkedToBasket = []
        CntRecipe = 1
        self.AddToBasket.setChecked(False)
        model = TableModel_([''], ['Amount', 'Unit', 'Ingredient'])
        self.ShoppingListTable.setModel(model)
        self.ShoppingListTable.resizeColumnsToContents()
        self.GenShoppingList.setEnabled(False)
        self.searchPicnic.setEnabled(False)
        self.SelectedRecipesList.clear()
        self.CreatePdfFile.setEnabled(False)
        self.searchREWE.setEnabled(False)
    
    # Function defs  
    def SearchInput_Callback(self):
        global iList
        self.SelectIngredientsList.clear()
        i = 0
        
        while i < len(iList):
            if re.findall(self.SearchInput.text(), iList[i], flags=re.IGNORECASE) != []:
                self.SelectIngredientsList.addItem(iList[i])
            i += 1
       
    def Clear_Callback(self):
        self.SearchInput.clear()
    
    def SelectIngredientsList_Callback(self,item):
        #self.RecipeName.setText(item.text())
        self.SelectedItemsList.addItem(item.text())
        
        if self.SelectedItemsList.count() < 1:
            self.Find.setEnabled(False)
        else:
            self.Find.setEnabled(True)
    
    def SelectedItemsList_Callback(self,item):
        self.SelectedItemsList.takeItem(self.SelectedItemsList.currentRow())
        
        if self.SelectedItemsList.count() < 1:
            self.Find.setEnabled(False)
        else:
            self.Find.setEnabled(True)
    
    def Find_Callback(self):
        global results
        global MarkedToBasket
        global CntRecipe
        global LOCALE_IDX
        items = []
        ret = []
        
        self.ResetGui()
        
        for index in range(self.SelectedItemsList.count()):
            items.append(self.SelectedItemsList.item(index))
            ret.append(items[index].text())
        
        results = SearchRecipes([ret, DataPackage])
        self.RecipeName.setText(results[0][0])
        self.RecipeNumber.setText("Recipe Number = " + str(results[1][0]))
    
        self.RecipeCount.setText("Recipe 1 of " + str(len(results[0])))
        
        self.setTags()
        
        # Load image
        pixmap = QPixmap(IMG_FOLDER_LOCALE[LOCALE_IDX] + str(results[1][0]) + ".jpg")
        self.ImageLabel.setPixmap(pixmap.scaled(1000, 500, Qt.KeepAspectRatio))
        self.tabWidget.setCurrentIndex(0)
        
    def DeleteSelection_Callback(self):
        self.SelectedItemsList.clear()
        self.Find.setEnabled(False)
        
    def ShowRecipes_Callback(self,seed):
        global results
        global CntRecipe
        global MarkedToBasket
        global correlationFactor
        global DataPackage
        global LOCALE_IDX
        self.AddToBasket.setChecked(False)
        MarkedToBasket = []
        CntRecipe = 1
        # RecipeName.setText("ShowRecipes_Callback")
        results = GetCorrelation([DataPackage,correlationFactor,seed],LOCALE_IDX)
        self.RecipeName.setText(results[0][0])
        self.RecipeNumber.setText("Recipe Number = " + str(results[1][0]))
        self.RandomSeed.setText("RandSeed = " + str(results[4]))
        self.RecipeCount.setText("Recipe 1 of " + str(len(results[0])))
        self.modeStatus.setText("- RANDOM RECIPE MODE -")
        self.mode.setVisible(False)
        
        self.setTags()
        
        # Load image
        pixmap = QPixmap(IMG_FOLDER_LOCALE[LOCALE_IDX] + str(results[1][0]) + ".jpg")
        self.ImageLabel.setPixmap(pixmap.scaled(1000, 500, Qt.KeepAspectRatio))
        
    def GenShoppingList_Callback(self):
        global results
        global shoppingCart
        global MarkedToBasket        
        #ind = array(MarkedToBasket) - 1
        # print(results[0][ind.astype(int)])
        shoppingCart = CreateShoppingCart(results[2][array(MarkedToBasket) - 1])
        # Load data to shopping list
        var = shoppingCart
        
        for list in var:
            list[1]=list[1][0:3]

        model = TableModel_(var, ['Amount', 'Unit', 'Ingredient'])
        self.ShoppingListTable.setModel(model)
        self.ShoppingListTable.resizeColumnsToContents()
        
        if not shoppingCart:
            self.searchPicnic.setEnabled(False)
            self.CreatePdfFile.setEnabled(False)
            self.searchREWE.setEnabled(False)
        else:
            self.CreatePdfFile.setEnabled(True)
            self.searchREWE.setEnabled(True)
            if status:
                self.searchPicnic.setEnabled(True)
                 
    def Next_Callback(self):
        global results
        global CntRecipe
        global MarkedToBasket
        global LOCALE_IDX
        
        MaxValue = len(results[0])
        if CntRecipe < MaxValue:
            CntRecipe = CntRecipe + 1;
        self.RecipeCount.setText("Recipe "+ str(CntRecipe) + " of " + str(MaxValue))
        self.RecipeName.setText(results[0][CntRecipe - 1])
        self.RecipeNumber.setText("Recipe Number = " + str(results[1][CntRecipe - 1]))
        
        self.setTags()
        
        # Load image
        pixmap = QPixmap(IMG_FOLDER_LOCALE[LOCALE_IDX] + str(results[1][CntRecipe - 1]) + ".jpg")
        self.ImageLabel.setPixmap(pixmap.scaled(1000, 500, Qt.KeepAspectRatio))
        
        if CntRecipe in MarkedToBasket:
            self.AddToBasket.setChecked(True)
        else:
            self.AddToBasket.setChecked(False)
        
    def Previous_Callback(self):
        global results
        global CntRecipe
        global MarkedToBasket
        global LOCALE_IDX
            
        MaxValue = len(results[0])
        if CntRecipe > 1:
            CntRecipe = CntRecipe - 1;
        self.RecipeCount.setText("Recipe "+ str(CntRecipe) + " of " + str(MaxValue))
        self.RecipeName.setText(results[0][CntRecipe - 1])
        self.RecipeNumber.setText("Recipe Number = " + str(results[1][CntRecipe - 1]))
        
        self.setTags()
        
        # Load image
        pixmap = QPixmap(IMG_FOLDER_LOCALE[LOCALE_IDX] + str(results[1][CntRecipe - 1]) + ".jpg")
        self.ImageLabel.setPixmap(pixmap.scaled(1000, 500, Qt.KeepAspectRatio))
        
        if CntRecipe in MarkedToBasket:
            self.AddToBasket.setChecked(True)
        else:
            self.AddToBasket.setChecked(False)
    
    def AddToBasket_Callback(self):
        global CntRecipe
        global MarkedToBasket
        global results
        if self.AddToBasket.isChecked():
            if CntRecipe in MarkedToBasket:
                pass
            else:
                MarkedToBasket.append(CntRecipe)
                # print(MarkedToBasket)
        else:
            try:
                MarkedToBasket.pop(MarkedToBasket.index(CntRecipe))
                # print(MarkedToBasket)
            except:
                pass
        self.SelectedRecipesList.clear()
        for i in range(len(MarkedToBasket)):
            self.SelectedRecipesList.addItem(results[0][MarkedToBasket[i] - 1])
        if not MarkedToBasket:
            self.GenShoppingList.setEnabled(False)
        else:
            self.GenShoppingList.setEnabled(True)
      

    
    def handleButtonClicked(self):
        global items
        global actItemIndex
        global orderSelected
        button = self.sender()
        index = self.picnicTable.indexAt(button.pos())
        
        if index.isValid():
            if button.text() == '>>':
                #print("Next: " + str(index.row()))
                if actItemIndex[index.row()] < len(items[0][index.row()])-2:
                    actItemIndex[index.row()] = actItemIndex[index.row()] + 1
            else:
                if actItemIndex[index.row()] > 0:
                    actItemIndex[index.row()] = actItemIndex[index.row()] - 1
                #print("Prev: " + str(index.row()))
            picnicResult[0][index.row()][0] = items[0][index.row()][actItemIndex[index.row()]]['name']
            try:
                picnicResult[0][index.row()][1] = items[0][index.row()][actItemIndex[index.row()]]['price'] / 100
            except:
                picnicResult[0][index.row()][1] = items[0][index.row()][actItemIndex[index.row()]]['display_price'] / 100
            picnicResult[0][index.row()][2] = items[0][index.row()][actItemIndex[index.row()]]['unit_quantity']
            picnicResult[0][index.row()][3] = items[0][index.row()][actItemIndex[index.row()]]['id']
            self.picnicTable.setItem(index.row(), 0, QTableWidgetItem(str(picnicResult[0][index.row()][0] + " (" + items[2][index.row()][2] + ")")))
            self.picnicTable.setItem(index.row(), 1, QTableWidgetItem(str(picnicResult[0][index.row()][1]) + " €"))
            self.picnicTable.setItem(index.row(), 2, QTableWidgetItem(str(picnicResult[0][index.row()][2]) + " (" + str(items[2][index.row()][0]) + " " + str(items[2][index.row()][1]) + ")"))
            
            sumCosts = 0
            for i in range(len(orderSelected)):
                if orderSelected[i] == True:
                    sumCosts = sumCosts + float(re.sub(" €","",self.picnicTable.item(i,1).text()))
            self.SumCosts.setText("summarized costs " + str(round(sumCosts,2)) + " €")
                 
    def handleCheckbox(self):
        global orderSelected
        chkBox = self.sender()
        index = self.picnicTable.indexAt(chkBox.pos())
        if index.isValid():
            if chkBox.checkState() == 2:
                #print("Checked: " + str(index.row()))
                orderSelected[index.row()] = True
            else:
                #print("Unchecked: " + str(index.row()))
                orderSelected[index.row()] = False
                
            sumCosts = 0
            for i in range(len(orderSelected)):
                if orderSelected[i] == True:
                    sumCosts = sumCosts + float(re.sub(" €","",self.picnicTable.item(i,1).text()))
            self.SumCosts.setText("summarized costs " + str(round(sumCosts,2)) + " €")
                
    def clearPicnic_Callback(self):
        self.picnicNoMatchList.clear()
        self.picnicTable.clear()
        self.putOrder.setEnabled(False)
        self.SumCosts.setText("")
        
    def putOrder_Callback(self):
        global picnicResult
        global orderSelected
        putOrder(array(picnicResult[0])[[i for i, val in enumerate(orderSelected) if val]])
        
    def saveLoginData_Callback(self):
        global status
        global shoppingCart
        status = doLogin([self.picnicEmail.text(), self.picnicPassword.text()])
        
        if status:
            self.picnicLoginStatus.setText("Login successfully")
            if not shoppingCart:
                self.searchPicnic.setEnabled(False)
                self.CreatePdfFile.setEnabled(False)
            else:
                if status:
                    self.searchPicnic.setEnabled(True)
        else:
            self.picnicLoginStatus.setText("Bad login data")
            
    def numCorrelation_Callback(self):
        global correlationFactor
        correlationFactor = self.numCorrelation.value()
        
    def ShowRndSeed_Callback(self):
        if self.ShowRndSeed.isChecked():
            self.RandomSeed.setVisible(True)
        else:
            self.RandomSeed.setVisible(False)
            
    def ShowRecipeNum_Callback(self):
        if self.ShowRecipeNum.isChecked():
            self.RecipeNumber.setVisible(True)
        else:
            self.RecipeNumber.setVisible(False)
            
    def SimplifyIngredients_Callback(self):
        global iList
        global results
        global DataPackage
        global LOCALE_IDX
    
        DataPackage = LoadData(LOCALE_IDX)
        iList=DataPackage[5]
        self.SelectIngredientsList.addItems(iList)
    
        self.ResetGui()
        iList = DataPackage[5][1:]
        iList.sort()
        self.SelectIngredientsList.clear()
        self.SelectIngredientsList.addItems(iList)
        results = GetCorrelation([DataPackage,correlationFactor,Recipe_ActualNum],LOCALE_IDX)
        self.RecipeName.setText(results[0][0])
        self.RandomSeed.setText("RandSeed = " + str(results[4]))
        self.RecipeCount.setText("Recipe 1 of " + str(len(results[0])))
        self.RecipeNumber.setText("Recipe Number = " + str(results[1][0]))
        #self.modeStatus.setText("- RANDOM RECIPE "+ str(results[4]) +" -")
        self.modeStatus.setText("- RANDOM RECIPE MODE -")
        self.mode.setVisible(False)
        
        self.setTags()
        
        # Load image
        pixmap = QPixmap(IMG_FOLDER_LOCALE[LOCALE_IDX] + str(results[1][0]) + ".jpg")
        self.ImageLabel.setPixmap(pixmap.scaled(1000, 500, Qt.KeepAspectRatio))
    
    def CreatePdfFile_Callback(self):
        global shoppingCart
        global LOCALE_IDX
        create([results,array(MarkedToBasket) - 1,shoppingCart],IMG_FOLDER_LOCALE[LOCALE_IDX],self.sender())
    
    def StartWaitState(self):
        self._popframe = TranslucentWidget(self)
        self._popframe.move(0, 0)
        self._popframe.resize(self.width(), self.height())
        self._popflag = True
        self._popframe.show()
        
    def StopWaitState(self):
        self._popframe.close()
        self._popflag = False
        
    def handleThreads(self):

        print("step0")
 
        self.StartWaitState()
        self.thread.start()
        
    def searchREWE_Callback(self):
        global shoppingCart
        
        reAr = []
        for i in range(len(shoppingCart)):
            reAr.append(shoppingCart[i][0] + " " + shoppingCart[i][1] + " " + shoppingCart[i][2])
        put_order(reAr)
        
    def updater_Callback(self):    
        #print("Test")   
        self.dialog = Update()
        self.dialog.show()
        
    def LOCALE_Callback(self,LOCALE):
        global LOCALE_IDX
        LOCALE_IDX=LOCALE
        self.ResetGui()
        self.SimplifyIngredients_Callback()
        
    # def resizeEvent(sender, event: QResizeEvent):
    #     print("Resize")
    
    def resizeEvent(self, event):
        print("resize")
        
        try:
            self._popframe.resize(self.width(), self.height())
        except:
            #nada
            print("nada")
        
        # Load image
        # pixmap = QPixmap(IMG_FOLDER_LOCALE[LOCALE_IDX] + str(results[1][0]) + ".jpg")
        # self.ImageLabel.setPixmap(pixmap.scaled(1000, 500, Qt.KeepAspectRatio))
        # #QtGui.QMainWindow.resizeEvent(self, event)
    

app = QApplication(sys.argv)
a = MainH3R()
a.show()
sys.exit(app.exec_())    
