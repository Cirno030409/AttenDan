"""
Attendance system for RoboDone main program
Author@ yuta tanimura
"""

import datetime
import os
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
import windows.remove_student_window as remove_student_window
import windows.remove_student_without_card_window as remove_student_without_card_window
import windows.splash_window as splash_window

ml = mm.Mail()
windows = {}


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

    sg.theme("BluePurple")  # テーマをセット

    windows["main"] = main_window.get_window()  # windowを取得

    print(
        "=======    Welcome to "
        + const.SYSTEM_NAME
        + " ver. "
        + const.VERSION
        + "   ======="
    )

    if const.states["nfc"] == const.DISCONNECTED:
        print(
            "[Info] NFCカードリーダが接続されていません。入退室処理を有効化するには，NFCカードリーダが正常に接続されていることを確認し，システムを再起動してください。"
        )

    # メインループ ====================================================================================================
    while True:
        # ウィンドウ表示
        win, event, values = sg.read_all_windows(timeout=0)

        # 更新
        # NFCのカードのタッチを確認
        if (
            const.states["nfc"] == const.CONNECTED
            and const.states["system"] == const.ENABLED
        ):
            nfc.check_nfc_was_touched()  # NFCカードがタッチされたかどうかを確認
        else:
            const.nfc_data["touched_flag"] = False

        # システムの状態をトグルボタンに反映
        if const.states["system"] == const.ENABLED:
            toggles["power"] = True
        elif const.states["system"] == const.DISABLED:
            toggles["power"] = False

        # メインウィンドウ
        if win == windows["main"]:
            # クローズボタンの処理
            if event == sg.WIN_CLOSED:
                break

            # トグル状態に応じてボタンのテキストを変更
            if toggles["power"]:
                win["-power-"].update(text="入退室処理 有効", button_color="white on green")
            else:
                win["-power-"].update(text="入退室処理 無効", button_color="white on red")

            # NFCの状態表示を更新
            if const.states["nfc"] == const.DISCONNECTED:
                win["-nfcstate-"].update(
                    "NFCカードリーダが接続されていません", background_color="red", text_color="white"
                )
            elif (
                const.states["nfc"] == const.CONNECTED
                and const.states["system"] == const.ENABLED
            ):
                win["-nfcstate-"].update(
                    "カードをタッチすると，生徒の入退室処理が実行されます",
                    background_color="green",
                    text_color="white",
                )
            elif (
                const.states["nfc"] == const.CONNECTED
                and const.states["system"] == const.DISABLED
            ):
                win["-nfcstate-"].update(
                    "カードをタッチしても，入退室処理を行いません",
                    background_color="yellow",
                    text_color="black",
                )

            # 現在時刻の更新
            const.hour = datetime.datetime.now().hour
            const.minute = datetime.datetime.now().minute
            const.second = datetime.datetime.now().second
            win["-time-"].update(
                "%02d:%02d:%02d" % (const.hour, const.minute, const.second)
            )

            # システム状態切り替えトグルボタン
            if event == "-power-":
                toggles["power"] = not toggles["power"]  # トグルの状態を反転
                if toggles["power"]:
                    if const.states["nfc"] == const.DISCONNECTED:
                        sg.popup_ok(
                            "入退室処理を有効化できません。有効化するには，NFCカードリーダが正常に接続されていることを確認し，システムを再起動してください。",
                            title="システムエラー",
                            keep_on_top=True,
                            modal=True,
                        )
                        toggles["power"] = not toggles["power"]  # トグルの状態を元に戻す
                        continue
                    if (
                        sg.popup_yes_no(
                            "入退室処理を有効化すると，カードがタッチされると生徒の入退室処理が実行されるようになります。よろしいですか？",
                            title="システム有効化の確認",
                            keep_on_top=True,
                            modal=True,
                        )
                        == "Yes"
                    ):
                        const.states["system"] = const.ENABLED  # 入退室処理を有効化
                        print("[Info] 入退室処理が有効化されました")
                        if const.states["nfc"] == const.CONNECTED:
                            print(
                                "[Attention] 現在の状態でNFCカードリーダにカードをタッチすると，生徒の入退室処理が実行されます。これは，タッチされたカードの生徒の保護者へのメール送信などが行われることを意味します。不用意にカード操作を行わないようにしてください。"
                            )
                else:
                    const.states["system"] = const.DISABLED  # システムを無効化
                    print("[Info] 入退室処理が無効化されました")
                    if const.states["nfc"] == const.CONNECTED:
                        print(
                            "[Info] 現在の状態でNFCカードリーダにカードをタッチしても，入退室処理を行いません。カードをタッチしても安全です。"
                        )

            # データベース管理パネルのボタン
            if event == "-show_all_students-":
                print_formatted_list(db.execute_database("SELECT * FROM student"))
            elif event == "-show_all_system_logs-":
                print_formatted_list(db.execute_database("SELECT * FROM system_log"))
            elif event == "-add_student-":
                if const.states["system"] == const.DISABLED:
                    windows["add_student"] = add_student_window.get_window()
                else:
                    sg.popup_ok(
                        "生徒を登録するには，入退室処理を無効化してください。有効化中にこの操作は行えません。",
                        title="エラー",
                        keep_on_top=True,
                        modal=True,
                    )
            elif event == "-remove_student-":
                if const.states["system"] == const.DISABLED:
                    windows["remove_student"] = remove_student_window.get_window()
                else:
                    sg.popup_ok(
                        "生徒を除名するには，入退室処理を無効化してください。有効化中にこの操作は行えません。",
                        title="エラー",
                        keep_on_top=True,
                        modal=True,
                    )

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

        # 生徒登録画面
        elif "add_student" in windows and win == windows["add_student"]:
            if event == "-register-":
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

        # 生徒除名画面
        elif "remove_student" in windows and win == windows["remove_student"]:
            if event == "-remove-":
                if values["-st_name-"] == "":
                    sg.PopupOK(
                        "除名する生徒の名前を入力してください。",
                        title="生徒除名エラー",
                        keep_on_top=True,
                        modal=True,
                    )
                    continue
                remove_student(values["-st_name-"])
            elif event == "-register_without_card-":
                windows["remove_student"].close()
                windows[
                    "remove_student_without_card"
                ] = remove_student_without_card_window.get_window()

        # 生徒除名画面（カードなし）
        elif (
            "remove_student_without_card" in windows
            and win == windows["remove_student_without_card"]
        ):
            if event == "-register-":
                if (
                    values["-st_name-"] == ""
                    or values["-st_age-"] == ""
                    or values["-st_gender-"] == ""
                    or values["-st_parentsname-"] == ""
                    or values["-st_mail_address-"] == ""
                ):
                    sg.PopupOK(
                        "除名する生徒の情報をすべて入力してください。",
                        title="生徒除名エラー",
                        keep_on_top=True,
                        modal=True,
                    )
                    continue
                remove_student_without_card(
                    values["-st_name-"],
                    values["-st_age-"],
                    values["-st_gender-"],
                    values["-st_parentsname-"],
                    values["-st_mail_address-"],
                )


