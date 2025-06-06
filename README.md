# 智能RAG对话系统

基于CAMEL-AI框架实现的智能RAG对话系统，支持向量数据库检索和智能问答。

## 项目结构

```
├── small_ocr_content_list.json    # 数据文件
├── qdrant.py                      # Qdrant向量数据库操作
├── vector_retriever.py            # 向量检索器
├── main.py                        # 命令行版本主程序
├── app.py                         # Streamlit Web界面
├── requirements.txt               # 依赖包列表
└── README.md                      # 本文件
```

## 环境要求

- Python 3.11+
- CAMEL-AI框架
- Qdrant向量数据库
- 其他依赖包（见requirements.txt）

## 安装步骤

### 1. 创建虚拟环境
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 环境变量配置
在.env.example文件中配置个人llm模型api_key、base_url等信息，默认使用阿里云百炼平台。
然后文件名后缀改成.env。

## 快速开始

### 方式1：命令行版本
```bash
python main.py
```

### 方式2：Web界面版本
```bash
streamlit run app.py
```

## 功能特性

### 核心功能
- ✅ 向量数据库集成（Qdrant）
- ✅ 文本向量化存储
- ✅ 语义检索功能
- ✅ RAG问答流程
- ✅ 智能答案生成

### 界面选项
- 🖥️ 命令行交互界面
- 🌐 Streamlit Web界面
- 📊 检索结果可视化
- 📚 来源信息展示

### 技术栈
- **框架**: CAMEL-AI
- **向量数据库**: Qdrant
- **向量模型**: TencentBAC/Conan-embedding-v1
- **LLM**: gpt-4o-mini或qwen-max（可配置）
- **Web框架**: Streamlit
- **语言**: Python 3.11

## 使用说明

### 测试问题示例
系统已内置测试问题："交换价值是什么？"

期望检索到的内容：
> "交换价值首先表现为量的关系，表现为不同种使用价值彼此相交换的比例(6)，即随着时间和地点的不同而不断改变的关系。因此，交换价值好象是一种任意的、纯粹相对的东西；商品固有的、内在的交换价值似乎是经院哲学家所说的形容语的矛盾①。(7)现在我们进一步考察这个问题。"

示例答案：交换价值首先表现为量的关系，表现为不同种使用价值彼此相交换的比例，即随着时间和地
点的不同而不断改变的关系。

### RAG流程说明
1. **问题理解**: 接收用户输入的自然语言问题
2. **向量检索**: 将问题向量化，在数据库中检索相关文本片段
3. **上下文整合**: 整合检索到的Top-K个相关片段
4. **答案生成**: 基于检索内容使用LLM生成准确答案
5. **结果展示**: 显示答案和相关来源信息

### 自定义配置
在代码中可以调整以下参数：
- `top_k`: 检索结果数量（默认5）
- `temperature`: LLM生成温度（默认0.7）
- `max_tokens`: 最大生成长度（默认1000）

## 依赖包列表

创建 `requirements.txt` 文件：
```
camel-ai[all]>=0.1.0
qdrant-client>=1.6.0
sentence-transformers>=2.2.0
streamlit>=1.28.0
numpy>=1.24.0
torch>=2.0.0
transformers>=4.30.0
```

## 故障排除

### 常见问题

1. **模型下载慢**
   - 使用国内镜像源
   - 或手动下载模型到本地

2. **内存不足**
   - 减少batch_size
   - 使用更小的embedding模型

3. **API密钥错误**
   - 检查OPENAI_API_KEY环境变量
   - 确认API密钥有效性

4. **数据加载失败**
   - 检查JSON文件路径和格式
   - 确认文件编码为UTF-8

### 性能优化建议
- 使用GPU加速向量计算
- 实施向量索引优化
- 缓存常用查询结果
- 批量处理文本向量化

## 项目演示

### 命令行演示
```bash
$ python main.py

RAG系统初始化完成！
开始加载数据，共5条记录...
数据加载完成！

=== 测试指定问题 ===

问题: 交换价值是什么？
==================================================
正在检索相关内容...

检索到 3 条相关内容:

[检索结果 1] 来源: page_0
内容: 交换价值首先表现为量的关系，表现为不同种使用价值彼此相交换的比例(6)，即随着时间和地点的不同而不断改变的关系...

[检索结果 2] 来源: page_1  
内容: 某种特殊的商品，例如一夸特小麦，按各种极不相同的比例同别的商品交换...

正在生成答案...

答案: 根据检索到的内容，交换价值首先表现为量的关系，具体表现为不同种使用价值彼此相交换的比例。这种比例关系会随着时间和地点的不同而不断改变，因此交换价值看起来是一种相对的东西...
==================================================

=== 智能RAG对话系统 ===
输入问题开始对话，输入 'quit' 退出
========================================

请输入您的问题: 使用价值是什么？
```

### Web界面特色功能
- 🎯 实时检索结果展示
- 📊 Top-K检索片段可视化  
- 🔄 交互式参数调整
- 📱 响应式设计适配移动端
- 💾 会话历史记录
- 🎨 美观的UI界面

## 扩展功能建议

### 高级特性
1. **多轮对话支持**
   - 对话历史管理
   - 上下文连续性

2. **文档格式支持**
   - PDF文档解析
   - Word文档处理
   - 网页内容抓取

3. **检索优化**
   - 混合检索策略
   - 重排序机制
   - 查询扩展

4. **答案质量提升**
   - 事实性验证
   - 答案置信度评分
   - 多候选答案生成

### 部署选项
- Docker容器化部署
- 云平台一键部署
- API服务封装
- 微服务架构

## 开发者指南

### 代码结构说明
```python
# qdrant.py - 向量数据库核心功能
class QdrantDB:
    def __init__()           # 初始化数据库连接
    def save_text()          # 保存文本到向量库
    
# vector_retriever.py - 检索功能
class VecRetriever:
    def __init__()           # 初始化检索器
    def search()             # 语义搜索

# main.py - 主程序逻辑  
class IntelligentRAGSystem:
    def load_data()          # 数据加载
    def retrieve_context()   # 上下文检索
    def generate_answer()    # 答案生成
    def chat()              # 完整对话流程
```

### 自定义开发
1. **更换向量模型**
```python
# 修改QdrantDB初始化参数
db = QdrantDB(model_name="your-embedding-model")
```

2. **更换LLM模型**
```python
# 修改ChatAgent配置
agent = ChatAgent(
    model_type=ModelType.GPT_4,  # 或其他支持的模型
    model_config=config
)
```

3. **添加新的数据源**
```python
# 扩展load_data方法支持其他格式
def load_pdf_data(self, pdf_path):
    # PDF解析逻辑
    pass
```

## 许可证
本项目遵循MIT许可证，详见LICENSE文件。

## 贡献指南
欢迎提交Issue和Pull Request来改进项目！

## 联系方式
如有问题请在GitHub Issues中提出。

---
*基于CAMEL-AI框架开发的智能RAG对话系统*