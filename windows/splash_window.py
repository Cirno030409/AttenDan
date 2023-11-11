import PySimpleGUI as sg

import config.values as const


def get_window():
    layout = [
        [
            sg.Text(
                "" + const.SYSTEM_NAME + " ver. " + const.VERSION,
                font=("Arial", 20, "bold"),
                justification="center",
            )
        ],
    ]

    window = sg.Window(
        "splash screen",
        layout,
        no_titlebar=True,
        keep_on_top=True,
        size=(600, 400),
    )

    return window


if __name__ == "__main__":  # テスト用
    window = get_window()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()
