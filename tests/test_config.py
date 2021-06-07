from mnpolarity.config import config


def test_config():
    assert "data" in config
    assert "package_dir" in config
    assert "data_dir" in config
    assert "twint" in config