def register_student(
    name: str, age: int, gender: str, parent_name: str, mail_address: str
):  # 生徒を登録
    """
    生徒を登録します。

    Args:
        name (str): 登録する生徒の名前
        age (int): 登録する生徒の年齢
        gender (str): 登録する生徒の性別
        parent_name (str): 登録する生徒の保護者の名前
        mail_address (str): 登録する生徒の保護者のメールアドレス
    """
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
            sg.popup_ok("生徒の登録を完了しました。: " + name, title="完了", keep_on_top=True, modal=True)


def remove_student(name: str):
    """
    生徒の名前とカード情報を使用して，生徒を除名します。入力された名前とカードの名前を照合して，一致すれば除名を行います。

    Args:
        name (str): 除名する生徒の名前
    Returns:
        ret (int): 成功した場合は 0，失敗した場合は -1 を返す。
    """
    if (id := wait_card_popup("除名する生徒のカードをタッチしてください")) == -1:
        sg.popup_ok("生徒の除名がキャンセルされました。", title="キャンセル", keep_on_top=True, modal=True)
    else:
        ret = db.remove_student_from_database(id, name)
        if ret == -1:
            sg.popup_ok(
                "生徒の除名に失敗しました。このカードはデータベースに登録されていません。別のカードを試してください。詳細は，システム出力を参照してください。",
                title="エラー",
                keep_on_top=True,
                modal=True,
            )
        elif ret == -2:
            sg.popup_ok(
                "生徒の除名に失敗しました。入力された生徒の名前と，ICカードの登録されている名前が一致しません。別のカードを試してください。詳細は，システム出力を参照してください。",
                title="エラー",
                keep_on_top=True,
                modal=True,
            )
            return -1
        else:
            sg.popup_ok("生徒の除名を完了しました。: " + name, title="完了", keep_on_top=True, modal=True)
            


