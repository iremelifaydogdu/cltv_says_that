#CUSTOMER LIFETIME VALUE (Müşteri Yaşam Boyu Değeri)

#Bir müşterinin bir şirketle kurduğu ilişki-iletişim süresince bu şirkete kazandıracağı parasal değerdir.

#Şirketimizde orta-uzun vadeli daha müşteri odaklı-katma değer odaklı bir yaklaşım sergileyebiliriz. Bu aynı zamanda pazarlama faaliyetleri için ayrılacak olan bütçelerin
#belirlenmesinde bir rol oynayabilecektir.
#CLTV değerlerini hesaplayabilirsek bu durumda bir diğer kaygımız olan yeni müşteri bulma çabamızın da
#maliyetlerini eğer birimleştirebilirsek bu durumda var olanlarla yenilerini bulmak arasındaki teoride sıkça duyduğumuz ama pratikte uygulanması zor olan bu konuya dair de bir bilgi edinmiş oluruz.

#Yani elimizdeki mevcut müşteri kitlesinden önümüzdeki dönemde şöyle bir parasal değer bekliyoruz. Bir de yeni müşteri bulma maliyetimiz var bunun maliyeti de bu diyerek bu ikisini kıyaslayabiliriz.

#Peki CLTV nasıl hesaplanır? Bir çok formül vardır. Hesaplamak ve tahmin etmek farklı şeylerdir. Biz bu konu kapsamında basitçe hesaplama işlemi yapıcaz. Bu da kısmi olarak tahmin etmek demektir.
#Kısmi olarak tahmin olarak değerlerlendirilebilir fakat zaman projeksiyonu yönü olmayacaktır. İleriye yönelik geniş açıdan bir perspektif sunmayacak olacaktır. Fakat yine de var olan müşterilerimizin değerlerini
#belirlemek adına da oldukça değerli olacaktır.

#Siz olsanız nasıl hesaplardınız?

#Benimle kurduğu ilişki süresince müşterinin bana bırakacak olduğu değeri nasıl hespalardım?

#satın alma başına ortalama kazanç * satın alma sayısı = bir müşteri için potansiyel değer hesabı

#CLTV= (müşteri değeri /churn oranı) * kar marjı          #churn oranı bir sabittir. #kar marjı ise şirketin müşterilerle yaptığı alışverişlerde varsayacağı bir kar miktarı olacak. Kişilerin şirkete bıraktığı gelirle bu kar marjı çarpıldığında proift margin ortaya çıkacak.

#müşteri değeri= ortalama sipariş değeri * satın alma sıklığı

#ortalama sipariş değeri = toplam kişinin bıraktığı gelir miktarı / toplam işlem sayısı

# satın alma frekansı = toplam işlem sayısı (bir fatura kesilmesi=bir transaction/işlem, yani kaç birim aldığıyla ilgilnemiyoruz.) / toplam müşteri sayısı

#müşteri terk oranı (chrun rate)= 1- repeat rate (tekrar oranı= elde tutma oranı)

#repeat rate = birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler

#profit margin = total price * 0.10

#Sonuç olarak: her bir müşteri çin hesaplanacak olan CLTV değerlerine göre bir sıralama yapıldığında ve CLTV değerlerine göre belirli noktalardan bölme işlemi yapılarak gruplar oluşturulduğunda müşterilerimiz segmentlere ayrılmış olacaktır.


############################################
# CUSTOMER LIFETIME VALUE (Müşteri Yaşam Boyu Değeri)
############################################

# 1. Veri Hazırlama
# 2. Average Order Value (average_order_value = total_price / total_transaction)
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
# 4. Repeat Rate & Churn Rate (birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
# 5. Profit Margin (profit_margin =  total_price * 0.10)
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
# 8. Segmentlerin Oluşturulması
# 9. BONUS: Tüm İşlemlerin Fonksiyonlaştırılması

##################################################
# 1. Veri Hazırlama
##################################################

# Veri Seti Hikayesi
# https://archive.ics.uci.edu/ml/datasets/Online+Retail+II

