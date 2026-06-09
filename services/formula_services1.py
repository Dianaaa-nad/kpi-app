"""
formula_services.py — Kalkulasi formula KPI (combine, percentation, growth)

Format DataFrame: semi-long
    kdo_bsi | var_code | {periode_col} | {baseline_col}

Opsi A: calculate_combine() menghitung SUM untuk periode_col DAN baseline_col
sekaligus dalam memory, sehingga growth bisa memakai baseline combine yang benar.
"""

import pandas as pd
import numpy as np


# ====================================================================
# HELPER
# ====================================================================

def _to_numeric_cols(df, cols):
    """Konversi kolom ke numerik secara in-place, return df."""
    existing = [c for c in cols if c in df.columns]
    df[existing] = df[existing].apply(pd.to_numeric, errors="coerce")
    return df


# ====================================================================
# COMBINE
# ====================================================================

def calculate_combine(
    realisasi_df,
    configs_df,
    components_df,
    variables_df,
    period_cols,
    baseline_col=None,      # ← Opsi A: baseline ikut di-combine juga
):
    """
    Untuk setiap config bertipe 'combine':
        target_var = sum(source_var_1, source_var_2, ...)

    Dengan Opsi A, jika baseline_col diberikan, kolom baseline juga
    dijumlahkan sehingga hasil combine siap dipakai oleh calculate_growth().

    Contoh KONSUMER:
        KONSUMER[2026-03-01] = GRIYA + OTO + PENSIUN + MITRAGUNA  (periode)
        KONSUMER[2025-12-01] = GRIYA + OTO + PENSIUN + MITRAGUNA  (baseline)

    Hasil ditambahkan sebagai baris baru ke realisasi_df.
    """
    combined_rows = []

    combine_configs = configs_df[configs_df["formula_type"] == "combine"]

    # Kolom yang perlu dihitung: periode + baseline (jika ada)
    sum_cols = list(period_cols)
    if baseline_col and baseline_col not in sum_cols:
        sum_cols = sum_cols + [baseline_col]

    for _, config in combine_configs.iterrows():

        config_id          = config["config_id"]
        target_variable_id = config["variable_id"]

        target_var_row = variables_df[
            variables_df["variable_id"] == target_variable_id
        ]
        if target_var_row.empty:
            continue
        target_var_code = target_var_row.iloc[0]["var_code"]

        # Source variable IDs dari formula_components
        components = components_df[components_df["config_id"] == config_id]
        source_ids = components["source_variable_id"].tolist()

        if not source_ids:
            continue

        source_codes = variables_df[
            variables_df["variable_id"].isin(source_ids)
        ]["var_code"].tolist()

        temp = realisasi_df[
            realisasi_df["var_code"].isin(source_codes)
        ].copy()

        if temp.empty:
            continue

        # Kolom yang benar-benar ada di DataFrame
        existing_cols = [c for c in sum_cols if c in temp.columns]
        temp = _to_numeric_cols(temp, existing_cols)

        # Sum per cabang untuk semua kolom (periode + baseline)
        temp = (
            temp.groupby(["kdo_bsi"], as_index=False)[existing_cols]
            .sum(min_count=1)
        )
        temp["var_code"] = target_var_code

        combined_rows.append(temp)

    if combined_rows:
        df_combined = pd.concat(combined_rows, ignore_index=True)
        realisasi_df = pd.concat(
            [realisasi_df, df_combined], ignore_index=True
        )

    return realisasi_df


# ====================================================================
# PERCENTATION
# ====================================================================

