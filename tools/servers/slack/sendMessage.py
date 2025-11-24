def send_message(channel: str, message: str):
    """发送Slack消息"""
    from mcp_server import send_slack_message
    return send_slack_message(channel, message)
