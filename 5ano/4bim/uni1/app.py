# (TRAVA BLINDADA DE CONTROLE ABSOLUTO)
# VERSÃO 4 - Reestruturação pedagógica completa baseada no feedback do Raphael.
# - Fluxo de Múltiplas Etapas: Problema > Teste de MMC > Explicação > Teste de Resposta Final > Confirmação Visual.
# - Responsividade: O texto das frações agora é gerado pelo Streamlit (HTML) e não na imagem, garantindo legibilidade em qualquer tela.
# - Visualização: Linhas divisórias das barras agora são pretas para melhor contraste.
# - Interatividade: Adiciona campo para testar o conhecimento do MMC.
# - Pedagogia: Inclui texto explicativo detalhado sobre como os numeradores são ajustados após encontrar o MMC.

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import math

# --- FUNÇÕES AUXILIARES ---
def lcm(a, b):
    return abs(a*b) // math.gcd(a, b) if a != 0 and b != 0 else 0

def simplify_fraction(n, d):
    if n == 0: return 0, 1
    if d == 0: return n, 0 # Avoid division by zero
    common_divisor = math.gcd(n, d)
    return n // common_divisor, d // common_divisor

# --- LÓGICA DE GERAÇÃO DA IMAGEM (AGORA SÓ GRÁFICOS) ---
def create_fraction_bar_image(n_list, d_list, colors, title=""):
    img_width = 800
    bar_height = 80
    padding = 20
    vertical_gap = 100
    img_height = padding * 2 + len(n_list) * bar_height + (len(n_list) - 1) * (vertical_gap - bar_height)

    bg_color = '#FFFFFF'
    outline_color = '#000000'

    image = Image.new('RGB', (img_width, img_height), bg_color)
    draw = ImageDraw.Draw(image)

    try:
        font_title = ImageFont.truetype("arialbd.ttf", 30)
    except IOError:
        font_title = ImageFont.load_default()

    if title:
        title_bbox = draw.textbbox((0, 0), title, font=font_title)
        title_w = title_bbox[2] - title_bbox[0]
        draw.text(((img_width - title_w) / 2, 10), title, font=font_title, fill=outline_color)

    bar_width = img_width - 2 * padding

    for i, (n, d, color) in enumerate(zip(n_list, d_list, colors)):
        y = padding + 50 + i * vertical_gap

        # Draw bar outline
        draw.rectangle([padding, y, padding + bar_width, y + bar_height], outline=outline_color, width=2)

        # Draw filled portion
        fill_width = (n / d) * bar_width if d != 0 else 0
        draw.rectangle([padding, y, padding + fill_width, y + bar_height], fill=color)

        # Draw divider lines in black for contrast
        for j in range(1, d):
            x = padding + (j / d) * bar_width
            draw.line([x, y, x, y + bar_height], fill=outline_color, width=2)

    return image

# --- LÓGICA DO APLICATIVO STREAMLIT ---
st.set_page_config(layout="wide", page_title="Laboratório de Frações")

# Inicializa o session_state para controlar o fluxo
if 'step' not in st.session_state: st.session_state.step = "INPUT_MMC"
if 'mmc_guess' not in st.session_state: st.session_state.mmc_guess = 0
if 'mmc_correct' not in st.session_state: st.session_state.mmc_correct = False
if 'n1' not in st.session_state: st.session_state.n1 = 1
if 'd1' not in st.session_state: st.session_state.d1 = 4
if 'n2' not in st.session_state: st.session_state.n2 = 1
if 'd2' not in st.session_state: st.session_state.d2 = 6

# --- LAYOUT DA SIDEBAR ---
st.sidebar.title("Missão: Orçamento")
st.sidebar.header("Painel de Controle")
op_select = st.sidebar.radio("Selecione a Operação:", ('Soma', 'Subtração'), key='op_sim')
st.sidebar.markdown("---")
st.session_state.n1 = st.sidebar.number_input("Numerador 1", min_value=1, value=st.session_state.n1, key="n1_key")
st.session_state.d1 = st.sidebar.number_input("Denominador 1", min_value=2, value=st.session_state.d1, key="d1_key")
st.sidebar.markdown("---")
st.session_state.n2 = st.sidebar.number_input("Numerador 2", min_value=1, value=st.session_state.n2, key="n2_key")
st.session_state.d2 = st.sidebar.number_input("Denominador 2", min_value=2, value=st.session_state.d2, key="d2_key")

if st.sidebar.button("🚀 Novo Desafio", use_container_width=True):
    st.session_state.step = "INPUT_MMC"
    st.session_state.mmc_correct = False
    st.session_state.mmc_guess = 0
    st.experimental_rerun()

# --- LAYOUT PRINCIPAL ---
st.title("Laboratório Interativo de Frações")

n1, d1, n2, d2 = st.session_state.n1, st.session_state.d1, st.session_state.n2, st.session_state.d2
correct_mmc = lcm(d1, d2)

# ETAPA 1: APRESENTAÇÃO DO PROBLEMA
st.header("ETAPA 1: O Problema")
st.info("Observe os orçamentos. Os 'pedaços' de cada barra têm o mesmo tamanho? Não podemos somar/subtrair pedaços de tamanhos diferentes!")

img_col1, text_col1 = st.columns([4, 1])
with img_col1:
    problem_img = create_fraction_bar_image([n1, n2], [d1, d2], ['#4A90E2', '#50E3C2'])
    st.image(problem_img)
with text_col1:
    st.markdown(f"<p style='font-size: 44px; font-weight: bold; margin-top: 70px;'>{n1}/{d1}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 44px; font-weight: bold; margin-top: 55px;'>{op_select[0]}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 44px; font-weight: bold; margin-top: 55px;'>{n2}/{d2}</p>", unsafe_allow_html=True)

