# QMOOD Tabanlı Yazılım Kalitesi Analizi ve LLM Destekli Değerlendirme: OpenSearch Anomaly Detection Üzerine Ampirik Bir Çalışma

---

**Özet** — Bu çalışmada, açık kaynak kodlu OpenSearch Anomaly Detection projesinin 12 farklı sürümü üzerinde QMOOD (Quality Model for Object-Oriented Design) modeli kullanılarak sistematik bir yazılım tasarım kalitesi analizi gerçekleştirilmiştir. CK Tool aracılığıyla çıkarılan nesne yönelimli metriklerden (CBO, DIT, WMC, RFC, LCOM) 10 tasarım özelliği hesaplanmış ve Bansiya-Davis formülleriyle 6 kalite niteliği (Reusability, Flexibility, Understandability, Functionality, Extendibility, Effectiveness) elde edilmiştir. Sürüm bazlı evrim analizi, projenin 288 sınıftan 609 sınıfa büyümesi sürecinde coupling'in monoton artış (%22.1), encapsulation'ın belirgin düşüş (%22.3) ve extendibility'nin sürekli kötüleşme (%26.6) gösterdiğini ortaya koymuştur. Özellikle v2.16.0.0 sürümü, 227 yeni sınıf eklenmesiyle kritik bir kırılma noktası olarak tespit edilmiştir. Çalışmanın ikinci aşamasında, elde edilen metrik verileri ChatGPT (GPT-4), Google Gemini ve Claude olmak üzere üç farklı Büyük Dil Modeli'ne (LLM) sunulmuş ve modellerin yazılım kalitesi değerlendirme yetenekleri karşılaştırılmıştır. LLM'lerin metrik trendlerini doğru yorumladığı, ancak projeye özgü bağlam olmadan refactoring önerilerinin genel kaldığı tespit edilmiştir.

**Anahtar Kelimeler** — QMOOD, yazılım kalitesi, nesne yönelimli metrikler, yazılım evrimi, teknik borç, büyük dil modelleri, CK metrikleri, OpenSearch

---

## I. GİRİŞ

Yazılım sistemleri, yaşam döngüleri boyunca sürekli değişime uğramakta ve bu değişimler tasarım kalitesini doğrudan etkilemektedir. Lehman'ın yazılım evrimi yasalarına göre [1], bir yazılım sistemi çevresine uyum sağlamak için sürekli değiştirilmeli, ancak bu değişiklikler kontrol edilmediğinde yapısal bozulmaya (architectural erosion) yol açmaktadır. Bu bağlamda, nesne yönelimli yazılım sistemlerinin tasarım kalitesinin ölçülebilir metriklerle izlenmesi, yazılım mühendisliğinin temel araştırma alanlarından birini oluşturmaktadır.

QMOOD (Quality Model for Object-Oriented Design), Bansiya ve Davis [2] tarafından önerilen ve nesne yönelimli tasarım kalitesini hiyerarşik bir yapıda değerlendiren bir modeldir. Model, düşük seviyeli kod metriklerinden yüksek seviyeli kalite niteliklerine uzanan üç katmanlı bir soyutlama sunar. Bu yapı, yazılım evriminin farklı boyutlarını — yeniden kullanılabilirlikten genişletilebilirliğe — sistematik olarak izlemeyi mümkün kılar.

Son yıllarda Büyük Dil Modelleri (LLM), yazılım mühendisliğinde kod inceleme, hata tespiti ve kalite değerlendirme gibi alanlarda kullanılmaya başlanmıştır [3]. Bu modellerin metrik verilerini yorumlama ve kalite değerlendirmesi yapma yetenekleri, geleneksel metrik tabanlı analizlere tamamlayıcı bir perspektif sunma potansiyeli taşımaktadır.

Bu çalışmada, OpenSearch Anomaly Detection projesinin 12 sürümü QMOOD modeli ile analiz edilmiş ve sonuçlar üç farklı LLM ile değerlendirilmiştir. Çalışmanın katkıları şu şekilde özetlenebilir:

- Endüstriyel ölçekte bir Java projesinin 12 sürümlük QMOOD evrim analizi gerçekleştirilmiştir.
- Büyük ölçekli kod eklenmesinin (v2.16) tasarım kalitesine etkisi ampirik olarak gösterilmiştir.
- Üç farklı LLM'in metrik tabanlı kalite değerlendirme yetenekleri karşılaştırılmıştır.
- Prompt mühendisliğinin LLM çıktı kalitesine etkisi incelenmiştir.

Makalenin geri kalanı şu şekilde organize edilmiştir: Bölüm II ilgili çalışmaları özetler; Bölüm III kullanılan yöntemi açıklar; Bölüm IV analiz sürecini detaylandırır; Bölüm V sonuçları sunar; Bölüm VI bulguları tartışır; Bölüm VII sonuç ve gelecek çalışmaları içerir.

---

## II. LİTERATÜR ÖZETİ

### A. QMOOD Modeli

QMOOD, Bansiya ve Davis [2] tarafından 2002 yılında önerilen, nesne yönelimli yazılım sistemlerinin tasarım kalitesini hiyerarşik olarak değerlendiren bir modeldir. Model üç katmandan oluşur:

1. **Nesne yönelimli metrikler:** CBO, DIT, WMC, RFC, LCOM, NOM, NOA gibi doğrudan koddan ölçülen düşük seviyeli metrikler.
2. **Tasarım özellikleri (Design Properties):** Abstraction, Encapsulation, Coupling, Cohesion, Complexity, Design Size, Messaging, Composition, Inheritance, Polymorphism olmak üzere 10 tasarım özelliği.
3. **Kalite nitelikleri (Quality Attributes):** Reusability, Flexibility, Understandability, Functionality, Extendibility, Effectiveness olmak üzere 6 kalite niteliği.

Bansiya ve Davis, kalite niteliklerini tasarım özelliklerinin ağırlıklı doğrusal kombinasyonu olarak formüle etmiştir. Bu formüller, uzman değerlendirmeleriyle ampirik olarak doğrulanmıştır. Model, ISO/IEC 9126 standardıyla uyumlu kalite özelliklerini nesne yönelimli metriklere bağlaması nedeniyle yazılım kalitesi araştırmalarında yaygın biçimde kullanılmaktadır [4].

### B. Chidamber-Kemerer Metrik Seti

Chidamber ve Kemerer (CK) [5] tarafından 1994 yılında önerilen metrik seti, nesne yönelimli yazılımlar için en yaygın kabul görmüş metrik kümesidir. Bu sette yer alan temel metrikler:

- **CBO (Coupling Between Objects):** Bir sınıfın bağımlı olduğu diğer sınıf sayısını ölçer. Yüksek CBO değeri, sınıflar arası yüksek bağımlılığı ve bunun sonucu olarak düşük yeniden kullanılabilirliği gösterir.
- **DIT (Depth of Inheritance Tree):** Kalıtım ağacındaki derinliği ölçer. Derin hiyerarşiler daha fazla kalıtılmış davranış anlamına gelir, ancak anlaşılabilirliği düşürür.
- **WMC (Weighted Methods per Class):** Sınıftaki metotların toplam karmaşıklığını ölçer. Yüksek WMC, sınıfın bakım zorluğunu artırır.
- **RFC (Response for a Class):** Bir nesneye mesaj gönderildiğinde potansiyel olarak çalıştırılabilecek metot sayısıdır.
- **LCOM (Lack of Cohesion of Methods):** Metotlar arası uyum eksikliğini ölçer. Yüksek LCOM değeri, sınıfın birden fazla sorumluluk taşıdığını ve bölünmesi gerektiğini gösterir.
- **NOC (Number of Children):** Bir sınıfın doğrudan alt sınıf sayısını ölçer.

