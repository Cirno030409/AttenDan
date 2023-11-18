import PySimpleGUI as sg


def get_window():
    layout = [
        [
            sg.Text(
                "生徒を新規に登録します。登録する生徒の情報を入力してください。登録ボタンを選択後，登録するICカードをタッチしてください。",
                font=("Arial", 10),
                justification="center",
                expand_x=True,
                tooltip="生徒の名前",
                pad=((0, 20), (0, 20)),
            ),
        ],
        [
            sg.Text(
                "氏名:",
                font=("Arial", 15),
                justification="left",
                pad=((20, 0), (0, 0)),
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
            sg.Text(
                "年齢:",
                font=("Arial", 15),
                justification="left",
                pad=((20, 0), (0, 0)),
                tooltip="生徒の年齢",
            ),
            sg.InputText(
                size=(50, 1),
                font=("Arial", 15),
                key="-st_age-",
                pad=((0, 0), (0, 0)),
                tooltip="生徒の年齢を入力します",
                expand_x=True,
            ),
        ],
        [
            sg.Text(
                "性別:",
                font=("Arial", 15),
                justification="left",
                pad=((20, 0), (0, 0)),
                tooltip="生徒の性別",
            ),
            sg.InputText(
                size=(50, 1),
                font=("Arial", 15),
                key="-st_gender-",
                pad=((0, 0), (0, 0)),
                tooltip="生徒の性別を入力します",
                expand_x=True,
            ),
        ],
        [
            sg.Text(
                "保護者の氏名:",
                font=("Arial", 15),
                justification="left",
                pad=((20, 0), (0, 0)),
                tooltip="生徒の保護者の氏名",
            ),
            sg.InputText(
                size=(50, 1),
                font=("Arial", 15),
                key="-st_parentsname-",
                pad=((0, 0), (0, 0)),
                tooltip="生徒の保護者の氏名を入力します",
                expand_x=True,
            ),
        ],
        [
            sg.Text(
                "連絡用メールアドレス:",
                font=("Arial", 15),
                justification="left",
                pad=((20, 0), (0, 0)),
            ),
            sg.InputText(
                size=(50, 1),
                font=("Arial", 15),
                key="-st_mail_address-",
                pad=((0, 0), (0, 0)),
                tooltip="出欠の連絡に使用する保護者への連絡用のメールアドレスを入力します",
                expand_x=True,
            ),
        ],
        [
            sg.Button(
                "登録",
                size=(10, 2),
                key="-register-",
                tooltip="生徒を登録するときは，このボタンを押すか，IDカードをかざします",
                expand_x=True,
                pad=((20, 20), (20, 0)),
            ),
        ],
    ]

    window = sg.Window(
        "生徒の新規登録",
        layout,
        finalize=True,
    )

    return window
