# OpenSearch Anomaly Detection Projesi QMOOD ve CK Metrikleri Kalite Analiz Raporu

## 1. Giriş ve Metodoloji
Bu raporda, Java dilinde geliştirilmiş açık kaynaklı bir anomali tespit eklentisi olan **OpenSearch Anomaly Detection** projesinin 12 farklı sürümüne ait kaynak kod kalitesi değerlendirilmiştir. Analiz kapsamında, CK Tool kullanılarak elde edilen yazılım metrikleri ve Bansiya & Davis (2002) tarafından önerilen **QMOOD (Quality Model for Object-Oriented Design)** modeli referans alınmıştır. 

Projenin evrimi; sınıf sayısı, kod satırı (LOC), nesne yönelimli tasarım özellikleri (DSC, ANA, DAM, DCC, CAM, MOA, MFA, NOP, CIS, NOM) ve üst düzey kalite nitelikleri (Yeniden Kullanılabilirlik, Esneklik, Anlaşılabilirlik, İşlevsellik, Genişletilebilirlik, Etkililik) üzerinden incelenmiştir. Özellikle **v2.16.0.0** sürümünde gözlemlenen radikal yapısal değişimler ve bunun sistem mimarisine etkileri detaylandırılmıştır.

---

## 2. Temel Metrikler ve Tasarım Özellikleri Veri Seti

### 2.1. CK Yazılım Metrikleri Trendi
| Sürüm | Sınıf | Ort.CBO | Ort.DIT | Ort.WMC | Ort.RFC | Ort.LCOM | ToplamLOC | Max_CBO | Max_WMC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1.0.0.0** | 288 | 8.58 | 1.58 | 11.69 | 16.16 | 13.89 | 16903 | 118 | 103 |
| **1.1.0.0** | 327 | 9.24 | 1.62 | 14.75 | 19.05 | 27.19 | 23354 | 133 | 308 |
| **1.3.0.0** | 351 | 9.61 | 1.63 | 15.48 | 19.90 | 26.50 | 26338 | 136 | 314 |
| **2.0.0.0** | 351 | 9.62 | 1.63 | 15.49 | 19.91 | 26.50 | 26363 | 136 | 314 |
| **2.2.0.0** | 356 | 9.67 | 1.64 | 15.42 | 19.91 | 26.54 | 26604 | 138 | 314 |
| **2.4.0.0** | 356 | 9.67 | 1.64 | 15.43 | 19.91 | 26.54 | 26610 | 138 | 314 |
| **2.7.0.0** | 362 | 9.75 | 1.63 | 15.32 | 19.79 | 26.46 | 26932 | 140 | 318 |
| **2.10.0.0**| 362 | 9.75 | 1.63 | 15.33 | 19.83 | 26.49 | 26930 | 140 | 318 |
| **2.13.0.0**| 364 | 9.78 | 1.63 | 15.30 | 19.77 | 26.43 | 27041 | 140 | 318 |
| **2.16.0.0**| 591 | 10.48| 1.76 | 12.02 | 15.41 | 18.14 | 34392 | 214 | 190 |
| **2.19.0.0**| 609 | 10.47| 1.75 | 12.16 | 15.50 | 18.57 | 35613 | 217 | 196 |
| **3.0.0.0** | 609 | 10.47| 1.75 | 12.16 | 15.52 | 18.57 | 35612 | 217 | 196 |

