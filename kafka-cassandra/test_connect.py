from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement

# 配置Cassandra集群的节点和端口
nodes = ['127.0.0.1']  # 你的Cassandra节点地址
port = 9042  # Cassandra默认端口

# 如果Cassandra设置了密码，使用以下方式提供认证信息
auth_provider = PlainTextAuthProvider(username='cassandra', password='cassandra')

# 创建集群实例
try:
    cluster = Cluster(nodes, port=port, auth_provider=auth_provider)
    session = cluster.connect('actions')  # 选择键空间 actions

    # 测试插入数据
    user_id = 2
    anime_id = 102
    happened_at = '2024-08-02 9:00:00'  # 使用合适的时间格式

    insert_statement = SimpleStatement(
        """
        INSERT INTO views (user_id, anime_id, happened_at)
        VALUES (%s, %s, %s)
        """
    )
    session.execute(insert_statement, (user_id, anime_id, happened_at))
    print("Data inserted successfully.")

    # 测试查询数据
    select_statement = SimpleStatement(
        "SELECT * FROM views WHERE user_id = %s AND anime_id = %s"
    )
    rows = session.execute(select_statement, (user_id, anime_id))
    for row in rows:
        print(row)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 清理，关闭集群连接
    cluster.shutdown()