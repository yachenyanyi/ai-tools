"""
Agent实现，采用Anthropic提出的代码执行新范式
Agent不再直接调用工具，而是编写代码来完成任务
"""
from typing import Dict, Any, List
import json
from code_execution_env import execute_agent_code

class Agent:
    """
    实现新范式的Agent
    不再选择工具并填充参数，而是编写代码来完成整个工作流
    """
    
    def __init__(self):
        self.skills = {}  # 存储可复用的技能（代码片段）
        
    def generate_code_for_task(self, task_description: str) -> str:
        """
        根据任务描述生成相应的代码
        这是新范式的核心：Agent写代码而不是选择工具
        """
        # 根据任务类型生成相应的代码模板
        if "download document" in task_description.lower() and "update salesforce" in task_description.lower():
            # 示例：下载文档并更新Salesforce
            return """
# 从Google Drive下载会议纪要
document = get_document("abc123")

# 提取文档内容
content = document["result"]["content"]

# 更新Salesforce记录
update_result = update_salesforce_record("rec123", {"meeting_notes": content})

# 返回结果
result = {
    "document_title": document["result"]["title"], 
    "update_status": update_result["result"]["status"],
    "message": "Successfully updated Salesforce with meeting notes"
}
"""
        elif "process large spreadsheet" in task_description.lower():
            # 示例：处理大电子表格并返回摘要
            return """
# 获取大量电子表格数据
sheet_data = get_sheet_data("sheet123")

# 在代码执行环境中过滤和聚合数据
total_employees = len(sheet_data["result"])
departments = {}
emails = []
for row in sheet_data["result"]:
    dept = row["department"]
    departments[dept] = departments.get(dept, 0) + 1
    emails.append(row["email"])

# 只返回摘要信息，不返回完整数据集
result = {
    "total_employees": total_employees,
    "departments": departments,
    "sample_emails": emails[:3]  # 只返回前3个邮箱作为样本
}
"""
        elif "poll slack" in task_description.lower():
            # 示例：轮询Slack等待部署完成消息
            return """
# 轮询Slack直到找到部署完成消息
start_time = time.time()
timeout = 300  # 5分钟超时

while time.time() - start_time < timeout:
    messages = get_slack_messages("deploy-channel")
    
    # 检查是否有部署完成的消息
    for msg in messages["result"]:
        if "部署完成" in msg["text"] or "deployment complete" in msg["text"]:
            result = {
                "status": "success",
                "message": msg["text"],
                "timestamp": msg["ts"]
            }
            break
    else:
        # 如果没有找到完成消息，等待5秒后重试
        import time; time.sleep(5)  # 注意：在实际实现中，可能需要避免使用sleep
        continue
    break
else:
    # 如果超时仍未找到
    result = {
        "status": "timeout",
        "message": "Deployment completion message not found within timeout"
    }
"""
        else:
            # 默认处理：简单任务
            return f"""
# 执行任务: {task_description}

# 这里可以添加根据任务描述自动生成的代码
result = {{
    "task": "{task_description}",
    "status": "completed",
    "message": "Task completed using code execution paradigm"
}}
"""

    def execute_task(self, task_description: str) -> Dict[str, Any]:
        """
        执行任务：生成代码并执行
        """
        print(f"Agent received task: {task_description}")
        
        # 生成代码
        code = self.generate_code_for_task(task_description)
        print(f"Generated code:\n{code}")
        
        # 执行代码
        execution_result = execute_agent_code(code)
        
        return execution_result
    
    def save_skill(self, skill_name: str, code: str):
        """
        保存技能（可复用的代码片段）
        """
        self.skills[skill_name] = code
        print(f"Skill '{skill_name}' saved successfully")
    
    def execute_skill(self, skill_name: str, **kwargs) -> Dict[str, Any]:
        """
        执行已保存的技能
        """
        if skill_name not in self.skills:
            return {"success": False, "error": f"Skill '{skill_name}' not found"}
        
        # 在代码中替换参数
        code = self.skills[skill_name]
        for key, value in kwargs.items():
            code = code.replace(f"{{{{{key}}}}}", str(value))
        
        return execute_agent_code(code)

# 示例使用
if __name__ == "__main__":
    agent = Agent()
    
    print("=== 示例1: 下载文档并更新Salesforce ===")
    result1 = agent.execute_task("Download meeting notes from Google Drive and update Salesforce record")
    print(f"Result: {result1}\n")
    
    print("=== 示例2: 处理大电子表格 ===")
    result2 = agent.execute_task("Process large spreadsheet and return summary")
    print(f"Result: {result2}\n")
    
    print("=== 示例3: 轮询Slack ===")
    result3 = agent.execute_task("Poll Slack for deployment completion message")
    print(f"Result: {result3}\n")
    
    # 演示技能保存和复用
    print("=== 演示技能保存和复用 ===")
    export_sales_csv_skill = """
# 导出销售数据为CSV的技能

# 获取销售数据
sales_data = get_sheet_data("sales-sheet")

# 创建CSV内容
csv_content = "name,email,phone,department\\n"
for row in sales_data["result"]:
    csv_content += f"{row['name']},{row['email']},{row['phone']},{row['department']}\\n"

# 返回CSV内容而不是写入文件（在安全环境中）
result = {"status": "success", "csv_content": csv_content, "rows": len(sales_data["result"])}
"""
    
    agent.save_skill("export_sales_csv", export_sales_csv_skill)
    skill_result = agent.execute_skill("export_sales_csv")
    print(f"Skill execution result: {skill_result}")