import streamlit as st
from datetime import date, datetime, timedelta

# Library kalender Umm al-Qura (pengganti hijri_convert yang hasilnya bergeser 1 hari)
# Pasang dengan: pip install hijridate
from hijridate import Hijri, Gregorian

try:
    from zoneinfo import ZoneInfo
    ZONA_WAKTU = ZoneInfo("Asia/Jakarta")
except Exception:
    ZONA_WAKTU = None

st.set_page_config(
    page_title="Jadwal Ibadah Hijriah",
    page_icon="🕌",
    layout="centered",
)

# ==========================================
# 1. DATA NAMA BULAN & HARI
# ==========================================

bulanHijriah = [
    "Muharram", "Safar", "Rabiul Awal", "Rabiul Akhir",
    "Jumadil Awal", "Jumadil Akhir", "Rajab", "Sya'ban",
    "Ramadhan", "Syawal", "Dzulqa'dah", "Dzulhijjah"
]

NAMA_BULAN_MASEHI = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

NAMA_HARI_LENGKAP = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
NAMA_HARI_SINGKAT = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]

# ==========================================
# 2. DATA EVENT IBADAH
# ==========================================

event = {
    "1 Muharram": [
        "Tahun Baru Hijriah",
        "Menandai dimulainya tahun baru dalam kalender Hijriah. "
        "Dapat menjadi momentum untuk introspeksi dan memperbaiki diri."
    ],
    "9 Muharram": [
        "Puasa Tasu'a",
        "Puasa sunnah pada tanggal 9 Muharram."
    ],
    "10 Muharram": [
        "Puasa Asyura",
        "Puasa sunnah pada tanggal 10 Muharram."
    ],
    "1 Ramadhan": [
        "Awal Ramadan",
        "Awal bulan Ramadan, bulan diwajibkannya puasa bagi umat Islam "
        "yang memenuhi syarat."
    ],
    "17 Ramadhan": [
        "Nuzulul Quran",
        "Tanggal yang umum diperingati di Indonesia sebagai Nuzulul Quran."
    ],
    "8 Dzulhijjah": [
        "Puasa Tarwiyah",
        "Puasa yang dikenal dalam praktik sebagian umat Islam menjelang Arafah."
    ],
    "9 Dzulhijjah": [
        "Puasa Arafah",
        "Puasa sunnah yang sangat dianjurkan bagi orang yang tidak berhaji."
    ],
    "10 Dzulhijjah": [
        "Iduladha",
        "Hari Raya Iduladha yang berkaitan dengan ibadah haji dan kurban."
    ],
    "1 Syawal": [
        "Idulfitri",
        "Hari raya yang menandai berakhirnya bulan Ramadan."
    ],
    "12 Rabiul Awal": [
        "Maulid Nabi",
        "Tanggal yang umum digunakan di Indonesia untuk memperingati "
        "kelahiran Nabi Muhammad ﷺ."
    ],
    "27 Rajab": [
        "Isra Mikraj",
        "Tanggal yang umum digunakan dalam tradisi Indonesia untuk "
        "memperingati peristiwa Isra Mikraj."
    ],
    "26 Rabiul Akhir": [
        "Contoh Kegiatan",
        "Deskripsi contoh kegiatan. Silakan ganti dengan kegiatan yang benar."
    ]
}

# ==========================================
# 3. FUNGSI KONVERSI TANGGAL
# ==========================================

def tanggal_hari_ini_masehi():
    """Tanggal hari ini menurut WIB (bukan jam server)."""
    if ZONA_WAKTU is not None:
        return datetime.now(ZONA_WAKTU).date()
    return date.today()


def hijriah_hari_ini():
    """Mengembalikan (tahun_h, bulan_h, hari_h, tanggal_masehi)."""
    masehi = tanggal_hari_ini_masehi()
    h = Gregorian(masehi.year, masehi.month, masehi.day).to_hijri()
    return h.year, h.month, h.day, masehi


def awal_bulan(tahun_h, bulan_h):
    """Tanggal Masehi untuk tanggal 1 pada bulan Hijriah tersebut."""
    g = Hijri(tahun_h, bulan_h, 1).to_gregorian()
    return date(g.year, g.month, g.day)


def panjang_bulan(tahun_h, bulan_h):
    """Jumlah hari (29 atau 30) pada bulan Hijriah tersebut."""
    return Hijri(tahun_h, bulan_h, 1).month_length()


def format_masehi(tgl):
    hari = NAMA_HARI_LENGKAP[tgl.weekday()]
    return f"{hari}, {tgl.day} {NAMA_BULAN_MASEHI[tgl.month - 1]} {tgl.year}"


