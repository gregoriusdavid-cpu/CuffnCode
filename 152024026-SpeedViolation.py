import multiprocessing
import time
import random
import os

def proses_kamera(queue_data):
    """
    Proses 1: Mensimulasikan pembacaan frame dari kamera jalan raya.
    Proses ini meng-handle data input secara berkelanjutan.
    """
    print(f"[Proses Kamera] Berjalan pada PID: {os.getpid()}")
    
    # Simulasi mendeteksi 5 kendaraan yang lewat
    for i in range(1, 6):
        time.sleep(1.5)  # Simulasi jeda kendaraan lewat
        speed_simulated = random.randint(40, 110) # Simulasi kecepatan acak km/jam
        id_kendaraan = f"D-{random.randint(1000, 9999)}-XYZ"
        
        data_kendaraan = {
            "id": id_kendaraan,
            "kecepatan": speed_simulated,
            "timestamp": time.strftime("%H:%M:%S")
        }
        
        print(f"\n[Kamera] Merekam {id_kendaraan} melaju dengan kecepatan {speed_simulated} km/jam")
        queue_data.put(data_kendaraan)
    
    # Kirim sinyal bahwa kamera selesai merekam
    queue_data.put(None)
    print("[Proses Kamera] Selesai.")

def proses_deteksi_pelanggaran(queue_data, batas_kecepatan=80):
    """
    Proses 2: Memproses data dari Kamera (melalui Queue) secara paralel.
    Menentukan apakah kendaraan melanggar batas kecepatan atau tidak.
    """
    print(f"[Proses Deteksi] Berjalan pada PID: {os.getpid()}")
    
    while True:
        data = queue_data.get()
        if data is None:  # Jika menerima sinyal selesai
            break
            
        # Logika deteksi pelanggaran
        if data["kecepatan"] > batas_kecepatan:
            print(f"⚠️ [TILANG] Kendaraan {data['id']} MELANGGAR! Kecepatan: {data['kecepatan']} km/jam (Batas: {batas_kecepatan} km/jam) pada {data['timestamp']}")
        else:
            print(f"✅ [AMAN] Kendaraan {data['id']} patuh aturan. Kecepatan: {data['kecepatan']} km/jam.")
            
    print("[Proses Deteksi] Selesai.")

if __name__ == "__main__":
    print(f"[Proses Utama] PID: {os.getpid()}")
    
    # Batas kecepatan maksimum di jalan tersebut (km/jam)
    BATAS_MAKSIMAL = 80
    
    # Queue digunakan untuk komunikasi antar proses (Inter-Process Communication)
    shared_queue = multiprocessing.Queue()
    
    # Forking/Membuat proses baru menggunakan Multiprocessing
    p1 = multiprocessing.Process(target=proses_kamera, args=(shared_queue,))
    p2 = multiprocessing.Process(target=proses_deteksi_pelanggaran, args=(shared_queue, BATAS_MAKSIMAL))
    
    # Memulai kedua proses secara paralel
    p1.start()
    p2.start()
    
    # Menunggu kedua proses selesai sebelum menutup program utama
    p1.join()
    p2.join()
    
    print("\n[Proses Utama] Semua proses paralel selesai berjalan.")