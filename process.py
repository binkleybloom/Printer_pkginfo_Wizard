#!/usr/bin/python

"""CLI Application to streamline the creation of PKGInfo files for printer deployment in Munki. 
Created by Tim Schutt for Syracuse University, 2014
taschutt@syr.edu"""

import os, sys, subprocess, shlex, string, re
from optparse import Option

printers = []
selectedPrinter = ""
DeviceURI = ""
SelectedPPD = ""
PrinterDriver = ""
OptionList = []

def fnPrintCurrentState():
    os.system('clear')
    print "=============================\n"
    print "Selected Printer     :", Printer
    
    if (DeviceURI):
        print "Printer URI          :", DeviceURI
        print "Printer Make & Model :", PrinterMakeModel
        print "Printer Location     :", PrinterLocation
        
    if (DeviceURI[:6] == "smb://"):
        print "\nPrinter Connection   : Active Directory Queue"
        print "Print Server         :", PrintServer
        print "Printer Queue        :", PrinterQueue
    else:
        print "\nPrinter Connection   : Direct"
    
    if (SelectedPPD):
        print "\nPPD Selected         :", SelectedPPD
        
    if (PrinterDriver):
        print "Selected Drivers     :", PrinterDriver
            
    if (OptionList):
        x = False
        print "\nSelected Options     :",
        
        for eachoption in OptionList:
            if (x):
                print "                     :", eachoption
            else:
                print eachoption
                x = True
                
    print "\n=============================\n"