### C. Yazılım Evrimi ve Teknik Borç

Lehman [1], yazılım evrimini yöneten sekiz yasa tanımlamıştır. Bunlardan "sürekli değişim yasası" bir sistemin kullanışlılığını koruyabilmesi için sürekli uyarlanması gerektiğini, "artan karmaşıklık yasası" ise aktif önlem alınmadığında karmaşıklığın monoton artacağını ifade eder. Cunningham [6] tarafından ortaya atılan "teknik borç" metaforu, kısa vadeli tasarım tavizlerinin uzun vadede bakım maliyetlerini faiz gibi artırdığını belirtir. QMOOD metriklerindeki bozulma eğilimleri, teknik borcun nicel göstergeleri olarak yorumlanabilir.

### D. LLM Destekli Yazılım Mühendisliği

Büyük Dil Modelleri (LLM), yazılım mühendisliğinde kod üretimi, hata tespiti, kod inceleme ve kalite değerlendirme gibi alanlarda kullanılmaktadır [3]. Fan vd. [3], LLM'lerin yazılım mühendisliği görevlerindeki başarılarını ve sınırlılıklarını kapsamlı bir şekilde incelemiştir. Hou vd. [7], LLM'lerin yazılım testi alanındaki uygulamalarını sistematik olarak derlemiştir. Bu çalışmalar, LLM'lerin metrik tabanlı değerlendirmelerde umut verici sonuçlar ürettiğini, ancak alan bilgisi ve bağlam olmadan genelleyici yargılara eğilimli olduğunu göstermektedir.

### E. İlgili Ampirik Çalışmalar

Al Dallal [8], QMOOD modelini birden fazla açık kaynak proje üzerinde uygulayarak kalite niteliklerinin yazılım bakımıyla korelasyonunu incelemiştir. Padhy vd. [9], QMOOD metriklerinin yazılım hatalarını tahmin etmedeki etkinliğini araştırmıştır. Singh ve Malhotra [10], nesne yönelimli metriklerin yazılım kalitesini ölçmedeki geçerliliğini ampirik olarak doğrulamıştır. Mevcut çalışma, bu araştırmaları LLM tabanlı değerlendirme boyutuyla genişletmektedir.

---

## III. YÖNTEM

### A. Genel Yaklaşım

Çalışmada izlenen metodoloji dört ana aşamadan oluşmaktadır (Şekil 1):

```
Kaynak Kod ──→ CK Tool ──→ Ham Metrikler ──→ Tasarım Özellikleri ──→ Kalite Nitelikleri
                                                                            │
                                                                            ▼
                                                                    LLM Değerlendirme
```

*Şekil 1. Analiz sürecinin genel akışı.*

### B. Analiz Edilen Sistem

OpenSearch Anomaly Detection, Amazon OpenSearch platformu üzerinde çalışan, zaman serisi verilerinde anomali tespiti yapan açık kaynak kodlu bir Java eklentisidir. Proje aşağıdaki nedenlerle seçilmiştir:

- **Yeterli büyüklük:** 288–609 sınıf arasında değişen, anlamlı metrik analizi için uygun ölçekte bir projedir.
- **Zengin sürüm geçmişi:** 70'ten fazla release tag'i ile geniş bir evrim sürecine sahiptir.
- **Endüstriyel kalite:** Amazon/AWS tarafından desteklenen ve üretim ortamında kullanılan bir yazılımdır.
- **Nesne yönelimli tasarım:** Java dilinde yazılmış, QMOOD analizine uygun bir OOP yapısına sahiptir.

### C. Sürüm Seçim Stratejisi

Kalite değişimlerinin belirgin biçimde gözlemlenmesi amacıyla büyük sıçramalar içeren 12 sürüm seçilmiştir. Tablo I, analiz edilen sürümleri ve temel boyut metriklerini göstermektedir.

*TABLO I. ANALİZ EDİLEN SÜRÜMLER VE BOYUT METRİKLERİ*

| # | Sürüm | Sınıf Sayısı | Java Dosya Sayısı | Toplam LOC |
|---|-------|-------------|-------------------|-----------|
| 1 | 1.0.0.0 | 288 | 255 | 16,903 |
| 2 | 1.1.0.0 | 327 | 287 | 23,354 |
| 3 | 1.3.0.0 | 351 | 307 | 26,338 |
| 4 | 2.0.0.0 | 351 | 307 | 26,363 |
| 5 | 2.2.0.0 | 356 | 312 | 26,604 |
| 6 | 2.4.0.0 | 356 | 312 | 26,610 |
| 7 | 2.7.0.0 | 362 | 318 | 26,932 |
| 8 | 2.10.0.0 | 362 | 318 | 26,930 |
| 9 | 2.13.0.0 | 364 | 320 | 27,041 |
| 10 | 2.16.0.0 | 591 | 534 | 34,392 |
| 11 | 2.19.0.0 | 609 | 550 | 35,613 |
| 12 | 3.0.0.0 | 609 | 550 | 35,612 |

### D. Metrik Çıkarım Aracı

Metrik çıkarımında CK Tool (v0.7.0) [11] kullanılmıştır. CK Tool, Mauricio Aniche tarafından geliştirilmiş açık kaynak bir Java metrik analiz aracıdır ve sınıf bazında CSV formatında çıktı üretir. Araç, CBO, DIT, NOC, WMC, RFC, LCOM metriklerinin yanı sıra TCC (Tight Class Cohesion), publicMethodsQty, privateFieldsQty, abstractMethodsQty gibi ek metrikleri de sağlamaktadır.

Her sürüm için `src/main/java` dizini analiz edilmiş, test kodları (`src/test/`) analiz kapsamı dışında bırakılmıştır. Otomatik çıkarım, bir bash scripti ile gerçekleştirilmiştir; her sürüm `git checkout <tag>` ile kontrol edilmiş ve CK Tool çalıştırılmıştır.

### E. QMOOD Tasarım Özelliklerinin Hesaplanması

CK Tool çıktılarından QMOOD tasarım özellikleri Tablo II'deki eşlemelerle hesaplanmıştır.

*TABLO II. CK TOOL METRİKLERİNDEN QMOOD TASARIM ÖZELLİĞİ EŞLEMELERİ*

