"""
MCP (Model Context Protocol) Server模拟实现
提供各种工具的API接口，Agent可以通过代码来调用这些工具
"""
import json
import time
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ToolCall:
    tool_name: str
    parameters: Dict[str, Any]

class MCPServer:
    """模拟MCP服务器，提供各种工具的API接口"""
    
    def __init__(self):
        self.tools = {
            'google_drive': GoogleDriveTool(),
            'salesforce': SalesforceTool(),
            'slack': SlackTool(),
            'google_sheets': GoogleSheetsTool()
        }
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """调用指定的工具"""
        if tool_name not in self.tools:
            return {"error": f"Tool {tool_name} not found"}
        
        try:
            result = self.tools[tool_name].execute(**kwargs)
            return {"success": True, "result": result}
        except Exception as e:
            return {"error": str(e)}

class GoogleDriveTool:
    """Google Drive工具模拟"""
    
    def execute(self, operation: str, **kwargs):
        if operation == "get_document":
            document_id = kwargs.get("document_id")
            # 模拟从Google Drive获取文档
            if document_id == "abc123":
                return {
                    "id": "abc123",
                    "title": "Q4目标会议纪要",
                    "content": "讨论了Q4目标...\n完整纪要文本，包含大量详细内容和数据..."
                }
            else:
                return {"error": "Document not found"}
        elif operation == "upload_file":
            return {"status": "uploaded", "file_id": "xyz789"}
        else:
            return {"error": f"Operation {operation} not supported"}

class SalesforceTool:
    """Salesforce工具模拟"""
    
    def execute(self, operation: str, **kwargs):
        if operation == "update_record":
            record_id = kwargs.get("record_id")
            data = kwargs.get("data")
            # 模拟更新Salesforce记录
            return {
                "status": "success",
                "record_id": record_id,
                "updated_fields": len(data) if isinstance(data, dict) else 1
            }
        elif operation == "query_records":
            # 模拟查询记录
            return [
                {"id": "rec1", "name": "客户A", "status": "active"},
                {"id": "rec2", "name": "客户B", "status": "inactive"}
            ]
        else:
            return {"error": f"Operation {operation} not supported"}

class SlackTool:
    """Slack工具模拟"""
    
    def execute(self, operation: str, **kwargs):
        if operation == "send_message":
            channel = kwargs.get("channel")
            message = kwargs.get("message")
            return {"status": "sent", "channel": channel, "ts": time.time()}
        elif operation == "get_messages":
            # 模拟获取消息
            return [
                {"user": "U123", "text": "部署开始", "ts": time.time() - 300},
                {"user": "U123", "text": "部署完成", "ts": time.time() - 60}
            ]
        else:
            return {"error": f"Operation {operation} not supported"}

class GoogleSheetsTool:
    """Google Sheets工具模拟"""
    
    def execute(self, operation: str, **kwargs):
        if operation == "get_sheet_data":
            sheet_id = kwargs.get("sheet_id")
            # 模拟获取电子表格数据
            return [
                {"name": "张三", "email": "zhangsan@example.com", "phone": "13800138000", "department": "销售"},
                {"name": "李四", "email": "lisi@example.com", "phone": "13800138001", "department": "技术"},
                {"name": "王五", "email": "wangwu@example.com", "phone": "13800138002", "department": "市场"},
            ]
        elif operation == "update_sheet":
            return {"status": "updated", "rows_affected": kwargs.get("rows_count", 0)}
        else:
            return {"error": f"Operation {operation} not supported"}

# 全局MCP服务器实例
mcp_server = MCPServer()

def call_mcp_tool(tool_name: str, **kwargs) -> Dict[str, Any]:
    """供Agent代码调用的工具函数"""
    return mcp_server.call_tool(tool_name, **kwargs)

# 工具API接口，供Agent代码使用
def get_document(document_id: str):
    """获取Google Drive文档"""
    return call_mcp_tool("google_drive", operation="get_document", document_id=document_id)

def update_salesforce_record(record_id: str, data: Dict[str, Any]):
    """更新Salesforce记录"""
    return call_mcp_tool("salesforce", operation="update_record", record_id=record_id, data=data)

def send_slack_message(channel: str, message: str):
    """发送Slack消息"""
    return call_mcp_tool("slack", operation="send_message", channel=channel, message=message)

def get_slack_messages(channel: str):
    """获取Slack消息"""
    return call_mcp_tool("slack", operation="get_messages", channel=channel)

def get_sheet_data(sheet_id: str):
    """获取电子表格数据"""
    return call_mcp_tool("google_sheets", operation="get_sheet_data", sheet_id=sheet_id)

def update_sheet(sheet_id: str, data: List[Dict[str, Any]]):
    """更新电子表格"""
    return call_mcp_tool("google_sheets", operation="update_sheet", sheet_id=sheet_id, data=data)