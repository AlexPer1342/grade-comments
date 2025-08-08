import streamlit as st
import pandas as pd
import io
from streamlit import markdown

# Apply blue-themed CSS styling
st.markdown(
    """
    <style>
    /* Bendras fonas */
    .stApp {
        background-color: #f0f8ff;
    }

    /* Antraštės spalva */
    h1, h2, h3, .st-emotion-cache-10trblm {
        color: #1e3a8a;
    }

    /* Mygtukai */
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border: none;
        padding: 0.5em 1em;
        border-radius: 5px;
    }

    .stButton>button:hover {
        background-color: #2563eb;
    }

    /* Įvesties laukeliai */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border: 1px solid #3b82f6;
        border-radius: 4px;
    }

    .stRadio>div>label {
        color: #1e3a8a;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def generuoti_komentara_ir_pazymi(surinko, max_tasku):
    if max_tasku == 0:
        return "Nenurodyta maksimali taškų suma", 0

    procentai = round((surinko / max_tasku) * 100)
    # Apvalinimas į 10 balų sistemą (1,5 -> 2; 1,4 -> 1)
    pazymis = int((procentai / 10) + 0.5)

    if pazymis >= 9:
        lygis = "aukštesnysis"
    elif pazymis >= 7:
        lygis = "pagrindinis"
    elif pazymis >= 5:
        lygis = "patenkinamas"
    elif pazymis == 4:
        lygis = "slenkstinis"
    else:
        lygis = "nepatenkinamas"

    komentaras = f"Surinko {surinko} balų iš {max_tasku}. Teisingai atliko {procentai}% užduočių. Pasiekimų lygis - {lygis}."

    if lygis == "nepatenkinamas":
        komentaras += " Darbą reikia perlaikyti su mokytoju sutartu laiku. Mokytojų konsultacijų grafikas skelbiamas mokyklos stende ir internetinėje svetainėje."

    return komentaras, pazymis


def rankinis_ivedimas():
    st.subheader("📝 Rankinis įvedimas")

    mokinys = st.text_input("Mokinio vardas ir pavardė")
    max_tasku = st.number_input("Maksimalus taškų skaičius", min_value=1, value=10)
    surinko = st.number_input("Mokinys surinko taškų", min_value=0, value=0)

    if st.button("Generuoti komentarą ir pažymį"):
        komentaras, pazymis = generuoti_komentara_ir_pazymi(surinko, max_tasku)
        st.success(f"Pažymys: {pazymis}\nKomentaras: {komentaras}")


def failo_ikelimas():
    st.subheader("📁 Įkelti Excel failus")

    failai = st.file_uploader("Pasirinkite vieną ar kelis Excel failus", type=["xlsx"], accept_multiple_files=True)

    if failai:
        for failas in failai:
            st.markdown(f"**📄 Apdorojamas failas:** `{failas.name}`")
            df = pd.read_excel(failas)

            if set(['Surinko', 'Max taškų skaičius']).issubset(df.columns):
                df[['Komentaras', 'Pažymis']] = df.apply(
                    lambda row: pd.Series(generuoti_komentara_ir_pazymi(row['Surinko'], row['Max taškų skaičius'])),
                    axis=1)
                st.success(f"Komentarai ir pažymiai sėkmingai sugeneruoti faile: {failas.name}")
                st.dataframe(df)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    df.to_excel(writer, index=False)
                st.download_button("📥 Atsisiųsti su komentarais ir pažymiais", data=output.getvalue(),
                                   file_name=f"komentarai_{failas.name}")
            else:
                st.error(f"Faile `{failas.name}` trūksta būtinų stulpelių: 'Surinko', 'Max taškų skaičius'")
    st.subheader("📁 Įkelti Excel failą")

    df = pd.read_excel(failas)

    if set(['Surinko', 'Max taškų skaičius']).issubset(df.columns):
        df[['Komentaras', 'Pažymis']] = df.apply(
            lambda row: pd.Series(generuoti_komentara_ir_pazymi(row['Surinko'], row['Max taškų skaičius'])), axis=1)
        st.success("Komentarai ir pažymiai sėkmingai sugeneruoti!")
        st.dataframe(df)

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        st.download_button("📥 Atsisiųsti su komentarais ir pažymiais", data=output.getvalue(),
                           file_name="komentarai.xlsx")
    else:
        st.error("Trūksta būtinų stulpelių: 'Surinko', 'Max taškų skaičius'")


st.title("🎓 Komentarų ir pažymių generatorius prie mokinio darbo")
st.write("Pasirinkite įvedimo būdą:")

budas = st.radio("", ["Rankinis įvedimas", "Failo įkėlimas"])

if budas == "Rankinis įvedimas":
    rankinis_ivedimas()
else:
    failo_ikelimas()
