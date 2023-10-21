"""
Attendance system for RoboDone main program
Author@ yuta tanimura
"""

import datetime
import threading
import time

import PySimpleGUI as sg
import simpleaudio as sa

import config.constant_values as const
import Use_Database_sql as md
import Use_Mail as mm
import Use_NFC as nfc
import windows.add_student_window as add_student_window
import windows.main_window as main_window

db = md.Database()
ml = mm.Mail()
rd = nfc.CardReader()


def main():
    init_system()  # 初期化
    showgui_main()  # GUIを表示

    # システム終了処理
    add_systemlog_to_database("システム終了")  # システムログに記録
    db.commit_database()  # データベースにコミットする
    db.disconnect_from_database()  # データベースを切断する
    rd.disconnect_reader()  # NFCリーダーを切断する
    ml.logout_smtp()  # SMTPサーバーからログアウトする


def showgui_main():  # GUIを表示
    toggles = {
        "power": True,
    }
    const.state  # システム状態
    state_tmp = const.state  # 状態を一時保存

    sg.theme("BluePurple")  # テーマをセット

    main_win = main_window.get_window()  # windowを取得
    

    threading.Thread(
        target=nfc_update_sub_thread, daemon=True
    ).start()  # NFCの更新を別スレッドで行う

    print(
        "=====  Welcome to RoboDone Attendance System ver. " + const.VERSION + " ====="
    )

    # メインループ ====================================================================================================
    while True:
        # ウィンドウ表示
        window, event, values = sg.read_all_windows(timeout=0)

        # 全ウィンドウのGUIウィジェットの更新
        
        # メインウィンドウ
        if window == main_win:
            # クローズボタンの処理
            if event == sg.WIN_CLOSED:
                break
            # システム状態切り替えトグルボタン
            if event == "-power-":
                toggles["power"] = not toggles["power"]
                if toggles["power"]:
                    state = const.STAND_BY
                    print("[Info] システムが有効化されました")
                else:
                    state = const.STOP
                    print("[Info] システムが無効化されました")

                window["-power-"].update(
                    text="システム動作中" if toggles["power"] else "システム停止中",
                    button_color="white on green" if toggles["power"] else "white on red",
                )
            elif event == "\r":
                print("[Info] SQL command entered.")

            # データベース管理パネルのボタン
            elif event == "-show_all_students-":
                print_formatted_list(db.execute_database("SELECT * FROM student"))
            elif event == "-show_all_system_logs-":
                print_formatted_list(db.execute_database("SELECT * FROM system_log"))
            elif event == "-add_student-":
                add_student_win = add_student_window.get_window()
            elif event == "-remove_student-":
                pass

            # 　SQLの操作パネルのボタン
            elif event == "-execute-":
                if values["-sql-"] == "":
                    print("[Error] SQL command is empty.")
                else:
                    print("[Info] Executing SQL command...")
                    ret = db.execute_database(values["-sql-"])
                    if ret != -1:
                        print_formatted_list(ret)
                    print("[Info] SQL command execution completed.")
            elif event == "-commit-":
                db.commit_database()
            elif event == "-rollback-":
                db.rollback_database()

        # 生徒登録画面のボタン
        elif event == "-register-":
            register_student(
                values["-st_name-"],
                values["-st_age-"],
                values["-st_gender-"],
                values["-st_parentsname-"],
                values["-st_mail_address-"],
            )


def register_student(
    name: str, age: int, gender: str, parent_name: str, mail_address: str
):  # 生徒を登録
    wait_card("登録する生徒のカードをタッチしてください")


def init_system():  # 初期化
    print("[Info] system initializing...")
    if db.connect_to_Database() == -1:  # データベースに接続する
        print("[Error] Couldn't connect to database.")

    if (
        ml.login_smtp("robotomiline@gmail.com", "gzmt tjim egtb fwad") == -1
    ):  # SMTPサーバーにログイン
        print("[Error] Couldn't login to SMTP server.")

    if const.nfc_enabled:
        if rd.connect_reader() == -1:
            print("[Error] Couldn't connect to NFC reader.")
        else:
            const.state_nfc = const.STAND_BY
            const.state_nfc = const.STAND_BY

    add_systemlog_to_database("システム起動")  # システムログに記録
    print("[Info] system initialized.")


def popup_window(layout, duration=0):
    window = sg.Window(
        "Message",
        layout,
        no_titlebar=True,
        keep_on_top=True,
        finalize=True,
        auto_close=False if duration == 0 else True,
        auto_close_duration=duration,
    )
    return window


def wait_card(message="カードをタッチしてください"):
    sg.theme("LightGrey1")
    layout = [
        [
            sg.Text(
                message,
                text_color="black",
                font=("Arial", 20),
                key="-nfcstate-",
                justification="center",
                expand_x=True,
            )
        ],
        [
            sg.Image(
                filename="images/touching_card.png", key="-nfcimage-", expand_x=True
            )
        ],
        [sg.Button("キャンセル", font=("Arial", 20), key="-exit-", expand_x=True)],
    ]
    window = popup_window(layout)
    window.force_focus()
    while True:
        event, _ = window.read(timeout=0)
        if event == "-exit-":
            break
        elif nfc_data["touched_flag"]:
            window.close()
            return nfc_touched()
    window.close()


def nfc_touched():  # NFCカードがタッチされたときの処理
    if const.debug_msg:
        print("[Info] NFC card touched.", nfc_data["id"])
    const.wav_touched.play()
    nfc_data["touched_flag"] = False  # NFCカードがタッチされたフラグをFalseにする
    return nfc_data["id"]


