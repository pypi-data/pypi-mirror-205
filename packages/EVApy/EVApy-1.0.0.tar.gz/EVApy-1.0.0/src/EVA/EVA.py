import datetime
import typing
import EVA.EVAerrors as EVAerrors
from gql import gql, Client
from gql.transport.exceptions import TransportQueryError
from gql.transport.aiohttp import AIOHTTPTransport

"""
   ╔═══════════════════════════════════════════════════════════════╗
   ╠ Welcome to EVA API made in Python by Kilian Douarinou (Garoh) ╣
   ╚═══════════════════════════════════════════════════════════════╝
    
   ┌─────────────────────────────────────────────────────┐
   │ Here is an example of a simple script using EVA API │
   ├─────────────────────────────────────────────────────┴───────────────────────────────────────────────────────┐
   │ import asyncio                                                                                              │
   │ import EVA.EVA as eva                                                                                       │
   │                                                                                                             │
   │ async def main():                                                                                           │
   │     # Get stats for a given player with it's discriminant                                                   │
   │     # Ex. 'EVA_USERNAME#12345'                                                                              │
   │     player_stats = await eva.getStats(username='EVA_USERNAME#12345')                                        │
   │                                                                                                             │
   │     # Get all EVA cities for getting more informations                                                      │
   │     # We need the ID of the city actually                                                                   │
   │     cities = await eva.getCities()                                                                          │
   │                                                                                                             │
   │     # For example we get the ID of the first location in 'cities'.                                          │
   │     # It is the location ID for Tours city.                                                                 │
   │     location = await eva.getLocation(cities[0]['id']) # So location['id] = 15                               │
   │                                                                                                             │
   │     # So we can finally get Last Games of the player                                                        │
   │     # We use the 'userId' of the player located in 'player_stats['player']['userId']'                       │
   │     # And location ID from 'location['id']'                                                                 │
   │     last_games = await eva.getLastGames(player_stats['player']['userId'], 1, location['id'], items_limit=5) │
   │                                                                                                             │
   │     # We print every results to check values                                                                │
   │     # Once every requests are done before, you can skip this part                                           │
   │     # And do whatever you want with these data.                                                             │
   │     print("Player stats: ", player_stats, "\n")                                                             │
   │     print("Last Games of this Player: ", last_games, "\n")                                                  │
   │     print("EVA Location: ", location, "\n")                                                                 │
   │     print("EVA Cities: ", cities, "\n")                                                                     │
   │                                                                                                             │
   │ asyncio.run(main())                                                                                         │
   │                                                                                                             │
   └─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

   ┌────────────────────────────────────┐
   │ Here are the useful API functions  │
   ├────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
   │                                                                                                                                                   │
   ├ ■ await getStats(username: str, user_id: int, season_id: int)                                                                                     │
   ├─── ► Retrieves a player's public information.                                                                                                     │
   │                                                                                                                                                   │
   │                                                                                                                                                   │
   ├ ■ await getLastGames(user_id: int, season_id: int, location_id: int, terrain_ids: typing.Optional[typing.List[int]], page: int, items_limit: int) │
   ├─── ► Retrieve data from a player's last games.                                                                                                    │
   │                                                                                                                                                   │
   │                                                                                                                                                   │
   ├ ■ await getSeasonsList()                                                                                                                          │
   ├─── ► Get the list of seasons.                                                                                                                     │
   │                                                                                                                                                   │
   │                                                                                                                                                   │
   ├ ■ await getCities()                                                                                                                               │
   ├─── ► Get all cities where an Eva room is present.                                                                                                 │
   │                                                                                                                                                   │
   │                                                                                                                                                   │
   ├ ■ await getCalendar(date: datetime.datetime, location_id: int)                                                                                    │
   ├─── ► Get the calendar of an Eva room.                                                                                                             │
   │                                                                                                                                                   │
   │                                                                                                                                                   │
   ├ ■ await getSession(slot_id: str, terrain_id: int)                                                                                                 │
   ├─── ► Returns the content of a session and players who have booked.                                                                                │
   │                                                                                                                                                   │
   │                                                                                                                                                   │
   ├ ■ await getLocation(location_id: int)                                                                                                             │
   ├─── ► Get the city from a location ID.                                                                                                             │
   │                                                                                                                                                   │
   └───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
"""


