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
 To make the students understand use of cloud as Platform, Storage as a
services.
 To learn the efficient tools to implement the technique
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
Save the as “ITVoyagers.xml” file in “C:\xampp\htdocs\RSS” directory
(Please remember you can change file name but save the file in “.xml” format).
Now start “Apache” server from “XAMPP Control Panel”.
Open Google Chrome and enter “http://localhost/RSS/ITVoyagers.xml” in URL bar.
If your output looks like the one shown below, then you have to add RSS subscription 
extension.

To add extension go to following link.
https://chrome.google.com/webstore/detail/rsssubscriptionextensio/nlbjncdgjeocebhnmkbbbdekmmmcbfjd?hl=en Click on “Add to 
Chrome”.
Pop-up will show up click on “Add extension”
Now just refresh your page. Your output will get load.
Click on any link to check if it is workin


practical 8 
step 1 : open aws website.
step 2 : Now go to account name and click on User.
step 3 : Fill all the details and click on Create button.
step 4 : User is created successfully.
step 5 : Now click on Add Group Give the group name and click on add button.
step 6 : group created succesfully.
step 7 : Now logout to main account and login back into newly create user.






""" )