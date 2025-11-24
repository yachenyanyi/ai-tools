def update_record(record_id: str, data: dict):
    """更新Salesforce记录"""
    from mcp_server import update_salesforce_record
    return update_salesforce_record(record_id, data)
