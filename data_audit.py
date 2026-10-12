import pandas as pd

PLACEHOLDERS = {"", "na", "n/a", "nan", "none", "null", "unknown", "?", "-", "--", "missing"}


def dataset_summary(df):
    """Table-level checks."""
    dup = df.astype(str).duplicated()
    return pd.Series({
        "rows": len(df),
        "columns": df.shape[1],
        "duplicate_rows": int(dup.sum()),
        "rows_with_any_missing": int(df.isna().any(axis=1).sum()),
        "fully_empty_columns": int(df.isna().all().sum()),
    })


def audit_columns(df):
    """One row per column: basic quality metrics plus a short 'flags' hint."""
    rows = []
    for col in df.columns:
        s = df[col]
        s = s.astype(str).where(s.notna()) if s.map(lambda v: isinstance(v, (list, dict))).any() else s
        n, nn = len(s), s.notna().sum()
        vc = s.value_counts()
        r = {"column": col, "dtype": str(s.dtype), "missing": n - nn,
             "missing_%": round(100 * (n - nn) / n, 1), "unique": s.nunique(), "duplicated values": s.duplicated().sum()}
        flags = []
        if r["missing_%"] >= 99.9: flags.append("EMPTY")
        elif r["missing_%"] >= 30: flags.append("MOSTLY_MISSING")
        elif r["missing_%"] > 0: flags.append("MISSING")
        if r["unique"] <= 1 and nn: flags.append("CONSTANT")
        if r["unique"] == n: flags.append("ID?")

        rows.append(r)
    return pd.DataFrame(rows).set_index("column")