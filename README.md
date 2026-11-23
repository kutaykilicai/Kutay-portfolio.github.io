# Kutay Kılıç

Kişisel portfolyo sitem. GitHub Pages üzerinde yayında:
https://kutaykilicai.github.io/Kutay-portfolio.github.io/

![Sitenin giriş bölümü](docs/ekran-goruntusu.webp)

## Yapı

Derleme adımı olmayan statik bir site: HTML, CSS ve biraz JavaScript. `index.html` Türkçe, `en.html` İngilizce sürüm.

Metnin tamamı `tools/content.py` dosyasında, iki dil yan yana duruyor. Metni değiştirdikten sonra iki sayfayı yeniden üretmek için depo kökünde şunu çalıştırın:

```
python3 tools/build.py
```

Tasarım kararları (renkler, yazı, bölümler) `DESIGN.md` içinde. Kasım 2026 yeniden tasarımından önceki sürüm `onceki-tasarim-20261123` etiketinde duruyor.

## Kaynaklar

- Yazı tipi: cihazın sistem yazı tipi (Segoe UI Variable, SF Pro). Bulunmadığında `fonts/` klasöründeki Inter kullanılır; Inter SIL Open Font License 1.1 ile lisanslıdır.
- Proje ekran görüntüleri kendi depolarımdan alındı: kutaykilicai/vault-breach ve kutaykilicai/kuti-dock.

## Lisans

MIT
