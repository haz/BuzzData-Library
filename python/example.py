
from buzzdata import *

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



print "\n\n"
