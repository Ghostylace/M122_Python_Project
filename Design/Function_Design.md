# Function design

## Core functions

### fetch_free_games(params)

```Python
def fetch_free_games(params: dict) -> dict:
    """Query the IsThereAnyDeal API and return raw free-game data."""
    # build request URL and headers
    # call the API endpoint
    # parse JSON response
    # return raw payload
```

### map_free_games(raw_data)

```Python
def map_free_games(raw_data: dict) -> list:
    """Convert the raw API response into a list of domain game dictionaries."""
    # iterate through API result items
    # normalize fields: title, price, currency, platform, url, expiry
    # determine is_free flag and age restriction
    # return list of game dicts
```

### cache_games(games, ttl_minutes)

```Python
def cache_games(games: list, ttl_minutes: int) -> None:
    """Store the fetched game list and expiry metadata in a local cache."""
    # save games and timestamp/TTL
```

### load_cached_games()

```Python
def load_cached_games() -> tuple[list, bool]:
    """Load cached games and return whether cache is still valid."""
    # read cache storage
    # compare saved timestamp + TTL with current time
    # return games list and cache_is_valid boolean
```

### format_game_list(games)

```Python
def format_game_list(games: list) -> str:
    """Create a user-friendly text summary of free Steam games."""
    # group or sort games
    # format expiry and price information
    # return formatted string
```

### filter_expiring_games(games, within_days)

```Python
def filter_expiring_games(games: list, within_days: int) -> list:
    """Return games whose free offer expires within a date range."""
    # parse expiry dates
    # compare to current date
    # return filtered list
```

### notify_free_games(new_games, old_games)

```Python
def notify_free_games(new_games: list, old_games: list) -> None:
    """Identify newly added free games and optionally send notifications."""
    # compare old and new lists by id or title
    # if new games exist, build notification message
    # send message via configured notification channel
```

## Workflow functions

### update_free_games()

```Python
def update_free_games() -> dict:
    """Fetch the current free games list, using cache when possible."""
    # load cache and check validity
    # if cache expired or missing, fetch fresh data
    # map raw data to domain games
    # cache the fresh data
    # return the current deal collection
```

### get_latest_free_games()

```Python
def get_latest_free_games() -> list:
    """Return the latest cached free games without forcing an API refresh."""
    # load cache and return games if valid
    # if no valid cache, optionally call update_free_games
```

### has_free_steam_games()

```Python
def has_free_steam_games() -> bool:
    """Check whether any free Steam games are currently available."""
    # use get_latest_free_games or update_free_games
    # return True if any is_free games exist
```

## Supporting utilities

### build_itad_request(params)

```Python
def build_itad_request(params: dict) -> tuple[str, dict]:
    """Construct the URL and headers for the Itad API request."""
    # return request URL and headers payload
```

### parse_itad_response(response)

```Python
def parse_itad_response(response: dict) -> dict:
    """Validate and normalize the Itad response structure."""
    # check status and error fields
    # return consistent payload for mapping
```

### to_game_dict(dto)

```Python
def to_game_dict(dto: dict) -> dict:
    """Convert a single API DTO into the internal game dictionary shape."""
    # map field names and derive is_free / expiry
    # return normalized game dict
```

## Design notes

- Separate fetching, mapping, caching, formatting, and notification to keep functions small and testable.
- Use `update_free_games()` as the primary orchestrator for fresh data.
- Keep `get_latest_free_games()` lightweight so it can serve cached results quickly.
- Keep API-specific request/response handling in helper functions to make the workflow portable.
