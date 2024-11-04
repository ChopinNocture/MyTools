import qrcode

# URL to be encoded
url = "http://footballgame.w1.luyouxia.net/UESite/sharescore/"
url = "http://footballgame.w1.luyouxia.net/UESite/shareprize/"

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
file_path = "E:/DevDocumnets/足球互动/qrcode_score.png"
file_path = "E:/Development/Packages/qrcode_prize.png"

img.save(file_path)
