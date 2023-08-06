def KDS1():
    print("""
    
Write MongoDB query to :
1) Create, display and drop Database 
2) Create, display and drop Collection
3) Insert, display, update and delete a document

1)Create, display and drop Database
 Create a database 
 Syntax: use database_name 
 Display databases 
 Syntax: show dbs 
 Drop database 
 Syntax: db.database_name.drop()

2) Create, display and drop Collection
 Create a collection 
 Syntax : db.createCollection("collection_name")
 Display Collections 
 Syntax: show collections
 Drop Collection 
 Syntax: db.collection_name.drop()

3) Insert, display, update and delete a document

 Insert a document ( insertOne )
 Syntax: db.collection_name.insert({"name"})
 Insert more than one document ( insertMany ) 
 Syntax: db.collection_name.insertMany({"name1"}, {"name2"})
 Display documents 
 Syntax: db.collection_name.find() 
 Delete a document 
 Syntax: db.collection_name.remove({"deletion_criteria"}) 

    
    """)

def KDS2():
    print(""" 
    
Write MongoDB query to perform :
a)	Projection
b)	Limit
c)	Skip
d)	Sort
e)	Indexes


a)	Projection
Syntax: db.collection_name.find({ },{"key":"value"})

b)	Limit Syntax:
db.collection_name.find("key":"value").limit(value)
 

c)	Skip Syntax:
db.collection_name.find("key":"value").skip(value) 

d)	Sort Syntax:
db.collection_name.find("key":"value").sort("key":"value)
 
e)	Indexes Syntax:
To create an index:-> 
    db.collection_name.createIndex({"key":"index_value"}) 
To display/view indexes:-> db.collection_name.getIndexes()
To delete indexes:-> db.collection_name.dropIndexes()

    """)

def KDS3():
    print("""
R Studio -> new Project -> new Directory -> new Project 

data("iris")
names(iris)
new_data<- subset(iris,select = c(-Species))
new_data
cl<-kmeans(new_data,3)
cl
data<-new_data
wss<-sapply(1:15,function(k){kmeans(data,k) $tot.withinss})
wss
plot(1:15,wss,type="b",pch=19,frame=FALSE,xlab="Number of cluster k", ylab="Total within_clusters
     sum of squares")
install.packages("cluster")
library(cluster)
clusters<-hclust(dist(iris[,3:4]))
plot(clusters)
clusterCut<-cutree(clusters,3)
table(clusterCut,iris$Species)

        """)
    
def KDS4():
    print("""
data("AirPassengers")
class(AirPassengers)
start(AirPassengers)
end(AirPassengers)
frequency(AirPassengers)
summary(AirPassengers)
plot(AirPassengers)
abline(reg = lm(AirPassengers~time(AirPassengers)))
cycle(AirPassengers)
plot(aggregate(AirPassengers,FUN=mean))
boxplot(AirPassengers~cycle(AirPassengers))
    
       """)
    
def KDS5():
    print(""" 
CODE:

ftest<- read.csv(file.choose(), sep=",", header=T)
var.test(ftest$time_g1,ftest$time_g2,alternative="two.sided")

"one way anova"
data1<-read.csv(file.choose(),sep = ",", header = T)
names(data1)
summary(data1)
head(data1)
anv<-aov(formula = satindex~dept,data=data1)
summary(anv)

"two way anova"
data2<-read.csv(file.choose(),sep = ",", header = T)
names(data2)
summary(data2)
anv1<-aov(formula = satindex~dept+exp+dept*exp,data=data2)
summary(anv1)
  
    
    
    """)

def KDS6():
    print("""

Code: 

"testfor normal distrbution"
data1<- read.csv(file.choose(),sep=",",header=T)
shapiro.test(data1$C1)

"one sample t test"
apple<-read.csv(file.choose(),sep=",",header = T)
summary(apple)
t.test(apple$C1, alternative="greater", mu=97)

"independent t test"
time<-read.csv(file.choose(),sep=",",header = T)
summary(time)

"paired t test"
time1<-read.csv(file.choose(),sep = ",", header = T)
t.test(time1$HtFt,time1$HtBk, alternative = "greater", paired = T)

"t test for variance"
var<-read.csv(file.choose(), sep = ",", header = T)
summary(var)
var.test(var$X1, var$X2, alternative ="two.sided")
    
    
    """)

def KDS7():
    print(""" 
CODE:

height<-c(102,117,105,141,135,115,138,144,137,100,131,119,115,121,113)
weight<-c(61,46,62,54,60,69,51,50,46,69,48,56,64,48,59)
student<-lm(weight~height)student
predict(student,data.frame(height=199),interval="confidence")
plot(student)
    
    """)

