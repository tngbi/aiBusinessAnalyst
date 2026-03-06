
import shap
import xgboost as xgb

def compute_feature_importance(X,y):

    model = xgb.XGBRegressor()
    model.fit(X,y)

    explainer = shap.Explainer(model)

    shap_values = explainer(X)

    return shap_values
