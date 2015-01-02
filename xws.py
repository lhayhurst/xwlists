import json
import urllib2
from bs4 import BeautifulSoup
from persistence import TourneyList, Faction, Ship, ShipUpgrade


class VoidStateXWSFetcher:

    def fetch(self, list_id):
        url = "http://xwing-builder.co.uk/xws/" + str(list_id) + "#view=full"
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup( html )
        full_code_div = soup.find(id= 'view_full')
        if full_code_div is None:
            return None
        codes = full_code_div.find_all('code')
        if len(codes) is not 1:
            return None
        code = codes[0].text

        if code is None:
            return None

        xws = json.loads(code )
        return xws

class XWSToJuggler:

    def __init__(self, xws ):
        self.xws = xws

    def convert(self, pm, tourney_list):
        xws     = self.xws
        name    = xws['name']
        faction = xws['faction']
        pilots  = xws['pilots']
        points  = xws['points']

        tourney_list.name = name
        tourney_list.faction = Faction.from_string(faction)
        tourney_list.points = points


        for ship_pilot in pilots:
            ship = ship_pilot['ship']
            pilot = ship_pilot['name']
            sp          = pm.get_canonical_ship_pilot( ship, pilot, )
            ship       = Ship( ship_pilot_id=sp.id, tlist_id=tourney_list.id)
            tourney_list.ships.append( ship )

            if ship_pilot.has_key('upgrades'):
                upgrades = ship_pilot['upgrades']
                for upgrade_type in upgrades.keys():
                    for upgrade_name in upgrades[upgrade_type]:
                        upgrade = pm.get_upgrade_canonical(upgrade_type, upgrade_name)
                        ship_upgrade = ShipUpgrade( ship_id=ship.id, upgrade=upgrade )
                        ship.upgrades.append( ship_upgrade )

