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


# Retorna o tempo de início e o título do capítulo
def separate_time_name(str):
    out = (str.replace("\t", " ").replace("\u3000", " ").replace("-", " ")).split()
    time_parts = out[0].split(":")

    if len(time_parts) == 1:
        time = int(time_parts[0])
    elif len(time_parts) == 2:
        time = int(time_parts[0]) * 60 + int(time_parts[1])
    else:
        time = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2])

    return (time, out[1:])


def get_chapter_times(lines):
    ch_list = []
    for i in range(0, len(lines)):
        time, title = separate_time_name(lines[i])
        start = time

        ch_list.append({"title": title, "start_time": start})

    for i in range(len(ch_list)):
        try:
            ch_list[i]["end_time"] = ch_list[i + 1]["start_time"] - 1
        except:
            ch_list[i]["end_time"] = -1

    return ch_list


LINK = input("Link do vídeo: ")

yt = YouTube(LINK)
print(yt.title)
description = get_description(LINK)
lines = extract_chapter_timestamps(description)

chapters = get_chapter_times(lines)
for i, chapter in enumerate(chapters):
    print(i + 1, chapter)

chapters_index = input("Capítulos a serem extraídos: ")
chapters_index = [int(index) - 1 for index in chapters_index.split(",")]

selected_chapters = []
for i in chapters_index:
    selected_chapters.append(chapters[i])

for chapter in selected_chapters:
    title = chapter["title"]

    yt_opts = {
        "download_ranges": yt_dlp.utils.download_range_func(
            None, [(chapter["start_time"], chapter["end_time"])]
        ),
        "force_keyframes_at_cuts": True,
        "format": "wav/bestaudio/best",
        "postprocessors": [
            {  # Extract audio using ffmpeg
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        "outtmpl": f"output/{title}",
    }

    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download(LINK)
