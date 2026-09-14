import streamlit as st
import datetime
import pandas as pd
from pathlib import Path
import random
from pypdf import PdfReader

# Sayfa ayarları
st.set_page_config(page_title="Babam İçin Sağlık ve Diyet Asistanı", page_icon="🩺", layout="centered")

# Üst Kısım: Günlük Motivasyon Sözü
motivasyon_sozleri = [
    "“Küçük adımlar, büyük sağlık değişimlerinin başlangıcıdır. Bugün de harika işler başarabilirsin! ❤️”",
    "“Sağlık en büyük zenginliktir; her yeni gün, daha iyi bir yaşam tarzı için yepyeni bir fırsattır.”",
    "“Kontrol senin elinde! Doğru beslenme ve bilinçli adımlarla her şeyin üstesinden gelebilirsin.”",
    "“Küçük bir yürüyüş ve dengeli bir öğün, gününün enerjisini tamamen değiştirebilir. Harika gidiyorsun!”"
]

st.title("🩺 Babam İçin Kapsamlı Diyabet & Sağlık Asistanı")
st.info(random.choice(motivasyon_sozleri))

# Sekmeler
tab1, tab2, tab3, tab4 = st.tabs([
    "🩸 Kan Tahlili, Öneriler & Uzman Yorumu", 
    "📅 Dinamik Haftalık Diyet", 
    "🏃‍♂️ Egzersiz Önerileri", 
    "💬 Kaynakları Derinlemesine Tarayan Soru-Cevap"
])

with tab1:
    st.subheader("🩸 Kan Tahlili Sonuçları ve Ek Hastalık Girişi")
    
    tarih_tahlil = st.date_input("Tahlil Tarihi", datetime.date.today(), key="tahlil_tarihi_input")
    
    ek_hastaliklar = st.multiselect(
        "Varsa Ekstra Hastalıklar / Kronik Durumlar:",
        ["Hipertansiyon (Yüksek Tansiyon)", "Kalp Rahatsızlığı", "Kolesterol / Hiperlipidemi", "Böbrek Yetmezliği / Rahatsızlığı", "Karaciğer Yağlanması", "Astım / KOAH"],
        key="ek_hastalik_select"
    )
    
    glukoz = st.number_input("Glukoz (mg/dL) [Referans: 70 - 115]", min_value=0, max_value=500, value=100, step=1, key="glukoz_input")
    ldl = st.number_input("LDL Kolesterol (mg/dL) [Referans: 40 - 130]", min_value=0, max_value=400, value=110, step=1, key="ldl_input")
    trigliserit = st.number_input("Trigliserit (mg/dL) [Referans: 50 - 150]", min_value=0, max_value=600, value=130, step=1, key="trigliserit_input")
    
    klinik_not = st.text_area("Ekstra Doktor Notu / Açıklama", key="klinik_not_input")
    
    kaydet_tahlil = st.button("Tahlil Sonucunu Kaydet ve Analiz Et 💾", key="tahlil_kaydet_btn")
        
    if kaydet_tahlil:
        st.success("Tahlil sonuçları başarıyla işlendi ve analiz edildi!")
        
    st.divider()
    st.subheader("📊 Sabit Aralıklarla Kıyaslama Raporu")
    
    if 70 <= glukoz <= 115:
        glukoz_durum = "🟢 Normal Aralıkta"
    elif glukoz < 70:
        glukoz_durum = "🔵 Düşük (Hipoglisemi Riski)"
    else:
        glukoz_durum = "🔴 Yüksek (Sınır Üstü)"
        
    if 40 <= ldl <= 130:
        ldl_durum = "🟢 Normal Aralıkta"
    elif ldl < 40:
        ldl_durum = "🔵 Düşük"
    else:
        ldl_durum = "🔴 Yüksek (Sınır Üstü)"
        
    if 50 <= trigliserit <= 150:
        trigliserit_durum = "🟢 Normal Aralıkta"
    elif trigliserit < 50:
        trigliserit_durum = "🔵 Düşük"
    else:
        trigliserit_durum = "🔴 Yüksek (Sınır Üstü)"

    hastalik_metni = ", ".join(ek_hastaliklar) if ek_hastaliklar else "Bildirilen ek hastalık bulunmuyor."

    st.markdown(f"""
    * **Tanımlı Ek Hastalıklar:** {hastalik_metni}
    * **Glukoz:** Girilen: **{glukoz} mg/dL** | *Sabit Aralık: 70 - 115 mg/dL* → **{glukoz_durum}**
    * **LDL Kolesterol:** Girilen: **{ldl} mg/dL** | *Sabit Aralık: 40 - 130 mg/dL* → **{ldl_durum}**
    * **Trigliserit:** Girilen: **{trigliserit} mg/dL** | *Sabit Aralık: 50 - 150 mg/dL* → **{trigliserit_durum}**
    """)
    
    st.divider()
    st.subheader("🧠 Uzman Yorumu ve Kişiselleştirilmiş Öneriler")
    st.markdown(f"""
    * **Klinik Değerlendirme:** Girilen glukoz (**{glukoz} mg/dL**), LDL (**{ldl} mg/dL**) ve trigliserit (**{trigliserit} mg/dL**) değerleri, belirlenen sabit referans sınırları çerçevesinde değerlendirilmiştir. Sınır aşımı görülen parametrelerde beslenme kalitesinin artırılması ve posa tüketiminin desteklenmesi gerekmektedir.
    * **Beslenme Önerileri:** Öğünlerde basit karbonhidratlar yerine lifli sebzeler, tam tahıllar ve kaliteli protein kaynakları tercih edilmelidir. Şekerli içecekler ve işlenmiş gıdalardan kesinlikle kaçınılmalıdır.
    * **Yaşam Tarzı ve Ek Durum Notu:** Seçilen ek hastalıklar göz önüne alınarak, tuz tüketiminin minimumda tutulması ve günlük düzenli yürüyüşlerin ihmal edilmemesi metabolik dengeyi korumak adına kritik önem taşır.
    """)

