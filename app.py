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

# CSS avanzato per blindare i radio button in orizzontale su un'unica riga e compattare le etichette
st.markdown("""
<style>
    /* Forza il contenitore dei radio button a disposizione orizzontale */
    div.stRadio > div[role='radiogroup'] {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: stretch;
        width: 100%;
    }
    /* Ogni opzione radio occupa una quota uguale e ha margini ridotti */
    div.stRadio > div[role='radiogroup'] > label {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        border-radius: 6px;
        padding: 6px 4px;
        text-align: center;
        flex: 1 1 0px;
        margin: 0 3px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start;
    }
    /* Riduce la dimensione del testo della descrizione sotto al numero */
    div.stRadio > div[role='radiogroup'] > label p {
        font-size: 10px !important;
        color: #555555;
        margin-top: 2px;
        line-height: 1.1;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Inizializzazione dello stato della sessione per la navigazione a schermate
if 'step' not in st.session_state:
    st.session_state.step = 0

# Opzioni della scala Likert con descrizioni brevi per mantenere la riga perfetta
likert_labels = {
    1: "1<br>Fortemente in disaccordo",
    2: "2<br>In disaccordo",
    3: "3<br>Neutro / Indeciso",
    4: "4<br>In accordo",
    5: "5<br>Fortemente in accordo"
}

# SCHERMATA 0: Presentazione e istruzioni
if st.session_state.step == 0:
    st.title("UNITÀ OPERATIVA COMPLESA RETE DELLE CURE PALLIATIVE")
    st.subheader("UA Cure Palliative Adulto – Monitoraggio del Clima Organizzativo e del Benessere")
    
    st.markdown("""
    <div style="background-color: #F9F9F9; padding: 20px; border-radius: 5px; border: 1px solid #E0E0E0;">
    <p><b>Gentile Collega,</b></p>
    <p>Il presente questionario si inserisce all'interno di un programma di monitoraggio e miglioramento del clima organizzativo e della qualità della vita lavorativa della nostra Rete di Cure Palliative. La compilazione è <b>strettamente anonima</b> e i dati saranno trattati unicamente in forma aggregata. Le vostre risposte sono uno strumento fondamentale per valorizzare il benessere del personale e orientare azioni di supporto mirate.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Legenda della Scala Likert a 5 punti:")
    st.markdown("""
    * **1** = Fortemente in disaccordo
    * **2** = In disaccordo
    * **3** = Neutro / Indeciso
    * **4** = In accordo
    * **5** = Fortemente in accordo
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Inizia il Questionario ➔", type="primary", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

# SCHERMATA 1: Area 1
elif st.session_state.step == 1:
    st.progress(0.2, text="Area 1 di 5: Soddisfazione Lavorativa")
    st.header("🩺 AREA 1: Soddisfazione Lavorativa e Realizzazione Professionale")
    
    q1_1 = st.radio(
        "1. Nel complesso, trovo che il mio lavoro quotidiano in Cure Palliative mantenga un profondo significato e valore per la mia crescita professionale.",
        options=[1, 2, 3, 4, 5], format_func=lambda x: likert_labels[x],
        index=None, key="radio_1_1"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    q1_2 = st.radio(
        "2. Sento che le mie competenze specifiche e il mio contributo clinico sono adeguatamente riconosciuti dall'équipe e dalla direzione.",
        options=[1, 2, 3, 4, 5], format_func=lambda x: likert_labels[x],
        index=None, key="radio_1_2"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️️ Indietro"):
            st.session_state.step = 0
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            if q1_1 is None or q1_2 is None:
                st.warning("Per favore, rispondi a tutte le domande prima di procedere.")
            else:
                st.session_state.q1_1 = q1_1
                st.session_state.q1_2 = q1_2
                st.session_state.step = 2
                st.rerun()

# SCHERMATA 2: Area 2
elif st.session_state.step == 2:
    st.progress(0.4, text="Area 2 di 5: Clima Organizzativo")
    st.header("🩺 AREA 2: Clima Organizzativo e Dinamiche d'Équipe")

    questions_area2 = [
        "1. All'interno della nostra Unità Operativa esiste un clima di reciproco supporto, fiducia e collaborazione aperta tra medici e infermieri.",
        "2. I carichi di lavoro, la turnazione e la gestione delle risorse umane/strutturali sono organizzati in modo equo e sostenibile.",
        "3. I momenti di debriefing e di confronto multiprofessionale (es. riunioni d'équipe o supporto psicologico) sono sufficienti e utili per affrontare i casi complessi.",
        "4. La nostra unità promuove attivamente la parità di genere, garantendo uguali opportunità di crescita, rispetto e valorizzazione professionale indipendentemente dal genere.",
        "5. L’ambiente lavorativo è sicuro e rispettoso delle differenze individuali, garantendo un clima di piena accettazione e tutela rispetto all’orientamento sessuale e all’identità di persona."
    ]

    answers_2 = []
    for idx, q_text in enumerate(questions_area2, 1):
        ans = st.radio(
            q_text, options=[1, 2, 3, 4, 5], format_func=lambda x: likert_labels[x],
            index=None, key=f"radio_2_{idx}"
        )
        answers_2.append(ans)
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            if None in answers_2:
                st.warning("Per favore, rispondi a tutte le domande prima di procedere.")
            else:
                for idx, val in enumerate(answers_2, 1):
                    st.session_state[f'q2_{idx}'] = val
                st.session_state.step = 3
                st.rerun()

# SCHERMATA 3: Area 3
elif st.session_state.step == 3:
    st.progress(0.6, text="Area 3 di 5: Distress Personale")
    st.header("🩺 AREA 3: Distress Personale e Carico Emotivo")

    questions_area3 = [
        "1. Avverto un livello di esaurimento emotivo e fisico legato alla gestione quotidiana della sofferenza e del fine vita che compromette il mio benessere.",
        "2. Mi accorgo di portare a casa un peso emotivo significativo derivante dalle dinamiche lavorative, che fatica a dissolversi nel tempo libero.",
        "3. Sento di avere a disposizione adeguate strategie personali o istituzionali per gestire lo stress acuto e il rischio di compassion fatigue."
    ]

    answers_3 = []
    for idx, q_text in enumerate(questions_area3, 1):
        ans = st.radio(
            q_text, options=[1, 2, 3, 4, 5], format_func=lambda x: likert_labels[x],
            index=None, key=f"radio_3_{idx}"
        )
        answers_3.append(ans)
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            if None in answers_3:
                st.warning("Per favore, rispondi a tutte le domande prima di procedere.")
            else:
                for idx, val in enumerate(answers_3, 1):
                    st.session_state[f'q3_{idx}'] = val
                st.session_state.step = 4
                st.rerun()

# SCHERMATA 4: Area 4
elif st.session_state.step == 4:
    st.progress(0.8, text="Area 4 di 5: Autonomia e Supporto Etico")
    st.header("🩺 AREA 4: Autonomia, Decision Making e Supporto Etico")

    questions_area4 = [
        "1. Nei casi clinici complessi (es. ostinazione terapeutica, decisioni di fine vita), sento di poter esprimere liberamente il mio parere e di essere supportato nelle scelte etiche.",
        "2. Posso contare su chiare linee guida operative e su percorsi condivisi che riducono l'incertezza nella presa in carico del paziente e della famiglia."
    ]

    answers_4 = []
    for idx, q_text in enumerate(questions_area4, 1):
        ans = st.radio(
            q_text, options=[1, 2, 3, 4, 5], format_func=lambda x: likert_labels[x],
            index=None, key=f"radio_4_{idx}"
        )
        answers_4.append(ans)
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            if None in answers_4:
                st.warning("Per favore, rispondi a tutte le domande prima di procedere.")
            else:
                for idx, val in enumerate(answers_4, 1):
                    st.session_state[f'q4_{idx}'] = val
                st.session_state.step = 5
                st.rerun()

# SCHERMATA 5: Area 5 e Invio
elif st.session_state.step == 5:
    st.progress(1.0, text="Area 5 di 5: Sviluppo Professionale")
    st.header("🩺 AREA 5: Sviluppo Professionale e Prospettive Future")

    questions_area5 = [
        "1. L'azienda/struttura offre adeguate opportunità di formazione continua e aggiornamento specifico in cure palliative.",
        "2. Alla luce delle condizioni attuali, rifletterei positivamente sulla scelta di continuare a lavorare a lungo termine in questo specifico ambito assistenziale."
    ]

    answers_5 = []
    for idx, q_text in enumerate(questions_area5, 1):
        ans = st.radio(
            q_text, options=[1, 2, 3, 4, 5], format_func=lambda x: likert_labels[x],
            index=None, key=f"radio_5_{idx}"
        )
        answers_5.append(ans)
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("Invia Risposte in Modo Anonimo 🚀", type="primary"):
            if None in answers_5:
                st.warning("Per favore, rispondi a tutte le domande prima di procedere.")
            else:
                for idx, val in enumerate(answers_5, 1):
                    st.session_state[f'q5_{idx}'] = val
                st.session_state.step = 6
                st.rerun()

# SCHERMATA 6: Conferma e Cruscotto di Analisi / Grafico a Radar
elif st.session_state.step == 6:
    st.success("✅ Grazie per la collaborazione! Il questionario è stato registrato con successo in forma anonima.")
    
    st.markdown("---")
    st.markdown("### 📈 Cruscotto di Sintesi (Analisi di Reparto)")
    st.markdown("*Ecco la visualizzazione sintetica dei punteggi medi per area calcolati in base alle risposte inserite:*")

    # Calcolo delle medie per area (con inversione logica per l'Area 3 del distress)
    score_area1 = np.mean([st.session_state.q1_1, st.session_state.q1_2])
    score_area2 = np.mean([st.session_state.q2_1, st.session_state.q2_2, st.session_state.q2_3, st.session_state.q2_4, st.session_state.q2_5])
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
        st.session_state.step = 0
        st.rerun()
