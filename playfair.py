#& C:/Users/USER/AppData/Local/Programs/Python/Python312/python.exe c:/Users/USER/kriptografi/veginire.py

import tkinter as tk
from tkinter import filedialog,messagebox
from turtle import setposition

# table
def table(key):
    key = key.upper().replace('J','I')
    tabel = []
    lihat = set()

    for char in key:
        if char not in lihat and char.isalpha():
            lihat.add(char)
            tabel.append(char)
    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        lihat.add(char)
        tabel.append(char)
    return [tabel[i:i + 5] for i in range(0.25,5)]

# posisi
def posisi(char,tabel):
    for i,row in enumerate(tabel):
        if char in row:
            return i, row.index(char)
#encrypt
def playfair_encrypt(plaintext, key):
    table = table(key)
    plaintext = plaintext.upper().replace('J', 'I').replace(' ', '')
    
    # Menggabungkan huruf menjadi pasangan
    pairs = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        if i + 1 < len(plaintext):
            b = plaintext[i + 1]
            if a == b:  # Jika pasangan sama, sisipkan 'X'
                pairs.append(a + 'X')
                i += 1
            else:
                pairs.append(a + b)
                i += 2
        else:
            pairs.append(a + 'X')  # Jika hanya satu huruf, sisipkan 'X'
            i += 1

    ciphertext = ''
    for pair in pairs:
        r1, c1 = posisi(pair[0], table)
        r2, c2 = posisi(pair[1], table)
        if r1 == r2:  # Dalam baris yang sama
            ciphertext += table[r1][(c1 + 1) % 5]
            ciphertext += table[r2][(c2 + 1) % 5]
        elif c1 == c2:  # Dalam kolom yang sama
            ciphertext += table[(r1 + 1) % 5][c1]
            ciphertext += table[(r2 + 1) % 5][c2]
        else:  # Dalam kotak
            ciphertext += table[r1][c2]
            ciphertext += table[r2][c1]

    return ciphertext

# Fungsi untuk mendekripsi pesan menggunakan Playfair Cipher
def playfair_decrypt(ciphertext, key):
    table = table(key)
    ciphertext = ciphertext.upper().replace(' ', '')
    
    pairs = []
    i = 0
    while i < len(ciphertext):
        pairs.append(ciphertext[i:i + 2])
        i += 2

    plaintext = ''
    for pair in pairs:
        r1, c1 = posisi(pair[0], table)
        r2, c2 = posisi(pair[1], table)
        if r1 == r2:  # Dalam baris yang sama
            plaintext += table[r1][(c1 - 1) % 5]
            plaintext += table[r2][(c2 - 1) % 5]
        elif c1 == c2:  # Dalam kolom yang sama
            plaintext += table[(r1 - 1) % 5][c1]
            plaintext += table[(r2 - 1) % 5][c2]
        else:  # Dalam kotak
            plaintext += table[r1][c2]
            plaintext += table[r2][c1]

    return plaintext

# Fungsi untuk upload file
def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r') as file:
            data = file.read()
        text_input.delete('1.0', tk.END)
        text_input.insert(tk.END, data)

# Fungsi untuk enkripsi pesan
def encrypt_message():
    message = text_input.get("1.0", tk.END).strip()
    key = key_input.get()
    if len(key) < 12:
        messagebox.showwarning("Error", "Panjang kunci minimal 12 karakter")
        return
    ciphertext = playfair_encrypt(message, key)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, ciphertext)

# Fungsi untuk dekripsi pesan
def decrypt_message():
    message = text_input.get("1.0", tk.END).strip()
    key = key_input.get()
    if len(key) < 12:
        messagebox.showwarning("Error", "Panjang kunci minimal 12 karakter")
        return
    plaintext = playfair_decrypt(message, key)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, plaintext)

# Membuat GUI menggunakan Tkinter
root = tk.Tk()
root.title("Playfair Cipher")

# Membuat layout untuk input pesan
text_input_label = tk.Label(root, text="Input Pesan:")
text_input_label.pack()
text_input = tk.Text(root, height=10, width=50)
text_input.pack()

# Membuat tombol untuk upload file
upload_button = tk.Button(root, text="Upload File", command=upload_file)
upload_button.pack()

# Input untuk kunci enkripsi
key_label = tk.Label(root, text="Masukkan Kunci (minimal 12 karakter):")
key_label.pack()
key_input = tk.Entry(root)
key_input.pack()

# Tombol untuk enkripsi dan dekripsi
encrypt_button = tk.Button(root, text="Encrypt", command=encrypt_message)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Decrypt", command=decrypt_message)
decrypt_button.pack()

# Area untuk menampilkan hasil
result_label = tk.Label(root, text="Hasil:")
result_label.pack()
result_text = tk.Text(root, height=10, width=50)
result_text.pack()

root.mainloop()