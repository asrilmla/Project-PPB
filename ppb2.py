import random

BASES = ["A", "T", "G", "C"]

def read_fasta(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    dna_sekuens = ""
    for line in lines:
        if not line.startswith(">"):  
            dna_sekuens += line.strip().upper()
    return dna_sekuens 

def simulasi_mutasi(dna, rate):
    dna_baru = []
    for base in dna:
        if random.random() < rate:
            base = random.choice([b for b in BASES if b != base])
        dna_baru.append(base)
    return ''.join(dna_baru)

def menghitung_gsi(orig, mut):
    pasangan_basa = zip(orig, mut)     # pasangkan tiap basa DNA
    jumlah_mutasi = sum(a != b for a, b in pasangan_basa) # hitung jumlah mutasi
    total = len(orig)
    gsi = (1 - jumlah_mutasi / total) * 100
    return gsi, jumlah_mutasi, total

def menghitung_gc_content(dna):
    gc_count = dna.count('G') + dna.count('C')
    gc_content = (gc_count / len(dna)) * 100
    return gc_content

print("=== Genetic Stability Index (GSI) & GC Content Analyzer ===")
filename = input("Masukkan nama file FASTA: ")

try:
    dna = read_fasta(filename)
except FileNotFoundError:           #Menghentikan program jika file tidak ada
    raise SystemExit("File tidak ditemukan! Pastikan nama dan lokasi file benar.")

if not dna:         #Menghentikan program jika file tidak berisi DNA 
    raise ValueError("Tidak ada sekuens DNA yang ditemukan dalam file FASTA.")

print(f"\nSekuens DNA berhasil dibaca ({len(dna)} basa).")

rataan_mutasi = random.uniform(0.01, 0.10)

mutasi_dna = simulasi_mutasi(dna, rataan_mutasi)
gsi, total_mut, total_len = menghitung_gsi(dna, mutasi_dna)
gc_sebelum = menghitung_gc_content(dna)
gc_sesudah = menghitung_gc_content(mutasi_dna) #Mengambil hasil sebelum dan sesudah mutasi untuk dibandingkan

print("\n=== HASIL ANALISIS ===")
print(f"Total basa    : {total_len}")
print(f"Jumlah mutasi : {total_mut}")
print(f"Tingkat mutasi acak : {rataan_mutasi*100:.2f}%")    #Jumlah mutasi
print(f"Genetic Stability Index (GSI): {gsi:.2f}%")         #Persentase GSi
print(f"GC Content sebelum mutasi: {gc_sebelum:.2f}%")      #Perubahan GC Content

print("\n=== INTERPRETASI ===")
if gsi > 90:
    print("Gen sangat stabil terhadap mutasi.")
elif gsi > 75:
    print("Gen cukup stabil terhadap mutasi.")
elif gsi > 50:
    print("Gen mulai menunjukkan ketidakstabilan.")
else:
    print("Gen sangat rentan terhadap mutasi.")

if gc_sesudah > gc_sebelum:
    print("📈 Kandungan GC meningkat = potensi kestabilan struktur DNA meningkat.")
elif gc_sesudah < gc_sebelum:
    print("📉 Kandungan GC menurun = potensi kestabilan struktur DNA berkurang.")
else:
    print("🔸 Kandungan GC tetap = tidak ada perubahan signifikan pada kestabilan.")
