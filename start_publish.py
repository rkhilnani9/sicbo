import cv2
import subprocess
import numpy as np
import glob
import time
import shlex
from loguru import logger
from dice_combinations import DICE_COMBINATIONS

all_numbers = list(range(0, 37))

FPS = 30
HEIGHT = 540
WIDTH = 960
RTMP_URL = "rtmp://vid.heeraexch.com:1935/live/casino1"

common_image_paths = glob.glob(
    "/Users/rkhilnan/Desktop/sicbo/content/common_segment/*.jpg"
)
common_image_paths = sorted(
    common_image_paths, key=lambda x: int(x.split("/")[-1].split(".")[0])
)
# common_images = [cv2.imread(impath) for impath in common_image_paths]

combo_paths = {}
for combo in all_combinations:
    combo_str = "".join([str(digit) for digit in combo])
    paths = glob.glob(f"frames/{combo_str}/*.jpg")
    paths = sorted(paths, key=lambda x: int(x.split("/")[-1].split(".")[0]))
    combo_paths[combo_str] = paths

# command and params for ffmpeg
command = [
    "ffmpeg",
    "-y",
    "-r",
    str(FPS),
    "-f",
    "rawvideo",
    "-vcodec",
    "rawvideo",
    "-pix_fmt",
    "bgr24",
    "-s",
    "{}x{}".format(WIDTH, HEIGHT),
    "-i",
    "-",
    "-c:v",
    "libx264",
    "-pix_fmt",
    "yuv420p",
    "-preset",
    "ultrafast",
    "-f",
    "flv",
    RTMP_URL,
]

p = subprocess.Popen(command, stdin=subprocess.PIPE)
font = cv2.FONT_HERSHEY_SIMPLEX
k = 0
m = 0
while True:
    m += 1
    try:
        ts = time.time()
        print("ts:", ts)
        for ix, impath in enumerate(common_image_paths):
            im = cv2.imread(impath)
            k += 1

            # Call start bets event here and stop bets after X secs
            if ix == 0:
                round_start_script = f"python3 start_event.py --ts {str(ts)}"
                shlex_bet = shlex.split(round_start_script)
                subprocess.Popen(shlex_bet, start_new_session=True)
            time.sleep(1 / 38)
            cv2.putText(
                im, f"Common: {k}", (10, 100), font, 3, (0, 255, 0), 2, cv2.LINE_AA
            )
            try:
                p.stdin.write(im.tobytes())
            except:
                time.sleep(0.3)
                im = cv2.imread(impath)
                p.stdin.write(im.tobytes())
            if ix == (len(common_image_paths) - 100):
                bet_stop_script = f"python3 nomorebets.py --ts {str(ts)}"
                shlex_bet = shlex.split(bet_stop_script)
                subprocess.Popen(shlex_bet, start_new_session=True)
                generate_numbers_script = f"python3 gen_frames.py --ts {str(ts)}"
                shlex_bet = shlex.split(generate_numbers_script)
                subprocess.Popen(shlex_bet, start_new_session=True)

        dice_numbers = open("sicbo_dice_numbers.txt", "r").read()
        dice1 = dice_numbers.split(",")[0].strip()
        dice2 = dice_numbers.split(",")[1].strip()
        dice3 = dice_numbers.split(",")[2].strip()
        n_paths = combo_paths[dice1 + dice2 + dice3]
        for ix, impath in enumerate(n_paths):
            k += 1
            # Call start bets event here and stop bets after X secs
            im = cv2.imread(impath)
            time.sleep(1 / 38)
            cv2.putText(im, str(k), (10, 100), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(im, str(m), (10, 450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
            try:
                p.stdin.write(im.tobytes())
            except:
                time.sleep(0.3)
                im = cv2.imread(impath)
                p.stdin.write(im.tobytes())
            if ix == len(n_paths) - 100:
                cmd3 = f"python3 roundend.py --ts {str(ts)}"
                cmds3 = shlex.split(cmd3)
                p5 = subprocess.Popen(cmds3, start_new_session=True)
    except KeyboardInterrupt:
        p.stdin.close()