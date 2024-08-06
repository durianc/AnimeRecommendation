from recall.context import Context
from typing import List
from strategy import RecallStrategy,MostRatedStrategy,HighRatedStrategy,SimilarAnimeStrategy
import concurrent.futures

strategies: List[RecallStrategy] = [
    MostRatedStrategy(),
    HighRatedStrategy()

]


def anime_recall(context: Context, n=20) -> List[int]:
    with concurrent.futures.ThreadPoolExecutor() as executor:
        outputs = executor.map(lambda s: s.recall(context, n), strategies)
        outputs = [aid for l in outputs for aid in l]
        outputs = list(dict.fromkeys(outputs))

        return outputs


def similar_animes(context: Context, n=20) -> List[int]:
    stra = SimilarAnimeStrategy()
    return stra.recall(context, n)
