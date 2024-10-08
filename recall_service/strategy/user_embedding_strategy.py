from typing import List
from recall.context import Context
from strategy import RecallStrategy
from model.lsh import get_item_lsh
from dataset.embedding import get_one_user_embedding,get_all_item_embedding

class UserEmbeddingStrategy(RecallStrategy):
    def __init__(self) -> None:
        super().__init__()
        self.lsh=get_item_lsh()
        
    def name(self):
        return 'UserEmbedding'
    
    def recall(self, context: Context, n=20) -> List[int]:
        if context.user_id is None:
            return []
        
        user_id=context.user_id
        user_emb=get_one_user_embedding(user_id)
        
        if user_emb is None:
            return []
        
        return self.lsh.search(user_emb, n)
