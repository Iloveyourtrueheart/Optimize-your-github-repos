# GitHub Optimizer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/AI-Multi%20LLM-orange.svg" alt="Multi-LLM">
  <img src="https://img.shields.io/badge/GitHub-Automation-purple.svg" alt="GitHub">
</p>

> **让每一个 GitHub 项目都拥有专业级的 README**
>
> 只需一条命令，自动分析代码、智能优化文档、创建 PR 并合并(其实很鸡肋，不如自己搞个claudecode，所以我就懒得继续搞这个了)

---

## ✨ 功能特点

| 功能 | 说明 |
|------|------|
| 🏆 **README 优化** | 自动生成专业、美观、含金量高的 README 文档 |
| 🔍 **代码分析** | 智能分析代码质量问题，提供重构建议 |
| 💾 **自动备份** | 优化前自动备份，一键回滚，安全无忧 |
| 🤖 **多 LLM 支持** | DeepSeek、OpenAI、智谱、阿里、百度等多家供应商 |
| ⚡ **自动合并** | 自动创建 PR 并合并，无需手动操作 |
| 🎯 **零配置** | 首次运行自动引导配置，之后一键优化 |

---

## 🚀 快速开始

### 1. 安装

```bash
git clone https://github.com/YOUR_USERNAME/github-optimizer.git
cd github-optimizer
pip install -e .
```

### 2. 配置（只需一次）

首次使用需要配置 API Key：

```bash
python main.py setup --setup
```

按提示输入：
1. 选择 LLM 提供商（默认 DeepSeek）
2. 输入 LLM API Key
3. 输入 GitHub Token

配置保存在 `~/.github-optimizer/.env`

查看当前配置状态：
```bash
python main.py setup
```

### 3. 运行！

```bash
python main.py optimize --repo 用户名/仓库名
```

**参数说明：**
- `--repo` 后面跟 `用户名/仓库名`，不是完整网址！
- 例如：`python main.py optimize --repo zhangsan/my-project`

---

## 📖 使用示例

### 优化 GitHub 仓库

```bash
# 格式：python main.py optimize --repo 用户名/仓库名
python main.py optimize --repo example/project
python main.py optimize --repo zhangsan/python-learning
```

### 优化本地项目

```bash
python main.py optimize --repo ./my-project --local
```

### 指定 LLM 提供商

```bash
# DeepSeek（默认，性价比最高）
python main.py optimize --repo user/repo

# OpenAI GPT-4o
python main.py optimize --repo user/repo --provider openai --model gpt-4o

# 智谱 GLM
python main.py optimize --repo user/repo --provider zhipu
```

### 预览模式（不提交）

```bash
python main.py optimize --repo user/repo --dry-run
```

### 只创建 PR，不合并

```bash
python main.py optimize --repo user/repo --no-merge
```

### 指定 README 语言

```bash
# 生成中文 README（默认）
python main.py optimize --repo user/repo --lang chinese

# 生成英文 README
python main.py optimize --repo user/repo --lang english
```

---

## 🛠️ 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `setup --setup` | 配置 API Key | `setup --setup` |
| `setup` | 查看配置状态 | `setup` |
| `providers` | 查看支持的 LLM | `providers` |
| `optimize --repo` | 优化项目 | `optimize --repo user/repo` |
| `--repo` | GitHub 仓库或本地路径 | `--repo user/repo` |
| `--local` | 本地仓库模式 | `--local` |
| `--lang` | README 语言 | `--lang chinese` 或 `--lang english` |
| `--dry-run` | 预览模式，不提交 | `--dry-run` |
| `--no-merge` | 只创建 PR | `--no-merge` |
| `--provider` | LLM 提供商 | `--provider deepseek` |
| `--model` | LLM 模型 | `--model gpt-4o` |

---

## 🌐 支持的 LLM 提供商