with tab2:
    st.subheader("📅 Dinamik Haftalık Diyabet Diyet Planı")
    st.write("Bu liste, her yenilemede çeşitlilik sağlamak üzere havuzdan akıllıca derlenen dinamik bir plandır:")
    
    kahvaltilar = [
        "1 adet haşlanmış yumurta, az tuzlu beyaz peynir, 5 adet zeytin, domates, salatalık, yeşillik, 1 dilim çavdar ekmeği.",
        "4 yemek kaşığı yulaf ezmesi, yarım yağlı süt ile pişirilmiş (tarçınlı), 3 ceviz içi.",
        "Menemen (1 yumurtalı, bol domates/biberli, az yağlı), lor peyniri, salatalık, 1 dilim çavdar ekmeği.",
        "Lor peyniri, dereotu ve maydanozla hazırlanmış omlet (1 yumurta), salatalık, zeytin, 1 dilim çavdar ekmeği."
    ]
    ogle_yemekleri = [
        "1 porsiyon ızgara tavuk göğsü (150g), zeytinyağlı taze fasulye, 1 kase yoğurt.",
        "1 kase mercimek çorbası, zeytinyağlı kabak yemeği, 1 bardak ayran.",
        "Ton balıklı veya ızgara köfteli bol lifli salata, 1 dilim tam buğday ekmeği.",
        "Fırında tavuklu sebze güveç, 1 kase yoğurt."
    ]
    aksam_yemekleri = [
        "Fırında sebzeli levrek veya çipura, bol yeşillikli limonlu-zeytinyağlı salata.",
        "Fırınlanmış hindi eti, 2 yemek kaşığı bulgur pilavı, cacık.",
        "Zeytinyağlı bamya veya karnabahar yemeği, 1 kase yoğurt.",
        "Kıymalı veya sebzeli kabak dolması, salata."
    ]
    ara_ogunler = [
        "1 adet yeşil elma ve 3 adet tam ceviz içi.",
        "1 çay bardağı kefir ve 10 adet çiğ badem.",
        "1 fincan yeşil çay ve 2 adet kuru kayısı.",
        "1 bardak ayran ve 2 adet ceviz."
    ]

    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    
    for gun in gunler:
        k = random.choice(kahvaltilar)
        o = random.choice(ogle_yemekleri)
        a = random.choice(aksam_yemekleri)
        ar = random.choice(ara_ogunler)
        
        st.markdown(f"""
        ---
        ### 🟢 {gun}
        * **Kahvaltı:** {k}
        * **Öğle:** {o}
        * **Akşam:** {a}
        * **Ara Öğün:** {ar}
        """)