### 2.2. QMOOD Kalite Nitelikleri Trendi
| Sürüm | Reusability | Flexibility | Understandability | Functionality | Extendibility | Effectiveness |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1.0.0.0** | 4.147 | 0.040 | -9.572 | 2.988 | -3.286 | 1.132 |
| **1.1.0.0** | 4.401 | -0.041 | -10.860 | 3.177 | -3.606 | 1.167 |
| **1.3.0.0** | 4.409 | -0.099 | -11.256 | 3.221 | -3.791 | 1.180 |
| **2.0.0.0** | 4.406 | -0.097 | -11.265 | 3.222 | -3.800 | 1.182 |
| **2.2.0.0** | 4.393 | -0.114 | -11.267 | 3.222 | -3.823 | 1.181 |
| **2.4.0.0** | 4.393 | -0.114 | -11.270 | 3.222 | -3.823 | 1.181 |
| **2.7.0.0** | 4.369 | -0.112 | -11.267 | 3.220 | -3.864 | 1.190 |
| **2.10.0.0**| 4.369 | -0.111 | -11.268 | 3.220 | -3.862 | 1.190 |
| **2.13.0.0**| 4.361 | -0.125 | -11.272 | 3.220 | -3.878 | 1.187 |
| **2.16.0.0**| 4.060 | -0.605 | -10.744 | 3.192 | -4.163 | 1.054 |
| **2.19.0.0**| 4.093 | -0.617 | -10.797 | 3.204 | -4.159 | 1.047 |
| **3.0.0.0** | 4.093 | -0.617 | -10.798 | 3.204 | -4.159 | 1.047 |

---

## 3. Detaylı Değerlendirme ve Analiz

### 3.1. Genel Kalite Değerlendirmesi
Projenin v1.0.0.0'dan v3.0.0.0'a kadar olan evrimi incelendiğinde, sistemin hacimsel olarak (LOC: 16k -> 35k, Sınıf Sayısı: 288 -> 609) iki katından fazla büyüdüğü görülmektedir. İlk sürümlerde (v1.0 - v1.3) yeni özelliklerin hızla eklenmesi (Functionality: 2.988 -> 3.221) kalite niteliklerinde dalgalanmalara yol açmıştır. Özellikle Understandability (Anlaşılabilirlik) niteliğinin ilk başlarda hızla düşmesi (-9.572'den -11.256'ya), kod tabanının karmaşıklaştığını ve yapısal bütünlüğün başlarda ikinci plana atıldığını göstermektedir.

Sürüm 2.16.0.0'da gerçekleşen büyük sıçrama, projenin genel kalite profilini baştan aşağı değiştirmiştir. Bu sürümde Sınıf Sayısı 364'ten 591'e, LOC ise yaklaşık 27 binden 34 bine fırlamıştır. Ancak dikkat çekici olan, eklenen devasa kod hacmine rağmen ortalama karmaşıklığın (WMC) 15.30'dan 12.02'ye düşmesidir. Bu durum, anlaşılabirliği nispeten artırmış (-11.272'den -10.744'e) fakat sistemin Reusability (Yeniden Kullanılabilirlik) ve Effectiveness (Etkililik) gibi değerlerini belirgin şekilde aşağı çekmiştir.

Genel tabloya bakıldığında, projenin büyüdükçe Extendibility (Genişletilebilirlik) ve Flexibility (Esneklik) yeteneklerini kaybettiği görülmektedir. V2.16'daki devasa değişiklik, kod seviyesinde bazı iyileştirmeler (örneğin daha küçük sınıflar) getirse de, sistem geneline bakıldığında nesne yönelimli tasarımın esneklik sağlayan soyutlama (abstraction) prensiplerinden uzaklaşıldığını ve projenin "katılaşmaya" (rigid) başladığını kanıtlamaktadır. V3.0'a geçişte ise metriklerin neredeyse tamamen sabit kalması, ana sürüm geçişinin mimari bir yenilenmeden ziyade pazarlama veya API uyumluluğu odaklı olduğunu düşündürmektedir.

### 3.2. Bakım Yapılabilirlik (Maintainability) Analizi
Bakım yapılabilirlik; sınıfların iç uyumu (Cohesion - LCOM), bağımlılıkları (Coupling - CBO) ve karmaşıklığı (WMC, RFC) ile doğrudan ilişkilidir. V1.0'dan V1.1'e geçişte LCOM değerinin 13.89'dan 27.19'a fırlaması, bakım yapılabilirlik açısından ilk büyük darbeyi vurmuştur. LCOM'un (Lack of Cohesion of Methods) yüksek olması, sınıfların tek sorumluluk prensibinden (Single Responsibility) uzaklaştığını ve alakasız metotların aynı sınıf içinde biriktiğini gösterir. Bu durum, ilk sürümlerde hataları bulmayı ve gidermeyi oldukça zorlaştırmıştır.