def calculate_ratio(
    realisasi_df,
    configs_df,
    components_df,
    variables_df,
    period_cols,
    baseline_col=None,      # simetris dengan combine, jarang dipakai
):
    """
    Untuk setiap config bertipe 'percentation':
        target_var = numerator_var / denominator_var
    """
    ratio_rows = []

    ratio_configs = configs_df[configs_df["formula_type"] == "percentation"]

    calc_cols = list(period_cols)
    if baseline_col and baseline_col not in calc_cols:
        calc_cols = calc_cols + [baseline_col]

    for _, config in ratio_configs.iterrows():

        config_id          = config["config_id"]
        target_variable_id = config["variable_id"]

        target_var_row = variables_df[
            variables_df["variable_id"] == target_variable_id
        ]
        if target_var_row.empty:
            continue
        target_var_code = target_var_row.iloc[0]["var_code"]

        components = components_df[components_df["config_id"] == config_id]
        num_rows   = components[components["role"] == "numerator"]
        den_rows   = components[components["role"] == "denominator"]

        if num_rows.empty or den_rows.empty:
            continue

        numerator_id   = num_rows.iloc[0]["source_variable_id"]
        denominator_id = den_rows.iloc[0]["source_variable_id"]

        num_code = variables_df[
            variables_df["variable_id"] == numerator_id
        ]["var_code"].iloc[0]
        den_code = variables_df[
            variables_df["variable_id"] == denominator_id
        ]["var_code"].iloc[0]

        num_df = realisasi_df[realisasi_df["var_code"] == num_code].copy()
        den_df = realisasi_df[realisasi_df["var_code"] == den_code].copy()

        if num_df.empty or den_df.empty:
            continue

        ratio = num_df.merge(
            den_df, on="kdo_bsi", suffixes=("_num", "_den")
        )

        existing_cols = [c for c in calc_cols if c in num_df.columns]
        for col in existing_cols:
            num_col = f"{col}_num" if f"{col}_num" in ratio.columns else col
            den_col = f"{col}_den" if f"{col}_den" in ratio.columns else col

            num_val = pd.to_numeric(ratio[num_col], errors="coerce")
            den_val = pd.to_numeric(ratio[den_col], errors="coerce")                    

            ratio[col] = np.where(
                den_val == 0, np.nan, (num_val / den_val) * 100
            )

        result = ratio[["kdo_bsi"] + existing_cols].copy()
        result["var_code"] = target_var_code
        ratio_rows.append(result)        

    if ratio_rows:
        df_ratio = pd.concat(ratio_rows, ignore_index=True)
        realisasi_df = pd.concat(
            [realisasi_df, df_ratio], ignore_index=True
        )

    realisasi_df = realisasi_df.sort_values(
        ["kdo_bsi", "var_code"]
    ).reset_index(drop=True)
    
    print("DEBUG HASIL")
    print(
        realisasi_df[
            realisasi_df["kdo_bsi"] == "ID0010016"
        ].to_string()
    )

    return realisasi_df


# ====================================================================
# GROWTH
# ====================================================================

def calculate_growth(
    realisasi_df,
    configs_df,
    components_df,
    variables_df,
    period_cols,
    baseline_col,
):
    """
    Untuk setiap config bertipe 'growth':
        target_var[periode] = source_var[periode] - source_var[baseline_dec]

    Karena calculate_combine() sudah menghitung baseline untuk variabel
    combine (Opsi A), growth yang sourcenya adalah hasil combine
    (seperti CONSUMER_GROWTH ← KONSUMER) juga akan benar.

    Contoh lengkap CONSUMER_GROWTH_YTD:
        1. combine  : KONSUMER[Mar] = GRIYA+OTO+PENSIUN+MITRAGUNA (Mar)
                      KONSUMER[Des] = GRIYA+OTO+PENSIUN+MITRAGUNA (Des)
        2. growth   : CONSUMER_GROWTH[Mar] = KONSUMER[Mar] - KONSUMER[Des]
    """
    growth_rows = []

    growth_configs = configs_df[configs_df["formula_type"] == "growth"]

    for _, config in growth_configs.iterrows():

        config_id          = config["config_id"]
        target_variable_id = config["variable_id"]

        target_var_row = variables_df[
            variables_df["variable_id"] == target_variable_id
        ]
        if target_var_row.empty:
            continue
        target_var_code = target_var_row.iloc[0]["var_code"]

        components = components_df[components_df["config_id"] == config_id]
        subj_rows  = components[components["role"] == "subject"]

        if subj_rows.empty:
            print(f"  [WARN] Growth config {config_id} ({target_var_code}): "
                  f"tidak ada subject di formula_components")
            continue

        subject_id = subj_rows.iloc[0]["source_variable_id"]

        subject_code_row = variables_df[
            variables_df["variable_id"] == subject_id
        ]
        if subject_code_row.empty:
            continue
        subject_code = subject_code_row.iloc[0]["var_code"]

        # Ambil data subject — setelah combine, ini sudah berisi nilai
        # baseline yang benar jika subject adalah variabel combine
        temp = realisasi_df[
            realisasi_df["var_code"] == subject_code
        ].copy()

        if temp.empty:
            print(f"  [WARN] Growth config {config_id} ({target_var_code}): "
                  f"tidak ada data untuk subject '{subject_code}'")
            continue

        if baseline_col not in temp.columns:
            print(f"  [WARN] Growth config {config_id} ({target_var_code}): "
                  f"kolom baseline '{baseline_col}' tidak ada")
            continue

        existing_cols = [c for c in period_cols if c in temp.columns]
        all_num_cols  = existing_cols + [baseline_col]
        temp = _to_numeric_cols(temp, all_num_cols)

        # Growth = current - baseline
        baseline_series = temp[baseline_col].values
        for col in existing_cols:
            temp[col] = temp[col].values - baseline_series

        temp["var_code"] = target_var_code
        growth_rows.append(
            temp[["kdo_bsi", "var_code"] + existing_cols].copy()
        )

    if growth_rows:
        df_growth = pd.concat(growth_rows, ignore_index=True)
        realisasi_df = pd.concat(
            [realisasi_df, df_growth], ignore_index=True
        )

    realisasi_df = realisasi_df.sort_values(
        ["kdo_bsi", "var_code"]
    ).reset_index(drop=True)

    return realisasi_df