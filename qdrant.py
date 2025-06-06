import os
from camel.storages import QdrantStorage
from camel.embeddings import SentenceTransformerEncoder
from camel.storages import VectorRecord

class QdrantDB:
    """简单的Qdrant向量数据库操作类"""
    
    def __init__(self, model_name: str = "TencentBAC/Conan-embedding-v1",
                 collection_name: str = "my_rag_collection"):
        """
        初始化Qdrant数据库
        
        任务：
        1. 设置数据存储路径
        2. 初始化embedding模型
        3. 创建QdrantStorage实例
        
        参数:
            model_name: huggingface模型名称
        """
        # 设置rootpath（数据存储根目录）
        self.rootpath = os.path.dirname(__file__)
        
        # 初始化SentenceTransformerEncoder
        self.embedding_instance = SentenceTransformerEncoder(model_name=model_name)
        
        # 获取向量维度
        vector_dim = len(self.embedding_instance.embed_list(["test"])[0])
        
        # 初始化QdrantStorage
        self.storage_instance = QdrantStorage(
            vector_dim=vector_dim,
            path=os.path.join(self.rootpath, "qdrant_db"),
            collection_name=collection_name
        )
        
    def save_text(self, text: str, source_file: str = "unknown"):
        """
        保存单个文本到数据库
        
        任务：
        1. 将文本转换为向量
        2. 创建VectorRecord
        3. 保存到数据库
        
        参数:
            text: 要保存的文本
            source_file: 文本来源文件名
        """
        # 使用embedding_instance将文本转换为向量
        embedding_vector = self.embedding_instance.embed_list([text])[0]
        
        # 创建payload字典，包含text和source_file信息
        payload = {
            "text": text,
            "content path": source_file
        }
        
        # 创建VectorRecord对象
        record = VectorRecord(
            vector=embedding_vector,
            payload=payload
        )
        
        # 使用storage_instance.add()保存记录
        self.storage_instance.add([record])

# 使用示例：
"""
# 1. 创建数据库实例
db = QdrantDB()

# 2. 保存文本
db.save_text("这是第一段文本", "文档1.txt")
db.save_text("这是第二段文本", "文档2.txt")

print("文本保存完成！")
"""

# 实习生任务：
# 完成上述TODO部分，实现一个能够将文本保存到Qdrant向量数据库的功能