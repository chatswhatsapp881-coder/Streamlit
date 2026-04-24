"""
=============================================================================
SOLICITUDES DE OUTSOURCING - ARL BOLÍVAR
App Streamlit — Sin st.form, dinámico + Excel + PDF cédula por correo
=============================================================================
"""


import streamlit as st
from collections import defaultdict
from supabase import create_client
import datetime


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
    page_title="Hoja de vida POS Cadenas farma",
    page_icon="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAHO0lEQVR4Aa1WA3gkzRY9k6xt28qo4/yOR+FM9Nu2bds214zNxWwwEydr296deufV2v1w+rtfVavuuefeut1QC+UbtI11YnRcFeJor9jd+Mnhwox4msONHzi+GO+G1bwYozAV3vh/ITwLnenwroRaZNprsD+1FSK5mdZEa5TGOeS1FN5LcGOPvRYL4ly45eoCdMD/gthqWBy1KE/h4qkrNIJRr0qowSySecpeicSEpQiNruwUHdky1GF2dXvGVD10Wqyr05rEps6C7wgSKbK6EI7/FGFOdGe0nznqcTR1GeRCiVVIs1agPyReagddzC+0adDHTIXO9oa8BuHVsWDGEJ3zRoe/01QQW9vtWFI9DlGNd5V16AQ1CF2E3gkuzElbCeGow1YSeSQqHd3OLghLHyjWTfCLeZPjU7RVtBCcgtDgAdF3YPEvDwQvtTSntLYTiW78E1yKrrgUzC70ZDHNo3NGDXesCwouhCERveBr2wA/WzYMlnkwkswUSxDOA4n8La4dVfpBWYy71zG7C9P/XVO4IOzwZuTfnHDuYo4n4SKQCvhZ10OxPc803AyjrYVzOy6GT8WVfUrSnRZXnyNJLnyIl+CFc8Eb9qRGHLXXY0NcJXS4FAZaOlHyj6GYv6Pz76HEPInewZeW92cR0bMkq9nq6rGDSpjPDr4cvVhkbm4lwZt3Qx000JtvZAqSoBZ/iTeHlP660+HWlNgL0AUnEV+HJ1OXQ8TXIp1He6jB+MjxMFqWw9fahEkhw6AGM0VvZIkS/8XJW9i87gWIq8mEUS9KbsGRuBrYoBaK5WMS+IwK/MRUvAy1mOu5vWuR+5C1ptuswKnoiMgaGB0NOMwCbAyvRmeogT5qEnO/gyScLL4quQsMQcOhBrM8QzFfrJ1Q8cLye9yYKOVnCxXcft9CLQzRd0NveQcTQsfBh6nwZ0EaLDdALeZ70rsWVe40Ofs4wEazgL1csOvdiCnxE6AzmaG3xkA2FqXt6ZzbxsNgmghC7nm9WXcGIV+qYcQUqxbaaAt8zDaex2K4rgcGRPUl2Wi55pTIIABeyBEvIO/YweAloZ/D4UILPyjihvXwxRTbd/CPWcqc/somw9HyIEAMCexImRfRKtE/vDOdh7EP8H7UaOlU4dwn0giDdSb8YhcyLXw/5k/oIkdQmQTOV0KJ/Z3rVWNyxOMkEIMiIYaVffMPbDW9VnPvi9SNGMWm8rPMq5HyKhY3nbwCgvO7ZMdTzLNI4mEQVOoJOs7ns6Vc/O4Tz2XwuWJef4818jYGhfaGwZbMZ1r47lMMqgK66LeQ6zGCBNrmLs9DwGJTdVIDxPU7MFJ+YBRLHvSMnIvxhW+kjEYyN1oLSCiHYz18fHpKKQ18VrHOAXGKgGKbC535YehItL+2syTArcq1ZvD9Veg0YSDyhYJCIZB/qAHjKl7MSmmiAmys0NKhv83FXM/kwktgND8EgzlZRmpglAYqoZjzoZhuA0Fn75PcizgBzmdT7kqZCkmEKWCLhpHpGH51B6qyANrwZ5AhbKACyBOL0K8444eEeu/D9kbcgF7mwdBF+Mti4VYDhEY2GW1QP5zEuKv7wCd0FBfqx2f8oEQa5RzQcBwpC1JrCoBPVKBUQEcFeR2ETMlI7ThkHH7eq1gI1sKXQLa4+ypn0M4kt/ptiElXd6EqZVQjFzLvtn8wZkx7qEWW+AdlQiBT3Ap8LK4YW/b2Onudd7VlLjqp7IJ9KOda2QH9LLdLmaHyP3CGZyAjX0P592KumAB8LrpocvbOvK7SZ1+yC2aoAf8HqMA6Op5O+472vGoCOZ40LBQC2Z50vCTaQGKWeKFfycwd8S7vqfZatMPl4BfbmwpspOMvOL4IfczjANrgcpgtujLlxSgVx5DnuQen8Ifow7w49Ytv3ZrSgFsuXwOT2slPsZ/1AXCncLxZlQKZ4imUy+IrxVTRBWchXSQib/+OwEWmyltqMQmXgNxSBsuj3HYvwc/8gmy7gNdlCi8AhZ7NmiJxELkiHOfBLrzJ8Gfv3J2HfBcnL3jAjdGXLkLrFkb/gSTha14lt97FME/o6LQVFTL6j6SvC2Kq6I4MT7omf/eBseUvpadUYuzFf0qtG1iIWfC1ZHMsZ48femHZPcHIF3Vg4WlyxZ+s/MvstHTRF3kiU1N6THQvWuicXPFIctS5f0n6qL7M+0r5oaEKsiewN+BMzBI9uM4jtJ0y77lihgxQFfggpfpMUyCEV/6+/V2LnH+1L6kM71166seTX8ToHyhFL4DktJHfYvxVVhCYI/oj3ZPGaCtks8kXR7jW2/jmApGrqNoETY5Y5FVCIoWHBYu0Hrn7vvXK3HcPprXGY+6uIBZXCGZtT8XMzS/y2VmMeJV0XCTzXUQz438CmdPJfYwoj7ZPUyqE7OOFZ1iRkMZ7dOrZjVxPFsnfQSXb4f+GT0R7RjNKLpwtfmEjKeC4HKxujvm89xPnN5PsSLyk3vG/AJw8UVr0m/g8AAAAAElFTkSuQmCC",
    layout="wide"
)

LOGOS_CADENAS = [
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/9cm/91g/drj/idf3hb0pKj_1775769551319.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/g6l/m9o/nrr/idmJvu77_g_1774995536838.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/k6u/uf0/9cv/Imagen9.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/9bm/xxv/qft/Imagen10.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/wcm/ble/x4w/Imagen11.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/imp/95m/w4p/Imagen12.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/o30/qfp/5cj/Imagen13.png",
    "https://bab543b92f.imgdist.com/pub/bfra/v9e05eqk/v2k/lod/pj1/Imagen14.png",
]


# ─────────────────────────────────────────────────────────────────────────────
# 2. FUNCIONES AUXILIARES
# ─────────────────────────────────────────────────────────────────────────────

# ── Helper formato COP ─────────────────────────────────────────────
def fmt_cop(v) -> str:
    """Formatea valor como pesos colombianos: 1.234.567"""
    return f"{int(v):,}".replace(",", ".")

def _fetch_all(query_fn) -> list[dict]:
    """Pagina automáticamente hasta traer todos los registros de Supabase (supera límite de 1000)."""
    PAGE = 1000
    result = []
    offset = 0
    while True:
        res = query_fn(offset, offset + PAGE - 1)
        batch = res.data or []
        result.extend(batch)
        if len(batch) < PAGE:
            break
        offset += PAGE
    return result


@st.cache_data(ttl=300)
def get_segmentos_nielsen():
    """Retorna lista única de segmento_nielsen de la tabla universo."""
    data = _fetch_all(
        lambda s, e: supabase
            .table("universo")
            .select("segmento_nielsen")
            .not_.is_("segmento_nielsen", "null")
            .range(s, e)
            .execute()
    )
    valores = sorted({
                        r["segmento_nielsen"] for r in data
                        if r["segmento_nielsen"] == "DROGUERIAS"
                    })
    return ["— Seleccione —"] + valores


