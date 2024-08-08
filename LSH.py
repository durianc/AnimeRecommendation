import numpy as np
import faiss

# 假设我们有10个item，每个item用5维向量表示
np.random.seed(42)
num_items = 10
embedding_dim = 5
items = np.random.random((num_items, embedding_dim)).astype('float32')

# 创建LSH索引
n_bits = 2 * embedding_dim  # LSH bits数量，通常为维度的2倍
index = faiss.IndexLSH(embedding_dim, n_bits)

# 添加item到索引
index.add(items)

# 查询向量，例如查询第一个item的最近邻
query_index = 0
query_vector = items[query_index].reshape(1, -1)

# 执行检索
k = 3  # 找出最近的3个邻居
distances, indices = index.search(query_vector, k)

print(f"Query item embedding: {items[query_index]}")
print("Nearest neighbors indices:", indices[0])
print("Nearest neighbors distances:", distances[0])

# 输出最近邻的信息
for i in range(k):
    print(f"Neighbor {i+1}: Index={indices[0][i]}, Distance={distances[0][i]}, Embedding={items[indices[0][i]]}")