# Online Retail II isimli veri seti İngiltere merkezli online bir satış mağazasının
# 01/12/2009 - 09/12/2011 tarihleri arasındaki satışlarını içeriyor.

# Değişkenler
# InvoiceNo: Fatura numarası. Her işleme yani faturaya ait eşsiz numara. C ile başlıyorsa iptal edilen işlem.
# StockCode: Ürün kodu. Her bir ürün için eşsiz numara.
# Description: Ürün ismi
# Quantity: Ürün adedi. Faturalardaki ürünlerden kaçar tane satıldığını ifade etmektedir.
# InvoiceDate: Fatura tarihi ve zamanı.
# UnitPrice: Ürün fiyatı (Sterlin cinsinden)
# CustomerID: Eşsiz müşteri numarası
# Country: Ülke ismi. Müşterinin yaşadığı ülke.

#Fatura kesme işlemine göre biçimlendirilmiş bir datadır. Bizim için önemli olan faturadır.
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
pd.set_option('display.max_columns', None) #bütün sütunlar, print edince değişkenlerin tüm hepsini getirmek istediğimizi ifade eder.
# pd.set_option('display.max_rows', None) #bütün satırlar
pd.set_option('display.float_format', lambda x: '%.5f' % x) #float sayıların virgülden sonra ondalık olarak kaç basamak getirmesi gerektiğini

df_ = pd.read_excel("HAFTA 3/Materyaller/cltv/online_retail_II.xlsx", sheet_name="Year 2009-2010")
df = df_.copy()
df.head()

df.isnull().sum()
df = df[~df["Invoice"].str.contains("C", na=False)] #içinde C ifadesi olmayanarı getirir
df.describe().T
df = df[(df['Quantity'] > 0)] #eksi sayıda miktar olamaz, df'i buna göre filtrele ve df'e eşitle.
df.dropna(inplace=True) #eksik değerleri uçurmamız gerek.

#Veri setinde şöyle bir problem var: veriye baktığımda birim fiyatı görüyorum, kaç tane satın alınma gerçekleştirildiğini görüyrum ama faturanın toplam fiyatını görmüyorum.
df["TotalPrice"] = df["Quantity"] * df["Price"]

#Veri setinin en kritik bölümüne gelelim:

cltv_c = df.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                        'Quantity': lambda x: x.sum(),
                                        'TotalPrice': lambda x: x.sum()})

#quantity burada analiz etmek, gözlemlemek için var.
cltv_c
#             Invoice  Quantity  TotalPrice
#Customer ID
#12346.00000       11        70   372.86000
#12347.00000        2       828  1323.32000
#12348.00000        1       373   222.16000
#12349.00000        3       993  2671.14000
#12351.00000        1       261   300.93000
#              ...       ...         ...
#18283.00000        6       336   641.77000
#18284.00000        1       494   461.68000
#18285.00000        1       145   427.00000
#18286.00000        2       608  1296.43000
#18287.00000        4      1427  2345.71000
#[4314 rows x 3 columns]


cltv_c.columns
#Index(['Invoice', 'Quantity', 'TotalPrice'], dtype='object')

cltv_c.columns = ['total_transaction', 'total_unit', 'total_price'] #yukarıdaki isimleri yeniden tanımlıyorum.

#RFM analizindeki recency değeri burada yok, frequency = total transaction, maturity ise total price ile aynıdır.


##################################################
# 2. Average Order Value (average_order_value = total_price / total_transaction)
##################################################

cltv_c.head()
cltv_c["average_order_value"] = cltv_c["total_price"] / cltv_c["total_transaction"]
cltv_c["average_order_value"]
#Customer ID
#12346.00000    33.89636
#12347.00000   661.66000
#12348.00000   222.16000
#12349.00000   890.38000
#12351.00000   300.93000
#                 ...
#18283.00000   106.96167
#18284.00000   461.68000
#18285.00000   427.00000
#18286.00000   648.21500
#18287.00000   586.42750
#Name: average_order_value, Length: 4314, dtype: float64


