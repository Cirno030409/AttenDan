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
ignore_nfc_error = False # NFCエラーを無視するかどうか
debug_msg = True # デバッグメッセージを表示するかどうか

# ファイルパス
SPLASH_IMAGE_PATH = "images/splash_s.png" # スプラッシュ画面の画像
SAVES_PATH = "saves/values.json"  # 保存先のパス
TOUCH_SOUND_PATH = "sounds/touch_beep.wav"  # タッチ時の音声ファイルのパス
ERROR_SOUND_PATH = "sounds/voices/voice_error_attendance_process.wav"  # エラー時音声
MORNING_SOUND_PATH = "sounds/voices/voice_good_morning.wav"  # 朝の挨拶音声
HELLO_SOUND_PATH = "sounds/voices/voice_hello.wav"  # 挨拶音声
GOODBYE_SOUND_PATH = "sounds/voices/voice_goodbye.wav"  # さよなら音声

# Global variable
nfc_data = {"id": "", "touched_flag": False}
"""
id: NFCカードのID
touched_flag: NFCカードがタッチされたかどうかを保持するフラグ（読みとったらFalseにする）
"""

exceptions = [] # 例外を保持するリスト

timers = {} # タイマーを保持するリスト

with open("system_values.json", "r") as f:
    data = json.load(f)
    VERSION = data["system_version"]
    RELEASE_NOTES = data["release_notes"]

wav = {}
wav["touched"] = sa.WaveObject.from_wave_file(TOUCH_SOUND_PATH)
wav["error"] = sa.WaveObject.from_wave_file(ERROR_SOUND_PATH)
wav["morning"] = sa.WaveObject.from_wave_file(MORNING_SOUND_PATH)
wav["hello"] = sa.WaveObject.from_wave_file(HELLO_SOUND_PATH)
wav["goodbye"] = sa.WaveObject.from_wave_file(GOODBYE_SOUND_PATH)


# 現在時刻
year = 0
month = 0
day = 0
hour = 0
minute = 0
second = 0
