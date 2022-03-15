lineGroupMorphus

-Install requirements.txt
-Update CSV files with extensions.

Run script: python3 lineGroupMorphus.py
-This script will look at all CSV data stored in the 'data' folder

Run script: python3 lineGroupMorphusPath.py
-You must specify the folder path of the CSV files (located in 'data')
    For example: python3 lineGroupMorphusPath.py 'data/15/'
    -If we're updating the t1Support.csv this full path would be 'data/15/t1Support.csv'
    -This allows you to use this script as a scheduled task pointed to different folders