from pathlib import Path
import joblib
import pandas as pd


# ==========================================================
# PATHS
# ==========================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODELS_DIR / "best_model.pkl"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.pkl"


# ==========================================================
# LOAD ARTIFACTS
# ==========================================================
_model = None
_preprocessor = None


def load_model():
    """
    Load the trained model only once and cache it in memory.
    """
    global _model

    if _model is None:
        _model = joblib.load(MODEL_PATH)

    return _model


def load_preprocessor():
    """
    Load the preprocessing pipeline only once and cache it in memory.
    """
    global _preprocessor

    if _preprocessor is None:
        _preprocessor = joblib.load(PREPROCESSOR_PATH)

    return _preprocessor


# ==========================================================
# PREDICTION
# ==========================================================
def predict_launch_success(
    launch_site,
    payload_mass,
    orbit,
    booster_version
):
    """
    Return the predicted probability of launch success.
    """

    # Create a single-row DataFrame with the user inputs.
    input_df = pd.DataFrame(
        [{
            "Launch Site": launch_site,
            "Payload Mass (kg)": payload_mass,
            "Orbit": orbit,
            "Booster Version": booster_version,
        }]
    )

    # Load artifacts.
    preprocessor = load_preprocessor()
    model = load_model()

    # Transform the input data.
    X = preprocessor.transform(input_df)

    # Predict probability of the positive class (success = 1).
    probability = model.predict_proba(X)[0][1]

    return probability


# ==========================================================
# BUSINESS RECOMMENDATION
# ==========================================================
def generate_recommendation(probability_percent):
    """
    Generate an executive recommendation based on the predicted probability.
    """

    if probability_percent >= 85:
        return (
            "High probability of mission success. "
            "Operational conditions appear favorable."
        )

    elif probability_percent >= 70:
        return (
            "Moderate to high probability of success. "
            "Proceed with standard risk monitoring."
        )

    elif probability_percent >= 50:
        return (
            "Moderate probability of success. "
            "Review mission parameters before approval."
        )

    else:
        return (
            "Low probability of success. "
            "Further analysis is recommended before launch."
        )