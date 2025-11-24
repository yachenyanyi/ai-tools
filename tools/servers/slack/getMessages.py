def get_messages(channel: str):
    """获取Slack消息"""
    from mcp_server import get_slack_messages
    return get_slack_messages(channel)
