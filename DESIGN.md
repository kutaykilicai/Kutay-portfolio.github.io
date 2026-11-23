# Tasarım notları (v3)

## Kısa
- Kimin için: Kutay Kılıç. Ziyaretçi: işe alım yapanlar, ekip liderleri, birlikte proje yapmak isteyenler.
- Dil: Türkçe (index.html) ve İngilizce (en.html). Metin yalnızca gerçek kaynaklardan (depo README'leri, önceki sürüm) gelir; uydurma rakam, referans ya da proje yok.

## Düzen
- sreedesigns.com düzeninden esinli editoryal ızgara: kenarlarda ve dört sütunda sayfa boyu 1 px dikey çizgiler, bölümler arasında 1 px yatay çizgiler.
- Sabit, saydam üst menü: solda KK logosu ve ad, sağda köşeli parantezli bağlantılar. Sol altta © 2026, sağ altta LinkedIn ve GitHub.
- Giriş: tam ekran, kendi yazdığım WebGL ipek shader'ı (lacivertten grafite akış, hafif ark reaktörü mavisi). Azaltılmış harekette ya da WebGL yoksa CSS degradesi.
- İşler: dört sütunlu ızgarada 7 öne çıkan proje, kaydırmalı yükseklikler, bir geniş kart, 3+1 satır. Üzerine gelince imleci izleyen ışık ve tarama çizgisi; kart üstten çıkarken 0,93'e küçülüp solar.
- Deneyler: çizgili bento. Tüm projeler: Proje, Açıklama, Yığın, bağlantı sütunlu tablo; masaüstünde imleci izleyen önizleme.
- Hakkımda, araçlar şeridi, yapay zeka jürisi alıntıları (001 / 008 sayaçlı, soldurarak geçiş), kelime ağlı altbilgi.
- E-posta bağlantısı açmadan önce sorar ve adresi kopyalama seçeneği sunar.

## Sistem
- Renk jetonları `style.css` içindeki `:root` bloğunda. Zemin #0A0B0D, yüzeyler #121418 ve #1A1D22, çizgi rgba(255,255,255,.08), yazı #EDEFF2, ikincil yazı #9AA1AB (zeminde 7,6:1), vurgu #5AC8FA (10:1), etkileşim #0A84FF. Altın #C9A227 yalnızca köşedeki küçük nokta. Kırmızı yok.
- Yazı: başlıklar Newsreader (OFL, kendi barındırılan), arayüz Inter (OFL), sonra Segoe UI Variable ve SF. Sayaçlar tabular-nums.
- Kartlar düz, 2-4 px köşe, gölge yok. Bağlantı ve düğmeler köşeli parantez tipografisi.
- Hareket: yalnızca transform ve opacity; belirme 0,3 sn ease, 100 ms aralıklı. prefers-reduced-motion açıkken hareket yok.

## Kaynak
- Metin tools/content.py içinde; `python3 tools/build.py` iki HTML dosyasını üretir. Jüri sonuçları tools/jury.json.
