"""
安全代码执行环境
实现Anthropic提出的代码执行范式，让Agent能够编写代码来调用工具
而不是直接调用工具，从而减少Token消耗
"""
import subprocess
import tempfile
import os
import sys
import io
import contextlib
from typing import Dict, Any, Optional
import json
import ast
import RestrictedPython
from RestrictedPython import compile_restricted
from RestrictedPython.compile import compile_restricted_exec
from RestrictedPython.Guards import safe_globals, safe_builtins
from RestrictedPython.transformer import ALLOWED_FUNC_NAMES

from mcp_server import (
    get_document, update_salesforce_record, send_slack_message, 
    get_slack_messages, get_sheet_data, update_sheet, call_mcp_tool
)

class CodeExecutionEnvironment:
    """
    安全的代码执行环境，支持Agent编写代码来调用工具
    实现Anthropic提出的代码执行范式
    """
    
    def __init__(self):
        # 定义安全的全局变量，包括工具API
        self.safe_globals = {
            '__builtins__': {
                'len': len,
                'str': str,
                'int': int,
                'float': float,
                'bool': bool,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'range': range,
                'enumerate': enumerate,
                'zip': zip,
                'max': max,
                'min': min,
                'sum': sum,
                'abs': abs,
                'round': round,
                'pow': pow,
                'divmod': divmod,
                'sorted': sorted,
                'reversed': reversed,
                'all': all,
                'any': any,
                'isinstance': isinstance,
                'issubclass': issubclass,
                'type': type,
                'Exception': Exception,
                'ValueError': ValueError,
                'TypeError': TypeError,
                'KeyError': KeyError,
                'IndexError': IndexError,
                'AttributeError': AttributeError,
                'ZeroDivisionError': ZeroDivisionError,
                'json': json,
            },
            # RestrictedPython需要的安全函数
            '_print_': lambda x: x,
            '_getitem_': lambda ob, index: ob[index],
            '_getiter_': lambda ob: iter(ob),
            '_iter_unpack_sequence_': lambda ob: ob,
            '__import__': __import__,
            '_unpack_sequence_': lambda ob: ob,
            '_abs_': abs,
            '_min_': min,
            '_max_': max,
            '_sum_': sum,
            '_getattr_': getattr,
            '_setattr_': setattr,
            '_delattr_': delattr,
            '_getpath_': lambda ob, name: getattr(ob, name),
            # 注意：_write_函数不会添加，以保持环境安全
            # 工具API接口
            'get_document': get_document,
            'update_salesforce_record': update_salesforce_record,
            'send_slack_message': send_slack_message,
            'get_slack_messages': get_slack_messages,
            'get_sheet_data': get_sheet_data,
            'update_sheet': update_sheet,
            'call_mcp_tool': call_mcp_tool,
        }
        
        # 添加标准库的安全子集
        safe_modules = [
            'math', 'random', 'datetime', 'collections', 'itertools', 
            'functools', 'operator', 'json', 're', 'urllib.parse', 'time'
        ]
        
        for module_name in safe_modules:
            try:
                module = __import__(module_name)
                self.safe_globals[module_name] = module
            except ImportError:
                pass
    
    def execute_code(self, code: str) -> Dict[str, Any]:
        """
        执行Agent编写的代码
        这是新范式的核心：Agent写代码而不是直接调用工具
        """
        result = {
            "success": True,
            "output": "",
            "result": None,
            "error": None
        }
        
        # 捕获输出
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        try:
            # 重定向输出
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture
            
            # 使用RestrictedPython编译代码以增加安全性
            byte_code, error_log, warnings, used_names = compile_restricted_exec(code)
            
            if error_log:
                result["success"] = False
                result["error"] = f"Compilation errors: {error_log}"
                return result
            
            if byte_code is None:
                result["success"] = False
                result["error"] = "Compilation failed: returned None"
                return result
            
            # 执行代码
            local_vars = {}
            exec(byte_code, self.safe_globals, local_vars)
            
            # 获取结果
            result["output"] = stdout_capture.getvalue()
            result["result"] = local_vars.get("result", None)
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            result["output"] = stdout_capture.getvalue()
        finally:
            # 恢复原始输出
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
        return result

    def validate_code(self, code: str) -> Dict[str, Any]:
        """
        验证代码的安全性
        """
        try:
            # 解析代码为AST以检查是否有不安全的操作
            tree = ast.parse(code)
            
            # 检查是否有危险操作
            dangerous_nodes = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                    # 检查是否导入了危险模块
                    for alias in node.names:
                        module_name = alias.name
                        if module_name in ['os', 'sys', 'subprocess', 'shutil', 'socket', 'urllib.request']:
                            dangerous_nodes.append(f"Dangerous import: {module_name}")
                elif isinstance(node, ast.Call):
                    # 检查函数调用
                    if isinstance(node.func, ast.Name):
                        if node.func.id in ['eval', 'exec', 'compile']:
                            dangerous_nodes.append(f"Dangerous function call: {node.func.id}")
            
            if dangerous_nodes:
                return {
                    "valid": False,
                    "errors": dangerous_nodes
                }
            
            return {
                "valid": True,
                "errors": []
            }
        except SyntaxError as e:
            return {
                "valid": False,
                "errors": [f"Syntax error: {str(e)}"]
            }

# 全局代码执行环境实例
execution_env = CodeExecutionEnvironment()

def execute_agent_code(code: str) -> Dict[str, Any]:
    """
    执行Agent编写的代码，这是新范式的关键接口
    """
    # 首先验证代码安全性
    validation_result = execution_env.validate_code(code)
    if not validation_result["valid"]:
        return {
            "success": False,
            "error": f"Code validation failed: {validation_result['errors']}"
        }
    
    # 执行代码
    return execution_env.execute_code(code)

# 示例用法
if __name__ == "__main__":
    print("Code Execution Environment initialized")
    
    # 示例1：下载文档并更新Salesforce记录
    example_code1 = """
# 从Google Drive下载会议纪要
document = get_document("abc123")

# 处理文档内容
content = document["result"]["content"]

# 更新Salesforce记录
update_result = update_salesforce_record("rec123", {"meeting_notes": content})
result = {"document_title": document["result"]["title"], "update_status": update_result["result"]["status"]}
"""
    
    print("\nExecuting example code 1:")
    result1 = execute_agent_code(example_code1)
    print(f"Result: {result1}")
    
    # 示例2：处理大量数据并只返回摘要
    example_code2 = """
# 获取大量电子表格数据
sheet_data = get_sheet_data("sheet123")

# 在代码执行环境中处理数据，只返回摘要
total_employees = len(sheet_data["result"])
departments = {}
for row in sheet_data["result"]:
    dept = row["department"]
    departments[dept] = departments.get(dept, 0) + 1

result = {
    "total_employees": total_employees,
    "departments": departments
}
"""
    
    print("\nExecuting example code 2:")
    result2 = execute_agent_code(example_code2)
    print(f"Result: {result2}")