# 🚀 Kutay Kılıç - Personal Portfolio

<div align="center">

![Portfolio Preview](https://img.shields.io/badge/Status-Live-brightgreen?style=for-the-badge)
![HTML5](https://img.shields.io/badge/HTML5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-%23F7DF1E.svg?style=for-the-badge&logo=javascript&logoColor=black)

**[🌐 Live Demo](https://kutaykilicai.github.io/Kutay-portfolio.github.io/)**

*Minimalist ve modern tasarımla oluşturulmuş kişisel portfolyo websitesi*

---

</div>

## 📋 İçerik

- [Hakkında](#-hakkında)
- [Özellikler](#-özellikler)
- [Teknolojiler](#-teknolojiler)
- [Kurulum](#-kurulum)
- [Kullanım](#-kullanım)
- [Proje Yapısı](#-proje-yapısı)
- [Özelleştirme](#-özelleştirme)
- [Deployment](#-deployment)
- [Katkıda Bulunma](#-katkıda-bulunma)
- [İletişim](#-i̇letişim)

## 🎯 Hakkında

Bu proje, Kutay Kılıç'ın profesyonel becerilerini, projelerini ve deneyimlerini sergilemek için tasarlanmış modern bir kişisel portfolyo websitesidir. Temiz ve kullanıcı dostu arayüzü ile ziyaretçilere etkileyici bir deneyim sunar.

### ✨ Temel Amacı
- Profesyonel profili ve yetenekleri sergilemek
- Tamamlanan projeleri görsellerle sunmak
- Potansiyel işverenler ve müşteriler için kolay erişilebilir bir platform oluşturmak
- Modern web standartlarına uygun responsive tasarım sunmak

## 🌟 Özellikler

### 🎨 Tasarım
- **Responsive Tasarım**: Tüm cihazlarda mükemmel görünüm
- **Modern UI/UX**: Minimalist ve kullanıcı dostu arayüz
- **Smooth Animations**: Akıcı geçiş efektleri ve micro-interactions
- **Dark/Light Theme**: Kullanıcı tercihine göre tema seçimi

### 🔧 Fonksiyonalite
- **Hızlı Yükleme**: Optimize edilmiş performans
- **SEO Friendly**: Arama motorları için optimize edilmiş
- **Cross-Browser Support**: Tüm modern tarayıcılarda uyumlu
- **Accessibility**: WCAG standartlarına uygun erişilebilirlik

### 📱 Bölümler
- **Ana Sayfa**: Etkileyici hero section ve kısa tanıtım
- **Hakkımda**: Detaylı profil bilgileri ve özgeçmiş
- **Projeler**: Portfolio çalışmaları ve case studies
- **Yetenekler**: Teknik beceriler ve yeterlilikler
- **İletişim**: Kolay erişilebilir iletişim formu

## 🛠 Teknolojiler

### Frontend
```
HTML5      - Semantic markup ve yapı
CSS3       - Modern styling ve flexbox/grid
JavaScript - Interaktif özellikler ve DOM manipülasyonu
```

### Araçlar ve Kütüphaneler
- **Font Awesome**: İkonlar için
- **Google Fonts**: Typography için
- **AOS Library**: Scroll animasyonları için
- **Vanilla JS**: Framework bağımlılığı olmadan

### Hosting & Deployment
- **GitHub Pages**: Ücretsiz ve güvenilir hosting
- **Custom Domain**: Profesyonel görünüm için

## 🚀 Kurulum

### Ön Koşullar
- Git
- Modern web browser
- Code editor (VS Code önerilen)

### Adımlar

1. **Repository'yi klonlayın**
```bash
git clone https://github.com/kutaykilicai/Kutay-portfolio.github.io.git
cd Kutay-portfolio.github.io
```

2. **Proje dosyalarını açın**
```bash
# VS Code ile açmak için
code .
```

3. **Live Server ile çalıştırın**
- VS Code Live Server extension kullanın
- Veya herhangi bir local server ile `index.html` dosyasını açın

### Hızlı Başlangıç
```bash
# Proje klasörüne gidin
cd Kutay-portfolio.github.io

# Python ile basit server başlatın
python -m http.server 8000

# Tarayıcıda açın: http://localhost:8000
```

## 📁 Proje Yapısı

```
Kutay-portfolio.github.io/
├── 📁 assets/
│   ├── 📁 css/
│   │   ├── style.css
│   │   └── responsive.css
│   ├── 📁 js/
│   │   ├── main.js
│   │   └── animations.js
│   ├── 📁 images/
│   │   ├── profile/
│   │   ├── projects/
│   │   └── icons/
│   └── 📁 fonts/
├── 📁 components/
│   ├── header.html
│   ├── footer.html
│   └── navigation.html
├── 📄 index.html
├── 📄 about.html
├── 📄 projects.html
├── 📄 contact.html
├── 📄 README.md
└── 📄 LICENSE
```

## 🎨 Özelleştirme

### Renk Paleti Değiştirme
```css
/* assets/css/style.css dosyasında */
:root {
  --primary-color: #your-color;
  --secondary-color: #your-color;
  --accent-color: #your-color;
}
```

### İçerik Güncelleme
1. **Kişisel Bilgiler**: `index.html` ve `about.html` dosyalarını düzenleyin
2. **Projeler**: `projects.html` dosyasına yeni projeler ekleyin
3. **Görseller**: `assets/images/` klasörüne yeni görseller ekleyin

### Animasyon Ayarları
```javascript
// assets/js/animations.js dosyasında
AOS.init({
  duration: 800,
  delay: 100,
  once: true
});
```

## 🌐 Deployment

### GitHub Pages ile Otomatik Deployment

1. **Repository ayarları**
```
Settings > Pages > Source: Deploy from a branch
Branch: main (veya master)
Folder: / (root)
```

2. **Custom Domain (Opsiyonel)**
- `CNAME` dosyası oluşturun
- Domain'inizi `your-domain.com` şeklinde yazın

### Manuel Deployment
```bash
# Değişiklikleri commit edin
git add .
git commit -m "Update portfolio content"

# GitHub'a push edin
git push origin main
```

## 📊 Performans Optimizasyonu

### Görsel Optimizasyonu
- Görselleri WebP formatında kullanın
- Lazy loading implementasyonu
- Responsive images ile multiple sizes

### CSS & JS Optimizasyonu
```html
<!-- Critical CSS inline -->
<style>
  /* Critical styles here */
</style>

<!-- Non-critical CSS -->
<link rel="preload" href="assets/css/style.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

## 🔍 SEO Optimizasyonu

### Meta Tags
```html
<meta name="description" content="Kutay Kılıç - Web Developer Portfolio">
<meta name="keywords" content="web developer, frontend, portfolio, kutay kılıç">
<meta property="og:title" content="Kutay Kılıç - Personal Portfolio">
<meta property="og:description" content="Modern web developer portfolio">
<meta property="og:image" content="assets/images/og-image.jpg">
```

### Structured Data
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Kutay Kılıç",
  "jobTitle": "Web Developer",
  "url": "https://kutaykilicai.github.io/Kutay-portfolio.github.io/"
}
```

## 🤝 Katkıda Bulunma

Katkılarınız her zaman hoş karşılanır! Katkıda bulunmak için:

1. **Fork** edin
2. **Feature branch** oluşturun (`git checkout -b feature/amazing-feature`)
3. **Commit** edin (`git commit -m 'Add amazing feature'`)
4. **Push** edin (`git push origin feature/amazing-feature`)
5. **Pull Request** oluşturun

### Katkı Kuralları
- Clean ve readable code yazın
- Responsive design prensiplerini takip edin
- Browser compatibility'yi test edin
- Commit mesajlarında conventional commits kullanın

## 🐛 Bug Report

Bug bulduysanız lütfen şunları belirtin:
- Tarayıcı ve versiyonu
- İşletim sistemi
- Hatanın yeniden üretilme adımları
- Beklenen ve gerçek davranış

## 📜 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

```
MIT License

Copyright (c) 2024 Kutay Kılıç

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

## 📞 İletişim

<div align="center">

**Kutay Kılıç**

[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-blue?style=for-the-badge)](https://kutaykilicai.github.io/Kutay-portfolio.github.io/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/kutay-kilic)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail)](mailto:kutay@example.com)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/kutaykilicai)

</div>

---

<div align="center">

**⭐ Bu projeyi beğendiyseniz star vermeyi unutmayın!**

*Made with ❤️ by Kutay Kılıç*

</div>
