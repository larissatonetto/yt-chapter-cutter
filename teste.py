import yt_dlp
from yt_dlp.utils import download_range_func

start_time1 = 2  # accepts decimal value like 2.3
end_time1 = 7

start_time2 = 8  # accepts decimal value like 2.3
end_time2 = 10

yt_opts = {
    "verbose": True,
    "download_ranges": download_range_func(
        None, [(start_time1, end_time1), (start_time2, end_time2)]
    ),
    "force_keyframes_at_cuts": True,
}

with yt_dlp.YoutubeDL(yt_opts) as ydl:
    ydl.download("https://www.youtube.com/watch?v=BxUS1K7xu30")
