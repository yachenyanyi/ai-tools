# Anthropic新Agent范式演示项目

本项目演示了Anthropic提出的Agent开发新范式，通过代码执行范式显著降低Token消耗，提高开发效率。

## 核心概念

- **传统Agent模式**：Agent选择工具并填充参数
- **新范式**：Agent编写代码来完成整个工作流
- **Token消耗**：从150,000降至2,000，节省98.7%

## 项目结构

- `agent.py`：实现新范式的Agent类
- `code_execution_env.py`：安全的代码执行环境
- `mcp_server.py`：MCP (Model Context Protocol) 服务器模拟
- `filesystem_tools.py`：文件系统工具，支持渐进式披露
- `demo.py`：完整演示程序

## 运行方法

```bash
# 运行完整演示
python demo.py

# 运行单个组件测试
python -c "from agent import Agent; agent = Agent(); result = agent.execute_task('Process large spreadsheet and return summary'); print(result)"
```

## 核心优势

1. **渐进式披露**：按需发现和加载工具，避免预加载所有定义
2. **上下文高效**：大数据在执行环境中处理，只返回摘要
3. **强大控制流**：支持循环、条件判断等复杂逻辑
4. **隐私保护**：敏感数据不经过模型上下文
5. **状态持久化**：通过文件系统实现任务中断和恢复
6. **技能积累**：可复用代码片段形成高级能力工具箱

## 技术实现

- 使用RestrictedPython确保代码执行安全
- MCP服务器提供工具API接口
- 虚拟文件系统支持工具发现
- 安全的全局变量和函数限制

## 成本节省

- 传统方法：约200,000 Token
- 新范式：约2,000 Token
- 节省：99% Token消耗
