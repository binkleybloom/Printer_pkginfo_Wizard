Munki printer deployment wizard
=

Python code by Tim Schutt, Syracuse University, &copy; 2014

*Under active development - use at your own risk*

Shell scripts largely based on code available at the Munki wiki, under "Related Tasks: Managing Printers with Munki" by Walter Myer, SUNY Purchase &copy; 2010 
and Nick McSpadden, 2013

Setup
=
download via:

	$ git clone https://github.com/binkleybloom/Printer_pkginfo_Wizard

There are two required components:
<li>the process.py script
<li>the supportFiles directory and its unmodified contents - must be in the same directory as process.py

You may rename the process.py file to process.command if you wish to be able to  double click it to launch instead of calling it from a terminal session.

To use this tool:
-
On the machine that you will be running the tool from, you will need:
<ol>
<li>A current installation of Munki - downloadable from https://github.com/munki/munki/releases
<li>The printer installed on the machine where you run this tool. It needs to be configured as you would like it deployed - this includes the drivers, how it is named, location information, duplex / paper trays / staple output options configured... you get the idea. This information gets pulled for the deployment.
</ol>
If you want to configure package dependency to ensure the correct drivers are installed when you deploy the printer, you will need to populate the "driverCollection" dictionary at the top of the python script with your printer driver packages.

Then, just cd to the directory with the tool, fire it off with './process.py' and follow the directions. At the end, it should provide you with a .plist file suitable for inclusion in your repository.

*Note:*
I have made assumptions based on my own environment that may not match yours - predominately regarding how Active Directory print queues are used. This is a very large area of "YMMV".