def fnGetConfiguredPrinter():
    if (len(printers) > 0):
        del printers [:]
        
    listPrintersCMD = ['/usr/bin/lpstat', '-p']    
    listPrinters = subprocess.Popen(listPrintersCMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (printersList, errorBucket) = listPrinters.communicate()
    
    for printerLine in printersList.split('\n'):
        if printerLine.count(' ') > 1:
            printerElements = printerLine.split()
            printers.append(printerElements.pop(1))
    
    fnChooseConfiguredPrinter(printers)



def fnChooseConfiguredPrinter(printers):
    os.system("clear")
    
    print "\tPlease select the printer you wish to deploy.\n"
    
    for prnIndex, printer in enumerate(printers):
        print '\t[', prnIndex, ']', printer            
    
    printerSelection = raw_input('\n\n\tChoice: ')
    
    ### check input here ###
    
    os.system("clear")
    fnPrnSelVerify(printers[int(printerSelection)])
   
   
def fnPrnSelVerify(selectedPrinter):

    print '\n\tYou selected: ', selectedPrinter, "\n\n"
    
    x = raw_input("\tIs this correct? [y or n]: ")
    
    
    if str(x) is "n":
        fnChooseConfiguredPrinter(printers)
    elif str(x) is "y":
        global Printer
        Printer = selectedPrinter
    else:
        os.system('clear')
        print "I'm sorry, I didn't understand that."

        fnPrnSelVerify(selectedPrinter)


def fnGetDeviceOptions(SelPrinter):
    cmdGetURI = ['/usr/bin/lpoptions', '-p', SelPrinter]
    processGetURI = subprocess.Popen(cmdGetURI, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (options, errorbucket) = processGetURI.communicate()
    optionsRawList = shlex.split(options)
    
    print optionsRawList
    
    OptionsList = {}
    
#    for ov in optionsRawList:
#        print ov
    
    for ov in optionsRawList:
        if "=" in ov:
            ovDictLoad = string.split(ov, "=")
            OptionsList[ovDictLoad[0]] = str(ovDictLoad[1])
    
    global DeviceURI 
    DeviceURI = OptionsList['device-uri']
    global PrinterMakeModel 
    PrinterMakeModel = OptionsList['printer-make-and-model']
    global PrinterLocation
    PrinterLocation = OptionsList['printer-location']
    
    if (DeviceURI[:6] == "smb://"):
        global PrintServer
        global PrinterQueue
        matched = re.match(r"(smb:\/\/[\w\-\.]+)\/(.+)", DeviceURI)
        PrintServer = matched.group(1)
        PrinterQueue = matched.group(2)


def fnChoosePPD():
    fnPrintCurrentState()
    print "What PPD would you like to use with this printer?"
    print "Enter a search term for the PPD. Usually, a model number works well when "
    print "attempting to select a PPD, so if you have an HP M401dne, try 'M401', or  "
    print "for a Canon ImageRunner Advance 6075 copier, try simply '6075'."
    
    ppdSearchTerm = raw_input('Search Term: ')
    
    if (len(ppdSearchTerm) < 1):
        fnChoosePPD()
    
    cmdPPDSearch = ['/bin/ls', '/Library/Printers/PPDs/Contents/Resources']
    processPPDSearch = subprocess.Popen(cmdPPDSearch, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (ppdListRaw, errorbucket) = processPPDSearch.communicate()
    
    ppdList = string.split(ppdListRaw, '\n')
    
    foundPPDs = []
    
    for ppd in ppdList:
        if str(ppdSearchTerm) in ppd:
            foundPPDs.append(ppd)
            
    fnPrintCurrentState()
    
    if (len(foundPPDs) < 1):
        print "I'm sorry - I couldn't find anything."
        print "Do you have the drivers installed on this system?"
        junk = raw_input("Press [Enter] to retry.")
        fnChoosePPD()
    else:  
        print "I found the following PPDs that might work - enter the number"
        print "of the one you would like to use, or '9999' to search again."  
        for ppdIndex, ppdSuggest in enumerate(foundPPDs):
            print "[",ppdIndex,"] -", ppdSuggest
        print "[ 9999 ] - Search Again\n"
        print "# of found PPDs:", len(foundPPDs)
        
        ppdSelectIndex = int(raw_input('Selection: '))
        
        if ppdSelectIndex == "9999":
            print "OK - restarting search"
            fnChoosePPD()
        elif (ppdSelectIndex >= 0) & (ppdSelectIndex < int(len(foundPPDs))):
            global SelectedPPD
            SelectedPPD = foundPPDs[int(ppdSelectIndex)]
            print "You selected ", SelectedPPD
        else:
            print "!!! ERROR, Will Robinson - I don't have that in my list !!!\n\n"
            fnChoosePPD()
 
def fnSetPackageDependancy():
    printerStyles = ["Hewlett Packard", "Canon - Commercial Copiers", 'Canon - Consumer Printers', 'Lexmark', 'Epson']
    driverSets = ['HewlettPackardPrinterDrivers','Canon_UFR_II_Installer','CanonPrinterDrivers','LexmarkPrinterDrivers','EPSONPrinterDrivers']
    
    print "These are the driver sets available in the Munki repository."
    print "Please select which set is required by this printer, or if"
    print "you will install the drivers by hand."
    
    for dI, dV in enumerate(printerStyles):
        print '[',dI,'] -', dV
    
    print "[9999] - No Dependency, will install by hand."
    
    driverSelect = int(raw_input('Selection: '))
    
    if (driverSelect == 9999):
        global PrinterDriver
        PrinterDriver = ''
    elif ((driverSelect >= 0) & (driverSelect < len(driverSets))):
        global PrinterDriver
        PrinterDriver = driverSets[driverSelect]
    else:
        print "I'm sorry, I didn't understand that input. Please try again"
        fnSetPackageDependancy()
    
def fnSetPrinterOptions():
    cmdGetOpts = ['lpoptions', '-p', Printer, '-l']
    processGetOpts = subprocess.Popen(cmdGetOpts, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (resultGetOpts, errorbucket) = processGetOpts.communicate()
    
    resultLinesGetOpts = string.split(resultGetOpts, '\n')
    
    global OptionList
    OptionList = []
    printerOptionsDict = {}
    printerOptions = []

    for option in resultLinesGetOpts:
        if len(option) > 3:
            optionSet = string.split(option, ':')
            tempKey = optionSet[0]
            tOK = string.split(tempKey, "/")
            oK = tOK[0]
            query = re.compile('\*\w+')
            optResult = query.findall(optionSet[1])
            oV = optResult[0]
            printerOptionsDict[oK] = oV    

    for key, stuff in printerOptionsDict.iteritems():
        printerOptions.append(key + "=" + stuff[1:])
        
    for number, option in enumerate(printerOptions):
        print "[", number, "] ", option
        
    optionSelect = str(raw_input('Please enter the options you would like to include, separated by commas. : '))
    
    for selection in string.split(optionSelect, ','):
        OptionList.append(printerOptions[int(selection)])
        
    if (DeviceURI[0:6] == "smb://"):
        OptionList.append('printer-is-shared=False')
        OptionList.append('printer-error-policy=abort-job')
        OptionList.append('printer-op-policy=authenticated')
        
def fnVerifySelections(retry):
    
    if (retry):
        print "\tI'm sorry, I didn't understand that response.\n\tPlease enter 'y' or 'n'."
    
    verified = str(raw_input('\tAre these settings correct? [y/n]: '))
    
    if verified == 'y':
        fnSetPKGINFOName()
    elif verified == 'n':
        printerSelection = fnGetConfiguredPrinter()
    else:
        fnPrintCurrentState()
        fnVerifySelections(True)
    
def fnSetPKGINFOName():
    
    print ""



def fnSetPKGINFOVersion():
    
    print ""
 
#### Call the functions in order ####
    
printerSelection = fnGetConfiguredPrinter()
fnPrintCurrentState()
fnGetDeviceOptions(Printer)
fnPrintCurrentState()
fnChoosePPD()
fnPrintCurrentState()
fnSetPackageDependancy()
fnPrintCurrentState()
fnSetPrinterOptions()
fnPrintCurrentState()
fnVerifySelections(False)