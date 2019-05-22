#!/usr/bin/env python3

import argparse
import itertools
import math
import pprint

import imageio
import PBNHelper

from colors import colors

delicious_color_keys = ['liliac', 'cream', 'creme', 'orangeish', 'wine', 'pear', 'butter', 'blood', 'maize', 'sunflower', 'avocado', 'mushroom', 'saffron', 'russet', 'cranberry', 'aqua', 'bordeaux', 'rose', 'pumpkin', 'orange', 'chocolate', 'cocoa', 'raspberry', 'pistachio', 'watermelon', 'caramel', 'tomato', 'lime', 'lemon', 'goldenrod', 'velvet', 'chestnut', 'mint', 'apricot', 'merlot', 'wheat', 'celery', 'mulberry', 'melon', 'claret', 'banana', 'pea', 'grape', 'cherry', 'grapefruit', 'eggshell', 'lilac', 'salmon', 'cornflower', 'wintergreen', 'kiwi', 'cinnamon', 'sage', 'asparagus', 'berry', 'peach', 'mango', 'ice', 'burgundy', 'mocha', 'blurple', 'burple', 'tangerine', 'spearmint', 'bubblegum', 'eggplant', 'squash', 'butterscotch', 'blueberry', 'custard', 'apple', 'olive', 'seaweed', 'coffee', 'mustard', 'strawberry', 'aubergine', 'plum']

delicious_colors = {name: colors[name] for name in delicious_color_keys}

def color_dist(c1, c2):
    return (c1["r"] - c2["r"]) ** 2 + (c1["g"] - c2["g"]) ** 2 + (c1["b"] - c2["b"]) ** 2

def closest_delicious_color(c): 
    return min(delicious_colors, key=lambda k: color_dist(delicious_colors[k], c))

def closest_color(c): 
    return min(colors, key=lambda k: color_dist(colors[k], c))

def just_color(c):
    return "#" + format(c["r"], '02x') + format(c["g"], '02x') + format(c["b"], '02x')

def nearest_eight(n):
    return min(255, int(round(n / 24.0) * 24.0))

def eighth_hex(c):
    return "#" + format(nearest_eight(c["r"]), '02x') + format(nearest_eight(c["g"]), '02x') + format(nearest_eight(c["b"]), '02x')

rgb_to_color = None

def map_image(fn, im):
    (h,w,_) = im.shape
    def to_rgb(a):
        if len(a) == 3:
            [r,g,b] = a
        else:
            [r,g,b,_] = a
        # int(x) handles 16-bit PNG
        return {"r": int(r), "g": int(g), "b": int(b)}
    def trans(p):
        a = 1
        if len(p) == 3:
            [r,g,b] = p
        else:
            [r,g,b,a] = p
        return a == 0
    return [fn(to_rgb(im[y][x]), y, x) for x in range(w) for y in range(h) if not trans(im[y][x])]

def delicious_pixels(im):
    return map_image(lambda c,y,x: {"c": c, "y": y, "x": x}, im)

def tuple_to_rgb(t):
    (r, g, b) = t
    return {"r": r, "g": g, "b": b}

def rgb_to_tuple(r):
    return (r["r"], r["g"], r["b"])

def mask_color_bit(x, n):
    bits = float(2 ** n)
    return min(255, int(round(x / bits) * bits))

def mask_color_bits(t, n):
    return tuple(map(lambda x: mask_color_bit(x, n), t))

def do_graded_reduce(ps, pixel_color):
    color_pixels = itertools.groupby(ps, pixel_color)

    d = {}
    for tuple_c, vs in color_pixels:
        d[tuple_c] = list(vs)

    color_pixels = d

    ENOUGH = 25
    MAX_MASK = 7

    enough_pixels = {}

    # Well, this is gonna be wrong once I run it...
    not_enough_pixels = {}

    for x in range(MAX_MASK):
        for tuple_c, vs in color_pixels.items():
            pixels = list(vs)

            if len(pixels) > ENOUGH:
                if tuple_c in enough_pixels:
                    enough_pixels[tuple_c] += pixels
                else:
                    enough_pixels[tuple_c] = pixels
            else:
                reduced_c = mask_color_bits(tuple_c, x)

                if reduced_c in enough_pixels:
                    enough_pixels[reduced_c] += pixels
                elif reduced_c in not_enough_pixels:
                    not_enough_pixels[reduced_c] += pixels
                else:
                    not_enough_pixels[reduced_c] = pixels

        color_pixels = not_enough_pixels
        not_enough_pixels = {}

    for tuple_c, vs in color_pixels.items():
        pixels = list(vs)
        if tuple_c in enough_pixels:
            enough_pixels[tuple_c] += pixels
        else:
            enough_pixels[tuple_c] = pixels

    return enough_pixels


