_UNITS = ["","satu","dua","tiga","empat","lima","enam","tujuh","delapan","sembilan","sepuluh","sebelas"]

def terbilang_indonesia(n):
    try:
        n = int(n)
    except Exception:
        return ""
    if n < 0:
        return "minus " + terbilang_indonesia(-n)
    if n < 12:
        return _UNITS[n]
    if n < 20:
        return terbilang_indonesia(n-10) + " belas"
    if n < 100:
        q, r = divmod(n, 10)
        s = terbilang_indonesia(q) + " puluh"
        if r:
            s += " " + terbilang_indonesia(r)
        return s
    if n < 200:
        return "seratus " + (terbilang_indonesia(n-100) if n>100 else "")
    if n < 1000:
        q, r = divmod(n, 100)
        s = terbilang_indonesia(q) + " ratus"
        if r:
            s += " " + terbilang_indonesia(r)
        return s
    if n < 2000:
        return "seribu " + (terbilang_indonesia(n-1000) if n>1000 else "")
    if n < 1000000:
        q, r = divmod(n, 1000)
        s = terbilang_indonesia(q) + " ribu"
        if r:
            s += " " + terbilang_indonesia(r)
        return s
    if n < 1000000000:
        q, r = divmod(n, 1000000)
        s = terbilang_indonesia(q) + " juta"
        if r:
            s += " " + terbilang_indonesia(r)
        return s
    return "Angka terlalu besar"