Sürüm 2.16.0.0, bakım yapılabilirlik açısından bir nevi "kurtarma operasyonu" niteliği taşımaktadır. Bu sürümde Ortalama WMC (15.30 -> 12.02), Ortalama RFC (19.77 -> 15.41) and LCOM (26.43 -> 18.14) ciddi düşüşler yaşamıştır. Özellikle Max_WMC'nin 318'den 190'a inmesi, kod tabanındaki "God Class" (Tanrı Sınıf - her şeyi yapan devasa sınıf) anti-örüntüsünün parçalandığını, sınıfların daha küçük ve odaklı hale getirildiğini ispatlamaktadır. Sınıf içindeki bu sadeleşme, geliştiricilerin kod parçalarını okumasını ve yerel bazda bakım yapmasını kolaylaştırmıştır.

Ancak, bu operasyonun bakım yapılabilirliğe negatif bir faturası da olmuştur: Sınıflar arası bağımlılık (CBO). Ortalama CBO 9.78'den 10.48'e çıkarken, Max_CBO 140'tan 214'e fırlamıştır. Yani kodlar daha küçük dosyalara bölünmüş, ancak bu dosyalar birbirine sıkı sıkıya bağlanmıştır (Spaghetti Code). Sonuç olarak; tekil dosyaları okumak ve düzeltmek kolaylaşmış olsa da, bir değişikliğin sistemin geneline yayılma riski (dalga etkisi) artmış, bu da sistem çapındaki bakım zorluğunu yükseltmiştir.

### 3.3. Teknik Borç Tahmini
Projenin teknik borç haritası, Max_CBO ve Max_WMC gibi uç değerler üzerinden net bir şekilde okunabilmektedir. İlk sürümlerde, Max_WMC'nin 308-318 bandında seyretmesi, geliştirme ekibinin pazara hızlı çıkmak veya yeni özellikleri hızlıca yetiştirmek adına mimari tasarımı es geçerek kodları birkaç merkezi sınıfa yığdığını göstermektedir. Bu "şişkinlik", projenin ilk 10 sürümü boyunca ödenmeyen yüksek faizli bir teknik borç olarak taşınmıştır.

V2.16.0.0 sürümündeki büyük refactoring, WMC odaklı teknik borcun bir kısmının ödendiğini gösteriyor. Ancak teknik borç tamamen silinmemiş, sadece şekil değiştirmiştir. Max_WMC borcu ödenirken, Max_CBO borcu yaratılmıştır (140 -> 214). Bir sınıfın tam 214 farklı sınıfa bağlı (coupled) olması, nesne yönelimli tasarım (OOD) kurallarının ihlal edildiği devasa bir tasarım borcudur. Bu merkezi orkestratör sınıf, ileride yapılacak herhangi bir inovasyonun önündeki en büyük darboğaz (bottleneck) haline gelmiştir.

Teknik borcun bir diğer kanıtı ise QMOOD esneklik (Flexibility) ve genişletilebilirlik (Extendibility) metriklerinin v2.16'dan sonra çökmesi ve v3.0 dahil olmak üzere düzelmemesidir. V2.19'dan V3.0'a geçişte hiçbir tasarım metriğinin (0'a yakın değişim) iyileşmemesi, ekibin teknik borçları kabullendiğini veya bu borçlara dokunmaktan korktuğunu (fragile system) göstermektedir. Projede biriken bu mimari teknik borç, gelecekte yeni özellik ekleme maliyetini (Time to Market) eksponansiyel olarak artıracaktır.

### 3.4. Refactoring Önerileri
Metrik analizlerine dayanarak, projenin acilen "Sınıflar Arası Bağımlılıkları (Coupling) Azaltma" stratejisine odaklanması gerekmektedir. Özellikle Max_CBO değeri 214 olan sınıf veya sınıflar derhal tespit edilmelidir. Bu kadar yüksek bağımlılık genellikle "Facade", "Mediator" veya gereksiz yere her şeyi yönetmeye çalışan merkezi yöneticilerden (Manager/Handler) kaynaklanır. Bu sınıflara Yüzdeleme (Extract Class) veya Arayüz Ayrımı (Interface Segregation) uygulanarak bağımlılıklar alt modüllere dağıtılmalı, Dependency Injection kullanımı sıkılaştırılmalıdır.

