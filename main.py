from moviepy.editor import *
from pytube import YouTube
from bs4 import BeautifulSoup
import requests
import re

pattern = re.compile("\d+:\d+(:\d+)*")


def get_description(link):
    soup = BeautifulSoup(requests.get(LINK).content)
    pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
    description = pattern.findall(str(soup))[0].replace("\\n", "\n")

    return description


def extract_chapter_timestamps(description):
    desc_lines = description.splitlines()
    filtered_lines = []

    for line in desc_lines:
        if pattern.match(line):
            filtered_lines.append(line)

    return filtered_lines


def separate_time_name(str):
    out = (str.replace("\t", " ").replace("\u3000", " ")).split()
    time_parts = out[0].split(":")

    return (tuple(map(int, time_parts)), out[1])


LINK = ""
VIDEO_NAME = "video.mp4"

# Save video frames as chapter previews

if not LINK:
    print("Video not found.")
    sys.exit(1)

yt = YouTube(LINK)
print(yt.title)
description = get_description(LINK)
lines = extract_chapter_timestamps(description)

if not os.path.exists(VIDEO_NAME):
    sys.stderr.write(
        # "Error downloading videos. Check that you've installed youtube-dl.\n"
        "Couldn't find video file.\n"
    )
    sys.exit(1)

start_time = (0, 0, 0)
audio = AudioFileClip(VIDEO_NAME)
for i in range(0, len(lines)):
    # Pegando o valor do capítulo atual e o tempo que começa o recorte
    start_time, name = separate_time_name(lines[i])
    print(start_time, name)
    end_time = -1

    # Procurando o final do recorte
    try:
        next_line = lines[i + 1]
        end_time, next_name = separate_time_name(next_line)
        print("End time: ", end_time)

    except IndexError:
        print("Fim da lista")
        pass

    if end_time == -1:
        sc = audio.subclip(start_time)
    else:
        sc = audio.subclip(start_time, end_time)

    sc.write_audiofile("output/" + name + ".wav", nbytes=4, codec="pcm_s16le")
