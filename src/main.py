import flet as ft
from tabs.formatter import formatter_tab


class Destination:
    def __init__(self, icon: str|ft.Icon, selected_icon: str|ft.Icon, label: str, body: ft.Control):
        self.icon = icon
        self.selected_icon = selected_icon
        self.label = label
        self.body = body


async def main(page: ft.Page):

    page.appbar = ft.AppBar(
        leading=ft.Container(padding=5, content=ft.Image(src="icon.png")),
        leading_width=40,
        title=ft.Text("Hydra"),
        center_title=True,
        bgcolor=ft.Colors.INVERSE_PRIMARY,
    )


    destinations = [
        Destination(
            icon=ft.Icons.RUN_CIRCLE_OUTLINED,
            selected_icon=ft.Icons.RUN_CIRCLE,
            label="Formatter",
            body=formatter_tab(page)
        ),
        Destination(
            icon=ft.Icon(ft.Icons.BOOKMARK_BORDER),
            selected_icon=ft.Icon(ft.Icons.BOOKMARK),
            label="Generator",
            body=ft.Container(
               content=ft.Text("This is the second content area"),
            ),
        ),
        Destination(
            icon=ft.Icons.SETTINGS_OUTLINED,
            selected_icon=ft.Icon(ft.Icons.SETTINGS),
            label="Settings",
            body=ft.Container(
               content=ft.Text("3 This is the second content area"),
            ),
        ),
    ]

    view = ft.Container(
        content = destinations[0].body,
        expand=True,
    )

    def change_destination(e):
        view.content = destinations[e.control.selected_index].body
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=80,
        width=80,
        group_alignment=-0.9,
        destinations=[
            ft.NavigationRailDestination(
                icon=d.icon,
                selected_icon=d.selected_icon,
                label=d.label,
            ) for d in destinations],
        on_change=change_destination,
    )

    page.add(
        ft.Row(
            [
                rail,
                ft.VerticalDivider(width=1),
                view
            ],
            expand=True,
        )
    )


ft.app(main)