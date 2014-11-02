#!/bin/bash
/usr/sbin/lpadmin -x <printername>
rm -f /private/etc/cups/deployment/receipts/<printername>.plist