##################################################
# 3. Purchase Frequency (total_transaction / total_number_of_customers)
##################################################

cltv_c.head()
cltv_c["total_transaction"]
cltv_c.shape[0] #total number of customers
#4314
cltv_c["purchase_frequency"] = cltv_c["total_transaction"] / cltv_c.shape[0]
cltv_c["purchase_frequency"]
#Customer ID
#12346.00000   0.00255
#12347.00000   0.00046
#12348.00000   0.00023
#12349.00000   0.00070
#12351.00000   0.00023
#                ...
#18283.00000   0.00139
#18284.00000   0.00023
#18285.00000   0.00023
#18286.00000   0.00046
#18287.00000   0.00093
#Name: purchase_frequency, Length: 4314, dtype: float64



##################################################
# 4. Repeat Rate & Churn Rate (Repeat_rate= birden fazla alışveriş yapan müşteri sayısı / tüm müşteriler)
##################################################
#Tekrarlama oranı ve kaybetme oranı

#birden fazla alışveriş yapan müşteri sayısını nasıl buluruz:
cltv_c[cltv_c["total_transaction"] > 1] #total tarnsaction değeri 1'den büyük olan müşteriler geldi.
#             total_transaction  total_unit  total_price  average_order_value  \
#Customer ID
#12346.00000                 11          70    372.86000             33.89636
#12347.00000                  2         828   1323.32000            661.66000
#12349.00000                  3         993   2671.14000            890.38000
#12352.00000                  2         188    343.80000            171.90000
#12356.00000                  3        1826   3562.25000           1187.41667
#                        ...         ...          ...                  ...
#18276.00000                  5        1060   1320.66000            264.13200
#18277.00000                  4         381   1069.67000            267.41750
#18283.00000                  6         336    641.77000            106.96167
#18286.00000                  2         608   1296.43000            648.21500
#18287.00000                  4        1427   2345.71000            586.42750
#             purchase_frequency
#Customer ID
#12346.00000             0.00255
#12347.00000             0.00046
#12349.00000             0.00070
#12352.00000             0.00046
#12356.00000             0.00070
#                         ...
#18276.00000             0.00116
#18277.00000             0.00093
#18283.00000             0.00139
#18286.00000             0.00046
#18287.00000             0.00093
#[2893 rows x 5 columns]

#birden fazla alışveriş yapan müşteri sayısı ifadesine nasıl erişirim?:
cltv_c[cltv_c["total_transaction"] > 1].shape[0]
# 2893

repeat_rate = cltv_c[cltv_c["total_transaction"] > 1].shape[0] / cltv_c.shape[0]
repeat_rate
#0.6706073249884098

churn_rate = 1 - repeat_rate


##################################################
# 5. Profit Margin (profit_margin =  total_price * 0.10)
##################################################

cltv_c['profit_margin'] = cltv_c['total_price'] * 0.10


##################################################
# 6. Customer Value (customer_value = average_order_value * purchase_frequency)
##################################################

cltv_c['customer_value'] = cltv_c['average_order_value'] * cltv_c["purchase_frequency"]
cltv_c['customer_value']
#Customer ID
#12346.00000   0.08643
#12347.00000   0.30675
#12348.00000   0.05150
#12349.00000   0.61918
#12351.00000   0.06976
#                ...
#18283.00000   0.14876
#18284.00000   0.10702
#18285.00000   0.09898
#18286.00000   0.30052
#18287.00000   0.54374
#Name: customer_value, Length: 4314, dtype: float64



##################################################
# 7. Customer Lifetime Value (CLTV = (customer_value / churn_rate) x profit_margin)
##################################################

cltv_c["cltv"] = (cltv_c["customer_value"] / churn_rate) * cltv_c["profit_margin"]
cltv_c["cltv"]
#Customer ID
#12346.00000     9.78357
#12347.00000   123.23546
#12348.00000     3.47326
#12349.00000   502.11041
#12351.00000     6.37290
#                 ...
#18283.00000    28.98443
#18284.00000    14.99989
#18285.00000    12.83103
#18286.00000   118.27803
#18287.00000   387.21713
#Name: cltv, Length: 4314, dtype: float64



