import flet as ft
import asyncio


class CancelToken:
    def __init__(self):
        self.stopped = False

    def cancel(self):
        self.stopped = True

    def reset(self):
        self.stopped = False


class Console(ft.Container):
    def __init__(self):
        super().__init__(expand=True)
        self.margin = ft.Margin(10, 50, 10, 10)  

        self.progress_ring = ft.ProgressRing(visible=False, width=20, height=20)
        self.console_txt = ft.TextField(
            value="",
            read_only=True,
            multiline=True,
            expand=True,
            border=ft.InputBorder.NONE,
        )

        self.cancel_token = CancelToken()

        self.cancel_button = ft.ElevatedButton(
            text="Cancel",
            icon=ft.Icons.CANCEL_ROUNDED,
            color=ft.Colors.RED,
            tooltip="Pause record",
            on_click=lambda _: self.cancel_token.cancel(),
            visible = False
        )


        self.content = ft.Column([
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Run",
                        icon=ft.Icons.PLAY_CIRCLE_FILL_ROUNDED,
                        color=ft.Colors.GREEN,
                        on_click=self.start,
                        tooltip="Execute selected command",
                    ),
                    ft.ElevatedButton(
                        text="Clean",
                        icon=ft.Icons.CLEANING_SERVICES_ROUNDED,
                        color=ft.Colors.ORANGE,
                        tooltip="Pause record",
                        on_click=lambda _: self.clear_console(),
                    ),
                    self.cancel_button,
                    self.progress_ring,
                ],
            ),
            ft.Card(
                content=ft.Container(
                    content=self.console_txt, padding=ft.padding.all(10)
                ),
                expand=True,
            ),
        ])
        self.expand = True

        self.script = ""

    async def start(self, e):
        self.cancel_button.visible = True
        self.cancel_token.reset()

        self.console_txt.value = ""
        self.progress_ring.visible = True
        self.update()

        proc = await asyncio.create_subprocess_shell(
            f"PYTHONUNBUFFERED=1 {self.script}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        async def read_stream(stream):
            while True:
                if self.cancel_token.stopped:
                    proc.kill()
                    break

                line = await stream.readline()
                if not line:
                    break
                self.console_txt.value += line.decode()
                self.update()

        await asyncio.gather(read_stream(proc.stdout), read_stream(proc.stderr))

        self.cancel_button.visible = False
        self.progress_ring.visible = False
        self.update()

    def clear_console(self):
        self.console_txt.value = ""
        self.update()
