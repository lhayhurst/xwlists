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


    session = myapp.db_connector.get_session()

    with open(pilots_file) as data_file:
        pilots = json.loads(data_file.read())
        for pilot in pilots:
            p = pilot['name']
            db_pilot = session.query(Pilot).filter(Pilot.name ==p).first()
            if db_pilot is None:
                db_pilot = session.query(Pilot).filter(Pilot.name ==p).first()
                if db_pilot is None:
                    print pilot['name']


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
