# Codex CLI と Agents SDK でワークフローを安定化する

開発者は常に一貫性を求めます。Codex CLI と Agents SDK を組み合わせることで、その一貫性を大規模に拡張できます。大規模なリファクタリング、新機能の展開、新しいテスト体制の導入など、Codex は CLI・IDE・クラウドの各ワークフローとシームレスに統合され、再現性のある開発パターンを自動化します。

このガイドでは、Codex CLI を Model Context Protocol (MCP) サーバーとして公開し、Agents SDK で単体および複数エージェントのシステムを構築する方法を解説します。読み終えるころには次の内容を理解できます。

- Codex CLI を MCP サーバーとして初期化する方法。
- 限定的なタスクに Codex を割り当てる単一エージェントのワークフローを構築する方法。
- 役割間のゲート制御を導入した複数エージェントのワークフローを調整する方法。
- ツール呼び出しやハンドオフを追跡して、エージェントの挙動を可視化する方法。

## 事前準備

開始する前に、次の準備が整っていることを確認してください。

- Python と JavaScript の基本的な知識。
- VS Code や Cursor などの開発環境。
- `OPENAI_API_KEY` 環境変数から参照できる OpenAI API キー。

作業ディレクトリに `.env` ファイルを作成し、次のように設定します。

```bash
OPENAI_API_KEY="sk-..."
```

依存関係は `pip`（または `uv` を使用している場合は `uv pip`）でインストールします。

```bash
pip install openai-agents openai
```

## Codex CLI を MCP サーバーとして起動する

Codex CLI は常駐する MCP サーバーとして実行できます。以下のコードは `npx` 経由で Codex CLI を起動し、長時間のタスクでも完了できるよう最大 100 時間接続を維持します。

```python
import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

async def main() -> None:
    async with MCPServerStdio(
        name="Codex CLI",
        params={
            "command": "npx",
            "args": ["-y", "codex", "mcp"],
        },
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        print("Codex MCP server started.")
        # ここにエージェントの処理を追加します。
        return

if __name__ == "__main__":
    asyncio.run(main())
```

## 単一エージェントのワークフローを構築する

まずは 2 つの役割を持つ軽量なシステムから始めます。

1. **ゲームデザイナー** — シンプルなブラウザゲームの短いブリーフを作成します。
2. **ゲーム開発者** — デザイナーの依頼に沿ってゲームを実装します。

開発者エージェントは Codex MCP を利用して、承認なしに作業ディレクトリへファイルを書き込みます。

```python
developer_agent = Agent(
    name="Game Developer",
    instructions=(
        "You are an expert in building simple games using basic html + css + javascript with no dependencies. "
        "Save your work in a file called index.html in the current directory."
        "Always call codex with \"approval-policy\": \"never\" and \"sandbox\": \"workspace-write\""
    ),
    mcp_servers=[codex_mcp_server],
)

designer_agent = Agent(
    name="Game Designer",
    instructions=(
        "You are an indie game connoisseur. Come up with an idea for a single page html + css + javascript game that a developer could build in about 50 lines of code. "
        "Format your request as a 3 sentence design brief for a game developer and call the Game Developer coder with your idea."
    ),
    model="gpt-5",
    handoffs=[developer_agent],
)

result = await Runner.run(designer_agent, "Implement a fun new game!")
```

スクリプトを実行すると `index.html` が生成され、完成したゲームをブラウザで確認できます。

次の完全な例では `.env` から認証情報を読み込み、Codex CLI を初期化したうえで、デザイナーから開発者へのワークフローを実行します。

