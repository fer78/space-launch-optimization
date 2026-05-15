from pathlib import Path
import pandas as pd


# ==========================================================
# PATHS
# ==========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATASET_PATH = DATA_DIR / "spacex_launch_geo.csv"


# ==========================================================
# LOAD DATASET
# ==========================================================
def load_data():
    """
    Load the main dataset and return it as a pandas DataFrame.
    """
    return pd.read_csv(DATASET_PATH)


# ==========================================================
# HOME KPIs
# ==========================================================
def get_home_kpis():
    """
    Calculate the main KPIs displayed on the home page.
    """
    df = load_data()

    total_launches = len(df)
    success_rate = round(df["class"].mean() * 100, 2)
    launch_sites = df["Launch Site"].nunique()

    # Placeholder value for demonstration purposes.
    best_model_accuracy = 94.2

    return {
        "total_launches": total_launches,
        "success_rate": success_rate,
        "launch_sites": launch_sites,
        "best_model_accuracy": best_model_accuracy,
    }


# ==========================================================
# FORM OPTIONS
# ==========================================================
def get_launch_sites():
    """
    Return the list of available launch sites.
    """
    df = load_data()
    return sorted(df["Launch Site"].dropna().unique().tolist())


def get_orbits():
    """
    Return the list of available orbit types.
    """
    df = load_data()
    return sorted(df["Orbit"].dropna().unique().tolist())


def get_booster_versions():
    """
    Return the list of available booster versions.
    """
    df = load_data()
    return sorted(df["Booster Version"].dropna().unique().tolist())