import simpleaudio as sa
import json

SYSTEM_NAME = "アテンダン"

# システム状態の定数
ENABLED = 1
DISABLED = 0

# NFCの状態の定数
DISCONNECTED = 0
CONNECTED = 1

states = dict()
states["system"] = DISABLED  # システム状態
states["nfc"] = True  # NFCの状態

# Switching functions for debug
ignore_nfc_error = False
debug_msg = True

# ファイルパス
SPLASH_IMAGE_PATH = "images/splash_s.png" # スプラッシュ画面の画像
SAVES_PATH = "saves/values.json"  # 保存先のパス
TOUCH_SOUND_PATH = "sounds/touch_beep.wav"  # タッチ時の音声ファイルのパス

# Global variable
nfc_data = {"id": "", "touched_flag": False}
"""
id: NFCカードのID
touched_flag: NFCカードがタッチされたかどうかを保持するフラグ（読みとったらFalseにする）
"""

with open("system_values.json", "r") as f:
    VERSION = json.load(f)["system_version"]

wav_touched = sa.WaveObject.from_wave_file(TOUCH_SOUND_PATH)

# 現在時刻
year = 0
month = 0
day = 0
hour = 0
minute = 0
second = 0
