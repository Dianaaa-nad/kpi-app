"""
calculation_service.py — Kalkulasi skor KPI per periode

Alur:
    load_data()
        → calculate_combine()   (butuh formula_components terisi)
        → calculate_ratio()     (butuh formula_components terisi)
        → calculate_growth()    (butuh formula_components terisi)
        → loop per (cabang × variabel) → achievement → score
        → save_variable_scores()   (UPSERT)
        → save_kpi_score_records() (UPSERT cabang + area)
"""

import pandas as pd
import numpy as np
from datetime import date

from db import get_engine, get_connection
from services.formula_services import (
    calculate_combine,
    calculate_ratio,
    calculate_growth,
)

FORMULA_TYPES = {"combine", "percentation", "growth"}


# ====================================================================
# LOAD DATA
# ====================================================================

def load_realisasi_wide(engine, periode: date, baseline_periode: date):
    periode_col  = str(periode)
    baseline_col = str(baseline_periode)

    current_df = pd.read_sql(
        """
        SELECT b.kdo_bsi, v.var_code, r.value AS val
        FROM   kpi_realizations r
        JOIN   branches         b ON r.branch_id   = b.branch_id
        JOIN   kpi_variables    v ON r.variable_id = v.variable_id
        WHERE  r.periode = %(p)s
        """,
        engine,
        params={"p": str(periode)},
    ).rename(columns={"val": periode_col})
    current_df = current_df.drop_duplicates(subset=["kdo_bsi", "var_code"], keep="last")

    baseline_df = pd.read_sql(
        """
        SELECT b.kdo_bsi, v.var_code, r.value AS val
        FROM   kpi_realizations r
        JOIN   branches         b ON r.branch_id   = b.branch_id
        JOIN   kpi_variables    v ON r.variable_id = v.variable_id
        WHERE  r.periode = %(p)s
        """,
        engine,
        params={"p": str(baseline_periode)},
    ).rename(columns={"val": baseline_col})
    baseline_df = baseline_df.drop_duplicates(subset=["kdo_bsi", "var_code"], keep="last")

    merged = current_df.merge(
        baseline_df[["kdo_bsi", "var_code", baseline_col]],
        on=["kdo_bsi", "var_code"],
        how="left",
    )

    return merged, periode_col, baseline_col


def load_configs(engine, periode: date):
    return pd.read_sql(
        """
        SELECT config_id, variable_id, periode, formula_type,
               is_displayed, max_weight
        FROM   variable_configs
        WHERE  periode = %(p)s
        """,
        engine,
        params={"p": str(periode)},
    )


def load_components(engine):
    return pd.read_sql("SELECT * FROM formula_components", engine)


def load_variables(engine):
    return pd.read_sql("SELECT * FROM kpi_variables", engine)


def load_targets(engine, periode: date):
    df = pd.read_sql(
        """
        SELECT b.kdo_bsi, v.var_code, t.target_value
        FROM   kpi_targets   t
        JOIN   branches      b ON t.branch_id   = b.branch_id
        JOIN   kpi_variables v ON t.variable_id = v.variable_id
        WHERE  t.periode = %(p)s
        """,
        engine,
        params={"p": str(periode)},
    )
    return df.drop_duplicates(subset=["kdo_bsi", "var_code"], keep="last")


def load_branches(engine):
    return pd.read_sql(
        "SELECT branch_id, kdo_bsi, area_id, condition_id FROM branches",
        engine,
    )


def load_weights(engine, periode: date):
    return pd.read_sql(
        """
        SELECT vcw.condition_id, vcw.config_id, vcw.weight
        FROM   variable_config_weights vcw
        JOIN   variable_configs        vc ON vc.config_id = vcw.config_id
        WHERE  vc.periode = %(p)s
        """,
        engine,
        params={"p": str(periode)},
    )


# ====================================================================
# ACHIEVEMENT & SCORE
# ====================================================================

def calculate_achievement(realization, target, var_type="POSITIVE"):
    if target is None or pd.isna(target) or target == 0:
        return 100.0
    if realization is None or pd.isna(realization):
        return 0.0
    if var_type == "POSITIVE":
        return (realization / target) * 100
    elif var_type == "NEGATIVE":
        if realization == 0:
            return 100.0
        return (target / realization) * 100
    return 0.0


def calculate_score(achievement, weight, max_weight):
    if achievement is None or pd.isna(achievement) or weight is None:
        return 0.0
    cap = float(max_weight) if (max_weight is not None and not pd.isna(max_weight)) else 100.0
    capped = max(0.0, min(achievement, cap))
    return (capped / 100) * weight


# ====================================================================
# MAIN: CALCULATE PERIOD
# ====================================================================

