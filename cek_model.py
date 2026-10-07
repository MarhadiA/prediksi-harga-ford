import joblib

# Load file pkl
bundle = joblib.load('ford_price_model_terbaik.pkl')
model = bundle['model']

print("--- CEK ISI PIPELINE MODEL ---")
# Cek apakah di dalam pipeline ada tahapan preprocessing (seperti encoder)
if hasattr(model, 'named_steps'):
    for name, step in model.named_steps.items():
        print(f"Tahapan Pipeline: {name} -> Tipe: {type(step)}")
        # Jika ada encoder, coba lihat kategori aslinya
        if hasattr(step, 'categories_'):
            print(f"   -> Menemukan kategori tersimpan di {name}:")
            for i, cat in enumerate(step.categories_):
                print(f"      Kolom {i}: {cat}")
else:
    print("Model bukan berupa Pipeline standar.")