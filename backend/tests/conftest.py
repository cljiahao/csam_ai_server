import os
import pytest
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app import app
from db.base import Base
from db.session import get_db

from core.directory import directory

SQLALCHEMY_DATABASE_URL = f"sqlite:///{directory.base_dir}/tests/test_db.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)  # Create the tables.


@pytest.fixture(scope="session", autouse=True)
def cleanup_database(request: pytest.FixtureRequest) -> None:
    """Cleanup the test database after tests have run."""

    def remove_test_db() -> None:
        # Ensure that connections and sessions are closed
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

        # Remove the test database file
        if os.path.exists(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")):
            os.remove(SQLALCHEMY_DATABASE_URL.replace("sqlite:///", ""))

    request.addfinalizer(remove_test_db)


@pytest.fixture(scope="function")
def db_session(request: pytest.FixtureRequest) -> Generator[Session, None, None]:
    """Create a new database session with a rollback at the end of the test."""

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSession(bind=connection)

    def teardown() -> None:
        session.close()
        transaction.rollback()
        connection.close()

    request.addfinalizer(teardown)
    yield session


@pytest.fixture(scope="function")
def test_client(db_session: Session) -> Generator[TestClient, None, None]:
    """Create a test client that uses the override_get_db fixture to return a session."""

    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def mock_func_logger(monkeypatch: pytest.MonkeyPatch) -> MagicMock:
    """Dynamically mock the logger's error method for testing."""

    def _mock_func_logger(logger_path: str) -> MagicMock:
        """Create a mock for the specified logger path."""
        mock = MagicMock()
        monkeypatch.setattr(logger_path, mock)
        return mock

    return _mock_func_logger


@pytest.fixture
def mock_file_methods() -> MagicMock:
    """Fixture to mock file input."""

    mock_path = Path("/fake/path")

    mock_file = MagicMock()
    mock_file.filename = "test_image.png"
    mock_file.file.read.return_value = (
        b"\x00\x00\x00\x00"  # Simulate binary file content
    )

    return mock_path, mock_file


@pytest.fixture(scope="function")
def sample_lot_details() -> dict[str, str]:
    """Provide sample lot data for use in tests."""
    return {
        "lotNo": "1234567890",
        "plate": "test_image",
        "item": "GCM32ER71E106KA59_+B55-E01GJ",
    }


@pytest.fixture(scope="function")
def sample_chips_batch_details() -> dict[str, int]:
    """Provide sample chips and batch for use in tests."""
    return {
        "no_of_chips": 4000,
        "no_of_batches": 15,
        "no_of_real": 0,
    }


@pytest.fixture
def sample_file_names() -> list[str]:
    """Provide sample file names for use in tests"""
    # File_name format - {mode}_{batch}_{index}_{x_coord}_{y_coord}.png
    return [
        "0_0_339_1761_2435.png",
        "0_0_428_2670_2386.png",
        "0_1_3474_245_575.png",
        "0_2_3833_1155_374.png",
        "0_3_3615_1921_496.png",
        "0_3_3944_1890_314.png",
        "0_4_4391_2321_72.png",
        "0_7_2314_1103_1286.png",
        "0_9_2356_2272_1263.png",
        "0_10_1755_3245_1597.png",
        "0_10_2605_3311_1127.png",
        "0_10_2897_3142_967.png",
        "0_11_1039_556_2064.png",
        "0_12_598_855_2297.png",
        "0_15_366_3090_2419.png",
    ]


@pytest.fixture
def sample_settings_group(
    sample_lot_details: dict[str, str]
) -> dict[str, list[dict[str, str | dict[str, dict[str, list[int]]]]]]:
    """Sample settings group fixture."""
    return {
        "settingsGroup": [
            {
                "item": sample_lot_details["item"],
                "settings": {
                    "batch": {"erode": [1, 1], "close": [1, 1]},
                    "chip": {"erode": [1, 1], "close": [1, 1]},
                },
            },
        ]
    }


@pytest.fixture
def sample_color_group(
    sample_lot_details: dict[str, str]
) -> dict[str, list[dict[str, str]]]:
    """Sample color group fixture."""
    return {
        "colorGroup": [
            {
                "item": sample_lot_details["item"],
                "colors": [
                    {"category": "NG", "hex": "#FFFFFF"},
                    {"category": "Others", "hex": "#000000"},
                ],
            },
            {
                "item": "test_item",
                "colors": [
                    {"category": "NG", "hex": "#FFFFFF"},
                    {"category": "Others", "hex": "#000000"},
                ],
            },
        ]
    }
