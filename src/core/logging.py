from logging import basicConfig, INFO


def setup_logging() -> None:
    """Setup Loggin Format"""
    basicConfig(level=INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
