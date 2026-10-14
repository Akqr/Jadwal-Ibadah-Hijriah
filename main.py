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




def cek_event(hari, nomor_bulan):
    kunci = f"{hari} {bulanHijriah[nomor_bulan - 1]}"
    return event.get(kunci)


def event_terdekat(masehi_ini, batas_hari=400):
    """Cari event ibadah berikutnya SETELAH hari ini (hari ini tidak dihitung)."""
    for selisih in range(1, batas_hari + 1):
        tgl = masehi_ini + timedelta(days=selisih)

        try:
            h = Gregorian(tgl.year, tgl.month, tgl.day).to_hijri()
        except Exception:
            return None

        data = cek_event(h.day, h.month)
        if data:
            return {
                "nama": data[0],
                "selisih": selisih,
                "hari": h.day,
                "bulan": h.month,
                "tahun": h.year,
                "masehi": tgl,
            }

    return None


@st.dialog("Detail Kegiatan")
def detail_kegiatan(nama, deskripsi):
    st.header(nama)
    st.write(deskripsi)


def pilih_tanggal(tahun_h, bulan_h, hari_h):
    """Dipanggil lewat on_click: berjalan SEBELUM halaman digambar ulang,
    jadi tanggal terpilih langsung benar di klik yang sama."""
    st.session_state["tanggal_dipilih"] = (tahun_h, bulan_h, hari_h)


# ==========================================
#  TAMPILAN (CSS) - sederhana: warna solid, tanpa animasi
# ==========================================
# Warna:
#   latar  #0b3d2e   kartu  #11513a   garis  #1d6b4d
#   teks   #f2efe4   emas   #e0b13a (dipakai seperlunya)

CSS_TEMA = """
.stApp { background: #0b3d2e; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stAppDeployButton"] { display: none !important; }
[data-testid="stToolbar"] a { pointer-events: none; }
.block-container { padding-top: 2rem; padding-bottom: 3rem; max-width: 720px; }

/* Teks */
.stApp .stMarkdown p, .stApp .stMarkdown li { color: #f2efe4; }
.stApp h1, .stApp h2, .stApp h3 { color: #f2efe4 !important; font-weight: 600; }
[data-testid="stWidgetLabel"] p { color: #f2efe4 !important; }
[data-testid="stCaptionContainer"] { color: #b9c9bf !important; }
hr { border-color: #1d6b4d !important; }

/* Kepala halaman */
.kepala {
    background: #11513a;
    border: 1px solid #1d6b4d;
    border-left: 4px solid #e0b13a;
    border-radius: 6px;
    padding: 18px 20px;
    margin-bottom: 16px;
}
.kepala .judul { font-size: 0.95rem; color: #b9c9bf; margin-bottom: 4px; }
.kepala .judul .aksen { color: #e0b13a; }
.kepala .tanggal { font-size: 1.7rem; font-weight: 600; color: #f2efe4; line-height: 1.2; }
.kepala .masehi { font-size: 0.9rem; color: #b9c9bf; margin-top: 4px; }

/* Kartu info */
.kartu {
    background: #11513a;
    border: 1px solid #1d6b4d;
    border-radius: 6px;
    padding: 12px 16px;
    color: #f2efe4;
    margin-bottom: 10px;
}
.kartu small { color: #b9c9bf; }
.kartu .sisa { color: #e0b13a; font-weight: 600; }

.st-key-event_box, .st-key-pilihan_box {
    background: #11513a;
    border: 1px solid #1d6b4d;
    border-left: 4px solid #e0b13a;
    border-radius: 6px;
    padding: 12px 16px;
    margin-bottom: 10px;
}

.keterangan { text-align: center; color: #b9c9bf; font-size: .85rem; margin: 4px 0 10px 0; }

/* Catatan kaki (keterangan tugas) */
/* Menempel di dasar layar, rata tengah */
.footer-tugas {
    text-align: center;
    color: #b9c9bf;
    font-size: .8rem;
    line-height: 1.6;
    margin-top: 32px;
}
.footer-tugas b { color: #f2efe4; font-size: .9rem; }

/* Tombol umum */
.stButton button {
    background: #e0b13a;
    color: #0b3d2e;
    border: none;
    border-radius: 6px;
    font-weight: 600;
}
.stButton button:hover { background: #ebc355; color: #0b3d2e; }
.stButton button p { color: inherit; }

/* ===== Kalender: tetap 7 kolom di HP ===== */
.st-key-calendar_grid {
    background: #11513a;
    border: 1px solid #1d6b4d;
    border-radius: 8px;
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
    border-radius: 6px;
    background: #0b3d2e;
    border: 1px solid #1d6b4d;
    color: #f2efe4;
    font-weight: 400;
}
.st-key-calendar_grid button p { margin: 0; font-size: 0.9rem; color: inherit; }
.st-key-calendar_grid button:hover { background: #145a40; border-color: #e0b13a; color: #f2efe4; }

.nama-hari { text-align: center; font-weight: 600; font-size: 0.8rem; color: #b9c9bf; }

@media (max-width: 480px) {
    .block-container { padding-left: 0.8rem; padding-right: 0.8rem; }
    .kepala .tanggal { font-size: 1.4rem; }
    .st-key-calendar_grid { padding: 8px 4px; }
    .st-key-calendar_grid [data-testid="stHorizontalBlock"] { gap: 0.2rem !important; }
    .st-key-calendar_grid button { min-height: 36px; border-radius: 5px; }
    .st-key-calendar_grid button p { font-size: 0.78rem; }
    .nama-hari { font-size: 0.7rem; }
}
"""

