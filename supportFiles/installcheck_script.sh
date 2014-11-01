#!/bin/sh

# Based on 2010 Walter Meyer SUNY Purchase College (c)
# Modified by Nick McSpadden, 2013 and Tim Schutt, 2013 for Syracuse University

# This script was modified by Tim Schutt's Printer PkgInfo Wizard.

### Determine if receipt is installed ###
if [ -e /private/etc/cups/deployment/receipts/<printername>.plist ]; then
        storedVersion=`/usr/libexec/PlistBuddy -c "Print :version" /private/etc/cups/deployment/receipts/<printername>.plist`
        echo "Stored version: $storedVersion"
else
        storedVersion="0"
fi

versionComparison=`echo "$storedVersion < <version>" | bc -l`
# This will be 0 if the current receipt is greater than or equal to current version of the script

### Printer Install ###
# If the queue already exists (returns 0), we don't need to reinstall it.
/usr/bin/lpstat -p <printername>
if [ $? -eq 0 ]; then
        if [ $versionComparison == 0 ]; then
                # We are at the current or greater version
                exit 1
        fi
    # We are of lesser version, and therefore we should delete the printer and reinstall.
    exit 0
fi