from moviepy.editor import *
from pytube import YouTube
from bs4 import BeautifulSoup
import requests
import re
import yt_dlp

pattern = re.compile("\d+:\d+(:\d+)*")


def get_description(link):
    soup = BeautifulSoup(requests.get(LINK).content)
    pattern = re.compile('(?<=shortDescription":").*(?=","isCrawlable)')
    description = pattern.findall(str(soup))[0].replace("\\n", "\n")

    return description


# Separa apenas as linhas da descrição que contém um timestamp
def extract_chapter_timestamps(description):
    desc_lines = description.splitlines()
    filtered_lines = []

    for line in desc_lines:
        if pattern.match(line):
            filtered_lines.append(line)

    return filtered_lines


# Retorna uma tupla contendo os int de hora, minuto, segundo e o nome do capítulo
def separate_time_name(str):
    out = (str.replace("\t", " ").replace("\u3000", " ").replace("-", " ")).split()
    time_parts = out[0].split(":")

    return (tuple(map(int, time_parts)), out[1:])


def get_chapter_times(lines):
    ch_list = []
    for i in range(0, len(lines)):
        time, title = separate_time_name(lines[i])
        start = time

        ch_list.append({"title": title, "start_time": start})

    return ch_list


LINK = "https://www.youtube.com/watch?v=0wTf_bbkW2U"
VIDEO_NAME = "video.mp4"

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

chapters = get_chapter_times(lines)
print(chapters)

for chapter in chapters:
    print(f"Nome = {chapter['title']}")

# start_time = (0, 0, 0)
# audio = AudioFileClip(VIDEO_NAME)
# for i in range(0, len(lines)):
#     # Pegando o valor do capítulo atual e o tempo que começa o recorte
#     start_time, name = separate_time_name(lines[i])
#     print(start_time, name)
#     end_time = -1

#     # Procurando o final do recorte
#     try:
#         next_line = lines[i + 1]
#         end_time, next_name = separate_time_name(next_line)
#         print("End time: ", end_time)

#     except IndexError:
#         print("Fim da lista")
#         pass

#     if end_time == -1:
#         sc = audio.subclip(start_time)
#     else:
#         sc = audio.subclip(start_time, end_time)

#     sc.write_audiofile(
#         "output/" + yt.title + name + ".wav", nbytes=4, codec="pcm_s16le"
#     )
