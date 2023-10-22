import config.values as const
import Use_NFC as nfc

rd = nfc.CardReader()
id_tmp = ""  # IDを一時保存する変数

def check_nfc_was_touched():
    global id_tmp
    '''
    NFCカードがタッチされたかどうかを確認します。同一IDのカードが連続で読み込まれた場合，タッチされたとみなしません。
    
    引数:なし
    戻り値:タッチされた場合はカードのID，タッチされていない場合は-1
    '''
    if const.nfc_data["touched_flag"]:
        const.nfc_data["touched_flag"] = False  # NFCカードがタッチされたのを確認したのでフラグをFalseにする
        if const.nfc_data["id"] != id_tmp: # 同一ＩＤカードの連続読み取りを無視
            const.wav_touched.play() # タッチ音を再生
            if const.debug_msg:
                print("[Info] NFC card touched.", const.nfc_data["id"])
            id_tmp = const.nfc_data["id"]  # IDを一時保存
            return const.nfc_data["id"]
    else:
        return -1


def nfc_update_sub_thread():  # NFCの更新 別スレッドで実行される
    while True:
        if not const.nfc_data["touched_flag"]:
            const.nfc_data["id"] = rd.wait_for_card_touched()  # NFCカードの読み取りを待機
            const.nfc_data["touched_flag"] = True
            print("reading id:", const.nfc_data["id"])
            
def disconnect_reader(): # NFCリーダーの切断
    rd.disconnect_reader()
    
def connect_reader(): # NFCリーダーの接続
    rd.connect_reader()