def nfc_update_sub_thread():  # NFCの更新 別スレッドで実行される
    global nfc_data
    while True:
        if not nfc_data["touched_flag"]:
            nfc_data["id"] = rd.wait_for_card_touched()  # NFCカードの読み取りを待機
            nfc_data["touched_flag"] = True


def print_formatted_list(data: list):  # リストを整形して表示
    ret = ""
    for i in range(len(data)):
        for j in range(len(data[i])):
            ret = ret + str(data[i][j]) + " | "
        ret = ret + "\n"
    print(ret)


def enter_room(id: str):  # 入室処理
    id_list = db.execute_database("SELECT id FROM student")  # データベースからidを取得
    id_list_1d = []
    for i in range(len(id_list)):
        for j in range(len(id_list[i])):
            id_list_1d.append(id_list[i][j])  # id_listを1次元リストに変換
    if id not in id_list_1d:  # idがデータベースにない場合
        print("[Exit] No such ID in database.")
        return -1

    db.execute_database(
        "UPDATE student SET attendance = '出席' WHERE id = 'id003'"
    )  # 出席状況を欠席に変更
    dt = datetime.datetime.now()
    db.execute_database(
        "INSERT INTO log (id, year, month, day, hour, minute, second, attendance) VALUES ('"
        + id
        + "', '"
        + str(dt.year)
        + "', '"
        + str(dt.month)
        + "', '"
        + str(dt.day)
        + "', '"
        + str(dt.hour)
        + "', '"
        + str(dt.minute)
        + "', '"
        + str(dt.second)
        + "', '入室')"
    )  # ログに記録
    db.commit_database()  # データベースにコミットする
    print("[Enter] " + id + " Entered.", str(datetime.datetime.now()))


def get_fields_from_database(table: str):  # データベースからフィールドを取得
    ret = db.execute_database("PRAGMA table_info(" + table + ")")  # データベースからフィールドを取得
    fields = []
    for i in ret:
        fields.append(i[1])  # フィールドをリストに追加
    return fields


def add_student_to_database(data: dict):
    # 生徒をデータベースに追加，データベースのフィールドをキーに持った辞書型を渡すことで追加できる
    fields_database = get_fields_from_database("student")  # データベースから生徒テーブルのフィールドを取得
    fields_data = list(data.keys())  # 引数のフィールドを取得
    for i in fields_database:  # 引数のフィールドがデータベースにあるか確認
        if i not in fields_data:
            print(
                "[Error] add_student_to_database: Failed to add data to database. Fields mismatch.: ",
                i,
            )
            return -1
    id_list = db.execute_database("SELECT id FROM student")  # データベースからidを取得
    id_list_1d = []
    for i in range(len(id_list)):
        for j in range(len(id_list[i])):
            id_list_1d.append(id_list[i][j])
    if data["id"] in id_list_1d:  # idがデータベースにある場合
        print(
            "[Error] Failed to add student. This ID already exists in database. : ",
            data["name"],
        )
        return -1

    # 引数の文字列を成形
    fields_attr = ", ".join(fields_database)  # フィールドをカンマ区切りにする
    data_attr = "', '".join(list(data.values()))  # データをカンマ区切りにする

    if (
        db.execute_database(
            "INSERT INTO student (" + fields_attr + ") VALUES ('" + data_attr + "')"
        )
        == -1
    ):
        print("[Error] add_student_to_database: Couldn't add data to database.")
        return -1
    print("[Info] Added student to database. :", data["name"])


def add_systemlog_to_database(data: str):  # システムログをデータベースに追加
    dt = datetime.datetime.now()
    db.execute_database(
        "INSERT INTO system_log (year, month, day, hour, minute, second, operation) VALUES ('"
        + str(dt.year)
        + "', '"
        + str(dt.month)
        + "', '"
        + str(dt.day)
        + "', '"
        + str(dt.hour)
        + "', '"
        + str(dt.minute)
        + "', '"
        + str(dt.second)
        + "', '"
        + data
        + "')"
    )  # ログに記録
    db.commit_database()  # データベースにコミットする


def exit_room(id: str):  # 退室処理
    id_list = db.execute_database("SELECT id FROM student")  # データベースからidを取得
    id_list_1d = []
    for i in range(len(id_list)):
        for j in range(len(id_list[i])):
            id_list_1d.append(id_list[i][j])  # id_listを1次元リストに変換
    if id not in id_list_1d:  # idがデータベースにない場合
        print("[Enter] No such ID in database.")
        return -1

    db.execute_database(
        "UPDATE student SET attendance = '退席' WHERE id = 'id003'"
    )  # 出席状況を欠席に変更
    dt = datetime.datetime.now()
    db.execute_database(
        "INSERT INTO log (id, year, month, day, hour, minute, second, attendance) VALUES ('"
        + id
        + "', '"
        + str(dt.year)
        + "', '"
        + str(dt.month)
        + "', '"
        + str(dt.day)
        + "', '"
        + str(dt.hour)
        + "', '"
        + str(dt.minute)
        + "', '"
        + str(dt.second)
        + "', '退出')"
    )  # ログに記録
    db.commit_database()  # データベースにコミットする
    print("[Exit] " + id + " Exited.", str(datetime.datetime.now()))


if __name__ == "__main__":
    main()
    exit(0)
