import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from examples.basic import run_agent_example
from examples.model_providers.local_dummy_provider import DummyProvider
from agents import RunConfig

def test_main_calls_runner_and_prints_final_output():
    dummy_result = SimpleNamespace(final_output="Test tip: keep tests small.")
    runner_mock = AsyncMock(return_value=dummy_result)

    with patch("examples.basic.run_agent_example.Runner.run", runner_mock):
        with patch("builtins.print") as mock_print:
            asyncio.run(run_agent_example.main())

    runner_mock.assert_awaited_once()
    args, kwargs = runner_mock.call_args
    # prompt is the second positional argument
    assert args[1] == "What's a quick tip for writing tests?"
    assert "run_config" in kwargs
    assert isinstance(kwargs["run_config"].model_provider, DummyProvider)

    mock_print.assert_any_call("Final output:")
    mock_print.assert_any_call(dummy_result.final_output)


def test_main_creates_agent_with_expected_attrs():
    runner_mock = AsyncMock(return_value=SimpleNamespace(final_output="ok"))

    with patch("examples.basic.run_agent_example.Runner.run", runner_mock):
        with patch("builtins.print"):
            asyncio.run(run_agent_example.main())

    args, _ = runner_mock.call_args
    agent_passed = args[0]
    assert getattr(agent_passed, "name") == "LocalAssistant"
    assert getattr(agent_passed, "instructions") == "You respond concisely and politely."
    def test_main_calls_runner_and_prints_final_output():
        dummy_result = SimpleNamespace(final_output="Test tip: keep tests small.")
        runner_mock = AsyncMock(return_value=dummy_result)

        with patch("examples.basic.run_agent_example.Runner.run", runner_mock):
            with patch("builtins.print") as mock_print:
                asyncio.run(run_agent_example.main())

        runner_mock.assert_awaited_once()
        args, kwargs = runner_mock.call_args
        # prompt is the second positional argument
        assert args[1] == "What's a quick tip for writing tests?"
        assert "run_config" in kwargs
        assert isinstance(kwargs["run_config"].model_provider, DummyProvider)

        mock_print.assert_any_call("Final output:")
        mock_print.assert_any_call(dummy_result.final_output)


    def test_main_creates_agent_with_expected_attrs():
        runner_mock = AsyncMock(return_value=SimpleNamespace(final_output="ok"))

        with patch("examples.basic.run_agent_example.Runner.run", runner_mock):
            with patch("builtins.print"):
                asyncio.run(run_agent_example.main())

        args, _ = runner_mock.call_args
        agent_passed = args[0]
        assert getattr(agent_passed, "name") == "LocalAssistant"
        assert getattr(agent_passed, "instructions") == "You respond concisely and politely."


    def test_main_prints_exactly_two_lines_in_order():
        dummy_result = SimpleNamespace(final_output="Another tip.")
        runner_mock = AsyncMock(return_value=dummy_result)

        with patch("examples.basic.run_agent_example.Runner.run", runner_mock):
            with patch("builtins.print") as mock_print:
                asyncio.run(run_agent_example.main())

        assert mock_print.call_count == 2
        first_call_arg = mock_print.call_args_list[0][0][0]
        second_call_arg = mock_print.call_args_list[1][0][0]
        assert first_call_arg == "Final output:"
        assert second_call_arg == dummy_result.final_output


    def test_main_passes_runconfig_instance_and_provider_type():
        dummy_result = SimpleNamespace(final_output="ok")
        runner_mock = AsyncMock(return_value=dummy_result)

        with patch("examples.basic.run_agent_example.Runner.run", runner_mock):
            with patch("builtins.print"):
                asyncio.run(run_agent_example.main())

        _, kwargs = runner_mock.call_args
        assert "run_config" in kwargs
        assert isinstance(kwargs["run_config"], RunConfig)
        assert isinstance(kwargs["run_config"].model_provider, DummyProvider)
