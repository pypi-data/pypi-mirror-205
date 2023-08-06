def allpr():
    print("""
    
practical no 2 

virtualization with kvm

Step 1 : #sudo grep -c "svm\|vmx" /proc/cpuinfo.
Step 2 : #sudo apt-get install qemu-kvm libvirt-bin bridge-utils virt-manager.
Step 3 : #sudoadduserrait.
After running this command, log out and log back in as rait.
Step 4 : #sudoadduserraitlibvirtd.
After running this command, log out and log back in as rait.
Step 5 : Open Virtual Machine Manager application and Create Virtual Machine.
Step 6 : Create a new virtual machine as shown below.
Step 7 : Install windows operating system on virtual machine.
Step 8: Installation of windows on virtual machine.
Step 9: Installation of windows 7 on virtual machine.
Step 10: Initialization of windows on virtual machine.


practical no 3 
Installation Steps: (https://docs.openstack.org/devstack/latest/guides/single-machine.html)
Add user
useradd -s /bin/bash -d /opt/stack -m stack
apt-get install sudo -y
echo "stack ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
login as stack user
Download DevStack
sudo apt-get install git -y || sudo yum install -y git
git clone https://git.openstack.org/openstack-dev/devstack
cd devstack
Run DevStack

Now to configure stack.sh. DevStack includes a sample in devstack/samples/local.conf.
Create local.conf as shown below to do the following:

local.conf should look something like this:
[[local|localrc]]
FLOATING_RANGE=192.168.1.224/27
FIXED_RANGE=10.11.12.0/24
FIXED_NETWORK_SIZE=256
FLAT_INTERFACE=eth0
ADMIN_PASSWORD=supersecret
DATABASE_PASSWORD=iheartdatabases
RABBIT_PASSWORD=flopsymopsy
SERVICE_PASSWORD=iheartksl

Run DevStack:

./stack.sh


practical no 4 

Ex 4: Study and implementation of Storage as a Service
1. Aim: To study and implementation of Storage as a Service
2. Objectives: From this experiment, the student will be able to
3 To make the students understand use of cloud as Platform, Storage as a
services.
4 To learn the efficient tools to implement the technique
3. Outcomes: The learner will be able to
4. Conclusion:

Google Docs provide an efficient way for storage of data. It fits well in
Storage as a service (SaaS). It has varied options to create documents,
presentations and also spreadsheets. It saves documents automatically after a
few seconds and can be shared anywhere on the Internet at the click of a
button.

practical no 5 

Identity management 

 steps :- 
1) go to demo.owncloud.org

2) login with default credentials i.e Usename & Password = demo or username and password = test 

3) New Screen will appear in which you can see the files or folders uploaded by you on the won cloud Service, you can upload files and folders by clicking on plus(+) sign.
One can share the uploaded file using the share option i.e sending files through links via Gmail or using other options in the menu eg.(Facebook, Twitter).

    """)

