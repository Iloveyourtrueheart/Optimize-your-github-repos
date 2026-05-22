#!/usr/bin/env python3
"""
GitHub 项目优化器 CLI
命令行工具，用于优化 GitHub 项目
"""

import os
import sys
from pathlib import Path

# Windows 控制台 UTF-8 支持
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

import click
from dotenv import load_dotenv

from optimizer import GitHubOptimizer
from llm import list_providers, PROVIDER_CONFIGS, LLMProvider


def load_config():
    """加载配置"""
    # 尝试加载 .env 文件
    env_path = Path.home() / ".github-optimizer" / ".env"
    if env_path.exists():
        load_dotenv(env_path)

    # 也检查当前目录
    if Path(".env").exists():
        load_dotenv(".env")

    llm_provider = os.environ.get("LLM_PROVIDER", "deepseek")
    llm_api_key = os.environ.get("LLM_API_KEY")
    llm_model = os.environ.get("LLM_MODEL")
    github_token = os.environ.get("GITHUB_TOKEN")

    return llm_provider, llm_api_key, llm_model, github_token


def save_config(llm_provider: str, llm_api_key: str, llm_model: str, github_token: str):
    """保存配置"""
    config_dir = Path.home() / ".github-optimizer"
    config_dir.mkdir(parents=True, exist_ok=True)

    config_path = config_dir / ".env"
    with open(config_path, 'w') as f:
        f.write(f"LLM_PROVIDER={llm_provider}\n")
        f.write(f"LLM_API_KEY={llm_api_key}\n")
        if llm_model:
            f.write(f"LLM_MODEL={llm_model}\n")
        f.write(f"GITHUB_TOKEN={github_token}\n")

    print(f"配置已保存到 {config_path}")


def show_config_status():
    """显示配置状态"""
    llm_provider, llm_api_key, llm_model, github_token = load_config()

    if llm_api_key and github_token:
        click.echo("✓ 配置已完成")
        click.echo(f"  LLM Provider: {llm_provider}")
        if llm_model:
            click.echo(f"  LLM Model: {llm_model}")
        else:
            provider_config = PROVIDER_CONFIGS.get(LLMProvider(llm_provider), {})
            default_model = provider_config.get("default_model", "unknown")
            click.echo(f"  LLM Model: {default_model} (默认)")
        click.echo(f"  LLM API Key: {llm_api_key[:8]}...")
        click.echo(f"  GitHub Token: {github_token[:8]}...")
    else:
        click.echo("✗ 尚未配置，请运行: python main.py setup --setup")


@click.group()
def cli():
    """GitHub 项目优化器 - 一键优化你的 GitHub 项目"""
    pass


@cli.command()
def providers():
    """显示支持的 LLM 提供商"""
    click.echo("=== 支持的 LLM 提供商 ===\n")

    for info in list_providers():
        click.echo(f"[{info['id']}] {info['name']}")
        click.echo(f"    默认模型: {info['default']}")
        click.echo(f"    可用模型: {', '.join(info['models'][:3])}...")
        click.echo("")


@cli.command()
@click.option("--setup", is_flag=True, help="配置 API Key")
def setup(setup):
    """首次配置 API Key"""
    if not setup:
        show_config_status()
        return

    click.echo("=== GitHub 项目优化器配置 ===\n")
    click.echo("支持的 LLM 提供商:\n")

    for info in list_providers():
        click.echo(f"  [{info['id']}] {info['name']}")

    click.echo("")

    # 选择 provider
    provider_choices = [info['id'] for info in list_providers()]
    provider = click.prompt(
        "请选择 LLM 提供商 (输入编号)",
        type=click.Choice(provider_choices),
        default="deepseek"
    )

    provider_config = PROVIDER_CONFIGS[LLMProvider(provider)]
    click.echo(f"\n已选择: {provider_config['name']}")
    click.echo(f"默认模型: {provider_config['default_model']}")

    model = click.prompt(
        f"请输入模型名称 (直接回车使用默认: {provider_config['default_model']})",
        default=""
    )
    if not model:
        model = provider_config['default_model']

    click.echo(f"使用模型: {model}")

    click.echo("\n请获取 API Key:")
    if provider == "openai":
        click.echo("  https://platform.openai.com/api-keys")
    elif provider == "deepseek":
        click.echo("  https://platform.deepseek.com/api_keys")
    elif provider == "zhipu":
        click.echo("  https://open.bigmodel.cn/usercenter/apikeys")
    elif provider == "ali":
        click.echo("  https://dashscope.console.aliyun.com/api-key")
    elif provider == "baidu":
        click.echo("  https://console.bce.baidu.com/qianfan/ais/console/applicationConsole/application")
    elif provider == "minimax":
        click.echo("  https://platform.minimax.chat/user-center/basic-information/interface-key")
    elif provider == "siliconflow":
        click.echo("  https://account.siliconflow.cn/api-keys")
    elif provider == "groq":
        click.echo("  https://console.groq.com/keys")
    elif provider == "gemini":
        click.echo("  https://aistudio.google.com/app/apikey")

    llm_api_key = click.prompt("请输入 LLM API Key")

    click.echo("\n请获取 GitHub Token:")
    click.echo("  https://github.com/settings/tokens")
    click.echo("  需要 repo 全部权限")
    github_token = click.prompt("请输入 GitHub Token")

    save_config(provider, llm_api_key, model, github_token)
    click.echo("\n✓ 配置完成！")


