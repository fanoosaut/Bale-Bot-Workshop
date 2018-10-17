from PIL import Image


def combine(file_name):
    background = Image.open(file_name)
    width, height = background.size

    foreground = Image.open("Template.png")
    foreground = foreground.resize((width, height), Image.ANTIALIAS)

    background.paste(foreground, (0, 0), foreground)
    background.save("result.jpg")
    background.show()

