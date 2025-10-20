# (TRAVA BLINDADA DE CONTROLE ABSOLUTO)
# VERSÃO 8 - Correção de Bugs e Refinamento Final
# - CORRIGIDO (TypeError): Os inputs agora são tratados como inteiros, prevenindo o erro 'float object cannot be interpreted as an integer'.
# - MELHORADO (Layout): O texto das frações agora é renderizado com st.latex() para uma aparência matemática perfeita e tamanho consistente.
# - CORRIGIDO (Alinhamento): O layout foi refeito para garantir o alinhamento vertical entre a barra e a fração em LaTeX.
# - REMOVIDO: O aviso de 'use_column_width' foi eliminado.

import streamlit as st
from PIL import Image, ImageDraw
import io
import math

# --- FUNÇÕES AUXILIARES ---
def lcm(a, b):
    return abs(a*b) // math.gcd(int(a), int(b)) if a != 0 and b != 0 else 0

def simplify_fraction(n, d):
    n, d = int(n), int(d) # Garante que os números sejam inteiros
    if n == 0: return 0, 1
    if d == 0: return n, 0
    common_divisor = math.gcd(n, d)
    return n // common_divisor, d // common_divisor

def get_simultaneous_factorization_hint(a, b):
    temp_a, temp_b = int(a), int(b)
    d = 2
    hint_str = f"**Dica: Fatoração Simultânea**\n\n```\n{a}, {b} | "
    while temp_a > 1 or temp_b > 1:
        if temp_a % d == 0 or temp_b % d == 0:
            hint_str += f"{d}\n"
            if temp_a % d == 0: temp_a //= d
            if temp_b % d == 0: temp_b //= d
            hint_str += f"{temp_a}, {temp_b} | "
        else:
            d += 1
            if d > max(a, b) + 1: break
    hint_str = hint_str.rstrip("| ") + "\n```\n\nAgora, multiplique os fatores à direita da linha."
    return hint_str

# --- LÓGICA DE GERAÇÃO DA IMAGEM ---
@st.cache_data
def create_fraction_bar_image(n, d, color):
    n, d = int(n), int(d)
    img_width, bar_height, padding = 700, 60, 5 # Barra um pouco menor
    bg_color, outline_color = '#FFFFFF', '#000000'
    image = Image.new('RGB', (img_width, bar_height + 2*padding), bg_color)
    draw = ImageDraw.Draw(image)
    bar_width = img_width - 2 * padding
    y = padding

    fill_width = (n / d) * bar_width if d != 0 else 0
    draw.rectangle([padding, y, padding + fill_width, y + bar_height], fill=color)
    draw.rectangle([padding, y, padding + bar_width, y + bar_height], outline=outline_color, width=3)
    for j in range(1, d):
        x = padding + (j / d) * bar_width
        draw.line([x, y, x, y + bar_height], fill=outline_color, width=3)
    return image

# --- LÓGICA DO APLICATIVO STREAMLIT ---
st.set_page_config(layout="centered", page_title="Laboratório de Frações")

def reset_progress():
    st.session_state.step = "INPUT_MMC"
    st.session_state.mmc_correct = False
    st.session_state.mmc_guess = 0
    st.session_state.ans_n = 0
    st.session_state.ans_d = 1
    if "mmc_input" in st.session_state: del st.session_state["mmc_input"]
    if "ans_n_final" in st.session_state: del st.session_state["ans_n_final"]
    if "ans_d_final" in st.session_state: del st.session_state["ans_d_final"]

if 'step' not in st.session_state: reset_progress()

# --- SIDEBAR ---
with st.sidebar:
    st.title("Missão: Orçamento")
    st.header("Painel de Controle")
    op_select = st.radio("Selecione a Operação:", ('Soma', 'Subtração'), key='op_sim', on_change=reset_progress)
    st.markdown("---")
    # Força o input a ser um inteiro com step=1
    n1 = st.number_input("Numerador 1", min_value=1, value=1, step=1, key="n1_key", on_change=reset_progress)
    d1 = st.number_input("Denominador 1", min_value=2, value=4, step=1, key="d1_key", on_change=reset_progress)
    st.markdown("---")
    n2 = st.number_input("Numerador 2", min_value=1, value=1, step=1, key="n2_key", on_change=reset_progress)
    d2 = st.number_input("Denominador 2", min_value=2, value=6, step=1, key="d2_key", on_change=reset_progress)
    st.markdown("---")
    st.button("🚀 Novo Desafio (Limpar)", use_container_width=True, on_click=reset_progress)

# --- LAYOUT PRINCIPAL ---
st.title("Laboratório Interativo de Frações")

correct_mmc = lcm(d1, d2)
op_symbol_latex = '+' if op_select == 'Soma' else '-'