# ==========================================
# 4. MENCARI EVENT
# ==========================================

def cek_event(hari, nomor_bulan):
    kunci = f"{hari} {bulanHijriah[nomor_bulan - 1]}"
    return event.get(kunci)


# ==========================================
# 5. DIALOG DETAIL KEGIATAN
# ==========================================

@st.dialog("Detail Kegiatan")
def detail_kegiatan(nama, deskripsi):
    st.header(nama)
    st.write(deskripsi)


# ==========================================
# 6. TEMA HIJAU ISLAMI (CSS)
# ==========================================

POLA_BINTANG = (
    "url(\"data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 64 64'%3E"
    "%3Cg fill='none' stroke='%23f4c430' stroke-opacity='0.16' stroke-width='1'%3E"
    "%3Crect x='16' y='16' width='32' height='32'/%3E"
    "%3Crect x='16' y='16' width='32' height='32' transform='rotate(45 32 32)'/%3E"
    "%3C/g%3E%3C/svg%3E\")"
)

CSS_TEMA = """
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Poppins:wght@400;500;600&display=swap');

:root {
    --hijau-tua: #06251b;
    --hijau: #0b3d2e;
    --hijau-muda: #14633f;
    --emas: #f4c430;
    --krem: #fff8dc;
}

.stApp {
    background:
        POLA_BINTANG,
        linear-gradient(180deg, #06251b 0%, #0b3d2e 55%, #0e4a35 100%);
    background-attachment: fixed;
    font-family: 'Poppins', sans-serif;
}

[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; max-width: 720px; }

/* Teks umum */
.stApp .stMarkdown p, .stApp .stMarkdown li { color: var(--krem); }
.stApp h2, .stApp h3 {
    color: var(--emas) !important;
    font-family: 'Amiri', serif;
}
[data-testid="stWidgetLabel"] p { color: var(--krem) !important; }

/* Banner utama */
.hero {
    position: relative;
    overflow: hidden;
    text-align: center;
    padding: 30px 16px 26px 16px;
    margin-bottom: 18px;
    border-radius: 22px;
    border: 1px solid rgba(244, 196, 48, 0.5);
    background:
        radial-gradient(circle at 50% 0%, rgba(244, 196, 48, 0.22), transparent 60%),
        linear-gradient(160deg, #14633f 0%, #0b3d2e 100%);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
}
.hero-bulan { font-size: 2.2rem; line-height: 1; color: var(--emas);
              text-shadow: 0 0 14px rgba(244, 196, 48, 0.7); }
.hero-judul { font-family: 'Amiri', serif; font-size: 1.9rem; font-weight: 700;
              color: var(--emas); margin: 6px 0 2px 0; }
.hero-hijri { font-size: 1.35rem; font-weight: 600; color: var(--krem); }
.hero-masehi { font-size: 0.85rem; color: rgba(255, 248, 220, 0.7); margin-top: 2px; }

.bintang { position: absolute; color: var(--emas);
           text-shadow: 0 0 8px rgba(244, 196, 48, 0.8);
           animation: kelip 3s ease-in-out infinite; }
.b1 { top: 10%; left: 8%;  font-size: 20px; }
.b2 { top: 16%; right: 10%; font-size: 28px; animation-delay: .6s; }
.b3 { bottom: 14%; left: 16%; font-size: 14px; animation-delay: 1.2s; }
.b4 { bottom: 18%; right: 18%; font-size: 18px; animation-delay: 1.8s; }
.b5 { top: 46%; left: 3%; font-size: 12px; animation-delay: .3s; }
.b6 { top: 50%; right: 4%; font-size: 14px; animation-delay: 2.1s; }
@keyframes kelip {
    0%, 100% { opacity: .35; transform: scale(.85); }
    50% { opacity: 1; transform: scale(1.15); }
}

/* Kartu */
.kartu {
    background: rgba(255, 248, 220, 0.07);
    border: 1px solid rgba(244, 196, 48, 0.3);
    border-radius: 14px;
    padding: 14px 16px;
    color: var(--krem);
}
.st-key-event_box, .st-key-pilihan_box {
    background: rgba(244, 196, 48, 0.12);
    border: 1px solid rgba(244, 196, 48, 0.45);
    border-left: 5px solid var(--emas);
    border-radius: 14px;
    padding: 14px 16px;
}
.pemisah { text-align: center; color: var(--emas); letter-spacing: 8px;
           margin: 18px 0 6px 0; opacity: .8; }
.keterangan-bulan { text-align: center; color: rgba(255, 248, 220, 0.75);
                    font-size: .85rem; margin-bottom: 10px; }

/* Tombol umum */
.stButton button {
    background: var(--emas);
    color: var(--hijau-tua);
    border: none;
    border-radius: 10px;
    font-weight: 600;
}
.stButton button:hover { background: #ffd95a; color: var(--hijau-tua); }
.stButton button p { color: inherit; }

/* ===== Kalender: tetap 7 kolom di HP ===== */
.st-key-calendar_grid {
    background: rgba(255, 248, 220, 0.06);
    border: 1px solid rgba(244, 196, 48, 0.25);
    border-radius: 16px;
    padding: 12px 8px;
}
.st-key-calendar_grid [data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 0.3rem !important;
}
.st-key-calendar_grid [data-testid="stColumn"],
.st-key-calendar_grid [data-testid="column"] {
    min-width: 0 !important;
    width: auto !important;
    flex: 1 1 0 !important;
}
.st-key-calendar_grid [data-testid="stVerticalBlock"] { gap: 0.3rem; }

.st-key-calendar_grid button {
    position: relative;
    width: 100%;
    min-height: 42px;
    padding: 0;
    border-radius: 10px;
    background: var(--hijau-muda);
    border: 1px solid rgba(244, 196, 48, 0.3);
    color: var(--krem);
}
.st-key-calendar_grid button p { margin: 0; font-size: 0.9rem; color: inherit; }
.st-key-calendar_grid button:hover { background: #1b7a4f; border-color: var(--emas); color: var(--krem); }

.nama-hari { text-align: center; font-weight: 600; font-size: 0.8rem; color: var(--emas); }
.nama-hari.jumat { color: #ffe98a; }

@media (max-width: 480px) {
    .block-container { padding-left: 0.8rem; padding-right: 0.8rem; }
    .hero-judul { font-size: 1.6rem; }
    .hero-hijri { font-size: 1.15rem; }
    .st-key-calendar_grid { padding: 8px 4px; }
    .st-key-calendar_grid [data-testid="stHorizontalBlock"] { gap: 0.2rem !important; }
    .st-key-calendar_grid button { min-height: 36px; border-radius: 8px; }
    .st-key-calendar_grid button p { font-size: 0.78rem; }
    .nama-hari { font-size: 0.7rem; }
}
""".replace("POLA_BINTANG", POLA_BINTANG)

