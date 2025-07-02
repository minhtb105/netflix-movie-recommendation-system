import logging
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Optional
from sklearn.metrics.pairwise import cosine_similarity
import mlflow
import mlflow.pyfunc as pyfunc
from mlflow.tracking import MlflowClient


class Model(ABC):
    @abstractmethod
    def train(self, df: pd.DataFrame):
        pass

    @abstractmethod
    def recommend(self, user_id: int, N: int = 5):
        pass

class PopularityBased(Model):
    def train(self, df: pd.DataFrame):
        self.rating_mean = df.groupby('item_id').rating.mean().sort_values(ascending=False)
        self.rating_mean.to_pickle('model/popularity_model.pkl')
        mlflow.log_artifact('model/popularity_model.pkl', artifact_path='popularity_model')

    def recommend(self, user_id: int = None, N: int = 5):
        return self.rating_mean.head(N)

class UserBasedCF(Model):
    def train(self, df: pd.DataFrame, target_user_id: Optional[int] = None):
        self.user_item_matrix = df.pivot(index="user_id", columns="item_id", values="rating").fillna(0)
        self.user_sim_matrix = cosine_similarity(self.user_item_matrix)
        self.user_sim_df = pd.DataFrame(self.user_sim_matrix,
                                        index=self.user_item_matrix.index,
                                        columns=self.user_item_matrix.index)
        self.user_item_matrix.to_pickle('model/user_item_matrix.pkl')
        mlflow.log_artifact('model/user_item_matrix.pkl', artifact_path='user_item_matrix')
        self.user_sim_df.to_pickle('model/user_based_cf_model.pkl')
        mlflow.log_artifact('model/user_based_cf_model.pkl', artifact_path='user_based_cf_model')

    def predict(self, user_id: int, item_id: int, k: int = 5):
        if item_id not in self.user_item_matrix.columns or user_id not in self.user_item_matrix.index:
            return np.nan

        users_rated = self.user_item_matrix[self.user_item_matrix[item_id] > 0].index
        if len(users_rated) == 0:
            return np.nan

        sim_scores = self.user_sim_df.loc[user_id, users_rated]
        top_k_users = sim_scores.sort_values(ascending=False).head(k)
        ratings = self.user_item_matrix.loc[top_k_users.index, item_id]

        if ratings.sum() == 0 or top_k_users.sum() == 0:
            return np.nan

        return np.dot(top_k_users, ratings) / np.sum(np.abs(top_k_users))

    def recommend(self, user_id: int, N: int = 5):
        if user_id not in self.user_item_matrix.index:
            return []

        items_rated = self.user_item_matrix.loc[user_id][self.user_item_matrix.loc[user_id] > 0].index
        all_items = self.user_item_matrix.columns
        unrated_items = [item for item in all_items if item not in items_rated]
        predictions = {item: self.predict(user_id, item) for item in unrated_items}
        ranked = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
        return ranked[:N]

class ItemBasedCF(Model):
    def train(self, df: pd.DataFrame):
        self.user_item_matrix = df.pivot_table(index='user_id', columns='item_id', values='rating')
        self.item_user_matrix = self.user_item_matrix.T.fillna(0)
        self.item_sim_matrix = cosine_similarity(self.item_user_matrix)
        self.item_sim_df = pd.DataFrame(self.item_sim_matrix,
                                        index=self.item_user_matrix.index,
                                        columns=self.item_user_matrix.index)
        self.user_item_matrix.to_pickle('model/user_item_matrix.pkl')
        mlflow.log_artifact('model/user_item_matrix.pkl', artifact_path='user_item_matrix')
        self.item_sim_df.to_pickle('model/item_based_cf_model.pkl')
        mlflow.log_artifact('model/item_based_cf_model.pkl', artifact_path='item_based_cf_model')

    def predict(self, user_id: int, item_id: int, k: int = 5):
        if user_id not in self.user_item_matrix.index or item_id not in self.item_sim_df.index:
            return np.nan

        user_ratings = self.user_item_matrix.loc[user_id].dropna()
        if item_id in user_ratings:
            return user_ratings[item_id]

        sim_scores = self.item_sim_df.loc[item_id, user_ratings.index]
        top_k_items = sim_scores.sort_values(ascending=False).head(k)
        top_k_ratings = user_ratings[top_k_items.index]

        if top_k_ratings.empty or top_k_items.sum() == 0:
            return np.nan

        return np.dot(top_k_items, top_k_ratings) / np.sum(np.abs(top_k_items))

    def recommend(self, user_id: int, N: int = 5):
        if user_id not in self.user_item_matrix.index:
            return []

        user_rated = self.user_item_matrix.loc[user_id].dropna().index
        all_items = self.item_user_matrix.index
        unrated_items = [item for item in all_items if item not in user_rated]
        predictions = {item: self.predict(user_id, item) for item in unrated_items}
        ranked = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
        return ranked[:N]

class ContentBasedCF(Model):
    def train(self, df: pd.DataFrame):
        pass

class MatrixFactorization(Model):
    def train(self, df, **kwargs):
        pass