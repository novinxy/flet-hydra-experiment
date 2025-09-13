import shlex
import asyncio
import flet as ft

from tabs.console import Console


def formatter_tab(page):
    console = Console()
    console.script = "uv run script.py"
    console1 = Console()
    console1.script = "uv run pytest"
    console1.visible = False

    def change_console(e):
        console1.visible = not console1.visible
        console.visible = not console.visible
        page.update()

    options = ft.Dropdown(
        options=[
            ft.dropdown.Option("uv run script.py"),
            ft.dropdown.Option("uv run pytest"),
        ],
        label="Select command",
        on_change=change_console
    )


    return ft.Column(
        controls=[
            ft.Text("This is the Formatter tab"),
            options,
            console,
            console1
        ],
        expand=True,
    )
