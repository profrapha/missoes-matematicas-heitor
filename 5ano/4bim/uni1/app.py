# (TRAVA BLINDADA DE CONTROLE ABSOLUTO)
# VERSÃO 3 - Implementa o fluxo pedagógico completo sugerido pelo Raphael.
# - Adiciona campos de input para o aluno testar sua resposta.
# - Adiciona o botão "Verificar Resposta" com feedback.
# - Melhora a função do botão "Próximo Desafio" para limpar os inputs.
# - Aumenta o tamanho das fontes para melhor legibilidade em telas menores (responsividade).
# - Adiciona textos explicativos sobre o MMC diretamente na interface.
# - Garante que o aviso de 'deprecation' não apareça.

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import math

# --- FUNÇÕES AUXILIARES ---
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b) if a != 0 and b != 0 else 0

def simplify_fraction(n, d):
    if n == 0: return 0, 1
    common_divisor = math.gcd(n, d)
    return n // common_divisor, d // common_divisor

# --- LÓGICA DE GERAÇÃO DA IMAGEM ---
def create_fraction_bar_image(n1, d1, n2, d2, operation, title, show_lcm=False, show_result=False, bar_color1='#4A90E2', bar_color2='#50E3C2', bg_color='#FFFFFF', text_color='#000000'):
    img_width = 800
    img_height = 480 if show_result else 320
    bar_height = 80
    padding = 50

    try:
        # Tamanhos de fonte aumentados para legibilidade no celular
        font_title = ImageFont.truetype("arialbd.ttf", 30) # Negrito
        font_fraction = ImageFont.truetype("arialbd.ttf", 28) # Negrito
        font_label = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font_title = ImageFont.load_default()
        font_fraction = ImageFont.load_default()
        font_label = ImageFont.load_default()

    image = Image.new('RGB', (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)

    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_w = title_bbox[2] - title_bbox[0]
    draw.text(((img_width - title_w) / 2, 15), title, font=font_title, fill=text_color)

    bar_width = img_width - 2 * padding
    y1, y2 = 90, 210
    common_denominator = lcm(d1, d2)

    def draw_bar(y, n, d, color, original_text=""):
        draw.rectangle([padding, y, padding + bar_width, y + bar_height], outline=text_color, width=2)
        fill_width = (n / d) * bar_width if d != 0 else 0
        draw.rectangle([padding, y, padding + fill_width, y + bar_height], fill=color)
        for i in range(1, d):
            x = padding + (i / d) * bar_width
            draw.line([x, y, x, y + bar_height], fill=bg_color, width=3)
        draw.text((padding + bar_width + 15, y + bar_height/2 - 15), f"{n}/{d}", font=font_fraction, fill=text_color)
        if original_text:
            draw.text((padding - 50, y + bar_height/2 - 12), original_text, font=font_label, fill=text_color)

    if not show_lcm:
        draw_bar(y1, n1, d1, bar_color1)
        draw_bar(y2, n2, d2, bar_color2)
    else:
        n1_equiv = n1 * (common_denominator // d1)
        draw_bar(y1, n1_equiv, common_denominator, bar_color1, original_text=f"({n1}/{d1})")
        n2_equiv = n2 * (common_denominator // d2)
        draw_bar(y2, n2_equiv, common_denominator, bar_color2, original_text=f"({n2}/{d2})")

    if show_result:
        y_result = 360
        n_result_num = 0
        if operation == 'Soma':
            n_result_num = (n1 * (common_denominator // d1)) + (n2 * (common_denominator // d2))
        else:
            n_result_num = (n1 * (common_denominator // d1)) - (n2 * (common_denominator // d2))

        n_simple, d_simple = simplify_fraction(n_result_num, common_denominator)
        result_text = f"Resultado: {n_result_num}/{common_denominator}"
        if (n_simple, d_simple) != (n_result_num, common_denominator):
             result_text += f" = {n_simple}/{d_simple}"

        draw_bar(y_result, n_result_num, common_denominator, '#E34A7F')

        result_bbox = draw.textbbox((0, 0), result_text, font=font_title)
        result_w = result_bbox[2] - result_bbox[0]
        draw.text(((img_width - result_w) / 2, y_result - 40), result_text, font=font_title, fill=text_color)

    return image

# --- LÓGICA DO APLICATIVO STREAMLIT ---
st.set_page_config(layout="wide")

# Inicializa o session_state
if 'step' not in st.session_state:
    st.session_state.step = 0 # 0: initial, 1: checked, 2: reset
if 'n1' not in st.session_state: st.session_state.n1 = 1
if 'd1' not in st.session_state: st.session_state.d1 = 2
if 'n2' not in st.session_state: st.session_state.n2 = 1
if 'd2' not in st.session_state: st.session_state.d2 = 3
if 'ans_n' not in st.session_state: st.session_state.ans_n = 0
if 'ans_d' not in st.session_state: st.session_state.ans_d = 1


st.sidebar.title("### GERADOR DE MISSÃO: GM-03")
st.sidebar.header("Painel de Controle")

# --- MODO 1: LABORATÓRIO INTERATIVO ---
st.title("Laboratório de Orçamento da Missão")
st.sidebar.subheader("Controles do Desafio")
op_select = st.sidebar.radio("Operação:", ('Soma', 'Subtração'), key='op_sim')

# Inputs na sidebar
st.sidebar.markdown("---")
st.session_state.n1 = st.sidebar.number_input("Numerador 1", min_value=1, value=st.session_state.n1)
st.session_state.d1 = st.sidebar.number_input("Denominador 1", min_value=2, value=st.session_state.d1)
st.sidebar.markdown("---")
st.session_state.n2 = st.sidebar.number_input("Numerador 2", min_value=1, value=st.session_state.n2)
st.session_state.d2 = st.sidebar.number_input("Denominador 2", min_value=2, value=st.session_state.d2)

# --- FLUXO NARRATIVO GUIADO ---
st.subheader("ETAPA 1: O Problema")
st.info("Comandante, observe as barras. Os 'pedaços' de cada orçamento têm o mesmo tamanho? Podemos juntá-los diretamente?")
problem_img = create_fraction_bar_image(st.session_state.n1, st.session_state.d1, st.session_state.n2, st.session_state.d2, op_select, "Visualização do Problema", show_result=False)
st.image(problem_img, use_container_width=True)

st.subheader("ETAPA 2: A Solução (MMC)")
st.info("Para somar, precisamos de pedaços do mesmo tamanho. O MMC (Mínimo Múltiplo Comum) nos ajuda a encontrar o 'corte' perfeito para as duas barras.")
solution_img = create_fraction_bar_image(st.session_state.n1, st.session_state.d1, st.session_state.n2, st.session_state.d2, op_select, "Visualização com Denominador Comum (MMC)", show_lcm=True, show_result=False)
st.image(solution_img, use_container_width=True)
st.markdown(f"> **Explicação:** O MMC entre **{st.session_state.d1}** e **{st.session_state.d2}** é **{lcm(st.session_state.d1, st.session_state.d2)}**. Por isso, a ferramenta re-dividiu as barras em pedaços desse tamanho. É para isso que o MMC serve!")

st.subheader("ETAPA 3: Teste seu Cálculo")
st.info("Agora que as barras estão divididas igualmente, calcule o resultado final no seu caderno e digite sua resposta abaixo.")

# Inputs para a resposta do aluno
col1, col2 = st.columns(2)
with col1:
    st.session_state.ans_n = st.number_input("Seu Numerador:", min_value=0, value=st.session_state.ans_n, key="ans_n_key")
with col2:
    st.session_state.ans_d = st.number_input("Seu Denominador:", min_value=1, value=st.session_state.ans_d, key="ans_d_key")

# Botões de Ação
btn_check = st.button("Verificar Minha Resposta", type="primary", use_container_width=True)

if btn_check:
    st.session_state.step = 1 # Mudar para o estado "verificado"

    # Calcular a resposta correta
    common_d = lcm(st.session_state.d1, st.session_state.d2)
    if op_select == 'Soma':
        correct_n = (st.session_state.n1 * (common_d // st.session_state.d1)) + (st.session_state.n2 * (common_d // st.session_state.d2))
    else:
        correct_n = (st.session_state.n1 * (common_d // st.session_state.d1)) - (st.session_state.n2 * (common_d // st.session_state.d2))

    # Simplificar as duas respostas para comparar
    correct_n_simple, correct_d_simple = simplify_fraction(correct_n, common_d)
    user_n_simple, user_d_simple = simplify_fraction(st.session_state.ans_n, st.session_state.ans_d)

    # Verificar
    if (user_n_simple, user_d_simple) == (correct_n_simple, correct_d_simple):
        st.success("🚀 **CORRETO!** Resposta perfeita, Comandante! Veja a confirmação visual abaixo.")
    else:
        st.error(f"🚨 **QUASE LÁ!** Sua resposta foi {st.session_state.ans_n}/{st.session_state.ans_d}. A resposta correta é {correct_n}/{common_d}. Compare com a imagem abaixo e veja onde está a diferença.")

# Mostrar o resultado final se o botão foi pressionado
if st.session_state.step == 1:
    st.subheader("ETAPA 4: Confirmação Visual")
    result_img = create_fraction_bar_image(st.session_state.n1, st.session_state.d1, st.session_state.n2, st.session_state.d2, op_select, "Confirmação do Resultado", show_lcm=True, show_result=True)
    st.image(result_img, use_container_width=True)

if st.sidebar.button("Próximo Desafio (Limpar)", use_container_width=True):
    st.session_state.step = 0
    st.session_state.n1 = 1
    st.session_state.d1 = 2
    st.session_state.n2 = 1
    st.session_state.d2 = 3
    st.session_state.ans_n = 0
    st.session_state.ans_d = 1
    st.experimental_rerun() # Força a recarga da página com os valores resetados
