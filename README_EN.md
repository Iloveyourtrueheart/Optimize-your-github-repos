# GitHub Optimizer

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/AI-Multi%20LLM-orange.svg" alt="Multi-LLM">
  <img src="https://img.shields.io/badge/GitHub-Automation-purple.svg" alt="GitHub">
</p>

> **Make every GitHub project have a professional-grade README**
>
> One command to analyze code, optimize documentation, create PR and merge automatically

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🏆 **README Optimization** | Auto-generate professional, beautiful README |
| 🔍 **Code Analysis** | Intelligent code quality analysis and suggestions |
| 💾 **Auto Backup** | Safe rollback before optimization |
| 🤖 **Multi-LLM** | DeepSeek, OpenAI, Zhipu, Alibaba, Baidu & more |
| ⚡ **Auto Merge** | Auto-create and merge PR |
| 🎯 **Zero Config** | Auto-guided setup, one-click optimize |

---

## 🚀 Quick Start

### 1. Install

```bash
git clone https://github.com/YOUR_USERNAME/github-optimizer.git
cd github-optimizer
pip install -e .
```

### 2. Setup (once)

```bash
python main.py --setup
```

### 3. Run!

```bash
python main.py optimize --repo 用户名/仓库名
```

**Note:** `--repo` takes `用户名/仓库名`, not the full URL!

---

## 📖 Usage

```bash
# Format: python main.py optimize --repo username/repo
python main.py optimize --repo user/repo

# Local repo
python main.py optimize --repo ./my-project --local

# Specify LLM
python main.py optimize --repo user/repo --provider openai --model gpt-4o

# English README
python main.py optimize --repo user/repo --lang english

# Preview only
python main.py optimize --repo user/repo --dry-run
```

---

## 🛠️ Options

| Option | Description |
|--------|-------------|
| `optimize --repo` | Optimize project |
| `--repo` | GitHub repo (用户名/仓库名) or local path |
| `--local` | Use local repository |
| `--lang` | README language: `chinese` or `english` |
| `setup --setup` | Configure API keys |
| `setup` | Show config status |
| `--dry-run` | Preview without committing |
| `--no-merge` | Create PR only, no auto-merge |
| `--provider` | LLM provider name |
| `--model` | LLM model name |
| `--providers` | List supported LLM providers |

---

## 🌐 Supported LLM Providers

| Provider | Default Model | Price |
|----------|---------------|-------|
| **DeepSeek** | deepseek-chat | 💰💰 |
| OpenAI | gpt-4o | 💰💰💰💰 |
| Zhipu GLM | glm-4 | 💰💰 |
| Alibaba | qwen-turbo | 💰💰 |
| Baidu | ernie-4.0 | 💰💰 |
| MiniMax | MiniMax-Text-01 | 💰 |
| SiliconFlow | Qwen2.5-72B | 💰💰 |
| Groq | llama-3.1-70b | 🆓 |
| Gemini | gemini-2.0-flash | 💰💰 |

### Get GitHub Token (Step by Step)

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name (e.g., `github-optimizer`)

4. **Select Scopes (Important!)**

   ✅ **Required:**
   - `repo` - Read/write repo, create branches, push, PR (required - this is all you need)

   ❌ **Do NOT check:**
   - ~~workflows~~ - Don't need to modify GitHub Actions
   - ~~admin:repo*~~ - Too many permissions, not safe

   **Just check `repo` - that's all you need!**

5. Click "Generate token"
6. **Copy the token immediately** - it only shows once!

---

## 📁 Project Structure

```
github-optimizer/
├── main.py              # Entry point
├── cli.py               # CLI interface
├── optimizer.py         # Core logic
├── llm.py              # LLM provider interface
├── requirements.txt     # Dependencies
├── setup.py             # pip install config
└── README.md           # Documentation
```

---

## 🤝 Contributing

Issues and PRs are welcome!