#Bu değerleri küçükten büyüğe, büyükten küçüğe sıralamak istiyoruz, görelim bizim için en değerli müşteriler kimler diye:
cltv_c.sort_values(by="cltv", ascending=False).head()
#             total_transaction  total_unit  total_price  average_order_value  \
#Customer ID
#18102.00000                 89      124216 349164.35000           3923.19494
#14646.00000                 78      170342 248396.50000           3184.57051
#14156.00000                102      108107 196566.74000           1927.12490
#14911.00000                205       69722 152147.57000            742.18327
#13694.00000                 94      125893 131443.19000           1398.33181
#             purchase_frequency  customer_value  profit_margin          cltv
#Customer ID
#18102.00000             0.02063        80.93749    34916.43500 8579573.77276
#14646.00000             0.01808        57.57916    24839.65000 4342070.45829
#14156.00000             0.02364        45.56484    19656.67400 2719105.08615
#14911.00000             0.04752        35.26833    15214.75700 1629055.80978
#13694.00000             0.02179        30.46898    13144.31900 1215855.89003

cltv_c.describe().T
#                        count       mean          std     min       25%  \
#total_transaction   4314.00000    4.45410      8.16866 1.00000   1.00000
#total_unit          4314.00000 1284.01113   6458.45205 1.00000 158.00000
#total_price         4314.00000 2047.28866   8912.52324 0.00000 307.95000
#average_order_value 4314.00000  378.14723    492.51721 0.00000 181.95632
#purchase_frequency  4314.00000    0.00103      0.00189 0.00023   0.00023
#customer_value      4314.00000    0.47457      2.06595 0.00000   0.07138
#profit_margin       4314.00000  204.72887    891.25232 0.00000  30.79500
#cltv                4314.00000 5883.60651 156068.63594 0.00000   6.67369
#                          50%        75%           max
#total_transaction     2.00000    5.00000     205.00000
#total_unit          382.00000  995.25000  220600.00000
#total_price         705.55000 1722.80250  349164.35000  ##

#Bu müşterinin en tepede olması durumunu doğrulamaya çalışıyoruz.
#             total_transaction  total_unit  total_price  average_order_value  \
#Customer ID
#18102.00000                 89      124216 349164.35000           3923.19494


#349164.35000
#average_order_value değerleri farklı, tek başına sırlama için kullanılmamış olabilir.
#başka faktörler de göz önünde bulundurulmuş olabilir.

##################################################
# 8. Segmentlerin Oluşturulması
##################################################
#cltv= her bir müşterimizin bizim için bizimle sağlayacak olduğu iletişim ve etkileşime yönelik biçmiş olduğumuz değeri
#bu değer diğer tüm metriklerin de bazı etkilerini içinde barındıran bir değer.
#bir müşteri grubuyla daha fazla ilgilenmeyi tercih etmem gerekirse nereye odaklanabileceğimi bildiğim anlamına geliyor.


cltv_c.sort_values(by="cltv", ascending=False).head()
cltv_c.sort_values(by="cltv", ascending=False).tail()

#ilgileneceğim müşterilerin kaç tanesine odaklanmalıyım? fikir verecek yaklaşım segmentlere ayırmaktır.


cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])
#qcut der ki bana bir değişken ver ve kaç parçaya bölmek istediğini söyle labellarını da verirsen küçükten büyüğe sıralar ve istediğin şekilde etiketlendirirm der.
cltv_c.sort_values(by="cltv", ascending=False).head() #segmentler oluşturuldu ve buna göre yanlarına müşteriler yazıldı.

