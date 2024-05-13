# 404CTF{5feef3c530abba7ae2242487b25b6f6b}

import numpy as np

# Function to read channel data and convert ASCII '48'/'49' to binary 0/1
def read_and_convert_channels(channel_files):
    binary_channels = []
    for file_path in channel_files:
        channel_data = np.fromfile(file_path, dtype='uint8')
        binary_channel = np.where(channel_data == 49, 1, 0)
        binary_channels.append(binary_channel)
    return binary_channels

# Function to decode the channels and perform error correction
def decode_channels(channels):
    decoded_bytes = []
    for byte_bits in zip(*channels):
        byte_bits = list(byte_bits)  # Convert tuple to list to allow modifications
        if sum(byte_bits[:7]) % 2 != byte_bits[7]:  # Check parity
            byte_bits[3] = 1 - byte_bits[3]  # Correct the suspected error bit in channel 4
        decoded_bytes.append(byte_bits[:7])  # Use the original 7 data bits
    return np.packbits(np.array(decoded_bytes))

# Define the paths to the channel files
channel_files = [
    "channel_1",
    "channel_2",
    "channel_3",
    "channel_4",
    "channel_5",
    "channel_6",
    "channel_7",
    "channel_8"
]

# Read and convert channel data from files
channels = read_and_convert_channels(channel_files)

# Decode channels
decoded_data = decode_channels(channels)

# Save the corrected image file
with open("corrected_flag.png", "wb") as img_file:
    img_file.write(decoded_data.tobytes())
