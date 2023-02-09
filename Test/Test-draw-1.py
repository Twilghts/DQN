from PIL import Image

# Open the first image
img1 = Image.open("image1.jpg")

# Open the second image
img2 = Image.open("image2.jpg")

# Open the third image
img3 = Image.open("image3.jpg")

# Create a new image with the size of the two images combined
widths, heights = zip(*(i.size for i in [img1, img2, img3]))
total_width = sum(widths)
max_height = max(heights)
new_img = Image.new("RGB", (total_width, max_height))

# Paste the first image into the new image
new_img.paste(img1, (0, 0))

# Paste the second image into the new image
new_img.paste(img2, (img1.width, 0))

# Paste the third image into the new image
new_img.paste(img3, (img1.width + img2.width, 0))

# Save the final combined image
new_img.save("combined_image.jpg")
