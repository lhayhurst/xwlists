import json
import urllib2
from BeautifulSoup import BeautifulSoup
from persistence import TourneyList, Faction, Ship, ShipUpgrade, ArchtypeList


class XWSListConverter:
    def __init__(self, list):
        self.data = {}
        self.data['faction'] = str(list.faction().value)
        pilots = []
        self.data['pilots'] = pilots
        self.data['version'] = "0.2.1"
        self.data['vendor'] = { 'listjuggler': {} }

        for ship in list.ships:
            sp = ship.ship_pilot
            p  = sp.pilot
            pilot_href = {}
            pilots.append( pilot_href )
            pilot_href[ "name"]   = p.canon_name
            pilot_href[ "ship"]   = str(sp.ship_type.value)
            pilot_upgrades = {}
            if len(ship.upgrades) > 0:
                pilot_href['upgrades'] = pilot_upgrades
            for ship_upgrade in ship.upgrades:
                ut = str(ship_upgrade.upgrade.upgrade_type.value)
                if not pilot_upgrades.has_key(ut):
                    pilot_upgrades[ut] = []
                pilot_upgrades[ut].append( ship_upgrade.upgrade.canon_name)



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
        code = full_code_div.find('code')

        if code is None:
            return None

        xws = json.loads(code.text )
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
        #TODO: temporary hack
        if faction == "rebels":
            faction = "rebel"
        if faction == "empire":
            faction = "imperial"

        tourney_list.faction = Faction.from_string(faction)


        points = 0
        ships = []

        for ship_pilot in pilots:
            ship = ship_pilot['ship']
            pilot = ship_pilot['name']
            sp          = pm.get_canonical_ship_pilot( ship, pilot )
            if sp is None:
                raise Exception("xws lookup failed for ship " + ship + ", pilot " + pilot )
            points      = points + sp.pilot.cost
            ship        = Ship( ship_pilot=sp)
            ships.append(ship)

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
                        ship_upgrade = ShipUpgrade( ship=ship, upgrade=upgrade )
                        ship.upgrades.append( ship_upgrade )

        if archtype is None:
            #ding ding!
            #we've never seen this list before!
            #note that this quote is a dupe of the add_squads method in xwlists.py
            #refactor it if we get a third way of adding archtypes
            archtype = ArchtypeList()
            pm.db_connector.get_session().add(archtype)
            archtype.ships = ships
            for ship in ships:
                ship.archtype = archtype
                pm.db_connector.get_session().add(ship)
            #TODO: temporary hack
            if faction == "rebel":
                faction = "rebels"
            if faction == "imperial":
                faction = "empire"
            archtype.faction = Faction.from_string( faction )
            archtype.points = points
            pm.db_connector.get_session().commit()

        tourney_list.archtype = archtype
        tourney_list.archtype_id = archtype.id
        pm.db_connector.get_session().add(tourney_list)
        pm.db_connector.get_session().commit()