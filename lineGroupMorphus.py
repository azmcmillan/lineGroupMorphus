# Goal is to update line group members
#
import requests
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

login = True
host = 'cucm-pub.kh.org'
print('####')
print('#### Enter your AXL credentials for ' + host + '.')
print('####\n')

for i in range(3):
    user = input('Username:')
    password = getpass()
    url = ('https://'+host+':8443/axl/')
    session = requests.Session()
    session.auth = (user, password)
    auth = session.post(url)
    authDict = auth.cookies.get_dict()
    if auth.status_code == 599:
        print('####')
        print('#### Authentication successful...')
        print('####')
        cook = str('JSESSIONID='+authDict.get('JSESSIONID')+'; JSESSIONIDSSO='+authDict.get('JSESSIONIDSSO'))
        break
    else:
        print('\n!!!!')
        print('!!!! Incorrect username or password. Please try again.')
        print('!!!!\n')
else:
    raise SystemExit('Too many login attempts!!!\n\n')

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
        print('*******************************************************************************************')
        print('Update is complete... The current line group members are shown below...')
        print('*******************************************************************************************\n\n')

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
        print('Line group: '+lineGroupName)
        root = etree.fromstring(response.content)
        for dn in root.xpath('.//*[local-name()="pattern"]'):
                print(dn.text)


#
# Update line groups
#

continueHuntGroupUpdate = True
while(continueHuntGroupUpdate):
        print('Which hunt group are you updating?')
        print('1. Epic - Tier 1 Support')
        print('2. Epic - Tier 2 - ASAP')
        print('3. Epic - Tier 2 - Amb')
        print('4. Epic - Tier 2 - Beaker Lab')
        print('5. Epic - Tier 2 - Billing')
        print('6. Epic - Tier 2 - Cupid Cardiology')
        print('7. Epic - Tier 2 - HIM')
        print('8. Epic - Tier 2 - Inpatient')
        print('9. Epic - Tier 2 - OpTime Anesthesia')
        print('10. Epic - Tier 2 - Patient Access')
        print('11. Epic - Tier 2 - Radiant Radiology')
        print('12. Epic - Tier 2 - Willow Pharmacy')
        print('99. Update all hunt groups\n')
        lineGroupNameSel = input('Enter the number of the hunt group you\'re modifying:')
        lineGroupNameSel = int(lineGroupNameSel)
        if lineGroupNameSel == 1:
                lineGroupName = 'Epic - Tier 1 Support'
                lineGroup = pd.read_csv('data/t1Support.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 2:
                lineGroupName = 'Epic - Tier 2 - ASAP'
                lineGroup = pd.read_csv('data/t2Asap.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 3:
                lineGroupName = 'Epic - Tier 2 - Amb'
                lineGroup = pd.read_csv('data/t2Amb.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 4:
                lineGroupName = 'Epic - Tier 2 - Beaker Lab'
                lineGroup = pd.read_csv('data/t2BeakerLab.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 5:
                lineGroupName = 'Epic - Tier 2 - Billing'
                lineGroup = pd.read_csv('data/t2Billing.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 6:
                lineGroupName = 'Epic - Tier 2 - Cupid Cardiology'
                lineGroup = pd.read_csv('data/t2CupidCardiology.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 7:
                lineGroupName = 'Epic - Tier 2 - HIM'
                lineGroup = pd.read_csv('data/t2Him.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 8:
                lineGroupName = 'Epic - Tier 2 - Inpatient'
                lineGroup = pd.read_csv('data/t2Inpatient.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 9:
                lineGroupName = 'Epic - Tier 2 - OpTime Anesthesia'
                lineGroup = pd.read_csv('data/t2OpTimeAnesthesia.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 10:
                lineGroupName = 'Epic - Tier 2 - Patient Access'
                lineGroup = pd.read_csv('data/t2PatientAccess.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 11:
                lineGroupName = 'Epic - Tier 2 - Radiant Radiology'
                lineGroup = pd.read_csv('data/t2RadiantRadiology.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 12:
                lineGroupName = 'Epic - Tier 2 - Willow Pharmacy'
                lineGroup = pd.read_csv('data/t2WillowPharmacy.csv')
                buildLineGroup()
                retrieveLineGroup()
        elif lineGroupNameSel == 99:
                #
                # Are you sure you want to update all groups?
                #
                areYouSure = False
                areYouSure = input('\n\nAre you sure you want to update ALL hunt groups? (y/n) ').lower()
                if areYouSure.startswith('y'): areYouSure = True
                else: areYouSure = False
                while(areYouSure):
                        lineGroupName = 'Epic - Tier 2 - ASAP'
                        lineGroup = pd.read_csv('data/t2Asap.csv')
                        buildLineGroup()
                        retrieveLineGroup()
                        lineGroupName = 'Epic - Tier 2 - Amb'
                        lineGroup = pd.read_csv('data/t2Amb.csv')
                        buildLineGroup()
                        retrieveLineGroup()
                        lineGroupName = 'Epic - Tier 2 - Beaker Lab'
                        lineGroup = pd.read_csv('data/t2BeakerLab.csv')
                        buildLineGroup()
                        retrieveLineGroup()
                        lineGroupName = 'Epic - Tier 2 - Billing'
                        lineGroup = pd.read_csv('data/t2Billing.csv')
                        buildLineGroup()
                        retrieveLineGroup()
                        lineGroupName = 'Epic - Tier 2 - Cupid Cardiology'
                        lineGroup = pd.read_csv('data/t2CupidCardiology.csv')
                        buildLineGroup()
                        retrieveLineGroup()
                        lineGroupName = 'Epic - Tier 2 - HIM'
                        lineGroup = pd.read_csv('data/t2Him.csv')
                        buildLineGroup()
                        retrieveLineGroup()
                        lineGroupName = 'Epic - Tier 2 - Inpatient'
                        lineGroup = pd.read_csv('data/t2Inpatient.csv')
                        buildLineGroup()
                        retrieveLineGroup()
                        lineGroupName = 'Epic - Tier 2 - OpTime Anesthesia'
                        lineGroup = pd.read_csv('data/t2OpTimeAnesthesia.csv')
                        buildLineGroup()
                        retrieveLineGroup()
                        lineGroupName = 'Epic - Tier 2 - Patient Access'
                        lineGroup = pd.read_csv('data/t2PatientAccess.csv')
                        buildLineGroup()
                        retrieveLineGroup()
                        lineGroupName = 'Epic - Tier 2 - Radiant Radiology'
                        lineGroup = pd.read_csv('data/t2RadiantRadiology.csv')
                        buildLineGroup()
                        retrieveLineGroup()
                        lineGroupName = 'Epic - Tier 2 - Willow Pharmacy'
                        lineGroup = pd.read_csv('data/t2WillowPharmacy.csv')
                        buildLineGroup()
                        retrieveLineGroup()
                        print('\n\nALL HUNT GROUPS WERE UPDATED!!!')
                        areYouSure = False
        #
        # Ask the user if they'd like to continue to another line group
        #
        continueHuntGroupUpdate = input('\n\nWould you like to update another hunt group? (y/n) ').lower()
        if continueHuntGroupUpdate.startswith('n'): continueHuntGroupUpdate = False
        else: continueHuntGroupUpdate = True

print('\n\nUpdates complete. Exiting...\n')