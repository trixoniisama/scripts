from vstools import core, Keyframes
from pathlib import Path
import argparse
import os

def keyframes_helper(file_path, overwrite, method, min_kf_dist, max_kf_dist):

    out = Path(os.path.dirname(file_path)) / "svt_keyframes.cfg"
    if out.exists() and not overwrite:
        print("Reusing existing keyframes config.")
        exit()
    print("Generating keyframes config file...")
    clip = core.lsmas.LWLibavSource(r"{}".format(file_path))
    keyframes = Keyframes.from_clip(clip, 1 if method=="accurate" else 0)

    #print(len(keyframes))
    for i, frame in enumerate(keyframes):
        if i == 0:
            keyframes_cut = [str(frame)]
        else:
            frame_diff = keyframes[i]-keyframes[i-1]

            if frame_diff>=min_kf_dist:
                keyframes_cut.append(str(frame))

            if frame_diff>=max_kf_dist and frame_diff-max_kf_dist>=min_kf_dist:
                keyframes_cut.append(str(keyframes[i-1]+max_kf_dist))
    #print(len(keyframes_cut))

    keyframes_str = f"ForceKeyFrames : {'f,'.join([str(i) for i in keyframes_cut])}f"
    with open(out, "w", encoding="utf-8") as f:
        f.write(keyframes_str)
    print("Done")
    print("Feed the config file to SVT-AV1 using '--config'. Don't forget to set '--keyint 0'!!")

if __name__ == "__main__":
    VALID_METHODS = ["accurate", "accurate++"]

    parser = argparse.ArgumentParser(prog='SVT-AV1 Keyframes Helper', description='Determines the keyframes placement in a video and generates the necessary SVT-AV1 config file')
    parser.add_argument('source', help='Input video path')
    parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrites existing config file')
    parser.add_argument('-m', '--method', dest='method', choices=VALID_METHODS, default='accurate', help='Algorithm selection. Accurate uses WWXD. Accurate++ uses the intersection of WWXD and SCXVID, can help avoid false positives. Default: accurate')
    parser.add_argument('-min', '--min_kf_dist', dest='min_kf_dist', type=int, default=24, help='Minimum number of frames for a scenecut. Default: 24')
    parser.add_argument('-max', '--max_kf_dist', dest='max_kf_dist', type=int, default=240, help='Maximum scene length. If a scene is longer than the specified value, a keyframe is added every max_kf_dist frames. Except when the distance between the added keyframe and the next one is smaller than min_kf_dist. Helps with seeking performance. Default: 240')
    args = parser.parse_args()

    keyframes_helper(args.source, args.overwrite, args.method, args.min_kf_dist, args.max_kf_dist)
