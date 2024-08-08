from strategy.recall_strategy import RecallStrategy
from strategy.similar_strategy import SimilarAnimeStrategy
from strategy.simple_strategy import SimpleRecallStrategy
from strategy.most_rated_strategy import MostRatedStrategy
from strategy.high_rated_strategy import HighRatedStrategy
from strategy.user_embedding_strategy import UserEmbeddingStrategy
__all__ = [
    RecallStrategy,
    UserEmbeddingStrategy,
    SimpleRecallStrategy,
    SimilarAnimeStrategy,
    MostRatedStrategy,
    HighRatedStrategy
]
