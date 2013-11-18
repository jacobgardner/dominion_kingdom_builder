Dominion Kingdom Builder
========================

There are other similar programs to this floating about the internet, but let me just float this one along too.  The other apps usually refer to themselves as dominion deck builders, but this is a bit of a misnomer since you're choosing decks to use in the supply.  

So _THIS_ app allows you to choose the 10 random decks to add to the supply (the Kingdom) in addition to the starting treasures, victory and curse cards.  (Actually, there's no enforcement of 10 decks to use in your Kingdom.)

The benefit of this app above the others are **NUMEROUS**.  Well at least a couple...

 * It's open source -- Add or remove features.  If I like your changes, I'll merge them.  If I don't like you're changes, I'll tell you why.  
 * Support for multiple supply piles from a single collection -- Have more than 6 people that want to play from your single collection of cards?  Well you can make completely non-conflicting kingdoms from the same collection. 
 * Card-type constraints -- Whether you want to play with no attack cards or nothing but them, you can set those constraints and customize your game.
 * Print out the kingdom alphabetically, sorted by cost, and/or grouped by expansion.  Whatever you want.


Prerequisites
-------------

Install the prerequisite programs:

	pip install -r requirements.txt


Usage
-----

```
python dominion.py [-h] [-d] [-g] [-s KEY] kingdoms

positional arguments:
  kingdoms              The number of kingdoms to create from a single
                        collection

optional arguments:
  -h, --help            show this help message and exit
  -d, --dominiondeck    When enabled, the deck is also generated at
                        dominiondeck.com
  -g, --group-by-set
  -s KEY, --sort-on KEY
                        Sort on 'name' or 'cost'.
```

License
-------

See [LICENSE.md](LICENSE.md) for software license information.
