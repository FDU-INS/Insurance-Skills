"""Tests for healthsim.config module."""

import io
import logging

from healthsim.config import HealthSimSettings, setup_logging


class TestHealthSimSettings:
    """Tests for HealthSimSettings."""

    def test_default_values(self) -> None:
        """Test default settings values."""
        settings = HealthSimSettings()

        assert settings.app_name == "healthsim"
        assert settings.debug is False
        assert settings.log_level == "INFO"
        assert settings.random_seed is None
        assert settings.locale == "en_US"

    def test_custom_values(self) -> None:
        """Test custom settings values."""
        settings = HealthSimSettings(
            app_name="myapp",
            debug=True,
            log_level="DEBUG",
            random_seed=42,
            locale="en_GB",
        )

        assert settings.app_name == "myapp"
        assert settings.debug is True
        assert settings.log_level == "DEBUG"
        assert settings.random_seed == 42
        assert settings.locale == "en_GB"

    def test_extra_fields_allowed(self) -> None:
        """Test that extra fields are allowed for extension."""
        settings = HealthSimSettings(custom_field="value")
        assert settings.custom_field == "value"


class TestSetupLogging:
    """Tests for setup_logging function."""

    def test_returns_logger(self) -> None:
        """Test that setup_logging returns a logger."""
        logger = setup_logging(app_name="test_app")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_app"

    def test_log_level(self) -> None:
        """Test that log level is set correctly."""
        logger = setup_logging(level="DEBUG", app_name="debug_app")
        assert logger.level == logging.DEBUG

        logger = setup_logging(level="WARNING", app_name="warn_app")
        assert logger.level == logging.WARNING

    def test_custom_stream(self) -> None:
        """Test logging to custom stream."""
        stream = io.StringIO()
        logger = setup_logging(level="INFO", app_name="stream_test", stream=stream)

        logger.info("Test message")
        output = stream.getvalue()

        assert "Test message" in output
        assert "stream_test" in output

    def test_custom_format(self) -> None:
        """Test custom format string."""
        stream = io.StringIO()
        logger = setup_logging(
            level="INFO",
            app_name="format_test",
            stream=stream,
            format_string="%(levelname)s: %(message)s",
        )

        logger.info("Custom format test")
        output = stream.getvalue()

        assert "INFO: Custom format test" in output
