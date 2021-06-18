# NextdoorScraper
## Installation Instructions
You should already have a main.zip file. I recommend unzipping it in a folder dedicated to the scraper, such as C:\Users\John\Desktop\NextDoorScraper\
<br/>When unzipped, the main.exe file will be found in the main.dist folder. That exe is the one that you will be running.

Install Microsoft Edge Driver, and save the executable in the same folder as main.exe. You can get that driver here: https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
<br/>Currently, it is recommended to get the stable release (Version: 91.0.864.53) for x64 if you are on Windows, but if you have an issue with the version just download the right one for you.
<br/>You will need Microsoft Edge for this program to work.

<br/>
Double click main.exe to run the program. You will need to enter your phone number, cell carrier, nextdoor email, and nextdoor password. To avoid from having to retype this every time you run the program, you can put them in a file called secrets.txt, preferably in the same folder as everything else.

Your secrets.txt file should have one entry per line, in the following order:
* Phone number (see formatting below)
* Phone carrier (see formatting below)
* Email (see formatting below)
* Password
The email and password are what you use to log into https://nextdoor.com

### Formatting
Your entries must be formatted in a certain way. You can view how it should look like by typing 'help' when prompted, but they will also be here for reference.
* Phone number: You must enter a 10 digit phone number without any spaces or hypens. For example, if your phone number was (999)-444-5555, you'd enter it as 9994445555.
* Email: You must enter a valid email (john@business.com)
* Cell domain: You must enter your cell domain in the correct format. Examples are listed below: 
  * ['Alltell', 'ATT', 'Boost', 'Cricket', 'Firstnet', 'GoogleFi', 'MetroPCS', 'Republic', 'Sprint', 'TMobile',
         'USCellular', 'Verizon', 'Virgin']

<br/>You will then be prompted on what search terms you want to be notified about. These are what the program will actually look for - so if you were looking for cameras and printers, you'd input: 'camera, printer' as a comma separated list. If you do not enter anything, a default list of ['exercise', 'equipment', 'dumbbell', 'wood'] will be used.

 You will also need to provide an __**Absolute**__ path to where your database will be stored. You don't actually need to have a database already in existance, but you must provide the full path, even
 if the database will be located in your folder. Ex: <span style="color:blue">C:\Users\John\Desktop\NextDoorScraper\db.json</span>
<br/>The database file must end with .json. 

<br/>That should be all you need! If you have any issues or suggestion, create a new issue in the project's issue tracker. Feel free to fork the project and adapt it to any other websites.