def remove_student_without_card(
    name: str, age: int, gender: str, parents_name: str, mail_address: str
):
    """
    生徒の情報データのみを使って，生徒を除名します。全て一致するデータが見つかれば，除名を行います。

    Args:
        name (str): 除名する生徒の名前
        age (int): 除名する生徒の年齢
        gender (str): 除名する生徒の性別
        parents_name (str): 除名する生徒の保護者の名前
        mail_address (str): 除名する生徒の保護者のメールアドレス
    """
    students = db.execute_database(
        "SELECT * FROM student natural join on student.id = parent.id"
    )
    print(students)
    for student in students:
        if (
            student[0] == name
            and student[1] == age
            and student[2] == gender
            and student[3] == parents_name
            and student[4] == mail_address
        ):
            id = student["id"]
            sg.popup_yes_no(
                "入力された情報に一致する生徒が見つかりました。: \n氏名: %s\n年齢: %s\n性別: %s\n保護者の氏名: %s\n保護者のメールアドレス: %s\n\nこの生徒を除名を実行してよろしいですか？"
                % name,
                age,
                gender,
                parents_name,
                mail_address,
                title="除名の確認",
                keep_on_top=True,
                modal=True,
            )

    sg.popup_ok(
        "入力された情報に一致する生徒が見つからなかったため，除名できませんでした。入力した情報が正しいか，もう一度確認してください",
        title="除名エラー",
        keep_on_top=True,
        modal=True,
    )


def init_system():  # 初期化
    print("[Info] system initializing...")

    # if os.name != "nt":
    #     sg.popup_ok(
    #         "本システムは，Windows以外での動作は保証されていません。Windows以外のプラットフォーム上での動作は，思いもよらぬ誤動作を招く可能性があります。",
    #         title="警告",
    #         keep_on_top=True,
    #         modal=True,
    #     )
    if db.connect_to_database() == -1:  # データベースに接続する
        print("[Error] Couldn't connect to database.")

    if (
        ml.login_smtp("robotomiline@gmail.com", "gzmt tjim egtb fwad") == -1
    ):  # SMTPサーバーにログイン
        print("[Error] Couldn't login to SMTP server.")

    if (not const.ignore_nfc_error) and (nfc.connect_reader() == -1):
        const.states["nfc"] = const.DISCONNECTED
        const.states["system"] = const.DISABLED
        print("[Error] Couldn't connect to NFC reader.")
        sg.popup_ok(
            "NFCカードリーダに接続できませんでした。NFCカードリーダが正常に接続されていることを確認してから，システムを再起動してください。",
            title="NFCカードリーダ接続エラー",
            keep_on_top=True,
            modal=True,
        )
    else:
        const.states["nfc"] = const.CONNECTED
        threading.Thread(
            target=nfc.nfc_update_sub_thread, daemon=True
        ).start()  # NFCの更新を行うスレッドを起動

    db.add_systemlog_to_database("システム起動")  # システムログに記録
    print("[Info] system initialized.")


def popup_window(layout, duration=0):
    """
    ポップアップウィンドウを作成します。

    Args:
        layout (list): pysimpleguiのレイアウト
        duration (int, optional): ウィンドウを表示する時間（秒）. Defaults to 0.
    Returns:
        window (sg.Window): ウィンドウ
    """
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
                font=("Arial", 20, "bold"),
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
        [sg.Button("キャンセル", font=("Arial", 20, "bold"), key="-exit-", expand_x=True)],
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
