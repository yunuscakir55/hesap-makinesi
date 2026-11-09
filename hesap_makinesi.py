import ast
import operator
import math
import tkinter as tk
import re
from tkinter import messagebox

ARKA_PLAN = "#171923"
PANEL = "#222633"
EKRAN_RENGI = "#10131A"
SAYI_RENGI = "#303747"
ISLEM_RENGI = "#414C65"
VURGU_RENGI = "#6C8CFF"
YAZI_RENGI = "#F5F7FA"
IKINCIL_YAZI = "#AAB2C5"
SILME_RENGI = "#A84252"
ESITTIR_RENGI = "#5278F5"

OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

def kotanjant(x):
    sinüs = math.sin(x)

    if math.isclose(sinüs, 0.0, abs_tol=1e-12):
        raise ZeroDivisionError

    return math.cos(x) / sinüs

def kok_al(sayi, derece):
    if derece == 0:
        raise ValueError("Kök derecesi sıfır olamaz.")

    if sayi < 0:
        if derece % 2 == 0:
            raise ValueError("Negatif sayının çift dereceli kökü alınamaz.")

        return -((-sayi) ** (1 / derece))

    return sayi ** (1 / derece)

def faktoriyel_al(sayi):
    if not isinstance(sayi, int) or isinstance(sayi, bool):
        raise ValueError("Faktöriyel tam sayı gerektirir.")

    if sayi < 0:
        raise ValueError("Negatif sayıların faktöriyeli alınamaz.")

    if sayi > 1000:
        raise ValueError("Sayı çok büyük.")

    return math.factorial(sayi)

FONKSIYONLAR = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "cot": kotanjant,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "log": math.log10,
    "ln": math.log,
    "sqrt": math.sqrt,
    "cbrt": math.cbrt,
    "kok": kok_al,
    "fact": faktoriyel_al,
    "abs": abs
}

def hesapla(ifade, aci_modu="DEG", ans=0):
    ifade = re.sub(r'(\d)\s*(pi|e)\b', r'\1*\2', ifade)
    ifade = re.sub(r'(\))\s*(pi|e)\b', r'\1*\2', ifade)
    ifade = re.sub(r'\b(pi|e)\s*(\()', r'\1*\2', ifade)
    ifade = re.sub(r'(\d|\))\s*(sin|cos|tan|cot|asin|acos|atan|log|ln|sqrt|cbrt|kok|fact|abs)\s*\(', r'\1*\2(', ifade)
    ifade = re.sub(r'(\d|\))\s*(\()', r'\1*\2', ifade)
    ifade = re.sub(r'(\))\s*(\d)', r'\1*\2', ifade)
    ifade = re.sub(
        r'(\d+(?:\.\d+)?|\([^()]*\))!',
        r'fact(\1)',
        ifade
    )

    yuzde_deseni = r'(\d+(?:\.\d+)?|\([^()]*\))\s*([+-])\s*(\d+(?:\.\d+)?)%'

    def yuzde_donusumu(eslesme):
        taban = eslesme.group(1)
        islem = eslesme.group(2)
        yuzde = eslesme.group(3)

        return f"({taban}{islem}({taban}*{yuzde}/100))"

    ifade = re.sub(yuzde_deseni, yuzde_donusumu, ifade)

    ifade = re.sub(
        r'(\d+(?:\.\d+)?)%',
        r'(\1/100)',
        ifade
    )

    def degerlendir(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            if isinstance(node.value, float) and not math.isfinite(node.value):
                raise ValueError("Geçersiz veya sonsuz sayı.")
            return node.value
        
        if isinstance(node, ast.Name):
            sabitler = {
                "pi": math.pi,
                "e": math.e,
                "Ans": ans
            }

            if node.id in sabitler:
                return sabitler[node.id]

            raise ValueError("Bilinmeyen matematiksel sabit.")

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Geçersiz fonksiyon.")

            fonksiyon = FONKSIYONLAR.get(node.func.id)

            if fonksiyon is None or node.keywords:
                raise ValueError("Geçersiz matematik fonksiyonu.")

            if node.func.id == "kok":
                if len(node.args) != 2:
                    raise ValueError("Kök fonksiyonu iki değer gerektirir.")

                sayi = degerlendir(node.args[0])
                derece = degerlendir(node.args[1])

                if not isinstance(derece, (int, float)) or not math.isfinite(derece) or derece != int(derece):
                    raise ValueError("Kök derecesi tam sayı olmalıdır.")

                return kok_al(sayi, int(derece))

            if len(node.args) != 1:
                raise ValueError("Bu fonksiyon tek değer gerektirir.")

            arguman = degerlendir(node.args[0])

            aci_fonksiyonlari = ("sin", "cos", "tan", "cot")
            ters_fonksiyonlar = ("asin", "acos", "atan")

            if aci_modu == "DEG" and node.func.id in aci_fonksiyonlari:
                arguman = math.radians(arguman)

            if node.func.id == "tan":
                if math.isclose(math.cos(arguman), 0.0, abs_tol=1e-12):
                    raise ValueError("Tanjant bu açıda tanımsızdır.")

            sonuc = fonksiyon(arguman)

            if isinstance(sonuc, complex):
                raise ValueError("Karmaşık sayılar desteklenmiyor.")

            if isinstance(sonuc, float) and not math.isfinite(sonuc):
                raise ValueError("Sonuç sonlu bir sayı olmalıdır.")

            if aci_modu == "DEG" and node.func.id in ters_fonksiyonlar:
                sonuc = math.degrees(sonuc)

            return sonuc

        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            sol = degerlendir(node.left)
            sag = degerlendir(node.right)

            if isinstance(node.op, ast.Div) and sag == 0:
                raise ZeroDivisionError

            if isinstance(node.op, ast.Pow) and abs(sag) > 1000:
                raise ValueError("Üs değeri çok büyük.")

            sonuc = OPERATORS[type(node.op)](sol, sag)

            if isinstance(sonuc, complex):
                raise ValueError("Karmaşık sayılar desteklenmiyor.")

            if isinstance(sonuc, float) and not math.isfinite(sonuc):
                raise ValueError("Sonuç çok büyük.")

            return sonuc

        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](degerlendir(node.operand))

        raise ValueError("Geçersiz matematiksel ifade.")

    agac = ast.parse(ifade, mode="eval")
    return degerlendir(agac.body)


