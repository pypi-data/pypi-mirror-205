# Routing_flet -> Enrutamiento y protección de paginas facil con flet
---
# instalar
```
pip install Routing-flet
```
# Actualizar
```
pip install Routing-flet --upgrade
```
---
# Ejemplo:
```
import flet as ft
from Routing_flet import RoutePage

def main(page: ft.Page):

    ruta = RoutePage(page)
    ruta.run()

ft.app(target=main, view=ft.WEB_BROWSER, port=9999, route_url_strategy='hash')
```