@st.cache_data(ttl=300)
def get_formatos_by_segmento(segmento_nielsen: str):
    """Retorna formatos de cadena filtrados por segmento_nielsen."""
    data = _fetch_all(
        lambda s, e: supabase
            .table("universo")
            .select("comerciante_red")
            .eq("segmento_nielsen", segmento_nielsen)
            .not_.is_("comerciante_red", "null")
            .range(s, e)
            .execute()
    )
    valores = sorted({r["comerciante_red"] for r in data if r["comerciante_red"]})
    return ["— Seleccione —"] + valores


@st.cache_data(ttl=300)
def get_pdvs_by_segmento_formato(segmento_nielsen: str, comerciante_red: str):
    """Retorna nombres de PDV filtrados por segmento y formato."""
    data = _fetch_all(
        lambda s, e: supabase
            .table("universo")
            .select("nombre_pdv_en_tdr")
            .eq("segmento_nielsen", segmento_nielsen)
            .eq("comerciante_red", comerciante_red)
            .not_.is_("nombre_pdv_en_tdr", "null")
            .range(s, e)
            .execute()
    )
    valores = sorted({r["nombre_pdv_en_tdr"] for r in data if r["nombre_pdv_en_tdr"]})
    return ["— Seleccione —"] + valores


def get_pdv_info(segmento_nielsen: str, comerciante_red: str, nombre_pdv: str) -> dict | None:
    """Retorna el registro completo del PDV seleccionado en la tabla universo."""
    res = (
        supabase
        .table("universo")
        .select("*")
        .eq("segmento_nielsen", segmento_nielsen)
        .eq("comerciante_red", comerciante_red)
        .eq("nombre_pdv_en_tdr", nombre_pdv)
        .limit(1)
        .execute()
    )
    return res.data[0] if res.data else None


def get_sellout_agregado_by_ean_pdv(ean_pdv) -> dict:
    """
    Llama a la RPC get_sellout_agregado en Supabase.
    RPC hace GROUP BY anio, mes_num, marca, material en Postgres.
    - valor_bay en millones -> x 1_000_000
    - Anos: 2025 (base) y 2026 (actual)
    - Foot Care = MEXSANA*, ACID MANTLE*, BEPANTHEN
    - OTC = resto
    """

    ORDEN_MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                   "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    MESES_NUM   = {m: i+1 for i, m in enumerate(ORDEN_MESES)}

    FOOT_MARCAS = {
        "MEXSANA","MEXSANA MEDICAL",
        "ACID MANTLE","ACID MANTLE BABY","ACID MANTLE PROB5","ACID MANTLE TATTOO",
        "BEPANTHEN",
    }

    ANIO_A = 2025
    ANIO_B = 2026

    # Una sola llamada RPC — GROUP BY en Postgres, sin timeout
    res   = supabase.rpc("get_sellout_agregado", {"p_ean": str(ean_pdv)}).execute()
    filas = res.data or []

    mes_anio:   dict[tuple, float] = defaultdict(float)
    total_anio: dict[int,   float] = defaultdict(float)
    marca_anio: dict[tuple, float] = defaultdict(float)
    sku_anio:   dict[tuple, float] = defaultdict(float)

    for r in filas:
        a    = r.get("anio")
        mn   = r.get("mes_num")
        marc = (r.get("marca")    or "").upper().strip()
        mat  = (r.get("material") or "").strip()
        v    = float(r.get("total_valor") or 0) * 1_000_000

        if a not in (ANIO_A, ANIO_B):
            continue
        if mn:
            mes_anio[(a, mn)]    += v
            total_anio[a]        += v
        if marc:
            marca_anio[(a, marc)] += v
        if mat:
            sku_anio[(a, mat)]    += v

    tiene_datos = bool(total_anio)

    # Meses con datos > 0 por año (para calcular promedios correctos)
    m_A = len({mn for (a, mn) in mes_anio if a == ANIO_A and mes_anio[(a, mn)] > 0}) or 1
    m_B = len({mn for (a, mn) in mes_anio if a == ANIO_B and mes_anio[(a, mn)] > 0}) or 1

    # Sell Out mensual con acumulados
    sell_out_mensual = {}
    acum_A = acum_B = 0
    for mes_nombre in ORDEN_MESES:
        n    = MESES_NUM[mes_nombre]
        vA   = round(mes_anio.get((ANIO_A, n), 0))
        vB   = round(mes_anio.get((ANIO_B, n), 0))
        acum_A += vA
        acum_B += vB
        sell_out_mensual[mes_nombre] = {
            "sell_out_mes_2025":  vA,  "sell_out_mes_2026":  vB,
            "sell_out_acum_2025": acum_A, "sell_out_acum_2026": acum_B,
            # alias para compatibilidad con el formulario
            "sell_out_mes_2020":  vA,  "sell_out_mes_2021":  vB,
            "sell_out_acum_2020": acum_A, "sell_out_acum_2021": acum_B,
        }

    # Sell Out por marca — promedio mensual
    marcas_unicas = {m for (a, m) in marca_anio if m}
    sell_out_marcas = {
        marca: {
            "prom_mes_2025": round(marca_anio.get((ANIO_A, marca), 0) / m_A),
            "prom_mes_2026": round(marca_anio.get((ANIO_B, marca), 0) / m_B),
            "prom_mes_2020": round(marca_anio.get((ANIO_A, marca), 0) / m_A),
            "prom_mes_2021": round(marca_anio.get((ANIO_B, marca), 0) / m_B),
            "peso_pct": 0.0,
        }
        for marca in marcas_unicas
    }

    # Top SKUs (material) — promedio mensual
    skus_unicos = {s for (a, s) in sku_anio if s}
    sell_out_skus = {
        sku: {
            "prom_mes_2025": round(sku_anio.get((ANIO_A, sku), 0) / m_A),
            "prom_mes_2026": round(sku_anio.get((ANIO_B, sku), 0) / m_B),
        }
        for sku in skus_unicos
    }

    # Ventas promedio total y por categoria (clasificado por marca)
    foot_B = sum(v for (a, m), v in marca_anio.items() if a == ANIO_B and m in FOOT_MARCAS)
    otc_B  = sum(v for (a, m), v in marca_anio.items() if a == ANIO_B and m not in FOOT_MARCAS)

    return {
        "sell_out_mensual":  sell_out_mensual,
        "sell_out_marcas":   sell_out_marcas,
        "sell_out_skus":     sell_out_skus,
        "ventas_prom_total": round(total_anio.get(ANIO_B, 0) / m_B),
        "ventas_prom_otc":   round(otc_B / m_B),
        "ventas_prom_foot":  round(foot_B / m_B),
        "tiene_datos":       tiene_datos,
        "anio_a": ANIO_A,
        "anio_b": ANIO_B,
    }



def get_ranking_pdv(ean_pdv) -> dict:
    """
    Llama a la RPC get_ranking_pdv en Supabase.
    Retorna dict con strings tipo "979 de 4080" por cada ranking.
    """
    VACIO = {"ranking_nacional": "", "ranking_cadena_nacional": "",
             "ranking_cadena_regional": "", "tiene_datos": False}
    try:
        res  = supabase.rpc("get_ranking_pdv", {"p_ean": str(ean_pdv)}).execute()
        data = res.data[0] if res.data else None

        if not data:
            return VACIO

        r_nac = data.get("ranking_nacional")
        t_nac = data.get("total_pdvs_nacional")
        r_cad = data.get("ranking_cadena_nacional")
        t_cad = data.get("total_pdvs_cadena")
        r_reg = data.get("ranking_cadena_regional")
        t_reg = data.get("total_pdvs_cadena_region")

        return {
            "ranking_nacional":        f"{r_nac} de {t_nac}" if r_nac is not None else "",
            "ranking_cadena_nacional": f"{r_cad} de {t_cad}" if r_cad is not None else "",
            "ranking_cadena_regional": f"{r_reg} de {t_reg}" if r_reg is not None else "",
            "tiene_datos": True,
        }

    except Exception as e:
        # Mostrar error real en pantalla para debug
        import streamlit as st
        st.error(f"❌ Error en get_ranking_pdv: {e}")
        return VACIO


