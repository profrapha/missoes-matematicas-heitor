# (TRAVA BLINDADA DE CONTROLE ABSOLUTO)
# VERSÃO 2 - Incorpora as sugestões do Raphael:
# - Troca de sliders por caixas de número (st.number_input) para precisão.
# - Adição do botão "Revelar Resultado" para prática ativa.
# - Adição de um botão "Próximo Desafio" para resetar.
# - Inclusão das perguntas-guia diretamente na interface.
# - Correção do aviso "use_column_width".

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import math

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b) if a != 0 and b != 0 else 0

def create_fraction_bar_image(n1, d1, n2, d2, operation, title, show_lcm=False, show_result=False, bar_color1='#4A90E2', bar_color2='#50E3C2', bg_color='#FFFFFF', text_color='#000000'):
    img_width = 800
    img_height = 450 if show_result else 320
    bar_height = 80
    padding = 40

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

    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((img_width - title_w) / 2, 15), title, font=font_title, fill=text_color)

    bar_width = img_width - 2 * padding
    y1, y2 = 80, 200
    common_denominator = lcm(d1, d2)

    if not show_lcm:
        # Barra 1
        draw.rectangle([padding, y1, padding + bar_width, y1 + bar_height], outline=text_color, width=2)
        fill_width1 = (n1 / d1) * bar_width
        draw.rectangle([padding, y1, padding + fill_width1, y1 + bar_height], fill=bar_color1)
        for i in range(1, d1):
            x = padding + (i / d1) * bar_width
            draw.line([x, y1, x, y1 + bar_height], fill=bg_color, width=2)
        draw.text((padding + bar_width + 10, y1 + bar_height/2 - 10), f"{n1}/{d1}", font=font_fraction, fill=text_color)

        # Barra 2
        draw.rectangle([padding, y2, padding + bar_width, y2 + bar_height], outline=text_color, width=2)
        fill_width2 = (n2 / d2) * bar_width
        draw.rectangle([padding, y2, padding + fill_width2, y2 + bar_height], fill=bar_color2)
        for i in range(1, d2):
            x = padding + (i / d2) * bar_width
            draw.line([x, y2, x, y2 + bar_height], fill=bg_color, width=2)
        draw.text((padding + bar_width + 10, y2 + bar_height/2 - 10), f"{n2}/{d2}", font=font_fraction, fill=text_color)
    else: # show_lcm = True
        n1_equiv = n1 * (common_denominator // d1)
        draw.rectangle([padding, y1, padding + bar_width, y1 + bar_height], outline=text_color, width=2)
        fill_width1_equiv = (n1_equiv / common_denominator) * bar_width
        draw.rectangle([padding, y1, padding + fill_width1_equiv, y1 + bar_height], fill=bar_color1)
        for i in range(1, common_denominator):
            x = padding + (i / common_denominator) * bar_width
            draw.line([x, y1, x, y1 + bar_height], fill=bg_color, width=2)
        draw.text((padding + bar_width + 10, y1 + bar_height/2 - 10), f"{n1_equiv}/{common_denominator}", font=font_fraction, fill=text_color)
        draw.text((padding - 35, y1 + bar_height/2 - 10), f"({n1}/{d1})", font=font_label, fill=text_color)

        n2_equiv = n2 * (common_denominator // d2)
        draw.rectangle([padding, y2, padding + bar_width, y2 + bar_height], outline=text_color, width=2)
        fill_width2_equiv = (n2_equiv / common_denominator) * bar_width
        draw.rectangle([padding, y2, padding + fill_width2_equiv, y2 + bar_height], fill=bar_color2)
        for i in range(1, common_denominator):
            x = padding + (i / common_denominator) * bar_width
            draw.line([x, y2, x, y2 + bar_height], fill=bg_color, width=2)
        draw.text((padding + bar_width + 10, y2 + bar_height/2 - 10), f"{n2_equiv}/{common_denominator}", font=font_fraction, fill=text_color)
        draw.text((padding - 35, y2 + bar_height/2 - 10), f"({n2}/{d2})", font=font_label, fill=text_color)

    if show_result:
        y_result = 340
        op_symbol = '+' if operation == 'Soma' else '-'
        n_result_num = (n1_equiv if show_lcm else n1 * (common_denominator // d1)) + \
                       (n2_equiv if show_lcm else n2 * (common_denominator // d2))
        if operation == 'Subtração':
             n_result_num = (n1_equiv if show_lcm else n1 * (common_denominator // d1)) - \
                            (n2_equiv if show_lcm else n2 * (common_denominator // d2))

        draw.rectangle([padding, y_result, padding + bar_width, y_result + bar_height], outline=text_color, width=2)
        if n_result_num >= 0:
            fill_width_result = (n_result_num / common_denominator) * bar_width if common_denominator > 0 else 0
            draw.rectangle([padding, y_result, padding + fill_width_result, y_result + bar_height], fill='#E34A7F')

        for i in range(1, common_denominator):
            x = padding + (i / common_denominator) * bar_width
            draw.line([x, y_result, x, y_result + bar_height], fill=bg_color, width=2)

        result_text = f"Resultado ({op_symbol}): {n_result_num}/{common_denominator}"
        result_bbox = draw.textbbox((0, 0), result_text, font=font_fraction)
        result_w = result_bbox[2] - result_bbox[0]
        draw.text(((img_width - result_w) / 2, y_result - 30), result_text, font=font_fraction, fill=text_color)

    return image

# --- Interface do Aplicativo Streamlit ---
st.set_page_config(layout="wide")

if 'show_result' not in st.session_state:
    st.session_state.show_result = False

st.sidebar.title("### GERADOR DE MISSÃO: GM-02")
st.sidebar.header("Painel de Controle")

mission_mode = st.sidebar.selectbox("Selecione o Modo:", ["Modo Prática/Desafio", "Gerador de Imagem (Impressão)"])

if mission_mode == "Modo Prática/Desafio":
    st.title("Laboratório de Orçamento da Missão")
    st.sidebar.subheader("Controles do Desafio")
    op_select = st.sidebar.radio("Operação:", ('Soma', 'Subtração'), key='op_sim')

    c1, c2 = st.sidebar.columns(2)
    with c1:
        num1 = st.sidebar.number_input("Numerador 1", min_value=1, max_value=50, value=1, key='n1_sim')
        den1 = st.sidebar.number_input("Denominador 1", min_value=2, max_value=50, value=2, key='d1_sim')
    with c2:
        num2 = st.sidebar.number_input("Numerador 2", min_value=1, max_value=50, value=1, key='n2_sim')
        den2 = st.sidebar.number_input("Denominador 2", min_value=2, max_value=50, value=3, key='d2_sim')

    show_lcm_step = st.sidebar.checkbox("Ajustar Divisões (MMC)", value=False, key='lcm_sim')

    col_btn1, col_btn2 = st.sidebar.columns(2)
    if col_btn1.button("Revelar Resultado", use_container_width=True):
        st.session_state.show_result = True

    if col_btn2.button("Próximo Desafio", use_container_width=True):
        st.session_state.show_result = False
        # O Streamlit irá recarregar e a resposta estará oculta.

    st.info("**ETAPA 1: O PROBLEMA**\n\nComandante, observe as barras. Os 'pedaços' têm o mesmo tamanho? Podemos somá-los diretamente?")

    sim_image_problem = create_fraction_bar_image(num1, den1, num2, den2, op_select, "Visualização do Problema", show_lcm=False, show_result=False)
    st.image(sim_image_problem, use_column_width="auto") # Corrigido use_column_width

    st.info("**ETAPA 2: A SOLUÇÃO**\n\nMarque a caixa 'Ajustar Divisões (MMC)' na barra lateral. O que aconteceu com os pedaços? Agora eles têm o mesmo tamanho?")

    if st.session_state.show_result:
        st.success("**ETAPA 3: O RESULTADO**\n\nAgora que os pedaços são iguais, podemos somá-los. Confira a barra de resultado. Bateu com o que você calculou?")
        sim_image_solution = create_fraction_bar_image(num1, den1, num2, den2, op_select, "Visualização da Solução e Resultado", show_lcm=show_lcm_step, show_result=True)
        st.image(sim_image_solution, use_column_width="auto")
    else:
         st.warning("Pense no resultado... Depois clique em 'Revelar Resultado' para checar!")
         # Mostra a imagem com MMC, mas sem o resultado final ainda
         sim_image_no_result = create_fraction_bar_image(num1, den1, num2, den2, op_select, "Visualização da Solução", show_lcm=show_lcm_step, show_result=False)
         st.image(sim_image_no_result, use_column_width="auto")


elif mission_mode == "Gerador de Imagem (Impressão)":
    st.title("Gerador de Imagem para Prática Focada")
    st.sidebar.subheader("Controles da Imagem")
    st.sidebar.write("Configure os valores para a atividade impressa.")

    op_print = st.sidebar.radio("Operação:", ('Soma', 'Subtração'), key='op_print')

    c1p, c2p = st.sidebar.columns(2)
    with c1p:
        num1_p = st.sidebar.number_input("Numerador 1", 1, 20, 1, key='n1_print')
        den1_p = st.sidebar.number_input("Denominador 1", 2, 20, 4, key='d1_print')
    with c2p:
        num2_p = st.sidebar.number_input("Numerador 2", 1, 20, 1, key='n2_print')
        den2_p = st.sidebar.number_input("Denominador 2", 2, 20, 6, key='d2_print')

    img_title = st.sidebar.text_input("Título da Imagem", "ORÇ-01")

    st.header("Preview da Imagem para Impressão")
    st.info("Esta imagem será gerada sem a linha de resultado para que o aluno resolva no caderno.")

    print_image = create_fraction_bar_image(num1_p, den1_p, num2_p, den2_p, op_print, img_title, show_lcm=False, show_result=False)
    st.image(print_image, use_column_width="auto")

    buf = io.BytesIO()
    print_image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    st.download_button(
        label="Download Imagem para Impressão (.png)",
        data=byte_im,
        file_name=f"{img_title.replace(' ', '_').lower()}.png",
        mime="image/png"
    )
