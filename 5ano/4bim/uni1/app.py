# (TRAVA BLINDADA DE CONTROLE ABSOLUTO)
# Este é o ÚNICO código que você precisa para esta missão.
# Ele cria um aplicativo Streamlit com dois modos:
# 1. Um simulador interativo para a monitoria.
# 2. Um gerador de imagens para imprimir e colar no caderno.
# Esta versão usa a biblioteca 'Pillow' para desenhar, evitando os erros da 'matplotlib'.

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import math

# Função para calcular o Mínimo Múltiplo Comum (MMC)
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b) if a != 0 and b != 0 else 0

# --- Lógica de Geração da Imagem (Usando Pillow) ---
def create_fraction_bar_image(n1, d1, n2, d2, operation, title, show_lcm=False, show_result=True, bar_color1='#4A90E2', bar_color2='#50E3C2', bg_color='#FFFFFF', text_color='#000000'):
    # Configurações da imagem
    img_width = 800
    # A altura muda se a linha de resultado for desenhada ou não
    img_height = 450 if show_result else 320
    bar_height = 80
    padding = 40

    # Tenta carregar uma fonte padrão (arial). Se não encontrar, usa a fonte default.
    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_label = ImageFont.truetype("arial.ttf", 18)
        font_fraction = ImageFont.truetype("arial.ttf", 22)
    except IOError:
        font_title = ImageFont.load_default()
        font_label = ImageFont.load_default()
        font_fraction = ImageFont.load_default()

    image = Image.new('RGB', (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)

    # Desenha o Título
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((img_width - title_w) / 2, 15), title, font=font_title, fill=text_color)

    bar_width = img_width - 2 * padding
    y1 = 80
    y2 = 200

    common_denominator = lcm(d1, d2)

    # --- Desenha as Barras de Fração ---
    # Modo SEM MMC (para a imagem impressa ou passo inicial do simulador)
    if not show_lcm:
        # Barra 1 (Original)
        draw.rectangle([padding, y1, padding + bar_width, y1 + bar_height], outline=text_color, width=2)
        fill_width1 = (n1 / d1) * bar_width
        draw.rectangle([padding, y1, padding + fill_width1, y1 + bar_height], fill=bar_color1)
        for i in range(1, d1):
            x = padding + (i / d1) * bar_width
            draw.line([x, y1, x, y1 + bar_height], fill=bg_color, width=2)
        draw.text((padding + bar_width + 10, y1 + bar_height/2 - 10), f"{n1}/{d1}", font=font_fraction, fill=text_color)

        # Barra 2 (Original)
        draw.rectangle([padding, y2, padding + bar_width, y2 + bar_height], outline=text_color, width=2)
        fill_width2 = (n2 / d2) * bar_width
        draw.rectangle([padding, y2, padding + fill_width2, y2 + bar_height], fill=bar_color2)
        for i in range(1, d2):
            x = padding + (i / d2) * bar_width
            draw.line([x, y2, x, y2 + bar_height], fill=bg_color, width=2)
        draw.text((padding + bar_width + 10, y2 + bar_height/2 - 10), f"{n2}/{d2}", font=font_fraction, fill=text_color)
    # Modo COM MMC (para o passo final do simulador)
    else:
        # Barra 1 (Equivalente)
        n1_equiv = n1 * (common_denominator // d1)
        draw.rectangle([padding, y1, padding + bar_width, y1 + bar_height], outline=text_color, width=2)
        fill_width1_equiv = (n1_equiv / common_denominator) * bar_width
        draw.rectangle([padding, y1, padding + fill_width1_equiv, y1 + bar_height], fill=bar_color1)
        for i in range(1, common_denominator):
            x = padding + (i / common_denominator) * bar_width
            draw.line([x, y1, x, y1 + bar_height], fill=bg_color, width=2)
        draw.text((padding + bar_width + 10, y1 + bar_height/2 - 10), f"{n1_equiv}/{common_denominator}", font=font_fraction, fill=text_color)
        draw.text((padding - 35, y1 + bar_height/2 - 10), f"({n1}/{d1})", font=font_label, fill=text_color)

        # Barra 2 (Equivalente)
        n2_equiv = n2 * (common_denominator // d2)
        draw.rectangle([padding, y2, padding + bar_width, y2 + bar_height], outline=text_color, width=2)
        fill_width2_equiv = (n2_equiv / common_denominator) * bar_width
        draw.rectangle([padding, y2, padding + fill_width2_equiv, y2 + bar_height], fill=bar_color2)
        for i in range(1, common_denominator):
            x = padding + (i / common_denominator) * bar_width
            draw.line([x, y2, x, y2 + bar_height], fill=bg_color, width=2)
        draw.text((padding + bar_width + 10, y2 + bar_height/2 - 10), f"{n2_equiv}/{common_denominator}", font=font_fraction, fill=text_color)
        draw.text((padding - 35, y2 + bar_height/2 - 10), f"({n2}/{d2})", font=font_label, fill=text_color)

    # --- Desenha o Resultado (apenas se 'show_result' for Verdadeiro) ---
    if show_result:
        y_result = 340
        if operation == 'Soma':
            n_result = (n1 * (common_denominator // d1)) + (n2 * (common_denominator // d2))
            op_symbol = '+'
        else: # Subtração
            n_result = (n1 * (common_denominator // d1)) - (n2 * (common_denominator // d2))
            op_symbol = '-'

        if n_result >= 0:
            draw.rectangle([padding, y_result, padding + bar_width, y_result + bar_height], outline=text_color, width=2)
            fill_width_result = (n_result / common_denominator) * bar_width if common_denominator > 0 else 0
            draw.rectangle([padding, y_result, padding + fill_width_result, y_result + bar_height], fill='#E34A7F')
            for i in range(1, common_denominator):
                x = padding + (i / common_denominator) * bar_width
                draw.line([x, y_result, x, y_result + bar_height], fill=bg_color, width=2)

        result_text = f"Resultado ({op_symbol}): {n_result}/{common_denominator}"
        result_bbox = draw.textbbox((0, 0), result_text, font=font_fraction)
        result_w = result_bbox[2] - result_bbox[0]
        draw.text(((img_width - result_w) / 2, y_result - 30), result_text, font=font_fraction, fill=text_color)

    return image

# --- Interface do Aplicativo Streamlit ---
st.set_page_config(layout="wide")

st.sidebar.title("### GERADOR DE MISSÃO: GM-01")
st.sidebar.header("Painel de Controle")

# Seletor de modo
mission_visual = st.sidebar.selectbox("Selecione o Modo:", ["Simulador de Orçamento (Interativo)", "Gerador de Imagem (Impressão)"])

# MODO 1: SIMULADOR INTERATIVO
if mission_visual == "Simulador de Orçamento (Interativo)":
    st.title("Simulador de Orçamento da Missão")
    st.sidebar.subheader("Controles da Simulação")
    op_select = st.sidebar.radio("Operação:", ('Soma', 'Subtração'), key='op_sim')

    c1, c2 = st.sidebar.columns(2)
    with c1:
        st.sidebar.markdown("##### Orçamento 1 (Azul)")
        num1 = st.sidebar.slider("Numerador 1", 1, 20, 1, key='n1_sim')
        den1 = st.sidebar.slider("Denominador 1", 2, 20, 2, key='d1_sim')
    with c2:
        st.sidebar.markdown("##### Orçamento 2 (Verde)")
        num2 = st.sidebar.slider("Numerador 2", 1, 20, 1, key='n2_sim')
        den2 = st.sidebar.slider("Denominador 2", 2, 20, 3, key='d2_sim')

    show_lcm_step = st.sidebar.checkbox("Ajustar Divisões (MMC)", value=False, key='lcm_sim')

    st.sidebar.subheader("Customização Visual")
    color1 = st.sidebar.color_picker('Cor Orçamento 1', '#4A90E2')
    color2 = st.sidebar.color_picker('Cor Orçamento 2', '#50E3C2')

    st.header("Visualização Interativa")
    st.write(f"Simulando a operação: **{num1}/{den1} {op_select} {num2}/{den2}**")

    sim_image = create_fraction_bar_image(num1, den1, num2, den2, op_select, "Simulador de Orçamento", show_lcm_step, show_result=True, bar_color1=color1, bar_color2=color2)
    st.image(sim_image, use_column_width=True)

# MODO 2: GERADOR DE IMAGEM PARA IMPRESSÃO
elif mission_visual == "Gerador de Imagem (Impressão)":
    st.title("Gerador de Imagem para Prática Focada")
    st.sidebar.subheader("Controles da Imagem")
    st.sidebar.write("Configure os valores para a atividade impressa.")

    op_print = st.sidebar.radio("Operação:", ('Soma', 'Subtração'), key='op_print')

    c1p, c2p = st.sidebar.columns(2)
    with c1p:
        st.sidebar.markdown("##### Fração 1")
        num1_p = st.sidebar.number_input("Numerador 1", 1, 20, 1, key='n1_print')
        den1_p = st.sidebar.number_input("Denominador 1", 2, 20, 4, key='d1_print')
    with c2p:
        st.sidebar.markdown("##### Fração 2")
        num2_p = st.sidebar.number_input("Numerador 2", 1, 20, 1, key='n2_print')
        den2_p = st.sidebar.number_input("Denominador 2", 2, 20, 6, key='d2_print')

    img_title = st.sidebar.text_input("Título da Imagem", "ORÇ-01")

    st.header("Preview da Imagem para Impressão")
    st.info("Esta imagem será gerada sem a linha de resultado para que o aluno resolva no caderno.")

    # Gera a imagem sem mostrar o resultado (show_result=False)
    print_image = create_fraction_bar_image(num1_p, den1_p, num2_p, den2_p, op_print, img_title, show_lcm=False, show_result=False)
    st.image(print_image, use_column_width=True)

    # Prepara a imagem para o botão de download
    buf = io.BytesIO()
    print_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Imagem para Impressão (.png)",
        data=byte_im,
        file_name=f"{img_title.replace(' ', '_').lower()}.png",
        mime="image/png"
    )
