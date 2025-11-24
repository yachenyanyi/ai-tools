def query_records(object_type: str, criteria: dict):
    """查询Salesforce记录"""
    from mcp_server import call_mcp_tool
    return call_mcp_tool("salesforce", operation="query_records", 
                         object_type=object_type, criteria=criteria)
