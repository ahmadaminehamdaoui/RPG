try:
    import noise
    importedNoise = True
except:
    from classes.tiles.defaultMap import defaultMap
    importedNoise = False

from random import randint
from classes.tiles.tile import Tile
from classes.tiles.prop import Prop

def perlin_gen(dim=(128,128), scale=25, octaves=2, lacunarity=2.0, persistence=1.2, seed=-1):
    if importedNoise:
        while seed<0 and seed>-20:
            seed = randint(-300,300)

        # --- GENERATION SAVING --- #
        row = []
        ts = []

        # --- NOISE GEN --- #
        for y in range(dim[1]):
            for x in range(dim[0]):
                value = noise.pnoise2( x/scale,
                                    y/scale,
                                    octaves=octaves,
                                    persistence=persistence,
                                    lacunarity=lacunarity,
                                    repeatx=dim[0],
                                    repeaty=dim[1],
                                    base=seed)
                # -- DEFINE TILE -- #
                if value < -0.25:
                    result = 'water',''
                elif value < -0.18:
                    result = 'sand',''
                elif value < 0.15:
                    result = 'grass',''
                else:
                    result = 'mountain',''
                row.append([Tile(result[0]), result[1]])
            ts.append(row)
            row = []
        
        # mountains should always have a vertical connection
        for y in range(dim[1]):
            for x in range(dim[0]):
                if ts[y][x][0].tileID == 'mountain':
                    if not((y<dim[1]-1 and ts[y+1][x][0].tileID == 'mountain') or (y>0 and ts[y-1][x][0].tileID == 'mountain')):
                        ts[y-1][x][0].set_tileID('mountain')
        
    else:
        ts = defaultMap
        for y in range(len(ts)):
            for x in range(len(ts[0])):
                ts[y][x][0] = Tile(ts[y][x][0])
    # ------------------------------------------ #
    for y in range(dim[1]):
        for x in range(dim[0]):
            ts[y][x][0].update(ts, x, y)
    return ts

def prop_gen(ts):
    row = []
    tilesheet = []

    for y in range(ts.get_height()):
        for x in range(ts.get_width()):
            if ts.tileLayer[y][x][0].tileID == 'grass':
                if randint(0,30)==0:
                    row.append(Prop(str(randint(1,4))))
                else:
                    row.append(Prop('0'))
            elif ts.tileLayer[y][x][0].tileID == 'sand':
                if randint(0,30)==0:
                    row.append(Prop(str(randint(5,8))))
                else:
                    row.append(Prop('0'))
            else:
                    row.append(Prop('0'))

        tilesheet.append(row)
        row = []
    
    return tilesheet

'''
from PIL import Image

# --- COLORS --- #
blue = (66,110,225)
green = (36,135,32)
beach = (240,210,172)
mountain = (140,140,140)

def define_color(value):
    if value <-0.25:
        return blue
    elif value < -0.18:
        return beach
    elif value < 0.25:
        return green
    return mountain

# --- NOISE SETTINGS --- #

shape = (128,128)   # (256,256)
scale = 25         # 50

octaves = 2
lacunarity = 2.0
persistence = 1.2

seed = -1
while seed<0 and seed>-20:
    seed = randint(-300,300)

# --- SAVE DIRECTORY --- #
image_filepath = "noise1.png"
image = Image.new(mode='RGB', size=shape)

# --- NOISE GEN --- #
for x in range(shape[0]):
    for y in range(shape[1]):
        value = noise.pnoise2( x/scale,
                            y/scale,
                            octaves=octaves,
                            persistence=persistence,
                            lacunarity=lacunarity,
                            repeatx=shape[0],
                            repeaty=shape[1],
                            base=seed)
        color = define_color(value)
        image.putpixel((x,y), color)

print(seed)
image.save(image_filepath)
'''