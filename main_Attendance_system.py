"""
Attendance system for RoboDone main program
Author@ yuta tanimura
"""

import threading

import PySimpleGUI as sg
import simpleaudio as sa

import config.values as const
import functions.database_func as db
import functions.nfc_func as nfc
import Use_Database_sql as md
import Use_Mail as mm
import windows.add_student_window as add_student_window
import windows.main_window as main_window
import windows.splash_window as splash_window

ml = mm.Mail()


def main():
    window = splash_window.get_window()
    window.read(timeout=0)
    init_system()  # 初期化
    window.close()
    showgui_main()  # GUIを表示

    # システム終了処理
    db.add_systemlog_to_database("システム終了")  # システムログに記録
    db.commit_database()  # データベースにコミットする
    db.disconnect_from_database()  # データベースを切断する
    nfc.disconnect_reader()  # NFCリーダーを切断する
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
        target=nfc.nfc_update_sub_thread, daemon=True
    ).start()  # NFCの更新を別スレッドで行う

    print(
        "=======    Welcome to "
        + const.SYSTEM_NAME
        + " ver. "
        + const.VERSION
        + "   ======="
    )

    # メインループ ====================================================================================================
    while True:
        # ウィンドウ表示
        window, event, values = sg.read_all_windows(timeout=0)

        # NFCのカードのタッチを確認
        nfc.check_nfc_was_touched()  # NFCカードがタッチされたかどうかを確認

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
            if (
                values["-st_name-"] == ""
                or values["-st_age-"] == ""
                or values["-st_gender-"] == ""
                or values["-st_parentsname-"] == ""
                or values["-st_mail_address-"] == ""
            ):
                sg.PopupOK(
                    "登録するには，生徒の情報をすべて入力する必要があります。",
                    title="生徒登録エラー",
                    keep_on_top=True,
                    modal=True,
                )
                continue
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
    if (id := wait_card_popup("登録する生徒のカードをタッチしてください")) == -1:
        sg.popup_ok("生徒の登録がキャンセルされました。", title="キャンセル", keep_on_top=True, modal=True)
    else:
        data = {
            "name": name,
            "age": age,
            "gender": gender,
            "parent_name": parent_name,
            "mail_address": mail_address,
            "id": id,
            "attendance": "退席",
        }
        if db.add_student_to_database(data) == -1:
            sg.popup_ok(
                "生徒の登録に失敗しました。詳細はシステム出力を参照してください。",
                title="エラー",
                keep_on_top=True,
                modal=True,
            )
        else:
            sg.popup_ok("生徒の登録を完了しました。", title="完了", keep_on_top=True, modal=True)


def init_system():  # 初期化
    print("[Info] system initializing...")
    if db.connect_to_database() == -1:  # データベースに接続する
        print("[Error] Couldn't connect to database.")

    if (
        ml.login_smtp("robotomiline@gmail.com", "gzmt tjim egtb fwad") == -1
    ):  # SMTPサーバーにログイン
        print("[Error] Couldn't login to SMTP server.")

    if const.nfc_enabled:
        if nfc.connect_reader() == -1:
            print("[Error] Couldn't connect to NFC reader.")
        else:
            const.state_nfc = const.STAND_BY
            const.state_nfc = const.STAND_BY

    db.add_systemlog_to_database("システム起動")  # システムログに記録
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
        modal=True,
    )
    return window


def wait_card_popup(message="カードをタッチしてください"):
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
            window.close()
            return -1
        elif (id := nfc.check_nfc_was_touched(dismiss_time=2)) != -1:  # NFCカードがタッチされた場合
            print("[Info] NFC card touched.", id)
            window.close()
            return id
        else:  # NFCカードがタッチされていない場合
            continue


def print_formatted_list(data: list):  # リストを整形して表示
    ret = ""
    for i in range(len(data)):
        for j in range(len(data[i])):
            ret = ret + str(data[i][j]) + " | "
        ret = ret + "\n"
    print(ret)


if __name__ == "__main__":
    main()
    exit(0)
