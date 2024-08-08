from typing import Dict, List
import numpy as np
import faiss
from dataset.embedding import get_one_user_embedding, get_all_item_embedding

# 局部敏感哈希（LSH）索引类


class LSH:
    def __init__(self, embeddings: Dict[int, List[float]]) -> None:
        items = embeddings.items()  # 将字典转换为键值对列表
        self.ids = [i[0] for i in items]  # 将键（即items列表中的第0个元素）存储到self.ids
        vectors = [i[1] for i in items]  # 将值（即items列表中的第1个元素）存储到vectors列表
        d = len(vectors[0])  # 计算向量的维度，取vectors列表中第一个元素的长度
        print(f'd={d}')  # 打印维度d
        self.index = faiss.IndexLSH(d, 256)  # 创建一个faiss的LSH索引，维度为d，哈希表大小为256
        array_vec = np.asarray(vectors, dtype=np.float32)  # 将向量列表转换为numpy数组
        self.index.add(array_vec)  # 将数组添加到索引中
        assert (self.index.is_trained)  # 确保索引已经训练完成
        print(f'LSH index added {self.index.ntotal} vectors')  # 打印添加到索引中的向量总数

    def search(self, vec: List[float], n=20) -> List[int]:  # 搜索函数
        # 搜索函数，接收一个向量vec和返回结果数量n

        print(vec)
        # 将输入的向量vec转换为numpy数组，并搜索最相似的n个向量
        D, I = self.index.search(np.asarray([vec], dtype=np.float32), n)

        # I[0] 索引列表，其中包含了最相似的n个向量在原始数据中的索引
        neighbors = I[0]

        # 根据邻居索引列表，从self.ids中获取对应的原始id
        res = [self.ids[i] for i in neighbors]

        print('D:')
        print(D)  # 打印距离信息
        print('I:')
        print(I)  # 打印索引信息
        return res  # 返回搜索结果，即最相似的n个向量对应的原始id列表

def get_item_lsh() -> LSH:
    # 获取所有item的embedding
    item_embeddings = get_all_item_embedding()
    # 创建LSH索引
    lsh = LSH(item_embeddings)
    return lsh
   