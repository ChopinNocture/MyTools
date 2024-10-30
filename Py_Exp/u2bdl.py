import os
import pytube
import argparse


def download_from(url, dir):
    #url = 'https://www.youtube.com/watch?v=F-fKsnUtnd4'
    youtube = pytube.YouTube(url)
    print(youtube.streams.get_highest_resolution())
    video = youtube.streams.order_by('resolution')[-1] # get_highest_resolution()
    audio = youtube.streams.filter(only_audio=True).order_by("abr")[-1]
    print(video, audio)
    # video.download(dir)
    audio.download(dir)


def add_arguments(parser):
    parser.add_argument(
        '-url', '-u',
        action='store',
        dest='url',
        help='movie of youtube url',
        required=True
    )
    parser.add_argument(
        '-dir',
        action='store',
        dest='dir',
        help='where to store, default is ./',
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Download movie from Youtube!")
    add_arguments(parser)
    args = parser.parse_args()

    dest = os.getcwd()
    if args.dir is not None:
        dest = args.dir
    download_from(args.url, dest)