class HesapMakinesi:

    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Hesap Makinesi")
        self.pencere.geometry("420x700")
        self.pencere.resizable(True, True)
        self.pencere.minsize(420, 650)
        self.pencere.configure(bg=ARKA_PLAN)

        self.ifade = tk.StringVar()
        self.gecmis = []
        self.aci_modu = "DEG"
        self.ans = 0
        self.sonuc_gosterildi = False
        self.bellek = 0
        self.bilimsel_modu = True

        baslik = tk.Label(
            pencere,
            text="HESAP MAKİNESİ",
            font=("Arial", 12, "bold"),
            bg=ARKA_PLAN,
            fg=IKINCIL_YAZI
        )
        baslik.pack(pady=(18, 10))

        ekran_paneli = tk.Frame(
            pencere,
            bg=EKRAN_RENGI
        )
        ekran_paneli.pack(fill="x", padx=14, pady=(0, 12))

        self.ekran = tk.Entry(
            ekran_paneli,
            textvariable=self.ifade,
            font=("Arial", 23, "bold"),
            bg=EKRAN_RENGI,
            fg=YAZI_RENGI,
            insertbackground=YAZI_RENGI,
            justify="right",
            relief="flat",
            bd=0
        )
        self.ekran.pack(fill="x", padx=12, pady=18, ipady=10)
        self.ekran.bind("<Key>", self.klavye_tusu)
        self.ifade.trace_add(
            "write",
            lambda *args: self.ekran_yazi_boyutunu_ayarla()
        )

        yardimci = tk.Frame(pencere, bg=ARKA_PLAN)
        yardimci.pack(fill="x", padx=12, pady=(0, 5))

        self.buton_olustur(
            yardimci, "Temizle", self.temizle,
            PANEL, SILME_RENGI
        ).pack(side="left", expand=True, fill="x", padx=3)

        self.aci_butonu = self.buton_olustur(
            yardimci, self.aci_modu, self.aci_modunu_degistir,
            PANEL, "#00BFA5"
        )
        self.aci_butonu.pack(
            side="left", expand=True, fill="x", padx=3
        )

        self.buton_olustur(
            yardimci, "Sil ⌫", self.sil,
            PANEL, YAZI_RENGI
        ).pack(side="left", expand=True, fill="x", padx=3)

        self.buton_olustur(
            yardimci, "Geçmiş", self.gecmisi_goster,
            PANEL, YAZI_RENGI
        ).pack(side="left", expand=True, fill="x", padx=3)

        bellek_satiri = tk.Frame(pencere, bg=ARKA_PLAN)
        bellek_satiri.pack(fill="x", padx=12, pady=(0, 5))

        bellek_butonlari = [
            ("MC", self.bellek_temizle),
            ("MR", self.bellek_goster),
            ("M+", self.bellege_ekle),
            ("M−", self.bellekten_cikar)
        ]

        for metin, komut in bellek_butonlari:
            self.buton_olustur(
                bellek_satiri, metin, komut,
                PANEL, YAZI_RENGI
            ).pack(
                side="left",
                expand=True,
                fill="x",
                padx=3
            )

        mod_satiri = tk.Frame(pencere, bg=ARKA_PLAN)
        mod_satiri.pack(fill="x", padx=12, pady=(0, 5))

        self.mod_butonu = self.buton_olustur(
            mod_satiri,
            "Bilimsel Mod ▼",
            self.bilimsel_modunu_degistir,
            PANEL,
            "#00BFA5"
        )
        self.mod_butonu.pack(fill="x", padx=3)
            
        self.bilimsel_panel = tk.Frame(pencere, bg=ARKA_PLAN)
        self.bilimsel_panel.pack(fill="x")
        bilimsel_satir = tk.Frame(self.bilimsel_panel, bg=ARKA_PLAN)
        bilimsel_satir.pack(fill="x", padx=12, pady=(0, 5))

        bilimsel_butonlari = [
            ("π", "pi"),
            ("e", "e"),
            ("Ans", "Ans"),
            ("!", "!")
        ]

        for metin, deger in bilimsel_butonlari:
            self.buton_olustur(
                bilimsel_satir, metin,
                lambda x=deger: self.ifade_ekle(x),
                PANEL, "#00BFA5"
            ).pack(
                side="left",
                expand=True,
                fill="x",
                padx=3
            )

        trig_satiri = tk.Frame(self.bilimsel_panel, bg=ARKA_PLAN)
        trig_satiri.pack(fill="x", padx=12, pady=(0, 5))

        trig_butonlari = [
            ("sin", "sin("),
            ("cos", "cos("),
            ("tan", "tan("),
            ("cot", "cot("),
            ("√", "sqrt(")
        ]

        for metin, deger in trig_butonlari:
            self.buton_olustur(
                trig_satiri, metin,
                lambda x=deger: self.ifade_ekle(x),
                PANEL, "#00BFA5"
            ).pack(
                side="left",
                expand=True,
                fill="x",
                padx=3
            )

        ileri_satiri = tk.Frame(self.bilimsel_panel, bg=ARKA_PLAN)
        ileri_satiri.pack(fill="x", padx=12, pady=(0, 5))

        ileri_butonlari = [
            ("asin", "asin("),
            ("acos", "acos("),
            ("atan", "atan("),
            ("log", "log("),
            ("ln", "ln(")
        ]

        for metin, deger in ileri_butonlari:
            self.buton_olustur(
                ileri_satiri, metin,
                lambda x=deger: self.ifade_ekle(x),
                PANEL, "#00BFA5"
            ).pack(
                side="left",
                expand=True,
                fill="x",
                padx=3
            )

        kok_satiri = tk.Frame(self.bilimsel_panel, bg=ARKA_PLAN)
        kok_satiri.pack(fill="x", padx=12, pady=(0, 5))

        kok_butonlari = [
            ("∛", "cbrt("),
            ("n√", "kok("),
            ("|x|", "abs(")
        ]

        for metin, deger in kok_butonlari:
            self.buton_olustur(
                kok_satiri, metin,
                lambda x=deger: self.ifade_ekle(x),
                PANEL, "#00BFA5"
            ).pack(
                side="left",
                expand=True,
                fill="x",
                padx=3
            )

        butonlar = [
            ["7", "8", "9", "÷"],
            ["4", "5", "6", "×"],
            ["1", "2", "3", "−"],
            ["±", "0", ".", "+"],
            ["(", ")", "%", "xʸ"],
        ]

        for satir in butonlar:
            cerceve = tk.Frame(pencere, bg=ARKA_PLAN)
            if satir == butonlar[0]:
                self.ilk_sayi_satiri = cerceve
            cerceve.pack(
                expand=True,
                fill="both",
                padx=10,
                pady=2
            )

            for metin in satir:
                renk = SAYI_RENGI
                yazi = YAZI_RENGI

                if metin in ["÷", "×", "−", "+", "%", "(", ")", "xʸ"]:
                    renk = ISLEM_RENGI

                if metin == "xʸ":
                    komut = lambda: self.ifade_ekle("**")
                elif metin == "±":
                    komut = self.isareti_degistir
                else:
                    komut = lambda x=metin: self.buton_tikla(x)

                self.buton_olustur(
                    cerceve, metin, komut, renk, yazi
                ).pack(
                    side="left",
                    expand=True,
                    fill="both",
                    padx=3,
                    pady=3
                )

        alt_satir = tk.Frame(pencere, bg=ARKA_PLAN)
        alt_satir.pack(fill="x", padx=10, pady=(5, 12))

        self.buton_olustur(
            alt_satir, "Yeni İşlem", self.temizle,
            PANEL, YAZI_RENGI
        ).pack(side="left", expand=True, fill="both", padx=3, ipady=8)

        self.buton_olustur(
            alt_satir, "=  HESAPLA", self.sonucu_hesapla,
            ESITTIR_RENGI, "#FFFFFF"
        ).pack(side="left", expand=True, fill="both", padx=3, ipady=8)

        self.ekran.focus_set()

    def aci_modunu_degistir(self):
        if self.aci_modu == "DEG":
            self.aci_modu = "RAD"
        else:
            self.aci_modu = "DEG"

        self.aci_butonu.config(text=self.aci_modu)

    def buton_olustur(self, ebeveyn, metin, komut, arka_plan, yazi_rengi):
        buton = tk.Button(
            ebeveyn,
            text=metin,
            command=komut,
            font=("Arial", 12, "bold"),
            bg=arka_plan,
            fg=yazi_rengi,
            activebackground=VURGU_RENGI,
            activeforeground="#FFFFFF",
            relief="flat",
            bd=0,
            cursor="hand2"
        )

        buton.bind(
            "<Enter>",
            lambda olay: buton.config(bg=VURGU_RENGI)
        )

        buton.bind(
            "<Leave>",
            lambda olay: buton.config(bg=arka_plan)
        )

        return buton

    def ekran_yazi_boyutunu_ayarla(self, olay=None):
        uzunluk = len(self.ifade.get())

        if uzunluk <= 12:
            boyut = 23
        elif uzunluk <= 20:
            boyut = 19
        elif uzunluk <= 30:
            boyut = 15
        else:
            boyut = 12

        self.ekran.config(font=("Arial", boyut, "bold"))

    def ifade_ekle(self, metin):
        if self.sonuc_gosterildi:
            if metin[0].isdigit() or metin == ".":
                self.temizle()

            self.sonuc_gosterildi = False

        if self.ekran.selection_present():
            self.ekran.delete(tk.SEL_FIRST, tk.SEL_LAST)

        self.ekran.insert(tk.INSERT, metin)
        self.ekran.focus_set()

    def temizle(self):
        self.ifade.set("")
        self.sonuc_gosterildi = False

    def sil(self):
        if self.ekran.selection_present():
            self.ekran.delete(tk.SEL_FIRST, tk.SEL_LAST)
        else:
            imlec = self.ekran.index(tk.INSERT)

            if imlec > 0:
                self.ekran.delete(imlec - 1)

        self.ekran.focus_set()

    def isareti_degistir(self):
        mevcut = self.ifade.get()

        if not mevcut:
            self.ifade.set("-")
        elif mevcut.startswith("-"):
            self.ifade.set(mevcut[1:])
        else:
            self.ifade.set("-" + mevcut)

    def klavye_tusu(self, olay):
        if self.sonuc_gosterildi:
            if olay.char.isdigit() or olay.char == ".":
                self.temizle()
            self.sonuc_gosterildi = False

        if olay.keysym == "Return":
            self.sonucu_hesapla()
            return "break"

        elif olay.keysym == "Escape":
            self.temizle()
            return "break"

        elif olay.keysym == "BackSpace":
            self.sil()
            return "break"

        elif olay.keysym == "Delete":
            self.sil()
            return "break"

        elif olay.char == "^":
            self.ekran.insert(tk.INSERT, "**")
            return "break"

    def buton_tikla(self, tus):
        donusum = {
            "÷": "/",
            "×": "*",
            "−": "-",
            "π": "pi"
        }

        self.ifade_ekle(donusum.get(tus, tus))


    def gecmisi_goster(self):
        pencere = tk.Toplevel(self.pencere)
        pencere.title("İşlem Geçmişi")
        pencere.geometry("400x450")
        pencere.update_idletasks()
        ana_x = self.pencere.winfo_rootx()
        ana_y = self.pencere.winfo_rooty()
        ana_genislik = self.pencere.winfo_width()
        ana_yukseklik = self.pencere.winfo_height()
        x = ana_x + (ana_genislik - 400) // 2
        y = ana_y + (ana_yukseklik - 450) // 2
        pencere.geometry(f"400x450+{x}+{y}")
        pencere.transient(self.pencere)
        pencere.grab_set()
        pencere.focus_set()
        pencere.configure(bg="#1e1e1e")
        pencere.resizable(False, False)

        baslik = tk.Label(
            pencere,
            text="İŞLEM GEÇMİŞİ",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="white"
        )
        baslik.pack(pady=15)

        liste = tk.Listbox(
            pencere,
            font=("Arial", 12),
            bg="#2d2d2d",
            fg="white",
            selectbackground="#007acc",
            selectforeground="white",
            width=40,
            height=15
        )
        liste.pack(padx=15, pady=10, fill="both", expand=True)

        for kayit in reversed(self.gecmis):
            liste.insert(tk.END, kayit)

        def gecmisi_temizle():
            cevap = messagebox.askyesno(
                "Geçmişi Temizle",
                "Tüm işlem geçmişini silmek istediğinize emin misiniz?",
                parent=pencere
            )

            if cevap:
                self.gecmis.clear()
                liste.delete(0, tk.END)

                if cevap:
                    self.gecmis.clear()
                    liste.delete(0, tk.END)

        def islemi_tekrar_kullan(olay=None):
            secim = liste.curselection()

            if not secim:
                messagebox.showwarning(
                    "Uyarı",
                    "Lütfen listeden bir işlem seçin.",
                    parent=pencere
                )
                return

            kayit = liste.get(secim[0])
            ifade = kayit.partition(" = ")[0]

            self.ekran.delete(0, tk.END)
            self.ekran.insert(0, ifade)
            self.sonuc_gosterildi = False

            pencere.destroy()

        liste.bind("<Double-Button-1>", islemi_tekrar_kullan)
        liste.bind("<Return>", islemi_tekrar_kullan)
        liste.bind("<Escape>", lambda olay: pencere.destroy())

        kullan_butonu = tk.Button(
            pencere,
            text="Seçili İşlemi Kullan",
            font=("Arial", 11, "bold"),
            bg="#007acc",
            fg="white",
            command=islemi_tekrar_kullan
        )
        kullan_butonu.pack(pady=10)

        temizle_butonu = tk.Button(
            pencere,
            text="Geçmişi Temizle",
            font=("Arial", 11, "bold"),
            bg="#c0392b",
            fg="white",
            command=gecmisi_temizle
        )
        temizle_butonu.pack(pady=5)

    def sonucu_hesapla(self):
        ifade = self.ifade.get().strip()

        if not ifade:
            return

        try:
            sonuc = hesapla(ifade, self.aci_modu, self.ans)
            self.ans = sonuc
            
            kayit = f"{ifade} = {sonuc}"
            self.gecmis.append(kayit)
            self.ifade.set(str(sonuc))
            self.sonuc_gosterildi = True

        except ZeroDivisionError:
            messagebox.showerror(
                "Hata",
                "Bir sayı sıfıra bölünemez.",
                parent=self.pencere
            )

        except (ValueError, SyntaxError, TypeError, OverflowError):
            messagebox.showerror(
                "Hata",
                "Geçersiz işlem girdiniz.",
                parent=self.pencere
            )

    def bilimsel_modunu_degistir(self):
        if self.bilimsel_modu:
            self.bilimsel_panel.pack_forget()
            self.bilimsel_modu = False
            self.mod_butonu.config(text="Bilimsel Mod ▲")
        else:
            self.bilimsel_panel.pack(
                before=self.ilk_sayi_satiri,
                fill="x"
            )
            self.bilimsel_modu = True
            self.mod_butonu.config(text="Bilimsel Mod ▼")

    def bellek_temizle(self):
        self.bellek = 0


    def bellek_goster(self):
        self.ifade_ekle(str(self.bellek))


    def bellege_ekle(self):
        ifade = self.ifade.get().strip()

        if not ifade:
            return

        try:
            sonuc = hesapla(ifade, self.aci_modu, self.ans)
            self.bellek += sonuc

        except (ValueError, SyntaxError, TypeError, OverflowError, ZeroDivisionError):
            messagebox.showerror(
                "Hata",
                "Hafızaya eklemek için geçerli bir işlem girin.",
                parent=self.pencere
            )


    def bellekten_cikar(self):
        ifade = self.ifade.get().strip()

        if not ifade:
            return

        try:
            sonuc = hesapla(ifade, self.aci_modu, self.ans)
            self.bellek -= sonuc

        except (ValueError, SyntaxError, TypeError, OverflowError, ZeroDivisionError):
            messagebox.showerror(
                "Hata",
                "Hafızadan çıkarmak için geçerli bir işlem girin.",
                parent=self.pencere
            )

pencere = tk.Tk()
uygulama = HesapMakinesi(pencere)
pencere.mainloop()

