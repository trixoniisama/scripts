import sys
import json

def get_ranges(scenes):
     ranges = []
     ranges.insert(0,0)
     with open(scenes, "r") as rfile:
        content = json.load(rfile)
        for i in range(len(content['scenes'])):
            ranges.append(content['scenes'][i]['end_frame'])
        return ranges

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/scenes.json")
    else:
        ranges = get_ranges(sys.argv[1])
        str_range = ""
        for i in range(len(ranges)-1):
            str_range+=f"{ranges[i]}f,"

        with open(f'{sys.argv[1][:-5]}.cfg', "w") as wfile:
            wfile.write('ForceKeyFrames : '+str_range[3:-1])
        print("Feed the config file to SVT-AV1 using '--config'. Don't forget to set '--keyint 0'!!")
