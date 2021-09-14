from pytube import YouTube
from youtube_search import YoutubeSearch
from pyrogram import filters
from coffeesix import bot_username
from pafy import new

def stream_video_from_yt_query(query: str):
    link = f"https://youtube.com{YoutubeSearch(query, 1).to_dict()[0]['url_suffix']}"
    yt = YouTube(link)
    x = yt.streams.filter(file_extension="mp4", res="720p")[0].download("downloads")
    return x


def command(cmd: str):
    return filters.command([cmd, f"{cmd}@{bot_username}"])


def stream_video_via_link(query: str):
    link = f"https://youtube.com{YoutubeSearch(query, 1).to_dict()[0]['url_suffix']}"
    res = new(link)
    url = res.getbest().url
    for stream in res.streams:
        if stream.resolution == "1280x720":
            url = stream.url
    return url
