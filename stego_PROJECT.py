import cv2
import os

# Function to check if the image exists
def load_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not open image '{image_path}'. Check the path and file format.")
        exit()
    return img

# Function to encode the message in the image
def encode_message(img, msg):
    height, width, _ = img.shape
    n, m, z = 0, 0, 0

    for char in msg:
        img[n, m, z] = ord(char)  # Convert character to ASCII value
        z += 1
        if z == 3:  # Move to the next pixel
            z = 0
            m += 1
            if m == width:
                m = 0
                n += 1
                if n == height:
                    print("Error: Image is too small for the message.")
                    exit()

    return img

# Function to decode the message from the image
def decode_message(img, msg_length, password, input_password):
    if password != input_password:
        print("Unauthorized access! Incorrect passcode.")
        return

    height, width, _ = img.shape
    n, m, z = 0, 0, 0
    decoded_msg = ""

    for _ in range(msg_length):
        decoded_msg += chr(img[n, m, z])  # Convert ASCII value back to character
        z += 1
        if z == 3:
            z = 0
            m += 1
            if m == width:
                m = 0
                n += 1

    print("\nDecrypted Message:", decoded_msg)

# Main execution
image_path = "riding.jpg"  # Update this with your image path
img = load_image(image_path)

msg = input("Enter secret message: ")
password = input("Enter a passcode: ")

# Encoding the message
encoded_img = encode_message(img, msg)

# Save and show the encoded image
output_image_path = "stego_image.bmp"
cv2.imwrite(output_image_path, encoded_img)
print(f"\nMessage hidden successfully! Encoded image saved as '{output_image_path}'.")
cv2.imshow("Encoded Image", encoded_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Decoding the message
input_password = input("\nEnter passcode for decryption: ")
decode_message(encoded_img, len(msg), password, input_password)
