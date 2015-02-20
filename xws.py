import json
import urllib2
from BeautifulSoup import BeautifulSoup
from persistence import TourneyList, Faction, Ship, ShipUpgrade


class FabFetcher:
    def fetch(self, fab_url):
        fab_url = fab_url + "&xws=1"
        response = urllib2.urlopen(fab_url)
        data = response.read()
        xws  = json.loads(data)
        return xws


class YASBFetcher:
    def fetch(self, yasb_uri):
        url = "https://yasb-xws.herokuapp.com/?" + yasb_uri
        response = urllib2.urlopen(url)
        data = response.read()
        xws  = json.loads(data)
        return xws

class VoidStateXWSFetcher:

    def fetch(self, list_id):
        url = "http://xwing-builder.co.uk/xws/" + str(list_id) + "#view=full"
        print "fetching url " + url
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
        name    = None
        if xws.has_key( name ):
            name    = xws['name']
        faction = xws['faction']
        pilots  = xws['pilots']

        tourney_list.name = name
        tourney_list.faction = Faction.from_string(faction)


        points = 0

        for ship_pilot in pilots:
            ship = ship_pilot['ship']
            pilot = ship_pilot['name']
            sp          = pm.get_canonical_ship_pilot( ship, pilot )
            if sp is None:
                raise Exception("xws lookup failed for ship " + ship + ", pilot " + pilot )
            points      = points + sp.pilot.cost
            ship        = Ship( ship_pilot_id=sp.id, tlist_id=tourney_list.id)
            tourney_list.ships.append( ship )

            if ship_pilot.has_key('upgrades'):
                upgrades = ship_pilot['upgrades']
                hastiex1 = False
                #this is a nasty hack but, what can you do
                for upgrade_type in upgrades.keys():
                    if upgrade_type == 'title':
                        for title in upgrades[upgrade_type]:
                            if title == 'tiex1':
                                hastiex1 = True
                                break

                for upgrade_type in upgrades.keys():
                    if upgrade_type is None or upgrade_type == 'undefined':
                        raise Exception("got undefined upgrade type from xws source!" )


                    for upgrade_name in upgrades[upgrade_type]:
                        upgrade = pm.get_upgrade_canonical(upgrade_type, upgrade_name)
                        if upgrade is None:
                            raise Exception("xws lookup failed for upgrade " +  upgrade_name )
                        if hastiex1 and upgrade_type=='system':
                            cost = upgrade.cost
                            cost = cost - 4
                            if cost < 0:
                                cost = 0
                            points  = points + cost
                        else:
                            points  = points + upgrade.cost
                        ship_upgrade = ShipUpgrade( ship_id=ship.id, upgrade=upgrade )
                        ship.upgrades.append( ship_upgrade )

        tourney_list.points = points