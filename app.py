import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import openpyxl

# Configurazione della pagina
st.set_page_config(
    page_title="Monitoraggio Clima Organizzativo - Cure Palliative",
    page_icon="🏥",
    layout="centered"
)

# Inizializzazione dello stato della sessione per la navigazione a schermate
if 'step' not in st.session_state:
    st.session_state.step = 0

# Testi esatti richiesti
titolo_principale = "QUESTIONARIO DI MONITORAGGIO DEL BENESSERE E CLIMA ORGANIZZATIVO IN CURE PALLIATIVE"
sottotitolo = "Unità Operativa Complessa Rete delle Cure Palliative – UA Cure Palliative Adulto<br>Valutazione della Soddisfazione e del Distress del Personale Sanitario"

# Funzione per mostrare l'intestazione centrata e ridotta del 20%
def render_header():
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 25px;">
        <h2 style="font-size: 22px; color: #1F4E78; font-weight: bold; margin-bottom: 8px;">{titolo_principale}</h2>
        <p style="font-size: 13px; color: #555555; line-height: 1.4;">{sottotitolo}</p>
    </div>
    """, unsafe_allow_html=True)

# Funzione d'appoggio per creare una scala Likert orizzontale pulita con colonne
def render_likert_question(question_text, key_name):
    st.markdown(f"**{question_text}**")
    
    if key_name not in st.session_state:
        st.session_state[key_name] = None
        
    cols = st.columns(5)
    labels = [
        "Fortemente in disaccordo",
        "In disaccordo",
        "Neutro / Indeciso",
        "In accordo",
        "Fortemente in accordo"
    ]
    
    selected_val = st.session_state[key_name]
    
    for i in range(5):
        val = i + 1
        with cols[i]:
            is_selected = (selected_val == val)
            btn_label = f"🔵 **{val}**" if is_selected else f"⚪ {val}"
            if st.button(btn_label, key=f"btn_{key_name}_{val}", use_container_width=True):
                st.session_state[key_name] = val
                st.rerun()
            st.markdown(f"<div style='text-align: center; font-size: 11px; color: #555555; min-height: 30px;'>{labels[i]}</div>", unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
    return st.session_state[key_name]

# Funzione per registrare i dati direttamente nel file Excel ufficiale di analisi
def registra_risposta_su_excel():
    excel_file = "Strumento_Analisi_Questionario_Cure_Palliative.xlsx"
    
    # Calcolo delle medie per area rispettando la struttura del file Excel
    m_area1 = np.mean([st.session_state.q1_1, st.session_state.q1_2])
    m_area2 = np.mean([st.session_state.q2_1, st.session_state.q2_2, st.session_state.q2_3, st.session_state.q2_4, st.session_state.q2_5])
    # Area 3 Distress (invertita: 6 - valore)
    m_area3 = np.mean([6 - st.session_state.q3_1, 6 - st.session_state.q3_2, 6 - st.session_state.q3_3])
    m_area4 = np.mean([st.session_state.q4_1, st.session_state.q4_2])
    m_area5 = np.mean([st.session_state.q5_1, st.session_state.q5_2])
    
    indice_globale = np.mean([m_area1, m_area2, m_area3, m_area4, m_area5])
    
    # Leggiamo il file Excel esistente per determinare il progressivo dell'ID Risposta
    if os.path.exists(excel_file):
        df_esistente = pd.read_excel(excel_file, sheet_name='Raccolta Dati')
        num_id = len(df_esistente) + 1
    else:
        num_id = 1
        
    id_risposta_str = f"ID_{num_id:03d}"
    data_compilazione = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    
    nuova_riga = {
        "Data_Ora": data_compilazione,
        "ID Risposta": id_risposta_str,
        "Profilo Professionale": "Anonimo", # Senza dati anagrafici per tutelare la privacy
        "A1_Q1 (Significato Lavoro)": st.session_state.q1_1,
        "A1_Q2 (Riconoscimento)": st.session_state.q1_2,
        "A2_Q3 (Supporto Équipe)": st.session_state.q2_1,
        "A2_Q4 (Carichi Sostenibili)": st.session_state.q2_2,
        "A2_Q5 (Debriefing)": st.session_state.q2_3,
        "A2_Q6 (Parità di Genere)": st.session_state.q2_4,
        "A2_Q7 (Inclusione/Orientamento)": st.session_state.q2_5,
        "A3_Q8 (Esaurimento Emotivo)*": st.session_state.q3_1,
        "A3_Q9 (Peso Emotivo)*": st.session_state.q3_2,
        "A3_Q10 (Strategie Coping)": st.session_state.q3_3,
        "A4_Q11 (Supporto Etico)": st.session_state.q4_1,
        "A4_Q12 (Linee Guida)": st.session_state.q4_2,
        "A5_Q13 (Formazione)": st.session_state.q5_1,
        "A5_Q14 (Prospettive Future)": st.session_state.q5_2,
        "Media Area 1": round(m_area1, 2),
        "Media Area 2": round(m_area2, 2),
        "Media Area 3 (Invertita)": round(m_area3, 2),
        "Media Area 4": round(m_area4, 2),
        "Media Area 5": round(m_area5, 2),
        "Indice Benessere Globale": round(indice_globale, 2)
    }
    
    df_nuovo = pd.DataFrame([nuova_riga])
    
    if os.path.exists(excel_file):
        # Utilizziamo pandas ExcelWriter per aggiornare il foglio 'Raccolta Dati' mantenendo 'Analisi e Sintesi'
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            # Leggiamo tutto il foglio esistente per appendere la riga in fondo
            df_full = pd.read_excel(excel_file, sheet_name='Raccolta Dati')
            df_updated = pd.concat([df_full, df_nuovo], ignore_index=True)
            df_updated.to_excel(writer, sheet_name='Raccolta Dati', index=False)
    else:
        # Se per qualche motivo il file non è presente, lo creiamo da zero con i due fogli
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df_nuovo.to_excel(writer, sheet_name='Raccolta Dati', index=False)
            df_sintesi = pd.DataFrame({
                "DASHBOARD DI MONITORAGGIO - SINTESI RISULTATI": ["Unità Operativa Complessa Rete delle Cure Palliative"],
                "Numero Item": [14],
                "Media Totale": [round(indice_globale, 2)],
                "Mediani / Note": ["Aggiornato in tempo reale"],
                "Stato / Soglia": ["Ottimale"]
            })
            df_sintesi.to_excel(writer, sheet_name='Analisi e Sintesi', index=False)

# SCHERMATA 0: Presentazione e istruzioni
if st.session_state.step == 0:
    render_header()
    st.markdown("<br>", unsafe_allow_html=True)
    
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
    render_header()
    st.progress(0.2, text="Area 1 di 5: Soddisfazione Lavorativa")
    st.header("🩺 AREA 1: Soddisfazione Lavorativa e Realizzazione Professionale")
    
    val1 = render_likert_question("1. Nel complesso, trovo che il mio lavoro quotidiano in Cure Palliative mantenga un profondo significato e valore per la mia crescita professionale.", "q1_1")
    val2 = render_likert_question("2. Sento che le mie competenze specifiche e il mio contributo clinico sono adeguatamente riconosciuti dall'équipe e dalla direzione.", "q1_2")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 0
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            if val1 is None or val2 is None:
                st.warning("Per favore, rispondi a tutte le domande prima di procedere.")
            else:
                st.session_state.step = 2
                st.rerun()

# SCHERMATA 2: Area 2
elif st.session_state.step == 2:
    render_header()
    st.progress(0.4, text="Area 2 di 5: Clima Organizzativo")
    st.header("🩺 AREA 2: Clima Organizzativo e Dinamiche d'Équipe")

    q_texts_2 = [
        "1. All'interno della nostra Unità Operativa esiste un clima di reciproco supporto, fiducia e collaborazione aperta tra medici e infermieri.",
        "2. I carichi di lavoro, la turnazione e la gestione delle risorse umane/strutturali sono organizzati in modo equo e sostenibile.",
        "3. I momenti di debriefing e di confronto multiprofessionale (es. riunioni d'équipe o supporto psicologico) sono sufficienti e utili per affrontare i casi complessi.",
        "4. La nostra unità promuove attivamente la parità di genere, garantendo uguali opportunità di crescita, rispetto e valorizzazione professionale indipendentemente dal genere.",
        "5. L’ambiente lavorativo è sicuro e rispettoso delle differenze individuali, garantendo un clima di piena accettazione e tutela rispetto all’orientamento sessuale e all’identità di persona."
    ]
    
    vals_2 = []
    for i, q in enumerate(q_texts_2, 1):
        v = render_likert_question(q, f"q2_{i}")
        vals_2.append(v)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 1
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            if None in vals_2:
                st.warning("Per favore, rispondi a tutte le domande prima di procedere.")
            else:
                st.session_state.step = 3
                st.rerun()

# SCHERMATA 3: Area 3
elif st.session_state.step == 3:
    render_header()
    st.progress(0.6, text="Area 3 di 5: Distress Personale")
    st.header("🩺 AREA 3: Distress Personale e Carico Emotivo")

    q_texts_3 = [
        "1. Avverto un livello di esaurimento emotivo e fisico legato alla gestione quotidiana della sofferenza e del fine vita che compromette il mio benessere.",
        "2. Mi accorgo di portare a casa un peso emotivo significativo derivante dalle dinamiche lavorative, che fatica a dissolversi nel tempo libero.",
        "3. Sento di avere a disposizione adeguate strategie personali o istituzionali per gestire lo stress acuto e il rischio di compassion fatigue."
    ]
    
    vals_3 = []
    for i, q in enumerate(q_texts_3, 1):
        v = render_likert_question(q, f"q3_{i}")
        vals_3.append(v)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 2
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            if None in vals_3:
                st.warning("Per favore, rispondi a tutte le domande prima di procedere.")
            else:
                st.session_state.step = 4
                st.rerun()

# SCHERMATA 4: Area 4
elif st.session_state.step == 4:
    render_header()
    st.progress(0.8, text="Area 4 di 5: Autonomia e Supporto Etico")
    st.header("🩺 AREA 4: Autonomia, Decision Making e Supporto Etico")

    q_texts_4 = [
        "1. Nei casi clinici complessi (es. ostinazione terapeutica, decisioni di fine vita), sento di poter esprimere liberamente il mio parere e di essere supportato nelle scelte etiche.",
        "2. Posso contare su chiare linee guida operative e su percorsi condivisi che riducono l'incertezza nella presa in carico del paziente e della famiglia."
    ]
    
    vals_4 = []
    for i, q in enumerate(q_texts_4, 1):
        v = render_likert_question(q, f"q4_{i}")
        vals_4.append(v)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 3
            st.rerun()
    with col2:
        if st.button("Avanti ➔", type="primary"):
            if None in vals_4:
                st.warning("Per favore, rispondi a tutte le domande prima di procedere.")
            else:
                st.session_state.step = 5
                st.rerun()

# SCHERMATA 5: Area 5 e Invio
elif st.session_state.step == 5:
    render_header()
    st.progress(1.0, text="Area 5 di 5: Sviluppo Professionale")
    st.header("🩺 AREA 5: Sviluppo Professionale e Prospettive Future")

    q_texts_5 = [
        "1. L'azienda/struttura offre adeguate opportunità di formazione continua e aggiornamento specifico in cure palliative.",
        "2. Alla luce delle condizioni attuali, rifletterei positivamente sulla scelta di continuare a lavorare a lungo termine in questo specifico ambito assistenziale."
    ]
    
    vals_5 = []
    for i, q in enumerate(q_texts_5, 1):
        v = render_likert_question(q, f"q5_{i}")
        vals_5.append(v)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Indietro"):
            st.session_state.step = 4
            st.rerun()
    with col2:
        if st.button("Invia Risposte in Modo Anonimo 🚀", type="primary"):
            if None in vals_5:
                st.warning("Per favore, rispondi a tutte le domande prima di procedere.")
            else:
                # Salvataggio automatico sul file Excel ufficiale
                registra_risposta_su_excel()
                st.session_state.step = 6
                st.rerun()

# SCHERMATA 6: Conferma e Cruscotto Personale
elif st.session_state.step == 6:
    render_header()
    st.success("✅ Grazie per la collaborazione! Il questionario è stato registrato con successo in forma anonima.")
    
    st.markdown("---")
    st.markdown("### CRUSCOTTO DI SINTESI (le mie risposte)")
    st.markdown("*Ecco la visualizzazione sintetica dei punteggi medi per area calcolate in base alle tue risposte:*")

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
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.step = 0
        st.rerun()