```python
import os
from dotenv import load_dotenv
import asyncio
from agents import Agent, Runner, set_default_openai_api
from agents.mcp import MCPServerStdio

load_dotenv(override=True)
set_default_openai_api(os.getenv("OPENAI_API_KEY"))

async def main() -> None:
    async with MCPServerStdio(
        name="Codex CLI",
        params={
            "command": "npx",
            "args": ["-y", "codex", "mcp"],
        },
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        developer_agent = Agent(
            name="Game Developer",
            instructions=(
                "You are an expert in building simple games using basic html + css + javascript with no dependencies. "
                "Save your work in a file called index.html in the current directory."
                "Always call codex with \"approval-policy\": \"never\" and \"sandbox\": \"workspace-write\""
            ),
            mcp_servers=[codex_mcp_server],
        )

        designer_agent = Agent(
            name="Game Designer",
            instructions=(
                "You are an indie game connoisseur. Come up with an idea for a single page html + css + javascript game that a developer could build in about 50 lines of code. "
                "Format your request as a 3 sentence design brief for a game developer and call the Game Developer coder with your idea."
            ),
            model="gpt-5",
            handoffs=[developer_agent],
        )

        result = await Runner.run(designer_agent, "Implement a fun new game!")

if __name__ == "__main__":
    try:
        asyncio.get_running_loop()
        await main()
    except RuntimeError:
        asyncio.run(main())
```

## 複数エージェントのワークフローを調整する

より大きなワークフローでは、役割を細分化したチームを構成します。

- **プロジェクトマネージャー** — タスクを分解し、要件をまとめ、進行を管理します。
- **デザイナー** — UI/UX 仕様を作成します。
- **フロントエンド開発者** — UI/UX を実装します。
- **バックエンド開発者** — API とロジックを実装します。
- **テスター** — 成果物を受け入れ条件と照合します。

プロジェクトマネージャーは、各専門エージェントにハンドオフする前に成果物の存在を確認するゲート制御を行います。これは JIRA や QA 承認などの現実的なワークフローに近い構成です。

まずは Codex CLI MCP サーバーを単一エージェントの例と同様に初期化します。

```python
async def main() -> None:
    async with MCPServerStdio(
        name="Codex CLI",
        params={
            "command": "npx",
            "args": ["-y", "codex", "mcp"],
        },
        client_session_timeout_seconds=360000,
    ) as codex_mcp_server:
        print("Codex MCP server started.")
        # ここに複数エージェントの構築を追加します。
        return
```

次に、各専門エージェントを定義し Codex MCP サーバーへアクセス権を与えます。`RECOMMENDED_PROMPT_PREFIX` を各エージェントへ渡し、ハンドオフを最適化します。

```python
# 下流のエージェントを先に定義してから、PM が handoffs で参照します。
designer_agent = Agent(
    name="Designer",
    instructions=(
        f"""{RECOMMENDED_PROMPT_PREFIX}"""
        "You are the Designer.\n"
        "Your only source of truth is AGENT_TASKS.md and REQUIREMENTS.md from the Project Manager.\n"
        "Do not assume anything that is not written there.\n\n"
        "You may use the internet for additional guidance or research."
        "Deliverables (write to /design):\n"
        "- design_spec.md – a single page describing the UI/UX layout, main screens, and key visual notes as requested in AGENT_TASKS.md.\n"
        "- wireframe.md – a simple text or ASCII wireframe if specified.\n\n"
        "Keep the output short and implementation-friendly.\n"
        "When complete, handoff to the Project Manager with transfer_to_project_manager_agent."
        "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."
    ),
    model="gpt-5",
    tools=[WebSearchTool()],
    mcp_servers=[codex_mcp_server],
    handoffs=[],
)

frontend_developer_agent = Agent(
    name="Frontend Developer",
    instructions=(
        f"""{RECOMMENDED_PROMPT_PREFIX}"""
        "You are the Frontend Developer.\n"
        "Read AGENT_TASKS.md and design_spec.md. Implement exactly what is described there.\n\n"
        "Deliverables (write to /frontend):\n"
        "- index.html – main page structure\n"
        "- styles.css or inline styles if specified\n"
        "- main.js or game.js if specified\n\n"
        "Follow the Designer’s DOM structure and any integration points given by the Project Manager.\n"
        "Do not add features or branding beyond the provided documents.\n\n"
        "When complete, handoff to the Project Manager with transfer_to_project_manager_agent."
        "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."
    ),
    model="gpt-5",
    mcp_servers=[codex_mcp_server],
    handoffs=[],
)

backend_developer_agent = Agent(
    name="Backend Developer",
    instructions=(
        f"""{RECOMMENDED_PROMPT_PREFIX}"""
        "You are the Backend Developer.\n"
        "Read AGENT_TASKS.md and REQUIREMENTS.md. Implement the backend endpoints described there.\n\n"
        "Deliverables (write to /backend):\n"
        "- package.json – include a start script if requested\n"
        "- server.js – implement the API endpoints and logic exactly as specified\n\n"
        "Keep the code as simple and readable as possible. No external database.\n\n"
        "When complete, handoff to the Project Manager with transfer_to_project_manager_agent."
        "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."
    ),
    model="gpt-5",
    mcp_servers=[codex_mcp_server],
    handoffs=[],
)

tester_agent = Agent(
    name="Tester",
    instructions=(
        f"""{RECOMMENDED_PROMPT_PREFIX}"""
        "You are the Tester.\n"
        "Read AGENT_TASKS.md and TEST.md. Verify that the outputs of the other roles meet the acceptance criteria.\n\n"
        "Deliverables (write to /tests):\n"
        "- TEST_PLAN.md – bullet list of manual checks or automated steps as requested\n"
        "- test.sh or a simple automated script if specified\n\n"
        "Keep it minimal and easy to run.\n\n"
        "When complete, handoff to the Project Manager with transfer_to_project_manager_agent."
        "When creating files, call Codex MCP with {\"approval-policy\":\"never\",\"sandbox\":\"workspace-write\"}."
    ),
    model="gpt-5",
    mcp_servers=[codex_mcp_server],
    handoffs=[],
)
```

