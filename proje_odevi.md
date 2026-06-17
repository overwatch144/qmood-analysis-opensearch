# Yazılım Mimarileri ve Tasarım Yöntemleri Dersi — Dönem Projesi Yönergesi

## QMOOD Tabanlı Yazılım Kalitesi Analizi ve LLM Destekli Değerlendirme

---

## 1. Projenin Amacı

Bu proje kapsamında sizlerin, yazılım mimarisi ve yazılım tasarım kalitesi kavramlarını ölçülebilir metrikler üzerinden analiz etmeleri amaçlanmaktadır. Çalışmada nesne yönelimli yazılım sistemlerinin tasarım kalitesini değerlendirmek için literatürde yaygın olarak kullanılan **QMOOD (Quality Model for Object-Oriented Design)** modeli temel alınacaktır.

Seçilen açık kaynak kodlu bir yazılım sisteminin en az 10 farklı sürümünü inceleyerek yazılımın zaman içerisindeki kalite değişimi analiz edilecektir. Analiz sürecinde QMOOD modelindeki kalite nitelikleri, kalite özellikleri, tasarım özellikleri ve nesne yönelimli yazılım metrikleri kullanılacaktır.

Projenin ikinci aşamasında elde edilen metrik verileri farklı Büyük Dil Modellerine (LLM) verilerek modellerin yazılım kalite değerlendirme yetenekleri karşılaştırılacaktır.

---

## 2. Proje Kapsamı

Projede aşağıdaki temel aşamalar gerçekleştirilecektir:

- Açık kaynak bir yazılım sisteminin seçilmesi
- En az 10 farklı sürümün analiz edilmesi
- QMOOD metriklerinin çıkarılması
- Kalite niteliklerinin hesaplanması
- Yazılım evriminin incelenmesi
- LLM tabanlı kalite değerlendirmelerinin gerçekleştirilmesi
- Sonuçların karşılaştırmalı analizinin yapılması

---

## 3. QMOOD Modeli

Projede aşağıdaki QMOOD bileşenleri kullanılacaktır:

### Tasarım Özellikleri

- Abstraction
- Encapsulation
- Coupling
- Cohesion
- Complexity
- Design Size
- Messaging
- Composition
- Inheritance
- Polymorphism

### Kalite Nitelikleri

- Reusability
- Flexibility
- Understandability
- Functionality
- Extendibility
- Effectiveness

---

## 4. Kullanılabilecek Metrikler

Projede aşağıdaki nesne yönelimli yazılım metrikleri kullanılabilir:

- **DIT** — Depth of Inheritance Tree
- **NOC** — Number of Children
- **WMC** — Weighted Methods per Class
- **CBO** — Coupling Between Objects
- **RFC** — Response for a Class
- **LCOM** — Lack of Cohesion of Methods
- **NOM** — Number of Methods
- **NOA** — Number of Attributes
- **MPC** — Message Passing Coupling
- **DAC** — Data Abstraction Coupling

---

## 5. Yazılım Sürümlerinin Analizi

Her sürüm için aşağıdaki işlemler gerçekleştirilmelidir:

- Kaynak koddan metrik çıkarımı
- QMOOD kalite skorlarının hesaplanması
- Sürümler arası kalite değişiminin incelenmesi
- Mimari bozulmaların yorumlanması
- Teknik borç belirtilerinin değerlendirilmesi

Yazılım büyüdükçe kalite değişimleri analiz edilerek yorumlanmalıdır.

---

## 6. LLM Destekli Kalite Değerlendirmesi

Projede en az 3 farklı LLM modeli kullanılacaktır.

**Örnek modeller:**

- ChatGPT
- Gemini
- Claude
- DeepSeek
- Llama

**LLM modellerine aşağıdaki bilgiler verilebilir** (verilen örneklere benzer bilgilerin sizler tarafından önerilmesi beklenmektedir):

- Yazılım metrikleri
- Coupling ve cohesion değerleri
- Karmaşıklık ölçümleri
- Inheritance yapıları
- Önceki sürümle farklar

**LLM modellerinden aşağıdaki analizler beklenmektedir:**

- Genel kalite değerlendirmesi
- Bakım yapılabilirlik analizi
- Teknik borç tahmini
- Refactoring önerileri
- Mimari kalite yorumları

---

## 7. Kullanılabilecek Araçlar

### Kod Analiz Araçları

- SonarQube
- CK Tool
- Understand
- Designite
- PMD

### Veri Analizi Araçları

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Jupyter Notebook

---

## 8. Beklenen Çıktılar

Proje final sınavı yerine sayılacak ve aşağıdaki çıktılar teslim edilecektir:

- Teknik rapor
- Sunum dosyası
- Analiz kodları
- Kullanılan promptlar
- Grafikler ve görselleştirmeler
- GitHub proje bağlantısı

**Raporda aşağıdaki bölümlerin bulunması beklenmektedir:**

1. Giriş
2. Literatür Özeti
3. Yöntem
4. Analiz Süreci
5. Sonuçlar
6. Tartışma
7. Sonuç ve Gelecek Çalışmalar

---

## 9. Değerlendirme Kriterleri

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

## 10. Proje Kuralları

- Projeler en fazla 3 kişilik gruplar halinde yapılabilir.
- Her grubun farklı yazılım sistemi seçmesi gerekmektedir.
- Kullanılan tüm kaynaklar referans gösterilmelidir.
- Prompt mühendisliği süreci raporda açıklanmalıdır.
- LLM çıktıları eleştirel biçimde değerlendirilmelidir.
- Hazır analiz sonuçlarının doğrudan kullanılması yasaktır.