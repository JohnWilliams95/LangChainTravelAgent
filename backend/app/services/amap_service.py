"""高德地图MCP服务封装"""

from typing import List, Dict, Any, Optional
from ..config import get_settings
from ..models.schemas import Location, POIInfo, WeatherInfo
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from ..tools.mcp_agent import get_mcp_tools
from ..tools.mcp_agent import get_mcp_agent, query_mcp_agent




class AmapService:
    """高德地图服务封装类"""

    def __init__(self):
        """初始化服务"""
        # self.mcp_tool = get_amap_mcp_tool

    async def search_poi(self, keywords: str, city: str, citylimit: bool = True):
        """
        搜索POI
        
        Args:
            keywords: 搜索关键词
            city: 城市
            citylimit: 是否限制在城市范围内
            
        Returns:
            POI信息列表
        """
        try:
            response = await query_mcp_agent(
                prompt=f"请使用高德地图maps_text_search工具搜索POI,关键词:{keywords}，城市：{city}, citylimit: {citylimit}"
            )
            
            return response
            
        except Exception as e:
            print(f"❌ POI搜索失败: {str(e)}")
            return []
    
    async def get_weather(self, city: str):
        """
        查询天气
        
        Args:
            city: 城市名称
            
        Returns:
            天气信息列表
        """
        try:
            response = await query_mcp_agent(
                prompt=f"请使用高德地图maps_weather工具查询{city}的天气信息"
            )
            return response
            
        except Exception as e:
            print(f"❌ 天气查询失败: {str(e)}")
            return []
    
    async def plan_route(
        self,
        origin_address: str,
        destination_address: str,
        origin_city: Optional[str] = None,
        destination_city: Optional[str] = None,
        route_type: str = "walking"
    ) -> Dict[str, Any]:
        """
        规划路线
        
        Args:
            origin_address: 起点地址
            destination_address: 终点地址
            origin_city: 起点城市
            destination_city: 终点城市
            route_type: 路线类型 (walking/driving/transit)
            
        Returns:
            路线信息
        """
        try:
            # 根据路线类型选择工具
            tool_map = {
                "walking": "maps_direction_walking_by_address",
                "driving": "maps_direction_driving_by_address",
                "transit": "maps_direction_transit_integrated_by_address"
            }
            
            tool_name = tool_map.get(route_type, "maps_direction_walking_by_address")
            
            # 构建参数
            arguments = {
                "origin_address": origin_address,
                "destination_address": destination_address
            }
            
            # 公共交通需要城市参数
            if route_type == "transit":
                if origin_city:
                    arguments["origin_city"] = origin_city
                if destination_city:
                    arguments["destination_city"] = destination_city
            else:
                # 其他路线类型也可以提供城市参数提高准确性
                if origin_city:
                    arguments["origin_city"] = origin_city
                if destination_city:
                    arguments["destination_city"] = destination_city
            
            # 调用MCP工具
            response = await query_mcp_agent(
                prompt = (
                    f"请使用高德地图{tool_name}工具规划路线，"
                    f"起点：{arguments['origin_address']}，"
                    f"终点：{arguments['destination_address']}"
                )
            )
            return response
            
        except Exception as e:
            print(f"❌ 路线规划失败: {str(e)}")
            return {}
    
    async def geocode(self, address: str, city: Optional[str] = None) -> Optional[Location]:
        """
        地理编码(地址转坐标)

        Args:
            address: 地址
            city: 城市

        Returns:
            经纬度坐标
        """
        try:
            arguments = {"address": address}
            if city:
                arguments["city"] = city

            # maps_geo
            response = await query_mcp_agent(
                prompt=f"调用高德地图maps_geo工具，根据{arguments['address']}和{arguments['city']}查询对应的地理编码信息（地址转为坐标）"
            )
            return response

        except Exception as e:
            print(f"❌ 地理编码失败: {str(e)}")
            return None

    async def get_poi_detail(self, poi_id: str) -> Dict[str, Any]:
        """
        获取POI详情

        Args:
            poi_id: POI ID

        Returns:
            POI详情信息
        """
        # maps_search_detail
        try:
            response = await query_mcp_agent(
                prompt=f"调用maps_search_detail工具，根据{poi_id}去获取对应的POI详情"
            )
            return response

        
            # # 解析结果并提取图片
            # import json
            # import re

            # # 尝试从结果中提取JSON
            # json_match = re.search(r'\{.*\}', result, re.DOTALL)
            # if json_match:
            #     data = json.loads(json_match.group())
            #     return data

            # return {"raw": result}

        except Exception as e:
            print(f"❌ 获取POI详情失败: {str(e)}")
            return {}


# 创建全局服务实例
_amap_service = None


def get_amap_service() -> AmapService:
    """获取高德地图服务实例(单例模式)"""
    global _amap_service
    
    if _amap_service is None:
        _amap_service = AmapService()
    
    return _amap_service
