import streamlit as st
import pandas as pd
import numpy as np
import pickle
import streamlit_modal as modal
import streamlit.components.v1 as components

st.write("""#### Preencha as informações abaixo e clique no botão 'Enviar' para ter o seu diagnóstico.""")

pickle_in = open('ensemble_model.pkl', 'rb')
classifier = pickle.load(pickle_in)

pickle_in = open('ensemble_proba_model.pkl', 'rb')
proba = pickle.load(pickle_in)


with st.form("features"):
    altura = st.number_input ("Qual a sua altura em metros?")
    peso = st.number_input ("Qual o seu peso em Quilos (Kg)?")
    numero_gravidez = st.number_input("Quantas vezes você já engravidou?", min_value = 0, value = 0)
    glicose = st.number_input ("Quantos mg/dL de Glicose foi reportado no último exame de sangue?", value = 0)
    pressao_sangue = st.number_input ("Qual a sua pressão sanguínea diastólica em mmHg no último exame realizado?", value = 0)  
    espessura_pele = st.number_input ("Qual a espessura da dobra subcutanea tricipital em milímetros? (medida realizada com adipometro na regiao do tríceps)", value = 0)
    insulina = st.number_input ("Quantos µIU/mL de Insulina foi reportado no último exame de sangue?", value = 0)
    fat_pred_diab = st.number_input ("Qual o seu fator de predisposição à diabetes? (baseado em histórico familiar)", value = 0.0, format = "%f")
    idade = st.number_input ("Qual a sua idade nesse momento?", value = 0)
    enviar = st.form_submit_button("Enviar")

def prediction(ind_mass_corp, numero_gravidez, glicose, pressao_sangue,espessura_pele,insulina,fat_pred_diab,idade, model = classifier, model2 = proba):  
   
    prediction = model.predict(
        pd.DataFrame({'Pregnancies':[numero_gravidez], 'Glucose':[glicose], 'BloodPressure':[pressao_sangue], 'SkinThickness':[espessura_pele], 'Insulin':[insulina],
       'BMI':[ind_mass_corp], 'DiabetesPedigreeFunction':[fat_pred_diab], 'Age':[idade]}))
    print(prediction)
    proba = model2.predict_proba(
        pd.DataFrame({'Pregnancies':[numero_gravidez], 'Glucose':[glicose], 'BloodPressure':[pressao_sangue], 'SkinThickness':[espessura_pele], 'Insulin':[insulina],
       'BMI':[ind_mass_corp], 'DiabetesPedigreeFunction':[fat_pred_diab], 'Age':[idade]}))
    return [prediction, proba]
if enviar:
    modal.open()

if modal.is_open():
    with modal.container():
        ind_mass_corp = (peso/(altura**2))
        booleano = prediction (ind_mass_corp, numero_gravidez, glicose, pressao_sangue,espessura_pele,insulina,fat_pred_diab,idade)

        if booleano [0] == 0:
            st.write ('#### Parabéns, você tem poucas chances de possuir diabetes \n#### (Apenas {:.2f}%). Continue cuidando da sua saúde.'.format(100*booleano[1][0] [1]))
        else:
            st.write ('#### Existe uma chance de {:.2f}% de você ser diabético. \n#### Recomenda-se procurar um médico.'.format(100*booleano[1][0] [booleano[0][0]]))

            
        st.markdown('<a href="https://carvalhofs-diabets-predict-principal-l1e0kt.streamlitapp.com/Contatos_Especialistas" target="_self"><button type="button">Retornar para Contatos de Especialistas</button></a>', unsafe_allow_html=True)