| Tasarım Özelliği | Kısaltma | CK Tool Eşlemesi | Hesaplama Yöntemi |
|---|---|---|---|
| Design Size | DSC | — | Toplam sınıf sayısı |
| Abstraction | ANA | abstractMethodsQty, totalMethodsQty | μ(abstractMethods / totalMethods) |
| Encapsulation | DAM | privateFieldsQty, totalFieldsQty | μ(privateFields / totalFields) |
| Coupling | DCC | cbo | μ(CBO) |
| Cohesion | CAM | tcc (Tight Class Cohesion) | μ(TCC) |
| Composition | MOA | totalFieldsQty, staticFieldsQty | μ(totalFields − staticFields) |
| Inheritance | MFA | dit | P(DIT > 0) |
| Polymorphism | NOP | abstractMethodsQty, dit | μ(abstractMethods) + P(DIT > 0) |
| Messaging | CIS | publicMethodsQty | μ(publicMethods) |
| Complexity | NOM | wmc | μ(WMC) |

*Not: μ ortalama, P oran fonksiyonunu ifade etmektedir.*

### F. QMOOD Kalite Niteliklerinin Hesaplanması

Kalite nitelikleri, Bansiya ve Davis [2] tarafından tanımlanan doğrusal formüller kullanılarak hesaplanmıştır (Tablo III). Design Size (DSC) değeri, sınıf sayısının diğer metriklere göre büyüklük farkından kaynaklanan ölçek etkisini azaltmak amacıyla log₂ dönüşümüyle normalize edilmiştir.

*TABLO III. QMOOD KALİTE NİTELİĞİ FORMÜLLERİ [2]*

| Kalite Niteliği | Formül |
|---|---|
| Reusability | −0.25×DCC + 0.25×CAM + 0.5×CIS + 0.5×DSC* |
| Flexibility | 0.25×DAM − 0.25×DCC + 0.5×MOA + 0.5×NOP |
| Understandability | −0.33×ANA + 0.33×DAM − 0.33×DCC + 0.33×CAM − 0.33×NOP − 0.33×NOM − 0.33×DSC* |
| Functionality | 0.12×CAM + 0.22×NOP + 0.22×CIS + 0.22×DSC* + 0.22×ANA |
| Extendibility | 0.5×ANA − 0.5×DCC + 0.5×MFA + 0.5×NOP |
| Effectiveness | 0.2×ANA + 0.2×DAM + 0.2×MOA + 0.2×MFA + 0.2×NOP |

*DSC* = log₂(DSC + 1)*

### G. LLM Destekli Değerlendirme

Üç farklı LLM modeli kullanılmıştır:

1. **ChatGPT (GPT-4)** — OpenAI
2. **Gemini** — Google DeepMind
3. **Claude** — Anthropic

Her modele standart bir prompt ile aşağıdaki veriler sunulmuştur: (i) 12 sürümün ham metrik verileri, (ii) QMOOD tasarım özellikleri tablosu, (iii) QMOOD kalite nitelikleri tablosu, (iv) sürümler arası değişim (delta) verileri. Modellerden beş farklı analiz istenmiştir: genel kalite değerlendirmesi, bakım yapılabilirlik analizi, teknik borç tahmini, refactoring önerileri ve mimari kalite yorumları.

Prompt mühendisliği sürecinde iteratif bir yaklaşım izlenmiştir. İlk iterasyonda yalnızca kalite nitelikleri tablosu verildiğinde çıktılar yüzeysel kalmıştır. İkinci iterasyonda ham metrikler, delta verileri ve v2.16 sıçramasına ilişkin spesifik sorular eklenerek çıktı kalitesi artırılmıştır.

Kullanılan standart prompt yapısı Ek-A'da verilmiştir.

---

## IV. ANALİZ SÜRECİ

### A. Veri Toplama

Repo klonlanmış ve `git tag` komutuyla 80+ release tag'i listelenmiştir. Her seçilen sürüm için `git checkout <tag>` yapılmış, CK Tool `src/main/java` dizininde çalıştırılmış ve sınıf bazlı CSV çıktıları elde edilmiştir. Süreç, bir bash scripti ile otomatize edilmiştir.

### B. Ham Metrik Sonuçları

Tablo IV, 12 sürüme ait ortalama CK metrik değerlerini göstermektedir.

*TABLO IV. SÜRÜM BAZLI ORTALAMA CK METRİK DEĞERLERİ*

| Sürüm | Sınıf | μ(CBO) | μ(DIT) | μ(WMC) | μ(RFC) | μ(LCOM) | ΣLOC |
|-------|-------|--------|--------|--------|--------|---------|------|
| 1.0.0.0 | 288 | 8.58 | 1.58 | 11.69 | 16.16 | 13.89 | 16,903 |
| 1.1.0.0 | 327 | 9.24 | 1.62 | 14.75 | 19.05 | 27.19 | 23,354 |
| 1.3.0.0 | 351 | 9.61 | 1.63 | 15.48 | 19.90 | 26.50 | 26,338 |
| 2.0.0.0 | 351 | 9.62 | 1.63 | 15.49 | 19.91 | 26.50 | 26,363 |
| 2.2.0.0 | 356 | 9.67 | 1.64 | 15.42 | 19.91 | 26.54 | 26,604 |
| 2.4.0.0 | 356 | 9.67 | 1.64 | 15.43 | 19.91 | 26.54 | 26,610 |
| 2.7.0.0 | 362 | 9.75 | 1.63 | 15.32 | 19.79 | 26.46 | 26,932 |
| 2.10.0.0 | 362 | 9.75 | 1.63 | 15.33 | 19.83 | 26.49 | 26,930 |
| 2.13.0.0 | 364 | 9.78 | 1.63 | 15.30 | 19.77 | 26.43 | 27,041 |
| 2.16.0.0 | 591 | 10.48 | 1.76 | 12.02 | 15.41 | 18.14 | 34,392 |
| 2.19.0.0 | 609 | 10.47 | 1.75 | 12.16 | 15.50 | 18.57 | 35,613 |
| 3.0.0.0 | 609 | 10.47 | 1.75 | 12.16 | 15.52 | 18.57 | 35,612 |

Veriler üç belirgin dönemi ortaya koymaktadır:

**Dönem 1 — Hızlı Büyüme (v1.0 → v1.3):** Sınıf sayısı %21.9 artmış, LCOM neredeyse iki katına çıkmıştır (13.89 → 26.50). Bu durum, hızlı özellik eklemenin kohezyon kalitesini düşürdüğüne işaret etmektedir.

**Dönem 2 — Stabil Evrim (v2.0 → v2.13):** Sınıf sayısı yalnızca %3.7 artmıştır (351 → 364). Metrikler dar bir bantta kalmış olup olgun bir geliştirme dönemine işaret etmektedir.

**Dönem 3 — Yapısal Dönüşüm (v2.16 → v3.0):** Sınıf sayısı %62.4 artmıştır (364 → 591). Ortalama WMC düşmüş (15.30 → 12.02), bu da yeni eklenen sınıfların daha basit yapıda olduğunu göstermektedir.

### C. Tasarım Özellikleri

Tablo V, QMOOD tasarım özelliklerinin sürüm bazlı değerlerini sunmaktadır.

*TABLO V. QMOOD TASARIM ÖZELLİKLERİ*