# I got x and y swapped... Fix here.
def delicious_commands(im, yoff, xoff, window, graded_reduce, flat_reduce):
    def pixel_color(pix): return rgb_to_tuple(pix["c"])
    def pixel_coords(pix): return str(pix['x'] + xoff) + ',' + str(pix['y'] + yoff)
    
    p = sorted(delicious_pixels(im), key=pixel_color)

    if graded_reduce:
        color_pixels = do_graded_reduce(p, pixel_color)
    elif flat_reduce:
        color_pixels = itertools.groupby(p, lambda c: mask_color_bits(rgb_to_tuple(c["c"]), 4))

        d = {}
        for tuple_c, vs in color_pixels:
            d[tuple_c] = list(vs)

        color_pixels = d
    else:
        color_pixels = itertools.groupby(p, lambda c: rgb_to_tuple(c["c"]))

        d = {}
        for tuple_c, vs in color_pixels:
            d[tuple_c] = list(vs)

        color_pixels = d

    commands = []

    up = PBNHelper.UnicodeProtocol(132, 99) # TODO

    # Transform my color_pixels dict into the PBNHelper dict
    up_dict = {}

    for tuple_c, vs in color_pixels.items():
        up_dict[up.get_color_rgb(tuple_c[0], tuple_c[1], tuple_c[2])] = map(lambda v: up.get_cord(v['x'], v['y']), vs)
    
    list(map(print, up.generate_messages(up_dict)))

    # pixels_list = []

    # for tuple_c, vs in color_pixels.items():
    #     for v in vs:
    #         # v is...
    #         pixels_list.append((up.get_cord(v['x'], v['y']), up.get_color_rgb(tuple_c[0], tuple_c[1], tuple_c[2])))

    # for tuple_c, vs in color_pixels.items():
    #     pixels = list(vs)

    #     # TODO: We still have the original color of all the pixels
    #     # Average the color of all the pixels instead of just using the reduction...

    #     s_c = rgb_to_color(tuple_to_rgb(tuple_c))

    #     i = 0

    #     while i < len(pixels):
    #         print(s_c + ' ' + ';'.join(map(pixel_coords, pixels[i:i+window])))
    #         i += window

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Give dwango chat commands for drawing an image in a delicious fashion.')
    parser.add_argument("imagefile", type=str)
    parser.add_argument("--window", type=int, default=65, help='Pixels per chat line')
    parser.add_argument("--yoff", type=int, default=1, help='y-offset of top left pixel')
    parser.add_argument("--xoff", type=int, default=1, help='x-offset of top left pixel')
    parser.add_argument("--mode", type=str, default='graded-reduce', help='Determines what colors get written - delicious, gross or hex')
    parser.add_argument("--maxy", type=int, default=99)
    parser.add_argument("--maxx", type=int, default=132)

    args = parser.parse_args()

    if args.mode == 'delicious':
        rgb_to_color = closest_delicious_color
    elif args.mode == 'gross':
        rgb_to_color = closest_color
    elif args.mode == 'hex':
        rgb_to_color = just_color
    elif args.mode == 'reduced-hex':
        rgb_to_color = just_color
    elif args.mode == 'graded-reduce':
        rgb_to_color = just_color
    else:
        raise Exception("Color mode must be delicious, gross or hex")

    im = imageio.imread(args.imagefile)

    h = im.shape[0]
    w = im.shape[1]

    if not (1 <= args.yoff <= args.maxy):
        raise Exception("Y offset must be between 1 and 92")

    if not (1 <= args.yoff + h - 1 <= args.maxy):
        raise Exception("Image goes off top. Y offset + image height must be between 1 and 92")

    if not (1 <= args.xoff <= args.maxx):
        raise Exception("X offset must be between 1 and 123")

    if not (1 <= args.xoff + w - 1 <= args.maxx):
        raise Exception("Image goes off right. X offset + image width must be between 1 and 123")

    delicious_commands(im, args.yoff, args.xoff, args.window, args.mode == 'graded-reduce', args.mode == 'reduced-hex')
