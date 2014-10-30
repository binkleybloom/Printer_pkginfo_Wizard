Instructions
============
This tool has fairly specific edits for my environment. Edits will be needed for yours.
---------------------------------------------------------------------------------------

This process is best used while you have a text editor window open to record values you need to
copy in to the scripts.

Use of this tool:

1. Copy the entire folder and name the new folder to your printer deployment name.
	eg: 'psy-printer-CanoniRA6075-1'

	1.1. Configure the printer via PRQ-03 on your setup machine or VM.
 
	1.2. Enable the CUPS web interface by opening a terminal session and entering
		$ sudo cupsctl WebInterface=yes

	1.3. Browse to local CUPS web interface at http://localhost:631 - click on “Printers” in top menu, 
	and select the printer you are configuring.

	1.4. The queue name is after the printer server URL - 
    so in smb://AS-PRQ-03.ad.syr.edu/AS-CSG-LEX-X734DE-CSG1029 
    the printer name is AS-CSG-LEX-X734DE-CSG1029. Make a note of this for later.
	
2. Edit the top section in 'installcheck_script.sh' and 'postinstall_script.sh' to match 
your printer. The two sections should be identical between the files so edit once and 
copy/paste. 

3. If you need to install more than 4 options for the printer, you will need to add the 
extra lines below line #63 in the postinstall_script.sh file. Blank options are ignored.

4. Edit the printer name in the uninstall_script.sh file where noted.

5. Double-click the "process.command" file. It will prompt you for the name of the 
installer as it will show in Munki. You may use AlphaNumeric as well as "-" and "_" chars.

6. A PrinterDeployName.plist file will be generated inside the directory. Locate this file 
and copy it to the "munkirepo/pkginfo" directory.

7. Create a deployment manifest for the printer, and include the associated driver package 
in the manifest.

NOTE: It is good practice to edit the printer deployment plist (in MunkiAdmin) and set the 
printer driver package as a requirement for the deployment. This will ensure that the 
printer deployment will not run if the drivers have not been installed.


CONFIGURING PRINTER OPTIONS
============================
To get a list of appropriate keys & values for printer options to specify during the deploy 
script, I find the following technique works well:

1. Set up the printer on your Deployment VM or desktop (working machine).
2. In the Printers pref pane, open the printer and select the "options" tab.
3. Make note of any flags that are checked in that section.
4. Open the Terminal 

	4a. enter "lpstat -p" to get the list of configured printers - select and copy the printer
		name that you are working on for the deployment
		
	4b. enter "lpoptions -p <printer name you just copied> -l" - this will print out the list
		of keys for printer options and their current settings. You will receive MANY more lines in 
		this output than you had for checkboxes in the printer options GUI. Find the options
		that match the check boxes from the UI. Those are the ones you need to configure in
		the deployment scripts.