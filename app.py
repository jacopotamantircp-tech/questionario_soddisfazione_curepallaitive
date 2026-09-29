import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configurazione della pagina
st.set_page_config(
    page_title="Monitoraggio Clima Organizzativo - Cure Palliative",
    page_icon="🏥",
    layout="centered"
)

# Inizializzazione dello stato della sessione per la navigazione a schermate
if 'step' not in st.session_state:
    st.session_state.step = 0

# Dizionario delle etichette della scala Likert
likert_options = {
    1: "1 - Fortemente in disaccordo",
    2: "2 - In disaccordo",
    3: "3 - Neutro / Indeciso",
    4: "4 - In accordo",
    5: "5 - Fortemente in accordo"
}

def get_likert_index(val):
    # Converte il valore salvato nell'indice della selectbox (default 2 -> Neutro)
    return val - 1

# SCHERMATA 0: Presentazione e istruzioni
if st.session_state.step == 0:
    st.title("🏥 Unità Operativa Complessa Rete delle Cure Palliative")
    st.subheader("UA Cure Palliative Adulto – Monitoraggio del Clima Organizzativo e del Benessere")
    
    st.markdown("""
    <div style="background-color: #F9F9F9; padding: 20px; border-radius: 5px; border: 1px solid #E0E0E0;">
    <p><b>Gentile Collega,</b></p>
    <p>Il presente questionario si inserisce all'interno di un programma di monitoraggio e miglioramento del clima organizzativo e della qualità della vita lavorativa della nostra Rete di Cure Palliative. La compilazione è <b>strettamente anonima</b> e i dati saranno trattati unicamente in forma aggregata. Le vostre risposte sono uno strumento fondamentale per valorizzare il benessere del personale e orientare azioni di supporto mirate[cite: 1, 2].</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Legenda della Scala Likert a 5 punti:")
    st.markdown("""
    * **1** = Fortemente in disaccordo[cite: 1, 2]
    * **2** = In disaccordo[cite: 1, 2]
    * **3** = Neutro / Indeciso[cite: 1, 2]
    * **4** = In accordo[cite: 1, 2]
    * **5** = Fortemente in accordo[cite: 1, 2]
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Inizia il Questionario ➔", type="primary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# SCHERMATA 1: Area 1
elif st.session_state.step == 1:
    st.progress(0.2, text="Area 1 di 5: Soddisfazione Lavorativa")
    st.header("📂 AREA 1: Soddisfazione Lavorativa e Realizzazione Professionale")
    
    if 'q1_1' not in st.session_state: st.session_state.q1_1 = 3
    if 'q1_2' not in st.session_state: st.session_state.q1_2 = 3

    st.markdown("**1. Nel complesso, trovo che il mio lavoro quotidiano in Cure Palliative mantenga un profondo significato e valore per la mia crescita professionale[cite: 1, 2].**")
    st.session_state.q1_1 = st.radio(
        "Scelta Area 1.1", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_options[x],
        index=get_likert_index(st.session_state.q1_1), horizontal=True, label_visibility="collapsed", key="radio_1_1"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**2. Sento che le mie competenze specifiche e il mio contributo clinico sono adeguatamente riconosciuti dall'équipe e dalla direzione[cite: 1, 2].**")
    st.session_state.q1_2 = st.radio(
        "Scelta Area 1.2", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_options[x],
        index=get_likert_index(st.session_state.q1_2), horizontal=True, label_visibility="collapsed", key="radio_1_2"
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 0
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            st.session_state.step = 2
            st.rerun()

# SCHERMATA 2: Area 2
elif st.session_state.step == 2:
    st.progress(0.4, text="Area 2 di 5: Clima Organizzativo")
    st.header("📂 AREA 2: Clima Organizzativo e Dinamiche d'Équipe")

    for i in range(1, 6):
        if f'q2_{i}' not in st.session_state: st.session_state[f'q2_{i}'] = 3

    questions_area2 = [
        "All'interno della nostra Unità Operativa esiste un clima di reciproco supporto, fiducia e collaborazione aperta tra medici e infermieri[cite: 1, 2].",
        "I carichi di lavoro, la turnazione e la gestione delle risorse umane/strutturali sono organizzati in modo equo e sostenibile[cite: 1, 2].",
        "I momenti di debriefing e di confronto multiprofessionale (es. riunioni d'équipe o supporto psicologico) sono sufficienti e utili per affrontare i casi complessi[cite: 1, 2].",
        "La nostra unità promuove attivamente la parità di genere, garantendo uguali opportunità di crescita, rispetto e valorizzazione professionale indipendentemente dal genere[cite: 1, 2].",
        "L’ambiente lavorativo è sicuro e rispettoso delle differenze individuali, garantendo un clima di piena accettazione e tutela rispetto all’orientamento sessuale e all’identità di persona[cite: 1, 2]."
    ]

    for idx, q_text in enumerate(questions_area2, 1):
        st.markdown(f"**{idx}. {q_text}**")
        st.session_state[f'q2_{idx}'] = st.radio(
            f"Scelta Area 2.{idx}", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_options[x],
            index=get_likert_index(st.session_state[f'q2_{idx}']), horizontal=True, label_visibility="collapsed", key=f"radio_2_{idx}"
        )
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            st.session_state.step = 3
            st.rerun()

# SCHERMATA 3: Area 3
elif st.session_state.step == 3:
    st.progress(0.6, text="Area 3 di 5: Distress Personale")
    st.header("📂 AREA 3: Distress Personale e Carico Emotivo")

    for i in range(1, 4):
        if f'q3_{i}' not in st.session_state: st.session_state[f'q3_{i}'] = 3

    questions_area3 = [
        "Avverto un livello di esaurimento emotivo e fisico legato alla gestione quotidiana della sofferenza e del fine vita che compromette il mio benessere[cite: 1, 2].",
        "Mi accorgo di portare a casa un peso emotivo significativo derivante dalle dinamiche lavorative, che fatica a dissolversi nel tempo libero[cite: 1, 2].",
        "Sento di avere a disposizione adeguate strategie personali o istituzionali per gestire lo stress acuto e il rischio di compassion fatigue[cite: 1, 2]."
    ]

    for idx, q_text in enumerate(questions_area3, 1):
        st.markdown(f"**{idx}. {q_text}**")
        st.session_state[f'q3_{idx}'] = st.radio(
            f"Scelta Area 3.{idx}", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_options[x],
            index=get_likert_index(st.session_state[f'q3_{idx}']), horizontal=True, label_visibility="collapsed", key=f"radio_3_{idx}"
        )
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            st.session_state.step = 4
            st.rerun()

# SCHERMATA 4: Area 4
elif st.session_state.step == 4:
    st.progress(0.8, text="Area 4 di 5: Autonomia e Supporto Etico")
    st.header("📂 AREA 4: Autonomia, Decision Making e Supporto Etico")

    for i in range(1, 3):
        if f'q4_{i}' not in st.session_state: st.session_state[f'q4_{i}'] = 3

    questions_area4 = [
        "Nei casi clinici complessi (es. ostinazione terapeutica, decisioni di fine vita), sento di poter esprimere liberamente il mio parere e di essere supportato nelle scelte etiche[cite: 1, 2].",
        "Posso contare su chiare linee guida operative e su percorsi condivisi che riducono l'incertezza nella presa in carico del paziente e della famiglia[cite: 1, 2]."
    ]

    for idx, q_text in enumerate(questions_area4, 1):
        st.markdown(f"**{idx}. {q_text}**")
        st.session_state[f'q4_{idx}'] = st.radio(
            f"Scelta Area 4.{idx}", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_options[x],
            index=get_likert_index(st.session_state[f'q4_{idx}']), horizontal=True, label_visibility="collapsed", key=f"radio_4_{idx}"
        )
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            st.session_state.step = 5
            st.rerun()

# SCHERMATA 5: Area 5 e Invio
elif st.session_state.step == 5:
    st.progress(1.0, text="Area 5 di 5: Sviluppo Professionale")
    st.header("📂 AREA 5: Sviluppo Professionale e Prospettive Future")

    for i in range(1, 3):
        if f'q5_{i}' not in st.session_state: st.session_state[f'q5_{i}'] = 3

    questions_area5 = [
        "L'azienda/struttura offre adeguate opportunità di formazione continua e aggiornamento specifico in cure palliative[cite: 1, 2].",
        "Alla luce delle condizioni attuali, rifletterei positivamente sulla scelta di continuare a lavorare a lungo termine in questo specifico ambito assistenziale[cite: 1, 2]."
    ]

    for idx, q_text in enumerate(questions_area5, 1):
        st.markdown(f"**{idx}. {q_text}**")
        st.session_state[f'q5_{idx}'] = st.radio(
            f"Scelta Area 5.{idx}", options=[1, 2, 3, 4, 5], format_func=lambda x: likert_options[x],
            index=get_likert_index(st.session_state[f'q5_{idx}']), horizontal=True, label_visibility="collapsed", key=f"radio_5_{idx}"
        )
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("Invia Risposte in Modo Anonimo 🚀", type="primary"):
            st.session_state.step = 6
            st.rerun()

# SCHERMATA 6: Conferma e Cruscotto di Analisi / Grafico a Radar
elif st.session_state.step == 6:
    st.success("✅ Grazie per la collaborazione! Il questionario è stato registrato con successo in forma anonima[cite: 1, 2].")
    
    st.markdown("---")
    st.markdown("### 📈 Cruscotto di Sintesi (Analisi di Reparto)")
    st.markdown("*Ecco la visualizzazione sintetica dei punteggi medi per area calcolati in base alle risposte inserite:*")

    # Calcolo delle medie per area (invertendo opportunamente l'Area 3 del distress affinché 5 significhi benessere positivo)
    score_area1 = np.mean([st.session_state.q1_1, st.session_state.q1_2])
    score_area2 = np.mean([st.session_state.q2_1, st.session_state.q2_2, st.session_state.q2_3, st.session_state.q2_4, st.session_state.q2_5])
    # Per il distress (Area 3), un punteggio alto di accordo indica disagio, quindi invertiamo la scala (6 - valore) per coerenza grafica positiva
    score_area3 = np.mean([6 - st.session_state.q3_1, 6 - st.session_state.q3_2, 6 - st.session_state.q3_3])
    score_area4 = np.mean([st.session_state.q4_1, st.session_state.q4_2])
    score_area5 = np.mean([st.session_state.q5_1, st.session_state.q5_2])

    df_radar = pd.DataFrame(dict(
        Punteggio=[score_area1, score_area2, score_area3, score_area4, score_area5],
        Area=[
            "1. Soddisfazione Prof.",
            "2. Clima & Team",
            "3. Benessere/No Distress",
            "4. Autonomia ed Etica",
            "5. Futuro e Formazione"
        ]
    ))

    fig = px.line_polar(df_radar, r='Punteggio', theta='Area', line_close=True, range_r=[0, 5])
    fig.update_traces(fill='toself', line_color='#1F4E78')
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
    
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Compila un nuovo questionario"):
        # Reset delle schermate
        st.session_state.step = 0
        st.rerun()
