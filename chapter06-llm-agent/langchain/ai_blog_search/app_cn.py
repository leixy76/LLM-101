"""
AI博客搜索系统 - 基于LangGraph的智能RAG应用

这是一个完整的智能检索增强生成(RAG)系统，使用LangChain和LangGraph构建。
系统能够智能地处理用户查询，自动决定是否需要检索文档、重写查询或直接生成答案。

主要技术栈：
- LangChain: 大语言模型应用开发框架
- LangGraph: 状态图工作流管理
- Qdrant: 向量数据库
- Google Gemini: 嵌入和对话模型
- Streamlit: Web用户界面

作者：AI学习者社区
适用对象：大模型技术初学者
"""

# 导入必要的库和模块
import streamlit as st  # Streamlit用于构建Web界面
from typing import Annotated, Literal, Sequence, TypedDict  # 类型注解
from uuid import uuid4  # 生成唯一标识符
from functools import partial  # 函数式编程工具

# LangChain核心组件
from langchain_core.messages import BaseMessage, HumanMessage  # 消息类型
from langchain_core.output_parsers import StrOutputParser  # 输出解析器
from langchain_core.pydantic_v1 import BaseModel, Field  # 数据模型

# LangChain Google集成
from langchain_google_genai import (
    ChatGoogleGenerativeAI,  # Google对话模型
    GoogleGenerativeAIEmbeddings  # Google嵌入模型
)

# LangChain文档处理
from langchain_community.document_loaders import WebBaseLoader  # 网页内容加载器
from langchain_text_splitters import RecursiveCharacterTextSplitter  # 文档分割器

# LangChain Qdrant集成
from langchain_qdrant import QdrantVectorStore  # Qdrant向量存储
from qdrant_client import QdrantClient  # Qdrant客户端

# LangGraph工作流组件
from langgraph.graph import StateGraph, START, END  # 状态图构建
from langgraph.graph.message import add_messages  # 消息处理
from langgraph.prebuilt import tools_condition, ToolNode  # 预构建工具

# LangChain Hub用于获取预定义提示模板
from langchain import hub

# 设置Streamlit页面配置
st.set_page_config(
    page_title="AI博客智能搜索系统",  # 页面标题
    page_icon="🤖",  # 页面图标
    layout="wide"  # 宽屏布局
)

# 初始化会话状态变量
# Streamlit使用session_state来在页面刷新间保持数据
if 'qdrant_host' not in st.session_state:
    st.session_state.qdrant_host = ""
if 'qdrant_api_key' not in st.session_state:
    st.session_state.qdrant_api_key = ""
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = ""


def set_sidebar():
    """
    设置侧边栏用于API密钥和配置管理
    
    这个函数创建一个侧边栏界面，让用户输入必要的API配置信息：
    - Qdrant数据库主机地址
    - Qdrant API密钥
    - Google Gemini API密钥
    
    所有输入都使用password类型以保护敏感信息
    """
    with st.sidebar:
        st.subheader("🔧 API配置")
        
        # 输入框使用password类型隐藏敏感信息
        qdrant_host = st.text_input(
            "输入Qdrant主机URL:", 
            type="password",
            help="例如: https://your-cluster.qdrant.io"
        )
        qdrant_api_key = st.text_input(
            "输入Qdrant API密钥:", 
            type="password",
            help="从Qdrant控制台获取的API密钥"
        )
        gemini_api_key = st.text_input(
            "输入Gemini API密钥:", 
            type="password",
            help="从Google AI Studio获取的API密钥"
        )

        # 配置完成按钮
        if st.button("✅ 完成配置"):
            if qdrant_host and qdrant_api_key and gemini_api_key:
                # 保存配置到会话状态
                st.session_state.qdrant_host = qdrant_host
                st.session_state.qdrant_api_key = qdrant_api_key
                st.session_state.gemini_api_key = gemini_api_key
                st.success("🎉 API密钥配置成功！")
            else:
                st.warning("⚠️ 请填写所有API配置字段")


