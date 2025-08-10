import logging
from src.model_dev import Model
from src.evaluation import (
    RMSE, MSE, Precision, Recall, F1Score,
    PrecisionAtK, RecallAtK, F1AtK, MAPAtK, NDCGAtK, MRR
)
import mlflow


def evaluate_model(model: Model, X_test, y_test, k: int = 10) -> None:
    """
    Evaluates the model on the ingested data
    Args:
        df: the ingested data 
    """
    try:
        y_pred = model.predict(X_test)
        
        # Point-wise metrics
        rmse = RMSE()
        rmse_score = rmse.calculate_scores(y_test, y_pred)
        mlflow.log_metric("rmse", rmse_score)

        mse = MSE()
        mse_score = mse.calculate_scores(y_test, y_pred)
        mlflow.log_metric("mse", mse_score)

        precision = Precision()
        precision_score = precision.calculate_scores(y_test, y_pred)
        mlflow.log_metric("precision", precision_score)
        
        recall = Recall()
        recall_score = recall.calculate_scores(y_test, y_pred)
        mlflow.log_metric("recall", recall_score)
        
        f1_score = F1Score()
        f1_score_value = f1_score.calculate_scores(y_test, y_pred)
        mlflow.log_metric("f1_score", f1_score_value)
        
        # Ranking-based metrics 
        mlflow.log_metric(f"precision_at_{k}", PrecisionAtK(k).calculate_scores(y_test[0], y_pred[0]))
        mlflow.log_metric(f"recall_at_{k}", RecallAtK(k).calculate_scores(y_test[0], y_pred[0]))
        mlflow.log_metric(f"f1_at_{k}", F1AtK(k).calculate_scores(y_test[0], y_pred[0]))
        mlflow.log_metric(f"map_at_{k}", MAPAtK(k).calculate_scores(y_test, y_pred))
        mlflow.log_metric(f"ndcg_at_{k}", NDCGAtK(k).calculate_scores(y_test[0], y_pred[0]))
        mlflow.log_metric("mrr", MRR().calculate_scores(y_test, y_pred))
    except Exception as e:
        logging.error(f"Error while evaluating model: {e}")
        raise e
    