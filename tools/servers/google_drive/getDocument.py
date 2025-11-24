def get_document(document_id: str):
    """获取Google Drive文档"""
    from mcp_server import get_document as mcp_get_document
    return mcp_get_document(document_id)
