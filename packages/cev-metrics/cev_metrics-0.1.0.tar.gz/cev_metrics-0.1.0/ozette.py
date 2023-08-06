import re

import pandas as pd

NON_ROBUST_LABEL = "0_0_0_0_0"

def parse_label(label: str) -> list[tuple[str, str]]:
    return [
        (inner_label[:-1], inner_label[-1])
        for inner_label in re.split("(\w+[\-|\+])", label)
        if inner_label
    ]

def prepare_ozette(df, robust_only=True):
    # ISMB data
    if "cellType" in df.columns:
        robust = (df["cellType"] != NON_ROBUST_LABEL).to_numpy()
        if robust_only:
            df = df[robust].reset_index(drop=True)
            robust = None

        coords = df[["x", "y"]].to_numpy()
        labels = df["complete_faust_label"].to_numpy()

    else:
        robust = (df["faustLabels"] != NON_ROBUST_LABEL).to_numpy()
        representative_label = df["faustLabels"][robust].iloc[0]

        if robust_only:
            df = df[robust].reset_index(drop=True)
            coords = df[["umapX", "umapY"]].to_numpy()
            labels = df["faustLabels"].to_numpy()
            robust = None
        else:
            coords = df[["umapX", "umapY"]].to_numpy()
            df = df[["faustLabels"]]
            df["label"] = ""
            for marker in parse_label(representative_label):
                name = marker[0]
                marker_annoation = (
                    name + df[f"{name}_faust_annotation"]
                )
                df["label"] += marker_annoation
            labels = df["label"].to_numpy()

    df = pd.DataFrame(coords, columns=["x", "y"])
    df["label"] = pd.Series(labels, dtype="category")
    return df

def load():
    df = prepare_ozette(
        pd.read_parquet("../../OzetteTech/cev/data/TISSUE_138_samples FM96_OM138_035_CD45 live.fcs.parquet.gzip")
    )
    return df
