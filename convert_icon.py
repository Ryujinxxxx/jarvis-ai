from PIL import Image

# Open your PNG file
img = Image.open("C:\\Users\\mfahm\\jarvis-ai\\man.png")

# Save it as ICO
img.save("C:\\Users\\mfahm\\jarvis-ai\\jarvis.ico", format='ICO', sizes=[(256,256)])

print("Conversion complete! jarvis.ico created.")
