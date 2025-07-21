import logging
import numpy as np
from abc import ABC, abstractmethod

class Evaluation(ABC):
    @abstractmethod
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Calculate the scores for the model
        Args:
            y_true: True labels
            y_pred: predicted labels
        Returns:
            None
        """
        pass
    
class MSE(Evaluation):
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Calculate Mean Squared Error
        Args:
            y_true: True labels
            y_pred: predicted labels
        Returns:
            MSE score
        """
        try:
            mse = np.mean((y_true - y_pred) ** 2)
            logging.info(f'Mean Squared Error: {mse}')
            
            return mse
        except Exception as e:
            logging.error(f"Error while calculating MSE: {e}")
            raise e 
            
class RMSE(Evaluation):
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Calculate Root Mean Squared Error
        Args:
            y_true: True labels
            y_pred: predicted labels
        Returns:
            RMSE score
        """
        try:
            mse = np.mean((y_true - y_pred) ** 2)
            rmse = np.sqrt(mse)
            logging.info(f'Root Mean Squared Error: {rmse}')
            
            return rmse
        except Exception as e:
            logging.error(f"Error while calculating RMSE: {e}")
            raise e
    
class Precision(Evaluation):
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Calculate Precision
        Args:
            y_true: True labels
            y_pred: predicted labels
        Returns:
            Precision score
        """
        try:
            true_positive = np.sum((y_true == 1) & (y_pred == 1))
            false_positive = np.sum((y_true == 0) & (y_pred == 1))
            precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0.0
            
            logging.info(f'Precision: {precision}')
            
            return precision
        except Exception as e:
            logging.error(f"Error while calculating Precision: {e}")
            raise e
        
class Recall(Evaluation):
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Calculate Recall
        Args:
            y_true: True labels
            y_pred: predicted labels
        Returns:
            Recall score
        """
        try:
            true_positive = np.sum((y_true == 1) & (y_pred == 1))
            false_negative = np.sum((y_true == 1) & (y_pred == 0))
            recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0.0
            
            logging.info(f'Recall: {recall}')
            
            return recall
        except Exception as e:
            logging.error(f"Error while calculating Recall: {e}")
            raise e
        
class F1Score(Evaluation):
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Calculate F1 Score
        Args:
            y_true: True labels
            y_pred: predicted labels
        Returns:
            F1 Score
        """
        try:
            precision = Precision().calculate_scores(y_true, y_pred)
            recall = Recall().calculate_scores(y_true, y_pred)
            f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            
            logging.info(f'F1 Score: {f1_score}')
            
            return f1_score
        except Exception as e:
            logging.error(f"Error while calculating F1 Score: {e}")
            raise e
        
class PrecisionAtK(Evaluation):
    def __init__(self, k: int):
        self.k = k
        
    def calculate_scores(self, y_true: set, y_pred: list):
        """
        Precision@K: fraction of recommended items in top-K that are relevant.
        Args:
            y_true: Set of ground-truth relevant items
            y_pred: List of recommended items (ordered)
        Returns:
            Precision@K score
        """
        try:
            top_k_preds = y_pred[:self.k]
            relevant_in_top_k = sum(1 for item in top_k_preds if item in y_true)
            precision_at_k = relevant_in_top_k / self.k
            
            logging.info(f'Precision@{self.k}: {precision_at_k}')
            return precision_at_k
        except Exception as e:
            logging.error(f"Error while calculating Precision@{self.k}: {e}")
            raise e


class RecallAtK(Evaluation):
    def __init__(self, k: int):
        self.k = k
        
    def calculate_scores(self, y_true: set, y_pred: list):
        """
        Recall@K: fraction of relevant items covered in top-K recommendations.
        Args:
            y_true: Set of ground-truth relevant items
            y_pred: List of recommended items (ordered)
        Returns:
            Recall@K score
        """
        try:
            top_k_preds = y_pred[:self.k]
            relevant_in_top_k = sum(1 for item in top_k_preds if item in y_true)
            recall_at_k = relevant_in_top_k / len(y_true) if len(y_true) > 0 else 0.0
            
            logging.info(f'Recall@{self.k}: {recall_at_k}')
            return recall_at_k
        except Exception as e:
            logging.error(f"Error while calculating Recall@{self.k}: {e}")
            raise e
        
class F1AtK(Evaluation):
    def __init__(self, k: int):
        self.k = k

    def calculate_scores(self, y_true: set, y_pred: list):
        """
        F1@K: harmonic mean of Precision@K and Recall@K
        Args:
            y_true: Set of ground-truth relevant items
            y_pred: List of recommended items (ordered)
        Returns:
            F1@K score
        """
        try:
            top_k_preds = y_pred[:self.k]
            relevant_in_top_k = sum(1 for item in top_k_preds if item in y_true)

            precision_at_k = relevant_in_top_k / self.k
            recall_at_k = relevant_in_top_k / len(y_true) if len(y_true) > 0 else 0.0

            if precision_at_k + recall_at_k > 0:
                f1_at_k = 2 * (precision_at_k * recall_at_k) / (precision_at_k + recall_at_k)
            else:
                f1_at_k = 0.0

            logging.info(f'F1@{self.k}: {f1_at_k}')
            return f1_at_k

        except Exception as e:
            logging.error(f"Error while calculating F1@{self.k}: {e}")
            raise e
