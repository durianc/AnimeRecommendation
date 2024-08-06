from strategy.recall_strategy import RecallStrategy
from recall.context import Context
import dataset.anime as dataset
from typing import List

(anime_df, _) = dataset.load_dataset()
sorted_df = anime_df.sort_index()


class SimilarAnimeStrategy(RecallStrategy):
    def name(self):
        return 'Similar Anime'

    def recall(self, context: Context, n=20) -> List[int]:
        anime_iloc = sorted_df.index.get_loc(context.anime_id)
        from_index = anime_iloc
        if from_index + n > len(sorted_df):
            from_index = len(sorted_df) - n

        return sorted_df.iloc[from_index:from_index + n].index.to_list()
