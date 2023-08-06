# Converts back and forth between different color formats [(255,0,0),#ff0000, 16711680,(255,0,255) ... ]

### pip install fabisschomagut

#### Tested against Windows 10 / Python 3.10 / Anaconda




### How to use it

```python

# Converting from one color format to another

from fabisschomagut import subtract_color,add_color,to_rgb_hex,to_rgba_hex,to_rgba_tuple,to_rgb_tuple

print(to_rgb_tuple(color="red"))
print(to_rgba_tuple(color=(255, 0, 0)))
print(to_rgb_hex(color="#ff0000"))
print(to_rgba_hex(color="0xFF0000"))


print(to_rgb_tuple(color=0xFF0000, invert=True))
print(to_rgba_tuple(color="red", invert=True))
print(to_rgb_hex(color="red", invert=True))
print(to_rgba_hex(color=(255, 0, 0), invert=True))


print(to_rgb_tuple(color="blue", invert=True))
print(to_rgba_tuple(color=(0, 255, 0), invert=True))
print(to_rgb_hex(color="ff0000", invert=False))
print(to_rgba_hex(color="#FFF000", invert=False))
print(to_rgb_tuple(color="BLUE", invert=False))
print(add_color(color1="BLUE", color2=(0, 255, 0), invert=False))

print(subtract_color(color1="pink", color2="#200000", invert=False))
print(to_rgb_hex(color=16746513, invert=False))

print(subtract_color(color1="pink", color2="0x200000", invert=False))
print(subtract_color(color1="ffc0cb", color2=0x200000, invert=False))
print(subtract_color(color1=0xFFC0CB, color2="#200000", invert=True))
print(to_rgb_hex(subtract_color(color1="pink", color2="200000", invert=True)))


# (255, 0, 0)
# (255, 0, 0, 255)
# 0xff0000
# (255, 0, 0, 255)
# 0xff0000ff
# #FF0000
# (0, 0, 255)
# (0, 0, 255, 255)
# 0x0000ff
# (0, 0, 255, 255)
# 0x0000ffff
# (255, 0, 0)
# (0, 255, 0, 255)
# 0xff0000
# (255, 240, 0, 255)
# 0xfff000ff
# (0, 0, 255)
# (0, 255, 255)
# (223, 192, 203)
# #FF8811
# 0xff8811
# (223, 192, 203)
# #200000
# (223, 192, 203)
# #FFC0CB
# (203, 192, 223)
# 0xcbc0df

```