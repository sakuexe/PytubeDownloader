
from multiprocessing import reduction
import pytube
from pytube import YouTube                          # these two are the main pieces for getting youtube data
import os
import time                                         # time module, allows conversion of "seconds" to "MM:SS"
from terminaleffects import clearTerminal, tcolors  # object with terminal colors and the clear function
from hurry.filesize import size, si                 # helps converting bytes to a more readable format
from downloadvideo import videoMerge                # merges video and audio together



def printInfo(userLink: YouTube):
    '''
        Function that prints out information about the video, to make sure the link was working properly
    '''
    clearTerminal.CLEAR()

    print(f"Title:{tcolors.bold} {userLink.title} {tcolors.clear}")
    print(f"Views:{tcolors.bold} {userLink.views} {tcolors.clear}")
    print(f"Length:{tcolors.bold} {time.strftime('%M:%S', time.gmtime(userLink.length))} {tcolors.clear}") # Prints out the time in a MM:SS format, rather than seconds
    #print("Ratings: ", userLink.rating)
    #print("Description: ", yt.description)


def chooseQuality(userLink: YouTube):
    '''
        Function that prints out the available streams for the given video. and return a user input
    '''

    print("\r\nAvailable versions: \r\n")

    streamItags = []    # makes a list to put all the itags to check later

    print("---Video---")
    for stream in userLink.streams.filter(file_extension="mp4", only_video=True):   # Prints out all available video streams in the mp4 format
        print(f"{tcolors.cyan}{stream.itag}. {tcolors.clear} | {stream.resolution} | {stream.fps}fps | {size(stream.filesize, system=si)}")
        streamItags.append(stream.itag)

    print("---Audio---")
    for stream in userLink.streams.filter(only_audio=True):     # Prints out all available audio streams
        print(f"{tcolors.cyan}{stream.itag}. {tcolors.clear} | {stream.abr} | {size(stream.filesize, system=si)} | {stream.mime_type}")
        streamItags.append(stream.itag)
    
    streamChoice = input(f"{tcolors.bold}Choose the version to be downloaded {tcolors.clear} \r\n(from the cyan indexes): {tcolors.cyan}")

    if int(streamChoice) in streamItags:
        return streamChoice
    else:
        raise Exception(f"{tcolors.red}The given itag does not match any streams. {tcolors.clear}")

    # returns the user's input, which is expected to be the desired stream's itag number.
    # if the input isnt found on the list of itags, throws an error.


def downloadVideo(userLink: YouTube, quality: str):
    '''
        function that takes the given video and desired format and downloads it to the desktop
    '''

    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')      # Find's the current PC's path to desktop directory
    video = userLink.streams.get_by_itag(quality)                                   # and saves the desired stream by the given itag number

    if "video" in video.mime_type:
        # if the stream is a video, it gets downloaded into a temporary directory
        # after that the highest quality audio stream gets downloaded into the same directory

        video.download("./temp/", filename=f"video-{video.default_filename}")
        userLink.streams.get_audio_only().download("./temp/", filename=f"audio-{video.default_filename}")

        # after the video and audio files have been downloaded, combineVideo function will be given the downloaded files names and the desktop path
        videoMerge.combineVideo(f"video-{video.default_filename}", f"audio-{video.default_filename}", desktop)
    else:
        # if the chosen stream is audio only, the file will get downloaded to the user's desktop folder
        video.download(desktop)
    
    clearTerminal.CLEAR()

    print(f"{tcolors.green}Video was downloaded to {tcolors.bold}{desktop}. {tcolors.clear}")
    # Lastly the confirmation that the process was completed and the path to the user's desktop directory get printed out


def main():
    clearTerminal.CLEAR()
    print("Youtube Downloader - By Saku")
    print(f"- {pytube.__version__}")
    userLink = input("Insert the link of the video: ")

    try:
        userLink = YouTube(userLink)
        printInfo(userLink)
    except:
        print(f"{tcolors.red}Couldn't find a Youtube video with the given link {tcolors.clear}")
        input("Press enter to exit")
        return

    try:
        quality = chooseQuality(userLink)
    except Exception as e:
        print(f"{tcolors.red}Something went wrong when choosing the stream. Try again {tcolors.clear}")
        print(tcolors.bold, e, tcolors.clear)
        input("Press enter to exit")
        return

    downloadVideo(userLink, quality)

    input("Press enter to quit")

main()