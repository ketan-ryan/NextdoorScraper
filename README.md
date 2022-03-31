# NextdoorScraper
## Note!
You may get some output in your console that looks like errors. If it is not color formatted, does not cause the program to crash, and does not say 'log', it doesn't matter.

## Installation Instructions (READ CAREFULLY)
1. You should already have a main.zip file. I recommend unzipping it in a folder dedicated to the scraper, such as C:\Users\John\Desktop\NextDoorScraper\
   * When unzipped, the main.exe file will be found in the main.dist folder. That exe is the one that you will be running.

2. Install Microsoft Edge Driver, and save the executable (msedgedriver.exe) in the same folder as main.exe. You can get that driver here: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
   * Currently, it is recommended to get the stable release (Version: 91.0.864.53) for x64 if you are on Windows, but if you have an issue with the version just download the right one for you.
   * You will need Microsoft Edge for this program to work.

3. Double click main.exe to run the program. The first thing it will ask you about is whether or not you have a secrets file.
4. The secrets file is a more convenient way of logging into your nextdoor account, instead of typing everything in every time. To create a secrets file, make a new text document in the same folder as main.exe called secrets.txt. You will need to format it a certain way (see below and next section)
    * On line 1, enter your phone number. 
    * On line 2, enter  your phone carrier. 
    * On line 3, enter the email you use to log into Nextdoor. 
    * On line 4, enter your password. 

### Formatting
Your entries must be formatted in a certain way. You can view how it should look like by typing 'help' when prompted, but they will also be here for reference.
* Phone number: You must enter a 10 digit phone number without any spaces or hyphens. For example, if your phone number was (999)-444-5555, you'd enter it as 9994445555.
* Email: You must enter a valid email (john@business.com)
* Cell domain: You must enter your cell domain in the correct format. Valid domains are listed below: 
  * ['Alltell', 'ATT', 'Boost', 'Cricket', 'Firstnet', 'GoogleFi', 'MetroPCS', 'Republic', 'Sprint', 'TMobile',
         'USCellular', 'Verizon', 'Virgin']

<br/>5. The next step is to enter the path to where your webdriver is stored. If left blank, it will be assumed the webdriver is in the same folder as main.exe.
  * An example path might be 'C:\Program Files\msedgedriver.exe'
  * You can also just enter 'msedgedriver.exe', or leave the field blank and hit enter, if the driver is in the same folder as main.exe.

<br/>6. [Optional] You will then be prompted on what search terms you want to be notified about. These are what the program will actually look for - so if you were looking for cameras and printers, you'd input: 'camera, printer' as a comma separated list. 
  * If you do not enter anything, a default list of ['exercise', 'equipment', 'dumbbell', 'wood'] will be used.

<br/>7. You will then need to provide a *_WINDOWS ABSOLUTE_* path to where your database will be stored. You don't actually need to have a database already in existance, but you must provide the full path, even
 if the database will be located in your folder. 
   * Ex: <span style="color:blue">C:\Users\John\Desktop\NextDoorScraper\db.json</span>
<br/>The database file must end with .json. 

<br/>That should be all you need! If you have any issues or suggestion, create a new issue in the project's issue tracker. Feel free to fork the project and adapt it to any other websites.

## Known Issues
* The program will not send you a text message if you have AT&T as your carrier. This is an AT&T issue, not an issue with the code - AT&T apparently does not like to receive email based SMS. The database will, however, still be populated and the console updated.
