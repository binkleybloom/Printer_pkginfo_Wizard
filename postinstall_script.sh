#!/bin/sh

# Windows/AD Hosted printer queue configuration package
# Based on 2010 Walter Meyer SUNY Purchase College (c)
# Modified by Nick McSpadden, 2013 and Tim Schutt, 2014

# Script to install and setup printers on a Mac OS X system in a "Munki-Friendly" way.
# Make sure to install the required drivers first!


# Definitions Area #

currentVersion="replaceVersion"


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
/usr/sbin/lpadmin \
        -E \
        -p "$printername" \
        -L "$location" \
        -D "$gui_display_name" \
        -v "${servername}${printername}" \
        -P "$driver_ppd" \
        -o "$option_1" \
        -o "$option_2" \
        -o "$option_3" \
        -o "$option_4" \
        -o printer-is-shared=false \
        -o printer-error-policy=abort-job \
        -o printer-op-policy=authenticated \
        -E
        
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