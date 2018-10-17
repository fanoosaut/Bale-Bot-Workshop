from PIL import Image

background = Image.open("yourPicture.jpg")
width, height = background.size

foreground = Image.open("Template.png")
foreground = foreground.resize((width, height), Image.ANTIALIAS)

background.paste(foreground, (0, 0), foreground)
background.save("result.jpg")
background.show()

