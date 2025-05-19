import re
from itertools import product


def benutzerwahl():
    print("Formelquelle wählen:")
    print("1 = hartcodierte Formel")
    print("2 = Formel aus Datei (formel.txt)")
    wahl = input("Deine Wahl (1 oder 2): ").strip()
    return wahl


def evaluiere_hartcodiert(X):
    # Beispiel: X[1] and (X[2] or (not X[3] and X[0]))
    return X[1] and (X[2] or (not X[3] and X[0]))

def wahrheitswerte_hartcodiert(n):
    for bits in product([False, True], repeat=n):
        if evaluiere_hartcodiert(bits):
            return bits
    return None


def lade_formel_aus_datei(pfad="formel.txt"):
    try:
        with open(pfad, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"❌ Datei '{pfad}' nicht gefunden.")
        return None

def finde_variablen(formel):
    return sorted(set(int(x[1:]) for x in re.findall(r'X\d+', formel)))

def evaluiere_dynamisch(formel, belegung):
    ersetzte_formel = (
        formel.replace('-', ' not ')
              .replace('&', ' and ')
              .replace('|', ' or ')
    )
    for i, val in belegung.items():
        ersetzte_formel = ersetzte_formel.replace(f'X{i}', str(val))
    try:
        return eval(ersetzte_formel)
    except Exception as e:
        print("❌ Fehler beim Auswerten:", e)
        return False

def wahrheitswerte_datei(formel):
    variablen = finde_variablen(formel)
    max_index = max(variablen)
    for bits in product([False, True], repeat=max_index + 1):
        belegung = {i: bits[i] for i in variablen}
        if evaluiere_dynamisch(formel, belegung):
            return belegung
    return None


if __name__ == "__main__":
    wahl = benutzerwahl()

    if wahl == "1":
        print("Verwende hartcodierte Formel: X[1] and (X[2] or (not X[3] and X[0]))")
        modell = wahrheitswerte_hartcodiert(4)
        if modell:
            print("Erfüllende Belegung gefunden:", modell)
        else:
            print("❌ Formel ist unerfüllbar.")

    elif wahl == "2":
        formel = lade_formel_aus_datei()
        if formel:
            print("Eingelesene Formel:", formel)
            modell = wahrheitswerte_datei(formel)
            if modell:
                print("Erfüllende Belegung gefunden:")
                for var, val in sorted(modell.items()):
                    print(f"X{var} = {val}")
            else:
                print("❌ Formel ist unerfüllbar.")
    else:
        print("Ungültige Eingabe. Bitte 1 oder 2 eingeben.")
