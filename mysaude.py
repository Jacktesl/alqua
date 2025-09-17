import streamlit as st
import os
import json
import urllib.parse
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv

# --- Carregar variáveis de ambiente ---
load_dotenv()

# --- Configurações Cloudinary ---
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

# --- Configurações Streamlit ---
st.set_page_config(page_title="My Alqualine Max", page_icon="💧", layout="wide")
DB_FILE = "produtos.json"

# --- Funções auxiliares ---
def carregar_produtos():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_produtos(produtos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=4)

# --- Carregar produtos existentes ---
produtos = carregar_produtos()

# --- Título ---
st.markdown(
    """
    <h1 style='text-align: center; color: #00CED1; font-family: Montserrat;'>
        💧 My Alqualine Max
    </h1>
    """,
    unsafe_allow_html=True
)
st.write("### Bem-vindo à nossa vitrine de produtos!")

# --- Sidebar Admin ---
st.sidebar.header("🔒 Área Administrativa")
senha = st.sidebar.text_input("Senha do Admin:", type="password")

if senha == "alqua2025":
    st.sidebar.success("Admin autenticado ✅")
    st.sidebar.subheader("📤 Adicionar Produto")

    nome = st.sidebar.text_input("Nome do Produto")
    descricao = st.sidebar.text_area("Descrição")
    preco = st.sidebar.text_input("Preço (R$)")
    arquivo = st.sidebar.file_uploader(
        "Imagem/Vídeo",
        type=["png", "jpg", "jpeg", "mp4", "webm", "ogg"]
    )

    if st.sidebar.button("Salvar Produto"):
        if nome and preco and arquivo:
            # --- Upload para Cloudinary ---
            upload_result = cloudinary.uploader.upload(arquivo, resource_type="auto")
            url_arquivo = upload_result['secure_url']

            produto = {
                "nome": nome,
                "descricao": descricao,
                "preco": preco,
                "arquivo": url_arquivo,
                "tipo": "video" if arquivo.name.lower().endswith((".mp4", ".webm", ".ogg")) else "imagem"
            }

            produtos.append(produto)
            salvar_produtos(produtos)
            st.sidebar.success(f"{nome} adicionado com sucesso!")
            st.rerun()
        else:
            st.sidebar.error("Preencha todos os campos obrigatórios!")
elif senha != "":
    st.sidebar.error("Senha incorreta!")

# --- Número do WhatsApp ---
WHATSAPP_NUM = "5511953432468"

# --- Vitrine de Produtos ---
st.write("## 🌊 Produtos Disponíveis")
if not produtos:
    st.info("Nenhum produto disponível ainda.")
else:
    cols = st.columns(3)
    for i, p in enumerate(produtos):
        with cols[i % 3]:
            # Nome do produto
            st.markdown(
                f"""
                <div style="
                    border-radius: 15px;
                    padding: 14px;
                    margin-bottom: 24px;
                    background: #0d1b2a;
                    color: white;
                    box-shadow: 0 4px 14px rgba(0,255,255,0.25);
                    text-align: center;
                    font-family: Montserrat;
                    max-width: 300px;
                ">
                    <div style="
                        background: #00CED1;
                        color: #0d1b2a;
                        padding: 6px 12px;
                        border-radius: 10px;
                        font-weight: bold;
                        margin-bottom: 12px;
                    ">
                        {p['nome']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Exibir imagem ou vídeo
            if p["tipo"] == "imagem":
                st.image(p["arquivo"], width=280)
            else:
                st.video(p["arquivo"], format="video/mp4", start_time=0)

            # Preço
            st.markdown(
                f"<div style='margin-top:8px; font-weight:bold; color:#00CED1;'>💲 R$ {p['preco']}</div>",
                unsafe_allow_html=True
            )

            # Descrição
            if p["descricao"]:
                st.markdown(
                    f"<div style='margin-top:4px; font-size:0.85em; color:#cccccc;'>{p['descricao']}</div>",
                    unsafe_allow_html=True
                )

            # Botão WhatsApp
            mensagem = urllib.parse.quote(f"Olá! Tenho interesse no produto {p['nome']}.")
            link_whats = f"https://wa.me/{WHATSAPP_NUM}?text={mensagem}"

            st.markdown(
                f"""
                <a href="{link_whats}" target="_blank" style="
                    display:inline-block;
                    margin-top:10px;
                    padding:10px 16px;
                    background:#00CED1;
                    color:#0d1b2a;
                    text-decoration:none;
                    font-weight:bold;
                    border-radius:8px;
                    box-shadow:0 3px 8px rgba(0,255,255,0.3);
                    font-family: Montserrat;
                ">
                    💬 Falar no WhatsApp
                </a>
                """,
                unsafe_allow_html=True
            )

            # Excluir (admin)
            if senha == "alqua2025":
                if st.button(f"🗑️ Excluir {p['nome']}", key=f"del_{i}"):
                    produtos.pop(i)
                    salvar_produtos(produtos)
                    st.success(f"{p['nome']} removido com sucesso!")
                    st.rerun()
