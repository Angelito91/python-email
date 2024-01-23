import flet as ft
from utils.utils import validator_email, send_email_message, create_message
from config import EMAIL, PASSWORD


class Home(ft.UserControl):
    def __init__(self, page):
        # Todos los controls
        self.page = page

        self.asunto = ft.TextField(label='Asunto', hint_text='De que trata?',
                                   border=ft.InputBorder.UNDERLINE, prefix_icon=ft.icons.PERSON_2_OUTLINED, max_length=50, autocorrect=True, autofocus=True)

        self.destino = ft.TextField(label='Destinatario', hint_text='A quien deseas enviar el correo?',
                                    border=ft.InputBorder.UNDERLINE, prefix_icon=ft.icons.EMAIL, enable_suggestions=True)

        self.contenido = ft.TextField(label="Contenido", hint_text='Hola como estas?', border=ft.InputBorder.UNDERLINE,
                                      prefix_icon=ft.icons.BOOK_OUTLINED, multiline=True, min_lines=5, max_lines=8, max_length=400)

        self.cancel = ft.ElevatedButton(
            "Cancelar", icon="cancel", on_click=self.on_cancel, color='red', style=ft.ButtonStyle(padding=20), width=230)

        self.accept = ft.ElevatedButton(
            "Enviar", icon="send", on_click=self.on_submit, color=ft.colors.CYAN, style=ft.ButtonStyle(padding=20), width=230)

        super().__init__()

    def on_cancel(self, e):
        # Limpiar todos los campos
        self.asunto.value = ""
        self.asunto.error_text = None
        self.destino.value = ""
        self.destino.error_text = None
        self.contenido.value = ""
        self.contenido.error_text = None
        self.page.banner.open = False
        self.page.update()
        self.update()

    def on_submit(self, e):
        # Comprobar que todos los campos estan correctos para enviar
        correct = True

        if len(self.asunto.value.strip()) == 0:
            self.asunto.error_text = "Te falta escribir un asunto"
            correct = False

        if not validator_email(self.destino.value):
            self.destino.error_text = "No es un email válido. Debe terminar **@gmail.com"
            correct = False

        if len(self.contenido.value.strip()) == 0:
            self.contenido.error_text = "Te falta escribir un contenido"
            correct = False

        if not EMAIL or not PASSWORD:
            # creando banner para indicar al usuario de que falta variables de entorno
            self.page.banner.content = ft.Text("Te falta configurar en las variables de entorno, tu email y la contraseña.", color=ft.colors.AMBER)
            self.page.banner.leading = ft.Icon(
                ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40)
            self.page.banner.actions.append(ft.TextButton("Más información...", url="https://google.com"))
            self.page.banner.open = True
            self.page.update()
            self.page.banner.actions.pop()

            correct = False

        if correct:
            self.page.banner.actions.remove()
            self.page.banner.open = False
            self.page.update()

            msg = create_message(self.asunto.value, EMAIL,
                                 self.destino.value, self.contenido.value)

            success = send_email_message(msg, EMAIL, PASSWORD)

            if success:
                # creando banner para indicar al usuario que se envio el mensaje
                self.page.banner.content = ft.Text(
                    "El mensaje ha sido enviado con éxito.", color=ft.colors.GREEN)
                self.page.banner.leading = ft.Icon(
                    ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=40)
                self.page.banner.open = True
                self.page.update()

            elif success == None:
                # creando banner para indicar al usuario que las variables de entorno son incorrectas
                self.page.banner.content = ft.Text(
                    "El usuario o la contraseña de las variables de entorno son incorrectos", color=ft.colors.AMBER)
                self.page.banner.leading = ft.Icon(
                    ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40)
                self.page.banner.open = True
                self.page.update()

            else:
                # creando banner para indicar al usuario que hubo un error
                self.page.banner.content = ft.Text(
                    "Hubo un error al enviar el mensaje, por favor revise su conexión a internet y vulva a intentar",  color=ft.colors.RED)
                self.page.banner.leading = ft.Icon(
                    ft.icons.ERROR_ROUNDED, color=ft.colors.RED, size=40)
                self.page.banner.open = True
                self.page.update()

        self.update()

    def build(self):
        return ft.Column([
            self.asunto,
            self.destino,
            self.contenido,
            ft.Row([
                self.cancel,
                self.accept
            ],
                alignment='center'
            )],
        )
