import PySimpleGUI as sg

import config.values as const


def get_window():
    # 入退室切り替えボタンのフレーム
    frame_system_info = sg.Frame(
        "システム状態",
        [
            [
                sg.Button(
                    "状態確認中...",
                    font=("Arial", 30, "bold"),
                    button_color="gray",
                    key="-power-",
                    tooltip="システムの有効化/無効化を切り替えます",
                    expand_x=True,
                    expand_y=True,
                ),
            ],
        ],
        expand_x=True,
        size=(100, 150),
        vertical_alignment="top",
    )  # 幅,高さ

    # 主な操作のフレーム
    frame_main_control = sg.Frame(
        "主な操作",
        [
            [
                sg.Button(
                    "テスト",
                    size=(10, 1),
                    key="-test-",
                    tooltip="新規に生徒を登録します",
                    expand_x=True,
                ),
            ],
        ],
        vertical_alignment="top",
        expand_x=True,
        expand_y=True,
    )  # 幅,高さ

    # データベース操作のフレーム
    frame_db_control = sg.Frame(
        "データベース管理",
        [
            [
                sg.Text(
                    "生徒の追加・除名など，データベースの管理や表示を行います",
                    font=("Arial", 10),
                    expand_x=True,
                    justification="center",
                ),
            ],
            [
                sg.Button(
                    "生徒の一覧の表示",
                    key="-show_all_students-",
                    tooltip="データベースにある生徒の一覧をすべて表示します",
                    expand_x=True,
                    auto_size_button=False,
                    size=(15, 1),
                ),
            ],
            [
                sg.Button(
                    "入退室ログの表示",
                    key="-show_all_logs-",
                    tooltip="データベースにある入退室ログをすべて表示します",
                    expand_x=True,
                    auto_size_button=False,
                    size=(15, 1),
                ),
                sg.Button(
                    "システムログの表示",
                    tooltip="システムログをすべて表示します",
                    key="-show_all_system_logs-",
                    expand_x=True,
                    auto_size_button=False,
                    size=(15, 1),
                ),
            ],
            [
                sg.Button(
                    "生徒の新規登録...",
                    key="-add_student-",
                    tooltip="新規に生徒を登録します",
                    expand_x=True,
                    auto_size_button=False,
                    size=(15, 1),
                ),
                sg.Button(
                    "生徒の除名...",
                    key="-remove_student-",
                    tooltip="新規に生徒を登録します",
                    expand_x=True,
                    auto_size_button=False,
                    size=(15, 1),
                ),
            ],
        ],
        expand_x=True,
        expand_y=False,
    )

    # SQL操作のフレーム
    frame_sql_control = sg.Frame(
        "SQLでのデータベース管理（高度）",
        [
            [
                sg.Text(
                    "SQLコマンドを使用して，データベースの管理を行います。",
                    font=("Arial", 10),
                    expand_x=True,
                    justification="center",
                ),
            ],
            [
                sg.Text(
                    "SQLの実行:",
                    font=("Arial", 15),
                    justification="left",
                    expand_x=True,
                    expand_y=True,
                    tooltip="データベースの管理",
                    key="-state-",
                ),
                sg.InputText(
                    font=("Arial", 15),
                    key="-sql-",
                    tooltip="実行するSQL文を入力します",
                    background_color="black",
                    text_color="light green",
                    expand_x=True,
                ),
            ],
            [
                sg.Button(
                    "実行",
                    font=("Arial", 13, "bold"),
                    size=(5, 1),
                    key="-execute-",
                    tooltip="入力されたSQL文を実行します",
                    expand_x=True,
                ),
            ],
            [
                sg.Button(
                    "コミット",
                    size=(10, 1),
                    key="-commit-",
                    tooltip="データベースの変更を確定します",
                    expand_x=True,
                ),
                sg.Button(
                    "ロールバック",
                    size=(10, 1),
                    key="-rollback-",
                    tooltip="データベースの変更を取り消します",
                    expand_x=True,
                ),
            ],
        ],
        expand_x=True,
        expand_y=False,
    )

    # システムログのフレーム
    frame_system_log = sg.Frame(
        "システム出力",
        [
            [
                sg.Multiline(
                    font=("Arial", 10),
                    key="-log-",
                    echo_stdout_stderr=True,
                    disabled=True,
                    autoscroll=True,
                    horizontal_scroll=True,
                    reroute_stdout=True,
                    reroute_cprint=True,
                    
                    write_only=True,
                    do_not_clear=True,
                    expand_x=True,
                    expand_y=True,
                    background_color="black",
                    text_color="light green",
                )
            ],
            [
                sg.Button(
                    "システム出力を別ウィンドウで表示...",
                    size=(50, 1),
                    key="-pop_log_win-",
                    expand_x=True,
                ),
            ],
        ],
        vertical_alignment="top",
        element_justification="left",
        size=(750, 500),
        expand_y=True,
    )

    # カラムレイアウト
    tab_main = [
        [
            sg.Column(
                [
                    [frame_system_info],
                    [frame_main_control],
                    [frame_db_control],
                    [frame_sql_control],
                ],
                vertical_alignment="top",
                justification="left",
                expand_x=True,
                # size=(600, 500),
                expand_y=True,
            ),
            sg.Column([[frame_system_log]], expand_x=False, expand_y=True),
        ],
    ]

    # 送信するメールを設定するタブ
    tab_entered_mail_mes_layout = [
        [
            sg.Text("入室時の送信するメールの内容を設定します"),
        ]
    ]
    tab_exited_mail_mes_layout = [
        [
            sg.Text("退室時の送信するメールの内容を設定します"),
        ]
    ]
    tab_set_mail_layout = [
        [
            sg.TabGroup(
                [
                    [sg.Tab("入室時", tab_entered_mail_mes_layout)],
                    [sg.Tab("退室時", tab_exited_mail_mes_layout)],
                ],
                expand_x=True,
                expand_y=True,
            )
        ]
    ]

    layout = [
        [
            sg.Text(
                "状態を確認しています...",
                background_color="gray",
                text_color="white",
                font=("Arial", 20, "bold"),
                expand_x=True,
                justification="center",
                key="-nfcstate-",
                tooltip="NFCリーダーの状態",
            ),
            sg.Text(
                "%02d:%02d:%02d" % (const.hour, const.minute, const.second),
                font=("Arial", 20, "bold"),
                key="-time-",
            ),
        ],
        [
            sg.TabGroup(
                [
                    [
                        sg.Tab("コントロールパネル", tab_main),
                        sg.Tab("メールの設定", tab_set_mail_layout),
                    ],
                ],
                expand_x=True,
                expand_y=True,
            ),
        ],
    ]

    window = sg.Window(
        const.SYSTEM_NAME + "  ver. " + const.VERSION,
        layout,
        resizable=False,
        finalize=True,
        size=(1300, 750),
        return_keyboard_events=True,
    )

    return window


if __name__ == "__main__":  # テスト用
    window = get_window()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()
