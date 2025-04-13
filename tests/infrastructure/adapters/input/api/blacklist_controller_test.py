from unittest.mock import AsyncMock, MagicMock, create_autospec, patch
from uuid import uuid4

import pytest
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.domain.entities.blacklists import (
    Blacklist,
    CreateBlacklistRequest,
    CreateBlacklistResponse,
    ValidateEmailInBlacklistResponse,
)
from src.infrastructure.adapters.input.api.blacklist import (
    create_blacklist,
    validate_email_in_blacklist,
)

# Fixtures --------------------------------------------------------------------


@pytest.fixture
def mock_request():
    request = MagicMock(spec=Request)
    request.state.client_ip = "192.168.1.1"
    return request


@pytest.fixture
def mock_security():
    security = create_autospec(HTTPBearer)
    security.return_value = MagicMock(credentials="valid_token")
    return security


@pytest.fixture
def mock_blacklist_service():
    service = MagicMock()
    service.create_blacklist = AsyncMock()
    service.get_blacklist_by_email = AsyncMock()
    return service


@pytest.fixture
def valid_token():
    return MagicMock(spec=HTTPAuthorizationCredentials)


# Common Test Data ------------------------------------------------------------


def create_test_blacklist():
    return Blacklist(
        email="test@example.com",
        app_uuid=uuid4(),
        blocked_reason="spam",
        ip_address="192.168.1.1",
    )


# Tests ------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_blacklist_success(
    mock_request, mock_blacklist_service, valid_token, simulate_failure_check
):
    # Arrange
    test_data = CreateBlacklistRequest(
        email="test@example.com", app_uuid=uuid4(), blocked_reason="spam"
    )

    # Act
    with patch(
        "src.infrastructure.adapters.input.api.blacklist.get_blacklist_service",
        return_value=mock_blacklist_service,
    ):
        response = await create_blacklist(
            request=mock_request,
            data=test_data,
            session=AsyncMock(),
            _token=valid_token,
        )

    # Assert
    mock_blacklist_service.create_blacklist.assert_awaited_once_with(
        data=test_data, ip_address=mock_request.state.client_ip
    )
    assert response == CreateBlacklistResponse(message="Blacklist created successfully")


@pytest.mark.asyncio
async def test_validate_email_blacklisted(
    mock_blacklist_service, valid_token, simulate_failure_check
):
    # Arrange
    mock_blacklist_service.get_blacklist_by_email.return_value = create_test_blacklist()

    # Act
    with patch(
        "src.infrastructure.adapters.input.api.blacklist.get_blacklist_service",
        return_value=mock_blacklist_service,
    ):
        response = await validate_email_in_blacklist(
            email="test@example.com", session=AsyncMock(), _token=valid_token
        )

    # Assert
    mock_blacklist_service.get_blacklist_by_email.assert_awaited_once_with(
        email="test@example.com"
    )
    assert response == ValidateEmailInBlacklistResponse(
        is_blacklisted=True, blocked_reason="spam"
    )


@pytest.mark.asyncio
async def test_validate_email_not_blacklisted(
    mock_blacklist_service, valid_token, simulate_failure_check
):
    # Arrange
    mock_blacklist_service.get_blacklist_by_email.return_value = None

    # Act
    with patch(
        "src.infrastructure.adapters.input.api.blacklist.get_blacklist_service",
        return_value=mock_blacklist_service,
    ):
        response = await validate_email_in_blacklist(
            email="notfound@example.com", session=AsyncMock(), _token=valid_token
        )

    # Assert
    assert response == ValidateEmailInBlacklistResponse(
        is_blacklisted=False, blocked_reason="User not blocked"
    )
