import os
import re
from pytube import YouTube

# Prompt the user for the YouTube video URL and save directory
url = input("Enter the YouTube video URL: ")
save_dir = input("Enter the directory to save the video: ")

# Get available streams for the video
yt = YouTube(url)
streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()

# Display available resolutions to the user
for i, stream in enumerate(streams):
    print(f"{i+1}. Resolution: {stream.resolution}, FPS: {stream.fps}, Size: {stream.filesize/1024/1024:.2f} MB")

# Prompt the user to select a resolution
selected_stream_index = int(input("Enter the number corresponding to the desired resolution: ")) - 1
selected_stream = streams[selected_stream_index]

# Prompt the user to select a file format
file_format = input("Enter 'mp3' to download audio or 'mp4' to download video: ").lower()

# Download the selected video stream as MP3 or MP4
if file_format == 'mp3':
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(save_dir, filename_prefix='audio_')
    # Replace invalid characters in video title with underscores
    video_title = re.sub(r'[^\w\-_.() ]', '_', yt.title)
    os.rename(os.path.join(save_dir, f'audio_{audio_stream.default_filename}'), os.path.join(save_dir, f'{video_title}.mp3'))
elif file_format == 'mp4':
    selected_stream.download(save_dir)
    # Replace invalid characters in video title with underscores
    video_title = re.sub(r'[^\w\-_.() ]', '_', yt.title)
    os.rename(os.path.join(save_dir, selected_stream.default_filename), os.path.join(save_dir, f'{video_title}.mp4'))
else:
    print("Invalid file format entered. Download aborted.")

print("Download complete!")