| Sürüm | DSC | ANA | DAM | DCC | CAM | MOA | MFA | NOP | CIS | NOM |
|-------|-----|------|------|------|------|------|------|------|------|------|
| 1.0.0.0 | 288 | 0.0012 | 0.579 | 8.58 | −0.142 | 3.08 | 1.00 | 1.003 | 4.48 | 11.69 |
| 1.1.0.0 | 327 | 0.0048 | 0.584 | 9.24 | −0.122 | 3.22 | 1.00 | 1.021 | 5.13 | 14.75 |
| 1.3.0.0 | 351 | 0.0045 | 0.579 | 9.61 | −0.120 | 3.30 | 1.00 | 1.020 | 5.22 | 15.48 |
| 2.0.0.0 | 351 | 0.0045 | 0.580 | 9.62 | −0.120 | 3.31 | 1.00 | 1.020 | 5.23 | 15.49 |
| 2.2.0.0 | 356 | 0.0049 | 0.578 | 9.67 | −0.118 | 3.30 | 1.00 | 1.022 | 5.20 | 15.42 |
| 2.4.0.0 | 356 | 0.0049 | 0.578 | 9.67 | −0.118 | 3.30 | 1.00 | 1.022 | 5.20 | 15.43 |
| 2.7.0.0 | 362 | 0.0048 | 0.578 | 9.75 | −0.116 | 3.34 | 1.00 | 1.022 | 5.17 | 15.32 |
| 2.10.0.0 | 362 | 0.0048 | 0.578 | 9.75 | −0.116 | 3.34 | 1.00 | 1.022 | 5.17 | 15.33 |
| 2.13.0.0 | 364 | 0.0048 | 0.578 | 9.78 | −0.115 | 3.33 | 1.00 | 1.022 | 5.16 | 15.30 |
| 2.16.0.0 | 591 | 0.0116 | 0.451 | 10.48 | −0.142 | 2.66 | 1.00 | 1.142 | 4.22 | 12.02 |
| 2.19.0.0 | 609 | 0.0112 | 0.449 | 10.47 | −0.138 | 2.64 | 1.00 | 1.140 | 4.24 | 12.16 |
| 3.0.0.0 | 609 | 0.0112 | 0.449 | 10.47 | −0.138 | 2.64 | 1.00 | 1.140 | 4.24 | 12.16 |

Dikkat çeken gözlemler:

- **Encapsulation (DAM):** v2.13'te 0.578 iken v2.16'da 0.451'e düşmüştür (%22.0 azalma). Yeni eklenen sınıflarda kapsülleme ilkelerine daha az uyulduğu görülmektedir.
- **Coupling (DCC):** 8.58'den 10.47'ye monoton artış göstermiştir (%22.1 artış). Bu, mimari bağımlılıkların yoğunlaştığını gösterir.
- **Cohesion (CAM):** Tüm sürümlerde negatif değer almıştır, bu da TCC'nin genel olarak düşük olduğunu ve metotlar arası bağımsızlığa işaret etmektedir.
- **Abstraction (ANA):** v2.16'da artış göstermiştir (0.0048 → 0.0116), yeni eklenen kodda soyut yapıların daha yoğun kullanıldığına işaret eder.

---

## V. SONUÇLAR

### A. Kalite Nitelikleri Tablosu

Tablo VI, 12 sürümün QMOOD kalite nitelik değerlerini sunmaktadır.

*TABLO VI. QMOOD KALİTE NİTELİKLERİ*

| Sürüm | Reusability | Flexibility | Understandability | Functionality | Extendibility | Effectiveness |
|-------|------------|-------------|-------------------|---------------|---------------|---------------|
| 1.0.0.0 | 4.147 | 0.040 | −9.572 | 2.988 | −3.286 | 1.132 |
| 1.1.0.0 | 4.401 | −0.041 | −10.860 | 3.177 | −3.606 | 1.167 |
| 1.3.0.0 | 4.409 | −0.099 | −11.256 | 3.221 | −3.791 | 1.180 |
| 2.0.0.0 | 4.406 | −0.097 | −11.265 | 3.222 | −3.800 | 1.182 |
| 2.2.0.0 | 4.393 | −0.114 | −11.267 | 3.222 | −3.823 | 1.181 |
| 2.4.0.0 | 4.393 | −0.114 | −11.270 | 3.222 | −3.823 | 1.181 |
| 2.7.0.0 | 4.369 | −0.112 | −11.267 | 3.220 | −3.864 | 1.190 |
| 2.10.0.0 | 4.369 | −0.111 | −11.268 | 3.220 | −3.862 | 1.190 |
| 2.13.0.0 | 4.361 | −0.125 | −11.272 | 3.220 | −3.878 | 1.187 |
| 2.16.0.0 | 4.060 | −0.605 | −10.744 | 3.192 | −4.163 | 1.054 |
| 2.19.0.0 | 4.093 | −0.617 | −10.797 | 3.204 | −4.159 | 1.047 |
| 3.0.0.0 | 4.093 | −0.617 | −10.798 | 3.204 | −4.159 | 1.047 |

### B. Kalite Niteliklerinin Evrimi

Şekil 2 (`results/quality_attributes_evolution.png`), altı kalite niteliğinin sürümler boyunca evrimini göstermektedir. Bulgular aşağıda detaylandırılmıştır.

**1) Reusability:** v1.0'dan v1.3'e artış (4.147 → 4.409), ardından v2.x serisinde kademeli düşüş (4.409 → 4.361), v2.16'da belirgin kötüleşme (4.361 → 4.060). CIS ve DSC bileşenlerindeki artış, DCC'deki artışı kompanse edememiştir.

**2) Flexibility:** v1.0'da pozitif olan tek kalite niteliğidir (0.040). v1.1'den itibaren negatife geçmiş, v2.16'da sert bir düşüş yaşamıştır (−0.125 → −0.605). Bu düşüşün temel nedeni coupling artışı ve encapsulation kaybıdır.

**3) Understandability:** Tüm sürümlerde negatif değer almıştır; bu, büyük ve karmaşık bir sisteme beklenen bir durumdur. İlginç biçimde v2.16'da kısmi iyileşme gözlenmiştir (−11.272 → −10.744). Bunun nedeni, yeni eklenen basit sınıfların ortalama NOM ve DCC değerlerini düşürmesidir.

**4) Functionality:** En stabil kalite niteliğidir; 2.988–3.222 aralığında dar bir bantta kalmıştır. Yeni özellik eklenmesi fonksiyonalite skorunu korumuştur.

**5) Extendibility:** Sürekli kötüleşen bir trend göstermiştir (−3.286 → −4.159, %26.6 düşüş). DCC'deki monoton artış, genişletilebilirliği doğrudan olumsuz etkileyen birincil faktördür. Bu, en kritik kalite sorunu olarak tespit edilmiştir.

**6) Effectiveness:** Nispeten stabil kalmıştır (1.047–1.190 aralığında). v2.16'da DAM düşüşünün etkisiyle azalma gözlenmiştir (1.187 → 1.054).

### C. Mimari Bozulma Analizi

Coupling-Cohesion ilişkisi (Şekil 5, `results/coupling_vs_cohesion.png`), klasik mimari bozulma kalıplarını ortaya koymaktadır:

1. **Bağımlılık yoğunlaşması:** CBO monoton artış göstermiş (8.58 → 10.47) ancak CAM stabil kalmıştır. Bu, sınıflar arası bağımlılıkların yönetilmeden büyüdüğünü gösterir.