def initialize_components():
    """
    初始化需要API密钥的核心组件
    
    这个函数负责初始化整个RAG系统的核心组件：
    1. Google嵌入模型 - 用于将文本转换为向量
    2. Qdrant客户端 - 用于向量数据库操作
    3. 向量存储 - 用于存储和检索文档向量
    
    Returns:
        tuple: (嵌入模型, Qdrant客户端, 向量存储) 或 (None, None, None)
    """
    # 检查是否所有必需的API密钥都已配置
    if not all([
        st.session_state.qdrant_host, 
        st.session_state.qdrant_api_key, 
        st.session_state.gemini_api_key
    ]):
        return None, None, None

    try:
        # 初始化Google嵌入模型
        # embedding-001是Google专门用于文本嵌入的模型
        embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=st.session_state.gemini_api_key
        )

        # 初始化Qdrant客户端
        # Qdrant是一个高性能的向量搜索引擎
        client = QdrantClient(
            st.session_state.qdrant_host,
            api_key=st.session_state.qdrant_api_key
        )

        # 初始化向量存储
        # 这是LangChain对Qdrant的封装，提供了便捷的文档操作接口
        db = QdrantVectorStore(
            client=client,
            collection_name="qdrant_db",  # 集合名称
            embedding=embedding_model     # 嵌入模型
        )

        return embedding_model, client, db
        
    except Exception as e:
        st.error(f"❌ 组件初始化错误: {str(e)}")
        return None, None, None


