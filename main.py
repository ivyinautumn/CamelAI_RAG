import json
import os
from typing import  Dict
from dotenv import load_dotenv
from camel.models import ModelFactory
from camel.agents import ChatAgent
from camel.messages import BaseMessage
from camel.types import ModelType, ModelPlatformType
from qdrant import QdrantDB
from vector_retriever import VecRetriever

class OnlineLLMRAGSystem:
    """支持多个在线大模型平台的RAG系统"""
    
    def __init__(self, platform: str, **kwargs):
        """
        初始化支持多平台的RAG系统
        
        参数:
            platform: 平台选择 ("openai", "aliyun")
            **kwargs: 平台特定的配置参数
        """
        # 初始化向量数据库
        self.db = QdrantDB(model_name="TencentBAC/Conan-embedding-v1")
        
        # 初始化检索器
        self.retriever = VecRetriever(self.db)
        
        # 根据平台配置LLM
        self.agent = self._init_llm_agent(platform, **kwargs)
        
        print(f"RAG系统初始化完成！使用平台: {platform}")
    
    def _init_llm_agent(self, platform: str, **kwargs):
        """初始化不同平台的LLM代理"""
        
        if platform == "openai":
            return self._init_openai_agent(**kwargs)
        elif platform == "aliyun":
            return self._init_aliyun_agent(**kwargs)
        else:
            raise ValueError(f"不支持的平台: {platform}")
    
    def _init_openai_agent(self, api_key: str, base_url: str):
        """初始化OpenAI代理"""
        
        model = ModelFactory.create(
            model_platform=ModelPlatformType.OPENAI,
            model_type=ModelType.GPT_4O_MINI,
            api_key=api_key,
            url=base_url,
            model_config_dict={"temperature": 0.7, "max_tokens": 1000}
        )
        
        return ChatAgent("你是一个乐于助人的助手。", model=model)
    
    def _init_aliyun_agent(self, api_key: str, base_url: str):
        """初始化阿里云通义千问代理"""
        
        model = ModelFactory.create(
            model_platform=ModelPlatformType.QWEN,
            model_type=ModelType.QWEN_MAX,
            api_key=api_key,
            url=base_url,
            model_config_dict={"temperature": 0.7, "max_tokens": 1000}
        )
        
        return ChatAgent("你是一个乐于助人的助手。", model=model)
    
    def load_data(self, json_file_path: str):
        """从JSON文件加载数据到向量数据库"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"开始加载数据，共{len(data)}条记录...")
            
            for i, item in enumerate(data):
                if item.get('text', '').strip():
                    source_info = f"page_{item.get('page_idx', 'unknown')}"
                    self.db.save_text(
                        text=item['text'],
                        source_file=source_info
                    )
                
                if (i + 1) % 50 == 0:
                    print(f"已处理 {i + 1}/{len(data)} 条记录")
            
            print("数据加载完成！")
            
        except Exception as e:
            print(f"数据加载失败: {e}")
    
    def chat(self, question: str, top_k: int = 5) -> Dict:
        """完整的RAG对话流程"""
        print(f"\n问题: {question}")
        print("=" * 50)
        
        # 检索相关上下文
        print("正在检索相关内容...")
        context_list = self.retriever.search(question, top_k)

        # 显示检索结果
        print(f"\n检索到 {len(context_list)} 条相关内容:")
        for i, item in enumerate(context_list, 1):
            print(f"\n[检索结果 {i}] 来源: {item['file_name']}")
            print(f"相似性得分: {float(item.get('similarity_score', 'Unknown')):.3f}")
            print(f"内容: {item['content'][:200]}{'...' if len(item['content']) > 200 else ''}")
        
        # 生成答案
        print("\n正在生成答案...")
        context_text = "\n\n".join([
            f"[来源: {item['file_name']}]\n{item['content']}"
            for item in context_list
        ])
        
        prompt = f"""基于以下检索到的相关内容，请回答用户的问题。请确保答案准确、相关且基于提供的内容。
                    相关内容：{context_text}
                    用户问题：{question}
                    请提供详细且准确的答案："""
        
        try:
            message = BaseMessage.make_user_message(role_name="用户", content=prompt)
            response = self.agent.step(message)
            answer = response.msg.content
        except Exception as e:
            answer = f"生成答案时出错: {e}"
        
        print(f"\n答案: {answer}")
        print("=" * 50)
        
        return {
            "question": question,
            "answer": answer,
            "retrieved_contexts": context_list
        }

def load_platform_config():
    """从环境变量加载平台配置"""
    
    # 加载 .env 文件
    load_dotenv()
    
    # 构建平台配置字典
    platform_configs = {
        "openai": {
            "platform": "openai",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_BASE_URL")
        },
        "aliyun": {
            "platform": "aliyun", 
            "api_key": os.getenv("ALIYUN_API_KEY"),
            "base_url": os.getenv("ALIYUN_BASE_URL")
        }
    }
    
    return platform_configs

def main():
    """主函数 - 演示不同平台的使用方式"""
    
    # 从环境变量加载配置
    platform_configs = load_platform_config()
    
    # 获取默认平台或使用环境变量中指定的平台
    selected_platform = os.getenv("DEFAULT_PLATFORM", "aliyun")
    
    config = platform_configs[selected_platform]
    
    # 检查配置是否完整
    if not config["api_key"] or not config["base_url"]:
        print(f"{selected_platform} 平台的配置不完整，请检查 .env 文件")
        return
    
    print(f"使用平台: {selected_platform}")
    
    # 创建RAG系统实例
    try:
        rag_system = OnlineLLMRAGSystem(**config)
    except Exception as e:
        print(f"RAG系统初始化失败: {e}")
        return
    
    # 加载数据
    json_file = os.getenv("DATA_FILE", "small_ocr_content_list.json")
    if os.path.exists(json_file):
        rag_system.load_data(json_file)
    else:
        print(f"数据文件 {json_file} 不存在")
        return
    
    # 测试问题
    test_question = "交换价值是什么？"
    rag_system.chat(test_question)

    # 无限问问题
    while True:
        user_question = input("\n请输入您的问题\n（例如“什么是商品的使用价值？”或输入'退出（quit）'结束对话）：")
        if user_question.lower() in ['退出', 'quit']:
            print("感谢使用，再见！")
            break
        rag_system.chat(user_question)

if __name__ == "__main__":
    main()