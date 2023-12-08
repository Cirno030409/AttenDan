import simpleaudio as sa

SYSTEM_NAME = "アテンダン"
VERSION = "1.0.0"  # バージョン

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
SAVES_PATH = "saves/saved_values.pkl"  # 保存先のパス

# Global variable
nfc_data = {"id": "", "touched_flag": False}
"""
id: NFCカードのID
touched_flag: NFCカードがタッチされたかどうかを保持するフラグ（読みとったらFalseにする）
"""

# 保存するデータ
saves = {
    "mail": {
        "enter": {
            "subject": "", 
            "body": ""
        },
        "exit": {
            "subject": "", 
            "body": ""
        },
        "test_address": ""
    }
}

wav_touched = sa.WaveObject.from_wave_file("sounds/touch_beep.wav")

# 現在時刻
hour = 0
minute = 0
second = 0