def allpr2():
    print("""

practical no 6
Practical 6: Study Cloud Security management
Login as Root user

Security using MFA(Multi Factor Authentication) device code:
1) goto aws.amazon.com
2) click on "My Account"
3) select "AWS management console" and click on it
4) Give Email id in the required field
if you are registering first time then select "I am a new user" radio button
5) click on "sign in using our secure server" button
6) follow the instruction and complete the formalities
(Note: do not provide any credit card details or bank details)
sign out from
7) Again go to "My Account"
select "AWS management console" and click on it
Sign in again by entering the user name and valid password ( check "I am
returning user and my password is" radio button)
Now you are logged in as a Root User
All AWS project can be viewed by you, but you cant make any changes in it
or you cant create new thing as you are not paying any charges to amazon (for
reason refer step:6)
To create the user in a root user follow the steps mentioned below:
1) click on "Identity and Access Management" in security and identity project
2) click in "Users" from dashboard
It will take you to "Create New Users"
click on create new user button
enter the "User Name"
(select "Generate and access key for each user" checkbox, it will create a user
with a specific key)
click on "Create" button at right bottom
3) once the user is created click on it
4) go to security credentials tab
5) click on "Create Access Key", it will create an access key for user.
6) click on "Manage MFA device" it will give you one QR code displayed on
the screen
you need to scan that QR code on your mobile phone using barcode scanner
(install it in mobile phone)you also need to install "Google Authenticator" in
your mobile phone to generate the MFA code
7) Google authenticator will keep on generating a new MFA code after every
60 seconds
that code you will have to enter while logging as a user.
Hence, the security is maintained by MFA device code...
one can not use your AWS account even if it may have your user name and
password, because MFA code is on your MFA device (mobiel phone in this
case) and it is getting changed after every 60 seconds.
Permissions in user account:
After creating the user by following above mentioned steps; you can give
certain permissions to specific user
1) click on created user
2) goto "Permissions" tab
3) click on "Attach Policy" button
4) select the needed policy from given list and click on apply.



Practical 7:Write a program for web feed


NOTE: It is no necessary to use XAMPP Server to perform this practical we just need server 
to run the program i.e. we can use Wamp Server.
We are using XAMPP. First open Notepad and write the following XML code in it.
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
<item>
<title> itvoyagers</title>
<link> https://itvoyagers.in/ </link>
<description>ITVoyagers is an educational blog for information technology and computer 
science program.We have started this
blog with a goal of meeting the requirements of learners to cope with the changing 
technology.
We are aiming to expand its scope in all sections of IT.</description>
</item>
<item>
<title>Cloud Computing</title>
<link> https://itvoyagers.in/cloud-computing/</link>
<description>Cloud Computing</description>
</item>
<item>
<title>Business intelligence </title>
<link> https://itvoyagers.in/advance-topics/business-intelligence/</link>
<description>Business intelligence blog</description>
</item>
<item>
<title>work from home</title>
<link>https://www.lifecharger.org/work-from-home-5-tips/</link>
<description>work from home</description>
</item>
</channel>
</rss>

practical 8 
step 1 : open aws website.
step 2 : Now go to account name and click on User.
step 3 : Fill all the details and click on Create button.
step 4 : User is created successfully.
step 5 : Now click on Add Group Give the group name and click on add button.
step 6 : group created succesfully.
step 7 : Now logout to main account and login back into newly create user.






cyber forencis

practical 1

Aim: Creating a Forensic Image using FTK Imager/Encase Imager:
-Creating Forensic Image
-Check Integrity of Data
-Analyze Forensic Image
Steps:
Creating Forensic Image
1. Click File, and then Create Disk Image, or click the button on the tool bar.
2. Select the source you want to make an image of and click Next.

https://E-next.in

02

If you select Logical Drive to select a floppy or CD as a source, you can check the Automate
multiple removable media box to create groups of images. Imager will automatically
increment the case numbers with each image, and if something interrupts the process, you
may assign case number manually.
3. Select the drive or browse to the source of the image you want, and then click Finish.

4. In the Create Image dialog, click Add.

https://E-next.in

02

 You can compare the stored hashes of your image content by checking the Verify
images after they are created box. If a file doesn’t have a hash, this option will
generate one.
 You can list the entire contents of your images with path, creation dates, whether files
were deleted, and other metadata. The list is saved in a tab-separated value format

5. Select the type of image you want to create, and then click Next.
Note: If you are creating an image of a CD or DVD, this step is skipped because all
CD/DVD images are created in the IsoBuster CUE format.

Now select Evidence Tree and analyze the virtual disk as physical disk.

Similarly to add raw image select again add evidence item and click on image file and click
on open option.
Click on finish.
Now raw image will be added as physical drive to analyze.

Aim: Data Acquisition:
- Perform data acquisition using:
- USB Write Blocker + FTK Imager
Steps:
Enable USB Write Block in Windows 10, 8 and 7 using registry
1. Press the Windows key + R to open the Run box. Type regedit and press Enter.

2. This will open the Registry Editor. Navigate to the following key:
HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control
3. Right-click on the Control key in the left pane, select New -> Key.
4. Name it as StorageDevicePolicies.

https://E-next.in

02

5. Select the StorageDevicePolicies key in the left pane, then right-click on any empty space
in the right pane and select New -> DWORD (32-bit) Value. Name it WriteProtect.

6. Double-click on WriteProtect and then change the value data from 0 to 1.

7. The new setting takes effect immediately. Every user who tries to copy / move data to USB
devices or format USB drive will get the error message
“The disk is write-protected”.
8. We can only open the file in the USB drive for reading, but it’s not allowed to modify and
save the changes back to USB drive.

So this is how you can enable write protection to all connected USB drives. If you want to
disable write protection at a later time, just open Registry Editor and set the WriteProtect
value to 0.

https://E-next.in

02

9. Now Create image of the USB drive using FTK imager

10. Select the USB drive folder by browsing and click next & Finish
11.In the Create Image dialog, click Add.

https://E-next.in

02

 You can compare the stored hashes of your image content by checking the Verify
images after they are created box. If a file doesn’t have a hash, this option will
generate one.
 You can list the entire contents of your images with path, creation dates, whether files
were deleted, and other metadata. The list is saved in a tab-separated value format

Select the type of image you want to create, and then click Next

practical 3 

Aim: Forensics Case Study:
- Solve the Case study (image file) provide in lab using Autopsy

Steps:
1. Start Autopsy

2. Select New Case

https://E-next.in

02

3. Enter Case Information and Base Directory & click on finish

https://E-next.in

02

4. Select the type of Data Source that has to be added

5. Select Data Source( here a previously made image file of a USB is selected)
6. Select all ingest modules

https://E-next.in

02

7.Wait for Data source to process and be added to local database. Click Finish

8. Now Autopsy window will appear and it will analyzing the disk that we have selected

https://E-next.in

02

9. All files will appear in table tab select any file to see the data.

10. Expand the tree from left side panel to view the files and then expand the deleted files
node
11. To recover the file, go to view node-> Deleted Files node , here select any file and right
click on it than select Extract Files option.

https://E-next.in

02

12. By default Export folder is choose to save the recovered file.

https://E-next.in

02

13. Now go to the Export Folder to view Recover file.

https://E-next.in

02

14. Click on Generate Report from autopsy window and Select the Excel format and click on
next

https://E-next.in

02

15. Click Finish after selecting All Results

https://E-next.in

02

Now Report is Generated So click on close Button, We can see the Report on Report Node.
Double click on the excel file and open it to view the report

practical 4
Aim: Capturing and analyzing network packets using Wireshark (Fundamentals):
- Identification the live network
- Capture Packets
- Analyze the captured packets
Steps:
1. Open Wireshark and click on Ethernet.

2. Now go on browser and open any unsecured website i.e www.razorba.com and perform
some activity on the website.
3. Now come back to Wireshark and enter http in the search bar.

https://E-next.in

02

4. Now click on the get request and see the details.

Practical No – 5

Aim: Analyze the packets provided in lab and solve the questions using Wireshark:
-What web server software is used by www.snopes.com?
-About what cell phone problem is the client concerned?
-According to Zillow, what instrument will Ryan learn to play?
-How many web servers are running Apache?
-What hosts (IP addresses) think that jokes are more entertaining when they are
explained?
Steps:
 What web server software is used by www.snopes.com?
1. Open the AskSnopess file

2. In the display filter type http.

https://E-next.in

02

3. In the second panel expand the hypertext transfer protocol.

4. Click on the host name > right click> Apply as column

https://E-next.in

02

5. Click any of the http packet > right click> Follow> TCP Stream

6. The webserver is Microsoft IIS/5.0

https://E-next.in

02

 About what cell phone problem is the client concerned?

1. In the display filter type frame matches”(?)cell”.

https://E-next.in

02

 According to Zillow, what instrument will Ryan learn to play?
1. In the display filter type frame matches”(?)zillow”.

2. In the second tab expand the transmission control protocol.
Right click on transmission control protocol > Protocol Preferences > Allow subdissector to
reassemble TCP stream.

3. Click on file > Export objects > HTTP.

https://E-next.in

02

4. Click on Save all.

5. Run the saved file and you will get the result.

https://E-next.in

02

 How many web servers are running Apache?
1. Right click on HTTP > Apply as column.

https://E-next.in

02

2. Click on Statistics > Endpoints.

3. Click the check box.

https://E-next.in

02

4. Beside IPv4 the number 21 shows that there are 21 web servers running on apache.

 What hosts (IP addresses) think that jokes are more entertaining when they are
explained?
1. In the display filter type frame matches”(?)jokes”.

Practical No – 6

Aim: Using Sysinternals tools for Network Tracking and Process Monitoring:
-Check Sysinternals tools
-Monitor Live Processes
-Capture RAM-Capture
-TCP/UDP packets
-Monitor Hard Disk
-Monitor Virtual Memory
-Monitor Cache Memory

Steps:
1) Check Sysinternals tools
Windows Sysinternals tools are utilities to manage, diagnose, troubleshoot, and monitor a
Microsoft Windows environment

The following are the categories of Sysinternals Tools:
 File and Disk Utilities
 Networking Utilities
 Process Utilities
 Security Utilities
 System Information Utilities
 Miscellaneous Utilities
2) Monitor Live Processes (Tool: ProcMon)

https://E-next.in

02

Click on filter > Process monitor filter

Click on tools > Process tree

Click on filter > File summary

https://E-next.in

02

3) Capture RAM (Tool: RAMCapture)
Open the Ramcapture tool.

Click on capture.

https://E-next.in

02

4) Capture TCP/UDP packets (Tool: TcpView)
Open the Tcpview tool.

Right click on any packet > whois

https://E-next.in

02

5) Monitor Hard Disk (Tool: DiskMon)
Open the Diskmon tool.

https://E-next.in

02

6) Monitor Virtual Memory (Tool: VMMap)
Open the VMMap tool.

7) Monitor Cache Memory (Tool: RAMMap)
Open the RAMMap tool.

Practical No – 7
Aim: Recovering and Inspecting deleted files
-Check for Deleted Files
-Recover the Deleted Files
-Analyzing and Inspecting the recovered files
Steps:
1. Open AccessData FTK Imager. Click on File > Create Disk Image.

2. Type the destination path.
3. Click on Logical drive.

4. Click on Add > Browse.

https://E-next.in

02

5. Select the type of data format and click next.

7. Open the Forensic toolkit and click on file > new case.

https://E-next.in

02

8. Enter the details and click on next.

9. Click on next.

https://E-next.in

02

10. Click on next.

11. Click on next.

12. Click on next.

https://E-next.in

02

13. Click on Add Evidence > Acquired Image of Drive > Continue.

14. Select the image file.

15. Click on OK.

https://E-next.in

02

16. Click on next.

17. Click on Finish.

18. Files are being carving.

https://E-next.in

02

19. In the left panel you can see all the recovered files.

20.Click on the Deleted file tab-> Right click on any deleted file to export it

https://E-next.in

02

21.Browse and choose the destination folder to export the deleted file

Practical No – 8
Aim: Acquisition of Cell phones and Mobile devices
Steps:
1. Download mobiledit forensic tool in mobile.
2. Open Mobiledit tool in PC.

3. Click on connect.

https://E-next.in

02

4. Connect your mobile device to the system. Click on phone > next.

5. Click the connection

6. Open the mobiledit tool in phone and click on the type of connection (i.e Wifi) > Copy the
IP address and enter it in the PC and click next.

https://E-next.in

02

7. It shows the phone which is connected. Click on next.

8. Click on next.

https://E-next.in

02

9. Click on whole system and click next.

10. Click on case and click next.

https://E-next.in

02

11. Click on your device in the left panel.

12. You can see all the files.

Practical No – 9

Aim: Email Forensics
- Mail Service Providers
- Email protocols
- Recovering emails
- Analyzing email header

Mail Service Providers
An email service provider (ESP) is a company that offers email marketing or bulk email
services. An ESP may provide tracking information showing the status of email sent to each
member of an address list. ESPs also often provide the ability to segment an address list into
interest groups or categories, allowing the user to send targeted information to people who
they believe will value the correspondence.
Here are nine features to look for when you select your business email service:
Spam Filter - Spam messages are a huge time waster. You don't want to spend your valuable
time reading them. That's why you want an email service that has a system in place to detect
and filter out inbox spam.
Reliability - Your business email provider needs to be up and running when you need it.
Your email should always be available. Email downtime could result in lost or unhappy
customers.
Integration - Some email services work well with other business tools such as calendars, and
productivity suites. If your business relies heavily on such tools, consider an email package
that integrates with the other tools you already use.
Security - With email hacks being a regular news item, you want your business email
provider to offer strong measures to keep your accounts secure. You need to keep your
messages safe and don't want any unauthorized use of your email account.
Ease of Use - As your business grows, more of your staff members need to create and use
email accounts. Reduce staff training time by selecting an email service provider that's easy
to use.
Archive Capabilities - The best business email providers provide a way for you to save,
store, and organize your email messages and drafts. For many businesses, keeping an
accurate and well-organized record of business communication is vital.
Advanced Features - When running a small business, advanced email features such as the
ability to recall sent messages or schedule tasks within email can be important. Which
advanced features are most important depends on your unique business needs.

https://E-next.in

02

Reputation - Your business email service provider needs to have a good reputation.
Remember, your email address is one of the first pieces of information prospective clients
see.
Storage - When selecting an email service provider, keep in mind the amount of storage
space included with your account. You don't want to run out of space.
Types of Popular Email Service Providers are as follows:
1.Gmail:
One of the most popular and best email service providers, Gmail is used for personal and
business communications alike. According to statistics reported by TechCrunch in 2016, over
a billion people use Gmail.
Gmail has a good reputation and includes many advanced features such as the Undo Send
feature and Email Forwarding. Since this service is owned by search engine giant, Google,
naturally it includes a powerful search utility and filter system.

Google has also added strengthened security measures such as two-step verification and
powerful spam filters to make it less likely that your account is hacked or that you receive
junk messages. Finally, it integrates cleanly with popular productivity tools including Google
Calendar and Google Docs.
2. Outlook
Microsoft's Outlook.com email provider is a strong option if you're looking for the best email
provider. Statistics from Microsoft show that Outlook had over 400 million users in 2016.
This popular email package has the support and resources of tech giant Microsoft behind it.
Outlook.com offers advanced features such as Clutter, which finds emails that are likely of
low priority and separates them from your inbox. Another advanced Outlook.com feature is
the ability to Undelete, or recover an email after you've accidentally discarded a message.
Outlook integrates well with popular software including other Microsoft products.
3.iCloud Mail
iCloud email is a possible email choice if you frequently access your email package from
your Apple mobile device. Apple employs several security features to make sure that your
iCloud account is not compromised including two-step verification or two-factor
authentication. There's also a spam filter.
4. Yahoo Mail
Yahoo! was one of the early Internet companies, dating back to 1994. Yahoo! Mail is popular
with many users. In 2016, it was announced that the company was acquired by Verizon.
Despite the recent changes to Yahoo! ownership, you can still sign up for a Yahoo! Mail
account. Some Yahoo! Mail features you can benefit from if you choose it as your email
provider include:
Auto deletion of Trash messages after 90 days

https://E-next.in

02

Huge storage capacity (1 TB)
Built-in web search tool, calendar, and notepad
Spam filters and SSL encryption

5. AOL Mail
AOL is another early Internet company. In the 1980s the company was known as America
Online. It was purchased by Verizon in 2015. The email component of the organization
remains a popular and strong service that has earned its place on this list of the best email
services.
Key AOL Mail features include advanced spam filters and virus protection. It's also known
for the ability to personalize your email address with the MyAddress feature that lets you
select your own email domain name.

6. Zoho Mail
Although Zoho Mail has several premium levels available, there is also a free level available
that allows you to have up to 25 users. For many small businesses, this will be enough—so
we have included the email service on our list of the best free email providers.
With the free level of Zoho Mail, you are limited to 5 GB of storage per user. It does include
antivirus protection and spam filtering. This email service integrates with other Zoho
productivity tools such as calendar, tasks, and notes.
Email Protocols
E-mail Protocols are set of rules that help the client to properly transmit the information to or
from the mail server
The most commonly used Email protocols on the internet - POP3, IMAP and SMTP. Each
one of them has specific function and way of work.
POP3
Post Office Protocol version 3 (POP3) is a standard mail protocol used to receive emails from
a remote server to a local email client. POP3 allows you to download email messages on your
local computer and read them even when you are offline. Note, that when you use POP3 to
connect to your email account, messages are downloaded locally and removed from the email
server. This means that if you access your account from multiple locations, that may not be
the best option for you. On the other hand, if you use POP3, your messages are stored on
your local computer, which reduces the space your email account uses on your web server.
By default, the POP3 protocol works on two ports:
Port 110 - this is the default POP3 non-encrypted port
Port 995 - this is the port you need to use if you want to connect using POP3 securely

https://E-next.in

02

IMAP
The Internet Message Access Protocol (IMAP) is a mail protocol used for accessing email on
a remote web server from a local client. IMAP and POP3 are the two most commonly used
Internet mail protocols for retrieving emails. Both protocols are supported by all modern
email clients and web servers.
While the POP3 protocol assumes that your email is being accessed only from one
application, IMAP allows simultaneous access by multiple clients. This is why IMAP is more
suitable for you if you're going to access your email from different locations or if your
messages are managed by multiple users.
By default, the IMAP protocol works on two ports:
Port 143 - this is the default IMAP non-encrypted port
Port 993 - this is the port you need to use if you want to connect using IMAP securely

SMTP
SMTP stands for Simple Mail Transfer Protocol. It was first proposed in 1982. It is a standard
protocol used for sending e-mail efficiently and reliably over the internet. Simple Mail
Transfer Protocol (SMTP) is the standard protocol for sending emails across the Internet.
By default, the SMTP protocol works on three ports:
Port 25 - this is the default SMTP non-encrypted port
Port 2525 - this port is opened on all SiteGround servers in case port 25 is filtered (by your
ISP for example) and you want to send non-encrypted emails with SMTP
Port 465 - this is the port used if you want to send messages using SMTP securely

Recovering email using AccessData FTK:
1. Start AccessData FTK by right-clicking the AccessData FTK desktop icon, clicking Run as
administrator, and clicking Continue in the UAC message box (if you’re using Vista). If
you’re prompted with a warning message and/or notification (see Figure below), click OK as
needed to continue. If asked whether you want to save the existing default case, click Yes.

https://E-next.in

02

2. When the AccessData FTK Startup dialog box opens, click Start a new case, and then click
OK.
3. In the New Case dialog box, type your name for the investigator name, and type the case
number and case name. Click Browse, navigate to and click your work folder, click OK, and
then click Next.
4. In the Case Information dialog box, enter your investigator information, and then click
Next.
5. Click Next until you reach the Refine Case - Default dialog box, shown in Figure below.
6. Click the Email Emphasis button, and then click Next.
7. Click Next until you reach the Add Evidence to Case dialog box, and then click the Add
Evidence button.
8. In the Add Evidence to Case dialog box, click the Individual File option button (see Figure
below), and then click Continue.
9. In the Select File dialog box, navigate to your work folder, click the Jim_shu’s.pst file, and
then click Open.
10. In the Evidence Information dialog box, click OK.

https://E-next.in

02

https://E-next.in

02

https://E-next.in

02

https://E-next.in

02

11. When the Add Evidence to Case dialog box opens, click Next. In the Case summary
dialog box, click Finish.

12. When FTK finishes processing the file, in the main FTK window, click the E-mail
Messages button, and then click the Full Path column header to sort the records (see Figure

Practical No – 10

Aim: Web Browser Forensics
-Web Browser working
-Forensics activities on browser
-Cache / Cookies analysis
-Last Internet activity

Steps:
1. Open BrowserHistoryExaminer.

2. Click on file > Capture History.

https://E-next.in

02

3. Select the capture folder and click on next.

4. Enter the destination to capture the data.

5. The History is been extracting.

https://E-next.in

02

6. The data has been retrieved.

7. On the left panel click on bookmarks.

https://E-next.in

02

8. On the left panel click on cached files.

9. On the left panel click on cached images.

https://E-next.in

02

10. On the left panel click on cookies.

11. To Create Reports. Click on file > Report and save the report as pdf or html page.


    """)