2. **v2.16 kırılma noktası:** 227 yeni sınıf eklenmesi, DAM'ı %22.0 düşürmüş ve DCC'yi artırmıştır. Bu geçiş, coupling-cohesion grafiğinde belirgin bir kayma olarak görülmektedir.

3. **v2.19 → v3.0 stabilizasyonu:** Son iki sürümde metrikler neredeyse aynı kalmıştır, bu da sistemin olgunlaştığını ve büyük yapısal değişiklikler yapılmadığını gösterir.

### D. Teknik Borç Göstergeleri

Veriler, aşağıdaki teknik borç göstergelerini ortaya koymaktadır:

- **Yüksek LCOM:** Ortalama LCOM değerleri 18–27 aralığındadır. Bu, sınıfların çoğunluğunda metotlar arası uyumun düşük olduğunu ve Single Responsibility Principle (SRP) ihlallerinin yaygın olabileceğini gösterir.
- **Aşırı bağımlı sınıflar:** Maksimum CBO değeri 217'ye ulaşmıştır, bu God Class anti-pattern'ine işaret eder.
- **Yüksek karmaşıklık:** Maksimum WMC değeri 318 olup, belirli sınıfların refactoring gerektirdiğini göstermektedir.
- **Kontrollü inheritance:** Maksimum DIT tüm sürümlerde 7'de sabit kalmıştır; bu, kalıtım hiyerarşisinin kontrol altında tutulduğunu gösterir.

### E. Sürümler Arası Delta Analizi

Tablo VII, en belirgin kalite değişimlerini özetlemektedir.

*TABLO VII. EN BELİRGİN KALİTE DEĞİŞİMLERİ (DELTA)*

| Sürüm Geçişi | En Çok Etkilenen Nitelik | Δ Değeri | Temel Neden |
|--------|-----------------|------|-------|
| v1.0 → v1.1 | Understandability | −1.288 | Hızlı büyüme, LCOM iki katı |
| v1.0 → v1.1 | Reusability | +0.254 | CIS ve DSC artışı |
| v1.1 → v1.3 | Flexibility | −0.058 | Coupling artışı |
| v2.13 → v2.16 | Flexibility | −0.479 | 227 yeni sınıf, DAM düşüşü |
| v2.13 → v2.16 | Extendibility | −0.285 | DCC sıçraması |
| v2.13 → v2.16 | Effectiveness | −0.133 | Encapsulation kaybı |
| v2.13 → v2.16 | Understandability | +0.529 | Yeni sınıfların düşük NOM'u |

---

## VI. TARTIŞMA

### A. LLM Değerlendirme Sonuçları

Üç farklı LLM modeline aynı standart prompt ve metrik verileri sunulmuş, her birinden 5 başlıkta (genel kalite, bakım yapılabilirlik, teknik borç, refactoring, mimari kalite) detaylı değerlendirme istenmiştir. LLM çıktılarının tam metinleri `chatgpt_response.md`, `gemini_response.md` ve `claude_response.md` dosyalarında yer almaktadır. Bu bölümde her modelin öne çıkan tespitleri özetlenmekte ve karşılaştırılmaktadır.

#### 1) ChatGPT (GPT-4)

ChatGPT, metrik verilerini başarılı biçimde yorumlamış ve dengeli bir perspektif sunmuştur. Model, projenin evrimini iki dönem olarak tanımlamıştır: mevcut yapı üzerine organik büyüme (v1.0–v2.13) ve kapsamlı yeniden yapılanma (v2.16+).

- *Genel kalite:* Projenin "olgun bir açık kaynak sistem davranışı" gösterdiğini belirtmiş; v2.16 sonrasında metriklerin yeniden dengelendiğini ve v3.0'da kararlı bir duruma ulaşıldığını vurgulamıştır.
- *Bakım yapılabilirlik:* LCOM'un v1.0→v1.1 geçişinde iki katına çıkmasını (13.89→27.19) "ilk büyük darbe" olarak nitelendirmiştir. v2.16'da WMC'nin %21, RFC'nin %22 düşüşünü "belirgin bir refactoring veya mimari yeniden organizasyon etkisi" şeklinde yorumlamıştır.
- *Teknik borç:* v2.16'nın teknik borcun tamamen azaltıldığı değil, "teknik borcun türünün değiştiği" bir sürüm olduğunu tespit etmiştir. Monolitik karmaşıklık borcu azalırken entegrasyon ve bağımlılık borcunun arttığını belirtmiştir.
- *Refactoring:* Max CBO 214 olan sınıfların Facade, Mediator veya Event-Driven mekanizmalarla ayrıştırılmasını; CAM'ın negatif olmasının Domain-Driven Design (DDD) prensiplerine göre yeniden yapılandırma gerektirdiğini; servis sınırlarının netleştirilerek cyclic dependency'lerin azaltılmasını önermiştir.
- *Mimari yorum:* "Sistem daha modüler hale gelirken modüller arası iletişim yoğunlaşmıştır" değerlendirmesiyle "iyi ayrıştırılmış fakat sıkı entegre edilmiş" bir yapı tanımlamıştır. Mevcut en büyük mimari riskin "düşük cohesion değil, yüksek coupling" olduğunu vurgulamıştır.

#### 2) Google Gemini

Gemini, en kapsamlı ve en eleştirel analizi sunmuştur. Özellikle mimari anti-pattern tespitleri ve teknik borç yorumlarında güçlü ifadeler kullanmıştır.

- *Genel kalite:* v2.16'daki değişikliğin "kod seviyesinde bazı iyileştirmeler getirse de nesne yönelimli tasarımın esneklik sağlayan soyutlama prensiplerinden uzaklaşıldığını ve projenin 'katılaşmaya' (rigid) başladığını" belirtmiştir. v3.0 geçişinin "mimari bir yenilenmeden ziyade pazarlama veya API uyumluluğu odaklı" olduğunu öne sürmüştür.
- *Bakım yapılabilirlik:* Max_WMC'nin 318'den 190'a düşmesini "God Class anti-örüntüsünün parçalandığı"nın kanıtı olarak görmüştür. Ancak CBO artışıyla birlikte sınıfların "birbirine sıkı sıkıya bağlandığını (Spaghetti Code)" ve sistem çapındaki bakım zorluğunun arttığını belirtmiştir.
- *Teknik borç:* En keskin tespitleri bu başlıkta yapmıştır. Max_CBO=214'ü "nesne yönelimli tasarım kurallarının ihlal edildiği devasa bir tasarım borcu" olarak tanımlamıştır. v2.19→v3.0 geçişinde hiçbir metriğin iyileşmemesini "ekibin teknik borçlara dokunmaktan korktuğu (fragile system)" şeklinde yorumlamış, bu mimari borcun gelecekte özellik ekleme maliyetini "eksponansiyel olarak artıracağını" öngörmüştür.
- *Refactoring:* Üç öncelikli alan belirlemiştir: (i) Max_CBO=214 sınıfların Extract Class ve Interface Segregation ile ayrıştırılması, (ii) DAM değerinin v2.16 öncesi seviyelere (0.570+) çekilmesi için alanların private yapılması, (iii) Dependency Inversion Principle ile somut bağımlılıklar arasına interface katmanları eklenerek Open/Closed Principle'ın sağlanması.
- *Mimari yorum:* En çarpıcı tespiti mimari bölümde yapmıştır: projenin "'büyük çamur topu' (Big Ball of Mud) evresinden, 'dağıtılmış ama birbirine dolanmış' (Distributed Spaghetti) bir evreye" geçtiğini belirtmiştir. CAM metriğinin sürekli negatif seyretmesini, projenin "nesne yönelimli olmaktan ziyade prosedürel bir anemik domain modeline (Anemic Domain Model) sahip olduğunun" göstergesi olarak yorumlamıştır. Hexagonal veya Clean Architecture yaklaşımlarının projeye entegre edilmesini önermiştir.