| 提供商 | 默认模型 | 特点 | 价格 |
|--------|----------|------|------|
| **DeepSeek** | deepseek-chat | 性价比最高，强烈推荐 | 💰💰 |
| OpenAI | gpt-4o | 性能最强 | 💰💰💰💰 |
| 智谱 GLM | glm-4 | 清华系国产 | 💰💰 |
| 阿里通义 | qwen-turbo | 阿里系国产 | 💰💰 |
| 百度文心 | ernie-4.0 | 百度系国产 | 💰💰 |
| MiniMax | MiniMax-Text-01 | 便宜 | 💰 |
| SiliconFlow | Qwen2.5-72B | 聚合开源模型 | 💰💰 |
| Groq | llama-3.1-70b | 免费快速 | 🆓 |
| Gemini | gemini-2.0-flash | Google | 💰💰 |

### 获取 API Key

| 提供商 | 获取地址 |
|--------|----------|
| DeepSeek | [platform.deepseek.com](https://platform.deepseek.com/api_keys) |
| OpenAI | [platform.openai.com](https://platform.openai.com/api-keys) |
| 智谱 GLM | [open.bigmodel.cn](https://open.bigmodel.cn/usercenter/apikeys) |
| 阿里通义 | [dashscope.aliyuncs.com](https://dashscope.console.aliyun.com/api-key) |
| 百度文心 | [console.bce.baidu.com](https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application) |
| MiniMax | [platform.minimax.chat](https://platform.minimax.chat/user-center/basic-information/interface-key) |
| SiliconFlow | [account.siliconflow.cn](https://account.siliconflow.cn/api-keys) |
| Groq | [console.groq.com](https://console.groq.com/keys) |
| Gemini | [aistudio.google.com](https://aistudio.google.com/app/apikey) |

### 获取 GitHub Token（详细步骤）

**什么是 GitHub Token？**
Token 就是一把"钥匙"，让程序能够代替你操作 GitHub 仓库（创建分支、提交文件、创建 PR、合并 PR）。

**手把手教你获取 Token：**

1. **打开 GitHub 设置页面**
   访问：https://github.com/settings/tokens

2. **点击 "Generate new token"**
   选择 "Generate new token (classic)"

3. **设置 Token 名称**
   随便填一个名字，比如 `github-optimizer`

4. **选择权限（重要！）**

   ✅ **必须勾选：**
   - `repo` - 读写仓库内容、创建分支、推送、创建 PR、合并 PR（必选，这个就够了）

   ❌ **不要勾选：**
   - ~~workflows~~ - 不需要修改 GitHub Actions
   - ~~admin:repo*~~ - 管理员权限过大，不安全

   **只需勾选 `repo` 一个权限即可**

5. **点击生成**
   滚动到页面底部，点击 "Generate token"

6. **复制 Token**
   页面会显示一串字符，复制它（以 `ghp_` 开头）

**⚠️ 重要提醒：**
- Token 只显示一次！刷新页面后就再也看不到了，请立刻复制保存
- 不要把 Token 告诉别人，它是你的密码
- 可以随时在 https://github.com/settings/tokens 删除它

---

## 🔄 工作流程

```
┌─────────────────────────────────────────────────────────┐
│  $ python main.py --repo user/repo                       │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│  1. 📦 克隆仓库到本地                                    │
│  2. 🔍 分析项目结构（语言、文件、技术栈）                  │
│  3. 💾 备份原文件到 ./backup/                           │
│  4. 🤖 调用 LLM 分析并生成优化建议                       │
│  5. 📝 保存新的 README.md                               │
│  6. 🌿 创建新分支并推送                                 │
│  7. 🔀 创建 PR 并自动合并                              │
└─────────────────────────────────────────────────────────┘
```

---

## 🔒 安全性

- **自动备份**：每次优化前自动完整备份
- **分支隔离**：所有更改在独立分支进行，不影响原代码
- **预览确认**：支持 `--dry-run` 预览变更内容
- **一键回滚**：备份文件保留在 `./backup/` 目录

---

## 📁 项目结构

```
github-optimizer/
├── main.py              # 🎯 程序入口
├── cli.py               # 💻 命令行接口
├── optimizer.py         # ⚙️  核心优化逻辑
├── llm.py              # 🤖 LLM 提供商接口
├── requirements.txt    # 📦 Python 依赖
├── setup.py            # 📦 pip 安装配置
└── README.md           # 📚 项目文档
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！
