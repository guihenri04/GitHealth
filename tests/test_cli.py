from __future__ import annotations

from githealth.cli import app


def test_doctor_command_runs(runner, monkeypatch) -> None:
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "GITHUB_TOKEN configurado" in result.output


def test_analyze_rejects_invalid_repository(runner) -> None:
    result = runner.invoke(app, ["analyze", "not-a-repo"])
    assert result.exit_code == 1
    assert "Erro" in result.output

