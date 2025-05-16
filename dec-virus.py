import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_file(filepath, key):
    try:
        with open(filepath, "rb") as f:
            encrypted_data = f.read()
        
        # Ekstrak IV (16 byte pertama)
        iv = encrypted_data[:16]
        ct = encrypted_data[16:]
        
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        
        # Simpan file terdekripsi (hapus ekstensi .enc)
        original_path = filepath[:-4] if filepath.endswith('.enc') else filepath
        with open(original_path, "wb") as f:
            f.write(pt)
        
        os.remove(filepath)
        return True
    except Exception as e:
        print(f"Gagal mendekripsi {filepath}: {str(e)}")
        return False

def main():
    # Lokasi folder yang terenkripsi
    encrypted_folder = "/sdcard/virus/"
    
    # File kunci (harus sama dengan yang digunakan untuk enkripsi)
    key_file = "key.key"
    
    # Baca kunci dekripsi
    try:
        with open(key_file, "rb") as f:
            key = f.read()
    except FileNotFoundError:
        print("File kunci tidak ditemukan! Pastikan file key.key ada di direktori yang sama.")
        return
    
    # Proses dekripsi semua file .enc
    decrypted_count = 0
    failed_count = 0
    
    for root, dirs, files in os.walk(encrypted_folder):
        for file in files:
            if file.lower().endswith('.enc'):
                full_path = os.path.join(root, file)
                if decrypt_file(full_path, key):
                    print(f"[+] Berhasil didekripsi: {full_path}")
                    decrypted_count += 1
                else:
                    failed_count += 1
    
    print("\n[!] HASIL DEKRIPSI:")
    print(f"File berhasil didekripsi: {decrypted_count}")
    print(f"File gagal didekripsi: {failed_count}")
    
    # Hapus file tebusan jika ada
    ransom_note = os.path.join(encrypted_folder, "WARNING.txt")
    if os.path.exists(ransom_note):
        os.remove(ransom_note)
        print(f"[!] File tebusan dihapus: {ransom_note}")

if __name__ == "__main__":
    main()
