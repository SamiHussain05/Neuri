from PIL import Image
from pytesseract import pytesseract

# Path to the image file
image_path = "Screenshot 2024-12-07 at 18.33.02.png"

# Open the image & store it in an image object
img = Image.open(image_path)

# Extract text from the image
text = pytesseract.image_to_string(img)

# Display the extracted text
print(text[:-1])