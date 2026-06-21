from artifactgate_eda.cli import main


def test_version(capsys):
    assert main(["--version"]) == 0
    assert "0.1.0" in capsys.readouterr().out


def test_help(capsys):
    assert main([]) == 0
    assert "artifactgate" in capsys.readouterr().out

