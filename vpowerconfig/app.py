import flet as ft


def main(page: ft.Page):
    page.title = "サンプル"
    t = ft.Text(value="Hello, world!", color="black")
    page.controls.append(t)
    page.update()


def start():
    ft.app(target=main)
