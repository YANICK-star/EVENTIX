import qrcode

url = 'https://d30286483f9fb4.lhr.life'
img = qrcode.make(url)
img.save('static/images/public_qr.png')
print(f"[OK] Generated public QR code for {url} -> static/images/public_qr.png")
