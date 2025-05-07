import streamlit as st
import pandas as pd
import transferencias
import ajustes
import auxiliar


st.set_page_config(
    layout='centered',
    page_title='Transferências e ajustes',
    page_icon='🧾',
    initial_sidebar_state='expanded'
)

st.header('Movimentação e ajuste de estoque')
st.text('Automação para transferir e ajustar estoque do Peoplesoft.')
st.divider()

st.subheader('Tipo de transação')
input_tipo = st.radio(
    label='Tipo de transação:',
    options=['Ajustes de estoque', 'Transferências entre locais'],
    horizontal=True,
    label_visibility='collapsed'
)
 

st.container(height=20, border=False)

st.subheader('Carregar aquivo')
arquivo_upload = st.file_uploader(
    key='file_upload', 
    label='Selecione o arquivo:', 
    type=['xlsx'], 
    accept_multiple_files=False, 
    help='Colunas obrigatórias: Item, Qtd')

if arquivo_upload is not None:
    df = pd.read_excel(arquivo_upload)
    df['Item'] = df['Item'].astype(str)
    df['Qtd'] = pd.to_numeric(df['Qtd'], errors='coerce').astype('Int64')
    auxiliar.df = df
    st.dataframe(key='file_upload', data=df, use_container_width=True, hide_index=True)

st.container(height=80, border=False)

left_bar = st.sidebar

with left_bar:

    form =  st.form(key='formulario', clear_on_submit=True, border=False)

    with form:

        txt_usuario = st.text_input(
            label='🧑🏽 Usuário:', 
            autocomplete=None)
        
        txt_senha = st.text_input(
            label='🔒 Senha',
            type='password',
            autocomplete=None)
        
        cd, setor= st.columns(2)
        
        txt_cd = cd.selectbox(
            label='CD',
            options=['', 'VD906', 'VD908', 'VD909', 'VD910', 'VD915', 'VD917']
        )

        txt_setor_responsavel = setor.text_input(
            label='Setor resp.',
            max_chars=5,
            autocomplete=None)
        
        if input_tipo == 'Transferências entre locais':
            select_tipo = st.selectbox(
                label='Tipo de movimentação',
                options=['Outros', 'Avaria', 'Fábrica', 'Validade'],
            )

            txt_cod_mov =st.text_input(
                label='Código da movimentação',
                max_chars=3,
                autocomplete=None)
            
        else:
            select_tipo = st.segmented_control(
                label='Tipo de movimentação',
                options=['Entrada (OEE)', 'Saída (BXE)'],
                default='Saída (BXE)'
                )
            
            txt_distribuicao = st.text_input(
            label='Motivo do ajuste',
            value='AJUSTE',
            autocomplete=None)
            
        area1, area2, area3 = st.columns([1.38, 1.12, 1.12])

        txt_area = area1.text_input(
            label='Área',
            max_chars=5,
            autocomplete=None)
        
        txt_nv1 = area2.text_input(
            label='Nv 1',
            max_chars=3,
            autocomplete=None)
        
        txt_nv2 = area3.text_input(
            label='Nv 2',
            max_chars=3,
            autocomplete=None)
    
    st.container(height=3, border=False)

    botao_iniciar = form.form_submit_button(
        label='Iniciar',
        use_container_width=True,
        type='primary')

    if botao_iniciar:

        if input_tipo == 'Transferências entre locais':
            transferencias.iniciar_automacao(
                usuario=str(txt_usuario),
                senha=str(txt_senha),
                cd=str(txt_cd),
                departamento_responsavel=str(txt_setor_responsavel),
                area=str(txt_area),
                nv1=str(txt_nv1),
                nv2=str(txt_nv2),
                motivo=str(select_tipo),
                cod_motivo=str(txt_cod_mov))
            
        else:
            ajustes.iniciar_automacao(
                usuario=str(txt_usuario),
                senha=str(txt_senha),
                cd=str(txt_cd),
                departamento_responsavel=str(txt_setor_responsavel),
                area=str(txt_area),
                nv1=str(txt_nv1),
                nv2=str(txt_nv2),
                motivo=str(select_tipo),
                distribuicao=str(txt_distribuicao))
