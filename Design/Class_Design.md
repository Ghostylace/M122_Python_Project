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

### Message class

```TS
class Message {
    games: Game[]

    constructor(games: Game[])

    createMessage(): string
}
```

### DealCollection class

```TS
class DealCollection {
    games: Game[]

    load_games() : Game[]
    loadNewGames(new_games: Game[]) : Game[]
    saveGames(): void
    getFreeGames(): Game[]
}
```

## Service classes

### ItadApiClient class

```TS
class ItadApiClient {
    fetchFreeGames(apiKey: string): Game[]
}
```

### SteamFreeGamesChecker class

```TS
class SteamFreeGamesChecker {
    fetchGames(): void
}
```

### GameMapper class

```TS
class GameMapper {
    map(jsonGame): Game
    mapMultipleFromJson(json): Game[]
}
```

### MailService class

```TS
class MailService {
    _loadConfig(): void
    sendMail(body: string): void
}
```

## Utility classes

### ConfigReader class

```TS
class ConfigReader {
    itadApiKey: string
    filter: string
    country: string

    readConfigFile(): string
}
```