各役割が成果物を作成したら `transfer_to_project_manager_agent` でプロジェクトマネージャーへ返し、必要なファイルが揃っているか検証します。

プロジェクトマネージャーは初期プロンプトを受け取り、プロジェクト直下にある計画ファイルを作成し、すべてのゲートロジックを制御します。

```python
project_manager_agent = Agent(
    name="Project Manager",
    instructions=(
        f"""{RECOMMENDED_PROMPT_PREFIX}"""
        """
        You are the Project Manager.

        Objective:
        Convert the input task list into three project-root files the team will execute against.

        Deliverables (write in project root):
        - REQUIREMENTS.md: concise summary of product goals, target users, key features, and constraints.
        - TEST.md: tasks with [Owner] tags (Designer, Frontend, Backend, Tester) and clear acceptance criteria.
        - AGENT_TASKS.md: one section per role containing:
          - Project name
          - Required deliverables (exact file names and purpose)
          - Key technical notes and constraints

        Process:
        - Resolve ambiguities with minimal, reasonable assumptions. Be specific so each role can act without guessing.
        - Create files using Codex MCP with {"approval-policy":"never","sandbox":"workspace-write"}.
        - Do not create folders. Only create REQUIREMENTS.md, TEST.md, AGENT_TASKS.md.

        Handoffs (gated by required files):
        1) After the three files above are created, hand off to the Designer with transfer_to_designer_agent and include REQUIREMENTS.md, and AGENT_TASKS.md.
        2) Wait for the Designer to produce /design/design_spec.md. Verify that file exists before proceeding.
        3) When design_spec.md exists, hand off in parallel to both:
           - Frontend Developer with transfer_to_frontend_developer_agent (provide design_spec.md, REQUIREMENTS.md, AGENT_TASKS.md).
           - Backend Developer with transfer_to_backend_developer_agent (provide REQUIREMENTS.md, AGENT_TASKS.md).
        4) Wait for Frontend to produce /frontend/index.html and Backend to produce /backend/server.js. Verify both files exist.
        5) When both exist, hand off to the Tester with transfer_to_tester_agent and provide all prior artifacts and outputs.
        6) Do not advance to the next handoff until the required files for that step are present. If something is missing, request the owning agent to supply it and re-check.

        PM Responsibilities:
        - Coordinate all roles, track file completion, and enforce the above gating checks.
        - Do NOT respond with status updates. Just handoff to the next agent until the project is complete.
        """
    ),
    model="gpt-5",
    model_settings=ModelSettings(
        reasoning=Reasoning(effort="medium")
    ),
    handoffs=[designer_agent, frontend_developer_agent, backend_developer_agent, tester_agent],
    mcp_servers=[codex_mcp_server],
)
```

