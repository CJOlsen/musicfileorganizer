# MP3 Library Builder
# By: Christopher Olsen
# Version: 0.01 (in (non-active) development)
# License: GNU GPL
#
# This program takes a pile of poorly named and organized music files and
# renames/organizes them based on their iD3 tag info
# ******** WARNING ********WARNING********WARNING********WARNING********
# It also trashes their current file structure in the process, so be careful
# and work on a backup copy of your music library.  If you think your library
# is too big to back up that's all the more reason to do it.  
#
# ******** WARNING ********WARNING********WARNING********WARNING********
# This program WILL mess up the file structure of any folder it is given,
# recusrsively searching every subdirectory and moving files it doesn't 
# understand into its 'Leftovers' folder
# So MAKE SURE it is given a folder containing only a bunch of music files
# (in any number of subfolders) that need to be renamed and reorganized.
#
#
# File structure is Artist/Album/Song
#
# This program currently names and places tracks with ~%75 success rate
#
# To run:  open a python shell and run the program, then call the function
# organizefolder(path) where 'path' is the path of the folder to be organized
#
# The future:  - could use some sort of error collection scheme
#              - some saftey could be built in to make malicious use more 
#               difficult
#              - OOP offers interesting possibilities
