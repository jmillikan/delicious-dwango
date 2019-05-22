#!/usr/bin/python3

class StandardHexProtocol():
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

    def get_cord(self, x ,y):
        return ''.join([str(x), ',', str(y)])

    def get_color_rgb(self, r, g, b, a=255):
        r2 = hex(r)[2:].rjust(2,'0')
        g2 = hex(g)[2:].rjust(2,'0')
        b2 = hex(b)[2:].rjust(2,'0')
        d = ['#', r2, g2, b2]
        if a != 255:
            d.append(hex(a)[2:].rjust(2, '0'))
        return ''.join(d)

    def get_color_hex(self, hexcolor):
        return ''.join(['#', hexcolor])

    def generate_messages(self, data):
        messages = []
        for color, pixels in data.items():
            current_message = color + ' '
            for pixel in pixels:
                if len(current_message) != len(color)+1:
                    new_message = current_message + ';' + pixel
                else:
                    new_message = current_message + pixel
                if len(new_message) > 500:
                    messages.append(current_message)
                    current_color = color
                    current_message = color + ' ' + pixel
                else:
                    current_message = new_message
            messages.append(current_message)
        return messages


class UnicodeProtocol():
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y

    def get_cord(self, x ,y):
        return chr(0x02FA1E + (self.size_x * y) + x)

    def get_color_rgb(self, r, g, b ,a=255):
        color_rg = chr(0x100000 | r << 8 | g)
        color_ba = chr(0x100000 | b << 8 | a)
        return color_rg + color_ba

    def get_color_hex(self, hexcolor):
        r = int(hexcolor[0:2], 16)
        g = int(hexcolor[2:4], 16)
        b = int(hexcolor[4:6], 16)
        if len(hexcolor) == 6:
            a = 255
        else:
            a = int(hexcolor[6:8], 16)
        return self.get_color_rgb(r, g, b, a)

    def generate_messages(self, data):
        messages = []
        current_message = ''
        last_color = ''
        for color, pixels in data.items():
            if current_message == '':
                current_message = color
                last_color = color
            for pixel in pixels:
                if last_color != color:
                    new_message = current_message + color + pixel
                else:
                    new_message = current_message + pixel
                if len(new_message) > 500:
                    messages.append(current_message)
                    current_message = color + pixel
                    last_color = color
                else:
                    current_message = new_message
        messages.append(current_message)
        return messages
