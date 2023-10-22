import PySimpleGUI as sg

import config.values as const


def get_window():
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
        size=(550, 200),
        vertical_alignment="top",
        expand_x=True,
    )  # 幅,高さ

    # システムログのフレーム
    frame_system_log = sg.Frame(
        "システム出力",
        [
            # テキストレイアウト
            [
                sg.Multiline(
                    size=(130, 100),
                    font=("Arial", 12),
                    key="-log-",
                    echo_stdout_stderr=True,
                    disabled=True,
                    autoscroll=True,
                    reroute_stdout=True,
                    reroute_cprint=True,
                    reroute_stderr=True,
                    write_only=True,
                    do_not_clear=True,
                    expand_y=True,
                    background_color="black",
                    text_color="light green",
                )
            ],
        ],
        vertical_alignment="top",
        # expand_y=True,
        expand_x=True,
    )

    # システム状態切り替えボタンのフレーム
    frame_system_info = sg.Frame(
        "システム状態",
        [
            [
                sg.Button(
                    "システム動作中",
                    font=("Arial", 30, "bold"),
                    button_color="white on green",
                    key="-power-",
                    tooltip="システムの有効化/無効化を切り替えます",
                    expand_x=True,
                    expand_y=True,
                ),
            ],
        ],
        size=(550, 120),
        vertical_alignment="top",
    )  # 幅,高さ

    # SQLコマンドのフレーム
    frame_db__control = sg.Frame(
        "データベース管理",
        [
            [
                sg.Button(
                    "生徒の一覧の表示",
                    key="-show_all_students-",
                    tooltip="データベースにある生徒の一覧をすべて表示します",
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
                    "生徒の新規追加",
                    key="-add_student-",
                    tooltip="新規に生徒を登録します",
                    expand_x=True,
                    auto_size_button=False,
                    size=(15, 1),
                ),
                sg.Button(
                    "生徒の除名",
                    key="-remove_student-",
                    tooltip="新規に生徒を登録します",
                    expand_x=True,
                    auto_size_button=False,
                    size=(15, 1),
                ),
            ],
        ],
        expand_x=True,
        expand_y=True,
    )
    frame_sql_control = sg.Frame(
        "SQLでのデータベース管理（高度）",
        [
            [
                sg.Text(
                    "SQLの実行:",
                    font=("Arial", 15),
                    justification="left",
                    expand_x=True,
                    expand_y=True,
                    pad=((0, 0), (0, 0)),
                    tooltip="データベースの管理",
                    key="-state-",
                ),
                sg.InputText(
                    size=(50, 1),
                    font=("Arial", 15),
                    key="-sql-",
                    tooltip="実行するSQL文を入力します",
                    background_color="black",
                    text_color="light green",
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
        size=(550, 120),
        expand_x=True,
        expand_y=True,
    )

    # フレームを縦に並べる
    col1 = [
        [frame_system_info],
        [frame_main_control],
        [frame_db__control],
        [frame_sql_control],
    ]
    col2 = [
        [frame_system_log],
    ]
    tab_main = [
        [sg.Column(col1, vertical_alignment="top"), sg.Column(col2)],
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

    # NFCの待機状態を表示するフレーム
    if const.state_nfc == const.DISCONNECTED:
        color = "red"
        msg = "カードリーダが接続されていません"
    elif const.state_nfc == const.STAND_BY:
        color = "green"
        msg = "カードをタッチしてください"

    layout = [
        [
            sg.Text(
                msg,
                background_color=color,
                text_color="white",
                font=("Arial", 20),
                expand_x=True,
                justification="center",
                key="-nfcstate-",
            ),
            sg.Text(
                "00:00:00",
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
                    ]
                ]
            )
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