def _send_query():
    """
      A decorator that builds and execute a query with all informations needed to send a compliant request to the EVA website.
    """
    transport = AIOHTTPTransport(url="https://api.eva.gg/graphql", headers={
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
        "Connection": "keep-alive",
        "content-type": "application/json",
        "Host": "api.eva.gg",
        "Origin": "https://www.eva.gg",
        "Referer": "https://www.eva.gg/",
        "sec-ch-ua": '"Opera GX";v="89", "Chromium";v="103", "_Not:A-Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36 OPR/89.0.4447.64"
    })

    def outer(func):
        async def inner(*args, **kwargs):
            async with Client(
                transport=transport,
                fetch_schema_from_transport=False,
            ) as session:
                try:
                    result = await session.execute(*(await func(*args, **kwargs)))
                except TransportQueryError as e:
                    if e.errors:
                        if e.errors[0]["message"] == 'User profile is private':
                            raise EVAerrors.UserIsPrivate(kwargs['username'] if 'username' in kwargs else None)
                        elif e.errors[0]["message"] == "User not found":
                            raise EVAerrors.UserNotFound(kwargs['username'] if 'username' in kwargs else None)
                        else:
                            raise
                except:
                    raise
                else:
                    if 'locations' in result:
                        if 'nodes' in result['locations']:
                            return result['locations']['nodes']
                    elif 'location' in result:
                        return result['location']
                    return result
        return inner
    return outer


@_send_query()
async def getStats(username: str = None, user_id: int = None, season_id: int = None) -> typing.Dict:
    """
      Retrieve a player's public information.

      Parameters
      ----------
      username: The username of the Eva account

      user_id: The id of the Eva account

      season_id: The number of the season
    """
    params = {}

    query = gql("""
    query($userId: Int, $username: String, $seasonId: Int) {
        player(userId: $userId, username: $username) {
        ... {
            userId
            username
            displayName
        }

        seasonPass(seasonId: $seasonId) {
            active
        }

        experience(gameId: 1, seasonId: $seasonId) {
            level
            levelProgressionPercentage
            experience
            experienceForNextLevel
            experienceForCurrentLevel
            seasonId
        }
        statistics(gameId: 1, seasonId: $seasonId) {
            data {
            gameCount
            gameTime
            gameVictoryCount
            gameDefeatCount
            gameDrawCount
            inflictedDamage
            bestInflictedDamage
            kills
            deaths
            assists
            killDeathRatio
            killsByDeaths
            traveledDistance
            traveledDistanceAverage
            bestKillStreak
            }
        }
        }
    }
    """)

    params['userId'] = user_id
    params['username'] = username
    params['seasonId'] = season_id

    return query, params


@_send_query()
async def getLastGames(user_id: int, season_id: int, location_id: int, terrain_ids: typing.Optional[typing.List[int]] = None, page: int = 1, items_limit: int = 20) -> typing.Dict:
    """
        Retrieve data from a player's last games.

        Parameters
        ----------
        user_id: The id of the Eva account

        page: The page number

        items_limit: The limit of the list of games

        season_id: EVA season ID

        location_id: EVA location ID

        terrain_ids (`List[int]`): List of terrain IDs

        Returns
        -------
        `Dict`: Dict of last X games of an EVA player
    """
    params = {}

    query = gql("""
    query (
        $userId: Int
        $page: PageInput
        $mode: [GameModeEnum!]
        $seasonId: Int
        $locationId: Int
        $terrainIds: [Int!]
    ) {
        gameHistories(
        userId: $userId
        page: $page
        mode: $mode
        seasonId: $seasonId
        locationId: $locationId
        terrainIds: $terrainIds
        ) {
        totalCount
        pageInfo {
            current
            itemsLimit
            total
        }
        nodes {
            ... {
            id
            createdAt

            data {
                duration
                mode
                map
                outcome
                waveCount
                success
                generatorPercent
                puzzleFailedCount
                plasmaHitCount
                teamOne {
                score
                name
                }
                teamTwo {
                score
                name
                }
            }
            players {
                id
                userId
                data {
                niceName
                rank
                team
                score
                outcome
                kills
                deaths
                assists
                team
                inflictedDamage
                bulletsFiredAccuracy
                }
            }
            }
        }
        }
    }
    """)

    params['userId'] = user_id
    params['page'] = page
    params['seasonId'] = season_id
    params['page'] = {
        'page': page,
        'itemsLimit': items_limit
    }
    params['locationId'] = location_id
    params['terrainIds'] = terrain_ids

    return query, params


@_send_query()
async def getSeasonsList() -> typing.List:
    """
        Get the list of seasons.
    """
    query = gql("""
    query {
        listSeasons {
        nodes {
            id
            from
            to
            seasonNumber
            active
            status
        }

        itemCount
        }
    }
    """)

    return query


@_send_query()
async def getCities() -> typing.Dict:
    """
        Get all cities where an Eva room is present.
    """
    params = {}

    query = gql("""
    query (
        $search: String
        $country: CountryEnum
        $sortOrder: SortOrderLocationsInput
    ) {
        locations(
        search: $search
        country: $country
        sortOrder: $sortOrder
        includesComingSoon: true
        ) {
        nodes {
            ... {
            id
            name
            playgroundName
            timezone
            emailContact
            department
            fullAddress
            isExternal
            sessionDuration
            sessionPriceConfiguration {
                peakHourSessionPrice
                offPeakHourSessionPrice
                offPeakHourSessionESportPrice
                peakHourSessionESportPrice
            }
            currency
            country
            telephone
            url
            geolocationPoint
            geolocationKmDistance
            isComingSoon
            defaultTags
            customTags
            tags
            visible
            abilities
            stripe {
                publicKey
            }
            }
        }
        }
    }
    """)

    params['search'] = ''
    params['sortOrder'] = {
        'by': 'COUNT_BOOKINGS_MONTHLY',
        'direction': 'DESC'
    }

    return query, params


