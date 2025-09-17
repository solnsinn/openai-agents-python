import os
from pathlib import Path
import pytest
from agents import coding_automation_agent as caa

def test_generate_code_writes_file_and_returns_path(tmp_path, monkeypatch):
    # Point BASE_DIR to a temporary directory for isolation
    monkeypatch.setattr(caa, "BASE_DIR", tmp_path.resolve())
    agent = caa.CodingAutomationAgent()

    code = "print('hello')\n"
    filename = "hello.py"
    returned = agent.generate_code(code, filename)
    ret_path = Path(returned)

    assert ret_path.exists()
    assert ret_path.read_text(encoding="utf-8") == code
    # Ensure file is inside the patched BASE_DIR
    assert tmp_path.resolve() in ret_path.parent.resolve().parents or ret_path.parent.resolve() == tmp_path.resolve()


def test_generate_code_sanitizes_filename_and_allows_final_component(tmp_path, monkeypatch):
    monkeypatch.setattr(caa, "BASE_DIR", tmp_path.resolve())
    agent = caa.CodingAutomationAgent()

    code = "x = 1\n"
    # Provide a filename containing path traversal; only the final component should be used
    returned = agent.generate_code(code, "../trick.py")
    p = Path(returned)
    assert p.name == "trick.py"
    assert p.exists()
    assert p.read_text(encoding="utf-8") == code


def test_generate_code_rejects_invalid_filename(tmp_path, monkeypatch):
    monkeypatch.setattr(caa, "BASE_DIR", tmp_path.resolve())
    agent = caa.CodingAutomationAgent()

    with pytest.raises(ValueError):
        agent.generate_code("x", "")  # empty filename

    with pytest.raises(ValueError):
        agent.generate_code("x", "..")  # invalid name component


def test_generate_code_rejects_absolute_directory_outside_base(tmp_path, monkeypatch):
    # Set BASE_DIR to a temp dir, then try to write to an absolute directory outside it
    monkeypatch.setattr(caa, "BASE_DIR", tmp_path.resolve())
    agent = caa.CodingAutomationAgent()

    outside_dir = tmp_path.parent.resolve()  # guaranteed to be outside the BASE_DIR
    with pytest.raises(ValueError):
        agent.generate_code("x", "a.py", directory=str(outside_dir))


def test_scaffold_website_creates_index_html(tmp_path, monkeypatch):
    monkeypatch.setattr(caa, "BASE_DIR", tmp_path.resolve())
    agent = caa.CodingAutomationAgent()

    site_name = "example_site"
    site_path_str = agent.scaffold_website(site_name)
    site_path = Path(site_path_str)

    assert site_path.exists() and site_path.is_dir()
    index = site_path / "index.html"
    assert index.exists()
    content = index.read_text(encoding="utf-8")
    assert f"<title>{site_name}</title>" in content
    assert f"Welcome to {site_name}" in content


@pytest.mark.parametrize("bad_name", ["", ".", "..", "bad/name", "bad\\name"])
def test_scaffold_website_rejects_invalid_site_name(tmp_path, monkeypatch, bad_name):
    monkeypatch.setattr(caa, "BASE_DIR", tmp_path.resolve())
    agent = caa.CodingAutomationAgent()

    with pytest.raises(ValueError):
        agent.scaffold_website(bad_name)


def test_automate_task_returns_subprocess_returncode(monkeypatch):
    agent = caa.CodingAutomationAgent()

    class DummyResult:
        def __init__(self, code):
            self.returncode = code

    def fake_run(cmd, shell=True):
        return DummyResult(42)

    monkeypatch.setattr(caa.subprocess, "run", fake_run)
    assert agent.automate_task("echo hi") == 42


def test_automate_task_handles_run_exception(monkeypatch):
    agent = caa.CodingAutomationAgent()

    def fake_run_raises(cmd, shell=True):
        raise RuntimeError("boom")

    monkeypatch.setattr(caa.subprocess, "run", fake_run_raises)
    # On exception the method returns 1
    assert agent.automate_task("will fail") == 1


