"""XWing Data Pull

Usage:
        xwing-data-pull.py [options] SHIP_FILE PILOTS_FILE UPGRADES_FILE all
        xwing-data-pull.py [options] SHIP_FILE PILOTS_FILE UPGRADES_FILE (ships|pilots|upgrades)

        simulate.py -h

Arguments:
        SHIP_FILE   JSON file with ships to process (from xwing-data)
        PILOTS_FILE JSON file with pilots to process (from xwing-data)
        UPGRADES_FILE JSON file with upgrades to process (from xwing-data)

        all         Run all steps in the data update
        ships       run just ships
        pilots      run just pilots
        upgrades    run just upgrades
Options:
        -h --help        show this message
        -v --verbose     show more information
        -r --report      report missing ships, pilots, or upgrades
        -d --db          generate db insert statements
        -m --metadata    generate meta data insert statements

The recommended way to run this job is to first run it with --report and all to see how far behind you are.
If ships are missing, you then run it with ships and --generate
"""

import json
import pprint
import sys
from docopt import docopt
import myapp
from persistence import Pilot, ShipPilot, PersistenceManager, UpgradeType
from xwingmetadata import XWingMetaData



if __name__ == '__main__':
    args = docopt(__doc__)
    ships_file  = args['SHIP_FILE']
    pilots_file = args['PILOTS_FILE']
    upgrades_file = args['UPGRADES_FILE']

    ship_map    = {}
    pilot_map   = {}
    upgrade_map = {}

    metadataupgrades = XWingMetaData().upgrades()
    metadataships    = XWingMetaData().ships_full()
    session = myapp.db_connector.get_session()
    pm = PersistenceManager(myapp.db_connector)


    pp = pprint.PrettyPrinter(indent=4)

    #listjuggler doesn't support epic
    ship_exclusions = ( "GR-75 Medium Transport", \
                   "CR90 Corvette (Fore)", \
                   "CR90 Corvette (Aft)", \
                   "Raider-class Corvette (Fore)", \
                   "Raider-class Corvette (Aft)",\
                   "Nashtah Pup Pilot", \
                   "Gozanti-class Cruiser", \
                   "C-ROC Cruiser", )

    with open(ships_file) as data_file:
        ships = json.loads(data_file.read())
        for ship in ships:
            ship_name = ship["name"]
            ship_map[ship_name] = ship
            #todo: implement new ships

            if args['ships']:
                if not metadataships.has_key(ship_name):
                    if ship_name not in ship_exclusions:
                        if args['--report']:
                            print "missing " + ship_name
                        if args['--db']:
                            ship_name_upper = ship_name.upper()
                            ship_name_canon = ship_name_upper + "_CANON_NAME"
                            print "%s = '%s'" % (ship_name_upper, ship_name)
                            print "%s = '%s'" % (ship_name_canon, ship['xws'])


    if args['pilots']:
        with open(pilots_file) as data_file:
            pilots = json.loads(data_file.read())
            for pilot in pilots:
                p = pilot['name']
                ship_xws = ship_map[ pilot['ship']]['xws']
                if not p in ship_exclusions:
#                    if 'Sabine' in str(p):
 #                       print pilot
                    db_pilot = pm.get_ship_pilot(pilot['ship'], p)
                    if db_pilot is None:
                        if args['--db']:
                            sql = "insert into pilot ( name, canon_name, cost, pilot_skill  ) " \
                                  "values ( '%s','%s', '%d', '%d' );" % \
                                  (pilot['name'], pilot['xws'], pilot['points'], pilot['skill'])
                            print sql
                            sql = "insert  ship_pilot ( ship_type, pilot_id) " \
                                  "select '%s', id from pilot where name='%s' and canon_name='%s';" % \
                                  (ship_xws,
                                   pilot['name'],
                                   pilot['xws'])
                            print sql
                        if args['--metadata']:
                            chassis = ship_map[pilot['ship']]
                            pp.pprint( { 'ship_size': chassis['size'], 'faction': None, 'name': pilot['name'], 'canon_name': pilot['xws'],
                                  'cost': pilot['points'],  'pilot_skill': pilot['skill'],
                                  'upgrades': (),'constraints': () } )




    if args['upgrades']:
        #epic stuff
        excluded_upgrades_slots = ['Cargo', 'Hardpoint', 'Team']
        with open(upgrades_file) as data_file:
            upgrades = json.loads(data_file.read())
            for u in upgrades:
                if u['slot'] not in excluded_upgrades_slots:
                    if u.has_key('size'):
                        if 'huge' in u['size']:
                            continue
                    upgrade_type = UpgradeType.from_description(u['slot']).value
                    ut = pm.get_upgrade_canonical(upgrade_type, u['xws'])
                    if ut is None:
                        if args['--db']:
                            print "insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( '%s', '%s', '%s', '%d');" % \
                                  ( upgrade_type, u['name'], u['xws'], u['points'])


