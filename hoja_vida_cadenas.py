"""
=============================================================================
SOLICITUDES DE OUTSOURCING - ARL BOLÍVAR
App Streamlit — Sin st.form, dinámico + Excel + PDF cédula por correo
=============================================================================
"""

import streamlit as st
import holidays
import datetime
import smtplib
import os
import io
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import openpyxl
from openpyxl.drawing.image import Image as XLImage
from openpyxl.utils.cell import coordinate_from_string
from openpyxl.utils import column_index_from_string as col_idx
import urllib.request
from supabase import create_client

# ─────────────────────────────────────────────────────────────────────────────
# 0. CONEXION SUPABASE
# ─────────────────────────────────────────────────────────────────────────────


SUPABASE_URL = "https://oofpblylbudmpeppqbou.supabase.co"
SUPABASE_KEY = "sb_publishable_BupeaEOOMqELWtuMzPvoVg_cOe0hXhl"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ─────────────────────────────────────────────────────────────────────────────
# 1. CONFIGURACIÓN GENERAL
# ─────────────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Hoja de vida Supermercados",
    page_icon="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAHO0lEQVR4Aa1WA3gkzRY9k6xt28qo4/yOR+FM9Nu2bds214zNxWwwEydr296deufV2v1w+rtfVavuuefeut1QC+UbtI11YnRcFeJor9jd+Mnhwox4msONHzi+GO+G1bwYozAV3vh/ITwLnenwroRaZNprsD+1FSK5mdZEa5TGOeS1FN5LcGOPvRYL4ly45eoCdMD/gthqWBy1KE/h4qkrNIJRr0qowSySecpeicSEpQiNruwUHdky1GF2dXvGVD10Wqyr05rEps6C7wgSKbK6EI7/FGFOdGe0nznqcTR1GeRCiVVIs1agPyReagddzC+0adDHTIXO9oa8BuHVsWDGEJ3zRoe/01QQW9vtWFI9DlGNd5V16AQ1CF2E3gkuzElbCeGow1YSeSQqHd3OLghLHyjWTfCLeZPjU7RVtBCcgtDgAdF3YPEvDwQvtTSntLYTiW78E1yKrrgUzC70ZDHNo3NGDXesCwouhCERveBr2wA/WzYMlnkwkswUSxDOA4n8La4dVfpBWYy71zG7C9P/XVO4IOzwZuTfnHDuYo4n4SKQCvhZ10OxPc803AyjrYVzOy6GT8WVfUrSnRZXnyNJLnyIl+CFc8Eb9qRGHLXXY0NcJXS4FAZaOlHyj6GYv6Pz76HEPInewZeW92cR0bMkq9nq6rGDSpjPDr4cvVhkbm4lwZt3Qx000JtvZAqSoBZ/iTeHlP660+HWlNgL0AUnEV+HJ1OXQ8TXIp1He6jB+MjxMFqWw9fahEkhw6AGM0VvZIkS/8XJW9i87gWIq8mEUS9KbsGRuBrYoBaK5WMS+IwK/MRUvAy1mOu5vWuR+5C1ptuswKnoiMgaGB0NOMwCbAyvRmeogT5qEnO/gyScLL4quQsMQcOhBrM8QzFfrJ1Q8cLye9yYKOVnCxXcft9CLQzRd0NveQcTQsfBh6nwZ0EaLDdALeZ70rsWVe40Ofs4wEazgL1csOvdiCnxE6AzmaG3xkA2FqXt6ZzbxsNgmghC7nm9WXcGIV+qYcQUqxbaaAt8zDaex2K4rgcGRPUl2Wi55pTIIABeyBEvIO/YweAloZ/D4UILPyjihvXwxRTbd/CPWcqc/somw9HyIEAMCexImRfRKtE/vDOdh7EP8H7UaOlU4dwn0giDdSb8YhcyLXw/5k/oIkdQmQTOV0KJ/Z3rVWNyxOMkEIMiIYaVffMPbDW9VnPvi9SNGMWm8rPMq5HyKhY3nbwCgvO7ZMdTzLNI4mEQVOoJOs7ns6Vc/O4Tz2XwuWJef4818jYGhfaGwZbMZ1r47lMMqgK66LeQ6zGCBNrmLs9DwGJTdVIDxPU7MFJ+YBRLHvSMnIvxhW+kjEYyN1oLSCiHYz18fHpKKQ18VrHOAXGKgGKbC535YehItL+2syTArcq1ZvD9Veg0YSDyhYJCIZB/qAHjKl7MSmmiAmys0NKhv83FXM/kwktgND8EgzlZRmpglAYqoZjzoZhuA0Fn75PcizgBzmdT7kqZCkmEKWCLhpHpGH51B6qyANrwZ5AhbKACyBOL0K8444eEeu/D9kbcgF7mwdBF+Mti4VYDhEY2GW1QP5zEuKv7wCd0FBfqx2f8oEQa5RzQcBwpC1JrCoBPVKBUQEcFeR2ETMlI7ThkHH7eq1gI1sKXQLa4+ypn0M4kt/ptiElXd6EqZVQjFzLvtn8wZkx7qEWW+AdlQiBT3Ap8LK4YW/b2Onudd7VlLjqp7IJ9KOda2QH9LLdLmaHyP3CGZyAjX0P592KumAB8LrpocvbOvK7SZ1+yC2aoAf8HqMA6Op5O+472vGoCOZ40LBQC2Z50vCTaQGKWeKFfycwd8S7vqfZatMPl4BfbmwpspOMvOL4IfczjANrgcpgtujLlxSgVx5DnuQen8Ifow7w49Ytv3ZrSgFsuXwOT2slPsZ/1AXCncLxZlQKZ4imUy+IrxVTRBWchXSQib/+OwEWmyltqMQmXgNxSBsuj3HYvwc/8gmy7gNdlCi8AhZ7NmiJxELkiHOfBLrzJ8Gfv3J2HfBcnL3jAjdGXLkLrFkb/gSTha14lt97FME/o6LQVFTL6j6SvC2Kq6I4MT7omf/eBseUvpadUYuzFf0qtG1iIWfC1ZHMsZ48femHZPcHIF3Vg4WlyxZ+s/MvstHTRF3kiU1N6THQvWuicXPFIctS5f0n6qL7M+0r5oaEKsiewN+BMzBI9uM4jtJ0y77lihgxQFfggpfpMUyCEV/6+/V2LnH+1L6kM71166seTX8ToHyhFL4DktJHfYvxVVhCYI/oj3ZPGaCtks8kXR7jW2/jmApGrqNoETY5Y5FVCIoWHBYu0Hrn7vvXK3HcPprXGY+6uIBZXCGZtT8XMzS/y2VmMeJV0XCTzXUQz438CmdPJfYwoj7ZPUyqE7OOFZ1iRkMZ7dOrZjVxPFsnfQSXb4f+GT0R7RjNKLpwtfmEjKeC4HKxujvm89xPnN5PsSLyk3vG/AJw8UVr0m/g8AAAAAElFTkSuQmCC",
    layout="wide"
)

