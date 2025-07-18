class Savasci:
    def __init__(self, adi, kaynak, can, saldiri_hedefleri, saldiri_hasarlari, saldiri_menzilleri):
        self.adi = adi
        self.kaynak = kaynak
        self.can = can
        self.saldiri_hedefleri = saldiri_hedefleri
        self.saldiri_hasarlari = saldiri_hasarlari
        self.saldiri_menzilleri = saldiri_menzilleri

class Muhafiz(Savasci):
    def __init__(self):
        super().__init__("Muhafiz", 10, 80, "Tüm düşmanlar", -20, [1, 1, 1])

class Okcu(Savasci):
    def __init__(self):
        super().__init__("Okçu", 20, 30, "En yüksek canı olan 3 düşman", -0.6, [2, 2, 2])

class Topcu(Savasci):
    def __init__(self):
        super().__init__("Topçu", 50, 30, "En yüksek canı olan 1 düşman", -1, [2, 2, 0])

class Atli(Savasci):
    def __init__(self):
        super().__init__("Atlı", 30, 40, "En pahalı 2 düşman", -30, [0, 0, 3])

class Saglikci(Savasci):
    def __init__(self):
        super().__init__("Sağlıkçı", 10, 100, "En az canı olan 3 dost birlik", 0.5, [2, 2, 2])

# Puan ve tahmini fayda değerlerini tanımlayalım
savaşçılar = [Muhafiz(), Okcu(), Topcu(), Atli(), Saglikci()]
puanlar = [s.kaynak for s in savaşçılar]
tahmini_faydalar = [-s.saldiri_hasarlari * s.can for s in savaşçılar]

# Puan/fayda oranlarını hesaplayalım
puan_fayda_oranları = [puan / fayda for puan, fayda in zip(puanlar, tahmini_faydalar)]

# En yüksek puan/fayda oranına sahip savaşçıyı seçelim
en_yuksek_oranli_savasci = savaşçılar[puan_fayda_oranları.index(max(puan_fayda_oranları))]

print("En yüksek puan/fayda oranına sahip savaşçı:", en_yuksek_oranli_savasci.adi)
