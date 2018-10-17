from PIL import Image


def combine(file_name):
    foreground = Image.open(file_name)
    background = Image.open("yourPicture.jpg")
    background.paste(foreground, (0, 0), foreground)
    background.save("result.jpg")
    background.show()
