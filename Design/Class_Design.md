# Class design

## Datatype classes

### Game class

```TS
class Game {
    id: string
    slug: string
    title: string
    type: string
    mature: boolean
    isFree: boolean
    price: float
    cut: float
    url: string
    expiry?: string
}
```

### DealCollection class

```TS
class DealCollection {
    games: Game[]
    fetchedAt: Date
    source: string

    addGame(game: Game): void
    getFreeGames(): Game[]
    getExpiringSoon(days: number): Game[]
}
```

### ApiResponse classes

```TS
class ItadGameDto {
    id: string
    slug: string
    title: string
    type: string
    mature: boolean
    isFree: boolean
    price: float
    cut: float
    url: string
    expiry?: string
}

class ItadSearchResponse {
    data: ItadGameDto[]
}
```

## Service classes

### ItadApiClient class

```TS
class ItadApiClient {
    apiKey: string

    constructor(apiKey: string)

    fetchFreeGames(params: ItadSearchParams): Promise<ItadSearchResponse>
    fetchGameDetails(gameId: string): Promise<ItadGameDto>
}
```

### ItadSearchParams class

```TS
class ItadSearchParams {
    country: string          // ISO country code for price conversion
    shops: int         // e.g. 61 for "steam"
    sort: string
}
```

### SteamFreeGamesChecker class

```TS
class SteamFreeGamesChecker {
    apiClient: ItadApiClient
    cache: GameCache
    formatter: GameFormatter
    notifier?: NotificationService

    constructor(apiClient: ItadApiClient, cache: GameCache, formatter: GameFormatter, notifier?: NotificationService)

    updateFreeGames(): Promise<DealCollection>
    getLatestFreeGames(): DealCollection
    getFreeGamesByPlatform(platform: string): Game[]
    getExpiringOffers(days: number): Game[]
}
```

### GameCache class

```TS
class GameCache {
    data: DealCollection
    ttlMinutes: number

    constructor(ttlMinutes: number)

    load(): DealCollection | null
    save(collection: DealCollection): void
    isExpired(): boolean
}
```

### GameFormatter class

```TS
class GameFormatter {
    formatList(collection: DealCollection): string
    formatForDisplay(game: Game): string
    formatSummary(collection: DealCollection): string
}
```

### NotificationService class (optional)

```TS
class NotificationService {
    send(message: string): Promise<void>
}
```

## Adapter / Mapper classes

### ItadToGameMapper class

```TS
class ItadToGameMapper {
    map(dto: ItadGameDto): Game
}
```

## Utility classes

### Config class

```TS
class AppConfig {
    itadApiKey: string
    filter: string
    country: string
}
```

## Class relationships

- `SteamFreeGamesChecker` depends on `ItadApiClient`, `GameCache`, `GameFormatter`, and optionally `NotificationService`.
- `ItadApiClient` retrieves raw data from the IsThereAnyDeal API.
- `ItadToGameMapper` converts raw API DTOs into domain `Game` objects.
- `DealCollection` holds a list of `Game` objects and provides helpers for filtering free and expiring offers.
- `GameCache` stores the latest `DealCollection` to avoid unnecessary API calls.
- `GameFormatter` prepares human-readable output for the UI or console.
- `NotificationService` can send alerts for newly found or expiring free games.

## Example workflow

1. `SteamFreeGamesChecker.updateFreeGames()` checks `GameCache.isExpired()`.
2. If the cache is expired, it calls `ItadApiClient.fetchFreeGames()`.
3. The raw `ItadSearchResponse` is mapped to `DealCollection` via `ItadToGameMapper`.
4. The new collection is saved with `GameCache.save()`.
5. `GameFormatter.formatList()` renders the free games list.
6. If configured, `NotificationService.send()` dispatches new free game alerts.

