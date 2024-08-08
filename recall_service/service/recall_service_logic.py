from recall.context import Context
from typing import List
import time
import concurrent.futures

from strategy import RecallStrategy, MostRatedStrategy, HighRatedStrategy, UserEmbeddingStrategy, SimilarAnimeStrategy
from model.lsh import get_item_lsh
from dataset.embedding import get_one_item_embedding
strategies: List[RecallStrategy] = [
    UserEmbeddingStrategy(),
    MostRatedStrategy(),
    HighRatedStrategy()

]


def anime_recall(context: Context, n=20) -> List[int]:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        outputs = executor.map(lambda s: s.recall(context, n), strategies)
        outputs = [aid for l in outputs for aid in l]
        outputs = list(dict.fromkeys(outputs))
        print(f'Got {len(outputs)} recommendations')
        
        return outputs


def similar_animes(context: Context, n=20) -> List[int]:
    lsh = get_item_lsh()
    target_item_emb = get_one_item_embedding(context.anime_id)
    return lsh.search(target_item_emb, n)


def run_strategy(strategy: RecallStrategy, context: Context, n):
    start_time = time.time()
    res = strategy.recall(context, n)
    elapsed_time = time.time()-start_time
    print(f'Strategy {strategy} took {elapsed_time} seconds')

    return res
