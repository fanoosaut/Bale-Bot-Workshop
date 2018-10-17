from PIL import Image

foreground = Image.open("Template.png")
background = Image.open("yourPicture.jpg")

background.paste(foreground, (0, 0), foreground)
background.save("result.jpg")
background.show()