def calculate_period(conn, periode):
    if isinstance(periode, str):
        periode = date.fromisoformat(periode)

    baseline_periode = date(periode.year - 1, 12, 1)

    print(f"[INFO] Periode: {periode}  |  Baseline: {baseline_periode}")

    engine = get_engine()

    # ── 1. Load Data ─────────────────────────────────────────────────
    realisasi_df, periode_col, baseline_col = load_realisasi_wide(
        engine, periode, baseline_periode
    )
    configs    = load_configs(engine, periode)
    components = load_components(engine)
    variables  = load_variables(engine)
    targets    = load_targets(engine, periode)
    branches   = load_branches(engine)
    weights_df = load_weights(engine, periode)

    if realisasi_df.empty:
        print(f"[SKIP] Tidak ada realisasi untuk periode {periode}")
        return None
    if configs.empty:
        print(f"[SKIP] Tidak ada variable_configs untuk periode {periode}")
        return None

    print(f"[INFO] {len(realisasi_df)} realisasi | {len(configs)} configs | "
          f"{len(branches)} cabang | {len(components)} components")

    period_cols = [periode_col]

    # ── 2. Jalankan Formula ──────────────────────────────────────────
    realisasi_df = calculate_combine(
        realisasi_df, configs, components, variables,
        period_cols, baseline_col=baseline_col,
    )
    realisasi_df = calculate_ratio(
        realisasi_df, configs, components, variables,
        period_cols, baseline_col=baseline_col,
    )
    realisasi_df = calculate_growth(
        realisasi_df, configs, components, variables,
        period_cols, baseline_col,
    )

    # ── 3. Hitung Score ──────────────────────────────────────────────
    # FIX: tidak lagi memisah formula_configs vs direct_configs.
    #
    # Pemisahan lama menggunakan:
    #   formula_configs = configs[configs["formula_type"].isin(FORMULA_TYPES)]
    #   direct_configs  = configs[~configs["formula_type"].isin(FORMULA_TYPES)]
    #
    # Bug: pandas .isin() mengembalikan False untuk NaN/None, dan ~False = True,
    # sehingga baris dengan formula_type=NULL masuk ke direct_configs. Tapi
    # karena closure _score_configs di-call dua kali dan all_scores di-append
    # keduanya, config yang formula_type-nya tidak terduga bisa diproses dua
    # kali → baris duplikat di all_scores → total_score double.
    #
    # Solusi: loop satu kali saja. formula_type_used diisi jika nilainya
    # termasuk FORMULA_TYPES, None jika tidak (direct/raw).

    all_scores = []

    for _, config in configs.iterrows():
        config_id         = config["config_id"]
        variable_id       = config["variable_id"]
        is_displayed      = bool(config["is_displayed"])
        formula_type      = config["formula_type"]
        max_weight        = config["max_weight"]

        # formula_type_used: hanya isi jika termasuk enum yang valid
        formula_type_used = (
            formula_type
            if (isinstance(formula_type, str) and formula_type in FORMULA_TYPES)
            else None
        )

        var_row = variables[variables["variable_id"] == variable_id]
        if var_row.empty:
            continue

        var_code = var_row.iloc[0]["var_code"]
        var_type = var_row.iloc[0]["type"]

        result_df = realisasi_df[
            realisasi_df["var_code"] == var_code
        ][["kdo_bsi", periode_col]].copy()

        if result_df.empty:
            print(f"  [WARN] Tidak ada data realisasi untuk {var_code}")
            continue

        result_df["realization_used"] = pd.to_numeric(
            result_df[periode_col], errors="coerce"
        )

        tgt = targets[targets["var_code"] == var_code][
            ["kdo_bsi", "target_value"]
        ]
        result_df = result_df.merge(tgt, on="kdo_bsi", how="left")
        result_df["target_used"] = pd.to_numeric(
            result_df["target_value"], errors="coerce"
        )

        result_df = result_df.merge(
            branches[["kdo_bsi", "branch_id", "condition_id"]],
            on="kdo_bsi",
            how="left",
        )

        w_map = weights_df[weights_df["config_id"] == config_id][
            ["condition_id", "weight"]
        ]
        result_df = result_df.merge(w_map, on="condition_id", how="left")
        result_df["weight_used"] = result_df["weight"].fillna(0)

        result_df["pencapaian"] = result_df.apply(
            lambda r: calculate_achievement(
                r["realization_used"], r["target_used"], var_type
            ),
            axis=1,
        )
        result_df["score"] = result_df.apply(
            lambda r, mw=max_weight: calculate_score(
                r["pencapaian"], r["weight_used"], mw
            ),
            axis=1,
        )

        result_df["variable_id"]       = variable_id
        result_df["formula_type_used"] = formula_type_used
        result_df["periode"]           = periode
        result_df["is_displayed"]      = is_displayed

        all_scores.append(
            result_df[[
                "branch_id", "variable_id", "periode",
                "realization_used", "target_used", "pencapaian",
                "weight_used", "score", "formula_type_used",
                "is_displayed",
            ]]
        )

    if not all_scores:
        print("[SKIP] Tidak ada skor yang dihasilkan")
        return None

    final_scores = pd.concat(all_scores, ignore_index=True)
    final_scores = final_scores[final_scores["branch_id"].notna()].copy()
    final_scores["branch_id"] = final_scores["branch_id"].astype(int)

    print(f"[INFO] Total skor: {len(final_scores)} baris | "
          f"is_displayed=True: {final_scores['is_displayed'].sum()} baris")

    # ── DEBUG: tampilkan rincian skor satu cabang sebelum disimpan ──────
    sample_branch_id = int(final_scores["branch_id"].iloc[2])
    sample_branch    = final_scores[final_scores["branch_id"] == sample_branch_id].copy()

    displayed   = sample_branch[sample_branch["is_displayed"] == True]
    undisplayed = sample_branch[sample_branch["is_displayed"] == False]

    # Lookup var_code untuk branch_id sample (join ke variables via variable_id)
    var_lookup = variables.set_index("variable_id")["var_code"].to_dict()
    displayed_debug = displayed.copy()
    displayed_debug["var_code"] = displayed_debug["variable_id"].map(var_lookup)

    print(f"\n{'='*60}")
    print(f"[DEBUG] Sample branch_id : {sample_branch_id}")
    print(f"[DEBUG] Total variabel   : {len(sample_branch)} "
          f"(is_displayed=True: {len(displayed)}, False: {len(undisplayed)})")
    print(f"\n[DEBUG] Variabel yang MASUK ke kpi_score_records (is_displayed=True):")
    print(
        displayed_debug[["var_code", "variable_id", "pencapaian", "weight_used", "score"]]
        .sort_values("var_code")
        .to_string(index=False)
    )
    print(f"\n[DEBUG] total_score cabang ini : "
          f"{displayed['score'].sum():.6f}")
    if len(undisplayed) > 0:
        undisplayed_debug = undisplayed.copy()
        undisplayed_debug["var_code"] = undisplayed_debug["variable_id"].map(var_lookup)
        print(f"\n[DEBUG] Variabel yang TIDAK masuk (is_displayed=False):")
        print(
            undisplayed_debug[["var_code", "variable_id", "score"]]
            .sort_values("var_code")
            .to_string(index=False)
        )
    print(f"{'='*60}\n")
    # ── END DEBUG ────────────────────────────────────────────────────

    # ── 4. Simpan ke DB ──────────────────────────────────────────────
    n_scores  = save_variable_scores(conn, final_scores)
    n_records = save_kpi_score_records(conn, final_scores, branches, periode)
    conn.commit()

    print(f"[OK] {n_scores} variable_scores | {n_records} kpi_score_records")

    return {"variable_scores": n_scores, "score_records": n_records}


