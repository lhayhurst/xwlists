import json
import sys
import myapp
from persistence import Pilot
from xwingmetadata import XWingMetaData

if __name__ == '__main__':
    ships_file  = sys.argv[1]
    pilots_file = sys.argv[2]
    upgrades_file = sys.argv[3]


    ship_map    = {}
    pilot_map   = {}
    upgrade_map = {}

    with open(ships_file) as data_file:
        ships = json.loads(data_file.read())
        for ship in ships:
            ship_map[ship["name"]] = ship
            #todo: implement new ships


    session = myapp.db_connector.get_session()

    #listjuggler doesn't support epic
    pilot_exclusions = ( "GR-75 Medium Transport", \
                   "CR90 Corvette (Fore)", \
                   "CR90 Corvette (Aft)", \
                   "Raider-class Corvette (Fore)", \
                   "Raider-class Corvette (Aft)",\
                   "Nashtah Pup Pilot", \
                   "Gozanti-Class Cruiser", \
                   "C-ROC Cruiser", )

    with open(pilots_file) as data_file:
        pilots = json.loads(data_file.read())
        for pilot in pilots:
            p = pilot['name']
            db_pilot = session.query(Pilot).filter(Pilot.name ==p).first()
            if db_pilot is None:
                if not pilot['name'] in pilot_exclusions:
                    #print pilot['name']
                    sql = "insert into pilot ( name, canon_name, cost, pilot_skill  ) " \
                          "values ( '%s','%s', '%d', '%d' );" % \
                          (pilot['name'], pilot['xws'], pilot['points'], pilot['skill'])
                    print sql
                    sql = "insert  ship_pilot ( ship_type, pilot_id) " \
                          "select '%s', id from pilot where name='%s' and canon_name='%s';" % \
                          (ship_map[ pilot['ship']]['xws'],
                           pilot['name'],
                           pilot['xws'])
                    print sql



#    with open(upgrades_file) as data_file:
#        upgrades = json.loads(data_file.read())


    #verify the metadata struct
    mships = XWingMetaData().ships_full()
    for s in mships.keys():
        sh = mships[s]
        for p in sh:
            db_pilot = session.query(Pilot).filter(Pilot.name ==p['name']).first()
            if db_pilot is None:
                1
                print p['name']