def KDS8():
    print(""" 

Code:
library(rpart)
install.packages('rattle')
install.packages('rpart.plot')
install.packages('RColorBrewer')
library(rattle)
library(rpart.plot)
library(RColorBrewer)
hitters<-read.csv(file.choose(),sep=",",header = T)
summary(hitters)
reg.tree <- rpart(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked,data=hitters,method="class")
#reg.tree <- rpart(Salary ~ Years + Hits, data = hitters)
rpart.plot(reg.tree, type = 4)
reg.tree$variable.importance
install.packages("MASS")
library(MASS)
#set.seed(1984)
library(rpart)
train <- sample(1:nrow(hitters), nrow(hitters)/2)
tree_baseball <- rpart(Survived ~ Pclass + Sex + Age + SibSp + Parch + Fare + Embarked,data=hitters)
#tree_baseball <- rpart(Salary ~ Hits + HmRun + Runs + RBI + Walks + Years + Errors, subset = train, data = hitters)
library(rpart.plot)
rpart.plot(tree_baseball)
tree_baseball$variable.importance
    
    
    """)

def KDS9():
    print(""" 

loan<-read.csv(file.choose(),header=T,sep=",")
head(loan)
summary(loan)
str(loan)
loan$AGE<-as.factor(loan$AGE)
str(loan)
names(loan)
"creating model1"
model1<-glm(DEFAULTER~.,family=binomial,data=loan)
summary(model1)
"global testing for the acceptance of the model"
null<-glm(DEFAULTER~1,family=binomial,data=loan)
anova(null,model1,test="chisq")
"predicting the probilities"
loan$predprob<-round(fitted(model1),2)
head(loan)
"classification and misclassification analysis"
table(loan$DEFAULTER,fitted(model1)>0.5)
sens<-95/(89+95)*100
sens
spc<-478/(478+39)*100
spc

"check the trade off between sensitivity and specificity using different cut off values"
table(loan$DEFAULTER,fitted(model1)>0.1)
table(loan$DEFAULTER,fitted(model1)>0.2)
table(loan$DEFAULTER,fitted(model1)>0.3)
table(loan$DEFAULTER,fitted(model1)>0.4)
table(loan$DEFAULTER,fitted(model1)>0.5)


"goodness of fit using reciver operationl curver"
pred<-predict(model1,loan,type="response")
install.packages("ROCR")
library(ROCR)
rocrpred<-prediction(pred,loan$DEFAULTER)
rocrperf<-performance(rocrpred,"tpr","fpr")
"to check proper cut off point"
plot(rocrperf,colorize=TRUE,print.cutoffs.at=seq(0.1,by=0.1))
"to check coeficients"
coef(model1)
exp(coef(model1))
    
    """)

def KDS10():
    print(""" 

Aim:  Parsing of xml text
Source Code:-
importcsv
import requests
importxml.etree.ElementTree as ET

defloadRSS():
url = 'https://www.w3schools.com/xml/simple.xml'

resp = requests.get(url)

with open('topnewsfeed.xml' , 'wb') as f:
f.write(resp.content)

defparseXML(xmlfile):

tree = ET.parse(xmlfile)

root = tree.getroot()

newsitems = []

for item in root.findall('./food'):

news = {}

for child in item:
news[child.tag] = child.text.encode('utf8')

newsitems.append(news)

returnnewsitems

defsavetoCSV(newsitems, filename):

fields = ['name' , 'price' , 'description' , 'calories']

with open(filename, 'w') as csvfile:

writer = csv.DictWriter(csvfile, fieldnames = fields)

writer.writeheader()

writer.writerows(newsitems)

def main():
loadRSS()

newsitems = parseXML('topnewsfeed.xml')

print(newsitems)

savetoCSV(newsitems, 'topnews.csv')

if __name__ == "__main__":

main()

    



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
Save the as "ITVoyagers.xml" file in "C:\xampp\htdocs\RSS" directory
(Please remember you can change file name but save the file in ".xml" format).
Now start "Apache" server from "XAMPP Control Panel".
Open Google Chrome and enter "http://localhost/RSS/ITVoyagers.xml" in URL bar.
If your output looks like the one shown below, then you have to add RSS subscription 
extension.

To add extension go to following link.
https://chrome.google.com/webstore/detail/rsssubscriptionextensio/nlbjncdgjeocebhnmkbbbdekmmmcbfjd?hl=en Click on "Add to 
Chrome".
Pop-up will show up click on "Add extension"
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
    
    """)

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