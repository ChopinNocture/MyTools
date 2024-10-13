import qrcode

# URL to be encoded
url = "https://baidu.com"

# Create QR code
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(url)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
file_path = "E:/DevDocumnets/足球互动/qrcode.png"
img.save(file_path)
