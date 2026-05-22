"""
GitHub 项目优化器 - 核心逻辑
使用 LLM API 分析和优化 GitHub 项目
"""

import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Any

from github import Github
from github.GithubException import GithubException
from tqdm import tqdm

from llm import LLMProvider, get_llm_config, create_llm_client, call_llm


class GitHubOptimizer:
    """GitHub 项目优化器"""

    def __init__(self, llm_provider: str, llm_api_key: str, llm_model: Optional[str], github_token: str, readme_lang: str = "chinese"):
        self.llm_provider = llm_provider
        self.llm_api_key = llm_api_key
        self.llm_model = llm_model
        self.github_token = github_token
        self.readme_lang = readme_lang  # "chinese" or "english"

        # 初始化 LLM
        llm_config = get_llm_config(llm_provider, llm_api_key, llm_model)
        self.llm_client = create_llm_client(llm_config)
        self.model = llm_config.model

        # 初始化 GitHub
        self.github_client = Github(github_token)

        self.work_dir = Path("~/.github-optimizer").expanduser()
        self.backup_dir = Path("./backup")
        self.current_repo_path: Optional[Path] = None
        self.current_repo_name: Optional[str] = None

    def setup(self):
        """初始化工作目录"""
        self.work_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def clone_repo(self, repo_identifier: str) -> Path:
        """克隆仓库到本地"""
        # 构建完整的 GitHub URL
        repo_url = f"https://github.com/{repo_identifier}"

        # 从 URL 提取 owner/repo
        parts = repo_url.replace("https://github.com/", "").replace(".git", "").split("/")
        repo_name = f"{parts[-2]}-{parts[-1]}"

        # 使用带时间戳的目录名，避免重复克隆问题
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_repo_name = f"{repo_name}_{timestamp}"
        target_dir = self.work_dir / self.current_repo_name

        print(f"正在克隆仓库到 {target_dir}...")

        # 克隆
        subprocess.run(["git", "clone", "--quiet", repo_url, str(target_dir)], check=True)
        self.current_repo_path = target_dir
        return target_dir

    def clone_local_repo(self, local_path: str) -> Path:
        """使用本地仓库"""
        local_path = Path(local_path).expanduser().absolute()
        self.current_repo_name = local_path.name
        self.current_repo_path = local_path
        return local_path

    def analyze_project_structure(self) -> dict:
        """分析项目结构"""
        if not self.current_repo_path:
            raise ValueError("请先克隆或打开仓库")

        structure = {
            "files": [],
            "readme_exists": False,
            "has_tests": False,
            "has_requirements": False,
            "has_package_json": False,
            "has_setup_py": False,
            "language": "unknown"
        }

        # 扫描项目文件
        for root, dirs, files in os.walk(self.current_repo_path):
            # 忽略隐藏目录和 node_modules
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]

            for file in files:
                if file.startswith('.'):
                    continue
                file_path = Path(root) / file
                rel_path = file_path.relative_to(self.current_repo_path)

                structure["files"].append(str(rel_path))

                # 检测特定文件
                if file.lower() == "readme.md":
                    structure["readme_exists"] = True
                if "test" in file.lower():
                    structure["has_tests"] = True
                if file == "requirements.txt":
                    structure["has_requirements"] = True
                if file == "package.json":
                    structure["has_package_json"] = True
                if file == "setup.py":
                    structure["has_setup_py"] = True

                # 检测语言
                ext = file.split('.')[-1].lower()
                lang_map = {
                    "py": "Python", "js": "JavaScript", "ts": "TypeScript",
                    "go": "Go", "rs": "Rust", "java": "Java",
                    "cpp": "C++", "c": "C", "rb": "Ruby"
                }
                if ext in lang_map:
                    structure["language"] = lang_map[ext]

        return structure

    def read_all_code_files(self) -> str:
        """读取所有代码文件内容"""
        if not self.current_repo_path:
            raise ValueError("请先克隆或打开仓库")

        content_parts = []
        code_extensions = {'.py', '.js', '.ts', '.go', '.rs', '.java', '.cpp', '.c', '.rb', '.md', '.txt', '.json', '.yaml', '.yml', '.toml'}

        for root, dirs, files in os.walk(self.current_repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]

            for file in files:
                if file.startswith('.'):
                    continue
                file_path = Path(root) / file
                ext = file_path.suffix.lower()

                if ext in code_extensions:
                    try:
                        rel_path = file_path.relative_to(self.current_repo_path)
                        with open(file_path, 'r', encoding='utf-8') as f:
                            file_content = f.read()

                        # 限制单个文件大小 (200KB)
                        if len(file_content) > 200 * 1024:
                            file_content = file_content[:200 * 1024] + "\n... (文件过长已截断)"

                        content_parts.append(f"\n=== {rel_path} ===\n{file_content}")
                    except Exception as e:
                        content_parts.append(f"\n=== {file} (读取失败: {e}) ===\n")

        return "\n".join(content_parts)

    def read_readme(self) -> Optional[str]:
        """读取现有 README"""
        if not self.current_repo_path:
            return None

        for name in ["README.md", "README.md", "readme.md", "README.MD"]:
            readme_path = self.current_repo_path / name
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    return f.read()
        return None

    def backup_current_state(self) -> Path:
        """备份当前状态"""
        if not self.current_repo_path:
            raise ValueError("请先克隆或打开仓库")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"{self.current_repo_name}_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)

        print(f"正在备份到 {backup_path}...")
        shutil.copytree(self.current_repo_path, backup_path, dirs_exist_ok=True)

        return backup_path

    def optimize_with_llm(self, project_info: dict, code_content: str, existing_readme: Optional[str]) -> dict:
        """使用 LLM 优化项目"""

        # 根据语言设置 README 生成要求
        if self.readme_lang == "english":
            readme_instruction = """For README, generate a complete professional README in English with:
- Badges: CI, version, Python version, etc. (do NOT add license badge)
- Project description
- Quick Start (3 steps)
- Features
- Project Structure
- Contributing
- Keep original license info unchanged"""
            readme_content_lang = "English"
            project_desc_lang = "English"
        else:
            readme_instruction = """对于 README，请生成包含以下部分的完整内容（中文）：
- 徽章栏（Badges）：CI、版本、Python版本等（不要添加许可证徽章）
- 项目描述（中英双语）
- 快速开始（Quick Start）- 3步完成
- 核心特性（Features）
- 目录结构（Project Structure）
- 贡献指南（Contributing）
- 保持原有的许可证信息不变"""
            readme_content_lang = "Chinese"
            project_desc_lang = "Chinese"

        system_prompt = f"""你是一位专业的软件工程师和开源项目顾问。你的任务是：

1. **优化代码**：分析代码质量问题，提供具体的代码改动
2. **优化 README**：生成专业、有吸引力、含金量高的 README

{readme_instruction}

重要提醒：
- 不要为项目添加任何许可证，所有许可证信息必须保持原样
- 不要声称自己是某个项目的作者
- 只优化 README 内容，不要修改任何许可证或法律文件
- 代码改动需要提供具体的 original（原始代码）和 improved（改进后代码）

请以 JSON 格式返回，格式如下：
{{
    "readme_content": "# 生成的 README 内容",
    "code_changes": [
        {{
            "file": "文件路径",
            "description": "改动描述",
            "original": "原始代码（不超过500字符）",
            "improved": "改进后代码（不超过500字符）"
        }}
    ],
    "summary": "优化总结"
}}"""

        project_description = f"""
项目名称: {project_info.get('name', 'Unknown')}
项目语言: {project_info.get('language', 'Unknown')}
文件数量: {len(project_info.get('files', []))}
是否有测试: {project_info.get('has_tests', False)}
是否有 requirements: {project_info.get('has_requirements', False)}
是否有 package.json: {project_info.get('has_package_json', False)}
是否有 setup.py: {project_info.get('has_setup_py', False)}
"""

        user_message = f"""请优化这个项目：

{project_description}

现有文件列表（前50个）：
{chr(10).join(project_info.get('files', [])[:50])}

现有 README 内容：
{existing_readme if existing_readme else '无'}

代码内容：
{code_content[:50000]}

请生成优化后的 README（{readme_content_lang}）和具体的代码改动。"""

        print(f"正在使用 {self.llm_provider} ({self.model}) 分析和优化项目...")

        response_text = call_llm(self.llm_client, self.model, system_prompt, user_message)

        import json
        import re

        # 尝试提取 JSON
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            try:
                result = json.loads(json_match.group())
                # 确保有 code_changes 字段
                if "code_changes" not in result:
                    result["code_changes"] = []
                return result
            except json.JSONDecodeError:
                pass

        # 如果 JSON 解析失败，返回原始内容
        return {
            "readme_content": response_text,
            "code_changes": [],
            "summary": "优化完成"
        }

    def preview_code_changes(self, code_changes: list):
        """预览代码改动"""
        if not code_changes:
            print("没有代码改动需要预览")
            return

        print("\n" + "=" * 60)
        print("代码改动预览")
        print("=" * 60)

        for i, change in enumerate(code_changes, 1):
            print(f"\n[{i}] 文件: {change.get('file', 'unknown')}")
            print(f"    描述: {change.get('description', '无')}")
            print(f"    原始代码:")
            print("    " + "-" * 40)
            for line in change.get('original', '').split('\n'):
                print(f"    | {line}")
            print(f"    改进后:")
            print("    " + "-" * 40)
            for line in change.get('improved', '').split('\n'):
                print(f"    | {line}")
            print("    " + "-" * 40)

        print("\n" + "=" * 60)

    def apply_code_changes(self, code_changes: list):
        """应用代码改动"""
        if not code_changes:
            print("没有代码改动需要应用")
            return

        if not self.current_repo_path:
            raise ValueError("请先克隆或打开仓库")

        for change in code_changes:
            file_path = self.current_repo_path / change.get('file', '')
            if not file_path.exists():
                print(f"文件不存在，跳过: {file_path}")
                continue

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()

                original_code = change.get('original', '')
                improved_code = change.get('improved', '')

                # 替换原始代码为改进后代码
                if original_code in original_content:
                    new_content = original_content.replace(original_code, improved_code)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"已应用改动: {change.get('file', '')}")
                else:
                    print(f"未找到匹配的原始代码，跳过: {change.get('file', '')}")
            except Exception as e:
                print(f"应用改动失败 {change.get('file', '')}: {e}")

    def save_readme(self, readme_content: str):
        """保存 README"""
        if not self.current_repo_path:
            raise ValueError("请先克隆或打开仓库")

        readme_path = self.current_repo_path / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"README 已更新: {readme_path}")

    def commit_and_push(self, commit_message: str = "docs: 优化 README 和代码"):
        """提交并推送更改"""
        if not self.current_repo_path:
            raise ValueError("请先克隆或打开仓库")

        # 配置 git
        subprocess.run(["git", "config", "user.email", "optimizer@github.com"], cwd=self.current_repo_path, check=True)
        subprocess.run(["git", "config", "user.name", "GitHub Optimizer"], cwd=self.current_repo_path, check=True)

        # 创建新分支
        branch_name = f"optimization-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        subprocess.run(["git", "checkout", "-b", branch_name], cwd=self.current_repo_path, check=True)

        # 添加所有更改
        subprocess.run(["git", "add", "-A"], cwd=self.current_repo_path, check=True)

        # 检查是否有更改
        result = subprocess.run(["git", "diff", "--cached", "--stat"], cwd=self.current_repo_path, capture_output=True, text=True)
        if not result.stdout.strip():
            print("没有检测到更改，跳过提交")
            return None

        # 提交
        subprocess.run(["git", "commit", "-m", commit_message], cwd=self.current_repo_path, check=True)

        # 推送到远程
        print("正在推送到远程...")
        subprocess.run(["git", "push", "-u", "origin", branch_name, "--quiet"], cwd=self.current_repo_path, check=True)

        return branch_name

    def create_pull_request(self, branch_name: str, title: str = "docs: 项目优化") -> Optional[Any]:
        """创建 Pull Request"""
        if not self.current_repo_path:
            return None

        # 从 git remote 获取仓库信息
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=self.current_repo_path,
            capture_output=True,
            text=True
        )
        remote_url = result.stdout.strip()

        # 提取 owner/repo
        parts = remote_url.replace("https://github.com/", "").replace(".git", "").split("/")
        if len(parts) >= 2:
            owner, repo = parts[-2], parts[-1]
        else:
            return None

        try:
            gh_repo = self.github_client.get_repo(f"{owner}/{repo}")

            # 获取默认分支
            default_branch = gh_repo.default_branch

            # 创建 PR
            pr = gh_repo.create_pull(
                title=title,
                body="""## 优化总结

本 PR 由 GitHub Optimizer 自动生成。

### 优化内容
- README 文档优化
- 代码结构和最佳实践改进

### 变更文件
- README.md

如有问题，欢迎反馈！""",
                head=branch_name,
                base=default_branch
            )

            print(f"PR 创建成功: {pr.html_url}")
            return pr

        except GithubException as e:
            print(f"创建 PR 失败: {e}")
            return None

    def merge_pull_request(self, pr_url: str) -> bool:
        """合并 Pull Request"""
        # 从 URL 提取 PR 编号
        parts = pr_url.split("/")
        try:
            pr_number = int(parts[-1])
        except (ValueError, IndexError):
            print(f"无法解析 PR 编号: {pr_url}")
            return False

        # 获取仓库信息
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=self.current_repo_path,
            capture_output=True,
            text=True
        )
        remote_url = result.stdout.strip()

        parts = remote_url.replace("https://github.com/", "").replace(".git", "").split("/")
        if len(parts) >= 2:
            owner, repo = parts[-2], parts[-1]
        else:
            return False

        try:
            gh_repo = self.github_client.get_repo(f"{owner}/{repo}")
            pr = gh_repo.get_pull(pr_number)
            pr.merge()
            print(f"PR #{pr_number} 已合并到 {repo}")
            return True

        except GithubException as e:
            print(f"合并 PR 失败: {e}")
            return False

    def cleanup(self):
        """清理工作目录"""
        if self.current_repo_path and self.current_repo_path.exists():
            # 切回默认分支
            try:
                subprocess.run(["git", "checkout", "main"], cwd=self.current_repo_path, check=False)
            except:
                try:
                    subprocess.run(["git", "checkout", "master"], cwd=self.current_repo_path, check=False)
                except:
                    pass