#### 3) Claude (Anthropic)

Claude, en sistematik ve yapısal analizi sunmuştur. Özellikle metrik değişimlerinin nedensellik analizinde ve nicel yorumlamalarda ayrıntılı bir yaklaşım sergilemiştir.

- *Genel kalite:* Projenin "iki belirgin evreye ayrılan bir gelişim" sergilediğini tespit etmiştir: istikrarlı organik büyüme (v1.0–v2.13) ve yapısal kırılma (v2.16+). Understandability'nin v2.16'da paradoksal iyileşmesini (+0.529), yeni eklenen sınıfların "daha düşük WMC ve LCOM değerlerine sahip olmasından" kaynaklandığını ve "yeni kodun daha iyi mühendislik pratikleriyle yazıldığını düşündürdüğünü" belirtmiştir.
- *Bakım yapılabilirlik:* Max CBO'nun 217'ye ulaşmasını "217 farklı sınıfla doğrudan ilişki" olarak somutlaştırmış, bu düzeydeki bağımlılığın "zincirleme etkiler yaratma potansiyeli" taşıdığını belirtmiştir. DIT'in 1.63'ten 1.76'ya çıkmasını ve MFA'nın 1.00'dan 1.14'e yükselmesini, "kalıtım hiyerarşisinin derinleştiği ve hata izlemeyi zorlaştırabileceği" şeklinde yorumlamıştır.
- *Teknik borç:* v2.16'da LCOM düşüşünün "biriken borcun ödenmesinden çok, yeni eklenen düşük-LCOM sınıfların ortalamayı aşağı çekmesinden" kaynaklandığını, "eski sınıflardaki kohezyon sorununun büyük olasılıkla yerinde durduğunu" tespit etmiştir. Toplam teknik borcu "orta-yüksek" seviyede değerlendirmiş ve en yüksek CBO/WMC sınıflarının refactoring'inin "birkaç sprint'lik yoğun çalışma gerektireceğini" öngörmüştür.
- *Refactoring:* Üç öncelik sırasıyla sunmuştur: (i) God Class Decomposition — Max CBO=217 sınıfların SRP'ye göre alt modüllere ayrılması, Facade/Mediator pattern'leri; (ii) Kohezyon iyileştirmesi — v1.1'den beri LCOM'u yüksek eski sınıflara Extract Class uygulanması; (iii) Bağımlılık yönetimi — Dependency Inversion ile arayüzlere bağımlılık oluşturulması ve "kalıtım yerine composition" tercih edilmesi.
- *Mimari yorum:* İlk dönemde "sınıf başına LOC artışının mevcut sınıfların şiştiğini" gösterdiğini, v2.16'da "yeni modülün mevcut sisteme yoğun bağımlılıklarla entegre edildiğini ve entegrasyon noktalarında mimari kalitenin düştüğünü" belirtmiştir. v2.19–v3.0 stabilitesini "projenin mimari olarak 'donma' noktasına geldiği ve mevcut yapının sınırlarına ulaştığı" şeklinde yorumlamıştır.

### B. LLM Karşılaştırması

Tablo VIII, üç modelin karşılaştırmalı değerlendirmesini sunmaktadır.

*TABLO VIII. LLM MODELLERİNİN KARŞILAŞTIRMASI*

| Değerlendirme Alanı | ChatGPT (GPT-4) | Gemini | Claude |
|---------------------|---------|--------|--------|
| Genel yaklaşım | Dengeli, pratik odaklı | Eleştirel, risk ve anti-pattern odaklı | Sistematik, yapısal ve nicel odaklı |
| v2.16 yorumu | "Teknik borcun türü değişmiş" | "Katılaşma (rigidity) başlamış" | "İki fazlı evrim, paradoksal iyileşme" |
| Teknik borç tahmini | Orta (tür değişimi vurgusu) | Yüksek (eksponansiyel maliyet uyarısı) | Orta-Yüksek (eski sınıflar odaklı) |
| Refactoring önerileri | DDD, Facade, Event-Driven | Extract Class, Interface Segregation, Hexagonal Arch. | God Class Decomposition, SRP, Composition over Inheritance |
| v3.0 yorumu | "Kararlı durum" | "Pazarlama odaklı, inovasyon kaybı" | "Mimari donma noktası" |
| Mimari tanı | "İyi ayrıştırılmış ama sıkı entegre" | "Big Ball of Mud → Distributed Spaghetti" | "Organik büyüme → yapısal dönüşüm" |
| Anti-pattern tespiti | God Class, merkezi koordinatör | God Class, Anemic Domain Model, Spaghetti Code | God Class, hub class |
| Kullanılan terminoloji | Yazılım mühendisliği | Mimari pattern + metafor ağırlıklı | Metrik-temelli, akademik |

**Ortak bulgular — üç modelin hemfikir olduğu tespitler:**

1. **Coupling en kritik risk faktörüdür.** Üç model de CBO'nun monoton artışını ve Max CBO=214/217 değerini en acil yapısal sorun olarak tanımlamıştır.
2. **v2.16 bir kırılma noktasıdır.** Tüm modeller bu sürümü projenin en kritik yapısal değişimi olarak nitelendirmiştir.
3. **LCOM artışı SRP ihlallerine işaret eder.** Özellikle v1.0→v1.1 geçişindeki iki katlık artış, üç modelin de vurguladığı bir noktadır.
4. **v2.16'da eklenen sınıflar daha basittir.** WMC ve LCOM düşüşleri, üç model tarafından da yeni kodun daha iyi mühendislik pratikleriyle yazıldığı şeklinde yorumlanmıştır.
5. **v3.0 mimari olarak stabildir.** Metrik değişiminin neredeyse sıfır olması, üç model tarafından da tespit edilmiştir.
6. **Refactoring'de God Class ayrıştırması önceliklidir.** Üç model de Max CBO değeri yüksek sınıfların parçalanmasını ilk öncelik olarak belirlemiştir.

**Farklılıklar ve çelişkiler:**

