"""Plugin registry for dimensional writers.

Writers are registered automatically when their packages are available.
This allows flexible deployment - install only what you need.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from healthsim.config.dimensional import TargetConfig
    from healthsim.dimensional.writers.base import BaseDimensionalWriter

logger = logging.getLogger(__name__)


class WriterRegistry:
    """Registry for dimensional writer plugins.

    Writers register themselves when imported. Only available writers
    (those with required packages installed) are usable.

    Usage:
        >>> # Get available targets
        >>> targets = WriterRegistry.list_available()
        >>>
        >>> # Get a writer class
        >>> writer_cls = WriterRegistry.get('databricks')
        >>>
        >>> # Create writer from config
        >>> writer = WriterRegistry.create_from_config(config)

    Class Methods:
        register: Register a new writer class.
        get: Get a writer class by name.
        list_available: List installed and available writers.
        create: Create a writer instance.
    """

    _writers: dict[str, type[BaseDimensionalWriter]] = {}

    @classmethod
    def register(cls, writer_class: type[BaseDimensionalWriter]) -> None:
        """Register a writer class.

        Args:
            writer_class: Writer class to register.

        Raises:
            ValueError: If writer class doesn't define TARGET_NAME.
        """
        name = writer_class.TARGET_NAME
        if not name:
            raise ValueError(f"Writer {writer_class} must define TARGET_NAME")

        cls._writers[name] = writer_class
        logger.debug(f"Registered writer: {name}")

    @classmethod
    def get(cls, target_name: str) -> type[BaseDimensionalWriter]:
        """Get a writer class by target name.

        Args:
            target_name: Name of target (e.g., 'duckdb', 'databricks').

        Returns:
            Writer class.

        Raises:
            ValueError: If target not registered or not available.
        """
        if target_name not in cls._writers:
            available = cls.list_available()
            raise ValueError(f"Unknown target '{target_name}'. Available: {available}")

        writer_class = cls._writers[target_name]

        if not writer_class.is_available():
            raise ValueError(
                f"Target '{target_name}' requires packages: "
                f"{writer_class.REQUIRED_PACKAGES}. "
                f"Install with: pip install healthsim-common[{target_name}]"
            )

        return writer_class

    @classmethod
    def list_registered(cls) -> list[str]:
        """List all registered writer names (may not all be available).

        Returns:
            List of registered target names.
        """
        return list(cls._writers.keys())

    @classmethod
    def list_available(cls) -> list[str]:
        """List writer names that are installed and available.

        Returns:
            List of available target names.
        """
        return [name for name, writer_class in cls._writers.items() if writer_class.is_available()]

    @classmethod
    def create(cls, target_name: str, **kwargs) -> BaseDimensionalWriter:
        """Create a writer instance.

        Args:
            target_name: Name of target.
            **kwargs: Writer-specific configuration.

        Returns:
            Configured writer instance.
        """
        writer_class = cls.get(target_name)
        return writer_class(**kwargs)

    @classmethod
    def create_from_config(cls, config: TargetConfig) -> BaseDimensionalWriter:
        """Create a writer from a configuration object.

        Args:
            config: Target configuration.

        Returns:
            Configured writer instance.
        """
        writer_class = cls.get(config.target_type)
        return writer_class.from_config(config)

    @classmethod
    def get_status(cls) -> dict[str, dict]:
        """Get status of all registered writers.

        Returns:
            Dict of target_name -> status info including:
                - registered: Always True
                - available: Whether required packages are installed
                - required_packages: List of required package names
        """
        status = {}
        for name, writer_class in cls._writers.items():
            status[name] = {
                "registered": True,
                "available": writer_class.is_available(),
                "required_packages": writer_class.REQUIRED_PACKAGES,
            }
        return status


def _auto_register_writers() -> None:
    """Auto-register available writers on module import."""
    # Always register DuckDB (it's a core dependency)
    from healthsim.dimensional.writers.duckdb_writer import DuckDBDimensionalWriter

    WriterRegistry.register(DuckDBDimensionalWriter)

    # Register Databricks if available
    try:
        from healthsim.dimensional.writers.databricks_writer import (
            DatabricksDimensionalWriter,
        )

        WriterRegistry.register(DatabricksDimensionalWriter)
    except ImportError:
        logger.debug("Databricks writer not available (package not installed)")


# Auto-register on import
_auto_register_writers()
