# QMOOD Tabanlı Yazılım Kalitesi Analizi — Yapılacaklar Listesi

**Seçilen Yazılım:** OpenSearch Anomaly Detection (`opensearch-project/anomaly-detection`)
**Ders:** Yazılım Mimarileri ve Tasarım Yöntemleri — Dönem Projesi

---

## Aşama 0 — Hazırlık

- [x] Repoyu klonla: `git clone https://github.com/opensearch-project/anomaly-detection.git`
- [x] Tüm sürümleri listele: `git tag` ile mevcut release/tag'leri çıkar (80+ tag listelendi)
- [x] Sürüm stratejisine karar ver: **büyük sıçramalar** seçildi (1.0→1.1→1.3→2.0→…→3.0)
- [x] Analiz edilecek 12 sürümü kesinleştir: 1.0.0.0, 1.1.0.0, 1.3.0.0, 2.0.0.0, 2.2.0.0, 2.4.0.0, 2.7.0.0, 2.10.0.0, 2.13.0.0, 2.16.0.0, 2.19.0.0, 3.0.0.0
- [x] Her sürümü `git checkout <tag>` ile kontrol et (extract_metrics.sh scripti ile otomatize edildi)
- [x] Java dilinin baskın olduğunu ve sürüm sayısının 10+ olduğunu teyit et (255–550 Java dosyası, 288–609 sınıf)
- [ ] Grup içi iş bölümünü netleştir (3 kişi varsa)

---

## Aşama 1 — Metrik Çıkarımı (Değerlendirme: %15)

