import streamlit as st
import pandas as pd

st.set_page_config(page_title="Blueprint Personality Test", layout="wide")

# ======================
# LOAD DATA CSV
# ======================
@st.cache_data
def load_personality_data():
    df = pd.read_csv("hasil_big5_final.csv")
    return df

data_kepribadian = load_personality_data()

# ======================
# FUNGSI MENENTUKAN TIPE
# ======================
def tentukan_tipe(skor):
    tipe = max(skor, key=skor.get)
    mapping = {
        "O": "Openness",
        "C": "Conscientiousness",
        "E": "Extraversion",
        "A": "Agreeableness",
        "N": "Neuroticism"
    }
    return mapping[tipe]

# ======================
# INTERFACE UTAMA
# ======================
st.title("Blueprint Personality Test")
st.write("Isi 10 pertanyaan berikut untuk mengetahui tipe kepribadian Anda.")

nama = st.text_input("Nama")
umur = st.number_input("Umur", min_value=10, max_value=100, step=1)

st.markdown("---")

# ======================
# LIST PERTANYAAN
# ======================
pertanyaan = [
    ("Saat melihat orang sukses, saya…", {
        "O": "Terinspirasi dan ingin tahu proses mereka.",
        "C": "Termotivasi untuk bekerja lebih keras.",
        "E": "Mengucapkan selamat dan menjadikannya energi positif.",
        "A": "Ikut senang tanpa iri.",
        "N": "Merasa minder dan membandingkan diri sendiri."
    }),
    ("Ketika suasana hati saya tidak stabil, saya…", {
        "O": "Menulis jurnal atau refleksi diri.",
        "C": "Mencari rutinitas untuk mengembalikan fokus.",
        "E": "Berbicara pada orang lain.",
        "A": "Berdiam dan menenangkan diri.",
        "N": "Sulit mengontrol emosi."
    }),
    ("Saat saya menatap masa depan, saya merasa…", {
        "O": "Penasaran akan hal baru.",
        "C": "Termotivasi membangun hidup terencana.",
        "E": "Bersemangat bersama orang terdekat.",
        "A": "Tenang karena yakin semuanya baik.",
        "N": "Cemas karena banyak yang tak bisa dikontrol."
    }),
    ("Saat orang lain lambat merespons pesan saya, saya…", {
        "O": "Berpikir mereka sedang sibuk.",
        "C": "Mencatat agar tidak terulang.",
        "E": "Mengirim pesan kedua yang ringan.",
        "A": "Memakluminya.",
        "N": "Merasa tidak dianggap penting."
    }),
    ("Saat rencana besar gagal, saya…", {
        "O": "Melihatnya sebagai arah baru.",
        "C": "Mengevaluasi kesalahan.",
        "E": "Tetap tersenyum dan mencari cara lain.",
        "A": "Menenangkan diri dan mendengarkan masukan.",
        "N": "Sulit menerima kegagalan."
    }),
    ("Saat membuat keputusan penting, saya lebih sering…", {
        "O": "Mengikuti intuisi.",
        "C": "Mempertimbangkan data.",
        "E": "Berdiskusi dengan orang lain.",
        "A": "Memikirkan dampak bagi orang lain.",
        "N": "Ragu karena takut salah."
    }),
    ("Saat berada di lingkungan baru, saya…", {
        "O": "Tertantang mengenal hal baru.",
        "C": "Menyesuaikan dengan aturan.",
        "E": "Mudah berbaur.",
        "A": "Membuat orang lain nyaman.",
        "N": "Canggung dan menunggu diajak."
    }),
    ("Saat menghadapi perbedaan pendapat dalam hubungan, saya…", {
        "O": "Melihatnya sebagai peluang belajar.",
        "C": "Mencari jalan tengah logis.",
        "E": "Menjaga percakapan tetap hangat.",
        "A": "Mengalah agar tidak konflik.",
        "N": "Jadi sangat sensitif."
    }),
    ("Saya ingin rumah tangga kami dikenal sebagai…", {
        "O": "Terbuka dan berkembang.",
        "C": "Tertib dan terencana.",
        "E": "Hangat dan penuh semangat.",
        "A": "Damai dan memahami.",
        "N": "Tenang tanpa tekanan."
    }),
    ("Dalam berkomunikasi dengan pasangan, saya lebih suka…", {
        "O": "Membahas topik beragam.",
        "C": "Menyampaikan hal penting secara terstruktur.",
        "E": "Berbicara ekspresif.",
        "A": "Mendengarkan dulu.",
        "N": "Menarik diri saat suasana hati buruk."
    }),
]

jawaban = []

# ======================
# TAMPILKAN PERTANYAAN
# ======================
for i, (q, opsi) in enumerate(pertanyaan):
    st.write(f"### {i+1}. {q}")
    pilih = st.radio("", list(opsi.values()), key=f"q{i}", index=None)  # <-- FIX
    # simpan kode O / C / E / A / N
    for k, v in opsi.items():
        if v == pilih:
            jawaban.append(k)

st.markdown("---")

# ======================
# PROSES HASIL
# ======================

if st.button("Lihat Hasil"):
    if not nama or not umur:
        st.error("Isi nama dan umur dulu.")
    elif len(jawaban) < 10:
        st.error("Semua pertanyaan wajib dijawab.")
    else:
        # hitung skor
        skor = {"O": 0, "C": 0, "E": 0, "A": 0, "N": 0}
        for j in jawaban:
            skor[j] += 1

        tipe_final = tentukan_tipe(skor)

        # Ambil deskripsi & saran dari CSV berdasarkan tipe Big-5
        row = data_kepribadian[data_kepribadian["Tipe_Big5"] == tipe_final].iloc[0]

        deskripsi = row["Deskripsi"]
        saran = row["Saran_Pasangan"]

        # ============================
        # TAMPILKAN OUTPUT AKHIR
        # ============================
        st.success("Hasil berhasil diproses!")

        st.subheader("📌 Hasil Kepribadian Anda")
        st.write(f"**Nama:** {nama}")
        st.write(f"**Umur:** {umur}")
        st.write(f"**Tipe Kepribadian:** {tipe_final}")

        st.markdown("### 🧠 Deskripsi Kepribadian")
        st.write(deskripsi)

        st.markdown("### 💡 Saran untuk Hubungan / Pasangan")
        st.write(saran)
