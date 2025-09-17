import asyncio
import sys
from pathlib import Path

# Ensure the repository root is on sys.path so absolute imports like
# "from examples.model_providers..." work when running this file directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from agents import Agent, Runner, RunConfig

from examples.model_providers.local_dummy_provider import DummyProvider


async def main():
    # Minimal agent that adds a deterministic reply without calling external APIs.
    agent = Agent(
        name="LocalAssistant",
        instructions="You respond concisely and politely.",
    )

    # Run the agent with a simple prompt using the local dummy provider.
    result = await Runner.run(
        agent,
        "What's a quick tip for writing tests?",
        run_config=RunConfig(model_provider=DummyProvider()),
    )
    # The DummyProvider returns dict-shaped output items; the run result may not
    # populate `final_output`. Fall back to printing the raw response items when
    # `final_output` is empty so the example shows the dummy reply.
    if result.final_output:
        print("Final output:")
        print(result.final_output)
    else:
        print("Final output (from raw_responses):")
        for resp in result.raw_responses:
            for item in getattr(resp, "output", []):
                # The item might be a dict-like value, a pydantic model, or
                # an attribute-access object provided by local stubs. Handle
                # each case robustly.
                # 1) dict-like
                if isinstance(item, dict):
                    content = item.get("content") or []
                    for c in content:
                        if isinstance(c, dict) and c.get("text"):
                            print(c.get("text"))
                        else:
                            print(c)
                    continue

                # 2) pydantic model or object with attributes
                content = getattr(item, "content", None)
                if content is None:
                    print(item)
                    continue

                # content may be a list of pydantic models or dicts
                for c in content:
                    # pydantic model_dump or attribute access
                    text = None
                    if hasattr(c, "model_dump") and callable(getattr(c, "model_dump")):
                        dumped = c.model_dump()
                        if isinstance(dumped, dict):
                            text = dumped.get("text")
                    elif isinstance(c, dict):
                        text = c.get("text")
                    elif hasattr(c, "text"):
                        text = getattr(c, "text")

                    if text is not None:
                        print(text)
                    else:
                        print(c)


if __name__ == "__main__":
    asyncio.run(main())
