import yt_dlp

link = input("Enter video url: ")
with yt_dlp.YoutubeDL() as yt:
    yt.download([link])
   