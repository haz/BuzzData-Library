
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
file1 = DataFile(room1, FILE)
file2 = DataFile(room2, FILE)


#######
# 0.1 #
#######

print "\nGetting the license list..."
print buzz_licenses()


#######
# 0.2 #
#######

print "\n\nGetting the topic list..."
print buzz_topics()


#####
# 1 #
#####

print "\n\nGetting dataroom details..."

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


#####
# 6 #
###########
# See 7.2
##########



#######
# 7.1 #
#######

print "\n\nCreating a dataroom..."
(response, room) = DataRoom.create(user2, API, 'buzzlib-test-room', True, 'This is the readme.', 'pdm', ['testing-buzzdata', 'justin-bieber'])
print "Response:"
print response


#######
# 7.2 #
#######
print "\n\nCreating a datafile..."
(response, datafile) = room.create_datafile('test-data-file')
print "Response:"
print response


#############
# 7.3 - 7.4 #
##################################
# Note that these two API calls
#  are combined to simplify the
#  process.
################
print "\n\nUploading a new data file..."
f = open('buzzlib-test.csv', 'w')
f.write("head1,head2\n0,0\n1,1")
f.close()
print datafile.upload('buzzlib-test.csv', 'This is just an example upload.')



#####
# 8 #
##############################################
# This is currently disabled by BuzzData
###########################


#####
# 9 #
#####

print "\n\nDeleting a dataset..."
print room.destroy()



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


######
# 12 #
############################################
# Currently only admins can create users.
#####################################


####################
##                ##
##    Staging     ##
##                ##
####################

# First create the data set we will modify
(response1, room) = DataRoom.create(user2, API, 'buzzlib-test-room', True, 'This is the readme.', 'pdm', ['testing-buzzdata', 'justin-bieber'])
(response2, datafile) = room.create_datafile('test-data-file')
response3 = datafile.upload('buzzlib-test.csv', 'This is just an example upload.')
#print "Newly created dataroom: %s / %s / %s" % (response1, response2, response3)

######
# 13 #
##############################
# See the operations below
###############


######
# 14 #
######
print "\n\nInserting a few rows..."
print datafile.insert_rows([['2','2'], ['3','3']])
#
################
# Equivalently #
################
#
#stage = datafile.create_stage()
#print "Stage id: %s" % stage.stage_id
#print stage.insert_rows([['2','2'], ['3','3']])
#print stage.commit()


######
# 15 #
######
print "\n\nUpdating a row..."
print datafile.update_row(['22','22'], 2)
#
################
# Equivalently #
################
#
#stage = datafile.create_stage()
#print "Stage id: %s" % stage.stage_id
#print stage.update_row(['22','22'], 2)
#print stage.commit()


######
# 16 #
######
print "\n\nDeleting a row..."
print datafile.delete_row(1)
#
################
# Equivalently #
################
#
#stage = datafile.create_stage()
#print "Stage id: %s" % stage.stage_id
#print stage.delete_row(1)
#print stage.commit()


######
# 17 #
##############################
# See the operations above
###############


######
# 18 #
######
print "\n\nRolling back a stage..."
stage = datafile.create_stage()
print "Stage id: %s" % stage.stage_id
print stage.insert_rows([['4','4']])
print stage.rollback()

###########################################
# Finally, destroy the test data room
#  Comment this line if you want to see
#  the updated data room on Buzz Data.
print room.destroy()

print "\n\n"
