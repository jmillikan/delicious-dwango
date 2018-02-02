import argparse
import itertools

import imageio
from colors import colors

delicious_color_keys = ['liliac', 'cream', 'creme', 'orangeish', 'wine', 'pear', 'butter', 'blood', 'maize', 'sunflower', 'avocado', 'mushroom', 'saffron', 'russet', 'cranberry', 'aqua', 'bordeaux', 'rose', 'pumpkin', 'orange', 'chocolate', 'cocoa', 'raspberry', 'pistachio', 'watermelon', 'caramel', 'tomato', 'lime', 'lemon', 'goldenrod', 'velvet', 'chestnut', 'mint', 'apricot', 'merlot', 'wheat', 'celery', 'mulberry', 'melon', 'claret', 'banana', 'pea', 'grape', 'cherry', 'grapefruit', 'eggshell', 'lilac', 'salmon', 'cornflower', 'wintergreen', 'kiwi', 'cinnamon', 'sage', 'asparagus', 'berry', 'peach', 'mango', 'ice', 'burgundy', 'mocha', 'blurple', 'burple', 'tangerine', 'spearmint', 'bubblegum', 'eggplant', 'squash', 'butterscotch', 'blueberry', 'custard', 'apple', 'olive', 'seaweed', 'coffee', 'mustard', 'strawberry', 'aubergine', 'plum']

delicious_colors = {name: colors[name] for name in delicious_color_keys}

def color_dist(c1, c2):
    return (c1["r"] - c2["r"]) ** 2 + (c1["g"] - c2["g"]) ** 2 + (c1["b"] - c2["b"]) ** 2

def closest_delicious_color(c): 
    return min(delicious_colors, key=lambda k: color_dist(delicious_colors[k], c))

def map_image(fn, im):
    (h,w,_) = im.shape
    def to_rgb(a):
        if len(a) == 3:
            [r,g,b] = a
        else:
            [r,g,b,_] = a
        return {"r": r, "g": g, "b": b}
    def trans(p):
        a = 1
        if len(p) == 3:
            [r,g,b] = p
        else:
            [r,g,b,a] = p
        return a == 0
    return [fn(to_rgb(im[y][x]), y, x) for x in range(w) for y in range(h) if not trans(im[y][x])]

def delicious_pixels(im):
    return map_image(lambda c,y,x: {"c": closest_delicious_color(c), "y": y, "x": x}, im)

# I got x and y swapped... Fix here.
def delicious_commands(im, yoff, xoff, window):
    def pixel_color(pix): return pix["c"]
    def pixel_coords(pix): return str(pix['x'] + xoff) + ',' + str(pix['y'] + yoff)
    
    p = sorted(delicious_pixels(im), key=pixel_color)

    color_pixels = itertools.groupby(p, pixel_color)

    commands = []

    for c, vs in color_pixels:
        pixels = list(vs)

        i = 0

        while i < len(pixels):
            print(c + ' ' + ';'.join(map(pixel_coords, pixels[i:i+window])))
            i += window

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Give dwango chat commands for drawing an image in a delicious fashion.')
    parser.add_argument("imagefile", type=str)
    parser.add_argument("--window", type=int, default=5)
    parser.add_argument("--yoff", type=int, default=0)
    parser.add_argument("--xoff", type=int, default=0)
    parser.add_argument("--gross", action='store_true')

    args = parser.parse_args()

    if(args.gross):
        delicious_colors = colors

    im = imageio.imread(args.imagefile)
    print(im.shape)

    delicious_commands(im, args.yoff, args.xoff, args.window)