def get_hoja_vida_existente(nombre_pdv: str) -> dict | None:
    """
    Busca si ya existe un registro de hoja de vida para este PDV
    en hoja_vida_cadenas_farmacias. Retorna el más reciente o None.
    """
    res = (
        supabase
        .table("hoja_vida_cadenas_farmacias")
        .select("*")
        .eq("punto_de_venta", nombre_pdv)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return res.data[0] if res.data else None


def upsert_hoja_vida(data: dict):
    """
    Upsert atómico usando on_conflict sobre punto_de_venta.
    Incluye control de concurrencia optimista con updated_at.
    Retorna (True, id, accion) o (False, msg, None).
    """
    try:
        pdv = data.get("punto_de_venta", "")

        # Leer id y updated_at actuales ANTES de guardar
        check = (
            supabase
            .table("hoja_vida_cadenas_farmacias")
            .select("id, updated_at")
            .eq("punto_de_venta", pdv)
            .limit(1)
            .execute()
        )

        if check.data:
            record_id     = check.data[0]["id"]
            updated_at_bd = check.data[0].get("updated_at")
            updated_at_ss = st.session_state.get("_hv_updated_at")

            # Control optimista: detectar si otro usuario guardó mientras tanto
            if updated_at_bd and updated_at_ss and updated_at_bd != updated_at_ss:
                return False, (
                    "⚠️ Este PDV fue modificado por otro usuario mientras lo editabas. "
                    "Recarga la página para ver la versión más reciente antes de guardar."
                ), None
            accion = "actualizado"
        else:
            record_id = None
            accion    = "insertado"

        # Upsert atómico — elimina la race condition del SELECT + INSERT/UPDATE separados
        data["updated_at"] = datetime.datetime.utcnow().isoformat()
        response = (
            supabase
            .table("hoja_vida_cadenas_farmacias")
            .upsert(data, on_conflict="punto_de_venta")
            .execute()
        )
        result_id = response.data[0]["id"] if response.data else record_id

        # Actualizar updated_at en session para futuros guardados en la misma sesión
        if response.data and response.data[0].get("updated_at"):
            st.session_state["_hv_updated_at"] = response.data[0]["updated_at"]

        return True, result_id, accion

    except Exception as e:
        return False, str(e), None


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
    .hv-existente-box {
        background: #fff3cd; border-left: 4px solid #e6a817;
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
    st.markdown("## Hoja de vida PDV Canal Cadenas de Farmacias")
    st.markdown("**Bayer** — Complete el formulario y presione **Enviar Solicitud**.")
    st.divider()


    # ══════════════════════════════════════════════════════════════════
    # 0. BÚSQUEDA EN UNIVERSO — Pre-llenado automático
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">🔍 BUSCAR PDV EN UNIVERSO (pre-llenado automático)</div>', unsafe_allow_html=True)

    # Inicializar session_state
    if "pdv_universo" not in st.session_state:
        st.session_state["pdv_universo"] = None
    if "hoja_vida_existente" not in st.session_state:
        st.session_state["hoja_vida_existente"] = None
    if "sellout_agregado" not in st.session_state:
        st.session_state["sellout_agregado"] = None

    # ── Definir _hv/_u/_so tempranamente para que estén disponibles en todo el scope ──
    _hv = st.session_state.get("hoja_vida_existente") or {}
    _u  = st.session_state.get("pdv_universo") or {}
    _so = st.session_state.get("sellout_agregado") or {}

    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        segmentos = get_segmentos_nielsen()
        seg_sel = st.selectbox("1. Segmento Nielsen", segmentos, key="univ_segmento")

    with col_f2:
        if seg_sel and seg_sel != "— Seleccione —":
            formatos = get_formatos_by_segmento(seg_sel)
        else:
            formatos = ["— Seleccione —"]
        fmt_sel = st.selectbox("2. Comercio", formatos, key="univ_formato",
                               disabled=(seg_sel == "— Seleccione —"))

    with col_f3:
        if fmt_sel and fmt_sel != "— Seleccione —":
            pdvs = get_pdvs_by_segmento_formato(seg_sel, fmt_sel)
        else:
            pdvs = ["— Seleccione —"]
        pdv_sel = st.selectbox("3. Nombre PDV (TDR)", pdvs, key="univ_pdv",
                               disabled=(fmt_sel == "— Seleccione —"))

    # ── Detectar cambio de PDV para recargar datos ────────────────────────
    _pdv_anterior = st.session_state.get("_pdv_cargado", "")
    if pdv_sel and pdv_sel != "— Seleccione —":
        pdv_info = get_pdv_info(seg_sel, fmt_sel, pdv_sel)
        st.session_state["pdv_universo"] = pdv_info

        if pdv_info and pdv_sel != _pdv_anterior:
            # PDV nuevo o cambiado — LIMPIAR keys del PDV anterior para forzar re-inicialización
            _keys_limpiar = [
                "ventas_mes_total", "ventas_mes_otc", "ventas_mes_foot",
                "rk_pdv_nac", "rk_pdv_cad_nac", "rk_pdv_cad_reg",
            ]
            for _i in range(1, 6):
                _keys_limpiar += [f"marca_{_i}", f"vta_marca_{_i}", f"sku_{_i}", f"vta_sku_{_i}"]
            _MESES_LIMPIAR = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                              "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
            for _mes in _MESES_LIMPIAR:
                _keys_limpiar += [
                    f"so_p20_{_mes}", f"so_p21_{_mes}",
                    f"so_a20_{_mes}", f"so_a21_{_mes}",
                ]
            for _key in _keys_limpiar:
                st.session_state.pop(_key, None)

            # Cargar datos y hacer rerun para que widgets lean valores
            nombre_pdv_buscar = pdv_info.get("nombre_pdv_en_tdr", pdv_sel)
            hv_existente = get_hoja_vida_existente(nombre_pdv_buscar)
            st.session_state["hoja_vida_existente"] = hv_existente
            st.session_state["_hv_updated_at"] = hv_existente.get("updated_at") if hv_existente else None
            _hv_tmp = hv_existente or {}

            ean_pdv = pdv_info.get("ean_pdv", "")
            if ean_pdv:
                ean_str = str(ean_pdv).strip()
                with st.spinner("Cargando datos de Sell Out..."):
                    so_agg = get_sellout_agregado_by_ean_pdv(ean_str)
                st.session_state["sellout_agregado"] = so_agg

                # ── Rankings PDV ──────────────────────────────────────────────
                with st.spinner("Calculando rankings..."):
                    rk_data = get_ranking_pdv(ean_str)
                st.session_state["rk_pdv_nac"]     = rk_data["ranking_nacional"]
                st.session_state["rk_pdv_cad_nac"] = rk_data["ranking_cadena_nacional"]
                st.session_state["rk_pdv_cad_reg"] = rk_data["ranking_cadena_regional"]

                if so_agg["tiene_datos"]:
                    # SELL OUT siempre tiene prioridad sobre hoja_vida (se actualiza cada 3-4 meses)
                    st.session_state["ventas_mes_total"] = so_agg["ventas_prom_total"] or int(_hv_tmp.get("ventas_por_mes") or 0)
                    st.session_state["ventas_mes_otc"]   = so_agg["ventas_prom_otc"]   or int(_hv_tmp.get("venta_prom_mes_otc") or 0)
                    st.session_state["ventas_mes_foot"]  = so_agg["ventas_prom_foot"]  or int(_hv_tmp.get("venta_prom_mes_foot_care") or 0)

                    # Top marcas: so primero, hv como fallback
                    _sm = sorted(
                        so_agg["sell_out_marcas"].items(),
                        key=lambda x: x[1].get("prom_mes_2026") or x[1].get("prom_mes_2025", 0),
                        reverse=True
                    )[:5]
                    if _sm:
                        for idx, (m, v) in enumerate(_sm, 1):
                            st.session_state[f"marca_{idx}"]     = m
                            st.session_state[f"vta_marca_{idx}"] = int(v.get("prom_mes_2026") or v.get("prom_mes_2025", 0))
                    elif _hv_tmp.get("top_marcas_mas_vendidas"):
                        for idx, _mp in enumerate(_hv_tmp["top_marcas_mas_vendidas"][:5], 1):
                            st.session_state[f"marca_{idx}"]     = _mp.get("marca", "") if isinstance(_mp, dict) else ""
                            st.session_state[f"vta_marca_{idx}"] = int(_mp.get("vtas_prom_mes", 0) if isinstance(_mp, dict) else 0)

                    # Top SKUs: so primero, hv como fallback
                    _ss = sorted(
                        so_agg["sell_out_skus"].items(),
                        key=lambda x: x[1].get("prom_mes_2026") or x[1].get("prom_mes_2025", 0),
                        reverse=True
                    )[:5]
                    if _ss:
                        for idx, (s, v) in enumerate(_ss, 1):
                            st.session_state[f"sku_{idx}"]     = s
                            st.session_state[f"vta_sku_{idx}"] = int(v.get("prom_mes_2026") or v.get("prom_mes_2025", 0))
                    elif _hv_tmp.get("top_skus_mas_vendidos"):
                        for idx, _sp in enumerate(_hv_tmp["top_skus_mas_vendidos"][:5], 1):
                            st.session_state[f"sku_{idx}"]     = _sp.get("sku", "") if isinstance(_sp, dict) else ""
                            st.session_state[f"vta_sku_{idx}"] = int(_sp.get("vtas_prom_mes", 0) if isinstance(_sp, dict) else 0)

                    # Sell Out mensual: so SIEMPRE reemplaza hv (datos frescos cada 3-4 meses)
                    for mes_n, vals in so_agg["sell_out_mensual"].items():
                        st.session_state[f"so_p20_{mes_n}"] = vals["sell_out_mes_2025"]
                        st.session_state[f"so_p21_{mes_n}"] = vals["sell_out_mes_2026"]
                        st.session_state[f"so_a20_{mes_n}"] = vals["sell_out_acum_2025"]
                        st.session_state[f"so_a21_{mes_n}"] = vals["sell_out_acum_2026"]
                else:
                    st.session_state["sellout_agregado"] = None
            else:
                st.session_state["sellout_agregado"] = None

            # Marcar PDV como cargado y forzar rerun para que widgets lean session_state
            st.session_state["_pdv_cargado"] = pdv_sel
            st.rerun()

        # PDV ya cargado — solo mostrar mensajes informativos
        if pdv_info:
            hv_existente = st.session_state.get("hoja_vida_existente")
            so_agg       = st.session_state.get("sellout_agregado") or {}
            ean_pdv      = pdv_info.get("ean_pdv", "")
            if so_agg and so_agg.get("tiene_datos"):
                st.success(f"📊 Sell Out cargado — ventas prom. mes: ${so_agg.get('ventas_prom_total', 0):,}")
            elif ean_pdv:
                st.caption(f"Sin datos de Sell Out para EAN `{ean_pdv}`.")
            else:
                st.caption("Este PDV no tiene EAN registrado — Sell Out no disponible.")

            if hv_existente:
                st.warning(
                    f"⚠️ Este PDV ya tiene una hoja de vida registrada "
                    f"(ID: **{hv_existente.get('id')}**). "
                    f"Los campos se pre-llenarán con esa información guardada."
                )
            else:
                st.success(
                    f"✅ PDV encontrado: **{pdv_info.get('nombre_compuesto_universo', pdv_sel)}** "
                    f"— Sin registro previo, se usarán datos del universo."
                )
    else:
        st.session_state["pdv_universo"] = None
        st.session_state["hoja_vida_existente"] = None
        st.session_state["sellout_agregado"] = None

    st.divider()

    # ── Prioridad de pre-llenado:
    #    1. Hoja de vida existente (datos ya guardados para ese PDV)
    #    2. Datos de sellout calculados (ventas reales de BD)
    #    3. Datos del universo (datos maestros)
    #    4. Vacío
    _hv = st.session_state.get("hoja_vida_existente") or {}
    _u  = st.session_state.get("pdv_universo") or {}
    _so = st.session_state.get("sellout_agregado") or {}

    def _v(campo_hv: str, campo_u: str = None) -> str:
        """Retorna el valor con prioridad hoja_vida > universo > vacío."""
        val = _hv.get(campo_hv) or _u.get(campo_u or campo_hv)
        return str(val) if val is not None else ""

    # ══════════════════════════════════════════════════════════════════
    # I. INFORMACIÓN GENERAL
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">I. INFORMACIÓN GENERAL DE SOLICITUD</div>', unsafe_allow_html=True)


    col1, col2 = st.columns(2)
    with col1:
        fecha_info = st.date_input("Fecha información (D/M/A)")

        # Selectbox cadena: prioridad hoja_vida > universo
        _cadenas_opts = [
            "Cruz Verde", "Farmatodo", "Colsubsidio", "Cafam", "Olímpica",
            "Locatel", "Comfandi", "Otra"]
        _cadena_val = _hv.get("nombre_cadena") or _u.get("comerciante_red", "")
        _cadena_idx = 0
        if _cadena_val:
            for _i, _opt in enumerate(_cadenas_opts):
                if _opt.lower() == _cadena_val.lower():
                    _cadena_idx = _i
                    break
        nombre_cadena   = st.selectbox("Nombre cadena", fmt_sel)

        punto_de_venta  = st.text_input("Punto de venta",
                            value=_v("punto_de_venta", "nombre_pdv_en_tdr"))
        dependenci_pdv  = st.text_input("Dependencia / Código SICOL PDV",
                            value=_v("dependenci_pdv", "ean_pdv"))
        telefono        = st.text_input("Teléfono",
                            value=_v("telefono", "telefono_celular"))
        direccion       = st.text_input("Dirección",
                            value=_v("direccion", "direccion"))
        nombre_gerente  = st.text_input("Nombre Gerente / Administrador PDV",
                            value=_v("nombre_gerente_pdv"))
        nombre_contacto = st.text_input("Nombre y cargo contacto clave",
                            value=_v("nombre_cargo_contacto"))

    with col2:
        # Rankings: session_state (calculado de sellout) > hoja_vida guardada > vacío
        _rk_nac_val     = st.session_state.get("rk_pdv_nac")     or _v("ranking_pdv_total_nacional")
        _rk_cad_nac_val = st.session_state.get("rk_pdv_cad_nac") or _v("ranking_pdv_cadena_nacional")
        _rk_cad_reg_val = st.session_state.get("rk_pdv_cad_reg") or _v("ranking_pdv_cadena_regional")

        ranking_nac     = st.text_input("Ranking PDV total nacional",
                            value=_rk_nac_val,
                            help="Posición del PDV vs todos los PDVs del país por venta promedio mensual")
        ranking_cad_nac = st.text_input("Ranking PDV cadena nacional",
                            value=_rk_cad_nac_val,
                            help="Posición dentro de su cadena a nivel nacional")
        ranking_cad_reg = st.text_input("Ranking PDV cadena regional",
                            value=_rk_cad_reg_val,
                            help="Posición dentro de su cadena + zona Nielsen")
        ranking_zona    = st.text_input("Ranking PDV zona asignada",
                            value=_v("ranking_pdv_zona_asignada"))
        codigo_ruta     = st.text_input("Código de ruta",
                            value=_v("codigo_ruta", "codigo_ruta"))
        tiene_domicilio = st.radio("¿Tiene domicilio?", ["Sí", "No"], horizontal=True)
        horas_24        = st.radio("¿24 horas?", ["Sí", "No"], horizontal=True)


    st.markdown("**Domicilio**")
    col3, col4 = st.columns(2)
    with col3:
        centralizado   = st.checkbox("Centralizado",
                            value=bool(_hv.get("centralizado", False)))
        pdv_check      = st.checkbox("PDV",
                            value=bool(_hv.get("pdv", False)))
        porc_domicilio = st.number_input("% venta domicilio", 0, 100, step=1,
                            value=int(_hv.get("porc_venta_domicilio", 0) or 0))
    with col4:
        _tel_opts = ["Exclusivo", "Central", "Propio"]
        _tel_val  = _hv.get("telefonista", "Exclusivo")
        _tel_idx  = _tel_opts.index(_tel_val) if _tel_val in _tel_opts else 0
        telefonista  = st.selectbox("Telefonista", _tel_opts, index=_tel_idx)
        nodo_central = st.radio("¿Es nodo o central abastecimiento domicilios?",
                            ["Sí", "No"], horizontal=True)


    st.markdown("**Estructura PDV**")
    col5, col6 = st.columns(2)
    with col5:
        autoservicio = st.checkbox("Droguería tipo autoservicio",
                            value=bool(_hv.get("drogueria_tipo_autoservicio", False)))
        ocounter     = st.checkbox("O-Counter",
                            value=bool(_hv.get("ocounter", False)))
        num_dep      = st.number_input("# Dependientes", 0, step=1,
                            value=int(_hv.get("num_dependientes", 0) or 0))
        num_turnos   = st.number_input("# Turnos", 0, step=1,
                            value=int(_hv.get("num_turnos", 0) or 0))
    with col6:
        num_vitrinas  = st.number_input("# Vitrinas", 0, step=1,
                            value=int(_hv.get("num_vitrinas", 0) or 0))
        num_gondolas  = st.number_input("# Góndolas", 0, step=1,
                            value=int(_hv.get("num_gondolas", 0) or 0))
        num_gabeteros = st.number_input("# Gaveteros", 0, step=1,
                            value=int(_hv.get("num_gabeteros", 0) or 0))


    st.markdown("**Ubicación**")
    col7, col8 = st.columns(2)
    with col7:
        _ubic_opts = ["Zona comercial", "Barrio", "Via principal"]
        _ubic_val  = _hv.get("ubicacion", "Zona comercial")
        _ubic_idx  = _ubic_opts.index(_ubic_val) if _ubic_val in _ubic_opts else 0
        ubicacion = st.selectbox("Ubicación", _ubic_opts, index=_ubic_idx)
    with col8:
        pass


    st.markdown("**Logística**")
    col9, col10 = st.columns(2)
    with col9:
        _entrega_opts = ["Punto de venta", "Bodega central"]
        _entrega_val  = _hv.get("entrega_de_mercancia", "Punto de venta")
        _entrega_idx  = _entrega_opts.index(_entrega_val) if _entrega_val in _entrega_opts else 0
        entrega_merc = st.radio("Entrega de mercancía", _entrega_opts,
                            index=_entrega_idx, horizontal=True)

        DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        _dias_ped_prev = [d.strip() for d in str(_hv.get("dias_de_pedido", "")).split(",") if d.strip() in DIAS_SEMANA]
        dias_pedido = st.multiselect("Días de pedido", options=DIAS_SEMANA,
                            default=_dias_ped_prev, placeholder="Seleccione uno o más días")

        _dias_vis_prev = [d.strip() for d in str(_hv.get("dias_de_visitas", "")).split(",") if d.strip() in DIAS_SEMANA]
        dias_visita = st.multiselect("Días de visita", options=DIAS_SEMANA,
                            default=_dias_vis_prev, placeholder="Seleccione uno o más días")

        _op_log_val = _hv.get("tiene_operador_logistico", "No")
        _op_log_idx = 0 if _op_log_val == "Sí" else 1
        operador_log = st.radio("¿Tiene operador logístico?", ["Sí", "No"],
                            index=_op_log_idx, horizontal=True)

    with col10:
        _freq_opts = ["Diario", "Semanal", "2 veces x sem", "3 veces x sem"]
        _freq_val  = _hv.get("frecuencia_de_pedido", "Diario")
        _freq_idx  = _freq_opts.index(_freq_val) if _freq_val in _freq_opts else 0
        frecuencia_ped = st.selectbox("Frecuencia de pedido", _freq_opts, index=_freq_idx)
        horario_obs    = st.text_input("Horario recibo obsequios",
                            value=_v("horario_recibo_obsequios"))
        intensidad_h   = st.number_input("Intensidad horaria en la semana", 0, step=1,
                            value=int(_hv.get("intensidad_horaria_semana", 0) or 0))
    
    st.markdown("**Ventas promedio mensuales**")

    def _int_prio(campo_hv, campo_so):
        if _hv.get(campo_hv) not in (None, "", 0):
            return int(_hv[campo_hv])
        v = _so.get(campo_so)
        return int(v) if v not in (None, "") else 0


    _vt = st.session_state.get("ventas_mes_total")
    _vo = st.session_state.get("ventas_mes_otc")
    _vf = st.session_state.get("ventas_mes_foot")
    st.session_state["ventas_mes_total"] = _vt if _vt not in (None, 0) else _int_prio("ventas_por_mes",          "ventas_prom_total")
    st.session_state["ventas_mes_otc"]   = _vo if _vo not in (None, 0) else _int_prio("venta_prom_mes_otc",       "ventas_prom_otc")
    st.session_state["ventas_mes_foot"]  = _vf if _vf not in (None, 0) else _int_prio("venta_prom_mes_foot_care", "ventas_prom_foot")


    col11, col12, col13 = st.columns(3)
    with col11:
        ventas_mes = st.number_input("Venta prom. mes total ($)", 0, step=1000, key="ventas_mes_total", format="%d")
        st.caption(f"$ {fmt_cop(ventas_mes)} COP")
    with col12:
        venta_otc  = st.number_input("Venta prom. mes OTC ($)", 0, step=1000, key="ventas_mes_otc", format="%d")
        st.caption(f"$ {fmt_cop(venta_otc)} COP")
    with col13:
        venta_foot = st.number_input("Venta prom. mes Foot Care ($)", 0, step=1000, key="ventas_mes_foot", format="%d")
        st.caption(f"$ {fmt_cop(venta_foot)} COP")


    st.markdown("**Top marcas más vendidas**")

    _marcas_ss = [st.session_state.get(f"marca_{i}", "") for i in range(1, 6)]
    _vtas_ss   = [st.session_state.get(f"vta_marca_{i}", 0) for i in range(1, 6)]
    _any_marca_loaded = any(m for m in _marcas_ss)

    if not _any_marca_loaded:
        _marcas_prev = _hv.get("top_marcas_mas_vendidas") or []
        if not isinstance(_marcas_prev, list):
            _marcas_prev = []
        if not _marcas_prev and _so.get("sell_out_marcas"):
            _so_marcas_sorted = sorted(
                _so["sell_out_marcas"].items(),
                key=lambda x: max(x[1].get("prom_mes_2026", 0), x[1].get("prom_mes_2025", 0)),
                reverse=True
            )[:5]
            _marcas_prev = [
                {"marca": m, "vtas_prom_mes": x[1].get("prom_mes_2026") or x[1].get("prom_mes_2025", 0)}
                for m, x in _so_marcas_sorted
            ]
        for i in range(1, 6):
            _mp = _marcas_prev[i - 1] if i - 1 < len(_marcas_prev) else {}
            _marcas_ss[i-1] = _mp.get("marca", "") if isinstance(_mp, dict) else ""
            _vtas_ss[i-1]   = int(_mp.get("vtas_prom_mes", 0) if isinstance(_mp, dict) else 0)

    for i in range(1, 6):
        st.session_state[f"marca_{i}"]     = _marcas_ss[i-1]
        st.session_state[f"vta_marca_{i}"] = _vtas_ss[i-1]

    marcas = []
    for i in range(1, 6):
        c1, c2 = st.columns([3, 1])
        with c1:
            marca = st.text_input(f"Marca {i}", key=f"marca_{i}")
        with c2:
            vta_m = st.number_input(f"Vtas prom mes marca {i}", 0, step=1000,
                        key=f"vta_marca_{i}", label_visibility="visible", format="%d")
            st.caption(f"$ {fmt_cop(vta_m)} COP")
        marcas.append({"marca": marca, "vtas_prom_mes": vta_m})


    st.markdown("**Top SKUs más vendidos**")

    _skus_ss  = [st.session_state.get(f"sku_{i}", "") for i in range(1, 6)]
    _vskus_ss = [st.session_state.get(f"vta_sku_{i}", 0) for i in range(1, 6)]
    _any_sku_loaded = any(s for s in _skus_ss)

    if not _any_sku_loaded:
        _skus_prev = _hv.get("top_skus_mas_vendidos") or []
        if not isinstance(_skus_prev, list):
            _skus_prev = []
        if not _skus_prev and _so.get("sell_out_skus"):
            _so_skus_sorted = sorted(
                _so["sell_out_skus"].items(),
                key=lambda x: max(x[1].get("prom_mes_2026", 0), x[1].get("prom_mes_2025", 0)),
                reverse=True
            )[:5]
            _skus_prev = [
                {"sku": s, "vtas_prom_mes": x[1].get("prom_mes_2026") or x[1].get("prom_mes_2025", 0)}
                for s, x in _so_skus_sorted
            ]
        for i in range(1, 6):
            _sp = _skus_prev[i - 1] if i - 1 < len(_skus_prev) else {}
            _skus_ss[i-1]  = _sp.get("sku", "") if isinstance(_sp, dict) else ""
            _vskus_ss[i-1] = int(_sp.get("vtas_prom_mes", 0) if isinstance(_sp, dict) else 0)

    for i in range(1, 6):
        st.session_state[f"sku_{i}"]     = _skus_ss[i-1]
        st.session_state[f"vta_sku_{i}"] = _vskus_ss[i-1]

    skus = []
    for i in range(1, 6):
        c1, c2 = st.columns([3, 1])
        with c1:
            sku = st.text_input(f"SKU {i}", key=f"sku_{i}")
        with c2:
            vta_s = st.number_input(f"Vtas prom mes SKU {i}", 0, step=1000,
                        key=f"vta_sku_{i}", label_visibility="visible", format="%d")
            st.caption(f"$ {fmt_cop(vta_s)} COP")
        skus.append({"sku": sku, "vtas_prom_mes": vta_s})


    # ══════════════════════════════════════════════════════════════════
    # II. SELL OUT
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">II. SELL OUT</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Ingrese ventas mes puntual y acumulado por año (2025 vs 2026). La Var% se calcula automáticamente.</div>', unsafe_allow_html=True)

    _so_prev = _hv.get("sell_out") or {}
    if _so_prev.get("mensual"):
        _so_mensual_prev = {r["mes"]: r for r in _so_prev["mensual"]}
    elif _so.get("sell_out_mensual"):
        _so_mensual_prev = _so["sell_out_mensual"]
    else:
        _so_mensual_prev = {}


    # ── Tabla 1: Sell Out mensual ──────────────────────────────────────
    st.markdown("#### Ventas Bayer — Sell Out mensual")

    MESES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
            "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

    header = st.columns([2, 1, 1, 1, 0.2, 1, 1, 1])
    header[0].markdown("")
    header[1].markdown("<div style='text-align:center;background:#10384f;color:white;padding:4px;border-radius:4px;font-size:0.78rem;'>Sell Out Mes</div>", unsafe_allow_html=True)
    header[5].markdown("<div style='text-align:center;background:#10384f;color:white;padding:4px;border-radius:4px;font-size:0.78rem;'>Sell Out Acumulado</div>", unsafe_allow_html=True)

    sub_header = st.columns([2, 1, 1, 1, 0.2, 1, 1, 1])
    for col, lbl in zip(sub_header, ["**Mes**", "**2025**", "**2026**", "**Var %**", "", "**2025**", "**2026**", "**Var %**"]):
        col.markdown(lbl)

    sell_out_data = []
    for mes in MESES:
        _m_prev = _so_mensual_prev.get(mes, {})
        if f"so_p20_{mes}" not in st.session_state:
            st.session_state[f"so_p20_{mes}"] = int(_m_prev.get("sell_out_mes_2020", 0) or 0)
        if f"so_p21_{mes}" not in st.session_state:
            st.session_state[f"so_p21_{mes}"] = int(_m_prev.get("sell_out_mes_2021", 0) or 0)
        if f"so_a20_{mes}" not in st.session_state:
            st.session_state[f"so_a20_{mes}"] = int(_m_prev.get("sell_out_acum_2020", 0) or 0)
        if f"so_a21_{mes}" not in st.session_state:
            st.session_state[f"so_a21_{mes}"] = int(_m_prev.get("sell_out_acum_2021", 0) or 0)

        cols = st.columns([2, 1, 1, 1, 0.2, 1, 1, 1])
        cols[0].markdown(mes)
        p20 = cols[1].number_input(f"Mes 2025 {mes}", 0, step=1000, key=f"so_p20_{mes}",
                label_visibility="collapsed", format="%d")
        p21 = cols[2].number_input(f"Mes 2026 {mes}", 0, step=1000, key=f"so_p21_{mes}",
                label_visibility="collapsed", format="%d")
        var_p = round(((p21 - p20) / p20 * 100) if p20 > 0 else 0.0, 1)
        cols[3].markdown(f"<div style='text-align:center;padding-top:8px;color:{'green' if var_p >= 0 else 'red'};'><b>{var_p:+.1f}%</b></div>", unsafe_allow_html=True)
        cols[4].markdown("")
        a20 = cols[5].number_input(f"Acum 2025 {mes}", 0, step=1000, key=f"so_a20_{mes}",
                label_visibility="collapsed", format="%d")
        a21 = cols[6].number_input(f"Acum 2026 {mes}", 0, step=1000, key=f"so_a21_{mes}",
                label_visibility="collapsed", format="%d")
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
    totales_cols[1].markdown(f"<div style='{style_total}'>$ {fmt_cop(tot_p20)}</div>", unsafe_allow_html=True)
    totales_cols[2].markdown(f"<div style='{style_total}'>$ {fmt_cop(tot_p21)}</div>", unsafe_allow_html=True)
    totales_cols[3].markdown(f"<div style='{style_total};color:{'green' if var_tp >= 0 else 'red'}'>{var_tp:+.1f}%</div>", unsafe_allow_html=True)
    totales_cols[4].markdown("")
    totales_cols[5].markdown(f"<div style='{style_total}'>$ {fmt_cop(tot_a20)}</div>", unsafe_allow_html=True)
    totales_cols[6].markdown(f"<div style='{style_total}'>$ {fmt_cop(tot_a21)}</div>", unsafe_allow_html=True)
    totales_cols[7].markdown(f"<div style='{style_total};color:{'green' if var_ta >= 0 else 'red'}'>{var_ta:+.1f}%</div>", unsafe_allow_html=True)

    st.markdown("---")


    # ── Tabla 2: Sell Out por Marca / División ─────────────────────────
    st.markdown("#### Sell Out por Marca — Promedio mensual")

    MARCAS_SO = {
        "FOOT CARE": ["MEXSANA TALCO", "MEXSANA SPRAY"],
        "OTC": ["ACID MANTLE", "REDOXON", "ALKA-SELTZER", "ASPIRIN CARDIO",
                "GYNOCANESTEN", "APRONAX", "ASPIRINA DOLOR", "OTRAS"],
    }

    if _so_prev.get("por_marca"):
        _so_marcas_prev = {r["marca"]: r for r in _so_prev["por_marca"]}
    elif _so.get("sell_out_marcas"):
        _so_marcas_prev = {
            marca: {"prom_mes_2020": vals["prom_mes_2020"], "prom_mes_2021": vals["prom_mes_2021"], "peso_pct": 0.0}
            for marca, vals in _so["sell_out_marcas"].items()
        }
    else:
        _so_marcas_prev = {}

    hdr = st.columns([1.5, 2, 1, 1.2, 1.2, 1])
    for col, lbl in zip(hdr, ["**División**", "**Marca**", "**Peso %**", "**Prom mes 2025**", "**Prom mes 2026**", "**Var %**"]):
        col.markdown(lbl)

    def _buscar_marca_so(nombre_formulario: str, indice_so: dict) -> dict:
        nombre_up = nombre_formulario.upper()
        if nombre_up in indice_so:
            return indice_so[nombre_up]
        for k, v in indice_so.items():
            if nombre_up in k or k in nombre_up:
                return v
        return {}

    sell_out_marcas = []
    for division, marcas_list in MARCAS_SO.items():
        rows_div = []
        for idx, marca in enumerate(marcas_list):
            _mp = _so_marcas_prev.get(marca, {}) or _buscar_marca_so(marca, _so_marcas_prev)
            row = st.columns([1.5, 2, 1, 1.2, 1.2, 1])
            if idx == 0:
                row[0].markdown(f"<div style='padding-top:8px;font-weight:600;'>{division}</div>", unsafe_allow_html=True)
            else:
                row[0].markdown("")
            row[1].markdown(f"<div style='padding-top:8px;'>{marca}</div>", unsafe_allow_html=True)
            peso  = row[2].number_input(f"Peso% {marca}", 0.0, 100.0, step=0.1,
                        key=f"som_peso_{marca}", label_visibility="collapsed",
                        value=float(_mp.get("peso_pct", 0.0) or 0.0))
            pm20  = row[3].number_input(f"Prom 2025 {marca}", 0, step=1000,
                        key=f"som_p20_{marca}", label_visibility="collapsed",
                        value=int(_mp.get("prom_mes_2020", 0) or 0), format="%d")
            pm21  = row[4].number_input(f"Prom 2026 {marca}", 0, step=1000,
                        key=f"som_p21_{marca}", label_visibility="collapsed",
                        value=int(_mp.get("prom_mes_2021", 0) or 0), format="%d")
            var_m = round(((pm21 - pm20) / pm20 * 100) if pm20 > 0 else 0.0, 1)
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
        sub_cols[3].markdown(f"<div style='{st_style}'>$ {fmt_cop(st_p20)}</div>", unsafe_allow_html=True)
        sub_cols[4].markdown(f"<div style='{st_style}'>$ {fmt_cop(st_p21)}</div>", unsafe_allow_html=True)
        sub_cols[5].markdown(f"<div style='{st_style};color:{'green' if var_st >= 0 else 'red'}'>{var_st:+.1f}%</div>", unsafe_allow_html=True)

        sell_out_marcas.extend(rows_div)

    # Total general
    all_pm20 = sum(r["prom_mes_2020"] for r in sell_out_marcas)
    all_pm21 = sum(r["prom_mes_2021"] for r in sell_out_marcas)
    var_all  = round(((all_pm21 - all_pm20) / all_pm20 * 100) if all_pm20 > 0 else 0.0, 1)
    tot_cols = st.columns([1.5, 2, 1, 1.2, 1.2, 1])
    tot_style = "background:#b8cce4;padding:4px 6px;border-radius:4px;font-weight:700;font-size:0.82rem;"
    tot_cols[0].markdown(f"<div style='{tot_style}'>TOTAL</div>", unsafe_allow_html=True)
    tot_cols[1].markdown(f"<div style='{tot_style}'></div>", unsafe_allow_html=True)
    tot_cols[2].markdown(f"<div style='{tot_style}'></div>", unsafe_allow_html=True)
    tot_cols[3].markdown(f"<div style='{tot_style}'>$ {fmt_cop(all_pm20)}</div>", unsafe_allow_html=True)
    tot_cols[4].markdown(f"<div style='{tot_style}'>$ {fmt_cop(all_pm21)}</div>", unsafe_allow_html=True)
    tot_cols[5].markdown(f"<div style='{tot_style};color:{'green' if var_all >= 0 else 'red'}'>{var_all:+.1f}%</div>", unsafe_allow_html=True)


    # ══════════════════════════════════════════════════════════════════
    # III. EXHIBICIÓN (Mobile-first)
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">III. EXHIBICIÓN</div>', unsafe_allow_html=True)
    st.caption("* Indique la cantidad y entre paréntesis el mes. Ejemplo: 2 (Ene)")

    MARCAS_EXH = ["Mexsana", "Acid Mantle", "Redoxon", "Alka Seltzer"]
    NUM_FILAS_EXH = 10

    _exh_prev = _hv.get("exhibicion") or []

    exhibicion_rows = []
    for i in range(1, NUM_FILAS_EXH + 1):
        _ep = _exh_prev[i - 1] if i - 1 < len(_exh_prev) else {}
        with st.expander(f"📋 Exhibición {i}", expanded=(i == 1)):
            tipo = st.text_input("Tipo de Exhibición", key=f"exh_tipo_{i}",
                        placeholder="Ej: Counter, Vitrina, Góndola...",
                        value=_ep.get("tipo", "") if isinstance(_ep, dict) else "")
            row = {"tipo": tipo}

            for marca in MARCAS_EXH:
                st.markdown(f"**{marca}**")
                c1, c2 = st.columns(2)
                with c1:
                    g = st.text_input("Gestión", key=f"exh_{marca}_g_{i}",
                            placeholder="cant(mes)",
                            value=_ep.get(f"{marca}_gestion", "") if isinstance(_ep, dict) else "")
                with c2:
                    n = st.text_input("Negoc", key=f"exh_{marca}_n_{i}",
                            placeholder="cant(mes)",
                            value=_ep.get(f"{marca}_negoc", "") if isinstance(_ep, dict) else "")
                row[f"{marca}_gestion"] = g
                row[f"{marca}_negoc"] = n

            st.markdown("**Otro**")
            co1, co2, co3 = st.columns([2, 1, 1])
            with co1:
                otro_marca = st.text_input("Marca", key=f"exh_otro_marca_{i}",
                                placeholder="Nombre marca",
                                value=_ep.get("otro_marca", "") if isinstance(_ep, dict) else "")
            with co2:
                otro_g = st.text_input("Gestión", key=f"exh_otro_g_{i}",
                                placeholder="cant(mes)",
                                value=_ep.get("otro_gestion", "") if isinstance(_ep, dict) else "")
            with co3:
                otro_n = st.text_input("Negoc", key=f"exh_otro_n_{i}",
                                placeholder="cant(mes)",
                                value=_ep.get("otro_negoc", "") if isinstance(_ep, dict) else "")
            row["otro_marca"] = otro_marca
            row["otro_gestion"] = otro_g
            row["otro_negoc"] = otro_n
            exhibicion_rows.append(row)


    # ══════════════════════════════════════════════════════════════════
    # IV. PARTICIPACIÓN EN LINEAL (SOS)
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
        ("ANTIMICOTICOS",  "CANESTEN",         "ANTIMICOTICOS TOPICOS",    True,  True),
        ("ANALGESICOS",    "APRONAX",          "ANALGESICOS DOLOR FUERTE", False, False),
        ("ANALGESICOS",    "ASP ULTRA + EFER", "ANALGESICOS DOLOR GENERAL",False, False),
        ("PREVENCION",     "ASA 100",          "PREVENCION CORAZON",       False, False),
        ("ANTIGRIPALES",   "TABCIN",           "ANTIGRIPALES",             False, False),
    ]

    _sos_prev = {r["marca"]: r for r in (_hv.get("participacion_lineal_sos") or [])}

    sos_data = []
    cat_actual = None
    for (cat, marca, universo_sos, blq_u1, blq_u2) in CATEGORIAS_SOS:
        if cat != cat_actual:
            st.markdown(f"""
            <div style='background:#2e75b6;color:white;padding:5px 10px;
            border-radius:5px;font-weight:700;font-size:0.85rem;margin-top:12px;'>
            {cat}
            </div>""", unsafe_allow_html=True)
            cat_actual = cat

        _sp = _sos_prev.get(marca, {})
        with st.expander(f"🔹 {marca} — {universo_sos}", expanded=False):
            obj = st.number_input("% SOS Objetivo", 0.0, 100.0, step=0.5,
                        key=f"sos_obj_{marca}",
                        value=float(_sp.get("pct_sos_objetivo", 0.0) or 0.0))

            st.markdown("**1er Semestre**")
            s1c1, s1c2 = st.columns(2)
            with s1c1:
                if blq_u1:
                    st.markdown("<div style='background:#222;height:38px;border-radius:4px;margin-top:4px;'></div>", unsafe_allow_html=True)
                    u1 = None
                else:
                    u1 = st.text_input("UNIV CMS", key=f"sos_u1_{marca}",
                            value=str(_sp.get("univ_cms_1s", "") or ""))
            with s1c2:
                c1 = st.text_input("CMS", key=f"sos_c1_{marca}",
                        value=str(_sp.get("cms_1s", "") or ""))

            st.markdown("**2do Semestre**")
            s2c1, s2c2 = st.columns(2)
            with s2c1:
                if blq_u2:
                    st.markdown("<div style='background:#222;height:38px;border-radius:4px;margin-top:4px;'></div>", unsafe_allow_html=True)
                    u2 = None
                else:
                    u2 = st.text_input("UNIV CMS", key=f"sos_u2_{marca}",
                            value=str(_sp.get("univ_cms_2s", "") or ""))
            with s2c2:
                c2 = st.text_input("CMS", key=f"sos_c2_{marca}",
                        value=str(_sp.get("cms_2s", "") or ""))

            sos_data.append({
                "categoria": cat, "marca": marca, "universo": universo_sos,
                "pct_sos_objetivo": obj,
                "univ_cms_1s": u1, "cms_1s": c1,
                "univ_cms_2s": u2, "cms_2s": c2,
            })


    # ══════════════════════════════════════════════════════════════════
    # V. OPORTUNIDADES DE EXHIBICIÓN
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">V. OPORTUNIDADES DE EXHIBICIÓN</div>', unsafe_allow_html=True)

    _oe_prev = _hv.get("oportunidad_exhibicion") or {}

    # ── 1. Exhibición Caja Registradora ───────────────────────────────
    st.markdown("""
    <div style='background:#2196a8;color:white;text-align:center;padding:6px;
    border-radius:5px;font-weight:700;font-size:0.88rem;margin-bottom:8px;'>
    Exhibición Caja Registradora
    </div>""", unsafe_allow_html=True)
    st.caption("* El pdv tiene este tipo de exhibición SI/NO; cuantas XX.")

    num_cajas = st.number_input("# Cajas registradoras", min_value=0, step=1, key="num_cajas",
                    value=int(_oe_prev.get("num_cajas_registradoras", 0) or 0))

    ITEMS_CAJA = [
        "Counter", "Mueble sobre vitrina", "Tiburón", "Módulo",
        "Balconera", "Bandeja", "Espacio para Ristra",
        "Espacio para Ganchera", "Entrepaño en vitrina",
    ]
    _caja_prev = {r["ubicacion"]: r for r in (_oe_prev.get("exhibicion_caja_registradora") or [])}

    exh_caja = []
    for item in ITEMS_CAJA:
        _cp = _caja_prev.get(item, {})
        with st.expander(f"📦 {item}", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                _tiene_val = _cp.get("tiene", "No")
                tiene = st.radio("¿Tiene?", ["Sí", "No"], key=f"caja_tiene_{item}",
                            horizontal=True,
                            index=0 if _tiene_val == "Sí" else 1)
            with c2:
                cant = st.number_input("Cantidad", min_value=0, step=1,
                            key=f"caja_cant_{item}",
                            value=int(_cp.get("cantidad", 0) or 0))
            exh_caja.append({"ubicacion": item, "tiene": tiene, "cantidad": cant})

    # ── 2. Exhibición diferente a Puestos de pago ─────────────────────
    st.markdown("""
    <div style='background:#2196a8;color:white;text-align:center;padding:6px;
    border-radius:5px;font-weight:700;font-size:0.88rem;margin:12px 0 8px 0;'>
    Exhibición diferente a Puestos de pago
    </div>""", unsafe_allow_html=True)
    st.caption("* Otros: Botadero")

    ITEMS_PDV = [
        "Punta de góndola", "Tope de tope", "Rejilla o lateral",
        "Mueble proveedor", "Mueble cliente", "Otros",
    ]
    _pdv_prev = {r["ubicacion"]: r for r in (_oe_prev.get("exhibicion_diferente_puestos_pago") or [])}

    exh_pdv = []
    for item in ITEMS_PDV:
        _pp = _pdv_prev.get(item, {})
        with st.expander(f"🏪 {item}", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                _tiene_val = _pp.get("tiene", "No")
                tiene = st.radio("¿Tiene?", ["Sí", "No"], key=f"pdv_tiene_{item}",
                            horizontal=True,
                            index=0 if _tiene_val == "Sí" else 1)
            with c2:
                cant = st.number_input("Cantidad", min_value=0, step=1,
                            key=f"pdv_cant_{item}",
                            value=int(_pp.get("cantidad", 0) or 0))
            if item == "Otros":
                obs = st.text_input("¿Cuál? (observaciones)", key=f"pdv_obs_{item}",
                            placeholder="Ej: Botadero",
                            value=_pp.get("observaciones", "") or "")
            else:
                obs = st.text_input("Observaciones", key=f"pdv_obs_{item}",
                            placeholder="Opcional",
                            value=_pp.get("observaciones", "") or "")
            exh_pdv.append({"ubicacion": item, "tiene": tiene, "cantidad": cant, "observaciones": obs})

    # ── 3. Espacios para visibilidad ──────────────────────────────────
    st.markdown("""
    <div style='background:#2196a8;color:white;text-align:center;padding:6px;
    border-radius:5px;font-weight:700;font-size:0.88rem;margin:12px 0 8px 0;'>
    Espacios para visibilidad
    </div>""", unsafe_allow_html=True)

    ITEMS_VIS = ["Antena", "Cajonero", "Puesto de pago", "Ventanal", "Pared", "Floorgraphic"]
    _vis_prev = {r["tipo"]: r for r in (_oe_prev.get("espacios_visibilidad") or [])}

    exh_visibilidad = []
    for item in ITEMS_VIS:
        _vp = _vis_prev.get(item, {})
        with st.expander(f"👁 {item}", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                _tiene_val = _vp.get("tiene", "No")
                tiene = st.radio("¿Tiene?", ["Sí", "No"], key=f"vis_tiene_{item}",
                            horizontal=True,
                            index=0 if _tiene_val == "Sí" else 1)
            with c2:
                cant = st.number_input("Cantidad", min_value=0, step=1,
                            key=f"vis_cant_{item}",
                            value=int(_vp.get("cantidad", 0) or 0))
            exh_visibilidad.append({"tipo": item, "tiene": tiene, "cantidad": cant})

    oportunidades_exhibicion = {
        "num_cajas_registradoras": int(num_cajas),
        "exhibicion_caja_registradora":        exh_caja,
        "exhibicion_diferente_puestos_pago":   exh_pdv,
        "espacios_visibilidad":                exh_visibilidad,
    }


    # ══════════════════════════════════════════════════════════════════
    # VI. COMPETIDORES CERCANOS
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">VI. COMPETIDORES CERCANOS</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">¿Cuántos PDV de estos formatos hay en un radio de 10 cuadras a la redonda?</div>', unsafe_allow_html=True)

    _comp_prev = _hv.get("competidores_cercanos") or {}

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
            val = col.number_input(cadena, 0, step=1, key=f"comp_{cadena}",
                        value=int(_comp_prev.get(cadena, 0) or 0))
            competidores_data[cadena] = val


    # ══════════════════════════════════════════════════════════════════
    # VII. COMENTARIOS RELEVANTES
    # ══════════════════════════════════════════════════════════════════
    st.markdown('<div class="section-header">VII. COMENTARIOS RELEVANTES</div>', unsafe_allow_html=True)
    comentarios = st.text_area("Comentarios relevantes del PDV", height=120,
                    value=_hv.get("comentarios_relevnates", "") or "")

    st.divider()


    # ══════════════════════════════════════════════════════════════════
    # BOTÓN ENVIAR
    # ══════════════════════════════════════════════════════════════════
    if st.button("✅ Enviar Solicitud", type="primary", use_container_width=True):

        payload = {
            # Sección I — columnas exactas de hoja_vida_cadenas_farmacias
            "nombre_cadena":              nombre_cadena,
            "punto_de_venta":             punto_de_venta,
            "dependenci_pdv":             dependenci_pdv,
            "telefono":                   telefono,
            "direccion":                  direccion,
            "nombre_gerente_pdv":         nombre_gerente,
            "nombre_cargo_contacto":      nombre_contacto,
            "ranking_pdv_total_nacional": ranking_nac,
            "ranking_pdv_cadena_nacional":ranking_cad_nac,
            "ranking_pdv_cadena_regional":ranking_cad_reg,
            "ranking_pdv_zona_asignada":  ranking_zona,
            "tiene_domicilio":            tiene_domicilio,
            "horas":                      horas_24,
            "centralizado":               centralizado,
            "pdv":                        pdv_check,
            "ventas_por_mes":             int(ventas_mes),
            "venta_prom_mes_otc":         int(venta_otc),
            "venta_prom_mes_foot_care":   int(venta_foot),
            "top_marcas_mas_vendidas":    marcas,
            "top_skus_mas_vendidos":      skus,
            "drogueria_tipo_autoservicio":autoservicio,
            "ocounter":                   ocounter,
            "num_dependientes":           int(num_dep),
            "num_turnos":                 int(num_turnos),
            "porc_venta_domicilio":       int(porc_domicilio),
            "telefonista":                telefonista,
            "ubicacion":                  ubicacion,
            "nodo_o_central":             nodo_central,
            "num_vitrinas":               int(num_vitrinas),
            "num_gondolas":               int(num_gondolas),
            "num_gabeteros":              int(num_gabeteros),
            "entrega_de_mercancia":       entrega_merc,
            "dias_de_pedido":             ", ".join(dias_pedido),
            "dias_de_visitas":            ", ".join(dias_visita),
            "tiene_operador_logistico":   operador_log,
            "frecuencia_de_pedido":       frecuencia_ped,
            "horario_recibo_obsequios":   horario_obs,
            "intensidad_horaria_semana":  int(intensidad_h),

            # Sección II
            "sell_out": {
                "mensual": sell_out_data,
                "por_marca": sell_out_marcas,
            },

            # Sección III
            "exhibicion":                 exhibicion_rows,

            # Sección IV
            "participacion_lineal_sos":   sos_data,

            # Sección V
            "oportunidad_exhibicion":     oportunidades_exhibicion,

            # Sección VI
            "competidores_cercanos":      competidores_data,

            # Sección VII
            "comentarios_relevnates":     comentarios,
        }

        with st.spinner("Guardando en Supabase..."):
            ok, result, accion = upsert_hoja_vida(payload)

        if ok:
            if accion == 'actualizado':
                st.success(f"✅ Registro **actualizado** exitosamente. ID: {result}")
            else:
                st.success(f"✅ Registro **insertado** exitosamente. ID: {result}")
            st.balloons()
        else:
            st.error(f"❌ Error al guardar: {result}")


if __name__ == "__main__":
    main()