- [x] CK Tool'u kur ve çalıştırmayı dene (ck-0.7.0-jar-with-dependencies.jar indirildi)
- [x] Her sürüm için CK Tool'u çalıştır, sınıf-bazlı CSV üret (`metrics/<version>/class.csv`)
- [x] Şu metrikleri topla: CBO, DIT, NOC, WMC, RFC, LCOM, NOM, NOA (tamamı CK Tool'dan)
- [x] QMOOD'un ihtiyaç duyduğu ek tasarım metriklerini belirle (DAM, CAM, MOA, MFA, DCC, ANA, NOP, DSC, CIS)
- [x] CK Tool'un vermediği metrikler için: Python scriptiyle (`qmood_analysis.py`) CK çıktısından türetildi (TCC→CAM, privateFieldsQty→DAM, abstractMethodsQty→ANA vb.)
- [x] Hangi metriğin hangi araçtan/nasıl geldiğini raporda belgele → rapor.tex Tablo II'de eşleme tablosu mevcut

---

## Aşama 2 — QMOOD Kalite Skorları (Değerlendirme: %20 — en kritik)

- [x] QMOOD hiyerarşisini kur: metrikler → tasarım özellikleri → kalite nitelikleri
- [x] Metrik → tasarım özelliği eşleme tablosunu hazırla (`results/design_properties.csv`)
- [x] Bansiya & Davis (2002) formüllerini uygula (DSC log₂ normalize)
- [x] 6 kalite niteliğini her sürüm için hesapla:
  - [x] Reusability (4.147 → 4.093)
  - [x] Flexibility (0.040 → −0.617)
  - [x] Understandability (−9.572 → −10.798)
  - [x] Functionality (2.988 → 3.204)
  - [x] Extendibility (−3.286 → −4.159)
  - [x] Effectiveness (1.132 → 1.047)
- [x] Hesaplama scriptini yaz (`qmood_analysis.py`) ve tüm sürümler için çalıştır
- [x] Sonuçları tek bir tabloda topla (`results/quality_attributes.csv`)

---

## Aşama 3 — Sürüm Analizi + Görselleştirme (Değerlendirme: %15 + %10)

- [x] Tüm sürümlerin skorlarını Pandas DataFrame'inde birleştir
- [x] Her kalite niteliği için zaman serisi grafiği çiz → `results/quality_attributes_evolution.png`
- [x] Tasarım boyutu (DSC) büyürken kalite değişimini gösteren grafik → `results/design_properties_evolution.png`
- [x] Sürümler arası fark/delta tabloları oluştur → `results/quality_delta.csv` + `quality_delta_heatmap.png`
- [x] Mimari bozulma belirtilerini yorumla → `results/coupling_vs_cohesion.png` (coupling↑ + cohesion sabit = bozulma)
- [x] Teknik borç belirtilerini değerlendir (Max CBO=217, Max WMC=318, LCOM ort. 18–27)
- [x] Grafiklere özen göster — 6 profesyonel grafik üretildi: kalite evrimi, tasarım özellikleri (6 panel), ham metrikler (4 panel), delta heatmap, radar karşılaştırma, coupling vs cohesion

---

## Aşama 4 — LLM Destekli Değerlendirme (Değerlendirme: %20 + %10 karşılaştırma)

- [x] En az 3 LLM seç: **ChatGPT (GPT-4)**, **Google Gemini**, **Claude (Anthropic)**
- [x] Standart prompt hazırla → `llm_prompt.txt` (ham metrikler + tasarım özellikleri + kalite nitelikleri + delta tablosu)
- [x] Prompt mühendisliği sürecini raporda açıkla → rapor.tex Bölüm VI.E
- [x] Her modelden iste:
  - [x] Genel kalite değerlendirmesi
  - [x] Bakım yapılabilirlik analizi
  - [x] Teknik borç tahmini
  - [x] Refactoring önerileri
  - [x] Mimari kalite yorumları
- [x] Modelleri karşılaştır → rapor.tex Tablo VIII + 6 ortak bulgu + 5 farklılık analizi
- [x] LLM çıktılarını eleştirel değerlendir → rapor.tex Bölüm VI.D (bağlam eksikliği, şiddet tutarsızlığı, spekülatif yorumlar)
- [x] LLM tam yanıtları: `chatgpt_response.md`, `gemini_response.md`, `claude_response.md`

---

## Aşama 5 — Rapor + Sunum + Teslim (Değerlendirme: %10)

- [x] Teknik raporu 7 bölümle yaz (IEEE formatında):
  - [x] 1. Giriş
  - [x] 2. Literatür Özeti
  - [x] 3. Yöntem
  - [x] 4. Analiz Süreci
  - [x] 5. Sonuçlar
  - [x] 6. Tartışma (gerçek LLM çıktılarıyla)
  - [x] 7. Sonuç ve Gelecek Çalışmalar
- [x] Kullanılan tüm kaynakları referans göster (14 IEEE formatında referans)
- [x] Sunum dosyasını hazırla → `sunum.pptx` (8 slayt, konuşmacı notlarıyla, ~5.5 dk)
- [x] GitHub deposunu düzenle: analiz kodları, promptlar, grafikler, README
- [x] Teslim çıktıları:
  - [x] Teknik rapor: `rapor.md` + `rapor.tex` + `rapor.pdf` (IEEE iki sütunlu format)
  - [x] Sunum: `sunum.pptx`
  - [x] Analiz kodları: `extract_metrics.sh`, `qmood_analysis.py`, `create_presentation.py`
  - [x] Promptlar: `llm_prompt.txt`
  - [x] Grafikler: `results/` dizininde 6 PNG
  - [x] GitHub bağlantısı: https://github.com/overwatch144/qmood-analysis-opensearch

---

## Değerlendirme Kriterleri Özeti

| Kriter | Ağırlık |
|---|---|
| QMOOD analizinin doğruluğu | %20 |
| Metrik çıkarım süreci | %15 |
| Yazılım sürüm analizi | %15 |
| LLM değerlendirme analizi | %20 |
| Karşılaştırmalı yorumlama | %10 |
| Görselleştirme kalitesi | %10 |
| Rapor düzeni ve akademik yazım | %10 |

---

## Önemli Notlar

- **Her grup farklı sistem seçmeli** — anomaly-detection listede yok, uygun.
- **Çok küçük kütüphaneler reddediliyor** (Jsoup, gson gibi) — anomaly-detection yeterince büyük.
- **Hazır analiz sonuçları doğrudan kullanılamaz.**
- QMOOD doğruluğu (%20) projenin en kritik kısmı — metrik eşlemelerini dikkatli belgele.