st.markdown(f"<style>{CSS_TEMA}</style>", unsafe_allow_html=True)

# ==========================================
# SPLASH SCREEN (tampil sekali saat pertama masuk)
# ==========================================
# Layar pembuka berisi bulan sabit, bintang berkelip, dan judul.
# Menghilang sendiri setelah sekitar 3 detik (diatur oleh animasi CSS
# "splash-hilang"). Untuk mempercepat/memperlambat, ubah angka 3.2s.

SPLASH_HTML = """
<style>
.splash {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    z-index: 99999999;
    background: #0b3d2e;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    animation: splash-hilang 3.2s ease forwards;
}
@keyframes splash-hilang {
    0%, 78% { opacity: 1; visibility: visible; }
    100% { opacity: 0; visibility: hidden; }
}

/* Bulan sabit: lingkaran transparan dengan bayangan bergeser */
.splash .bulan {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    margin-right: 16px;
    box-shadow: 16px 6px 0 0 #e0b13a;
    animation: splash-muncul 1s ease both;
}
.splash .judul {
    margin-top: 28px;
    font-size: 1.6rem;
    font-weight: 600;
    color: #f2efe4;
    text-align: center;
    animation: splash-naik 1s ease 0.4s both;
}
.splash .sub {
    margin-top: 6px;
    font-size: 0.95rem;
    color: #b9c9bf;
    text-align: center;
    padding: 0 16px;
    animation: splash-naik 1s ease 0.8s both;
}

/* Bintang kuning berkelip */
.splash .bintang {
    position: absolute;
    color: #e0b13a;
    animation: splash-kelip 2s ease-in-out infinite;
}

@keyframes splash-muncul {
    from { opacity: 0; transform: scale(0.6); }
    to { opacity: 1; transform: scale(1); }
}
@keyframes splash-naik {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes splash-kelip {
    0%, 100% { opacity: 0.25; transform: scale(0.8); }
    50% { opacity: 1; transform: scale(1.2); }
}

/* Kalau HP diatur "kurangi animasi", splash dilewati */
@media (prefers-reduced-motion: reduce) {
    .splash { display: none; }
}
</style>

<div class="splash">
    <span class="bintang" style="top:12%; left:15%; font-size:18px; animation-delay:0s;">★</span>
    <span class="bintang" style="top:20%; left:80%; font-size:26px; animation-delay:0.5s;">★</span>
    <span class="bintang" style="top:40%; left:5%;  font-size:12px; animation-delay:0.3s;">★</span>
    <span class="bintang" style="top:35%; left:92%; font-size:14px; animation-delay:1.2s;">★</span>
    <span class="bintang" style="top:70%; left:10%; font-size:14px; animation-delay:1s;">★</span>
    <span class="bintang" style="top:78%; left:85%; font-size:20px; animation-delay:1.5s;">★</span>
    <span class="bintang" style="top:88%; left:45%; font-size:16px; animation-delay:0.8s;">★</span>
    <span class="bintang" style="top:8%;  left:55%; font-size:12px; animation-delay:1.7s;">★</span>
    <div class="bulan"></div>
    <div class="judul">Jadwal Ibadah Hijriah</div>
    <div class="sub">Diajukan untuk memenuhi project individu PAI</div>
</div>
"""

# Tampilkan hanya di kunjungan pertama (tidak muncul lagi saat klik tanggal)
if "splash_selesai" not in st.session_state:
    st.session_state["splash_selesai"] = True
    st.markdown(SPLASH_HTML, unsafe_allow_html=True)


def css_hari_khusus(tahun, nomor_bulan, jumlah_hari, hari_ini_h, terpilih):
    """CSS tambahan: bintang kecil di hari ber-event, emas di hari ini, garis di tanggal terpilih."""
    aturan = []
    for hari in range(1, jumlah_hari + 1):
        sel = f".st-key-tgl_{tahun}_{nomor_bulan}_{hari} button"

        if cek_event(hari, nomor_bulan):
            aturan.append(
                f"{sel}::after {{ content: '★'; position: absolute; top: 1px; right: 4px; "
                f"font-size: .6rem; color: #e0b13a; }}"
            )

        if hari_ini_h == hari:
            aturan.append(
                f"{sel} {{ background: #e0b13a !important; border-color: #e0b13a !important; }} "
                f"{sel} p {{ color: #0b3d2e !important; font-weight: 700; }} "
                f"{sel}::after {{ color: #0b3d2e !important; }}"
            )

        if terpilih == hari:
            aturan.append(f"{sel} {{ box-shadow: 0 0 0 2px #f2efe4; }}")

    return "<style>" + "\n".join(aturan) + "</style>"


