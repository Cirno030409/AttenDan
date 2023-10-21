import PySimpleGUI as sg


def show_window():
    layout = [
        [
            sg.Text("Add Student", font=("Arial", 25)),
        ]
    ]

    window = sg.Window(
        "生徒の新規追加",
        layout,
        keep_on_top=True,
        finalize=True,
    )
