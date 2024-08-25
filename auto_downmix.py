import sys
import subprocess
import json

def normalized_downmix(file_path, bitrate):

    og_loudness = f"ffmpeg -hide_banner -i '{file_path}' -af 'ebur128' -f null -"
    p1 = subprocess.run(og_loudness, shell=True, capture_output=True, text=True, universal_newlines=True)
    p1 = str(p1).replace(r"\n", "\n").splitlines()
    p1 = p1[-20:]
    try:
        p1 = next(value for value in p1 if value.startswith("    I:"))
    except StopIteration:
        raise ValueError("Edge case or ffmpeg changed its syntax yet again...")

    l = []
    for t in p1.split():
        try:
            l.append(float(t))
        except ValueError:
            pass
    og_loudness = l[0]

    print(f"########################\n{p1}\n{og_loudness}")

    down_loudness = f"ffmpeg -hide_banner -i '{file_path}' -af 'lowpass=c=LFE:f=120,pan=stereo|FL=.3FL+.21FC+.3FLC+.21SL+.21BL+.15BC+.21LFE|FR=.3FR+.21FC+.3FRC+.21SR+.21BR+.15BC+.21LFE,ebur128' -f null -"
    p2 = subprocess.run(down_loudness, shell=True, capture_output=True, text=True, universal_newlines=True)
    p2 = str(p2).replace(r"\n", "\n").splitlines()
    p2 = p2[-20:]
    try:
        p2 = next(value for value in p2 if value.startswith("    I:"))
    except StopIteration:
        raise ValueError("Edge case or ffmpeg changed its syntax yet again...")

    l = []
    for t in p2.split():
        try:
            l.append(float(t))
        except ValueError:
            pass
    down_loudness = l[0]

    print(f"########################\n{p2}\n{down_loudness}")

    req_volume = round(og_loudness - down_loudness, 2) # - 0.5
    print(f"########################\n{req_volume}")

    final = f"ffmpeg -v quiet -hide_banner -i '{file_path}' -af 'lowpass=c=LFE:f=120,pan=stereo|FL=.3FL+.21FC+.3FLC+.21SL+.21BL+.15BC+.21LFE|FR=.3FR+.21FC+.3FRC+.21SR+.21BR+.15BC+.21LFE,volume={req_volume}dB' -f flac - | opusenc --ignorelength --bitrate {bitrate} - '{file_path}.opus'"
    mediainfo_output = subprocess.check_output(final, shell=True, text=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py path/to/audio.file bitrate")
    else:
        file_path = sys.argv[1]
        bitrate = sys.argv[2]
        normalized_downmix(file_path, bitrate)
