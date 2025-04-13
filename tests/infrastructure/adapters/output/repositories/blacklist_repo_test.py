from datetime import datetime
from unittest.mock import ANY, AsyncMock, Mock
from uuid import UUID, uuid4

import pytest

from src.domain.entities.blacklists import Blacklist
from src.infrastructure.adapters.output.repositories.blacklist import (
    BlacklistRepository,
)


@pytest.fixture
def mock_session():
    session = Mock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.execute = AsyncMock()
    return session


@pytest.fixture
def blacklist_repository(mock_session):
    return BlacklistRepository(mock_session)


@pytest.mark.asyncio
async def test_create_blacklist(blacklist_repository, mock_session):
    # Setup test data
    test_id = uuid4()
    created_at = datetime.now()
    blacklist_data = {
        "email": "test@example.com",
        "app_uuid": uuid4(),
        "blocked_reason": "test reason",
        "ip_address": "192.168.1.1",
    }
    blacklist_domain = Blacklist(**blacklist_data)

    # Mock the database model creation
    mock_session.add.assert_not_called()

    # Mock refresh to populate fields
    async def refresh_mock(model):
        model.id = test_id
        model.created_at = created_at
        model.updated_at = created_at

    mock_session.refresh.side_effect = refresh_mock

    # Execute
    result = await blacklist_repository.create(blacklist_domain)

    # Assertions
    mock_session.add.assert_called_once()
    added_model = mock_session.add.call_args[0][0]

    # Verify model creation with correct fields
    assert added_model.email == blacklist_data["email"]
    assert added_model.app_uuid == blacklist_data["app_uuid"]
    assert added_model.blocked_reason == blacklist_data["blocked_reason"]
    assert added_model.ip_address == blacklist_data["ip_address"]

    # Verify database operations
    mock_session.commit.assert_awaited_once()
    mock_session.refresh.assert_awaited_once_with(added_model)

    # Verify returned domain object
    assert isinstance(result, Blacklist)
    assert result.id == test_id
    assert result.created_at == created_at
    assert result.updated_at == created_at


@pytest.mark.asyncio
async def test_get_by_email_exists(blacklist_repository, mock_session):
    test_email = "exists@example.com"
    mock_model = Mock(
        email=test_email,
        app_uuid=uuid4(),
        blocked_reason="spam",
        ip_address="10.0.0.1",
        id=uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    # Proper mock chaining for execute().scalars().first()
    mock_result = Mock()
    mock_scalars = Mock()
    mock_scalars.first.return_value = mock_model
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_result

    result = await blacklist_repository.get_by_email(test_email)

    # Verify the execute call
    mock_session.execute.assert_awaited_once()

    # Verify result conversion
    assert isinstance(result, Blacklist)
    assert result.email == test_email
    assert result.id == mock_model.id
    assert result.blocked_reason == "spam"


@pytest.mark.asyncio
async def test_get_by_email_not_found(blacklist_repository, mock_session):
    test_email = "notfound@example.com"

    # Proper mock chaining for execute().scalars().first()
    mock_result = Mock()
    mock_scalars = Mock()
    mock_scalars.first.return_value = None
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_result

    result = await blacklist_repository.get_by_email(test_email)

    # Verify the execute call
    mock_session.execute.assert_awaited_once()

    # Verify None is returned when no results
    assert result is None
