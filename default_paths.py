from pathlib import Path
user_home = Path.home()
root_path = user_home.joinpath(".Gerencial Facil")
clients_path = root_path.joinpath("clientes")
products_path = root_path.joinpath("produtos")
reports_path = root_path.joinpath("relatorios")
config_path = root_path.joinpath("config")
qrcode_path = config_path.joinpath("qrcode.png")
icon_windows = config_path.joinpath("iconwindows.ico")
icon_linux = config_path.joinpath("iconlinux.png")
icon_mac = config_path.joinpath("iconmac.icns")
icon_bitmap = config_path.joinpath("icon_bitmap.bmp")