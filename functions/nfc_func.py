import time

import config.values as const
import Use_NFC as nfc

rd = nfc.CardReader()

id_tmp = ""  # IDを一時保存する変数
touched_time = 0  # タッチされた時間を保存する変数

def check_nfc_was_touched(dismiss_time=30):
    global id_tmp, touched_time
    '''
    NFCカードがタッチされたかどうかを確認する。指定された秒数内で，同一IDのカードが連続で読み込まれた場合，タッチされたとみなさない。
    
    引数: dismiss_time: 同一IDのカードが連続で読み込まれた場合，指定された秒数だけ無視する。
    戻り値: タッチされた場合はカードのID，タッチされていない場合は-1 を返す。
    '''
    if const.nfc_data["touched_flag"]:
        const.nfc_data["touched_flag"] = False  # NFCカードがタッチされたのを確認したのでフラグをFalseにする
        if (const.nfc_data["id"] != id_tmp or time.time() - touched_time > dismiss_time): # NFCカードがタッチされたかどうかを確認
            const.wav_touched.play() # タッチ音を再生
            touched_time = time.time() # タッチされた時間を保存
            if const.debug_msg:
                print("[Info] NFC card touched.", const.nfc_data["id"])
            id_tmp = const.nfc_data["id"]  # IDを一時保存
            return const.nfc_data["id"]
    
    return -1 # NFCカードがタッチされていない場合


def nfc_update_sub_thread():  # NFCの更新 別スレッドで実行される
    while True:
        if not const.nfc_data["touched_flag"]:
            const.nfc_data["id"] = rd.wait_for_card_touched()  # NFCカードの読み取りを待機
            const.nfc_data["touched_flag"] = True
            
def disconnect_reader(): # NFCリーダーの切断
    rd.disconnect_reader()
    
def connect_reader(): # NFCリーダーの接続
    rd.connect_reader()