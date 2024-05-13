import numpy as np
import matplotlib.pyplot as plt

def find_png_header(data):
    png_header = bytes([137, 80, 78, 71, 13, 10, 26, 10])
    start_indices = []
    index = data.find(png_header)
    while index != -1:
        start_indices.append(index)
        index = data.find(png_header, index + 1)
    return start_indices

# Load the raw ASK modulated data
file_path = 'flag.raw'  # Update this with the correct path
signal = np.fromfile(file_path, dtype=np.float32)

# Given the symbol rate and sampling rate, calculate the number of samples per symbol
symbol_samples = int(350000 / 1000)  # Number of samples per symbol

# Extract the symbols correctly, rescale to 0-255, and round to nearest integer
corrected_symbols = signal[::symbol_samples] * 255  # Rescale
corrected_demodulated_bytes = np.round(corrected_symbols).astype(np.uint8)

# Convert the byte data and search for the PNG header
corrected_demodulated_bytes_data = bytes(corrected_demodulated_bytes.tolist())
png_indices_corrected = find_png_header(corrected_demodulated_bytes_data)

# If PNG header is found, save the data as a PNG file
if png_indices_corrected:
    png_file_path = 'extracted_image.png'  # Update this with the desired path
    with open(png_file_path, 'wb') as f:
        f.write(corrected_demodulated_bytes_data)
    print(f"PNG file created at {png_file_path}")
else:
    print("No PNG header found in the data.")
