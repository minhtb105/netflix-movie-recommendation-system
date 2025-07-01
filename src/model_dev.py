import logging
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Optional
from sklearn.metrics.pairwise import cosine_similarity


class Model(ABC):
    @abstractmethod
    def train(self, X_train: pd.DataFrame, y_train: Optional[pd.DataFrame] = None):
        pass


class PopularityBased(Model):
    def train(self, X_train: pd.DataFrame, y_train: pd.DataFrame):
        df = pd.concat([X_train[['user_id', 'item_id']], y_train['rating']], axis=1)
        rating_mean = df.groupby('item_id').rating.mean().sort_values(ascending=False)
        return rating_mean.head(10)


class UserBasedCF(Model):
    def train(self, df: pd.DataFrame, target_user_id: Optional[int] = None):
        self.user_item_matrix = df.pivot(index="user_id", columns="item_id", values="rating").fillna(0)
        self.user_sim_matrix = cosine_similarity(self.user_item_matrix)
        self.user_sim_df = pd.DataFrame(self.user_sim_matrix,
                                        index=self.user_item_matrix.index,
                                        columns=self.user_item_matrix.index)

    def predict(self, user_id: int, item_id: int, k: int = 5):
        if item_id not in self.user_item_matrix.columns:
            return np.nan

        if user_id not in self.user_item_matrix.index:
            return np.nan

        users_rated = self.user_item_matrix[self.user_item_matrix[item_id] > 0].index
        if len(users_rated) == 0:
            return np.nan

        sim_scores = self.user_sim_df.loc[user_id, users_rated]
        top_k_users = sim_scores.sort_values(ascending=False).head(k)
        ratings = self.user_item_matrix.loc[top_k_users.index, item_id]

        if ratings.sum() == 0 or top_k_users.sum() == 0:
            return np.nan

        pred = np.dot(top_k_users, ratings) / np.sum(np.abs(top_k_users))
        return pred


class ItemBasedCF(Model):
    def train(self, df_train: pd.DataFrame):
        self.user_item_matrix = df_train.pivot_table(index='user_id', columns='item_id', values='rating')
        self.item_user_matrix = self.user_item_matrix.T.fillna(0)
        self.item_sim_matrix = cosine_similarity(self.item_user_matrix)
        self.item_sim_df = pd.DataFrame(self.item_sim_matrix,
                                        index=self.item_user_matrix.index,
                                        columns=self.item_user_matrix.index)

    def predict(self, user_id: int, item_id: int, k: int = 5):
        if user_id not in self.user_item_matrix.index:
            return np.nan

        if item_id not in self.item_sim_df.index:
            return np.nan

        user_ratings = self.user_item_matrix.loc[user_id].dropna()
        if item_id in user_ratings:
            return user_ratings[item_id]

        sim_scores = self.item_sim_df.loc[item_id, user_ratings.index]
        top_k_items = sim_scores.sort_values(ascending=False).head(k)
        top_k_ratings = user_ratings[top_k_items.index]

        if top_k_ratings.empty or top_k_items.sum() == 0:
            return np.nan

        predicted = np.dot(top_k_items, top_k_ratings) / np.sum(np.abs(top_k_items))
        return predicted

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
    def train(self, X_train, y_train, **kwargs):
        pass
