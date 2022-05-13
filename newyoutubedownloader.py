
import pytube
from pytube import YouTube                          # these two are the main pieces for getting youtube data
import os
import time                                         # time module, allows conversion of "seconds" to "MM:SS"
from terminaleffects import clearTerminal, tcolors  # has terminal colors and the clear function
from hurry.filesize import size, si                 # helps change bytes to a more readable format
from downloadvideo import videoMerge                # merges video and audio together



def printInfo(userLink: YouTube):
    clearTerminal.CLEAR()

    # Ylimääräisiä tietoja videosta joka auttaa varmistamaan että oikea video löytyi
    print(f"Title:{tcolors.bold} {userLink.title} {tcolors.clear}")
    print(f"Views:{tcolors.bold} {userLink.views} {tcolors.clear}")
    print(f"Length:{tcolors.bold} {time.strftime('%M:%S', time.gmtime(userLink.length))} {tcolors.clear}")
    #print("Ratings: ", userLink.rating)
    #print("Description: ", yt.description)


def chooseQuality(userLink: YouTube):
    print("\r\nAvailable versions: \r\n")

    print("---Video---")
    for stream in userLink.streams.filter(file_extension="mp4", only_video=True):
        print(f"{tcolors.cyan}{stream.itag}. {tcolors.clear} | {stream.resolution} | {stream.fps}fps | {size(stream.filesize, system=si)}")

    print("---Audio---")
    for stream in userLink.streams.filter(only_audio=True):
        print(f"{tcolors.cyan}{stream.itag}. {tcolors.clear} | {stream.abr} | {size(stream.filesize, system=si)} | {stream.mime_type}")

    return input(f"{tcolors.bold}Choose the version to be downloaded {tcolors.clear} \r\n(from the cyan indexes): {tcolors.cyan}")


def downloadVideo(userLink: YouTube, quality: str):
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    video = userLink.streams.get_by_itag(quality)

    if "video" in video.mime_type:
        video.download("./temp/", filename=f"video-{video.default_filename}")
        userLink.streams.get_audio_only().download("./temp/", filename=f"audio-{video.default_filename}")

        videoMerge.combineVideo(f"video-{video.default_filename}", f"audio-{video.default_filename}", desktop)
    else:
        video.download(desktop)
    
    clearTerminal.CLEAR()

    print(f"{tcolors.green}Video was downloaded to {tcolors.bold}{desktop}. {tcolors.clear}")


def main():
    print("Youtube Downloader - By Saku")
    print(f"- {pytube.__version__}")
    userLink = input("Insert the link of the video: ")
    userLink = YouTube(userLink)

    printInfo(userLink)
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