# ==========================================
#  HALAMAN UTAMA
# ==========================================

tahun_ini, bulan_ini, hari_ini, masehi_ini = hijriah_hari_ini()

st.markdown(
    "\n".join([
        '<div class="kepala">',
        '<div class="judul"><span class="aksen">★</span> Jadwal Ibadah Hijriah</div>',
        f'<div class="tanggal">{hari_ini} {bulanHijriah[bulan_ini - 1]} {tahun_ini} H</div>',
        f'<div class="masehi">{format_masehi(masehi_ini)}</div>',
        '</div>',
    ]),
    unsafe_allow_html=True,
)

data_event = cek_event(hari_ini, bulan_ini)

if data_event:
    with st.container(key="event_box"):
        st.markdown("**Ada kegiatan khusus hari ini**")
        st.markdown(data_event[0])

        if st.button("Baca selengkapnya", key="detail_event"):
            detail_kegiatan(data_event[0], data_event[1])
else:
    st.markdown(
        '<div class="kartu">Tidak ada kegiatan khusus hari ini.</div>',
        unsafe_allow_html=True,
    )

terdekat = event_terdekat(masehi_ini)

if terdekat:
    sisa = "besok" if terdekat["selisih"] == 1 else f"{terdekat['selisih']} hari lagi"
    tanggal_hijri_terdekat = (
        f"{terdekat['hari']} {bulanHijriah[terdekat['bulan'] - 1]} {terdekat['tahun']} H"
    )

    st.markdown(
        f'<div class="kartu"><b>Event terdekat:</b> {terdekat["nama"]} '
        f'<span class="sisa">({sisa})</span><br>'
        f'<small>{tanggal_hijri_terdekat} · {format_masehi(terdekat["masehi"])}</small></div>',
        unsafe_allow_html=True,
    )

st.divider()

# ==========================================
# . PILIH BULAN DAN TAHUN KALENDER
# ==========================================

st.subheader("Kalender Hijriah")

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

st.markdown(f"### {bulan} {tahun} H")

# ==========================================
#  MEMBUAT TAMPILAN KALENDER
# ==========================================

tanggal_awal = awal_bulan(tahun, nomor_bulan)
jumlah_hari = panjang_bulan(tahun, nomor_bulan)
posisi_awal = tanggal_awal.weekday()  # Senin = 0

st.markdown(
    f'<div class="keterangan">1 {bulan} {tahun} H = {format_masehi(tanggal_awal)}</div>',
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
            st.markdown(f'<div class="nama-hari">{nama}</div>', unsafe_allow_html=True)

    # Susunan tanggal
    daftar_tanggal = [None] * posisi_awal + list(range(1, jumlah_hari + 1))

    for awal in range(0, len(daftar_tanggal), 7):
        kolom = st.columns(7)

        for i, hari in enumerate(daftar_tanggal[awal:awal + 7]):
            with kolom[i]:
                if hari is not None:
                    st.button(
                        str(hari),
                        key=f"tgl_{tahun}_{nomor_bulan}_{hari}",
                        use_container_width=True,
                        on_click=pilih_tanggal,
                        args=(tahun, nomor_bulan, hari),
                    )

st.markdown(
    '<div class="keterangan">★ = ada kegiatan &nbsp;|&nbsp; kotak kuning = hari ini</div>',
    unsafe_allow_html=True,
)

# ==========================================
#  MENAMPILKAN TANGGAL YANG DIPILIH
# ==========================================

pilihan = st.session_state.get("tanggal_dipilih")

if pilihan and pilihan[0] == tahun and pilihan[1] == nomor_bulan:
    hari_pilihan = pilihan[2]
    tgl_masehi = tanggal_awal + timedelta(days=hari_pilihan - 1)

    st.divider()
    st.subheader(f"{hari_pilihan} {bulan} {tahun} H")
    st.caption(format_masehi(tgl_masehi))

    data_event_pilihan = cek_event(hari_pilihan, nomor_bulan)

    if data_event_pilihan:
        with st.container(key="pilihan_box"):
            st.markdown(f"**{data_event_pilihan[0]}**")

            if st.button("Lihat detail kegiatan", key="detail_kalender"):
                detail_kegiatan(data_event_pilihan[0], data_event_pilihan[1])
    else:
        st.markdown(
            '<div class="kartu">Belum ada kegiatan yang terdaftar pada tanggal ini.</div>',
            unsafe_allow_html=True,
        )

# ==========================================
#  CATATAN KAKI (keterangan tugas)
# ==========================================

st.markdown(
    '<div class="footer-tugas">'
    'Diajukan untuk memenuhi project individu PAI<br>'
    'Rekayasa Perangkat Lunak'
    '</div>',
    unsafe_allow_html=True,
)