İkinci büyük refactoring odağı, iç uyum (Cohesion) olmalıdır. V2.16'da LCOM 18.14'e düşmüş olsa da, bu değer modern ve sağlıklı bir Java projesi için hala çok yüksektir (ideali 0'a yakın olmasıdır). Sınıfların içinde birbiriyle veri paylaşmayan (CAM değerinin sürekli negatif olması bunu destekliyor) metot grupları tespit edilmelidir. Veri ve metotları daha iyi sarmalayan (Encapsulation) yeni sınıflar yaratılmalı, veriye erişim metrikleri (DAM - Data Access Metric) v2.16 öncesi seviyelere (0.570+) geri çekilecek şekilde alanlar (fields) private yapılarak getter/setter kullanımı modernize edilmelidir.

Son olarak, çakılan Flexibility (-0.617) ve Extendibility (-4.159) metriklerini toparlamak için Polymorphism (Çok Biçimlilik) ve Kalıtım (Inheritance/Interface) kullanımı artırılmalıdır. Projede ana sınıfların sürekli somut (concrete) sınıflarla iletişim kurduğu anlaşılmaktadır. Geliştirme ekibinin, mevcut somut bağımlılıklar arasına "Interface" katmanları ekleyerek (Dependency Inversion Principle) sistemi yeni eklentilere (plugin/extension) kapalı kodu değiştirmeden açık (Open/Closed Principle) hale getirmesi şarttır.

### 3.5. Mimari Kalite Yorumları
Projenin mimari kalitesi, bir "büyük çamur topu" (Big Ball of Mud) evresinden, "dağıtılmış ama birbirine dolanmış" (Distributed Spagetti) bir evreye geçişin hikayesidir. Coupling (CBO) ve Cohesion (LCOM) trendleri, mimarinin temel bir zafiyetini ortaya koyuyor: Sistem büyüdükçe sınırlar (boundaries) korunamamıştır. V1.0'dan V2.13'e kadar sınıfların şişmesine (low cohesion) göz yumulmuş, V2.16'da ise bu sınıflar parçalanmış ama aralarındaki hiyerarşik veya modüler sınırlar çizilemediği için bu kez de yüksek bağımlılık (high coupling) problemi doğmuştur.

V2.16.0.0 sıçraması, projenin yaşam döngüsündeki en kritik mimari müdahaledir. Bu sürümde anomali tespiti için tamamen yeni bir mekanizma (muhtemelen yeni modeller veya paralel işleme altyapısı) eklendiği, bunun için 230'a yakın yeni sınıf üretildiği anlaşılmaktadır. Ancak bu yeni eklentiler mevcut mimariye "zarif" bir şekilde (interface'ler üzerinden) entegre edilememiş; aksine, ana yapıya adeta kaynaklanmıştır (hard-coupled). Bu durum, QMOOD Effectiveness ve Reusability değerlerindeki düşüşle kendini doğrulamaktadır. Kod, başka bağlamlarda kullanılamayacak kadar OpenSearch'e veya spesifik bir modüle sıkı sıkıya bağlanmıştır.

V3.0'a gelindiğinde mimarinin inovasyon yeteneğini kaybettiği, sadece mevcut yükü taşıyabildiği görülmektedir. CAM (Cohesion Among Methods of Class) metriğinin negatif ve istikrarlı kötü gidişi, projenin "Nesne Yönelimli" (Object-Oriented) olmaktan ziyade, veriyi bir yerden alıp diğerine taşıyan "Prosedürel" (Procedural) bir anemik domain modeline (Anemic Domain Model) sahip olduğunu fısıldamaktadır. Gerçek bir mimari kalite için Hexagonal (Ports and Adapters) veya Clean Architecture gibi, iş kurallarını altyapı bağımlılıklarından izole eden mimari yaklaşımların projeye acilen entegre edilmesi gerekmektedir.