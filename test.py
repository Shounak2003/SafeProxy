import base64

# Test encoding and decoding
encoded_data = base64.b64encode(b"Hello, World!").decode()
decoded_data = base64.b64decode(encoded_data).decode()

print(f"Encoded data: {encoded_data}")
print(f"Decoded data: {decoded_data}")
