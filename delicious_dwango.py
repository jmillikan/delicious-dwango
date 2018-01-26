import argparse
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
        [r,g,b] = a
        return {"r": r, "g": g, "b": b}
    return [fn(to_rgb(im[y][x]), y, x) for x in range(w) for y in range(h)]

def delicious_pixels(im):
    return map_image(lambda c,y,x: {"c": closest_delicious_color(c), "y": y, "x": x}, im)

def delicious_commands(im, yoff, xoff):
    for pix in delicious_pixels(im):
        print(pix['c'] + ' ' + str(pix['y'] + yoff) + ',' + str(pix['x'] + xoff))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Give dwango chat commands for drawing an image in a delicious fashion.')
    parser.add_argument("imagefile", type=str)
    parser.add_argument("--yoff", type=int, default=0)
    parser.add_argument("--xoff", type=int, default=0)
    
    args = parser.parse_args()

    im = imageio.imread(args.imagefile)

    delicious_commands(im, args.yoff, args.xoff)
