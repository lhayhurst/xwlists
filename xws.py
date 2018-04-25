import json
import urllib2
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
import re
from persistence import TourneyList, Faction, Ship, ShipUpgrade, ArchtypeList


class XWSListConverter:
    def __init__(self, archtype, provide_points = False):
        self.data = {}
        if archtype is None:
            return
        if archtype.faction is None:
            print "detected list with no faction!"
            pass
        else:
            self.data['faction'] = str(archtype.faction.value)

        if archtype is None:
            return

        pilots = []
        self.data['pilots'] = pilots
        self.data['version'] = "4.2.0"
        self.data['vendor'] = { 'listjuggler': {} }
        if provide_points:
            self.data['points'] = archtype.points

        for ship in archtype.ships:
            sp = ship.ship_pilot
            p  = sp.pilot
            pilot_href = {}
            pilots.append( pilot_href )
            pilot_href[ "name"]   = p.canon_name
            pilot_href[ "ship"]   = str(sp.ship_type.value)
            if provide_points:
                pilot_href["points"]    = sp.pilot.cost
            pilot_upgrades = {}
            if len(ship.upgrades) > 0:
                pilot_href['upgrades'] = pilot_upgrades

            #queue annoying hacks!
            has_vaksai   = archtype.has_vaksai()
            has_tiex1    = archtype.has_tiex1()
            has_renegade = archtype.has_renegade()

            for ship_upgrade in ship.upgrades:
                if ship_upgrade.upgrade is not None:
                    ut = str(ship_upgrade.upgrade.upgrade_type.value)
                    if not pilot_upgrades.has_key(ut):
                        pilot_upgrades[ut] = []
                    if provide_points:
                        pilot_upgrades[ut].append( {'name': ship_upgrade.upgrade.canon_name,
                                                    'points':ship_upgrade.upgrade.get_cost(has_vaksai=has_vaksai,
                                                                                           has_tiex1=has_tiex1,
                                                                                           has_renegade=has_renegade)
                                                    } )
                    else:
                        pilot_upgrades[ut].append( ship_upgrade.upgrade.canon_name)

class GeneralXWSFetcher:
    fab_root        = "x-wing.fabpsb.net"
    voidstate_root  = "xwing-builder.co.uk"
    yasb_root       = "geordanr.github.io/xwing"

    def fetch(self, url):
        xws = None
        if GeneralXWSFetcher.fab_root in url:
            xws = FabFetcher().fetch(url)
        elif GeneralXWSFetcher.voidstate_root in url:
            #pull the list id out of the url
            #http://xwing-builder.co.uk/xws/127077#view=full
            match = re.match( ".*?\/(\d+)", url )
            if match is None:
                return None
            xws = VoidStateXWSFetcher().fetch( match.group(1))
        elif GeneralXWSFetcher.yasb_root in url:
            #extract out the uri from the base
            o = urlparse( url )
            if o is None:
                return None
            xws = YASBFetcher().fetch(o.query)
        return xws


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
        url = "http://" + GeneralXWSFetcher.voidstate_root + "/xws/" + str(list_id) + "#view=full"
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

    def convert(self, pm, tourney_list=None):
        xws     = self.xws
        name    = None
        if xws.has_key( 'name' ):
            name    = xws['name']
        faction = xws['faction']
        pilots  = xws['pilots']

        #TODO: temporary hack
        if faction == "rebels":
            faction = "rebel"
        if faction == "empire":
            faction = "imperial"



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

                #this is a nasty hack but, what can you do
                hastiex1 = False
                has_vaksai = False
                has_renegade = False

                for upgrade_type in upgrades.keys():
                    if upgrade_type == 'title':
                        for title in upgrades[upgrade_type]:
                            if title == 'tiex1':
                                hastiex1 = True
                                break #TODO: if any one faction gets more than one way to modifiy points down, breaking here won't work!
                            if title == 'vaksai':
                                has_vaksai = True
                                break
                    if upgrade_type == 'torpedo':
                        for torp in upgrades[upgrade_type]:
                            if torp == 'renegaderefit':
                                has_renegade = True
                                break

                for upgrade_type in upgrades.keys():
                    if upgrade_type is None or upgrade_type == 'undefined':
                        raise Exception("got undefined upgrade type from xws source!" )


                    for upgrade_name in upgrades[upgrade_type]:
                        upgrade = pm.get_upgrade_canonical(upgrade_type, upgrade_name)
                        if upgrade is None:
                            raise Exception("xws lookup failed for upgrade " +  upgrade_name )
                        points = points + upgrade.get_cost( has_vaksai=has_vaksai, has_tiex1=hastiex1, has_renegade=has_renegade)
                        ship_upgrade = ShipUpgrade( ship=ship, upgrade=upgrade )

        hashkey = ArchtypeList.generate_hash_key(ships)

        archtype = pm.get_archtype_by_hashkey(hashkey)
        first_time_archtype_seen = False

        if archtype is None:
            #ding ding!
            #we've never seen this list before!
            #note that this quote is a dupe of the add_squads method in xwlists.py
            #refactor it if we get a third way of adding archtypes
            first_time_archtype_seen = True
            archtype = ArchtypeList()
            archtype.ships = ships
            for ship in ships:
                ship.archtype = archtype
                pm.db_connector.get_session().add(ship)

            archtype.faction = Faction.from_string( faction )
            archtype.points  = points
            archtype.pretty  = archtype.pretty_print_list()
            archtype.hashkey = hashkey

            pm.db_connector.get_session().add(archtype)
            pm.db_connector.get_session().commit()

        if tourney_list is not None:
            tourney_list.name = name
            tourney_list.faction = Faction.from_string(faction)
            tourney_list.archtype = archtype
            tourney_list.archtype_id = archtype.id
            pm.db_connector.get_session().add(tourney_list)
            pm.db_connector.get_session().commit()

        return archtype, first_time_archtype_seen