最後に、各専門エージェントの `handoffs` をプロジェクトマネージャーへ戻すよう設定します。

```python
designer_agent.handoffs = [project_manager_agent]
frontend_developer_agent.handoffs = [project_manager_agent]
backend_developer_agent.handoffs = [project_manager_agent]
tester_agent.handoffs = [project_manager_agent]
```

プロジェクトマネージャーが処理するタスクリストの例を以下に示します。

```python
task_list = """
Goal: Build a tiny browser game to showcase a multi-agent workflow.

High-level requirements:
- Single-screen game called "Bug Busters".
- Player clicks a moving bug to earn points.
- Game ends after 20 seconds and shows final score.
- Optional: submit score to a simple backend and display a top-10 leaderboard.

Roles:
- Designer: create a one-page UI/UX spec and basic wireframe.
- Frontend Developer: implement the page and game logic.
- Backend Developer: implement a minimal API (GET /health, GET/POST /scores).
- Tester: write a quick test plan and a simple script to verify core routes.

Constraints:
- No external database—memory storage is fine.
- Keep everything readable for beginners; no frameworks required.
- All outputs should be small files saved in clearly named folders.
"""
```

システムを実行すると、数分でエージェントが連携して成果物を生成します。実行後は以下のようなファイル構成が作成されます。

```text
root_directory/
├── AGENT_TASKS.md
├── REQUIREMENTS.md
├── backend
│   ├── package.json
│   └── server.js
├── design
│   ├── design_spec.md
│   └── wireframe.md
├── frontend
│   ├── game.js
│   ├── index.html
│   └── styles.css
└── TEST.md
```

`node server.js` でバックエンドを起動し、`index.html` を開いてゲームをプレイできます。

## Traces でエージェントの挙動を追跡する

ワークフローが複雑になるほど、エージェント同士のやり取りを可視化することが重要です。Traces ダッシュボードでは次の情報を確認できます。

- プロンプト、ツール呼び出し、エージェント間ハンドオフ。
- MCP サーバー呼び出し、Codex CLI 呼び出し、実行時間、ファイル書き込み。
- エラーや警告。

トレースを確認すると、プロジェクトマネージャーが成果物の存在を確認しながらハンドオフを進めていることや、Codex MCP サーバーを通じて生成したアーティファクトを Responses API 経由で取得していることがわかります。タイムラインバーから各ステップの実行時間を比較でき、ボトルネックの検出や制御の流れの把握に役立ちます。

各トレースをクリックすると、プロンプト・ツール呼び出し・メタデータの詳細が表示されます。履歴を蓄積すれば、将来的なチューニングや最適化、評価にも活用できます。

## まとめ

このガイドでは、Codex CLI と Agents SDK を組み合わせて、再現性が高くスケールするワークフローを構築する方法を紹介しました。主なポイントは次のとおりです。

- **Codex MCP サーバーのセットアップ** — Codex CLI を MCP サーバーとして初期化し、エージェントのツールとして利用する手順。
- **単一エージェントの例** — デザイナーと開発者によるシンプルなワークフローで Codex を限定的なタスクに活用する方法。
- **複数エージェントのオーケストレーション** — プロジェクトマネージャーを中心に役割を分担し、ゲート制御で成果物を検証しながら進める方法。
- **Traces と可観測性** — プロンプトやツール呼び出し、ハンドオフ、実行時間、成果物を記録し、エージェントの挙動を可視化する手段。

これらの手法を応用し、実際のプロジェクトでも Codex MCP と Agents SDK を活用してみてください。
