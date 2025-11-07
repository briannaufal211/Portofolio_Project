# =============================================
# PORTOFOLIO PROJECT - Brian Naufal
# =============================================
# WEB SCRAPING OLX MOBIL BEKAS AREA TANGERANG)
# =============================================

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import sqlite3

# =============================================
# SETUP SELENIUM
# =============================================
browser = webdriver.Chrome()

# =============================================
# INISIALISASI PENYIMPAN DATA
# =============================================
vehicle_data = {
    'judul': [],
    'bahan_bakar': [],
    'harga': [],
    'mesin': [],
    'lokasi': [],
    'transmisi': [],
    'odometer': [],
    'keterangan': []
}

# =============================================
# INPUT PENCARIAN
# =============================================
search_term = input("Masukkan keyword mobil yang ingin dicari (contoh: toyota, honda, dll): ")

# URL AREA TANGERANG
formatted_url = f"https://www.olx.co.id/tangerang-kota_g4000079/mobil-bekas_c198/q-{search_term}"
browser.get(formatted_url)

time.sleep(3)  # Tunggu halaman awal siap

# =============================================
# LOAD SEMUA IKLAN DENGAN SCROLL + MUAT LEBIH
# =============================================
target_items = 100  # jumlah maksimal iklan (sesuai kebutuhan)
prev_count = 0

while True:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

    ads = browser.find_elements(By.CSS_SELECTOR, "li[data-aut-id='itemBox']")
    print(f"Iklan terdeteksi: {len(ads)}")

    # jika sudah cukup iklan
    if len(ads) >= target_items:
        print(f"Target {target_items} iklan tercapai")
        break

    # jika tidak bertambah, coba klik tombol “muat lebih banyak”
    if len(ads) == prev_count:
        try:
            load_more_btn = WebDriverWait(browser, 5).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, "button[data-aut-id='btnLoadMore']"))
            )
            browser.execute_script("arguments[0].scrollIntoView(true);", load_more_btn)
            time.sleep(1)
            browser.execute_script("arguments[0].click();", load_more_btn)
            print("Klik tombol 'Muat lebih banyak' untuk ambil iklan tambahan")
            time.sleep(3)
        except:
            print("Tidak ada tombol 'Muat lebih banyak' — berhenti scroll.")
            break

    prev_count = len(ads)

# =============================================
# AMBIL LINK IKLAN
# =============================================
ad_elements = browser.find_elements(By.CSS_SELECTOR, "li[data-aut-id='itemBox'] a")
product_links = [el.get_attribute("href") for el in ad_elements if el.get_attribute("href")]
product_links = product_links[:target_items]
print(f"Dapat {len(product_links)} link produk.\n")

# =============================================
# SCRAPING DETAIL PRODUK SATU PER SATU
# =============================================
for counter, product_url in enumerate(product_links):
    try:
        browser.get(product_url)

        # Scroll sedikit biar elemen detail termuat
        browser.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)

        # Tunggu sampai elemen utama muncul
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )

        page = BeautifulSoup(browser.page_source, "html.parser")

        # Ekstraksi elemen
        title = page.find("h1").get_text() if page.find("h1") else None
        fuel = page.find("h2", {"data-aut-id": "itemAttribute_fuel"})
        gearbox = page.find("h2", {"data-aut-id": "itemAttribute_transmission"})
        mileage = page.find("div", {"data-aut-id": "itemAttribute_mileage"})
        price = page.find("div", {"data-aut-id": "itemPrice"})

        # Ambil lokasi & kapasitas mesin
        area, engine_capacity = None, None
        info_boxes = page.find_all("div", class_="_3dS7E")
        for box in info_boxes:
            label = box.find("div", class_="_CCSn")
            value = box.find("div", class_="_3VRXh")
            if label and value:
                if "Lokasi" in label.get_text():
                    area = value.get_text()
                elif "Kapasitas mesin" in label.get_text():
                    engine_capacity = value.get_text()

        # Deskripsi
        desc_block = page.find("div", {"data-aut-id": "descriptionDetails"})
        desc = " ".join(desc_block.stripped_strings) if desc_block else None

        # Simpan ke dictionary
        vehicle_data['judul'].append(title)
        vehicle_data['bahan_bakar'].append(fuel.get_text() if fuel else None)
        vehicle_data['harga'].append(price.get_text() if price else None)
        vehicle_data['mesin'].append(engine_capacity)
        vehicle_data['lokasi'].append(area)
        vehicle_data['transmisi'].append(gearbox.get_text() if gearbox else None)
        vehicle_data['odometer'].append(mileage.get_text() if mileage else None)
        vehicle_data['keterangan'].append(desc)

        print(f"Data ke-{counter+1} berhasil diambil.")

    except Exception as e:
        print(f"Error di data ke-{counter+1}: {e}")
        for key in vehicle_data:
            vehicle_data[key].append(None)

browser.quit()
# =============================================
# KONVERSI KE DATAFRAME
# =============================================
df = pd.DataFrame(vehicle_data)

# =============================
# FILTER DATA HASIL SCRAPING
# =============================
df = df[df["lokasi"].str.contains("Tangerang", case=False, na=False)]  # hanya lokasi Tangerang

print("\n5 Data Pertama:")
print(df.head())

# =============================================
# SIMPAN KE CSV
# =============================================
df.to_csv("data_olx_tangerang.csv", index=False, encoding="utf-8-sig")
print("\nData tersimpan di 'data_olx_tangerang.csv'")

# =============================================
# SIMPAN KE DATABASE SQLITE
# =============================================
try:
    conn = sqlite3.connect("data_olx_tangerang.db")
    df.to_sql("mobil_olx_tangerang", conn, if_exists="replace", index=False)
    conn.close()
    print("Data juga tersimpan di SQLite: 'data_olx_tangerang.db' (tabel: mobil_olx_tangerang)")
except Exception as e:
    print(f"Gagal menyimpan ke database: {e}")


# %%
df


