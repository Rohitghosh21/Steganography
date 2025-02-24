from PIL import Image

def encrypt_image(image_path, message, output_path):
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = img.load()

    message += '\0'  # Null character to mark the end of the message
    message_bits = ''.join(format(ord(char), '08b') for char in message)

    idx = 0
    for i in range(img.width):
        for j in range(img.height):
            r, g, b = pixels[i, j]
            if idx < len(message_bits):
                r = (r & ~1) | int(message_bits[idx])
                idx += 1
            if idx < len(message_bits):
                g = (g & ~1) | int(message_bits[idx])
                idx += 1
            if idx < len(message_bits):
                b = (b & ~1) | int(message_bits[idx])
                idx += 1
            pixels[i, j] = (r, g, b)

    img.save(output_path)