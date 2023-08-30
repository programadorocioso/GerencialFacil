import qrcode
from PIL import Image
import io
import tkinter as tk
from PIL import Image
from processamento import pix_qrcode
# Gerar o QR Code
data = pix_qrcode()
qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
qr.add_data(data)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="black", back_color="white")

# Criar um objeto BytesIO para armazenar a imagem do QR Code
qr_image_stream = io.BytesIO()

# Salvar a imagem do QR Code no objeto BytesIO
qr_img.save(qr_image_stream, format="PNG")

# Voltar para o início do objeto BytesIO
qr_image_stream.seek(0)

# Criar um objeto ImageTk.PhotoImage a partir do objeto BytesIO
qr_image_tk = Image(Image.open(qr_image_stream))

# Criar uma janela do Tkinter
root = tk.Tk()

# Criar um rótulo para exibir a imagem do QR Code
label = tk.Label(root, image=qr_image_tk)
label.pack()

# Iniciar o loop principal do Tkinter
root.mainloop()