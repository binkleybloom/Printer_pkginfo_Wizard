#!/usr/bin/python

"""CLI Application to streamline the creation of PKGInfo files for printer deployment in Munki. 
Created by Tim Schutt for Syracuse University, 2014
taschutt@syr.edu"""

import os, sys, subprocess, shlex, string

printers = []
selectedPrinter = ""
DeviceURI = ""
SelectedPPD = ""

def fnPrintCurrentState():
    os.system('clear')
    print "=============================\n"
    print "\n    Selected Printer:", Printer
    
    if (DeviceURI):
        print "         Printer URI:", DeviceURI
        print "Printer Make & Model:", PrinterMakeModel
        print "    Printer Location:", PrinterLocation
    
    if (SelectedPPD):
        print "        PPD Selected:", SelectedPPD
        
#     if (SelectedOptions):
#         print "    Selected Options:"
#         for curOption as SelectedOptions:
#             print "         ", curOption
            
    
    print "\n=============================\n"

def fnGetConfiguredPrinter():
    listPrintersCMD = ['/usr/bin/lpstat', '-p']    
    listPrinters = subprocess.Popen(listPrintersCMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (printersList, error_output) = listPrinters.communicate()
    
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
    print SelPrinter
    cmdGetURI = ['/usr/bin/lpoptions', '-p', SelPrinter]
    processGetURI = subprocess.Popen(cmdGetURI, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (options, eropts) = processGetURI.communicate()
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
    (ppdListRaw, ppderr) = processPPDSearch.communicate()
    
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
        print '[',pI,'] -', pV
    
    print "[9999] - No Dependancy, will install by hand."



def fnSetPKGINFOName():
    
    print ""



def fnSetPKGINFOVersion():
    
    print ""
 
    
printerSelection = fnGetConfiguredPrinter()
fnPrintCurrentState()
fnGetDeviceOptions(Printer)
fnPrintCurrentState()
fnChoosePPD()
fnPrintCurrentState()
fnSetPackageDependancy()