@_send_query()
async def getCalendar(date: datetime.datetime, location_id: int = None) -> typing.Dict:
    """
        Get the calendar of an Eva room.
    """
    params = {}

    query = gql("""
    query($locationId: Int!, $currentDate: Date, $gameId: Int) {
        calendar(locationId: $locationId, currentDate: $currentDate) {
        firstDate
        currentDate
        lastDate
        location {
            id
            name
        }
        closingDays {
            date
            reason
        }
        sessionList(gameId: $gameId) {
            battlepassPercentage
            battlepassOpenSessionCount
            list {
            isPeakHour
            hasBattlepassAvailabilities
            slot {
                id
                date
                datetime
                startTime
                endTime
                duration
                locationId
            }

            availabilities {
                total
                totalESport
                available
                availableESport
                gameId
                hasBattlepassPlayer
                isESport
                isEmpty
                taken
                terrainId
                priority
                level
                session {
                terrainId
                slot {
                    id
                    date
                    datetime
                    startTime
                    endTime
                    duration
                    locationId
                }
                }
            }

            levelList
            sessionList {
                terrainId
                slot {
                id
                date
                datetime
                startTime
                endTime
                duration
                locationId
                }
            }
            }
        }
        }
    }
    """)

    params = {
        "locationId": location_id,
        "currentDate": date.strftime('%Y-%m-%d'),
        "gameId": None
    }

    return query, params


@_send_query()
async def getSession(slot_id: str, terrain_id: int) -> typing.Dict:
    """
        Returns the content of a session and players who have booked.

        Parameters
        ----------
        slot_id: Slot ID

        terrain_id: Terrain ID
    """
    params = {}

    query = gql(""" 
    query($slotId: String!, $terrainId: Int!) {
        getSession(slotId: $slotId, terrainId: $terrainId) {
        ... {
            ... {
            terrainId
            slot {
                id
                date
                datetime
                startTime
                endTime
                duration
                locationId
            }
            }

            bookingList {
            playerCount
            playerList {
                ... {
                userId
                username
                displayName
                }

                seasonPass {
                active
                }
                experience(gameId: 1) {
                level
                levelProgressionPercentage
                experience
                experienceForNextLevel
                experienceForCurrentLevel
                seasonId
                }
            }
            }
        }
        }
    }
    """)

    params['slotId'] = slot_id
    params["terrainId"] = terrain_id

    return query, params


@_send_query()
async def getLocation(location_id: int) -> typing.Dict:
    """
      Get the city from a location ID.

      Parameters
      ----------
      location_id: EVA location ID
    """
    params = {}

    query = gql(""" 
    query ($id: Int!) {
        location(id: $id) {
        ... {
            ... {
            id
            name
            playgroundName
            timezone
            emailContact
            department
            fullAddress
            isExternal
            sessionDuration
            sessionPriceConfiguration {
                peakHourSessionPrice
                offPeakHourSessionPrice
                offPeakHourSessionESportPrice
                peakHourSessionESportPrice
            }
            currency
            country
            telephone
            url
            geolocationPoint
            geolocationKmDistance
            isComingSoon
            defaultTags
            customTags
            tags
            visible
            abilities
            stripe {
                publicKey
            }
            }

            features {
            name
            availableCountries
            }

            details {
            games {
                id
                maxPlayer
                maxPlayerESport
                game {
                id
                name
                shortName
                maxPlayer
                maxPlayerESport
                minPlayer
                tags
                trailerFr
                trailerEn
                useMatchmaking
                }
            }
            terrains {
                ... {
                id
                name
                areaM2
                maxPlayer
                maxPlayerESport
                games {
                    gameId
                    maxPlayer
                    maxPlayerESport
                    isCompetitiveModeAvailable
                }
                }

                isClosed
            }
            }
        }

        offPeakHourSessionProduct {
            ... {
            name
            providerId
            baseProduct
            }
            price {
            amount
            currency
            providerId
            productProviderId
            }
        }
        offPeakHourSessionESportProduct {
            ... {
            name
            providerId
            baseProduct
            }
            price {
            amount
            currency
            providerId
            productProviderId
            }
        }
        peakHourSessionProduct {
            ... {
            name
            providerId
            baseProduct
            }
            price {
            amount
            currency
            providerId
            productProviderId
            }
        }
        peakHourSessionESportProduct {
            ... {
            name
            providerId
            baseProduct
            }
            price {
            amount
            currency
            providerId
            productProviderId
            }
        }
        }
    }
    """)

    params['id'] = location_id

    return query, params
