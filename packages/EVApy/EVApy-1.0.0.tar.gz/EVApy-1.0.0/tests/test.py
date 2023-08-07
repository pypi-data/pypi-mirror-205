import asyncio
import EVA.EVA as eva

async def main():
    # Get stats for a given player with it's discriminant
    # Ex. 'EVA_USERNAME#12345'
    player_stats = await eva.getStats(username='GAROH#64786')

    # Get all EVA cities for getting more informations
    # We need the ID of the city actually
    cities = await eva.getCities()

    # For example we get the ID of the first location in 'cities'.
    # It is the location ID for Tours city.
    location = await eva.getLocation(cities[0]['id']) # So location['id] = 15
    
    # So we can finally get Last Games of the player
    # We use the 'userId' of the player located in 'player_stats['player']['userId']'
    # And location ID from 'location['id']'
    last_games = await eva.getLastGames(player_stats['player']['userId'], 1, location['id'], items_limit=5)

    # We print every results to check values
    # Once every requests are done before, you can skip this part
    # And do whatever you want with these data.
    print("Player stats: ", player_stats, "\n")
    print("Last Games of this Player: ", last_games, "\n")
    print("EVA Location: ", location, "\n")
    print("EVA Cities: ", cities, "\n")

asyncio.run(main())