st.markdown(f"<style>{CSS_TEMA}</style>", unsafe_allow_html=True)


def css_hari_khusus(tahun, nomor_bulan, jumlah_hari, hari_ini_h, terpilih):
    """CSS tambahan: bintang di hari ber-event, emas di hari ini, cincin di tanggal terpilih."""
    aturan = []
    for hari in range(1, jumlah_hari + 1):
        sel = f".st-key-tgl_{tahun}_{nomor_bulan}_{hari} button"

        if cek_event(hari, nomor_bulan):
            aturan.append(
                f"{sel} {{ border-color: #f4c430 !important; }} "
                f"{sel}::after {{ content: '★'; position: absolute; top: 1px; right: 4px; "
                f"font-size: .6rem; color: #f4c430; }}"
            )

        if hari_ini_h == hari:
            aturan.append(
                f"{sel} {{ background: #f4c430 !important; border-color: #f4c430 !important; }} "
                f"{sel} p {{ color: #06251b !important; font-weight: 700; }} "
                f"{sel}::after {{ color: #06251b !important; }}"
            )

        if terpilih == hari:
            aturan.append(f"{sel} {{ box-shadow: 0 0 0 2px #fff8dc; }}")

    return "<style>" + "\n".join(aturan) + "</style>"


# ==========================================
# 7. HALAMAN UTAMA
# ==========================================

tahun_ini, bulan_ini, hari_ini, masehi_ini = hijriah_hari_ini()

st.markdown(
    "\n".join([
        '<div class="hero">',
        '<span class="bintang b1">★</span>',
        '<span class="bintang b2">✦</span>',
        '<span class="bintang b3">★</span>',
        '<span class="bintang b4">✦</span>',
        '<span class="bintang b5">★</span>',
        '<span class="bintang b6">✦</span>',
        '<div class="hero-bulan">☪</div>',
        '<div class="hero-judul">Jadwal Ibadah Hijriah</div>',
        f'<div class="hero-hijri">{hari_ini} {bulanHijriah[bulan_ini - 1]} {tahun_ini} H</div>',
        f'<div class="hero-masehi">{format_masehi(masehi_ini)}</div>',
        '</div>',
    ]),
    unsafe_allow_html=True,
)

data_event = cek_event(hari_ini, bulan_ini)

