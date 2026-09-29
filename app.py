import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# Configurazione della pagina
st.set_page_config(
    page_title="Monitoraggio Benessere - Cure Palliative",
    page_icon="🏥",
    layout="wide"
)

# Intestazione istituzionale
st.title("🏥 Unità Operativa Complessa di Cure Palliative")
st.subheader("Monitoraggio del Clima Organizzativo e Benessere Lavorativo")
st.markdown("""
*Gentile collega, questo questionario anonimo è volto a monitorare il benessere organizzativo, il carico lavorativo e il clima all'interno della nostra unità operativa. La compilazione richiede circa 3 minuti.*
""")

with st.form("questionario_form"):
    st.markdown("### 📋 Sezione Anagrafica e Ruolo")
    col1, col2 = st.columns(2)
    with col1:
        ruolo = st.selectbox("Ruolo Professionale", ["Medico", "Infermiere/a", "Altro personale sanitario"])
    with col2:
        Anzianita = st.selectbox("Anzianità di servizio in reparto", ["Meno di 1 anno", "1-5 anni", "Più di 5 anni"])

    st.markdown("---")
    st.markdown("### 📊 Valutazione (Scala da 1 a 5)")
    st.markdown("*1 = Per niente d'accordo / Mai | 5 = Pienamente d'accordo / Sempre*")

    # Domande strutturate sulle dimensioni chiave
    q1 = st.slider("1. Sento di avere un supporto adeguato dai colleghi e dal coordinamento nei momenti di maggiore carico emotivo.", 1, 5, 3)
    q2 = st.slider("2. I carichi di lavoro e i ritmi della nostra unità operativa sono sostenibili nel lungo termine.", 1, 5, 3)
    q3 = st.slider("3. Avverto segnali di esaurimento psicofisico (burnout) legati alla specificità delle cure palliative.", 1, 5, 3)
    q4 = st.slider("4. Nel reparto vengono garantite pari opportunità di crescita professionale e rispetto di genere.", 1, 5, 3)
    q5 = st.slider("5. Il clima organizzativo favorisce il rispetto dell'inclusività e della diversità (es. orientamento, identità).", 1, 5, 3)
    q6 = st.slider("6. Ho spazi e momenti strutturati di confronto o debriefing per elaborare il vissuto clinico.", 1, 5, 3)

    submitted = st.form_submit_button("Invia Risposta")

if submitted:
    # Salvataggio simulato o elaborazione dati
    st.success("✅ Risposta registrata con successo. Grazie per il tuo contributo!")
    
    # Esempio di elaborazione e visualizzazione Radar Chart immediata per il coordinatore
    st.markdown("---")
    st.markdown("### 📈 Analisi in Tempo Reale (Cruscotto di Reparto)")
    
    # Dati simulati di sintesi per il radar chart basati sulle risposte
    categories = ['Supporto Team', 'Sostenibilità Carichi', 'Gestione Distress', 'Pari Opportunità', 'Inclusività', 'Debriefing']
    values = [q1, q2, 6 - q3, q4, q5, q6] # Invertiamo la q3 del distress per coerenza di scala positiva
    
    df_radar = pd.DataFrame(dict(
        Punteggio=values,
        Dimensione=categories
    ))
    
    fig = px.line_polar(df_radar, r='Punteggio', theta='Dimensione', line_close=True, range_r=[0, 5])
    fig.update_traces(fill='toself', line_color='#1F4E78')
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 5])))
    
    st.plotly_chart(fig, use_container_width=True)
