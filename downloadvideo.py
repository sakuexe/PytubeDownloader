
import os
import ffmpeg

class videoMerge:
    def combineVideo(video: str, audio: str, destination: str):
        videoStream = ffmpeg.input(f"./temp/{video}")
        audioStream = ffmpeg.input(f"./temp/{audio}")
        videoTitle = video.replace("video-", "")

        ffmpeg.concat(videoStream, audioStream, v=1, a=1).output(f"{destination}/{videoTitle}").run()

        for file in os.listdir("./temp/"):
            os.remove(os.path.join("./temp/", file))