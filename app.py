import streamlit as st
import pandas as pd

st.set_page_config(page_title="Okul Yatırım Simülatörü", layout="wide")

st.title("🏫 Özel Okul Yatırım ve Finansal Simülasyon Motoru")
st.sidebar.header("⚙️ Simülasyon Ayarları")

# 1. KADEMELER VE AKTİVASYON
st.sidebar.subheader("Kademeleri Seçin")
anaokulu = st.sidebar.checkbox("Anaokulu", value=True)
ilkokul = st.sidebar.checkbox("İlkokul", value=True)
ortaokul = st.sidebar.checkbox("Ortaokul", value=True)
lise = st.sidebar.checkbox("Lise (Aktif/Pasif)", value=False)

# 2. GİRDİLER (Sliderlar)
st.sidebar.subheader("Finansal Parametreler")
ogrenci_ucreti = st.sidebar.slider("Yıllık Eğitim Ücreti (TL)", 150000, 600000, 350000)
ogretmen_maas = st.sidebar.slider("Ortalama Öğretmen Maaşı (Net/TL)", 30000, 80000, 45000)
doluluk_orani = st.sidebar.slider("Okul Doluluk Oranı (%)", 10, 100, 60)

# 3. HESAPLAMA MANTIĞI (Senin Excel verilerine göre)
sube_sayisi = 3
mevcut = 20
toplam_kapasite = 0
aktif_kademeler = []

if anaokulu: 
    toplam_kapasite += 1 * sube_sayisi * mevcut
    aktif_kademeler.append("Anaokulu")
if ilkokul: 
    toplam_kapasite += 4 * sube_sayisi * mevcut
    aktif_kademeler.append("İlkokul")
if ortaokul: 
    toplam_kapasite += 4 * sube_sayisi * mevcut
    aktif_kademeler.append("Ortaokul")
if lise: 
    toplam_kapasite += 4 * sube_sayisi * mevcut
    aktif_kademeler.append("Lise")

mevcut_ogrenci = int(toplam_kapasite * (doluluk_orani / 100))

# Personel Sayıları (Senin CSV'den esinlenerek)
mudur_sayisi = 1
mudur_yrd_sayisi = 3 if (ortaokul or lise) else 1
yardimci_personel = 10 # Temizlik, Güvenlik, Aşçı

# ÖĞRETMEN NORM HESABI
toplam_saat = (len(aktif_kademeler) * 4 * sube_sayisi * 45) # Basitleştirilmiş
ogretmen_sayisi = round(toplam_saat / 22)

# FİNANSAL TABLO
yillik_gelir = mevcut_ogrenci * ogrenci_ucreti
personel_gideri = (ogretmen_sayisi * ogretmen_maas * 1.6 * 12) + (yardimci_personel * 35000 * 1.4 * 12)
kar = yillik_gelir - personel_gideri

# EKRAN ÇIKTILARI
col1, col2, col3 = st.columns(3)
col1.metric("Toplam Öğrenci", mevcut_ogrenci)
col2.metric("Gereken Öğretmen", ogretmen_sayisi)
col3.metric("Tahmini Yıllık Kâr", f"{kar:,.0f} TL")

st.divider()
st.subheader("📊 Branş Bazlı Dağılım ve Risk Analizi")
st.info(f"Seçili Kademeler: {', '.join(aktif_kademeler)}")

if kar < 0:
    st.error("⚠️ DİKKAT: Mevcut doluluk oranıyla okul zarar ediyor! Ücretleri veya doluluğu artırın.")
else:
    st.success("✅ Okul şu an operasyonel olarak kârda görünüyor.")