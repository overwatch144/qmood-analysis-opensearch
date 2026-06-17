# OpenSearch Anomaly Detection Projesi QMOOD Analizi

## 1. Genel Kalite Değerlendirmesi

OpenSearch Anomaly Detection projesinin 12 sürümlük evrimi incelendiğinde, sistemin iki farklı gelişim dönemi geçirdiği görülmektedir. İlk dönem 1.0.0.0–2.13.0.0 aralığını kapsamaktadır. Bu dönemde sınıf sayısı 288’den 364’e, toplam LOC ise 16.903’ten 27.041’e yükselmiştir. Buna karşın ortalama CBO, WMC ve RFC metriklerinde kademeli bir artış gözlenmiştir. Özellikle CBO’nun 8.58’den 9.78’e yükselmesi ve LCOM’un 13.89’dan 26.43’e çıkması, büyüyen sistemin giderek daha fazla bağımlılık üretmeye başladığını ve sınıf içi bütünlüğün zayıfladığını göstermektedir.

QMOOD kalite nitelikleri bu eğilimi doğrulamaktadır. Reusability 4.147’den 4.361 seviyesine kadar yükselirken, Flexibility ve Extendibility sürekli kötüleşmiştir. Understandability metriğinin −9.57’den −11.27’ye düşmesi ise kod tabanının zamanla daha karmaşık hale geldiğini göstermektedir. Bu durum tipik olarak yeni özelliklerin mevcut mimari üzerine eklenmesiyle oluşan organik büyüme davranışına işaret etmektedir.

En dikkat çekici kırılma noktası ise 2.13.0.0 → 2.16.0.0 geçişidir. Bu sürümde sınıf sayısı yaklaşık %62 artarak 364’ten 591’e çıkmış, LOC ise %27 artmıştır. Buna rağmen ortalama WMC 15.30’dan 12.02’ye, RFC 19.77’den 15.41’e ve LCOM 26.43’ten 18.14’e düşmüştür. Bu durum sisteme büyük miktarda yeni kod eklenmesine rağmen karmaşıklığın daha küçük birimlere dağıtıldığını göstermektedir. Başka bir ifadeyle proje yalnızca büyümemiş, aynı zamanda yeniden yapılandırılmıştır.

Genel kalite açısından değerlendirildiğinde proje olgun bir açık kaynak sistem davranışı göstermektedir. 2.16 sonrasında kalite nitelikleri yeniden dengelenmiş, 2.19 ve 3.0 sürümlerinde ise metriklerin neredeyse sabit kalması mimarinin kararlı bir duruma ulaştığını göstermektedir.

---

## 2. Bakım Yapılabilirlik (Maintainability) Analizi

Bakım yapılabilirlik açısından en kritik göstergeler WMC, RFC, CBO ve LCOM metrikleridir. İlk sürümlerde WMC’nin 11.69’dan 15.49’a yükselmesi, sınıfların zamanla daha fazla sorumluluk üstlendiğini göstermektedir. RFC’nin yaklaşık 20 seviyesine çıkması da değişikliklerin sistem genelinde daha fazla etki yaratabileceğini işaret etmektedir. Bu dönemde bakım maliyetinin kademeli olarak arttığı söylenebilir.

LCOM eğilimi bakım yapılabilirlik açısından özellikle önemlidir. 1.0 sürümünde 13.89 olan değer 1.1 sürümünde ani şekilde 27.19’a yükselmiştir. Bu değişim sürümler arası delta tablosunda da en büyük bozulmalardan biri olarak görünmektedir. Cohesion'ın düşmesi, sınıfların birden fazla sorumluluk taşımaya başladığını ve bakım süreçlerinde geliştiricilerin daha fazla kod bağlamı anlaması gerektiğini göstermektedir.

Bununla birlikte 2.16.0.0 sürümü bakım yapılabilirlik açısından önemli bir iyileşme noktasıdır. Ortalama WMC yaklaşık %21 azalırken RFC yaklaşık %22 düşmüştür. LCOM değeri ise 26.43’ten 18.14’e gerilemiştir. Bu değişimler daha küçük, daha odaklı ve daha anlaşılabilir sınıflara geçiş yapıldığını göstermektedir. Dolayısıyla bakım yapılabilirlik açısından 2.16 sürümü belirgin bir refactoring veya mimari yeniden organizasyon etkisi göstermektedir.

Ancak bakım yapılabilirlik tamamen iyileşmiş değildir. Ortalama CBO değeri 10.48 seviyesine yükselmiş ve sonraki sürümlerde bu seviyede kalmıştır. Bu durum sınıfların iç karmaşıklığı azalırken sistemler arası bağımlılıkların arttığını göstermektedir. Dolayısıyla yerel bakım kolaylaşmış olsa da değişikliklerin sistem genelindeki etkisini analiz etmek hâlâ önemli bir maliyet oluşturmaktadır.

---

## 3. Teknik Borç Tahmini

Teknik borç genellikle artan karmaşıklık, düşük cohesion ve yüksek coupling kombinasyonu ile ilişkilendirilir. 1.0–2.13 arası dönemde teknik borcun sürekli arttığı söylenebilir. Özellikle LCOM’un yaklaşık iki katına çıkması, WMC ve RFC değerlerinin yükselmesi ve Understandability skorunun sürekli düşmesi bu görüşü desteklemektedir.

