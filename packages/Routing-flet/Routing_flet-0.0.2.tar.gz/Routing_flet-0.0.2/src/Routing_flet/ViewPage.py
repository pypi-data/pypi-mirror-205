from flet import Page, View, Column, Text, MainAxisAlignment, CrossAxisAlignment


class ViewPage:
    """ 
    Usar el siguiente metodo dentro de la clase si se requiere un login requerido a la página (True: para acceder | None: Por defecto) o denegar (False: Renvia a la ruta -> '/' )
    ```
    def login_requi(self):
        return None
    ```
    ---
    El metodo que se hereda en la clase -> def math_url(self): si no se desea una url dinámica no se agrega a la nueva clase creada, ya que por defecto es None.
    ```
    def math_url(self):
        return None
    ```
    ---
    Ejemplo de un enrutamiento dinámico:
    ```
    import flet as ft
    from Routing_flet import ViewPage

    class View(ViewPage):
        def __init__(self) -> None:
            self.route = '/about/1/2'

        def math_url(self):
            return ['id', 'name', 'edad']

        def view(self, page: ft.Page):
            page.title = 'contact'
            return ft.View(
                self.route,
                controls=[
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Text('index about', size=50),
                                width=450,
                                height=450,
                                bgcolor='green800',
                                alignment=ft.alignment.center,
                            ),
                            ft.FilledButton(
                                'ir a index',
                                width=120,
                                height=40,
                                on_click=lambda e:e.page.go('/')
                            ),
                        ]
                    )
                ],
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
    ``` 
    """

    def __init__(self) -> None:
        self.route = '/'

    def math_url(self) -> dict:
        return None

    def route(self) -> str:
        return self.route
    
    def login_requi(self):
        return None

    def view(self, page: Page):
        page.title = 'WiewPage'
        return View(
            self.route,
            controls=[
                Column(
                    Text('View Page', size=90)
                )
            ],
            vertical_alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER
        )
