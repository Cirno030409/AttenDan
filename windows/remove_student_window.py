import PySimpleGUI as sg


def get_window():
    layout = [
        [
            sg.Text(
                "生徒を除名します。除名された生徒に関連する情報は，データベースから全て消去されます。復元することはできません。",
                font=("Arial", 10),
                justification="center",
                expand_x=True,
                tooltip="生徒の名前",
                pad=((0, 20), (0, 10)),
            ),
        ],
        [
            sg.Text(
                "除名する生徒の氏名を入力し，除名ボタンを押下して当該生徒のカードをタッチしてください:",
                font=("Arial", 10),
                justification="left",
                pad=((0, 10), (0, 30)),
            ),
        ],
        [
            sg.Text(
                "除名する生徒の氏名:",
                font=("Arial", 15),
                justification="left",
                pad=((10, 0), (0, 0)),
                tooltip="生徒の名前",
            ),
            sg.InputText(
                size=(50, 1),
                font=("Arial", 15),
                key="-st_name-",
                pad=((0, 0), (0, 0)),
                tooltip="生徒の名前を入力します",
                expand_x=True,
            ),
        ],
        [
            sg.Button(
                "除名",
                size=(20, 2),
                key="-remove-",
                tooltip="生徒を除名するときは，このボタンを押すか，IDカードをかざします",
                expand_x=True,
                pad=((20, 20), (20, 0)),
            ),
        ],
        [
            sg.Button(
                "カード情報を使わずに除名...",
                size=(20, 2),
                key="-register_without_card-",
                tooltip="カードを紛失したり，カードが使えない場合は，このボタンを押して除名します",
                expand_x=True,
                pad=((20, 20), (20, 0)),
            )
        ],
    ]

    window = sg.Window(
        "生徒の除名",
        layout,
        finalize=True,
    )

    return window


if __name__ == "__main__":
    window = get_window()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()
