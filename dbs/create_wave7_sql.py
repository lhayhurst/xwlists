import myapp
from persistence import PersistenceManager, Pilot, ShipPilot

__author__ = 'lhayhurst'

ships = ['yv666', 'kihraxzfighter', 'kwing', 'tiepunisher']

ship_pilots = \
    {
        'yv666': [
            {'name': 'Bossk', 'canon_name': 'bossk', 'pilot_skill': 7, 'cost' : 35},
            {'name': 'Moralo Eval', 'canon_name': 'moraloeval', 'pilot_skill': 6, 'cost' : 34 },
            {'name': 'Latts Razzi', 'canon_name': 'lattsrazzi', 'pilot_skill': 5, 'cost' : 33},
            {'name': 'Trandoshan Slaver', 'canon_name': 'trandoshanslaver', 'pilot_skill': 7, 'cost' : 29},

        ],
        'kihraxzfighter': [
            {'name': 'Talonbane Cobra', 'canon_name': 'talonbanecobra', 'pilot_skill': 9, 'cost' : 28 },
            {'name': 'Graz The Hunter', 'canon_name': 'grazthehunter', 'pilot_skill': 6, 'cost' : 25},
            {'name': 'Black Sun Ace', 'canon_name': 'blacksunace', 'pilot_skill': 5, 'cost' : 23},
            {'name': 'Cartel Marauder', 'canon_name': 'cartelmarauder', 'pilot_skill': 2, 'cost' : 20}
        ],
        'tiepunisher': [
            {'name': 'Redline', 'canon_name': 'redline', 'pilot_skill': 7, 'cost' : 27},
            {'name': 'Deathrain', 'canon_name': 'Deathrain', 'pilot_skill': 6, 'cost' : 26},
            {'name': 'Black Eight Sq. Pilot', 'canon_name': 'blackeightsqpilot', 'pilot_skill': 4, 'cost' :23} ,
            {'name': 'Cutlass Squadron Pilot', 'canon_name': 'cutlasssquadronpilot', 'pilot_skill': 2, 'cost' : 21},
        ],
        'kwing' : [
            {'name': 'Miranda Doni', 'canon_name': 'mirandadoni', 'pilot_skill': 8, 'cost' : 29},
            {'name': 'Esege Tuketu', 'canon_name': 'esegetuketu', 'pilot_skill': 6, 'cost' : 28},
            {'name': 'Guardian Squadron Pilot', 'canon_name': 'guardiansquadronpilot', 'pilot_skill': 4, 'cost' : 25},
            {'name': 'Warden Squadron Pilot', 'canon_name': 'wardensquadronpilot', 'pilot_skill': 2, 'cost' : 23},
        ]
    }

upgrades = {'ept': [{'name': 'Crack Shot', 'canon_name': 'crackshot', 'cost': 1},
                    {'name': 'Lightning Reflexes', 'canon_name': 'lightningreflexes', 'cost': 1},
                    ],
            'illicit': [{'name': 'Glitterstim', 'canon_name': 'glitterstim', 'cost': 2}, ],
            'title': [{'name': 'Hound\'s Tooth', 'canon_name': 'houndstooth', 'cost': 6}, ],
            'crew': [{'name': 'Bombardier', 'canon_name': 'bombardier', 'cost': 1},
                     {'name': 'Bossk', 'canon_name': 'bossk', 'cost': 2}],
            'mod': [{'name': 'Advanced SLAM', 'canon_name': 'advancedslam', 'cost': 2},
                    {'name': 'Twin Ion Engine Mk. II', 'canon_name': 'twinionenginemkii', 'cost': 1},
                    {'name': 'Maneuvering Fins', 'canon_name': 'maneuveringfins', 'cost': 1},
                    {'name': 'Ion Projector', 'canon_name': 'ionprojector', 'cost': 2}],
            'cannon': [],
            'turret': [{'name': 'Twin Laser Turret', 'canon_name': 'twinlaserturret', 'cost': 6}],
            'missile': [{'name': 'Adv. Homing Missiles', 'canon_name': 'advhomingmissiles', 'cost': 3}],
            'torpedo': [{'name': 'Extra Munitions', 'canon_name': 'extramunitions', 'cost': 2},
                        {'name': 'Plasma Torpedoes', 'canon_name': 'plasmatorpedoes', 'cost': 3}],
            'bomb': [{'name': 'Cluster Mines', 'canon_name': 'clustermines', 'cost': 4},
                     {'name': 'Ion Bombs', 'canon_name': 'ionbombs', 'cost': 2},
                     {'name': 'Conner Net', 'canon_name': 'connernet', 'cost': 4}],
            'samd': []

            }

if __name__ == "__main__":
    for ship in ships:
        pilots = ship_pilots[ship]
        for pilot in pilots:
            sql = "insert into pilot ( name, canon_name, cost, pilot_skill  ) values ( '%s','%s', '%d', '%d' );" % \
                  ( pilot['name'],  pilot['canon_name'], pilot['cost'], pilot['pilot_skill']  )

            #print sql

            sql = "insert into ship_pilot ( ship_type, pilot_id) select '%s', id from pilot where canon_name='%s';" %\
                  ( ship, pilot['canon_name'])

            print sql

    for upgrade_type in upgrades.keys():
        for upgrade in upgrades[upgrade_type]:
            sql = "insert into upgrade ( upgrade_type, name, canon_name, cost ) values ( '%s', '%s', '%s', '%d');" %\
            ( upgrade_type, upgrade['name'], upgrade['canon_name'], upgrade['cost']  )
            #print sql

