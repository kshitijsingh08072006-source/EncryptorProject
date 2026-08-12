import time

read_time = 0.0
decrypt_time = 0.0
write_time = 0.0

from cryptography.fernet import Fernet
import hashlib
import base64
import sys
import os
import struct

if len(sys.argv) != 3:
    print("Usage: decryptor.py <file> <password>")
    sys.exit()

filename = sys.argv[1]
password = sys.argv[2]

password_hash = hashlib.sha256(password.encode()).digest()
key = base64.urlsafe_b64encode(password_hash)

cipher = Fernet(key)

temp_filename = filename + ".tmp"

try:
    total_size = os.path.getsize(filename)
    processed = 0

    with open(filename, "rb") as infile, \
         open(temp_filename, "wb") as outfile:

        while True:

            # Read encrypted chunk length
            t1 = time.perf_counter()
            length_data = infile.read(4)

            if not length_data:
                break

            chunk_length = struct.unpack("I", length_data)[0]

            # Read encrypted chunk
            encrypted_chunk = infile.read(chunk_length)
            read_time += time.perf_counter() - t1

            # Decrypt
            t1 = time.perf_counter()
            decrypted_chunk = cipher.decrypt(encrypted_chunk)
            decrypt_time += time.perf_counter() - t1

            # Write plaintext
            t1 = time.perf_counter()
            outfile.write(decrypted_chunk)
            write_time += time.perf_counter() - t1

            processed += 4 + chunk_length

            progress = (processed / total_size) * 100
            print(f"\rProgress: {progress:.1f}%", end="")

    print("\nDecryption complete.")

    if filename.endswith(".enc"):
        final_filename = filename[:-4]
    else:
        final_filename = filename + ".decrypted"

    os.remove(filename)

    os.rename(temp_filename, final_filename)

    print("Restored file:", final_filename)

except Exception as e:
    print("\nError:", e)

    if os.path.exists(temp_filename):
        print("Temporary decrypted file kept:")
        print(temp_filename)

print("\n===== DECRYPTION STATS =====")
print(f"Read Time    : {read_time:.6f} s")
print(f"Decrypt Time : {decrypt_time:.6f} s")
print(f"Write Time   : {write_time:.6f} s")
print(f"Total        : {read_time + decrypt_time + write_time:.6f} s")