# ====================================================================
# SIMPAN KE DB
# ====================================================================

def save_variable_scores(conn, final_scores: pd.DataFrame) -> int:
    """
    UPSERT semua variable_scores — termasuk variabel is_displayed=False
    agar data audit tetap lengkap.
    """
    sql = """
        INSERT INTO variable_scores
            (branch_id, variable_id, periode,
             realization_used, target_used, pencapaian,
             weight_used, score, formula_type_used)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            realization_used  = VALUES(realization_used),
            target_used       = VALUES(target_used),
            pencapaian        = VALUES(pencapaian),
            weight_used       = VALUES(weight_used),
            score             = VALUES(score),
            formula_type_used = VALUES(formula_type_used)
    """

    def _f(v):
        return float(v) if pd.notna(v) else None

    valid_types = {"combine", "percentation", "growth"}

    data = [
        (
            int(r.branch_id),
            int(r.variable_id),
            str(r.periode),
            _f(r.realization_used),
            _f(r.target_used),
            _f(r.pencapaian),
            _f(r.weight_used),
            _f(r.score),
            r.formula_type_used if r.formula_type_used in valid_types else None,
        )
        for r in final_scores.itertuples(index=False)
    ]

    with conn.cursor() as cur:
        cur.executemany(sql, data)

    return len(data)


def save_kpi_score_records(
    conn,
    final_scores: pd.DataFrame,
    branches: pd.DataFrame,
    periode: date,
) -> int:
    """
    Hitung total_score per cabang dan per area.
    Hanya variabel dengan is_displayed=True yang dijumlahkan.
    """
    sql_upsert = """
        INSERT INTO kpi_score_records (entity_id, entity_type, periode, total_score)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE total_score = VALUES(total_score)
    """

    displayed_scores = final_scores[final_scores["is_displayed"] == True].copy()

    if displayed_scores.empty:
        print("[WARN] Tidak ada skor dengan is_displayed=True")
        return 0

    # ── Per Cabang ───────────────────────────────────────────────────
    branch_totals = (
        displayed_scores
        .groupby("branch_id")["score"]
        .sum()
        .reset_index()
        .rename(columns={"score": "total_score"})
    )

    branch_data = [
        (int(r.branch_id), "branch", str(periode), float(r.total_score))
        for r in branch_totals.itertuples(index=False)
    ]
    with conn.cursor() as cur:
        cur.executemany(sql_upsert, branch_data)

    # ── Per Area ─────────────────────────────────────────────────────
    area_totals = (
        branch_totals
        .merge(branches[["branch_id", "area_id"]], on="branch_id", how="left")
        .groupby("area_id")["total_score"]
        .mean()
        .reset_index()
    )

    area_data = [
        (int(r.area_id), "area", str(periode), float(r.total_score))
        for r in area_totals.itertuples(index=False)
    ]
    with conn.cursor() as cur:
        cur.executemany(sql_upsert, area_data)

    return len(branch_data) + len(area_data)