if data_event:
    with st.container(key="event_box"):
        st.markdown("🎉 **Ada kegiatan khusus hari ini!**")
        st.markdown(f"✦ **{data_event[0]}**")

        if st.button("Baca selengkapnya", key="detail_event"):
            detail_kegiatan(data_event[0], data_event[1])
else:
    st.markdown(
        '<div class="kartu">🔔 Tidak ada kegiatan khusus hari ini.</div>',
        unsafe_allow_html=True,
    )

st.markdown('<div class="pemisah">✦ ✦ ✦</div>', unsafe_allow_html=True)

# ==========================================
# 8. PILIH BULAN DAN TAHUN KALENDER
# ==========================================

st.subheader("📅 Kalender Hijriah")

kolom1, kolom2 = st.columns(2)

with kolom1:
    bulan = st.selectbox(
        "Pilih bulan",
        bulanHijriah,
        index=bulan_ini - 1,
    )

with kolom2:
    tahun = st.number_input(
        "Tahun Hijriah",
        min_value=1440,
        max_value=1500,
        value=min(max(tahun_ini, 1440), 1500),
        step=1,
    )

tahun = int(tahun)
nomor_bulan = bulanHijriah.index(bulan) + 1

st.markdown(f"### Kalender {bulan} {tahun} H")

# ==========================================
# 9. MEMBUAT TAMPILAN KALENDER
# ==========================================

tanggal_awal = awal_bulan(tahun, nomor_bulan)
jumlah_hari = panjang_bulan(tahun, nomor_bulan)
posisi_awal = tanggal_awal.weekday()  # Senin = 0

st.markdown(
    f'<div class="keterangan-bulan">1 {bulan} {tahun} H = {format_masehi(tanggal_awal)}</div>',
    unsafe_allow_html=True,
)

pilihan = st.session_state.get("tanggal_dipilih")
hari_terpilih = pilihan[2] if pilihan and pilihan[0] == tahun and pilihan[1] == nomor_bulan else None
hari_ini_di_bulan_ini = hari_ini if (tahun == tahun_ini and nomor_bulan == bulan_ini) else None

st.markdown(
    css_hari_khusus(tahun, nomor_bulan, jumlah_hari, hari_ini_di_bulan_ini, hari_terpilih),
    unsafe_allow_html=True,
)

with st.container(key="calendar_grid"):
    # Nama hari
    kolom_hari = st.columns(7)
    for i, nama in enumerate(NAMA_HARI_SINGKAT):
        with kolom_hari[i]:
            kelas = "nama-hari jumat" if nama == "Jum" else "nama-hari"
            st.markdown(f'<div class="{kelas}">{nama}</div>', unsafe_allow_html=True)

    # Susunan tanggal
    daftar_tanggal = [None] * posisi_awal + list(range(1, jumlah_hari + 1))

    for awal in range(0, len(daftar_tanggal), 7):
        kolom = st.columns(7)

        for i, hari in enumerate(daftar_tanggal[awal:awal + 7]):
            with kolom[i]:
                if hari is not None:
                    if st.button(
                        str(hari),
                        key=f"tgl_{tahun}_{nomor_bulan}_{hari}",
                        use_container_width=True,
                    ):
                        st.session_state["tanggal_dipilih"] = (tahun, nomor_bulan, hari)
                        hari_terpilih = hari

st.markdown(
    '<div class="keterangan-bulan">★ = ada kegiatan &nbsp;|&nbsp; kotak emas = hari ini</div>',
    unsafe_allow_html=True,
)

# ==========================================
# 10. MENAMPILKAN TANGGAL YANG DIPILIH
# ==========================================

pilihan = st.session_state.get("tanggal_dipilih")

if pilihan and pilihan[0] == tahun and pilihan[1] == nomor_bulan:
    hari_pilihan = pilihan[2]
    tgl_masehi = tanggal_awal + timedelta(days=hari_pilihan - 1)

    st.markdown('<div class="pemisah">✦ ✦ ✦</div>', unsafe_allow_html=True)
    st.subheader(f"📅 {hari_pilihan} {bulan} {tahun} H")
    st.caption(format_masehi(tgl_masehi))

    data_event_pilihan = cek_event(hari_pilihan, nomor_bulan)

    if data_event_pilihan:
        with st.container(key="pilihan_box"):
            st.markdown(f"🎉 **{data_event_pilihan[0]}**")

            if st.button("Lihat detail kegiatan", key="detail_kalender"):
                detail_kegiatan(data_event_pilihan[0], data_event_pilihan[1])
    else:
        st.markdown(
            '<div class="kartu">Belum ada kegiatan yang terdaftar pada tanggal ini.</div>',
            unsafe_allow_html=True,
        )