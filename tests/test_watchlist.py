"""
tests/test_watchlist.py — CineLog

Tests for the watchlist service.
These tests demonstrate the patterns used across the codebase.
"""

import pytest
from app import create_app, db
from models import User, Film, WatchlistEntry
from services.watchlist_service import (
    add_to_watchlist,
    get_watchlist,
    FilmNotFoundError,
    AlreadyInWatchlistError,
    remove_from_watchlist,
    NotInWatchlistError,
)


@pytest.fixture
def app():
    """Create an isolated test app with an in-memory database."""
    app = create_app(config={
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def sample_user(app):
    """A user to use in tests."""
    with app.app_context():
        user = User(username="testuser", email="test@example.com")
        db.session.add(user)
        db.session.commit()
        return user.id


@pytest.fixture
def sample_film(app):
    """A film to use in tests."""
    with app.app_context():
        import uuid
        film_id = str(uuid.uuid4())
        film = Film(id=film_id, title="Test Film", director="Test Director", year=2026)
        db.session.add(film)
        db.session.commit()
        return film_id

# ── Nonexistent film ─────────────────────────────────────────────────────────

def test_add_to_watchlist_nonexistent_film_raises(app, sample_user):
    """
    Adding a film_id that doesn't exist in the database should raise
    FilmNotFoundError, not a database integrity error.
    """
    with app.app_context():
        fake_film_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(FilmNotFoundError):
            add_to_watchlist(user_id=sample_user, film_id=fake_film_id)



def test_add_duplicate_film_to_watchlist_raises(app, sample_user, sample_film):
    """
    Adding a film that is already on the watchlist should raise
    AlreadyInWatchlistError.
    """
    with app.app_context():
        add_to_watchlist(user_id=sample_user, film_id=sample_film)
        with pytest.raises(AlreadyInWatchlistError):
            add_to_watchlist(user_id=sample_user, film_id=sample_film)


def test_remove_from_watchlist(app, sample_user, sample_film):
    """
    Removing a film should delete the entry. Attempting to remove a film
    not on the watchlist should raise NotInWatchlistError.
    """
    with app.app_context():
        add_to_watchlist(user_id=sample_user, film_id=sample_film)
        assert remove_from_watchlist(user_id=sample_user, film_id=sample_film) is True
        
        with pytest.raises(NotInWatchlistError):
            remove_from_watchlist(user_id=sample_user, film_id=sample_film)

