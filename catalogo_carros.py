import streamlit as st
import pandas as pd

# 1. Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_parquet('data_full.parquet')

    # Remove linhas onde não temos marca, modelo ou URLs das imagens
    df = df.dropna(subset=['brand', 'model', 'image_urls'])

    return df


df = load_data()

# 2. Configurar a página
st.set_page_config(page_title='Catálogo de Carros', layout='wide')

st.title("🚗 Catálogo de Carros")

# --- BARRA LATERAL: FILTROS ---
st.sidebar.header("Filtros")

# --- Escolha a Marca
lista_marcas = sorted(df["brand"].unique())
marca_selecionado = st.sidebar.selectbox(
    "Escolha a Marca",
    lista_marcas
)

# --- Escolha o Carro
df_marca = df[df['brand'] == marca_selecionado]

lista_modelos = sorted(df_marca["model"].unique())

modelo_selecionado = st.sidebar.selectbox(
    "Escolha o Modelo",
    lista_modelos
)

# Pega a linha do carro escolhido
carro_info = df_marca[
    df_marca['model'] == modelo_selecionado
].iloc[0]


# --- TRATAMENTO DAS IMAGENS ---

# Transforma a string em uma lista
urls_string = carro_info['image_urls']

lista_imagens = [
    url.strip()
    for url in urls_string.split(',')
    if url.strip()
]

num_imagens = len(lista_imagens)


if num_imagens > 0:

    # Reseta o índice da imagem quando trocar de carro
    chave_carro = f"{marca_selecionado}_{modelo_selecionado}"

    if (
        'carro_atual' not in st.session_state
        or st.session_state.carro_atual != chave_carro
    ):
        st.session_state.foto_index = 0
        st.session_state.carro_atual = chave_carro

    # --- CONTROLES DE NAVEGAÇÃO ---

    col1, col2, col3 = st.columns([1, 4, 1])

    with col1:
        if st.button(
            "⬅️ Anterior",
            use_container_width=True
        ):
            if st.session_state.foto_index > 0:
                st.session_state.foto_index -= 1
            else:
                st.session_state.foto_index = num_imagens - 1

    with col2:
        # Imagem principal
        st.image(
            lista_imagens[st.session_state.foto_index],
            use_container_width=True
        )

    with col3:
        if st.button(
            "Próxima ➡️",
            use_container_width=True
        ):
            if st.session_state.foto_index < num_imagens - 1:
                st.session_state.foto_index += 1
            else:
                st.session_state.foto_index = 0

    # --- GALERIA DE MINIATURAS ---

    st.write("### 📸 Galeria de Fotos")
    st.write("Clique em uma miniatura para visualizá-la:")

    # Quantas miniaturas por linha
    cols_por_linha = 6

    # Cria as linhas da galeria
    for i in range(0, num_imagens, cols_por_linha):

        cols = st.columns(cols_por_linha)

        for j in range(cols_por_linha):

            idx = i + j

            if idx < num_imagens:

                with cols[j]:

                    # Botão da miniatura
                    if st.button(
                        f"Foto {idx + 1}",
                        key=f"thumb_{idx}",
                        use_container_width=True
                    ):
                        st.session_state.foto_index = idx
                        st.rerun()

                    # Imagem pequena
                    st.image(
                        lista_imagens[idx],
                        use_container_width=True
                    )

else:
    st.warning("Nenhuma imagem disponível para este modelo.")


st.divider()

# --- INFORMAÇÕES DO CARRO ---

st.subheader("📝 Descrição")