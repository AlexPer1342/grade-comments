# 🎓 Komentarų ir pažymių generatorius prie mokinio darbo

Ši Streamlit aplikacija padeda mokytojams automatiškai sugeneruoti komentarus ir pažymius remiantis mokinių surinktais taškais.

## ✅ Funkcionalumas

- Įvertinimo komentarai generuojami pagal šabloną:
  > Surinko ... balų iš ... Teisingai atliko ...% užduočių. Pasiekimų lygis - ...
- Pridedamas papildomas komentaras, jei pasiekimų lygis yra **nepatenkinamas**.
- Galima:
  - Įvesti duomenis rankiniu būdu
  - Įkelti vieną ar kelis Excel failus
- Galima atsisiųsti papildytus failus su stulpeliais **„Pažymis“** ir **„Komentaras“**
- Mėlynos minimalistinės sąsajos dizainas

## 📁 Failo struktūra

Įkeltame Excel faile turi būti šie stulpeliai:

| Mokinio vardas pavardė | Max taškų skaičius | Surinko |
|------------------------|--------------------|---------|
| Vardenis Pavardenis    | 20                 | 15      |

## 🧮 Pažymio skaičiavimas

Pažymys apskaičiuojamas pagal 10 balų sistemą:

- Procentai = (Surinko / Max taškų skaičius) * 100
- Pažymys = Procentai / 10, apvalinant (1,5 → 2; 1,4 → 1)

### Pasiekimų lygiai

| Pažymys | Lygis         |
|--------|---------------|
| 9-10   | aukštesnysis  |
| 7-8    | pagrindinis   |
| 5-6    | patenkinamas  |
| 4      | slenkstinis   |
| 1-3    | nepatenkinamas |

## 🚀 Paleidimas

```bash
pip install -r requirements.txt
streamlit run app.py
