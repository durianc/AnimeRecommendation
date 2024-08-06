from strategy.recall_strategy import RecallStrategy
import dataset.anime as dataset
from typing import List
class SimpleRecallStrategy(RecallStrategy):
    def __init__(self):
        super().__init__()

    def name(self):
        return 'Simple'

    def recall(self,context,n):
        (anime_df,_) = dataset.load_dataset()
        return anime_df.iloc[:n].index.to_list()