def prompt_apply_code_changes(code_changes: list) -> bool:
    """询问用户是否应用代码改动"""
    if not code_changes:
        return False

    click.echo("\n有代码改动待确认，请选择:")
    click.echo("  y - 全部应用代码改动")
    click.echo("  n - 跳过，不应用代码改动")
    click.echo("  q - 退出")

    while True:
        choice = click.prompt("请输入 (y/n/q)", default="n", show_default=False)
        if choice.lower() in ['y', 'yes']:
            return True
        elif choice.lower() in ['n', 'no']:
            return False
        elif choice.lower() == 'q':
            click.echo("已退出")
            sys.exit(0)


@cli.command()
@click.option("--repo", required=True, help="GitHub 仓库 URL 或本地路径")
@click.option("--local", is_flag=True, help="本地仓库模式")
@click.option("--dry-run", is_flag=True, help="预览模式，不提交更改")
@click.option("--no-merge", is_flag=True, help="只创建 PR，不自动合并")
@click.option("--provider", help="指定 LLM 提供商")
@click.option("--model", help="指定 LLM 模型")
@click.option("--lang", type=click.Choice(["chinese", "english"]), default="chinese", help="README 语言")
def optimize(repo: str, local: bool, dry_run: bool, no_merge: bool, provider: str, model: str, lang: str):
    """优化 GitHub 项目"""

    # 加载配置
    config_provider, llm_api_key, config_model, github_token = load_config()

    # 命令行参数优先
    provider = provider or config_provider
    model = model or config_model

    if not llm_api_key or not github_token:
        click.echo("✗ 尚未配置 API Key，请先运行: python main.py setup --setup")
        sys.exit(1)

    if not provider:
        provider = "deepseek"  # 默认

    try:
        # 初始化优化器
        optimizer = GitHubOptimizer(provider, llm_api_key, model, github_token, readme_lang=lang)
        optimizer.setup()

        click.echo("=== GitHub 项目优化器 ===\n")
        click.echo(f"LLM: {provider} / {optimizer.model}")
        click.echo(f"README: {lang}\n")

        # 克隆或打开仓库
        if local:
            click.echo(f"正在打开本地仓库: {repo}")
            repo_path = optimizer.clone_local_repo(repo)
        else:
            click.echo(f"正在克隆仓库: {repo}")
            repo_path = optimizer.clone_repo(repo)

        click.echo(f"✓ 仓库已准备: {repo_path}\n")

        # 分析项目结构
        click.echo("正在分析项目结构...")
        project_info = optimizer.analyze_project_structure()
        click.echo(f"✓ 项目语言: {project_info['language']}")
        click.echo(f"✓ 文件数量: {len(project_info['files'])}")
        click.echo(f"✓ 已有 README: {'是' if project_info['readme_exists'] else '否'}\n")

        # 备份
        click.echo("正在备份当前状态...")
        backup_path = optimizer.backup_current_state()
        click.echo(f"✓ 备份已保存: {backup_path}\n")

        # 读取代码和 README
        click.echo("正在读取项目代码...")
        code_content = optimizer.read_all_code_files()
        existing_readme = optimizer.read_readme()
        click.echo(f"✓ 已读取 {len(code_content)} 字符的代码\n")

        # 使用 LLM 优化
        result = optimizer.optimize_with_llm(project_info, code_content, existing_readme)
        click.echo("✓ LLM 分析完成\n")

        # 显示优化摘要
        click.echo("=== 优化摘要 ===")
        click.echo(result.get("summary", "优化完成"))
        click.echo("")

        # 处理代码改动
        code_changes = result.get("code_changes", [])
        if code_changes:
            optimizer.preview_code_changes(code_changes)

            if dry_run:
                click.echo("\n=== 预览模式 ===")
                click.echo("生成的 README 预览:")
                click.echo("-" * 40)
                click.echo(result.get("readme_content", "")[:1000])
                click.echo("-" * 40)
                click.echo("\n✓ 预览完成，如需应用请去掉 --dry-run 参数")
                return

            # 询问用户是否应用代码改动
            apply_code = prompt_apply_code_changes(code_changes)
            if apply_code:
                click.echo("正在应用代码改动...")
                optimizer.apply_code_changes(code_changes)
                click.echo("✓ 代码改动已应用\n")
        else:
            click.echo("没有检测到需要应用的代码改动\n")

        # 保存新的 README
        click.echo("正在保存 README...")
        optimizer.save_readme(result.get("readme_content", ""))
        click.echo("✓ README 已保存\n")

        # 提交并推送
        click.echo("正在提交更改...")
        branch_name = optimizer.commit_and_push()

        if branch_name:
            click.echo(f"✓ 已创建分支: {branch_name}\n")

            # 创建 PR
            click.echo("正在创建 Pull Request...")
            pr = optimizer.create_pull_request(branch_name)

            if pr:
                click.echo(f"✓ PR 创建成功: {pr.html_url}\n")

                # 自动合并（除非指定 --no-merge）
                if not no_merge:
                    click.echo("正在合并 Pull Request...")
                    if optimizer.merge_pull_request(pr.html_url):
                        click.echo("✓ PR 已合并！")
                    else:
                        click.echo("✗ 合并失败，请手动合并")
                else:
                    click.echo("（使用 --no-merge 跳过自动合并）")

        # 清理
        optimizer.cleanup()

        click.echo("\n=== 优化完成 ===")
        click.echo(f"备份位置: {backup_path}")
        if not dry_run and not no_merge:
            click.echo("✓ 项目已自动优化并合并！")

    except Exception as e:
        click.echo(f"\n✗ 错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


@cli.command()
def version():
    """显示版本信息"""
    click.echo("GitHub Optimizer v1.0.0")


if __name__ == "__main__":
    cli()