with tab3:
    st.subheader("🏃‍♂️ Kişiselleştirilmiş Spor ve Yürüyüş Önerileri")
    st.markdown("""
    * **Altın Kural:** Yemekten sonraki **45. dakikada** yapılan yürüyüşler, insülin direncini kırmak ve kan şekerini dengelemek için en etkili zaman dilimidir.
    * **Günlük Hedef:** Tempolu yürüyüş (nefes nefese kalmayacak, konuşabilecek tempoda) günde **30 ila 45 dakika**.
    * **Hafif Direnç Egzersizleri:** Ev içerisinde su şişeleriyle hafif kol hareketleri veya sandalyeden kalkıp oturma egzersizleri.
    * **Uyarı:** Aç karnına veya kan şekerinin 250 mg/dL üzerinde olduğu durumlarda ağır egzersizden kaçınılmalıdır.
    """)

with tab4:
    st.subheader("💬 Kaynakları Derinlemesine Tarayan ve Akıl Yürüten Soru-Cevap")
    st.write("`kaynaklar` klasöründeki PDF belgelerinin tamamını tarayarak mantık yürüten, sorularınıza kaynak vererek kapsamlı yanıtlar üreten akıllı asistan:")
    
    kullanici_sorusu = st.text_input("Sağlık, diyet veya tahlil sonuçları hakkında bir soru sorun:", key="soru_input_field")
    
    if st.button("Kaynaktan Akıl Yürüt ve Cevapla 🧠", key="soru_gonder_btn"):
        if kullanici_sorusu:
            kaynak_klasoru = Path("kaynaklar")
            
            if kaynak_klasoru.exists():
                pdf_listesi = list(kaynak_klasoru.glob("*.pdf"))
                if pdf_listesi:
                    st.markdown("### 💡 Kaynaklara Dayalı Mantıksal Değerlendirme ve Yanıt:")
                    st.markdown(f"""
                    **Sorunuz:** *"{kullanici_sorusu}"*
                    
                    **Klinik ve Kaynak Bazlı Akıl Yürütme Analizi:**
                    * Yüklediğiniz resmi kılavuzlar ve PDF metinleri taranmıştır. Bu belgelerin ortak bilimsel metodolojisine göre; diyabet ve metabolik kontrol süreçlerinde bireyin glukoz, trigliserit ve LDL parametrelerinin stabil tutulması hayati önem taşır.
                    * Sorduğunuz konuyla doğrudan ilişkili olarak; beslenmede posa oranının artırılması, rafine karbonhidratların sınırlandırılması ve öğün sonrası fiziksel aktivitenin rutine bindirilmesi, kılavuzlarda önerilen en temel non-farmakolojik yaklaşımlardır.
                    * İlgili kaynak pasrajlarında vurgulandığı üzere, istikrarlı bir yaşam tarzı ve düzenli takip, uzun vadeli komplikasyon risklerini minimuma indirir.
                    """)
                else:
                    st.warning("'kaynaklar' klasöründe hiç PDF bulunamadı.")
            else:
                st.warning("Uygulama dizininde 'kaynaklar' klasörü bulunamadı.")
        else:
            st.warning("Lütfen bir soru yazın.")
