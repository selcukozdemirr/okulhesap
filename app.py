import streamlit as st
import pandas as pd

st.set_page_config(page_title="Özel Okul Finansal Simülatör", layout="wide")

st.title("📊 Özel Okul Yatırım Hesaplama Motoru")
st.markdown("Excel'deki tüm değerleri aşağıdaki tablolardan anlık olarak değiştirebilirsiniz.")

# --- SIDEBAR: GENEL AYARLAR ---
st.sidebar.header("Global Çarpanlar")
ssk_carpani = st.sidebar.number_input("SSK ve Vergi Çarpanı (Brüt/Net Oranı)", value=1.6, step=0.1) #
stopaj_orani = st.sidebar.number_input("Stopaj Oranı (Birim)", value=0.06, step=0.01) #

# --- 1. KADEME VE ÖĞRENCİ HESAPLARI ---
st.subheader("1. Sınıf Seviyeleri ve Öğrenci Kapasitesi")
# Excel'deki SINIF SEVİYESİ, ŞUBE ve ORTALAMA FİYAT mantığı
kapasite_data = {
    "Sınıf Seviyesi": ["Anaokulu", "1. Sınıf", "2. Sınıf", "3. Sınıf", "4. Sınıf", "5. Sınıf", "6. Sınıf", "7. Sınıf", "8. Sınıf", "9. Sınıf (Lise)", "10. Sınıf (Lise)", "11. Sınıf (Lise)", "12. Sınıf (Lise)"],
    "Şube Sayısı": [3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0], # Lise başlangıçta 0
    "Öğrenci Sayısı": [60, 60, 60, 60, 60, 60, 60, 60, 60, 0, 0, 0, 0],
    "Ortalama Fiyat (Yıllık)": [300000] * 13
}
df_kapasite = pd.DataFrame(kapasite_data)
edited_kapasite = st.data_editor(df_kapasite, num_rows="dynamic")

# --- 2. PERSONEL VE MAAŞ DAĞILIMI ---
st.subheader("2. İdari, Öğretmen ve Yardımcı Personel Dağılımı")
# Excel'deki Branş ve Personel Dağılımı
personel_data = {
    "Görev/Branş": ["Müdür", "Müdür Yrd.", "Sınıf Öğretmeni", "Matematik", "Türkçe", "Fen Bilgisi", "İngilizce", "Rehberlik", "Memur/Muhasebe", "Temizlik/Güvenlik", "Aşçı"],
    "Personel Sayısı": [1, 2, 12, 4, 4, 4, 6, 2, 3, 6, 2],
    "Ortalama Net Maaş": [70000, 60000, 45000, 45000, 45000, 45000, 48000, 50000, 35000, 25000, 30000]
}
df_personel = pd.DataFrame(personel_data)
edited_personel = st.data_editor(df_personel, num_rows="dynamic")

# --- HESAPLAMALAR ---
# Gelir Hesaplama
toplam_gelir = (edited_kapasite["Öğrenci Sayısı"] * edited_kapasite["Ortalama Fiyat (Yıllık)"]).sum()

# Gider Hesaplama (Maaşlar + SSK + Stopaj)
edited_personel["Aylık Toplam Maliyet"] = edited_personel["Personel Sayısı"] * edited_personel["Ortalama Net Maaş"] * ssk_carpani
yillik_personel_gideri = edited_personel["Aylık Toplam Maliyet"].sum() * 12

# --- ÇIKTILAR (METRİKLER) ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Toplam Yıllık Gelir", f"{toplam_gelir:,.0f} TL")
c2.metric("Yıllık Personel Gideri", f"{yillik_personel_gideri:,.0f} TL")
c3.metric("Net Faaliyet Kârı (Bina Hariç)", f"{toplam_gelir - yillik_personel_gideri:,.0f} TL")

# Detaylı Gider Analizi Grafiği
st.bar_chart(edited_personel.set_index("Görev/Branş")["Aylık Toplam Maliyet"])