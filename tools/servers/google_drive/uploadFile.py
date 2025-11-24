def upload_file(file_path: str, folder_id: str):
    """上传文件到Google Drive"""
    from mcp_server import call_mcp_tool
    return call_mcp_tool("google_drive", operation="upload_file", 
                         file_path=file_path, folder_id=folder_id)
