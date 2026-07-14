
# PR Response Doc — CineLog Watchlist Feature

## AI Usage
<!-- Fill in at the end — how you used AI tools during this project -->

## Comments

| Comment                                                                                                                                                                                                                                                                                                        | **Topic**          | **Required Action**                                                                      |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | ---------------------------------------------------------------------------------------- |
| `save_to_watchlist()` should follow the project's naming convention. Compare with `add_to_collection()` — the pattern here is `verb_to_noun`. Please rename to `add_to_watchlist()` and update all call sites.                                                                                                 | Function Naming    | Rename `save_to_watchlist()` to `add_to_watchlist()` and update all call sites.          |
| What happens if a user calls this with a film that's already on their watchlist? The current implementation would add a duplicate entry. Please handle this case.                                                                                                                                              | Deduplication      | Add logic to `add_to_watchlist()` to prevent duplicate watchlist entries.                |
| Please add a test for the case where `film_id` doesn't exist in the database. Look at the existing tests in `test_collection.py` — the pattern is there.                                                                                                                                                       | Missing Test       | Create `tests/test_watchlist.py` to test the case where a `film_id` does not exist.      |
| I notice watchlists default to `public=True`. We don't have a documented decision on default visibility for user lists. Before I can approve this, I need you to add a note to your PR description explaining your reasoning. I want to make sure we're being intentional here, not just inheriting a default. | Default Visibility | Write a design decision justifying why `public=True` is (or isn't) the correct default.  |
| I'd prefer watchlists to default to "date added" order rather than alphabetical. Most users want to see what they added recently. I'm open to discussion if you see it differently — but let's make a decision and document it.                                                                                | Sort Order         | Write an argument for your chosen sort order (Date Added vs. Alphabetical).              |
| A refactor merged to `main` that changed film IDs from integers to UUIDs. Your watchlist code still references integer IDs. Please rebase on `main` and update accordingly.                                                                                                                                    | Rebase             | Rebase on `main` to resolve the conflict caused by the switch from Integer IDs to UUIDs. |

### Comment 1 — Rename

**What I did:**
Renamed `save_to_watchlist()` to `add_to_watchlist()` in `services/watchlist_service.py` to match the project's verb_to_noun convention. Also updated the function call in `routes/watchlist/watchlist.py`.

**How I verified:**
Used an editor-wide search to confirm I found and updated all call sites across the codebase, and ran tests.

### Comment 2 — Deduplication

**What I did:**
Created an `AlreadyInWatchlistError` exception in `services/watchlist_service.py` and added logic inside `add_to_watchlist()` to check if the film is already in the watchlist before adding it. Updated `routes/watchlist/watchlist.py` to catch this exception and return a 409 status code.

**How I verified:**
Referenced the `add_to_collection()` pattern in `services/collection_service.py` to ensure the deduplication check and error raising was implemented correctly.

### Comment 3 — Missing test

**What I did:**
Created `tests/test_watchlist.py` and wrote `test_add_to_watchlist_nonexistent_film_raises`. Included the necessary `app` and `sample_user` fixtures so the test could run independently.

**How I verified:**
Modeled the test structure after `test_add_to_collection_nonexistent_film_raises` in `tests/test_collection.py`. Ran `pytest tests/test_watchlist.py -v` to confirm the test successfully passes by raising `FilmNotFoundError`.

### Comment 4 — Default visibility

**My position:**
Watchlists should default to `public=False` (private by default).

**Reasoning:**
This is a privacy-first decision. A watchlist often serves not only as a personal backlog of films to watch but also as a list that users may not want to others to see. By defaulting to private, we allow users to feel safe about adding to their list without worrying about their public image on CineLog.

**Tradeoff acknowledged:**
The primary tradeoff is a reduction in social discovery. If most watchlists remain private, users have fewer opportunities to discover new films by browsing their friends' watchlists. We can mitigate this by clearly offering a "Make Public" toggle when creating or viewing the watchlist.

**What I did:**
Changed the default for `WatchlistEntry.public` to `False` in `models.py`. Added a `public` parameter to `add_to_watchlist()` in `services/watchlist_service.py` so callers can override the default, and updated the `/add` endpoint in `routes/watchlist/watchlist.py` to read `public` from the request body.

**How I verified:**
Checked the model to confirm the default boolean was successfully changed. Reviewed the route and service files to ensure the `public` parameter is properly passed down from the JSON request to the database model.

### Comment 5 — Sort order

**My position:**
Watchlists should default to "date added" (newest first).

**Reasoning:**
When a user opens their watchlist, they are usually deciding what to watch *next*. The most recently added films are usually top-of-mind and have the highest intent-to-watch, so placing them at the top makes sense.

**Engagement with reviewer's point:**
I agree with the reviewer that "Most users want to see what they added recently." While an alphabetical sort might help a user locate a specific film in a massive list, users usually want to see what they added recently. I think it is unlikely for most users to have massive lists.

**What I did:**
Changed the sort order in `get_watchlist()` in `services/watchlist_service.py` from `.order_by(Film.title.asc())` to `.order_by(WatchlistEntry.date_added.desc())`.

**How I verified:**
Checked the service implementation and ran the test suite to ensure no syntax errors were introduced.

### Comment 6 — Rebase

**What conflicted:**

**What I did:**

**How I verified:**

## PR Description
<!-- Written at the end — feature overview, design decisions, manual testing steps -->