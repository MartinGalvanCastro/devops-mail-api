from unittest.mock import AsyncMock, Mock, create_autospec
from uuid import UUID, uuid4

import pytest

from src.application.services.blacklist import BlacklistService
from src.domain.entities.blacklists import Blacklist, CreateBlacklistRequest
from src.domain.repositories.blacklist import IBlacklistRepository


@pytest.fixture
def mock_repo():
    return create_autospec(IBlacklistRepository)


@pytest.fixture
def blacklist_service(mock_repo):
    return BlacklistService(mock_repo)


@pytest.mark.asyncio
async def test_create_blacklist_success(blacklist_service, mock_repo):
    # Arrange
    test_email = "TEST@example.com"
    test_app_uuid = uuid4()
    test_reason = "Test reason"
    test_ip = "192.168.1.1"

    request = CreateBlacklistRequest(
        email=test_email, app_uuid=test_app_uuid, blocked_reason=test_reason
    )

    expected_blacklist = Blacklist(
        email=test_email.lower(),
        app_uuid=test_app_uuid,
        blocked_reason=test_reason,
        ip_address=test_ip,
    )

    mock_repo.create = AsyncMock(return_value=expected_blacklist)

    # Act
    result = await blacklist_service.create_blacklist(request, test_ip)

    # Assert
    mock_repo.create.assert_awaited_once()

    # Verify the created blacklist passed to repository
    created_arg = mock_repo.create.call_args[1]["data"]
    assert created_arg.email == test_email.lower()
    assert created_arg.app_uuid == test_app_uuid
    assert created_arg.blocked_reason == test_reason
    assert created_arg.ip_address == test_ip

    assert result == expected_blacklist


@pytest.mark.asyncio
async def test_create_blacklist_without_ip(blacklist_service, mock_repo):
    # Arrange
    request = CreateBlacklistRequest(
        email="test@example.com", app_uuid=uuid4(), blocked_reason="Test reason"
    )

    mock_repo.create = AsyncMock()

    # Act
    await blacklist_service.create_blacklist(request)

    # Assert
    created_arg = mock_repo.create.call_args[1]["data"]
    assert created_arg.ip_address is None


@pytest.mark.asyncio
async def test_get_blacklist_by_email_found(blacklist_service, mock_repo):
    # Arrange
    test_email = "TEST@example.com"
    expected_blacklist = Blacklist(
        email=test_email.lower(),
        app_uuid=uuid4(),
        blocked_reason="Test reason",
        ip_address="192.168.1.1",
    )

    mock_repo.get_by_email = AsyncMock(return_value=expected_blacklist)

    # Act
    result = await blacklist_service.get_blacklist_by_email(test_email)

    # Assert
    mock_repo.get_by_email.assert_awaited_once_with(email=test_email.lower())
    assert result == expected_blacklist


@pytest.mark.asyncio
async def test_get_blacklist_by_email_not_found(blacklist_service, mock_repo):
    # Arrange
    mock_repo.get_by_email = AsyncMock(return_value=None)

    # Act
    result = await blacklist_service.get_blacklist_by_email("nonexistent@example.com")

    # Assert
    mock_repo.get_by_email.assert_awaited_once_with(email="nonexistent@example.com")
    assert result is None