- **Ton ve yaklaşım:** ChatGPT en dengeli ve iyimser yaklaşımı sergilemiş, v2.16'yı "borcun türünün değişmesi" olarak değerlendirmiştir. Gemini en eleştirel tonu kullanmış, projenin "katılaştığını" ve "inovasyon yeteneğini kaybettiğini" vurgulamıştır. Claude akademik bir ton benimseyerek paradoksal ilişkileri (v2.16'da Understandability iyileşmesi gibi) ayrıntılı biçimde açıklamıştır.
- **v3.0 yorumu:** Bu, modeller arasındaki en belirgin ayrışma noktasıdır. ChatGPT "kararlı durum" derken, Gemini "pazarlama odaklı, mimari yenilenme yok" şeklinde eleştirmiş, Claude ise "donma noktası — mevcut yapının sınırlarına ulaşılmış" değerlendirmesinde bulunmuştur.
- **Mimari tanı dili:** Gemini'nin "Big Ball of Mud → Distributed Spaghetti" ve "Anemic Domain Model" gibi güçlü metaforları dikkat çekmektedir. ChatGPT daha ölçülü ifadeler kullanırken, Claude metrik değerlerine dayalı nicel argümanlar tercih etmiştir.
- **Teknik borç şiddeti:** ChatGPT "orta", Claude "orta-yüksek", Gemini ise en yüksek tehdit algısıyla "eksponansiyel maliyet artışı" öngörmüştür.
- **Refactoring derinliği:** Gemini, Clean Architecture ve Hexagonal Architecture gibi mimari düzeyde öneriler sunarken, ChatGPT DDD ve Event-Driven yaklaşımları önermiş, Claude ise metrik bazlı spesifik öncelikler belirlemiştir.

### C. Bulguların Değerlendirilmesi

Çalışmanın bulguları, Lehman'ın yazılım evrimi yasalarıyla [1] uyumludur. "Artan karmaşıklık yasası"na uygun olarak, coupling sürekli artmış ve aktif müdahale olmadan yapısal bozulma gözlenmiştir. v2.16'daki büyük ölçekli yapısal değişiklik, "sürekli değişim yasası"nın bir yansımasıdır; ancak bu değişiklik, bazı kalite niteliklerinde bozulmaya yol açmıştır. ChatGPT'nin "teknik borcun türünün değiştiği" tespiti bu çift yönlü etkiyi özetleyen en iyi ifadedir.

QMOOD sonuçları, Al Dallal [8] ve Padhy vd. [9] tarafından raporlanan eğilimlerle tutarlıdır: coupling artışı genişletilebilirliği olumsuz etkilerken, encapsulation kaybı etkinliği düşürmektedir. LLM'lerin bu ilişkileri doğru tespit etmesi, modellerin metrik tabanlı neden-sonuç analizinde güvenilir olduğunu göstermektedir.

### D. Eleştirel Değerlendirme ve Sınırlılıklar

LLM çıktıları genel olarak metrik bulgularıyla tutarlıdır ve birbirini tamamlayan perspektifler sunmuştur. Ancak aşağıdaki sınırlılıklar tespit edilmiştir:

1. **Bağlam eksikliği:** LLM'ler, projenin iş mantığını ve kullanım senaryolarını bilmeden yorum yapmıştır. Gemini'nin "Anemic Domain Model" tespiti gibi güçlü iddialar, kaynak kod incelemesi olmadan doğrulanamamaktadır. Refactoring önerileri bu nedenle genel tasarım kalıplarıyla sınırlı kalmıştır.
2. **Teknik borç şiddetinde tutarsızlık:** Üç model farklı şiddet dereceleri belirlemiştir (ChatGPT: orta, Claude: orta-yüksek, Gemini: yüksek). Bu, LLM'lerin mutlak değerlendirme yerine göreceli trend analizinde daha güvenilir olduğunu göstermektedir.
3. **Aşırı genelleme eğilimi:** Üç model de benzer kalıp önerilerini sunmuştur (God Class bölme, Facade/Mediator Pattern, Dependency Inversion). Bu, LLM'lerin proje bağlamından bağımsız "standart reçeteler" üretme eğiliminde olduğunu göstermektedir. Gemini'nin Clean Architecture önerisi en projeye özgü yaklaşım olarak öne çıkmaktadır.
4. **Spekülatif yorumlar:** Gemini'nin v3.0'ı "pazarlama odaklı" değerlendirmesi ve Claude'un "ekibin bilinçli tasarım kararı" tespiti, veri tarafından doğrudan desteklenmeyen spekülatif yorumlardır. LLM çıktıları eleştirel okunmalıdır.
5. **Metrik sınırlılıkları:** CK Tool'un sağladığı metriklerden bazı QMOOD tasarım özelliklerinin (özellikle CAM ve MOA) doğrudan hesaplanamaması, proxy metriklerin kullanılmasını gerektirmiştir.
6. **Normalize etme etkisi:** DSC'nin log₂ dönüşümü ile normalize edilmesi, mutlak skor değerlerini etkilemektedir. Ancak sürümler arası karşılaştırmalarda trend bilgisi korunmaktadır.

### E. Prompt Mühendisliği Süreci

İlk prompt denemesinde modellere yalnızca QMOOD kalite nitelikleri tablosu verilmiş, çıktılar yüzeysel kalmıştır. İkinci iterasyonda promptun iyileştirilmesiyle çıktı kalitesi önemli ölçüde artmıştır:

- Ham metrikler (CBO, WMC, LCOM, RFC vb.) ve maksimum değerler (Max_CBO, Max_WMC) eklenmiştir.
- QMOOD tasarım özellikleri tablosu dahil edilmiştir.
- Sürümler arası delta verileri paylaşılmıştır.
- Spesifik yönlendirme yapılmıştır: "v2.16.0.0'daki büyük sıçramayı değerlendirin."
- Proje bağlamı açıklanmıştır: "Java dilinde yazılmış açık kaynak anomali tespit eklentisi."

Bu iyileştirme, LLM'lerin yalnızca trendleri değil, nedensellikleri de yorumlayabilmesini sağlamıştır. Özellikle ham metriklerdeki Max değerlerinin eklenmesi, modellerin God Class tespiti yapabilmesi için kritik öneme sahiptir.

### F. Geçerlilik Tehditleri

- **İç geçerlilik:** CK Tool dışında ikinci bir araç (ör. Designite, SonarQube) ile çapraz doğrulama yapılmamıştır.
- **Dış geçerlilik:** Bulgular tek bir projeye dayanmakta olup genellenebilirlik sınırlıdır.
- **Yapı geçerliliği:** QMOOD'un bazı tasarım özelliklerinin (CAM, MOA) CK Tool çıktılarından proxy metriklerle hesaplanması, yapı geçerliliğini etkileyebilir.
- **LLM tekrarlanabilirliği:** LLM'lerin aynı prompt ile farklı zamanlarda farklı yanıtlar üretebileceği göz önünde bulundurulmalıdır.

---

## VII. SONUÇ VE GELECEK ÇALIŞMALAR

Bu çalışmada, OpenSearch Anomaly Detection projesinin 12 sürümü QMOOD modeli kullanılarak analiz edilmiş ve elde edilen veriler üç farklı LLM ile değerlendirilmiştir. Temel bulgular şu şekilde özetlenebilir:

1. **Yazılım büyümesi kaliteyi etkiler.** Proje, 288 sınıftan 609 sınıfa (%111 artış) büyümüş; bu süreçte reusability %1.3, flexibility %1644, extendibility %26.6 düşüş göstermiştir.

