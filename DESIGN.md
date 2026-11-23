# Tasarım notları

## Kısa
- Kimin için: Kutay Kılıç. Ziyaretçi: işe alım yapanlar, ekip liderleri, birlikte proje yapmak isteyenler.
- Sitenin işi: kim olduğunu üç saniyede anlatmak, projeleri göstermek, iletişime yönlendirmek.
- Dil: Türkçe (index.html) ve İngilizce (en.html). Metin yalnızca gerçek bilgilerden oluşur; uydurma rakam, referans veya proje yok.

## Konsept kartı
```
Fikir:       Denetçinin çalışma kağıdı. Vurgu kalemi ve tik işareti, BT denetiminden gelen birinin kendi işaretleri.
Metafor:     Denetim çalışma kağıdı: kağıt zemin, lacivert mürekkep, sarı fosforlu kalem, kenarda tik.
İmza:        Girişte "BT denetimi" sözcüğünün altına sarı vurgu çekilir, ardından tik atılır. Projelerde tik, kaynağı açık olan işleri gösterir (lejant var).
Duygu:       Sakin, düzenli, güvenilir. Apple HIG havası.
Hareket fiili: kalemle işaretlemek. Çizgiler soldan sağa çekilir, bir kez.
Ekran görüntüsü: dev "Kutay Kılıç", altında vurgulanmış "BT denetimi" ve tik, sağda kağıda basılmış vesikalık.
```

## Sistem
- Renk (60-30-10): kağıt #f4f2ec (nötr, açık, zemin) / lacivert #14213d (renkli, koyu, yazı ve deneyim ile iletişim bantları) / fosforlu sarı #f6b81a (yalnızca ana buton ve girişteki tek vurgu). Sarı, lacivertin renk çarkında yaklaşık 180 derece karşısı.
- Yazı: sistem yazı tipi (Windows'ta Segoe UI Variable, Apple cihazlarda SF Pro). Bunlar yoksa kendi barındırılan Inter (SIL OFL) devreye girer.
- Izgara: 12 sütun, 1200 px kap, 24 px sütun boşluğu. Köşe yarıçapı 12 px, butonlar hap şeklinde.
- Hareket: yalnızca transform, opacity, stroke-dashoffset. Tek easing. Sayfa durağanken hareket yok; bu bilinçli bir karar (sakin hareket tercihi). Reduced motion'da tüm işaretler baştan çizili, animasyon yok.

## Bölümler
1. Giriş: isim afişi, tek cümle, ana buton, vesikalık.
2. Hakkımda: solda metin, sağda kısa tablo (yıllar ve sayılar sitenin önceki sürümündeki gerçek değerler).
3. Deneyim: lacivert bant, tarih sütunlu kayıt listesi, stajlar.
4. Projeler: tikli liste; iki projede kendi reposundan alınmış gerçek ekran görüntüsü.
5. Yetenekler: dizin biçiminde grup ve araçlar; sertifikalar ve diller.
6. İletişim: lacivert alt bant, büyük e-posta.

## Kaynak ve içerik
- Ekran görüntüleri: kutaykilicai/vault-breach ve kutaykilicai/kuti-dock depolarındaki docs ve assets klasörleri (kişisel yol ve makine bilgisi içeren kısımlar kırpıldı).
- Metin tools/content.py içinde; `python3 tools/build.py` iki HTML dosyasını üretir.