class AgentState(TypedDict):
    """
    Agent状态定义
    
    这个类定义了在整个LangGraph工作流中传递的状态信息。
    使用TypedDict确保类型安全，Annotated提供额外的元数据。
    
    Attributes:
        messages: 对话消息序列，使用add_messages函数处理消息添加
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]


def grade_documents(state) -> Literal["generate", "rewrite"]:
    """
    文档相关性评分函数
    
    这是RAG系统的核心组件之一，负责评估检索到的文档是否与用户查询相关。
    基于评分结果，系统会决定是生成答案还是重写查询。
    
    工作流程：
    1. 提取用户的原始问题
    2. 获取最后检索到的文档内容
    3. 使用Gemini模型评估相关性
    4. 返回决策结果
    
    Args:
        state: 包含消息历史的状态对象
        
    Returns:
        Literal["generate", "rewrite"]: "generate"表示生成答案，"rewrite"表示重写查询
    """
    print("---执行文档相关性评分---")
    
    # 从状态中提取消息
    messages = state["messages"]
    last_message = messages[-1]  # 获取最后一条消息（检索到的文档）
    question = messages[0].content  # 获取原始用户问题
    docs = last_message.content  # 获取文档内容

    # 定义评分模型的输出格式
    class grade(BaseModel):
        """
        相关性评分的二元分类模型
        
        这个模型确保Gemini的输出格式标准化，只返回'yes'或'no'
        """
        binary_score: str = Field(
            description="相关性评分结果：'yes'表示相关，'no'表示不相关"
        )

    # 初始化带有结构化输出的Gemini模型
    model = ChatGoogleGenerativeAI(
        api_key=st.session_state.gemini_api_key,
        temperature=0,  # 设置为0确保输出一致性
        model="gemini-2.0-flash"
    )
    
    # 绑定输出格式
    llm_with_tool = model.with_structured_output(grade)

    # 构建评分提示
    prompt = f"""
    你是一个文档相关性评估专家。请评估检索到的文档是否与用户问题相关。

    用户问题: {question}
    
    检索到的文档: {docs}
    
    评估标准：
    1. 文档内容是否直接回答了用户的问题？
    2. 文档中是否包含与问题相关的关键信息？
    3. 文档的主题是否与问题的主题一致？
    
    如果文档相关且有用，请返回'yes'；如果不相关或无用，请返回'no'。
    """

    # 执行评分
    res = llm_with_tool.invoke([HumanMessage(content=prompt)])
    
    # 根据评分结果返回下一步动作
    if res.binary_score == "yes":
        print("---文档相关，准备生成答案---")
        return "generate"
    else:
        print("---文档不相关，需要重写查询---")
        return "rewrite"


def agent(state, tools):
    """
    核心Agent决策函数
    
    这是整个系统的"大脑"，负责分析用户查询并决定下一步行动。
    Agent会根据当前状态和可用工具来做出智能决策。
    
    决策逻辑：
    1. 分析用户查询的复杂度和类型
    2. 决定是否需要使用检索工具
    3. 如果查询简单明确，可能直接结束对话
    4. 如果需要更多信息，会调用检索工具
    
    Args:
        state: 当前对话状态
        tools: 可用的工具列表（主要是检索工具）
        
    Returns:
        dict: 包含Agent响应消息的状态更新
    """
    print("---调用Agent进行决策---")
    
    # 获取对话历史
    messages = state["messages"]
    
    # 初始化Gemini对话模型
    # 使用流式输出提升用户体验
    model = ChatGoogleGenerativeAI(
        api_key=st.session_state.gemini_api_key, 
        temperature=0,  # 确保输出一致性
        streaming=True,  # 启用流式输出
        model="gemini-2.0-flash"
    )
    
    # 绑定可用工具
    model = model.bind_tools(tools)
    
    # 调用模型生成响应
    response = model.invoke(messages)
    
    # 返回状态更新（添加Agent的响应到消息列表）
    return {"messages": [response]}


def rewrite(state):
    """
    查询重写函数
    
    当检索到的文档与用户查询不够相关时，这个函数会被调用来重写查询。
    重写的目标是生成一个更精确、更容易检索到相关文档的查询。
    
    重写策略：
    1. 分析原始查询的语义意图
    2. 识别关键概念和实体
    3. 重新组织语言表达
    4. 生成更精确的查询语句
    
    Args:
        state: 包含对话历史的状态
        
    Returns:
        dict: 包含重写后查询的状态更新
    """
    print("---执行查询重写---")
    
    # 提取消息和原始问题
    messages = state["messages"]
    question = messages[0].content

    # 构建重写提示消息
    msg = [
        HumanMessage(
            content=f"""
            请分析以下用户查询，理解其潜在的语义意图和含义。
            
            原始查询:
            ------- 
            {question} 
            -------
            
            请执行以下任务：
            1. 分析查询的核心意图和关键概念
            2. 识别可能影响检索效果的模糊表达
            3. 重新组织语言，使其更加精确和具体
            4. 生成一个改进的查询语句
            
            改进后的查询应该：
            - 更加具体和明确
            - 包含相关的关键词
            - 易于匹配相关文档
            
            请直接提供改进后的查询语句：
            """,
        )
    ]

    # 使用Gemini模型进行查询重写
    model = ChatGoogleGenerativeAI(
        api_key=st.session_state.gemini_api_key, 
        temperature=0, 
        model="gemini-2.0-flash", 
        streaming=True
    )
    
    # 生成重写后的查询
    response = model.invoke(msg)
    
    return {"messages": [response]}


def generate(state):
    """
    答案生成函数
    
    这是RAG流程的最后一步，基于检索到的相关文档生成最终答案。
    使用检索增强生成(RAG)模式，确保答案基于实际文档内容。
    
    RAG生成流程：
    1. 提取用户原始问题
    2. 获取检索到的相关文档
    3. 使用预定义的RAG提示模板
    4. 结合文档内容生成准确答案
    
    Args:
        state: 包含问题和文档的状态
        
    Returns:
        dict: 包含生成答案的状态更新
    """
    print("---生成最终答案---")
    
    # 提取消息、问题和文档
    messages = state["messages"]
    question = messages[0].content  # 原始用户问题
    last_message = messages[-1]     # 最后一条消息（检索到的文档）
    docs = last_message.content     # 文档内容

    # 从LangChain Hub获取预定义的RAG提示模板
    # 这个模板经过优化，能够有效结合问题和文档生成答案
    prompt_template = hub.pull("rlm/rag-prompt")

    # 初始化对话模型
    chat_model = ChatGoogleGenerativeAI(
        api_key=st.session_state.gemini_api_key, 
        model="gemini-2.0-flash", 
        temperature=0,  # 确保答案一致性
        streaming=True  # 流式输出
    )

    # 初始化输出解析器
    # 将模型输出转换为字符串格式
    output_parser = StrOutputParser()
    
    # 构建RAG处理链
    # 提示模板 -> 对话模型 -> 输出解析器
    rag_chain = prompt_template | chat_model | output_parser

    # 执行RAG生成
    # context: 检索到的文档内容
    # question: 用户的原始问题
    response = rag_chain.invoke({"context": docs, "question": question})
    
    return {"messages": [response]}


def get_graph(retriever_tool):
    """
    构建LangGraph工作流图
    
    这个函数创建整个RAG系统的工作流程图，定义了各个组件之间的连接关系。
    工作流图是一个有向图，节点代表处理步骤，边代表数据流向。
    
    工作流程：
    1. 用户查询 -> Agent决策
    2. Agent决策 -> 检索工具 或 直接结束
    3. 检索结果 -> 文档评分
    4. 文档评分 -> 生成答案 或 重写查询
    5. 重写查询 -> 回到Agent决策
    6. 生成答案 -> 结束
    
    Args:
        retriever_tool: 文档检索工具
        
    Returns:
        CompiledGraph: 编译后的工作流图
    """
    # 创建工具列表
    tools = [retriever_tool]
    
    # 定义状态图，使用AgentState作为状态类型
    workflow = StateGraph(AgentState)

    # 添加Agent节点
    # 使用partial函数将tools参数绑定到agent函数
    workflow.add_node("agent", partial(agent, tools=tools))
    
    # 添加检索节点
    # ToolNode是LangGraph预构建的工具执行节点
    retrieve = ToolNode(tools)
    workflow.add_node("retrieve", retrieve)
    
    # 添加查询重写节点
    workflow.add_node("rewrite", rewrite)
    
    # 添加答案生成节点
    workflow.add_node("generate", generate)

    # 定义工作流的起始点
    # 所有对话都从Agent节点开始
    workflow.add_edge(START, "agent")

    # 添加Agent节点的条件边
    # tools_condition是预构建的条件函数，用于判断是否需要调用工具
    workflow.add_conditional_edges(
        "agent",
        tools_condition,  # 条件判断函数
        {
            "tools": "retrieve",  # 如果需要工具，转到检索节点
            END: END,            # 如果不需要工具，直接结束
        },
    )

    # 添加检索节点的条件边
    # 检索完成后，需要评估文档相关性
    workflow.add_conditional_edges(
        "retrieve",
        grade_documents,  # 文档评分函数
        # 根据评分结果决定下一步：
        # "generate": 生成答案
        # "rewrite": 重写查询
    )
    
    # 添加固定边
    workflow.add_edge("generate", END)    # 生成答案后结束
    workflow.add_edge("rewrite", "agent") # 重写查询后回到Agent

    # 编译工作流图
    # 编译过程会验证图的完整性和正确性
    graph = workflow.compile()

    return graph


def generate_message(graph, inputs):
    """
    执行工作流并生成最终消息
    
    这个函数执行整个LangGraph工作流，并提取最终生成的答案。
    它会遍历工作流的所有输出，找到最终的生成结果。
    
    Args:
        graph: 编译后的工作流图
        inputs: 输入数据（包含用户查询）
        
    Returns:
        str: 生成的最终答案
    """
    generated_message = ""

    # 流式执行工作流图
    # graph.stream()会逐步执行工作流的每个节点
    for output in graph.stream(inputs):
        for key, value in output.items():
            # 查找生成节点的输出
            if key == "generate" and isinstance(value, dict):
                # 提取生成的消息
                generated_message = value.get("messages", [""])[0]
    
    return generated_message


def add_documents_to_qdrant(url, db):
    """
    将网页文档添加到Qdrant向量数据库
    
    这个函数实现了完整的文档处理流程：
    1. 从URL加载网页内容
    2. 将长文档分割成小块
    3. 为每个文档块生成唯一ID
    4. 将文档块存储到向量数据库
    
    文档分块的重要性：
    - 提高检索精度：小块更容易匹配特定查询
    - 控制上下文长度：避免超出模型输入限制
    - 提升检索效率：减少无关信息的干扰
    
    Args:
        url (str): 要处理的网页URL
        db: Qdrant向量存储实例
        
    Returns:
        bool: 处理成功返回True，失败返回False
    """
    try:
        # 使用WebBaseLoader加载网页内容
        # WebBaseLoader能够处理各种网页格式，提取主要文本内容
        docs = WebBaseLoader(url).load()
        
        # 初始化文档分割器
        # RecursiveCharacterTextSplitter使用递归方法智能分割文档
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=100,    # 每个块的最大字符数
            chunk_overlap=50   # 块之间的重叠字符数，保持上下文连续性
        )
        
        # 执行文档分割
        doc_chunks = text_splitter.split_documents(docs)
        
        # 为每个文档块生成唯一标识符
        # UUID确保每个文档块都有唯一的ID
        uuids = [str(uuid4()) for _ in range(len(doc_chunks))]
        
        # 将文档块添加到向量数据库
        # 这个过程包括：
        # 1. 使用嵌入模型将文本转换为向量
        # 2. 将向量和元数据存储到Qdrant
        db.add_documents(documents=doc_chunks, ids=uuids)
        
        return True
        
    except Exception as e:
        # 错误处理：显示具体错误信息
        st.error(f"❌ 文档添加错误: {str(e)}")
        return False


def main():
    """
    主函数 - Streamlit应用的入口点
    
    这个函数协调整个应用的用户界面和核心功能：
    1. 设置页面标题和说明
    2. 管理API配置
    3. 初始化核心组件
    4. 处理文档添加
    5. 执行智能问答
    
    用户交互流程：
    1. 配置API密钥
    2. 添加博客URL
    3. 输入问题
    4. 获取智能答案
    """
    # 页面标题和介绍
    st.title("🤖 AI博客智能搜索系统")
    st.markdown("""
    ### 基于LangGraph的智能RAG系统
    
    这是一个智能的博客搜索系统，能够：
    - 📚 **智能文档处理**：自动抓取和分析博客内容
    - 🧠 **智能查询理解**：理解用户意图，自动优化查询
    - 🔍 **精准信息检索**：基于向量相似度的语义搜索
    - 💬 **智能答案生成**：结合检索内容生成准确答案
    
    ---
    """)
    
    # 设置侧边栏配置
    set_sidebar()
    
    # 初始化核心组件
    embedding_model, client, db = initialize_components()
    
    # 检查组件是否成功初始化
    if not all([embedding_model, client, db]):
        st.warning("⚠️ 请先在侧边栏配置所有必需的API密钥")
        st.info("""
        ### 🔧 配置说明：
        
        1. **Qdrant配置**：
           - 注册Qdrant Cloud账户：https://qdrant.tech/
           - 创建集群并获取URL和API密钥
        
        2. **Google Gemini配置**：
           - 访问Google AI Studio：https://aistudio.google.com/
           - 创建API密钥
        
        3. **配置完成后**：
           - 点击"完成配置"按钮
           - 开始使用系统功能
        """)
        return
    
    # 创建检索工具
    # 这是Agent可以调用的工具，用于从向量数据库检索相关文档
    retriever_tool = db.as_retriever().as_tool(
        name="blog_search",
        description="搜索博客内容以回答用户问题。输入应该是一个搜索查询。"
    )
    
    # 构建LangGraph工作流
    graph = get_graph(retriever_tool)
    
    # 文档管理部分
    st.subheader("📄 文档管理")
    
    # 创建两列布局
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # 博客URL输入框
        blog_url = st.text_input(
            "输入博客文章URL:",
            placeholder="https://example.com/blog-post",
            help="输入您想要分析的博客文章链接"
        )
    
    with col2:
        st.write("")  # 添加空白以对齐按钮
        # 添加文档按钮
        if st.button("📥 添加文档", type="primary"):
            if blog_url:
                with st.spinner("正在处理文档..."):
                    # 调用文档添加函数
                    if add_documents_to_qdrant(blog_url, db):
                        st.success("✅ 文档添加成功！现在可以开始提问了。")
                    else:
                        st.error("❌ 文档添加失败，请检查URL是否有效。")
            else:
                st.warning("⚠️ 请先输入博客URL")
    
    # 分隔线
    st.divider()
    
    # 智能问答部分
    st.subheader("💬 智能问答")
    
    # 用户查询输入
    user_query = st.text_input(
        "请输入您的问题:",
        placeholder="例如：这篇文章的主要观点是什么？",
        help="输入关于博客内容的任何问题"
    )
    
    # 问答执行按钮
    if st.button("🚀 开始搜索", type="primary"):
        if user_query:
            # 显示处理状态
            with st.spinner("🤖 AI正在思考中..."):
                try:
                    # 构建输入数据
                    inputs = {"messages": [HumanMessage(content=user_query)]}
                    
                    # 执行LangGraph工作流
                    result = generate_message(graph, inputs)
                    
                    # 显示结果
                    if result:
                        st.subheader("🎯 智能答案")
                        st.write(result)
                        
                        # 添加反馈区域
                        st.divider()
                        st.subheader("📊 反馈")
                        
                        # 创建反馈按钮
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button("👍 答案有帮助"):
                                st.success("感谢您的反馈！")
                        with col2:
                            if st.button("👎 答案需要改进"):
                                st.info("我们会继续改进系统性能")
                        with col3:
                            if st.button("🔄 重新搜索"):
                                st.rerun()
                    else:
                        st.error("❌ 未能生成答案，请尝试重新表述您的问题")
                        
                except Exception as e:
                    st.error(f"❌ 处理过程中出现错误: {str(e)}")
                    st.info("💡 建议：请检查网络连接和API配置")
        else:
            st.warning("⚠️ 请输入您的问题")
    
    # 页面底部信息
    st.divider()
    st.markdown("""
    ### 🔍 系统工作原理
    
    1. **文档处理**：系统自动抓取博客内容并分割成小块
    2. **向量化存储**：使用Google Gemini嵌入模型将文本转换为向量
    3. **智能检索**：基于语义相似度检索相关文档片段
    4. **相关性评估**：AI自动评估检索结果的相关性
    5. **查询优化**：如果结果不相关，自动重写查询
    6. **答案生成**：基于相关文档生成准确、有用的答案
    
    ### 💡 使用技巧
    
    - **具体问题**：提出具体、明确的问题能获得更好的答案
    - **关键词**：在问题中包含相关关键词
    - **上下文**：提供足够的上下文信息
    - **多次尝试**：如果答案不满意，可以尝试重新表述问题
    """)


# 应用程序入口点
if __name__ == "__main__":
    main()