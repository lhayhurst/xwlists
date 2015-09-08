import myapp
from persistence import PersistenceManager, Pilot, ShipPilot
from xwingmetadata import T_70_CANON_NAME, TIE_FO_FIGHTER_CANON_NAME, ships, T_70, TIE_FO_FIGHTER, EPT_CANON, MOD_CANON, \
    DROID_CANON, TECH_CANON

__author__ = 'lhayhurst'

ship_canon_names = [ T_70_CANON_NAME, TIE_FO_FIGHTER_CANON_NAME ]

ship_pilots = \
    {
        T_70_CANON_NAME: ships[T_70],
        TIE_FO_FIGHTER_CANON_NAME: ships[TIE_FO_FIGHTER]
    }

upgrades = {
            EPT_CANON: [{'name': 'Wired', 'canon_name': 'wired', 'cost': 1}],
            TECH_CANON: [{'name': 'Weapons Guidance', 'canon_name': 'weaponsguidance', 'cost': 2}],
            DROID_CANON: [ {'name': 'BB-8', 'cost': 2, 'canon_name': 'bb8'},
                           {'name': 'R5-X3', 'cost': 1, 'canon_name': 'r5x3'}]
}

if __name__ == "__main__":
    for ship in ship_canon_names:
        pilots = ship_pilots[ship]
        for pilot in pilots:
            sql = "insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( '%s','%s', '%d', '%d' );" % \
                  ( pilot['name'],  pilot['canon_name'], pilot['cost'], pilot['pilot_skill']  )

            print sql

            sql = "insert into ship_pilot ( ship_type, pilot_id) select '%s', id from pilot where canon_name='%s';" %\
                  ( ship, pilot['canon_name'])

            print sql

    for upgrade_type in upgrades.keys():
        for upgrade in upgrades[upgrade_type]:
            sql = "insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( '%s', '%s', '%s', '%d');" %\
            ( upgrade_type, upgrade['name'], upgrade['canon_name'], upgrade['cost']  )
            print sql

