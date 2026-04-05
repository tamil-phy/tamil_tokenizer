"""Tests for CLI interface and output formats."""

import json
import subprocess
import sys
import pytest
from .benchmark_data import CLI_TEST_CASES


def run_cli(*args):
    """Helper to run the CLI and capture output."""
    cmd = [sys.executable, "-m", "tamil_tokenizer"] + list(args)
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=30,
        cwd=None,
    )
    return result


class TestCLI:
    """CLI interface tests."""

    @pytest.mark.parametrize(
        "args, expected_substr, description",
        CLI_TEST_CASES,
        ids=[c[2] for c in CLI_TEST_CASES],
    )
    def test_cli_output(self, args, expected_substr, description):
        result = run_cli(*args)
        combined = result.stdout + result.stderr
        assert expected_substr in combined, (
            f"[{description}] Expected '{expected_substr}' in output.\n"
            f"stdout: {result.stdout[:500]}\nstderr: {result.stderr[:500]}"
        )

    def test_cli_no_debug_noise_word(self):
        """Word tokenization should produce NO debug print output."""
        result = run_cli("அவன் வந்தான்.")
        noise_patterns = [
            "TamilRootWordParser loaded",
            "Loading configuration from",
            "Loaded ",
            "OuterList Size",
            "Error",
        ]
        for pattern in noise_patterns:
            assert pattern not in result.stdout, (
                f"Debug noise found in stdout: '{pattern}'"
            )

    def test_cli_no_debug_noise_morpheme(self):
        """Morpheme tokenization (heaviest path) should produce NO debug noise."""
        result = run_cli("பள்ளிக்கு சென்றான்.", "--level", "morpheme")
        noise_patterns = [
            "TamilRootWordParser loaded",
            "Loading configuration from",
            "OuterList Size",
            "totalCounter",
        ]
        for pattern in noise_patterns:
            assert pattern not in result.stdout, (
                f"Debug noise found in stdout: '{pattern}'"
            )
            assert pattern not in result.stderr, (
                f"Debug noise found in stderr: '{pattern}'"
            )

    def test_cli_json_valid(self):
        """JSON output must be valid JSON."""
        result = run_cli("அவன் வந்தான்.", "--format", "json")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        assert len(data) > 0
        assert "text" in data[0]
        assert "type" in data[0]

    def test_cli_json_morpheme_valid(self):
        """Morpheme JSON output must be valid and contain metadata."""
        result = run_cli("பள்ளிக்கு", "--level", "morpheme", "--format", "json")
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert isinstance(data, list)
        assert any(d["type"] == "root" for d in data)

    def test_cli_text_format(self):
        """Text format should produce one token per line."""
        result = run_cli("அவன் வந்தான்.", "--format", "text")
        assert result.returncode == 0
        lines = [l for l in result.stdout.strip().split("\n") if l.strip()]
        assert len(lines) == 3  # அவன் வந்தான் .

    def test_cli_table_format(self):
        """Table format should include token numbering and type."""
        result = run_cli("அவன் வந்தான்.", "--format", "table")
        assert result.returncode == 0
        assert "Tokens (" in result.stdout
        assert "word" in result.stdout

    def test_cli_no_args_shows_help(self):
        """Running without arguments should show help."""
        result = run_cli()
        combined = result.stdout + result.stderr
        assert "usage" in combined.lower() or "Tamil Tokenizer" in combined

    def test_cli_invalid_level(self):
        """Invalid level should produce an error."""
        result = run_cli("test", "--level", "invalid")
        assert result.returncode != 0

    def test_cli_all_levels_exit_zero(self):
        """All valid levels should exit with code 0."""
        for level in ["word", "character", "sentence", "morpheme"]:
            result = run_cli("அவன் வந்தான்.", "--level", level)
            assert result.returncode == 0, (
                f"Level '{level}' exited with code {result.returncode}"
            )

    def test_cli_all_formats_exit_zero(self):
        """All valid formats should exit with code 0."""
        for fmt in ["table", "text", "json"]:
            result = run_cli("அவன் வந்தான்.", "--format", fmt)
            assert result.returncode == 0, (
                f"Format '{fmt}' exited with code {result.returncode}"
            )
