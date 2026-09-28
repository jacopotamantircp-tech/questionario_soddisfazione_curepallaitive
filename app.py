import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import os

st.set_page_config(
    page_title="Monitoraggio Benessere - Cure Palliative",
    page_icon="🏥",
    layout="centered"
)

# File to store responses locally
DATA_FILE = "risposte_questionario.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    else:
        # Create empty DataFrame with expected columns
        columns = [
            "Timestamp", "Profilo",
            "A1_Q1", "A1_Q2",
            "A2_Q3", "A2_Q4", "A2_Q5", "A2_Q6", "A2_Q7",
            "A3_Q8", "A3_Q9", "A3_Q10",
            "A4_Q11", "A4_Q12",
            "A5_Q13", "A5_Q14",
            "Media_Area_1", "Media_Area_2", "Media_Area_3_Inv", "Media_Area_4", "Media_Area_5", "Indice_Globale"
        ]
        return pd.DataFrame(columns=columns)

def save_response(data_dict):
    df = load_data()
    new_row = pd.DataFrame([data_dict])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

st.title("🏥 Rete di Cure Palliative — UA Palliative Adulto")
st.subheader("Monitoraggio della Soddisfazione, del Clima Organizzativo e del Benessere del Personale")

# Sidebar navigation
page = st.sidebar.selectbox("Navigazione", ["Compila Questionario", "Dashboard Risultati (Area Riservata)"])

if page == "Compila Questionario":
    st.markdown("---")
    st.markdown("""
    **Gentile Collega,**  
    Il presente questionario si inserisce all'interno di un programma di monitoraggio e miglioramento del clima organizzativo e della qualità della vita lavorativa della nostra Rete di Cure Palliative. La compilazione è **completamente anonima** e i dati saranno trattati in forma aggregata.
    
    *Scala di risposta:* **1 = Fortemente in disaccordo** | **2 = In disaccordo** | **3 = Neutro / Indeciso** | **4 = In accordo** | **5 = Fortemente in accordo**
    """)
    st.markdown("---")
    
    with st.form("questionario_form"):
        st.markdown("### Profilo Professionale")
        profilo = st.selectbox("Seleziona il tuo profilo:", ["Medico", "Infermiere", "Altro professionista sanitario"])
        
        st.markdown("---")
        st.markdown("### AREA 1: Soddisfazione Lavorativa e Realizzazione Professionale")
        q1 = st.slider("1. Nel complesso, trovo che il mio lavoro quotidiano in Cure Palliative mantenga un profondo significato e valore per la mia crescita professionale.", 1, 5, 3)
        q2 = st.slider("2. Sento che le mie competenze specifiche e il mio contributo clinico sono adeguatamente riconosciuti dall'équipe e dalla direzione.", 1, 5, 3)
        
        st.markdown("---")
        st.markdown("### AREA 2: Clima Organizzativo e Dinamiche d'Équipe")
        q3 = st.slider("3. All'interno della nostra Unità Operativa esiste un clima di reciproco supporto, fiducia e collaborazione aperta tra medici e infermieri.", 1, 5, 3)
        q4 = st.slider("4. I carichi di lavoro, la turnazione e la gestione delle risorse umane/strutturali sono organizzati in modo equo e sostenibile.", 1, 5, 3)
        q5 = st.slider("5. I momenti di debriefing e di confronto multiprofessionale (es. riunioni d'équipe o supporto psicologico) sono sufficienti e utili per affrontare i casi complessi.", 1, 5, 3)
        q6 = st.slider("6. La nostra unità promuove attivamente la parità di genere, garantendo uguali opportunità di crescita, rispetto e valorizzazione professionale indipendentemente dal genere.", 1, 5, 3)
        q7 = st.slider("7. L’ambiente lavorativo è sicuro e rispettoso delle differenze individuali, garantendo un clima di piena accettazione e tutela rispetto all’orientamento sessuale e all’identità di persona.", 1, 5, 3)
        
        st.markdown("---")
        st.markdown("### AREA 3: Distress Personale e Carico Emotivo")
        q8 = st.slider("8. Avverto un livello di esaurimento emotivo e fisico legato alla gestione quotidiana della sofferenza e del fine vita che compromette il mio benessere. *(Item di distress)*", 1, 5, 3)
        q9 = st.slider("9. Mi accorgo di portare a casa un peso emotivo significativo derivante dalle dinamiche lavorative, che fatica a dissolversi nel tempo libero. *(Item di distress)*", 1, 5, 3)
        q10 = st.slider("10. Sento di avere a disposizione adeguate strategie personali o istituzionali per gestire lo stress acuto e il rischio di compassion fatigue.", 1, 5, 3)
        
        st.markdown("---")
        st.markdown("### AREA 4: Autonomia, Decision Making e Supporto Etico")
        q11 = st.slider("11. Nei casi clinici complessi (es. ostinazione terapeutica, decisioni di fine vita), sento di poter esprimere liberamente il mio parere e di essere supportato nelle scelte etiche.", 1, 5, 3)
        q12 = st.slider("12. Posso contare su chiare linee guida operative e su percorsi condivisi che riducono l'incertezza nella presa in carico del paziente e della famiglia.", 1, 5, 3)
        
        st.markdown("---")
        st.markdown("### AREA 5: Sviluppo Professionale e Prospettive Future")
        q13 = st.slider("13. L'azienda/struttura offre adeguate opportunità di formazione continua e aggiornamento specifico in cure palliative.", 1, 5, 3)
        q14 = st.slider("14. Alla luce delle condizioni attuali, rifletterei positivamente sulla scelta di continuare a lavorare a lungo termine in questo specifico ambito assistenziale.", 1, 5, 3)
        
        submitted = st.form_submit_button("Invia Risposte")
        
        if submitted:
            # Calculate means (Area 3 questions 8 & 9 are inverted: 6 - val)
            m_a1 = np.mean([q1, q2])
            m_a2 = np.mean([q3, q4, q5, q6, q7])
            m_a3 = np.mean([(6 - q8), (6 - q9), q10])
            m_a4 = np.mean([q11, q12])
            m_a5 = np.mean([q13, q14])
            m_glob = np.mean([m_a1, m_a2, m_a3, m_a4, m_a5])
            
            response_data = {
                "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Profilo": profilo,
                "A1_Q1": q1, "A1_Q2": q2,
                "A2_Q3": q3, "A2_Q4": q4, "A2_Q5": q5, "A2_Q6": q6, "A2_Q7": q7,
                "A3_Q8": q8, "A3_Q9": q9, "A3_Q10": q10,
                "A4_Q11": q11, "A4_Q12": q12,
                "A5_Q13": q13, "A5_Q14": q14,
                "Media_Area_1": round(m_a1, 2),
                "Media_Area_2": round(m_a2, 2),
                "Media_Area_3_Inv": round(m_a3, 2),
                "Media_Area_4": round(m_a4, 2),
                "Media_Area_5": round(m_a5, 2),
                "Indice_Globale": round(m_glob, 2)
            }
            
            save_response(response_data)
            st.success("✅ Risposte inviate con successo! Grazie per il tuo prezioso contributo.")