#çeyrek değerlere göre veri setini böldü qcut güzel, ama bunlar mantıklı mı?
#oluşturulan çeyrek değerlere göre oluşan segmentlerin betimlemesini yapmak gerekmektedir.
#yani bunları analiz etmek gerekmektedir.
cltv_c.groupby("segment").agg({"count", "mean", "sum"})
#normalde müşteri tekilinde olan cltv_c veri setni segmentlere göre group_by'a aldık ve segmentlerin herbisi için özet istatistik aldık.

#        total_transaction                total_unit                   \
#                      sum     mean count        sum       mean count
#segment
#D                    1326  1.22892  1079     117616  109.00463  1079
#C                    2160  2.00371  1078     305135  283.05659  1078
#B                    4063  3.76902  1078     733211  680.15863  1078
#A                   11666 10.81186  1079    4383262 4062.33735  1079
#          total_price                  average_order_value                  \
#                  sum       mean count                 sum      mean count
#segment
#D        192265.13000  178.18826  1079        169805.46550 157.37300  1079
#C        513016.45300  475.89652  1078        317422.35514 294.45487  1078
#B       1219605.20000 1131.35918  1078        420127.12365 389.72832  1078
#A       6907116.49100 6401.40546  1079        723972.22347 670.96592  1079
#        purchase_frequency               customer_value                \
#                       sum    mean count            sum    mean count
#segment
#D                  0.30737 0.00028  1079       44.56772 0.04130  1079
#C                  0.50070 0.00046  1078      118.91897 0.11031  1078
#B                  0.94182 0.00087  1078      282.70867 0.26225  1078
#A                  2.70422 0.00251  1079     1601.09330 1.48387  1079
#        profit_margin                           cltv
#                  sum      mean count            sum        mean count
#segment
#D         19226.51300  17.81883  1079     2849.32790     2.64071  1079
#C         51301.64530  47.58965  1078    18184.26342    16.86852  1078
#B        121960.52000 113.13592  1078   103549.86329    96.05739  1078
#A        690711.64910 640.14055  1079 25257295.04118 23408.05843  1079



cltv_c.to_csv("cltc_c.csv")

# 18102.00000       A
# 14646.00000       A
# 14156.00000       A
# 14911.00000       A
# 13694.00000       A

# Customer ID
# 18102.00000       A
# 14646.00000       A
# 14156.00000       A
# 14911.00000       A
# 13694.00000       A

##################################################
# 9. BONUS: Tüm İşlemlerin Fonksiyonlaştırılması
##################################################

def create_cltv_c(dataframe, profit=0.10):

    # Veriyi hazırlama
    dataframe = dataframe[~dataframe["Invoice"].str.contains("C", na=False)]
    dataframe = dataframe[(dataframe['Quantity'] > 0)]
    dataframe.dropna(inplace=True)
    dataframe["TotalPrice"] = dataframe["Quantity"] * dataframe["Price"]
    cltv_c = dataframe.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                                   'Quantity': lambda x: x.sum(),
                                                   'TotalPrice': lambda x: x.sum()})
    cltv_c.columns = ['total_transaction', 'total_unit', 'total_price']
    # avg_order_value
    cltv_c['avg_order_value'] = cltv_c['total_price'] / cltv_c['total_transaction']
    # purchase_frequency
    cltv_c["purchase_frequency"] = cltv_c['total_transaction'] / cltv_c.shape[0]
    # repeat rate & churn rate
    repeat_rate = cltv_c[cltv_c.total_transaction > 1].shape[0] / cltv_c.shape[0]
    churn_rate = 1 - repeat_rate
    # profit_margin
    cltv_c['profit_margin'] = cltv_c['total_price'] * profit
    # Customer Value
    cltv_c['customer_value'] = (cltv_c['avg_order_value'] * cltv_c["purchase_frequency"])
    # Customer Lifetime Value
    cltv_c['cltv'] = (cltv_c['customer_value'] / churn_rate) * cltv_c['profit_margin']
    # Segment
    cltv_c["segment"] = pd.qcut(cltv_c["cltv"], 4, labels=["D", "C", "B", "A"])

    return cltv_c


df = df_.copy()

clv = create_cltv_c(df)























































































