import time

read_time = 0.0
encrypt_time = 0.0
write_time = 0.0

from cryptography.fernet import Fernet
import hashlib
import base64
import sys
import os
import struct

CHUNK_SIZE = 1024 * 1024  # 1 MB

if len(sys.argv) != 3:
    print("Usage: encryptor.py <file> <password>")
    sys.exit()

filename = sys.argv[1]
password = sys.argv[2]

password_hash = hashlib.sha256(password.encode()).digest()
key = base64.urlsafe_b64encode(password_hash)

cipher = Fernet(key)

temp_filename = filename + ".tmp"
final_filename = filename + ".enc"

try:
    total_size = os.path.getsize(filename)
    processed = 0

    with open(filename, "rb") as infile, \
         open(temp_filename, "wb") as outfile:

        while True:
            t1 = time.perf_counter()
            chunk = infile.read(CHUNK_SIZE)
            read_time += time.perf_counter() - t1

            if not chunk:
                break

            t1 = time.perf_counter()
            encrypted_chunk = cipher.encrypt(chunk)
            encrypt_time += time.perf_counter() - t1

            t1 = time.perf_counter()

            # Write length of encrypted chunk
            outfile.write(struct.pack("I", len(encrypted_chunk)))

            # Write encrypted chunk
            outfile.write(encrypted_chunk)

            processed += len(chunk)

            write_time += time.perf_counter() - t1

            progress = (processed / total_size) * 100
            print(f"\rProgress: {progress:.1f}%", end="")

    print("\nEncryption complete.")

    os.remove(filename)

    os.rename(temp_filename, final_filename)

    print("Encrypted file:", final_filename)

except Exception as e:
    print("\nError:", e)

    if os.path.exists(temp_filename):
        print("Temporary encrypted file kept:")
        print(temp_filename)

print("\n===== ENCRYPTION STATS =====")
print(f"Read Time    : {read_time:.6f} s")
print(f"Encrypt Time : {encrypt_time:.6f} s")
print(f"Write Time   : {write_time:.6f} s")
print(f"Total        : {read_time + encrypt_time + write_time:.6f} s")