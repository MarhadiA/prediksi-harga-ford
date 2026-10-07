# import streamlit as st
# import pandas as pd
# import joblib

# #  modul analisis_regresi_ford ada agar FordFeatureBuilder bisa dibaca
# import analisis_regresi_ford

# # 1. Load file pkl
# @st.cache_resource
# def load_bundle():
#     return joblib.load('ford_price_model_terbaik.pkl')

# bundle = load_bundle()
# model = bundle['model']
import streamlit as st
import pandas as pd
import pickle  # Menggunakan pickle standar
import analisis_regresi_ford

# Load file pkl pakai pickle
@st.cache_resource
def load_bundle():
    with open('ford_price_model_terbaik.pkl', 'rb') as f:
        return pickle.load(f)

bundle = load_bundle()
model = bundle['model']
# Tampilan Web Streamlit
st.title(" Prediksi Harga Mobil Ford")
st.write("Masukkan spesifikasi mobil untuk memperkirakan harganya.")

# 2. Urutan Input Sesuai Permintaan
# Daftar pilihan model mobil umum pada dataset Ford
car_model = st.selectbox(
    "Model Mobil", 
    ["Fiesta", "Focus", "Kuga", "EcoSport", "Mustang", "Mondeo", "C-MAX", "Ka+", "S-MAX", "Edge"]
)

year = st.number_input("Tahun Mobil (Year)", min_value=1990, max_value=2026, value=2018)
if year < 1990 or year > 2026:
    st.error("Tahun mobil harus berada di antara 1990 dan 2026.")

budget = st.text_input("Uang yang Tersedia (Opsional)", value="")

transmission = st.selectbox("Transmisi (Transmission)", ["Manual", "Automatic", "Semi-Auto"])

fuelType = st.selectbox("Jenis Bahan Bakar (Fuel Type)", ["Petrol", "Diesel", "Hybrid", "Other"])

mileage = st.number_input("Kilometer (Mileage)", min_value=0, value=25000)
if mileage > 300000:
    st.warning("Peringatan: Kilometer sangat tinggi, hasil prediksi mungkin kurang akurat.")

mpg = st.number_input("MPG (Miles per Gallon)", min_value=0.0, value=50.0)
if mpg > 200.0:
    st.error("Nilai MPG terlalu tinggi, mohon periksa kembali.")

# Logika Filter Engine Size berdasarkan Model (Menyesuaikan pilihan secara dinamis)
engine_size_options = {
    "Fiesta": [1.0, 1.1, 1.25, 1.4, 1.5, 1.6],
    "Focus": [1.0, 1.4, 1.5, 1.6, 2.0, 2.3],
    "Kuga": [1.5, 2.0],
    "EcoSport": [1.0, 1.5],
    "Mustang": [2.3, 5.0],
    "Mondeo": [1.5, 2.0, 2.2],
    "C-MAX": [1.0, 1.5, 1.6, 2.0],
    "Ka+": [1.2],
    "S-MAX": [2.0],
    "Edge": [2.0]
}

available_engines = engine_size_options.get(car_model, [1.0, 1.2, 1.4, 1.5, 1.6, 2.0])
engineSize = st.selectbox("Kapasitas Mesin (Engine Size)", available_engines)

# 3. Tombol Prediksi
# if st.button("Prediksi Harga"):
#     # Buat DataFrame dengan 7 fitur utama (nanti FordFeatureBuilder di dalam .pkl yang akan mengurus kolom tambahan)
#     input_data = pd.DataFrame({
#         'model': [car_model],
#         'year': [year],
#         'transmission': [transmission],
#         'mileage': [mileage],
#         'fuelType': [fuelType],
#         'mpg': [mpg],
#         'engineSize': [engineSize]
#     })
    
#     try:
#         # Lakukan prediksi lewat pipeline model
#         prediction = model.predict(input_data)
        
#         # Tampilkan hasil
#         st.success(f"Estimasi Harga Mobil: ${prediction[0]:,.2f}")
        
#         # Cek budget jika diisi
#         if budget.strip() != "":
#             try:
#                 budget_val = float(budget)
#                 if budget_val >= prediction[0]:
#                     st.info("Status: Dana yang tersedia mencukupi untuk membeli mobil ini! 🎉")
#                 else:
#                     st.warning("Status: Estimasi harga mobil ini melebihi dana yang tersedia. ⚠️")
#             except ValueError:
#                 st.error("Format uang yang tersedia harus berupa angka.")
                
#     except Exception as e:
#         st.error(f"Terjadi kesalahan saat memprediksi: {e}")
# 3. Tombol Prediksi
if st.button("Prediksi Harga"):
    # Buat DataFrame dengan menyertakan kolom utama beserta model_grouped & fuel_grouped
    input_data = pd.DataFrame({
        'model': [car_model],
        'model_grouped': [car_model],  # Kolom tambahan yang dicari oleh model
        'year': [year],
        'transmission': [transmission],
        'mileage': [mileage],
        'fuelType': [fuelType],
        'fuel_grouped': [fuelType],    # Kolom tambahan yang dicari oleh model
        'mpg': [mpg],
        'engineSize': [engineSize]
    })
    
    try:
        # Lakukan prediksi lewat pipeline model
        prediction = model.predict(input_data)
        
        # Tampilkan hasil
        st.success(f"Estimasi Harga Mobil: ${prediction[0]:,.2f}")
        
        # Cek budget jika diisi
        if budget.strip() != "":
            try:
                budget_val = float(budget)
                if budget_val >= prediction[0]:
                    st.info("Status: Dana yang tersedia mencukupi untuk membeli mobil ini! 🎉")
                else:
                    st.warning("Status: Estimasi harga mobil ini melebihi dana yang tersedia. ⚠️")
            except ValueError:
                st.error("Format uang yang tersedia harus berupa angka.")
                
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memprediksi: {e}")