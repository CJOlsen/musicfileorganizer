# MP3 Library Builder
# By: Christopher Olsen
# Version: 0.01 (in (non-active) development)
# Copyright Notice: Copyright 2012 Christopher Olsen
# License: GNU General Public License, v3 (see LICENSE.txt)
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
#
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
# So MAKE SURE it is given a folder containing only music files
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

import os
import shutil
import fnmatch
from mutagen.mp3 import MP3,InvalidMPEGHeader,HeaderNotFoundError
from mutagen.m4a import M4A

import sys
import traceback

def move_file(home_path, file_path):
    """ Takes the path of the music folder and the path of the file to be moved
        , moves the file depending on its type

        Steps:

        1) check filetype, if not mp3/m4a  move to Leftovers
        2) get iD3 tags
        3) check for artist folder, create if needed
        4) check for album folder, create if needed
        5) rename file with track number and name
        6) move file into album folder"""
    
    filetype = 'undefined'
    
    if fnmatch.fnmatch(file_path, '*.mp3'):
        audio = MP3(file_path)
        filetype = '.mp3'
    elif fnmatch.fnmatch(file_path, '*.m4a'):
        audio = M4A(file_path)
        filetype = '.m4a'
    else:
        print 'moving file to leftovers 00'
        shutil.move(file_path, home_path + '/Leftovers')
        return

    artist, song, album, track_no = u'unknown_artist',u'unknown_song',\
                                    u'unknown_album',u'unknown_track'
                                         
    try:
        artist = audio["TPE1"][0].strip('/-')
    except: pass

    try:
        song = audio["TIT2"][0].strip('/-')
    except: pass
        
    try:
        album = audio["TALB"][0].strip('/-')
    except: pass
    
    try:
        track_no = str(audio["TRCK"].pprint())[5:]
        track_no = track_no.split('/')[0]
    except KeyError:
        """ this means the track number is unknown """
        print 'track key error', file_path
    except UnicodeEncodeError:
        print 'track unicode error', file_path

    current_artists = os.listdir(home_path +'/Music')
    
    if artist not in current_artists:
        os.mkdir(home_path + '/Music/' + artist)

    current_albums = os.listdir(home_path +'/Music/'+ artist)

    if album not in current_albums:
        os.mkdir(home_path +'/Music/'+ artist +'/'+ album)

    current_songs = os.listdir(home_path +'/Music/'+ artist +'/'+ album)

    try:
        """ if track number is unknown, song title won't include it """
        if int(str(track_no)) > 0:
            song_name = track_no + '.' + song + filetype
    except:
        song_name = song + filetype

    if song_name not in current_songs:
        # this renames *and moves* the file.  It's a little messy having
        # os and shutil moving files in different situations.
        os.rename(file_path, home_path +'/Music/'+ artist +'/'+ album +'/'+ song_name)

    else:
        pass
        #print 'duplicate error'
        #shutil.move(file_path, home_path + '/Duplicates')
    
    return            


def organizefolder(path):
    """ Takes a music folder as an argument
        Organizes the music folder
        Returns an error or success message """

    print 'Organization process beginning, this may take a few moments....'

    file_tuples = []
    
    for line in os.walk(path):
        """ This loop gives us a list of 3-tuples where the first object is
            the path, the second is a list of subdirectories in that path
            and the third is a list of the files for that path """
        file_tuples.append(line)

        
    if not os.path.exists(path + '/Leftovers'):
        os.mkdir(path + '/Leftovers')
    if not os.path.exists(path + '/Music'):
        os.mkdir(path + '/Music')

    for three_tuple in file_tuples:
        """ 'files' is a list of files in the path of three_tuple[0] (the path)
        """
        files = three_tuple[2]

        if len(files) > 0:
            for new_file in files:
                """ **new_file is only the name of a file, not the full path**
                    move_file will move the file into a)an existing musc folder,
                    b) a new music folder if needed, or c) the leftovers folder
                    if it isn't clear what should be done with the file """
                
                try:    
                    """ here 'path' is the path of the main music folder, and
                        and the second argument is the path of the file in
                        quiestion """
                    move_file(path, three_tuple[0] +'/'+ new_file)
                except:
                    print 'file move failed! for ', new_file
                    try:
                        print 'moving to leftovers 99'
                        print "Unexpected error:", sys.exc_info()[0]
                        print 'sys.exc_info()', sys.exc_info()
                        print 'traceback.print_tb(sys.exc_info()[2])',\
                              traceback.print_tb(sys.exc_info()[2])
                        shutil.move(three_tuple[0] +'/'+ new_file, path +\
                                     '/Leftovers')
                    except:
                        print '...file not moved to leftovers due to another '\
                                'unexpected error:', sys.exc_info()[0]
                    
    """ at this point the new file tree should be done """

    #organizeleftovers(path)
    #cleanup(path)

    print 'Finished!', len(os.listdir(path + '/Leftovers'))\
          ,'files are in the Leftovers folder and need to be handled manually. '\
          ,'This could mean the program was unable to properly handle their iD3'\
          ,'tags.  i.e. a name may have non-standard characters, etc.'
