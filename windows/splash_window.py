import PySimpleGUI as sg

import config.values as const


def get_window():
    layout = [
        [
            sg.Image(
                filename=const.SPLASH_IMAGE_PATH,
                size=(840, 480),
                pad=((0, 0), (0, 0)),
                expand_x=True,
                expand_y=True,
            ),
        ],
    ]

    window = sg.Window(
        "splash screen",
        layout,
        no_titlebar=True,
        keep_on_top=True,
        size=(840, 480),
    )

    return window


if __name__ == "__main__":  # テスト用
    window = get_window()
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
    window.close()