# ETAPA 2: TESTE DO MMC
st.header("ETAPA 2: Encontrando o Denominador Comum")
if not st.session_state.mmc_correct:
    st.warning("Para somar, precisamos 're-dividir' as barras em pedaços iguais. Qual é o menor número de pedaços (MMC) que funciona para os denominadores {} e {}?".format(d1, d2))
    st.session_state.mmc_guess = st.number_input("Digite sua resposta para o MMC:", min_value=1, key="mmc_input")
    if st.button("Verificar MMC", type="primary"):
        if st.session_state.mmc_guess == correct_mmc:
            st.session_state.mmc_correct = True
            st.experimental_rerun()
        else:
            st.error(f"Incorreto. O MMC de {d1} e {d2} não é {st.session_state.mmc_guess}. Tente de novo! Dica: procure o primeiro número que aparece na tabuada dos dois.")

# ETAPA 3: EXPLICAÇÃO E TESTE DA RESPOSTA FINAL
if st.session_state.mmc_correct:
    st.success(f"**Exato!** O denominador comum é **{correct_mmc}**.")

    n1_equiv = n1 * (correct_mmc // d1)
    n2_equiv = n2 * (correct_mmc // d2)

    st.info("Agora que as barras estão divididas igualmente, veja como as frações originais se transformam:")

    img_col2, text_col2 = st.columns([4, 1])
    with img_col2:
        equiv_img = create_fraction_bar_image([n1_equiv, n2_equiv], [correct_mmc, correct_mmc], ['#4A90E2', '#50E3C2'])
        st.image(equiv_img)
    with text_col2:
        st.markdown(f"""
        <p style='font-size: 20px; margin-top: 60px;'>Original: <strong>{n1}/{d1}</strong></p>
        <p style='font-size: 44px; font-weight: bold;'>{n1_equiv}/{correct_mmc}</p>
        <p style='font-size: 20px; margin-top: 70px;'>Original: <strong>{n2}/{d2}</strong></p>
        <p style='font-size: 44px; font-weight: bold;'>{n2_equiv}/{correct_mmc}</p>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    > **Como chegamos nisso?**
    > * Para a primeira fração ($$\\frac{{{n1}}}{{{d1}}}$$): dividimos o MMC pelo denominador ($${correct_mmc} \\div {d1} = {correct_mmc//d1}$$). Depois, multiplicamos o numerador por esse resultado ($${n1} \\times {correct_mmc//d1} = {n1_equiv}$$).
    > * Para a segunda fração ($$\\frac{{{n2}}}{{{d2}}}$$): fazemos o mesmo ($${correct_mmc} \\div {d2} = {correct_mmc//d2}$$), e então ($${n2} \\times {correct_mmc//d2} = {n2_equiv}$$).
    """)

    st.header("ETAPA 4: Qual é a Resposta Final?")
    st.warning(f"Calcule o resultado de $$\\frac{{{n1_equiv}}}{{{correct_mmc}}} {op_select[0]} \\frac{{{n2_equiv}}}{{{correct_mmc}}}$$ e digite sua resposta abaixo.")

    ans_n = st.number_input("Seu Numerador Final:", min_value=0, key="ans_n_final")
    ans_d = st.number_input("Seu Denominador Final:", min_value=1, key="ans_d_final")

    if st.button("Verificar Resposta Final", type="primary"):
        st.session_state.step = "SHOW_FINAL"

# ETAPA 5: CONFIRMAÇÃO VISUAL FINAL
if st.session_state.step == "SHOW_FINAL":
    if op_select == 'Soma':
        correct_n_final = n1_equiv + n2_equiv
    else:
        correct_n_final = n1_equiv - n2_equiv

    user_n_simple, user_d_simple = simplify_fraction(st.session_state.ans_n_final, st.session_state.ans_d_final)
    correct_n_simple, correct_d_simple = simplify_fraction(correct_n_final, correct_mmc)

    if (user_n_simple, user_d_simple) == (correct_n_simple, correct_d_simple):
        st.success("🚀 **PERFEITO, COMANDANTE!** Cálculo exato. Missão cumprida!")
    else:
        st.error(f"🚨 **RECALCULANDO...** Sua resposta foi $$\\frac{{{st.session_state.ans_n_final}}}{{{st.session_state.ans_d_final}}}$$. A resposta correta é $$\\frac{{{correct_n_final}}}{{{correct_mmc}}}$$. Compare com a confirmação visual.")

    st.header("ETAPA 5: Confirmação Visual do Resultado")
    img_col3, text_col3 = st.columns([4, 1])
    with img_col3:
        final_img = create_fraction_bar_image([n1_equiv, n2_equiv, correct_n_final], [correct_mmc, correct_mmc, correct_mmc], ['#4A90E2', '#50E3C2', '#E34A7F'], title="Resultado Final")
        st.image(final_img)
    with text_col3:
         st.markdown(f"<p style='font-size: 44px; font-weight: bold; margin-top: 70px;'>{n1_equiv}/{correct_mmc}</p>", unsafe_allow_html=True)
         st.markdown(f"<p style='font-size: 44px; font-weight: bold; margin-top: 55px;'>{op_select[0]}</p>", unsafe_allow_html=True)
         st.markdown(f"<p style='font-size: 44px; font-weight: bold; margin-top: 55px;'>{n2_equiv}/{correct_mmc}</p>", unsafe_allow_html=True)
         st.markdown(f"<p style='font-size: 44px; font-weight: bold; margin-top: 55px;'>=</p>", unsafe_allow_html=True)
         st.markdown(f"<p style='font-size: 44px; font-weight: bold; margin-top: 55px; color: #E34A7F;'>{correct_n_final}/{correct_mmc}</p>", unsafe_allow_html=True)
