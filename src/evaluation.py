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
        
    def calculate_scores(self, y_true: list, y_pred: list):
        """
        Recall@K: fraction of relevant items covered in top-K recommendations.
        Args:
            y_true: List of ground-truth relevant items
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

class MAPAtK(Evaluation):
    def __init__(self, k: int):
        self.k = k

    def calculate_scores(self, y_true_list: list, y_pred_list: list):
        """
        MAP@K over multiple users
        Args:
            y_true_list: List of sets (ground-truth items for each user)
            y_pred_list: List of lists (predicted items for each user)
        Returns:
            MAP@K score
        """
        try:
            average_precisions = []

            for y_true, y_pred in zip(y_true_list, y_pred_list):
                hits = 0
                precision_sum = 0

                for i, item in enumerate(y_pred[:self.k], start=1):
                    if item in y_true:
                        hits += 1
                        precision_sum += hits / i  # Precision at i

                ap_at_k = precision_sum / min(len(y_true), self.k) if len(y_true) > 0 else 0.0
                average_precisions.append(ap_at_k)

            map_at_k = np.mean(average_precisions)
            logging.info(f'MAP@{self.k}: {map_at_k}')
            return map_at_k

        except Exception as e:
            logging.error(f"Error while calculating MAP@{self.k}: {e}")
            raise e

class NDCGAtK(Evaluation):
    def __init__(self, k: int):
        self.k = k

    def calculate_scores(self, y_true: set, y_pred: list):
        """
        NDCG@K
        Args:
            y_true: Set of relevant items
            y_pred: List of recommended items
        Returns:
            NDCG@K score
        """
        try:
            dcg = 0.0
            for i, item in enumerate(y_pred[:self.k], start=1):
                if item in y_true:
                    dcg += 1 / np.log2(i + 1)

            # Ideal DCG
            ideal_hits = min(len(y_true), self.k)
            idcg = sum(1 / np.log2(i + 1) for i in range(1, ideal_hits + 1))

            ndcg = dcg / idcg if idcg > 0 else 0.0

            logging.info(f'NDCG@{self.k}: {ndcg}')
            return ndcg

        except Exception as e:
            logging.error(f"Error while calculating NDCG@{self.k}: {e}")
            raise e

class MRR(Evaluation):
    def calculate_scores(self, y_true_list: list, y_pred_list: list):
        """
        MRR (Mean Reciprocal Rank)
        Args:
            y_true_list: List of sets (ground-truth items for each user)
            y_pred_list: List of lists (predicted items for each user)
        Returns:
            MRR score
        """
        try:
            reciprocal_ranks = []

            for y_true, y_pred in zip(y_true_list, y_pred_list):
                rank = 0
                for idx, item in enumerate(y_pred, start=1):
                    if item in y_true:
                        rank = idx
                        break

                rr = 1 / rank if rank > 0 else 0.0
                reciprocal_ranks.append(rr)

            mrr = np.mean(reciprocal_ranks)
            logging.info(f'MRR: {mrr}')
            return mrr

        except Exception as e:
            logging.error(f"Error while calculating MRR: {e}")
            raise e
