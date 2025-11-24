"""
完整演示：Anthropic新Agent范式
展示代码执行范式如何解决传统Agent的Token消耗问题
"""
from agent import Agent
from filesystem_tools import ls, cat, find_tools
from code_execution_env import execute_agent_code
import time

def demonstrate_paradigm_shift():
    """
    演示新范式相对于传统方法的优势
    """
    print("="*60)
    print("ANTHROPIC新AGENT范式演示")
    print("代码执行范式 vs 传统工具调用范式")
    print("="*60)
    
    agent = Agent()
    
    print("\n1. 传统Agent模式的问题:")
    print("   - 工具定义过载: 所有工具定义加载到上下文 -> 消耗大量Token")
    print("   - 中间结果消耗: 每个中间结果都经过模型上下文 -> Token浪费")
    print("   - 例如: 处理2小时会议纪要(50,000 Token) -> Token消耗翻倍")
    
    print("\n2. 新范式解决方案:")
    print("   - Agent编写代码来调用工具，而不是直接调用")
    print("   - 数据在代码执行环境中流转，不经过模型上下文")
    print("   - 结果: Token消耗从150,000降到2,000，节省98.7%")
    
    print("\n" + "-"*50)
    print("演示1: 下载文档并更新Salesforce")
    print("-"*50)
    
    task1 = "Download meeting notes from Google Drive and update Salesforce record"
    result1 = agent.execute_task(task1)
    print(f"执行结果: {result1}")
    
    print("\n关键优势:")
    print("- 会议纪要内容在代码执行环境中处理")
    print("- 不会占用模型上下文Token")
    print("- 只有最终结果返回给模型")
    
    print("\n" + "-"*50)
    print("演示2: 处理大电子表格并返回摘要")
    print("-"*50)
    
    task2 = "Process large spreadsheet and return summary"
    result2 = agent.execute_task(task2)
    print(f"执行结果: {result2}")
    
    print("\n关键优势:")
    print("- 10,000行数据在执行环境中过滤和聚合")
    print("- 模型只看到5行摘要，而非全部10,000行")
    print("- 大幅减少Token消耗")
    
    print("\n" + "-"*50)
    print("演示3: 文件系统访问和渐进式披露")
    print("-"*50)
    
    print("Agent可以浏览文件系统发现可用工具:")
    print(f"根目录: {ls('/')}")
    print(f"服务器目录: {ls('servers')}")
    print(f"Google Drive工具: {ls('servers/google_drive')}")
    
    print("\n按需读取工具定义:")
    drive_tool = cat('servers/google_drive/getDocument.ts')
    print(f"getDocument.ts内容:\n{drive_tool}")
    
    print("\n关键优势:")
    print("- 不需要预先加载所有工具定义")
    print("- 按需发现和加载必要工具")
    print("- 减少初始Token消耗")
    
    print("\n" + "-"*50)
    print("演示4: 复杂控制流 - 轮询操作")
    print("-"*50)
    
    task3 = "Poll Slack for deployment completion message"
    result3 = agent.execute_task(task3)
    print(f"执行结果: {result3}")
    
    print("\n关键优势:")
    print("- 在代码环境中实现复杂控制流")
    print("- 而非通过多次工具调用模拟")
    print("- 减少模型交互次数和延迟")
    
    print("\n" + "-"*50)
    print("演示5: 技能保存和复用")
    print("-"*50)
    
    # 保存一个技能
    export_skill = """
# 导出销售数据为CSV的技能
import csv
import io

# 获取销售数据
sales_data = get_sheet_data("sales-sheet")

# 创建CSV内容
csv_content = "name,email,phone,department\\n"
for row in sales_data["result"]:
    csv_content += f"{row['name']},{row['email']},{row['phone']},{row['department']}\\n"

# 保存为文件
with open("sales_export.csv", "w") as f:
    f.write(csv_content)

result = {"status": "success", "file": "sales_export.csv", "rows": len(sales_data["result"])}
"""
    
    agent.save_skill("export_sales_csv", export_skill)
    skill_result = agent.execute_skill("export_sales_csv")
    print(f"技能执行结果: {skill_result}")
    
    print("\n关键优势:")
    print("- 技能可复用，形成高级能力工具箱")
    print("- 通过代码实现复杂任务自动化")
    print("- 无需每次都重新编写相同逻辑")

def compare_token_usage():
    """
    对比Token使用情况
    """
    print("\n" + "="*60)
    print("TOKEN使用对比")
    print("="*60)
    
    print("\n传统方法:")
    print("- 工具定义: 50,000 Token (所有工具描述)")
    print("- 文档内容: 50,000 Token (2小时会议纪要)")
    print("- 工具调用结果: 50,000 Token (中间结果存储)")
    print("- 其他上下文: 50,000 Token")
    print("总计: ~200,000 Token")
    
    print("\n新方法:")
    print("- 工具API引用: 100 Token (少量代码接口)")
    print("- 最终结果: 1,000 Token (摘要信息)")
    print("- 代码定义: 900 Token (执行逻辑)")
    print("总计: ~2,000 Token")
    
    print(f"\n节省: {(200000-2000)/200000*100:.1f}% Token消耗")

def main():
    """
    主函数：运行完整演示
    """
    print("开始演示Anthropic新Agent范式...")
    
    demonstrate_paradigm_shift()
    compare_token_usage()
    
    print("\n" + "="*60)
    print("总结: 新范式的核心优势")
    print("="*60)
    
    advantages = [
        "1. 渐进式披露: 按需发现和加载工具，避免预加载所有定义",
        "2. 上下文高效: 大数据在执行环境中处理，只返回摘要",
        "3. 强大控制流: 支持循环、条件判断等复杂逻辑",
        "4. 隐私保护: 敏感数据不经过模型上下文",
        "5. 状态持久化: 通过文件系统实现任务中断和恢复",
        "6. 技能积累: 可复用代码片段形成高级能力工具箱"
    ]
    
    for advantage in advantages:
        print(advantage)
    
    print(f"\n成本和时间节省:  高达98.7%")
    print("新范式让Agent能够以其最擅长的方式 - 编写代码 - 来更高效地与世界互动")

if __name__ == "__main__":
    main()