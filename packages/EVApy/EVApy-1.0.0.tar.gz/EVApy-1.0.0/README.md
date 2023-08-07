<h1 align='center'>EVA API</h1>
<p align="center">
<img src="https://github.com/LeGeRyChEeSe/EVApy/blob/main/images/eva_logo.jpg?raw=true" align="center" height=205 alt="EVApy" />
</p>
<p align="center">
<img src='https://visitor-badge.laobi.icu/badge?page_id=LeGeRyChEeSe.EVApy', alt='Visitors'/>
<a href="https://github.com/LeGeRyChEeSe/EVApy/stargazers">
<img src="https://img.shields.io/github/stars/LeGeRyChEeSe/EVApy" alt="Stars"/>
</a>
<a href="https://github.com/LeGeRyChEeSe/EVApy/issues">
<img src="https://img.shields.io/github/issues/LeGeRyChEeSe/EVApy" alt="Issues"/>
</a>

<p align="center">
This is the unofficial API for <a href="https://www.eva.gg/">EVA</a>.<br>
It's made for getting stats and previous games from a Player easily through the EVA API.<br>
There is also some other basic features like getting booking sessions from any EVA location.
<p align="center">

## Table of Contents
- [Installation](#installation)
- [Script Example](#script-example)
- [Contributing](#contributing)
- [License](#license)

## Installation

```python
pip install EVApy
```

## Script Example

- Here is an example of a simple script using EVA API

```python
import asyncio
import EVA.EVA as eva

async def main():
    # Get stats for a given player with it's discriminant
    # Ex. 'EVA_USERNAME#12345'
    player_stats = await eva.getStats(username='EVA_USERNAME#12345')

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
```

- Or you can use it in CLI

```python
>>> import asyncio
>>> import EVA.EVA as eva
>>> print(asyncio.run(eva.getStats(username='EVA_USERNAME#12345')))
```

## Contributing

Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewFeature`)
3. Commit your Changes (`git commit -m 'Add some NewFeature'`)
4. Push to the Branch (`git push origin feature/NewFeature`)
5. Open a Pull Request


*Thanks to every [contributors](https://github.com/LeGeRyChEeSe/EVApy/graphs/contributors) who have contributed in this project.*

## License

Distributed under the MIT License. See [LICENSE](https://github.com/LeGeRyChEeSe/EVApy/blob/main/LICENSE) for more information.

----

Author/Maintainer: [Garoh](https://github.com/LeGeRyChEeSe/) | Discord: GarohRL#4449