# Goal is to update line group members
#
import requests, sys, time
import datetime as datetime
from getpass import getpass
from lxml import etree
import pandas as pd

#
# Gather the credentials used to authenticate against the Cisco
# Call Manager server.
#
# Create a new session with your AXL credentials. All 
# queries to Call Manager will use the returned COOKIES 
# for authentication.
#

path = str(sys.argv[1])
login = True
host = 'cucm-pub.kh.org'

ts = time.time()
sttime = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H:%M')

with open(path + 'log.txt', 'a') as f:
        f.write('\nSCRIPT RAN AT: ' + str(sttime) + '\n')

for i in range(3):
    user = 'ENTER USERNAME HERE'
    password = 'ENTER PASSWORD HERE'
    url = ('https://'+host+':8443/axl/')
    session = requests.Session()
    session.auth = (user, password)
    auth = session.post(url)
    authDict = auth.cookies.get_dict()
    if auth.status_code == 599:
        with open(path + 'log.txt', 'a') as f:
                f.write('Login successful.\n')
        cook = str('JSESSIONID='+authDict.get('JSESSIONID')+'; JSESSIONIDSSO='+authDict.get('JSESSIONIDSSO'))
        break
    else:
        with open(path + 'log.txt', 'a') as f:
                f.write('Failed login.\n')
else:
    with open(path + 'log.txt', 'a') as f:
                f.write('Failed login.\n')

#
# Set headers and soap envelope
# 

action = 'updateLineGroup'
headers = {
        'SOAPAction': 'CUCM:DB ver=12.5 '+action,
        'Content-Type': 'text/xml',
        'Cookie': cook
        }
soapEnvStart = (
            '<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:ns=\"http://www.cisco.com/AXL/API/12.5\">\n'
            '    <soapenv:Header/>\n'
            '    <soapenv:Body>\n'
            )
soapEnvEnd = (
            '    </soapenv:Body>\n'
            '</soapenv:Envelope>'
            )

def buildLineGroup():
        #
        # Build out the members for the line group
        #
        lineSelectionOrder = 0
        members = ''
        for i in lineGroup.index:
                lineSelectionOrder += 1
                members += (
                '                    <member>\n'
                '                        <lineSelectionOrder>'+str(lineSelectionOrder)+'</lineSelectionOrder>\n'
                '                        <directoryNumber>\n'
                '                            <pattern>'+str(lineGroup['extension'][i])+'</pattern>\n'
                '                            <routePartitionName>Phone_Line_PT</routePartitionName>\n'
                '                        </directoryNumber>\n'
                '                    </member>\n'
                )
        #
        # Build the payload to update call manager
        #
        payload = (
                soapEnvStart+
                '        <ns:'+action+'>\n'
                '            <name>'+lineGroupName+'</name>\n'
                '                <members>\n'
                                     +members+
                '                </members>\n'
                '        </ns:'+action+'>\n'
                +soapEnvEnd
        )
        #
        # Push the update to Call Manager
        #
        response = requests.request("POST", url, headers=headers, data=payload)
        with open(path + 'log.txt', 'a') as f:
                f.write('The update has been pushed to Call Manager for ' + lineGroupName + '\n')
                f.write(str(response) + '\n')

def retrieveLineGroup():
        #
        # Show the current line group configuration.
        #
        action = 'getLineGroup'
        headers = {
                'SOAPAction': 'CUCM:DB ver=12.5 '+action,
                'Content-Type': 'text/xml',
                'Cookie': cook
                }
        payload = (
                soapEnvStart+
                '        <ns:'+action+'>\n'
                '            <name>'+lineGroupName+'</name>\n'
                '        </ns:'+action+'>\n'
                +soapEnvEnd
        )        
        response = requests.request("POST", url, headers=headers, data=payload)
        root = etree.fromstring(response.content)
        allDns = ''
        for dn in root.xpath('.//*[local-name()="pattern"]'):
                allDns += (dn.text + '\n')
        with open(path + 'log.txt', 'a') as f:
                f.write('The current line group members in Call Manager are shown below...\nLine group: ' + lineGroupName + '\n')
                f.write(allDns + '\n\n')


#
# Update line groups
#

lineGroupName = 'Epic - Tier 1 Support'
lineGroup = pd.read_csv('data/t1Support.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - ASAP'
lineGroup = pd.read_csv(path + 't2Asap.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - Amb'
lineGroup = pd.read_csv(path + 't2Amb.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - Beaker Lab'
lineGroup = pd.read_csv(path + 't2BeakerLab.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - Billing'
lineGroup = pd.read_csv(path + 't2Billing.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - Cupid Cardiology'
lineGroup = pd.read_csv(path + 't2CupidCardiology.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - HIM'
lineGroup = pd.read_csv(path + 't2Him.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - Inpatient'
lineGroup = pd.read_csv(path + 't2Inpatient.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - OpTime Anesthesia'
lineGroup = pd.read_csv(path + 't2OpTimeAnesthesia.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - Patient Access'
lineGroup = pd.read_csv(path + 't2PatientAccess.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - Radiant Radiology'
lineGroup = pd.read_csv(path + 't2RadiantRadiology.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - Willow Pharmacy'
lineGroup = pd.read_csv(path + 't2WillowPharmacy.csv')
buildLineGroup()
retrieveLineGroup()
lineGroupName = 'Epic - Tier 2 - User Security Access'
lineGroup = pd.read_csv(path + 't2UserSecurityAccess.csv')
buildLineGroup()
retrieveLineGroup()
#lineGroupName = 'zTest'
#lineGroup = pd.read_csv(path + 'zTest.csv')
#buildLineGroup()
#retrieveLineGroup()

with open(path + 'log.txt', 'a') as f:
                f.write('Updates complete...\n\n\n')