LOGOS_CADENAS = [
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/9cm/91g/drj/idf3hb0pKj_1775769551319.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/g6l/m9o/nrr/idmJvu77_g_1774995536838.png",      # ← ya está aquí el principal
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/by2/zpo/8zp/Imagen2.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/y84/x9o/n49/Imagen3.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/mhs/5yf/cep/Imagen4.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/zhp/b9c/wd8/Imagen5.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/5iy/ogw/w78/Imagen6.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/1vj/68t/9o2/Imagen7.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/pgq/jz2/rls/Imagen8.png",
]

# ─────────────────────────────────────────────────────────────────────────────
# 2. FUNCIONES AUXILIARES
# ─────────────────────────────────────────────────────────────────────────────


def insertar_hoja_vida(data: dict):
    """
    Inserta un registro en la tabla hoja_vida_cadenas_farmacias.
    Retorna (True, id) si fue exitoso, (False, mensaje_error) si falló.
    """
    try:
        response = (
            supabase
            .table("hoja_vida_supermercados")
            .insert(data)
            .execute()
        )
        inserted_id = response.data[0]["id"] if response.data else None
        return True, inserted_id
    except Exception as e:
        return False, str(e)


# ─────────────────────────────────────────────────────────────────────────────
# 3. INTERFAZ STREAMLIT
# ─────────────────────────────────────────────────────────────────────────────


