"""MCP Agent服务 - 封装高德地图MCP工具的LangChain Agent"""

from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient

from ..config import get_settings

# 全局实例
_mcp_client = None
_mcp_agent = None
tools = None

async def init_mcp_agent():
    """初始化MCP Agent（应用启动时调用）"""
    global _mcp_client, _mcp_agent, tools

    if _mcp_agent is not None:
        return

    settings = get_settings()

    if not settings.amap_api_key:
        raise ValueError("高德地图API Key未配置,请在.env文件中设置AMAP_API_KEY")

    # 创建MCP客户端
    _mcp_client = MultiServerMCPClient({
        "amap": {
            "transport": "sse",
            "url": f"https://mcp.amap.com/sse?key={settings.amap_api_key}",

        }
    })

    """
                "tools": [
                "maps_text_search", 
                "maps_weather", 
                "maps_direction_walking_by_address",
                "maps_direction_driving_by_address",
                "maps_direction_transit_integrated_by_address"
                ],
    """

    # 获取MCP工具
    tools = await _mcp_client.get_tools()

    # 创建LangChain Agent
    model = init_chat_model(
        model_provider="openai",
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        base_url=settings.openai_base_url,
    )

    _mcp_agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="你是一个地理信息服务助手，可以使用高德地图工具查询POI（兴趣点）、天气、路线规划、地理编码等。请根据用户需求调用相应工具完成任务。",
        checkpointer=InMemorySaver(),
    )

    print(f"✅ MCP Agent初始化成功, 工具数量: {len(tools)}")


def get_mcp_agent():
    """获取MCP Agent实例"""
    if _mcp_agent is None:
        raise RuntimeError("MCP Agent未初始化,请先调用 init_mcp_agent()")
    return _mcp_agent


async def query_mcp_agent(prompt: str) -> str:
    """查询MCP Agent"""
    agent = get_mcp_agent()
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": prompt}]},
        config={"configurable": {"thread_id": "mcp_agent"}},
    )
    return result["messages"][-1].content

def get_mcp_tools():
    """获取MCP Agent所得到的工具"""
    if tools is None:
        raise RuntimeError("MCP Agent未初始化,请先调用 init_mcp_agent()来得到工具信息")
    return tools