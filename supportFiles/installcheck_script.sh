#!/bin/sh

# Based on 2010 Walter Meyer SUNY Purchase College (c)
# Modified by Nick McSpadden, 2013
# Further modification by Tim Schutt, 2013-14 for Syracuse University

if [ -e /private/etc/cups/deployment/receipts/<printername>.plist ]; then
        storedVersion=`/usr/libexec/PlistBuddy -c "Print :version" /private/etc/cups/deployment/receipts/<printername>.plist`
        echo "Stored version: $storedVersion"
else
        storedVersion="0"
fi
# This will be 0 if the current receipt is greater than or equal to current version of the script

### Printer Install ###
# If the queue already exists (returns 0), we don't need to reinstall it.
versionComparison=`echo "$storedVersion < <version>" | bc -l`

/usr/bin/lpstat -p <printername>

if [ $? -eq 0 ]; then
    
    if [ $versionComparison == 0 ]; then
      exit 1
    fi
    
    exit 0
fi