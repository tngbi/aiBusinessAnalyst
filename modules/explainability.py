
import shap
import xgboost as xgb
import pandas as pd
from utils.logger import logger


def compute_feature_importance(df, target_col="Revenue"):
    """Train XGBoost on numeric features and return SHAP-based importances."""
    if target_col not in df.columns:
        logger.warning(f"Target column '{target_col}' not found — skipping explainability")
        return None, None

    # Select numeric features only (exclude the target)
    numeric_df = df.select_dtypes(include=["number"]).drop(columns=[target_col], errors="ignore")
    if numeric_df.empty:
        logger.warning("No numeric features available for explainability")
        return None, None

    X = numeric_df.fillna(0)
    y = df[target_col].fillna(0)

    model = xgb.XGBRegressor(n_estimators=100, max_depth=4, random_state=42)
    model.fit(X, y)

    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)

    # Build a tidy summary DataFrame
    importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Mean |SHAP|": shap_values.abs.mean(0).values,
    }).sort_values("Mean |SHAP|", ascending=False).reset_index(drop=True)

    logger.info(f"Computed SHAP importances for {len(X.columns)} features")
    return importance_df, shap_values
