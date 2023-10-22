import simpleaudio as sa

SYSTEM_NAME = "アテンダン"
VERSION = "0.0.1"  # バージョン

# システム状態の定数
NOW_PROCESSING = 2
STAND_BY = 1
STOP = 0

# NFCの状態の定数
DISCONNECTED = 0
STAND_BY = 1

state = STAND_BY  # システム状態
state_nfc = DISCONNECTED  # NFCの状態

# Switching functions for debug
nfc_enabled = True
debug_msg = True

# Global variable
nfc_data = {"id": "", "touched_flag": False}
"""
id: NFCカードのID
touched_flag: NFCカードがタッチされたかどうかを保持するフラグ（読みとったらFalseにする）
"""

wav_touched = sa.WaveObject.from_wave_file("sounds/touch_beep.wav")
