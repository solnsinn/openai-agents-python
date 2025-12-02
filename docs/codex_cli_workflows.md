# Building Consistent Workflows with Codex CLI and the Agents SDK

Developers strive for consistency in everything they do. With Codex CLI and the Agents SDK, that consistency can now scale like never before. Whether you are refactoring a large codebase, rolling out new features, or introducing a new testing framework, Codex integrates seamlessly into CLI, IDE, and cloud workflows to automate and enforce repeatable development patterns.

This guide walks through building both single and multi-agent systems using the Agents SDK with Codex CLI exposed as a Model Context Protocol (MCP) server. By the end you will understand how to:

- Initialize Codex CLI as an MCP server.
- Build single-agent workflows that scope Codex to focused tasks.
- Orchestrate multi-agent projects with explicit gating between roles.
- Trace agentic behavior to understand tooling calls and handoffs.

## Prerequisites

Before you begin, ensure you have:

- Basic familiarity with Python and JavaScript.
- A development environment such as VS Code or Cursor.
- An OpenAI API key available via the `OPENAI_API_KEY` environment variable.

Create a `.env` file in your working directory and add the following line:

```bash
OPENAI_API_KEY="sk-..."
```

Install the dependencies with `pip` (or `uv pip` if you are using `uv`):

```bash
pip install openai-agents openai
```

## Initialize Codex CLI as an MCP Server

Codex CLI can run as a long-lived MCP server. The snippet below launches Codex CLI via `npx` and keeps the MCP connection alive for up to 100 hours so Codex has time to complete long-running tasks.

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
        # Add agent code here.
        return

if __name__ == "__main__":
    asyncio.run(main())
```

## Build a Single-Agent Workflow

Start with a lightweight system containing two roles:

1. **Game Designer** – writes a short creative brief for a simple browser game.
2. **Game Developer** – implements the game according to the designer’s request.

The developer agent uses Codex MCP to write files directly to the working directory without interactive approval.

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

Running the script generates an `index.html` file that contains the complete game. Open the file in your browser and play the result produced by the agents.

The full example below loads credentials from `.env`, initializes Codex CLI, and executes the designer-to-developer workflow:

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
        # print(result.final_output)

if __name__ == "__main__":
    try:
        asyncio.get_running_loop()
        await main()
    except RuntimeError:
        asyncio.run(main())
```

> **Note:** When running inside Jupyter, use `await main()` to avoid the "asyncio.run() cannot be called from a running event loop" error.

## Orchestrate Multi-Agent Workflows

To scale up, introduce a complete delivery team with explicit gating logic managed by a Project Manager agent:

- **Project Manager** – produces shared planning artifacts, validates deliverables, and coordinates handoffs.
- **Designer** – generates design specifications.
- **Frontend Developer** – implements the UI and game logic.
- **Backend Developer** – provides supporting APIs.
- **Tester** – confirms everything meets acceptance criteria.

The Project Manager uses `transfer_to_*` handoff calls only after required files exist, mirroring enterprise workflows that depend on gated approvals.

### Configure the Codex MCP server

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
        # Define agents here.
        return
```

### Define the specialized agents

Each agent receives the `RECOMMENDED_PROMPT_PREFIX` helper and instructions to call Codex MCP with non-interactive approval when creating files.

```python
# Downstream agents are defined first for clarity.
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

### Define the Project Manager

The Project Manager is the only agent that receives the initial prompt. It generates planning artifacts, enforces gating, and coordinates the specialist roles.

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

# Ensure every specialist hands back to the PM when done.
designer_agent.handoffs = [project_manager_agent]
frontend_developer_agent.handoffs = [project_manager_agent]
backend_developer_agent.handoffs = [project_manager_agent]
tester_agent.handoffs = [project_manager_agent]
```

### Provide the task list

The Project Manager receives a high-level task list and converts it into actionable artifacts:

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

With the agents wired up, execute the full workflow:

```python
result = await Runner.run(project_manager_agent, task_list, max_turns=30)
print(result.final_output)
```

The system produces the following project structure:

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

Start the backend with `node server.js`, open `frontend/index.html`, and you are ready to play the generated game.

## Trace Agentic Behavior

As your workflows grow more complex, use Traces to observe the full agentic call stack. The Traces dashboard captures:

- Prompts, tool invocations, and handoffs between agents.
- MCP server calls, Codex CLI executions, and file writes.
- Errors and warnings produced during the run.

Traces reveal how the Project Manager coordinates the specialists, which Codex commands ran, and how long each step took. Drill into individual trace spans to inspect prompts, responses, and metadata so you can tune and debug future runs.

## Recap and Next Steps

In this guide you:

- Initialized Codex CLI as an MCP server for long-running tasks.
- Built a single-agent workflow that paired a designer with a developer.
- Scaled the pattern to a multi-agent system with gated handoffs.
- Learned how Traces provide observability across the entire agentic lifecycle.

To take these ideas further:

1. **Scale to larger rollouts.** Apply gated multi-agent orchestration to framework migrations, large refactors, or documentation overhauls.
2. **Accelerate delivery with confidence.** Coordinate specialized agents in parallel while enforcing artifact validation to keep quality high.
3. **Integrate with existing tooling.** Connect MCP-powered agents to systems like Jira, GitHub, or CI/CD pipelines to automate end-to-end development workflows.

Codex MCP and the Agents SDK combine to deliver repeatable, auditable automation—ready for teams that demand consistency at scale.