2. **Coupling en kritik kalite sorundur.** CBO'nun monoton artışı (8.58 → 10.47, %22.1), extendibility, flexibility ve reusability niteliklerini doğrudan olumsuz etkilemektedir.

3. **v2.16 yapısal bir kırılma noktasıdır.** 227 yeni sınıf eklenmiş, WMC düşerken DAM %22.0 azalmıştır. Bu durum, büyük ölçekli yapısal değişikliklerin çift yönlü kalite etkisini göstermektedir.

4. **LLM'ler metrik tabanlı kalite değerlendirmesinde kullanışlıdır.** Üç model de sürüm trendlerini doğru yorumlamış ve anlamlı öneriler sunmuştur. Ancak projeye özgü bağlam olmadan önerilerin genelliği sınırlayıcıdır.

5. **Prompt mühendisliği LLM çıktı kalitesini belirler.** Ham metriklerin, delta verilerinin ve spesifik soruların eklenmesi, çıktı derinliğini önemli ölçüde artırmıştır.

Gelecek çalışmalar şu yönlerde genişletilebilir: (i) v3.1–v3.7 sürümlerinin dahil edilmesiyle güncel trendlerin izlenmesi, (ii) en yüksek CBO ve LCOM değerlerine sahip sınıfların tekil analizi, (iii) Designite veya SonarQube ile çapraz doğrulama, (iv) LLM'lere kaynak kod verilerek spesifik refactoring önerilerinin alınması, (v) başka bir açık kaynak projeyle karşılaştırmalı analiz yapılması, (vi) SQALE modeli ile teknik borcun nicel tahmin edilmesi.

---

## KAYNAKLAR

[1] M. M. Lehman, "Laws of software evolution revisited," in *Proc. 5th European Workshop on Software Process Technology (EWSPT)*, 1996, pp. 108–124.

[2] J. Bansiya and C. G. Davis, "A hierarchical model for object-oriented design quality assessment," *IEEE Transactions on Software Engineering*, vol. 28, no. 1, pp. 4–17, Jan. 2002.

[3] A. Fan, B. Gokkaya, M. Harman, M. Lyubarskiy, S. Sengupta, S. Yoo, and J. M. Zhang, "Large language models for software engineering: Survey and open problems," *arXiv preprint arXiv:2310.03533*, 2023.

[4] ISO/IEC 9126-1:2001, "Software engineering — Product quality — Part 1: Quality model," International Organization for Standardization, 2001.

[5] S. R. Chidamber and C. F. Kemerer, "A metrics suite for object-oriented design," *IEEE Transactions on Software Engineering*, vol. 20, no. 6, pp. 476–493, Jun. 1994.

[6] W. Cunningham, "The WyCash portfolio management system," in *Proc. OOPSLA '92 Experience Report*, 1992.

[7] X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo, J. Grundy, and H. Wang, "Large language models for software engineering: A systematic literature review," *ACM Transactions on Software Engineering and Methodology*, vol. 33, no. 8, pp. 1–79, 2024.

[8] J. Al Dallal, "Object-oriented class maintainability prediction using internal quality attributes," *Information and Software Technology*, vol. 55, no. 11, pp. 2028–2048, 2013.

[9] N. Padhy, S. Satapathy, and R. P. Singh, "State-of-the-art object-oriented metrics and its reusability: A decade review," in *Smart Computing and Informatics*, Springer, 2018, pp. 431–441.

[10] G. Singh and R. Malhotra, "An empirical investigation of the effect of object-oriented design metrics on quality," *Software Quality Journal*, vol. 30, no. 4, pp. 983–1012, 2022.

[11] M. Aniche, "CK: Calculate Chidamber and Kemerer and many other metrics for Java projects," GitHub, 2015. [Online]. Available: https://github.com/mauricioaniche/ck

[12] R. C. Martin, *Agile Software Development, Principles, Patterns, and Practices*. Upper Saddle River, NJ: Prentice Hall, 2003.

[13] M. Fowler, *Refactoring: Improving the Design of Existing Code*, 2nd ed. Boston, MA: Addison-Wesley, 2018.

[14] OpenSearch Project, "anomaly-detection," GitHub, 2024. [Online]. Available: https://github.com/opensearch-project/anomaly-detection

---

## EK-A: KULLANILAN LLM PROMPTU

Üç model için aynı standart prompt yapısı kullanılmıştır:

```
Aşağıda OpenSearch Anomaly Detection projesinin 12 farklı sürümüne ait
QMOOD analiz sonuçları verilmektedir. Proje, Java dilinde yazılmış
açık kaynak bir anomali tespit eklentisidir. Metrikler CK Tool ile
çıkarılmış, QMOOD formülleri Bansiya & Davis (2002) referansıyla
uygulanmıştır.

Bu verileri analiz ederek:
1. Genel kalite değerlendirmesi yapınız.
2. Bakım yapılabilirlik (maintainability) analizi yapınız.
3. Teknik borç tahmini yapınız.
4. Refactoring önerileri sununuz.
5. Mimari kalite yorumları yapınız.

Özellikle sürüm 2.16.0.0'daki büyük sıçramayı ve bunun kaliteye
etkisini değerlendiriniz. Coupling ve cohesion trendlerini
yorumlayınız.

[HAM METRİKLER TABLOSU — Tablo IV]
[TASARIM ÖZELLİKLERİ TABLOSU — Tablo V]
[KALİTE NİTELİKLERİ TABLOSU — Tablo VI]
[DELTA TABLOSU — Tablo VII]
```

## EK-B: KULLANILAN ARAÇLAR

| Araç | Sürüm | Amaç |
|------|-------|------|
| CK Tool | 0.7.0 | Java metrik çıkarımı |
| Python | 3.12.1 | QMOOD hesaplama, analiz |
| Pandas | — | Veri işleme |
| NumPy | — | Sayısal hesaplamalar |
| Matplotlib | — | Görselleştirme |
| Java | 22.0.1 | CK Tool çalıştırma |

## EK-C: PROJE DOSYA YAPISI

```
software_design_project/
├── extract_metrics.sh          # CK Tool otomasyon scripti
├── qmood_analysis.py           # QMOOD hesaplama ve görselleştirme
├── rapor.md                    # Bu teknik rapor
├── anomaly-detection/          # Klonlanmış kaynak kod deposu
├── metrics/                    # Sürüm bazlı CK Tool çıktıları
│   ├── 1.0.0.0/class.csv
│   ├── 1.1.0.0/class.csv
│   ├── ...
│   └── 3.0.0.0/class.csv
└── results/                    # Hesaplanmış tablolar ve grafikler
    ├── quality_attributes.csv
    ├── design_properties.csv
    ├── raw_metrics.csv
    ├── quality_delta.csv
    ├── analysis_data.json
    ├── quality_attributes_evolution.png   (Şekil 2)
    ├── design_properties_evolution.png    (Şekil 3)
    ├── raw_metrics_evolution.png          (Şekil 4)
    ├── coupling_vs_cohesion.png           (Şekil 5)
    ├── quality_delta_heatmap.png          (Şekil 6)
    └── quality_radar_comparison.png       (Şekil 7)
```
