import sys
import ffprobe

def print_subs_info(file_path, mode):

    metadata = ffprobe.FFProbe(file_path)

    subtitle_count = 0
    languages = ""

    for stream in metadata.streams:
        if stream.is_subtitle():
            subtitle_count += 1
            if mode == "language":
                try:
                    languages += ffprobe.FFStream.language(stream) + ", "
                except:
                    pass
            elif mode == "title":
                try:
                    languages += ffprobe.FFStream.title(stream) + ", "
                except:
                    pass
            else:
                print("Unknown mode.")
                exit(0)

    print(languages[:-2])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py path/to/video.file {language/title}")
    else:
        file_path = sys.argv[1]
        mode = sys.argv[2]
        print_subs_info(file_path, mode)