# Componente para exibir uma linha de fração (imagem + texto em LaTeX)
def display_fraction_component(n, d, color, label=""):
    col1, col2 = st.columns([5, 2])
    with col1:
        if label:
            st.caption(label)
        st.image(create_fraction_bar_image(n, d, color), use_container_width=True)
    with col2:
        # Usando CSS para alinhar verticalmente o LaTeX
        st.markdown(f"<div style='height: 100%; display: flex; align-items: center; justify-content: center;'>", unsafe_allow_html=True)
        st.latex(f"\\frac{{{int(n)}}}{{{int(d)}}}")
        st.markdown("</div>", unsafe_allow_html=True)

st.header("ETAPA 1: O Problema")
st.info("Observe: os 'pedaços' de cada barra têm tamanhos diferentes. Não podemos somá-los diretamente!")
display_fraction_component(n1, d1, '#4A90E2')
st.latex(f"\\huge {op_symbol_latex}")
display_fraction_component(n2, d2, '#50E3C2')

st.header("ETAPA 2: Encontrando o Denominador Comum")
mmc_guess = st.number_input(f"Qual é o denominador comum (MMC) para {d1} e {d2}?", min_value=1, step=1, key="mmc_input")

if st.button("Verificar MMC", type="primary"):
    if int(mmc_guess) == correct_mmc:
        st.session_state.mmc_correct = True
        st.success(f"**Exato!** O denominador comum é **{correct_mmc}**.")
    else:
        st.session_state.mmc_correct = False
        st.error("Ainda não é esse. Veja uma dica para encontrar o número certo:")
        st.markdown(get_simultaneous_factorization_hint(d1, d2))

if st.session_state.get('mmc_correct', False):
    n1_equiv, n2_equiv = n1 * (correct_mmc // d1), n2 * (correct_mmc // d2)

    st.header("ETAPA 3: Criando Frações Equivalentes")
    st.info("Agora que sabemos o denominador comum, precisamos transformar as frações originais.")
    with st.container(border=True):
        st.markdown("> **A Regra de Ouro:** Para a fração não perder o valor, o mesmo número que multiplica o de baixo (denominador) também tem que multiplicar o de cima (numerador).")

        st.markdown(f"##### Fração 1: $$\\frac{{{n1}}}{{{d1}}}$$")
        multiplier1 = correct_mmc // d1
        st.write(f"Que número vezes **{d1}** resulta no MMC **{correct_mmc}**? A resposta é **{multiplier1}**.")
        st.latex(f"\\text{{Então, multiplicamos em cima e embaixo:}} \\quad \\frac{{{n1} \\times {multiplier1}}}{{{d1} \\times {multiplier1}}} = \\frac{{{n1_equiv}}}{{{correct_mmc}}}")
        display_fraction_component(n1_equiv, correct_mmc, '#4A90E2')
        st.markdown("---")

        st.markdown(f"##### Fração 2: $$\\frac{{{n2}}}{{{d2}}}$$")
        multiplier2 = correct_mmc // d2
        st.write(f"Que número vezes **{d2}** resulta no MMC **{correct_mmc}**? A resposta é **{multiplier2}**.")
        st.latex(f"\\text{{Então, multiplicamos em cima e embaixo:}} \\quad \\frac{{{n2} \\times {multiplier2}}}{{{d2} \\times {multiplier2}}} = \\frac{{{n2_equiv}}}{{{correct_mmc}}}")
        display_fraction_component(n2_equiv, correct_mmc, '#50E3C2')

    st.header("ETAPA 4: Qual é a Resposta Final?")
    st.warning(f"Calcule $$\\frac{{{n1_equiv}}}{{{correct_mmc}}} {op_symbol_latex} \\frac{{{n2_equiv}}}{{{correct_mmc}}}$$ e digite sua resposta.")
    ans_n = st.number_input("Seu Numerador Final:", step=1, key="ans_n_final")
    ans_d = st.number_input("Seu Denominador Final:", min_value=1, value=correct_mmc, step=1, key="ans_d_final")
    if st.button("Verificar Resposta Final", type="primary"):
        st.session_state.step = "SHOW_FINAL"

if st.session_state.get('step') == "SHOW_FINAL" and st.session_state.get('mmc_correct', False):
    if op_select == 'Soma': correct_n_final = n1_equiv + n2_equiv
    else: correct_n_final = n1_equiv - n2_equiv

    user_n_simple, user_d_simple = simplify_fraction(st.session_state.ans_n_final, st.session_state.ans_d_final)
    correct_n_simple, correct_d_simple = simplify_fraction(correct_n_final, correct_mmc)

    if (user_n_simple, user_d_simple) == (correct_n_simple, correct_d_simple):
        st.success("🚀 **PERFEITO, COMANDANTE!** Cálculo exato.")
    else:
        st.error(f"🚨 **RECALCULANDO...** Sua resposta foi $$\\frac{{{st.session_state.ans_n_final}}}{{{st.session_state.ans_d_final}}}$$. A resposta correta é $$\\frac{{{correct_n_final}}}{{{correct_mmc}}}$$.")

    st.header("ETAPA 5: Confirmação Visual")
    display_fraction_component(correct_n_final, correct_mmc, '#E34A7F', label="Barra de Resultado")
