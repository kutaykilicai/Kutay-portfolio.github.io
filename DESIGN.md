# Tasarım notları

## Kısa
- Kimin için: Kutay Kılıç. Ziyaretçi: işe alım yapanlar, ekip liderleri, birlikte proje yapmak isteyenler.
- Sitenin işi: kim olduğunu üç saniyede anlatmak, kendi yazdığı uygulamaları göstermek, iletişime yönlendirmek.
- Dil: Türkçe (index.html) ve İngilizce (en.html). Metin yalnızca gerçek kaynaklardan (depo README'leri, önceki sürüm) gelir; uydurma rakam, referans veya proje yok.

## Konsept kartı
```
Fikir:        Site, Kutay'ın kendi yazdığı Windows uygulamalarından biri gibi açılır: araç çubuğu, yan panel, Mica yüzeyler.
Metafor:      Masaüstü uygulama penceresi (Ağaç Boyutu ve DeepSeek Ajan'daki araç çubuğu + yan menü düzeni).
İmza:         Projelerdeki segmentli süzgeç: seçim hapı kategoriye kayar, kartlar yumuşakça yer değiştirir. Araç çubuğunun ortası bulunulan bölümün adını gösterir.
Duygu:        Sakin, düzenli, yerli bir Windows uygulaması kadar tanıdık.
Hareket fiili: yerine oturmak. Kısa yükselme, tek easing (cubic-bezier .22,1,.36,1).
Ekran görüntüsü: dev "Kutay Kılıç", altında kırmızı vurgulu "masaüstü uygulamaları ve yapay zeka ajanları", solda yan panel.
```

## Sistem
- Renk jetonları `style.css` içindeki `:root` bloğunda; paleti değiştirmek için yalnızca orayı düzenle.
  - Zemin Jet Black #0B0B0C, yüzeyler #141416 ve #1C1C1E, yükseltilmiş yüzey #2A2A2D, başlıklar #F3F4F6.
  - Smoke Grey #6A6C6E yalnızca kenarlık ve ayraçlarda; küçük metinde AA'yı geçmediği için ikincil yazı ve menü #9A9C9E.
  - Tek vurgu: Cherry Red #C41E1E. Yalnızca ana buton, logo ve girişteki tek vurgu çizgisi. Bağlantılar başlık rengindedir, odak halkası #F3F4F6.
  - Kontrast: başlık/zemin 17,9:1, ikincil yazı/zemin 7,1:1, ana buton beyaz/kırmızı 5,9:1.
- Yazı: Segoe UI Variable, -apple-system, SF Pro; ikisi de yoksa kendi barındırılan Inter, sonra system-ui.
- Menü bağlantıları büyük harf, 11 px, harf aralığı .08em. Girişte küçük büyük harfli rozet (1 px rgba(255,255,255,.2) kenar, 4 px köşe). H1 44 ile 64 px arası, satır yüksekliği 1,05, harf aralığı -0,02em, ağırlık 500.
- Düğmeler hap biçiminde (9999 px): ana düğme kırmızı dolgu ve beyaz yazı, ikincil düğme rgba(255,255,255,.05) zemin ve rgba(255,255,255,.25) kenar.
- Giriş fotoğrafı sağda, soldan siyaha eriyen geçiş, alt solma ve hafif kırmızı kenar parıltısıyla. Altında üst çizgili şeritte üç gerçek bilgi.
- Kart köşe yarıçapı 12 px. Araç çubuğu ve yan panel yarı saydam, backdrop-filter bulanıklığıyla Mica hissi; zeminde çok hafif doku.
- Hareket: yalnızca transform ve opacity. Giriş sırayla yükselir, bölümler görünür alana girince belirir (IntersectionObserver), üzerine gelince kart kalkar, basınca düğme küçülür, üzerine gelince parlaklık hafifçe artar, giriş fotoğrafı 40 saniyede çok yavaş büyür. prefers-reduced-motion açıksa hareket yok.
- Telefonda yan panel araç çubuğundaki düğmeyle açılan çekmeceye dönüşür.

## Bölümler
1. Giriş: isim, tek cümle, ana buton, eriyen portre, üç gerçek bilgi (proje ve açık depo sayısı content.py'den hesaplanır).
2. Hakkımda: metin, kısa tablo, deneyim ve stajlar.
3. Projeler: segmentli süzgeç, ekran görüntülü öne çıkanlar, diğer projeler listesi. Özel depolar bağlantısız ve işaretli.
4. Yetenekler, sertifikalar, diller.
5. Jüri: DeepSeek ve Gemini'nin son tur puanları ve gerekçeleri (tools/jury.json). Puanı site sahibi ya da yapan ajan vermez.
6. İletişim.

## Kaynak ve içerik
- Ekran görüntüleri: kutaykilicai/agac-boyutu, bolmeler, robokopya, hizli-indir, kuti-dock ve vault-breach depolarındaki örnek verili görüntüler.
- Metin tools/content.py içinde; `python3 tools/build.py` iki HTML dosyasını üretir.