elif page == "Dashboard Risultati (Area Riservata)":
    st.markdown("---")
    st.markdown("### 📊 Dashboard di Sintesi e Analisi dei Risultati")
    
    df = load_data()
    
    if df.empty:
        st.info("Nessuna risposta registrata al momento. Compila il questionario dalla sezione precedente per visualizzare i dati.")
    else:
        st.metric(label="Totale Compilazioni Raccolte", value=len(df))
        
        # Calculate average scores across all responses
        avg_scores = {
            "Soddisfazione Lavorativa": df["Media_Area_1"].mean(),
            "Clima Organizzativo": df["Media_Area_2"].mean(),
            "Distress (Invertito)": df["Media_Area_3_Inv"].mean(),
            "Autonomia ed Etica": df["Media_Area_4"].mean(),
            "Sviluppo Professionale": df["Media_Area_5"].mean()
        }
        
        radar_df = pd.DataFrame(dict(
            r=list(avg_scores.values()),
            theta=list(avg_scores.keys())
        ))
        
        fig = px.line_polar(radar_df, r='r', theta='theta', line_close=True, range_r=[1, 5])
        fig.update_traces(fill='toself', line_color='#1F4E78')
        fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[1, 5])), showlegend=False)
        
        st.markdown("#### Grafico a Radar - Medie per Macro-Area")
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Tabella Punteggi Medi d'Area")
        summary_table = pd.DataFrame(list(avg_scores.items()), columns=["Macro-Area", "Media Punteggio (1-5)"])
        summary_table["Media Punteggio (1-5)"] = summary_table["Media Punteggio (1-5)"].round(2)
        st.dataframe(summary_table, use_container_width=True)
        
        st.markdown("#### Esportazione Dati")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Scarica il Dataset Completo in formato CSV/Excel",
            data=csv,
            file_name="report_monitoraggio_palliative.csv",
            mime="text/csv"
        )