def main():
    st.markdown("""
    <style>
    .section-header {
        background: #10384f; color: white; padding: 8px 14px;
        border-radius: 6px; font-weight: 600; font-size: 0.95rem; margin: 20px 0 10px 0;
    }
    .info-box {
        background: #d4e6f1; border-left: 4px solid #10384f;
        padding: 10px 14px; border-radius: 4px; font-size: 0.88rem; margin: 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Logos ---
    logos_html = "".join([
        f'<img src="{url}" style="height:60px;width:auto;object-fit:contain;margin:0 10px;">'
        for url in LOGOS_CADENAS
    ])
    st.markdown(f"""
        <div style="display:flex;align-items:center;justify-content:center;
            flex-wrap:wrap;gap:10px;padding:10px 0;background:white;border-radius:8px;">
            {logos_html}
        </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("## Hoja de vida PDV Supermercados")
    st.markdown("**Bayer** — Complete el formulario y presione **Enviar Solicitud**.")
    st.divider()

    # ══════════════════════════════════════════════════════════════════
    # I. INFORMACIÓN GENERAL
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">I. INFORMACIÓN GENERAL DE SOLICITUD</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fecha_info      = st.date_input("Fecha información (D/M/A)")
        nombre_cadena   = st.selectbox("Nombre de la cadena", [
            "Exito", "Carulla", "Surtumax",
            "Cencosud", "Jumbo", "Metro","Olimpica"])
        punto_de_venta  = st.text_input("Punto de venta")
        dependenci_pdv  = st.text_input("Dependencia / Código SICOL PDV")
        telefono        = st.text_input("Teléfono")
        direccion       = st.text_input("Dirección")
        nombre_gerente  = st.text_input("Nombre Gerente / Administrador PDV")
        nombre_contacto = st.text_input("Nombre y cargo contacto clave")

    with col2:
        ranking_nac     = st.text_input("Ranking PDV total nacional")
        ranking_cad_nac = st.text_input("Ranking PDV cadena nacional")
        ranking_cad_reg = st.text_input("Ranking PDV cadena regional")
        ranking_zona    = st.text_input("Ranking PDV zona asignada")
        tiene_domicilio = st.radio("¿Tiene domicilio?", ["Sí", "No"], horizontal=True)

    st.markdown("**Domicilio**")
    col3, col4 = st.columns(2)
    with col3:
        centralizado   = st.checkbox("Centralizado")
        pdv_check      = st.checkbox("PDV")

    # ── Bloque Estructura PDV eliminado ──
    # ── Bloque Ubicación eliminado ──

    st.markdown("**Logística**")
    col9, col10 = st.columns(2)
    with col9:
        entrega_merc = st.radio("Entrega de mercancía",
                                ["Punto de venta", "Bodega central"], horizontal=True)
        DIAS_SEMANA  = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        dias_pedido  = st.multiselect("Días de pedido", options=DIAS_SEMANA,
                                    placeholder="Seleccione uno o más días")
        dias_visita  = st.multiselect("Días de visita", options=DIAS_SEMANA,
                                    placeholder="Seleccione uno o más días")
        operador_log = st.radio("¿Tiene operador logístico?", ["Sí", "No"], horizontal=True)
    with col10:
        frecuencia_ped = st.selectbox("Frecuencia de pedido",
                                    ["Diario", "Semanal", "2 veces x sem", "3 veces x sem"])
        horario_obs    = st.text_input("Horario recibo obsequios")
        intensidad_h   = st.number_input("Intensidad horaria en la semana", 0, step=1)

    st.markdown("**Ventas promedio mensuales**")
    col11, col12, col13 = st.columns(3)
    with col11:
        ventas_mes  = st.number_input("Venta prom. mes total ($)", 0, step=1000)
    with col12:
        venta_otc   = st.number_input("Venta prom. mes OTC ($)", 0, step=1000)
    with col13:
        venta_foot  = st.number_input("Venta prom. mes Foot Care ($)", 0, step=1000)

    st.markdown("**Top marcas más vendidas**")
    marcas = []
    for i in range(1, 6):
        c1, c2 = st.columns([3, 1])
        with c1:
            marca = st.text_input(f"Marca {i}", key=f"marca_{i}")
        with c2:
            vta_m = st.number_input(f"Vtas prom mes marca {i}", 0, step=1000, key=f"vta_marca_{i}", label_visibility="visible")
        marcas.append({"marca": marca, "vtas_prom_mes": vta_m})

    st.markdown("**Top SKUs más vendidos**")
    skus = []
    for i in range(1, 6):
        c1, c2 = st.columns([3, 1])
        with c1:
            sku = st.text_input(f"SKU {i}", key=f"sku_{i}")
        with c2:
            vta_s = st.number_input(f"Vtas prom mes SKU {i}", 0, step=1000, key=f"vta_sku_{i}", label_visibility="visible")
        skus.append({"sku": sku, "vtas_prom_mes": vta_s})

    # ══════════════════════════════════════════════════════════════════
    # II. SELL OUT
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">II. SELL OUT</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Ingrese ventas mes puntual y acumulado por año (2020 vs 2021). La Var% se calcula automáticamente.</div>', unsafe_allow_html=True)

    # ── Tabla 1: Sell Out mensual ──────────────────────────────────────
    st.markdown("#### Ventas Bayer — Sell Out mensual")

    MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
            "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

    # Encabezado de la tabla mensual
    header = st.columns([2, 1, 1, 1, 0.2, 1, 1, 1])
    header[0].markdown("")
    header[1].markdown("<div style='text-align:center;background:#10384f;color:white;padding:4px;border-radius:4px;font-size:0.78rem;'>Sell Out Mes</div>", unsafe_allow_html=True)
    header[5].markdown("<div style='text-align:center;background:#10384f;color:white;padding:4px;border-radius:4px;font-size:0.78rem;'>Sell Out Acumulado</div>", unsafe_allow_html=True)

    sub_header = st.columns([2, 1, 1, 1, 0.2, 1, 1, 1])
    for col, lbl in zip(sub_header, ["**Mes**", "**2020**", "**2021**", "**Var %**", "", "**2020**", "**2021**", "**Var %**"]):
        col.markdown(lbl)

    sell_out_data = []
    for mes in MESES:
        cols = st.columns([2, 1, 1, 1, 0.2, 1, 1, 1])
        cols[0].markdown(mes)
        p20 = cols[1].number_input(f"Mes 2020 {mes}", 0, step=1000, key=f"so_p20_{mes}", label_visibility="collapsed")
        p21 = cols[2].number_input(f"Mes 2021 {mes}", 0, step=1000, key=f"so_p21_{mes}", label_visibility="collapsed")
        var_p = round(((p21 - p20) / p20 * 100) if p20 > 0 else 0.0, 1)
        cols[3].markdown(f"<div style='text-align:center;padding-top:8px;color:{'green' if var_p >= 0 else 'red'};'><b>{var_p:+.1f}%</b></div>", unsafe_allow_html=True)
        cols[4].markdown("")  # separador visual
        a20 = cols[5].number_input(f"Acum 2020 {mes}", 0, step=1000, key=f"so_a20_{mes}", label_visibility="collapsed")
        a21 = cols[6].number_input(f"Acum 2021 {mes}", 0, step=1000, key=f"so_a21_{mes}", label_visibility="collapsed")
        var_a = round(((a21 - a20) / a20 * 100) if a20 > 0 else 0.0, 1)
        cols[7].markdown(f"<div style='text-align:center;padding-top:8px;color:{'green' if var_a >= 0 else 'red'};'><b>{var_a:+.1f}%</b></div>", unsafe_allow_html=True)
        sell_out_data.append({
            "mes": mes,
            "sell_out_mes_2020": p20, "sell_out_mes_2021": p21, "var_pct_mes": var_p,
            "sell_out_acum_2020": a20, "sell_out_acum_2021": a21, "var_pct_acum": var_a,
        })

    # Fila TOTAL
    totales_cols = st.columns([2, 1, 1, 1, 0.2, 1, 1, 1])
    tot_p20 = sum(r["sell_out_mes_2020"] for r in sell_out_data)
    tot_p21 = sum(r["sell_out_mes_2021"] for r in sell_out_data)
    tot_a20 = sum(r["sell_out_acum_2020"] for r in sell_out_data)
    tot_a21 = sum(r["sell_out_acum_2021"] for r in sell_out_data)
    var_tp = round(((tot_p21 - tot_p20) / tot_p20 * 100) if tot_p20 > 0 else 0.0, 1)
    var_ta = round(((tot_a21 - tot_a20) / tot_a20 * 100) if tot_a20 > 0 else 0.0, 1)

    style_total = "background:#b8cce4;padding:4px 6px;border-radius:4px;font-weight:700;font-size:0.82rem;"
    totales_cols[0].markdown(f"<div style='{style_total}'>TOTAL</div>", unsafe_allow_html=True)
    totales_cols[1].markdown(f"<div style='{style_total}'>{tot_p20:,.0f}</div>", unsafe_allow_html=True)
    totales_cols[2].markdown(f"<div style='{style_total}'>{tot_p21:,.0f}</div>", unsafe_allow_html=True)
    totales_cols[3].markdown(f"<div style='{style_total};color:{'green' if var_tp >= 0 else 'red'}'>{var_tp:+.1f}%</div>", unsafe_allow_html=True)
    totales_cols[4].markdown("")
    totales_cols[5].markdown(f"<div style='{style_total}'>{tot_a20:,.0f}</div>", unsafe_allow_html=True)
    totales_cols[6].markdown(f"<div style='{style_total}'>{tot_a21:,.0f}</div>", unsafe_allow_html=True)
    totales_cols[7].markdown(f"<div style='{style_total};color:{'green' if var_ta >= 0 else 'red'}'>{var_ta:+.1f}%</div>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Tabla 2: Sell Out por Marca / División ─────────────────────────
    st.markdown("#### Sell Out por Marca — Promedio mensual")

    MARCAS_SO = {
        "FOOT CARE": ["MEXSANA TALCO", "MEXSANA SPRAY"],
        "OTC": ["ACID MANTLE", "REDOXON", "ALKA-SELTZER", "ASPIRIN CARDIO",
                "GYNOCANESTEN", "APRONAX", "ASPIRINA DOLOR", "OTRAS"],
    }

    # Encabezado tabla marcas
    hdr = st.columns([1.5, 2, 1, 1.2, 1.2, 1])
    for col, lbl in zip(hdr, ["**División**", "**Marca**", "**Peso %**", "**Prom mes 2020**", "**Prom mes 2021**", "**Var %**"]):
        col.markdown(lbl)

    sell_out_marcas = []
    for division, marcas_list in MARCAS_SO.items():
        rows_div = []
        for idx, marca in enumerate(marcas_list):
            row = st.columns([1.5, 2, 1, 1.2, 1.2, 1])
            # Mostrar División solo en la primera fila del grupo
            if idx == 0:
                row[0].markdown(f"<div style='padding-top:8px;font-weight:600;'>{division}</div>", unsafe_allow_html=True)
            else:
                row[0].markdown("")
            row[1].markdown(f"<div style='padding-top:8px;'>{marca}</div>", unsafe_allow_html=True)
            peso   = row[2].number_input(f"Peso% {marca}", 0.0, 100.0, step=0.1, key=f"som_peso_{marca}", label_visibility="collapsed")
            pm20   = row[3].number_input(f"Prom 2020 {marca}", 0, step=1000, key=f"som_p20_{marca}", label_visibility="collapsed")
            pm21   = row[4].number_input(f"Prom 2021 {marca}", 0, step=1000, key=f"som_p21_{marca}", label_visibility="collapsed")
            var_m  = round(((pm21 - pm20) / pm20 * 100) if pm20 > 0 else 0.0, 1)
            row[5].markdown(f"<div style='text-align:center;padding-top:8px;color:{'green' if var_m >= 0 else 'red'};'><b>{var_m:+.1f}%</b></div>", unsafe_allow_html=True)
            rows_div.append({"division": division, "marca": marca, "peso_pct": peso,
                            "prom_mes_2020": pm20, "prom_mes_2021": pm21, "var_pct": var_m})

        # Subtotal por división
        sub_cols = st.columns([1.5, 2, 1, 1.2, 1.2, 1])
        st_p20 = sum(r["prom_mes_2020"] for r in rows_div)
        st_p21 = sum(r["prom_mes_2021"] for r in rows_div)
        var_st = round(((st_p21 - st_p20) / st_p20 * 100) if st_p20 > 0 else 0.0, 1)
        st_style = "background:#d9d9d9;padding:4px 6px;border-radius:4px;font-weight:700;font-size:0.82rem;"
        sub_cols[0].markdown("")
        sub_cols[1].markdown(f"<div style='{st_style}'>TOTAL {division}</div>", unsafe_allow_html=True)
        sub_cols[2].markdown(f"<div style='{st_style}'></div>", unsafe_allow_html=True)
        sub_cols[3].markdown(f"<div style='{st_style}'>{st_p20:,.0f}</div>", unsafe_allow_html=True)
        sub_cols[4].markdown(f"<div style='{st_style}'>{st_p21:,.0f}</div>", unsafe_allow_html=True)
        sub_cols[5].markdown(f"<div style='{st_style};color:{'green' if var_st >= 0 else 'red'}'>{var_st:+.1f}%</div>", unsafe_allow_html=True)

        sell_out_marcas.extend(rows_div)

    # TOTAL GENERAL marcas
    all_pm20 = sum(r["prom_mes_2020"] for r in sell_out_marcas)
    all_pm21 = sum(r["prom_mes_2021"] for r in sell_out_marcas)
    var_all  = round(((all_pm21 - all_pm20) / all_pm20 * 100) if all_pm20 > 0 else 0.0, 1)
    tot_cols = st.columns([1.5, 2, 1, 1.2, 1.2, 1])
    tot_style = "background:#b8cce4;padding:4px 6px;border-radius:4px;font-weight:700;font-size:0.82rem;"
    tot_cols[0].markdown(f"<div style='{tot_style}'>TOTAL</div>", unsafe_allow_html=True)
    tot_cols[1].markdown(f"<div style='{tot_style}'></div>", unsafe_allow_html=True)
    tot_cols[2].markdown(f"<div style='{tot_style}'></div>", unsafe_allow_html=True)
    tot_cols[3].markdown(f"<div style='{tot_style}'>{all_pm20:,.0f}</div>", unsafe_allow_html=True)
    tot_cols[4].markdown(f"<div style='{tot_style}'>{all_pm21:,.0f}</div>", unsafe_allow_html=True)
    tot_cols[5].markdown(f"<div style='{tot_style};color:{'green' if var_all >= 0 else 'red'}'>{var_all:+.1f}%</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # III. EXHIBICIÓN (Mobile-first)
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">III. EXHIBICIÓN</div>', unsafe_allow_html=True)
    st.caption("* Indique la cantidad y entre paréntesis el mes. Ejemplo: 2 (Ene)")

    MARCAS_EXH = ["Mexsana", "Acid Mantle", "Redoxon", "Alka Seltzer"]
    NUM_FILAS_EXH = 10

    exhibicion_rows = []
    for i in range(1, NUM_FILAS_EXH + 1):
        with st.expander(f"📋 Exhibición {i}", expanded=(i == 1)):
            tipo = st.text_input("Tipo de Exhibición", key=f"exh_tipo_{i}", placeholder="Ej: Counter, Vitrina, Góndola...")
            row = {"tipo": tipo}

            for marca in MARCAS_EXH:
                st.markdown(f"**{marca}**")
                c1, c2 = st.columns(2)
                with c1:
                    g = st.text_input("Gestión", key=f"exh_{marca}_g_{i}", placeholder="cant(mes)")
                with c2:
                    n = st.text_input("Negoc", key=f"exh_{marca}_n_{i}", placeholder="cant(mes)")
                row[f"{marca}_gestion"] = g
                row[f"{marca}_negoc"] = n

            st.markdown("**Otro**")
            co1, co2, co3 = st.columns([2, 1, 1])
            with co1:
                otro_marca = st.text_input("Marca", key=f"exh_otro_marca_{i}", placeholder="Nombre marca")
            with co2:
                otro_g = st.text_input("Gestión", key=f"exh_otro_g_{i}", placeholder="cant(mes)")
            with co3:
                otro_n = st.text_input("Negoc", key=f"exh_otro_n_{i}", placeholder="cant(mes)")
            row["otro_marca"] = otro_marca
            row["otro_gestion"] = otro_g
            row["otro_negoc"] = otro_n
            exhibicion_rows.append(row)


    # ══════════════════════════════════════════════════════════════════
    # IV. PARTICIPACIÓN EN LINEAL (SOS) — Mobile-first
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">IV. PARTICIPACIÓN EN LINEAL (SOS)</div>', unsafe_allow_html=True)

    CATEGORIAS_SOS = [
        ("FOOT CARE",      "MEXSANA TALCO",    "TALCOS",                   False, False),
        ("FOOT CARE",      "MEXSANA SPRAY",    "SPRAYS",                   False, False),
        ("DERMATOLOGICOS", "ACID MANTLE",      "DERMATOLOGICOS",           False, False),
        ("VITAMINAS",      "REDOXON",          "VITAMINAS EFERVESC",       False, False),
        ("VITAMINAS",      "REDOXITOS",        "VITAMINAS NIÑOS GOMAS",    False, False),
        ("GASTRO",         "ALKA REGULAR",     "GASTRO PESADEZ Y LLENURA", False, False),
        ("GASTRO",         "ALKA EXTREME",     "GASTRO POSTFIESTA",        False, False),
        ("ANTIMICOTICOS",  "GYNOCANESTEN",     "ANTIMICOTICOS VAGINALES",  False, False),
        ("ANTIMICOTICOS",  "CANESTEN",         "ANTIMICOTICOS TOPICOS",    True,  True),   # UNIV CMS bloqueadas
        ("ANALGESICOS",    "APRONAX",          "ANALGESICOS DOLOR FUERTE", False, False),
        ("ANALGESICOS",    "ASP ULTRA + EFER", "ANALGESICOS DOLOR GENERAL",False, False),
        ("PREVENCION",     "ASA 100",          "PREVENCION CORAZON",       False, False),
        ("ANTIGRIPALES",   "TABCIN",           "ANTIGRIPALES",             False, False),   # UNIV CMS bloqueadas
    ]
    # Tupla: (cat, marca, universo, bloq_univ_cms, bloq_univ_cms_2s)

    sos_data = []
    cat_actual = None
    for (cat, marca, universo, blq_u1, blq_u2) in CATEGORIAS_SOS:
        # Separador de categoría
        if cat != cat_actual:
            st.markdown(f"""
            <div style='background:#2e75b6;color:white;padding:5px 10px;
            border-radius:5px;font-weight:700;font-size:0.85rem;margin-top:12px;'>
            {cat}
            </div>""", unsafe_allow_html=True)
            cat_actual = cat

        with st.expander(f"🔹 {marca} — {universo}", expanded=False):
            obj = st.number_input(
                "% SOS Objetivo",
                0.0, 100.0, step=0.5,
                key=f"sos_obj_{marca}"
            )

            st.markdown("**1er Semestre**")
            s1c1, s1c2 = st.columns(2)
            with s1c1:
                if blq_u1:
                    st.markdown("<div style='background:#222;height:38px;border-radius:4px;margin-top:4px;'></div>", unsafe_allow_html=True)
                    u1 = None
                else:
                    u1 = st.text_input("UNIV CMS", key=f"sos_u1_{marca}")
            with s1c2:
                c1 = st.text_input("CMS", key=f"sos_c1_{marca}")

            st.markdown("**2do Semestre**")
            s2c1, s2c2 = st.columns(2)
            with s2c1:
                if blq_u2:
                    st.markdown("<div style='background:#222;height:38px;border-radius:4px;margin-top:4px;'></div>", unsafe_allow_html=True)
                    u2 = None
                else:
                    u2 = st.text_input("UNIV CMS", key=f"sos_u2_{marca}")
            with s2c2:
                c2 = st.text_input("CMS", key=f"sos_c2_{marca}")

            sos_data.append({
                "categoria": cat, "marca": marca, "universo": universo,
                "pct_sos_objetivo": obj,
                "univ_cms_1s": u1, "cms_1s": c1,
                "univ_cms_2s": u2, "cms_2s": c2,
            })

    # ══════════════════════════════════════════════════════════════════
    # V. OPORTUNIDADES DE EXHIBICIÓN
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">V. OPORTUNIDADES DE EXHIBICIÓN</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # V. OPORTUNIDADES DE EXHIBICIÓN
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">V. OPORTUNIDADES DE EXHIBICIÓN</div>', unsafe_allow_html=True)

    # ── 1. Exhibición Puestos de Pago ─────────────────────────────────
    st.markdown("""
    <div style='background:#2196a8;color:white;text-align:center;padding:6px;
    border-radius:5px;font-weight:700;font-size:0.88rem;margin-bottom:8px;'>
    Exhibición Puestos de Pago
    </div>""", unsafe_allow_html=True)
    st.caption("* El pdv tiene este tipo de exhibición SI/NO; cuantas XX.")

    col_alim, col_noalim = st.columns(2)
    with col_alim:
        num_puestos_alim = st.number_input("# Puestos de pago Alim", min_value=0, step=1, key="pp_alim")
    with col_noalim:
        num_puestos_noalim = st.number_input("# Puestos de pago NO Alim", min_value=0, step=1, key="pp_noalim")

    ITEMS_PUESTOS_PAGO = {
        "Aereo":   ["Mueble Aereo"],
        "Banda":   ["Counter", "Vidrio"],
        "Modulo":  ["Tiburon", "Modulo", "Balconera", "Bandeja",
                    "Espacio para Ristra", "Espacio para Ganchera"],
    }

    exh_puestos_pago = []
    for ubicacion, tipos in ITEMS_PUESTOS_PAGO.items():
        st.markdown(f"**{ubicacion}**")
        for tipo in tipos:
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.markdown(f"<div style='padding-top:8px;'>{tipo}</div>", unsafe_allow_html=True)
            with c2:
                tiene = st.radio("¿Tiene?", ["Sí", "No"],
                                key=f"pp_tiene_{ubicacion}_{tipo}", horizontal=True,
                                label_visibility="collapsed")
            with c3:
                cant = st.number_input("Cant.", min_value=0, step=1,
                                    key=f"pp_cant_{ubicacion}_{tipo}",
                                    label_visibility="collapsed")
            exh_puestos_pago.append({
                "ubicacion": ubicacion, "tipo": tipo,
                "tiene": tiene, "cantidad": cant
            })

    # ── 2. Exhibición diferente a Puestos de Pago ─────────────────────
    st.markdown("""
    <div style='background:#2196a8;color:white;text-align:center;padding:6px;
    border-radius:5px;font-weight:700;font-size:0.88rem;margin:12px 0 8px 0;'>
    Exhibición diferente a Puestos de Pago
    </div>""", unsafe_allow_html=True)
    st.caption("* Otros: Mueble pantalla, metro cuadrado, etc.")

    ITEMS_DIFERENTE_PP = {
        "Cosmeticos": [
            ("Punta de gondola", False),
            ("Chimenea",         False),
            ("Tope de tope",     False),
            ("Rejilla o lateral",False),
            ("Otros",            True),   # True = muestra campo "Cual"
        ],
        "Categoria Adyacente": [
            ("Punta de gondola", True),
            ("Chimenea",         True),
            ("Tope de tope",     True),
            ("Rejilla o lateral",True),
            ("Otros",            True),
        ],
    }

    exh_diferente_pp = []
    for ubicacion, tipos in ITEMS_DIFERENTE_PP.items():
        st.markdown(f"**{ubicacion}**")
        for tipo, muestra_obs in tipos:
            cols = st.columns([3, 1, 1, 2]) if muestra_obs else st.columns([3, 1, 1, 0.1])
            cols[0].markdown(f"<div style='padding-top:8px;'>{tipo}</div>", unsafe_allow_html=True)
            with cols[1]:
                tiene = st.radio("¿Tiene?", ["Sí", "No"],
                                key=f"dpp_tiene_{ubicacion}_{tipo}", horizontal=True,
                                label_visibility="collapsed")
            with cols[2]:
                cant = st.number_input("Cant.", min_value=0, step=1,
                                    key=f"dpp_cant_{ubicacion}_{tipo}",
                                    label_visibility="collapsed")
            obs = ""
            if muestra_obs:
                with cols[3]:
                    label = "¿Cuál?" if tipo == "Otros" else "Categoría"
                    obs = st.text_input(label, key=f"dpp_obs_{ubicacion}_{tipo}",
                                        label_visibility="collapsed",
                                        placeholder=label)
            exh_diferente_pp.append({
                "ubicacion": ubicacion, "tipo": tipo,
                "tiene": tiene, "cantidad": cant, "observaciones": obs
            })

    # ── 3. Exhibición Muebles de Piso ─────────────────────────────────
    st.markdown("""
    <div style='background:#2196a8;color:white;text-align:center;padding:6px;
    border-radius:5px;font-weight:700;font-size:0.88rem;margin:12px 0 8px 0;'>
    Exhibición Muebles de Piso
    </div>""", unsafe_allow_html=True)
    st.caption("* El pdv cuenta con espacio SI/NO, Cuantos XX.")

    ITEMS_MUEBLES_PISO = [
        ("Mueble proveedor", True),   # True = muestra campo categoría
        ("Mueble cliente",   True),
        ("Tropezon",         True),
        ("Otros",            False),  # muestra "Cual"
    ]

    exh_muebles_piso = []
    for tipo, es_categoria in ITEMS_MUEBLES_PISO:
        cols = st.columns([3, 1, 1, 2])
        cols[0].markdown(f"<div style='padding-top:8px;'>{tipo}</div>", unsafe_allow_html=True)
        with cols[1]:
            tiene = st.radio("¿Tiene?", ["Sí", "No"],
                            key=f"mp_tiene_{tipo}", horizontal=True,
                            label_visibility="collapsed")
        with cols[2]:
            cant = st.number_input("Cant.", min_value=0, step=1,
                                key=f"mp_cant_{tipo}",
                                label_visibility="collapsed")
        with cols[3]:
            label = "Categoría" if es_categoria else "¿Cuál?"
            obs = st.text_input(label, key=f"mp_obs_{tipo}",
                                label_visibility="collapsed",
                                placeholder=label)
        exh_muebles_piso.append({
            "tipo": tipo, "tiene": tiene,
            "cantidad": cant, "observaciones": obs
        })

    # Estructura final para el payload
    oportunidades_exhibicion = {
        "num_puestos_pago_alim":           int(num_puestos_alim),
        "num_puestos_pago_no_alim":        int(num_puestos_noalim),
        "exhibicion_puestos_pago":         exh_puestos_pago,
        "exhibicion_diferente_puestos_pago": exh_diferente_pp,
        "exhibicion_muebles_piso":         exh_muebles_piso,
    }

    # ══════════════════════════════════════════════════════════════════
    # VI. COMPETIDORES CERCANOS
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">VI. COMPETIDORES CERCANOS</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">¿Cuántos PDV de estos formatos hay en un radio de 10 cuadras a la redonda?</div>', unsafe_allow_html=True)

    COMPETIDORES = [
        ("Farmatodo", "Cruz Verde", "Colsubsidio"),
        ("Cafam", "Olímpica", "La 14"),
        ("Comfandi", "Locatel", "Drogas La Rebaja"),
        ("D1", "Ara", "Justo y Bueno"),
    ]
    competidores_data = {}
    for grupo in COMPETIDORES:
        cols_comp = st.columns(3)
        for col, cadena in zip(cols_comp, grupo):
            val = col.number_input(cadena, 0, step=1, key=f"comp_{cadena}")
            competidores_data[cadena] = val

    # ══════════════════════════════════════════════════════════════════
    # VII. COMENTARIOS RELEVANTES
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">VII. COMENTARIOS RELEVANTES</div>', unsafe_allow_html=True)
    comentarios = st.text_area("Comentarios relevantes del PDV", height=120)

    st.divider()

    # ══════════════════════════════════════════════════════════════════
    # BOTÓN ENVIAR
    # ══════════════════════════════════════════════════════════════════
    if st.button("✅ Enviar Solicitud", type="primary", use_container_width=True):

        payload = {
            "nombre_cadena":               nombre_cadena,
            "punto_de_venta":              punto_de_venta,
            "dependenci_pdv":              dependenci_pdv,
            "telefono":                    telefono,
            "direccion":                   direccion,
            "nombre_gerente_pdv":          nombre_gerente,
            "nombre_cargo_contacto":       nombre_contacto,
            "ranking_pdv_total_nacional":  ranking_nac,
            "ranking_pdv_cadena_nacional": ranking_cad_nac,
            "ranking_pdv_cadena_regional": ranking_cad_reg,
            "ranking_pdv_zona_asignada":   ranking_zona,
            "tiene_domicilio":             tiene_domicilio,
            "centralizado":                centralizado,
            "pdv":                         pdv_check,
            "ventas_por_mes":              int(ventas_mes),
            "venta_prom_mes_otc":          int(venta_otc),
            "venta_prom_mes_foot_care":    int(venta_foot),
            "top_marcas_mas_vendidas":     marcas,
            "top_skus_mas_vendidos":       skus,
            "entrega_de_mercancia":        entrega_merc,
            "dias_de_pedido":              ", ".join(dias_pedido),
            "dias_de_visitas":             ", ".join(dias_visita),
            "tiene_operador_logistico":    operador_log,
            "frecuencia_de_pedido":        frecuencia_ped,
            "horario_recibo_obsequios":    horario_obs,
            "intensidad_horaria_semana":   int(intensidad_h),
            "sell_out": {
                "mensual":    sell_out_data,
                "por_marca":  sell_out_marcas,
            },
            "exhibicion":                  exhibicion_rows,
            "participacion_lineal_sos":    sos_data,
            "oportunidad_exhibicion":      oportunidades_exhibicion,
            "competidores_cercanos":       competidores_data,
            "comentarios_relevnates":      comentarios,
        }

        with st.spinner("Guardando en Supabase..."):
            ok, result = insertar_hoja_vida(payload)

        if ok:
            st.success(f"✅ Registro guardado exitosamente. ID: **{result}**")
            st.balloons()
        else:
            st.error(f"❌ Error al guardar: {result}")


if __name__ == "__main__":
    main()

