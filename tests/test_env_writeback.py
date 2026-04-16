from pathlib import Path

from env_writer import append_env_var


def test_append_env_var_adds_new_line(tmp_path: Path):
    env = tmp_path / ".env"
    env.write_text("MNEMO_DSN=abc\n")

    append_env_var(env, "MEM9_TENANT_ID", "mnm_abc123")

    text = env.read_text()
    assert "MNEMO_DSN=abc" in text
    assert "MEM9_TENANT_ID=mnm_abc123" in text


def test_append_env_var_replaces_existing_line(tmp_path: Path):
    env = tmp_path / ".env"
    env.write_text("MNEMO_DSN=abc\nMEM9_TENANT_ID=OLD\n")

    append_env_var(env, "MEM9_TENANT_ID", "mnm_new")

    text = env.read_text()
    assert "MEM9_TENANT_ID=mnm_new" in text
    assert "MEM9_TENANT_ID=OLD" not in text
    assert text.count("MEM9_TENANT_ID=") == 1
