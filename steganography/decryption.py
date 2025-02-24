from PIL import Image

def decrypt_image(image_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    message_bits = []
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            message_bits.append(str(r & 1))
            message_bits.append(str(g & 1))
            message_bits.append(str(b & 1))

    message = ''
    for i in range(0, len(message_bits), 8):
        byte = ''.join(message_bits[i:i+8])
        if byte == '00000000':  # Null character marks the end
            break
        message += chr(int(byte, 2))

    return message