def test_repr_contains_name():
    agent = caa.CodingAutomationAgent(name="Tester")
    assert "CodingAutomationAgent" in repr(agent)
    assert "Tester" in repr(agent)

def test_automate_task_calls_run_with_shell_true_and_command(monkeypatch):
    agent = caa.CodingAutomationAgent()

    called = {}

    class DummyResult:
        def __init__(self, code):
            self.returncode = code

    def fake_run(cmd, shell=True):
        called["cmd"] = cmd
        called["shell"] = shell
        return DummyResult(0)

    monkeypatch.setattr(caa.subprocess, "run", fake_run)
    rc = agent.automate_task("echo 'hello world'")
    assert rc == 0
    assert called["cmd"] == "echo 'hello world'"
    assert called["shell"] is True

def test_scaffold_website_with_template_creates_index_html(tmp_path, monkeypatch):
    monkeypatch.setattr(caa, "BASE_DIR", tmp_path.resolve())
    agent = caa.CodingAutomationAgent()

    site_name = "templated_site"
    site_path_str = agent.scaffold_website(site_name, template="basic")
    site_path = Path(site_path_str)

    assert site_path.exists() and site_path.is_dir()
    index = site_path / "index.html"
    assert index.exists()
    content = index.read_text(encoding="utf-8")
    assert f"<title>{site_name}</title>" in content
    assert f"Welcome to {site_name}" in content
    # Ensure site directory is inside the patched BASE_DIR
    assert tmp_path.resolve() in site_path.resolve().parents or site_path.resolve().parent == tmp_path.resolve()

def test_scaffold_website_is_idempotent_and_preserves_existing_files(tmp_path, monkeypatch):
    monkeypatch.setattr(caa, "BASE_DIR", tmp_path.resolve())
    agent = caa.CodingAutomationAgent()

    site_name = "my_site"
    first = Path(agent.scaffold_website(site_name))
    # add an extra file to ensure subsequent scaffolding doesn't remove existing files
    extra = first / "extra.txt"
    extra.write_text("keep me", encoding="utf-8")

    second = Path(agent.scaffold_website(site_name))
    assert str(first.resolve()) == str(second.resolve())
    assert (second / "index.html").exists()
    assert extra.exists()
    def test_scaffold_website_returns_string_path_and_is_within_base(tmp_path, monkeypatch):
        monkeypatch.setattr(caa, "BASE_DIR", tmp_path.resolve())
        agent = caa.CodingAutomationAgent()

        site_name = "simple_site"
        returned = agent.scaffold_website(site_name)
        assert isinstance(returned, str)

        p = Path(returned)
        assert p.exists() and p.is_dir()
        # Ensure site directory is inside the patched BASE_DIR
        assert tmp_path.resolve() in p.resolve().parents or p.resolve().parent == tmp_path.resolve()

    def test_scaffold_website_allows_percent_encoded_names(tmp_path, monkeypatch):
        # Names that contain percent-encoded separators (e.g. "%2F") should be treated as literal characters
        monkeypatch.setattr(caa, "BASE_DIR", tmp_path.resolve())
        agent = caa.CodingAutomationAgent()

        site_name = "weird%2Fname"
        site_path_str = agent.scaffold_website(site_name)
        site_path = Path(site_path_str)
        assert site_path.exists() and site_path.is_dir()
        index = site_path / "index.html"
        assert index.exists()
        content = index.read_text(encoding="utf-8")
        assert f"<title>{site_name}</title>" in content

    def test_scaffold_website_rejects_site_name_with_actual_path_separator(tmp_path, monkeypatch):
        monkeypatch.setattr(caa, "BASE_DIR", tmp_path.resolve())
        agent = caa.CodingAutomationAgent()

        bad_name = f"bad{os.path.sep}name"
        with pytest.raises(ValueError):
            agent.scaffold_website(bad_name)




