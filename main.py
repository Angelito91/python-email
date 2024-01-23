import flet as ft
from views.home import Home


def main(page: ft.Page):
    page.title = "Python Email"
    page.scroll = ft.ScrollMode.AUTO
    page.auto_scroll = True
    page.window_max_height = 600
    page.window_min_height = 600
    page.window_max_width = 500
    page.window_min_width = 500

    page.appbar = ft.AppBar(
        leading_width=10,
        title=ft.Text("Python Email", color=ft.colors.CYAN_300),
        center_title=False,
        bgcolor=ft.colors.SURFACE_VARIANT
    )

    def close_banner(e):
        page.banner.open = False
        page.update()

    page.banner = ft.Banner(
        actions=[
            ft.TextButton("OK", on_click=close_banner),
        ]
    )

    page.add(Home(page))


if __name__ == "__main__":
    ft.app(main)