QMOOD kalite niteliklerinden Understandability’nin −9.57’den −11.27’ye gerilemesi geliştiricilerin sistemi anlamasının giderek zorlaştığını göstermektedir. Benzer şekilde Extendibility’nin −3.29’dan −3.88’e düşmesi de yeni özellik ekleme maliyetinin arttığını ifade etmektedir. Bu göstergeler, 2.13 sürümüne kadar teknik borcun kontrollü ancak sürekli büyüdüğünü göstermektedir.

2.16 sürümünde ilginç bir durum ortaya çıkmaktadır. Bir yandan Understandability yaklaşık 0.53 puan iyileşmekte ve cohesion belirgin şekilde yükselmektedir. Bu durum teknik borcun bir bölümünün ödendiğini düşündürmektedir. Öte yandan Flexibility değeri −0.125’ten −0.605’e ve Extendibility −3.878’den −4.163’e düşmektedir. Bunun nedeni DCC (coupling) ve DIT değerlerindeki artıştır.

Dolayısıyla 2.16 sürümü teknik borcun tamamen azaltıldığı bir sürüm değil, teknik borcun türünün değiştiği bir sürümdür. Önceden sistem içinde büyük ve karmaşık sınıflar şeklinde biriken borç, daha sonra daha modüler ancak daha bağımlı bileşenlere dönüşmüştür. Bu nedenle proje, monolitik karmaşıklık borcunu azaltırken entegrasyon ve bağımlılık borcunu artırmış görünmektedir.

---

## 4. Refactoring Önerileri

İlk öneri coupling azaltmaya yönelik olmalıdır. Ortalama CBO’nun 10.48 seviyesine yükselmesi ve maksimum CBO’nun 214’e çıkması oldukça dikkat çekicidir. Bir sınıfın 200’den fazla başka sınıfla ilişki kurması, mimaride merkezi koordinatör veya God Class benzeri yapılar bulunduğunu düşündürmektedir. Bu sınıflar tespit edilerek Facade, Mediator veya Event-Driven iletişim mekanizmalarıyla bağımlılıkları azaltılmalıdır.

İkinci öneri yüksek karmaşıklığa sahip sınıflar için uygulanmalıdır. Maksimum WMC değeri ilk dönemlerde 314–318 seviyelerine ulaşmış, daha sonra 190 civarına düşmüştür. İyileşme görülmesine rağmen 190 değeri hâlâ oldukça yüksektir. Bu sınıflar üzerinde Extract Class, Extract Method ve Strategy Pattern uygulamaları değerlendirilmelidir.

Üçüncü olarak, CAM değerlerinin tüm sürümlerde negatif olması dikkat çekmektedir. CAM, metod parametreleri arasındaki ortaklığı ölçtüğünden, negatif değerler sınıflar arasında anlamsal bütünlüğün istenen düzeyde olmadığını göstermektedir. Domain odaklı tasarım (DDD) prensipleriyle sınıfların iş sorumlulukları yeniden gözden geçirilebilir.

Son olarak, 2.16 sonrası mimaride ortaya çıkan yüksek coupling seviyeleri için servis sınırlarının netleştirilmesi önerilir. Eğer yeni eklenen modüller arasında yoğun karşılıklı bağımlılık bulunuyorsa, paket bağımlılık analizleri yapılarak cyclic dependency’ler azaltılmalıdır. Bu çalışma özellikle gelecekteki bakım maliyetlerini düşürecektir.

---

## 5. Mimari Kalite Yorumları

Mimari açıdan sistemin evrimi incelendiğinde iki farklı strateji görülmektedir. İlk strateji (1.0–2.13), mevcut yapı üzerine sürekli yeni özellik eklenmesi şeklindedir. Bu yaklaşım sınıf sayısında sınırlı büyüme yaratırken sınıf başına düşen karmaşıklığı artırmıştır. Sonuç olarak WMC, RFC ve LCOM değerleri yükselmiş; mimari giderek daha yoğun ve daha zor anlaşılır hale gelmiştir.

İkinci strateji ise 2.16 sürümüyle başlamaktadır. Sınıf sayısının 364’ten 591’e çıkması ve ortalama WMC’nin önemli ölçüde düşmesi, mimarinin daha ince taneli bileşenlere bölündüğünü göstermektedir. Bu durum mikro-modülerleşme veya kapsamlı refactoring faaliyetlerinin göstergesi olabilir. Özellikle cohesion’daki iyileşme (LCOM 26.43 → 18.14) mimari açıdan olumlu bir gelişmedir.

Buna karşın coupling eğilimi mimarinin zayıf noktası olmaya devam etmektedir. DCC değeri 8.58’den 10.48’e yükselmiş ve son sürümlerde bu seviyede sabitlenmiştir. Yani sistem daha modüler hale gelirken modüller arası iletişim yoğunlaşmıştır. Mimari kalite açısından bu durum iyi ayrıştırılmış fakat sıkı entegre edilmiş bir yapı olarak yorumlanabilir.

Sonuç olarak OpenSearch Anomaly Detection mimarisi, 2.16 sürümünde önemli bir yeniden yapılanma geçirerek sınıf içi kaliteyi artırmış, karmaşıklığı dağıtmış ve cohesion'ı iyileştirmiştir. Ancak bu dönüşüm coupling maliyetini artırmış ve QMOOD’un Flexibility ile Extendibility niteliklerinde belirgin düşüşlere yol açmıştır. Mimari olgunluk açısından 3.0 sürümü kararlı görünse de gelecekteki kalite iyileştirmelerinin odağı artık sınıf içi karmaşıklık değil, modüller arası bağımlılıkların azaltılması olmalıdır. Bu nedenle projenin mevcut en büyük mimari riski düşük cohesion değil, yüksek coupling olarak değerlendirilebilir.
