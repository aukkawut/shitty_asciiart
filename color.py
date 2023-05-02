from PIL import Image
import argparse
parser = argparse.ArgumentParser(description='Ascii art thingy')
parser.add_argument('filename', help='image')
parser.add_argument('--width', type=int, default=100, help='width (optional, default=100)')
parser.add_argument('--height', type=int, help='height (optional)')
parser.add_argument('--color', action='store_true', help='add weird color (optional)')
args = parser.parse_args()
img = Image.open(args.filename)
if args.height != None:
    img = img.resize((args.width, args.height))
else:
    img = img.resize((args.width, int(args.width * img.size[1] / img.size[0])))
ascii_chars = [' ', '.', ':', '-', '=', '+', '*', '%', '@','#', '▒', '▓', '█'] #order by luminosity if you want to change it
color_palette = [ #never use this shit before... 
    (0, 0, 0),        # black
    (128, 0, 0),      # dark red
    (0, 128, 0),      # dark green
    (128, 128, 0),    # dark yellow
    (0, 0, 128),      # dark blue
    (128, 0, 128),    # dark magenta
    (0, 128, 128),    # dark cyan
    (192, 192, 192),  # light gray
    (128, 128, 128),  # dark gray
    (255, 0, 0),      # red
    (0, 255, 0),      # green
    (255, 255, 0),    # yellow
    (0, 0, 255),      # blue
    (255, 0, 255),    # magenta
    (0, 255, 255),    # cyan
    (255, 255, 255),  # white
]

ascii_art = ''
for y in range(img.size[1]):
    for x in range(img.size[0]):
        r, g, b = img.getpixel((x, y))
        gray = int(0.21*r + 0.72*g + 0.07*b) #yeah, linear transform from CV course
        color_index = int((gray / 255) * (len(ascii_chars) - 1)) #luminosity
        if args.color:
            #stackoverflow code, don't mind me
            color = color_palette[color_index]
            closest_color_index = min(range(len(color_palette)), key=lambda i: sum([(color_palette[i][j]-color[j])**2 for j in range(3)]))
            closest_color = color_palette[closest_color_index]
            ascii_art += "\033[48;5;{}m{}\033[0m".format(closest_color_index, ascii_chars[color_index])
        else:
            ascii_art += ascii_chars[color_index]
    ascii_art += '\n'
print(ascii_art)
