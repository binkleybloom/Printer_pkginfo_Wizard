#!/bin/sh

# Windows/AD Hosted printer queue configuration package
# Based on 2010 Walter Meyer SUNY Purchase College (c)
# Modified by Nick McSpadden, 2013
# Fitted for Printer Deploy Wizard by Tim Schutt, Syracuse University, 2014

# Definitions Area #

currentVersion="<version>"
printername="<printername>"

### Determine if receipt is installed ###
if [ -e /private/etc/cups/deployment/receipts/$printername.plist ]; then
        storedVersion=`/usr/libexec/PlistBuddy -c "Print :version" /private/etc/cups/deployment/receipts/$printername.plist`
        echo "Stored version: $storedVersion"
else
        storedVersion="0"
fi

versionComparison=`echo "$storedVersion < $currentVersion" | bc -l`
# This will be 0 if the current receipt is greater than or equal to current version of the script

### Printer Install ###
# If the queue already exists (returns 0), we don't need to reinstall it.
/usr/bin/lpstat -p $printername
if [ $? -eq 0 ]; then
        if [ $versionComparison == 0 ]; then
                # We are at the current or greater version
                exit 1
        fi
    # We are of lesser version, and therefore we should delete the printer and reinstall.
    /usr/sbin/lpadmin -x $printername
fi

# Now we can install the printer.
<installcommand>
        
# Enable and start the printers on the system (after adding the printer initially it is paused).
# /usr/sbin/cupsenable $(lpstat -p | grep -w "printer" | awk '{print$2}')

# Create a receipt for the printer
mkdir -p /private/etc/cups/deployment/receipts
/usr/libexec/PlistBuddy -c "Add :version string" /private/etc/cups/deployment/receipts/$printername.plist
/usr/libexec/PlistBuddy -c "Set :version $currentVersion" /private/etc/cups/deployment/receipts/$printername.plist

# Permission the directories properly.
chown -R root:_lp /private/etc/cups/deployment
chmod -R 700 /private/etc/cups/deployment

exit 0