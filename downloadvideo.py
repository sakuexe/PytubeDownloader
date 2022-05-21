
import os
import ffmpeg
from terminaleffects import tcolors

class videoMerge:
    def combineVideo(video: str, audio: str, destination: str):
        '''
            The function takes two strings which include the file names to the audio and video files. Alongside this the desktop path will be given
            -
            Afterwards the downloaded files get merged into a single mp4 file with both audio and video.
            The newly merged video gets saved on the user's desktop.
        '''

        tcolors.clear
        videoStream = ffmpeg.input(f"./temp/{video}")
        audioStream = ffmpeg.input(f"./temp/{audio}")
        videoTitle = video.replace("video-", "")    # The filename for the end product gets called here

        ffmpeg.concat(videoStream, audioStream, v=1, a=1).output(f"{destination}/{videoTitle}").global_args("-loglevel", "quiet").run()
        # .global_args("-loglevel", "quiet") make it so that FFMPEG-python does not spam the terminal window with information during the process
        # this is the program's longest process and can take a lot longer than the initial files' downloads

        for file in os.listdir("./temp/"):              # lastly the files in the temporary directory get removed.
            os.remove(os.path.join("./temp/", file))