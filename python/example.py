
import os

from buzzdata import *

##########################################
##
## Numbers correspond to the numbering
##  on the BuzzData API website:
##  - http://buzzdata.com/faq/api/api-methods
##
## The order may be shuffled to accommodate
##  some of the more dynamic API calls.
##
######################


#########
# Setup #
#########
API = 'PUT YOUR OWN API KEY HERE'
USER = 'eviltrout'
ROOM = 'b-list-celebrities'
FILE = 'biaYUILGqr4y37yAyCM7w3'

user1 = User(USER)
user2 = User(USER, API)
room1 = DataRoom(user1, ROOM)
room2 = DataRoom(user2, ROOM, API)
file1 = DataFile(user1, ROOM, FILE)
file2 = DataFile(user1, ROOM, FILE, API)



#####
# 1 #
#####

print "\nGetting dataroom details..."

print "\nWithout key:"
print room1.details()

print "\nWith key:"
print room2.details()


#####
# 2 #
#####

print "\n\nListing a user's datarooms..."

print "\nWithout key:"
print user1.list_datarooms()

print "\nWith key:"
print user2.list_datarooms()


#####
# 3 #
#####

print "\n\nRetrieving a dataroom's data file list..."

print "\nWithout key:"
print room1.list_datafiles()

print "\nWith key:"
print room2.list_datafiles()


#####
# 4 #
#####

print "\n\nRetrieving a datafile's revision list..."

print "\nWithout key:"
print file1.history()

print "\nWith key:"
print file2.history()


#####
# 5 #
#####

print "\n\nDownloading a datafile..."

print "\nDefault download:"
file2.download()
os.system('ls')

print "\nNamed download:"
file2.download(filename='foo.xyz')
os.system('ls')

print "\nVersion download:"
file2.download(version=1)
os.system('ls')


#######
# 7.1 #
#######

print "\n\nCreating a dataroom..."

(response, room) = DataRoom.create(user2, API, 'buzzlib-test-room', True, 'This is the readme.', 'pdm', ['testing-buzzdata', 'justin-bieber'])
print "Response:"
print response



#####
# 6 #
#####

# Coming soon...



######
# 10 #
######

print "\n\nGetting user details..."

print "\nWithout key:"
print user1.details()

print "\nWith key:"
print user2.details()


######
# 11 #
######

print "\n\nSearching..."

print "\nWithout key:"
print buzz_search('soccer')

print "\nWith key:"
print buzz_search('soccer', API)


print "\n\n"
