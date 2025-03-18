# AutoGenTest 项目指南

## 🎯 项目概述
基于 Microsoft AutoGen 框架构建的多智能体协作实验项目

## ⚙️ 环境配置

### 创建虚拟环境
```bash
python -m venv venv
```

Windows 系统
激活
.\venv\Scripts\activate

Linux/macOS 系统
source venv/bin/activate

退出虚拟环境
deactivate

安装依赖
pip install -U "autogen-agentchat" "autogen-ext[openai]" "autogen-ext[mcp]" "mcp-server-fetch" "autogen-ext[http-tool]"