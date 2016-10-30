from xwingmetadata import VCX100_CANON_NAME, ATTACK_SHUTTLE_CANON_NAME, \
    G1A_STARFIGHTER_CANON_NAME, TIE_ADVANCED_PROTOTYPE_CANON_NAME, ships, ATTACK_SHUTTLE, TIE_ADVANCED_PROTOTYPE, \
    G1A_STARFIGHTER, VCX100, CREW_CANON, TITLE_CANON, EPT_CANON, SYSTEM_CANON, MOD_CANON, TIE_BOMBER, TIE_BOMBER_CANON

__author__ = 'lhayhurst'

ship_canon_names = [ VCX100_CANON_NAME, ATTACK_SHUTTLE_CANON_NAME,
                     TIE_ADVANCED_PROTOTYPE_CANON_NAME, G1A_STARFIGHTER_CANON_NAME, TIE_BOMBER_CANON]

ship_pilots = \
    {
        VCX100_CANON_NAME: ships[VCX100],
        ATTACK_SHUTTLE_CANON_NAME: ships[ATTACK_SHUTTLE],
        TIE_ADVANCED_PROTOTYPE_CANON_NAME: ships[TIE_ADVANCED_PROTOTYPE],
        G1A_STARFIGHTER_CANON_NAME: ships[G1A_STARFIGHTER],
        TIE_BOMBER_CANON: ships[TIE_BOMBER]
    }

upgrades = {
             CREW_CANON : [

        {'name': '4-Lom', 'canon_name': '4lom', 'cost': 1, },
        {'name': 'Zuckuss', 'canon_name': 'zuckuss', 'cost': 1, },
        {'name': 'Chopper', 'canon_name': 'chopper', 'cost': 0,},
        {'name': 'Hera Syndulla', 'canon_name': 'herasyndulla', 'cost': 1, },
        {'name': 'Zeb Orellios', 'canon_name': 'zeborellios', 'cost': 1, },
        {'name': 'Sabine Wren', 'canon_name': 'sabinewren', 'cost': 2, },
        {'name': 'Zeb Orellios', 'canon_name': 'zeborellios', 'cost': 1, },
        {'name': 'Ezra Bridger', 'canon_name': 'ezrabridger', 'cost': 3,},
        {'name': 'Kanan Jarrus', 'canon_name': 'kananjarrus', 'cost': 3, },
             ],

            TITLE_CANON: [
         {'name': 'Mist Hunter', 'cost': 0, 'canon_name' : 'misthunter',},
        {'name': 'Ghost', 'cost': 0, 'canon_name' : 'ghost',},
        {'name': 'Phantom', 'cost': 0, 'canon_name' : 'phantom',},
        {'name': 'Tie/v1', 'cost': 1, 'canon_name' : 'tiev1',},
            ],
             EPT_CANON: [
        {'name': 'Adaptability', 'cost': 0, 'canon_name':'adaptability'},
             ],
             SYSTEM_CANON: [         {'name': 'Electronic Baffle', 'canon_name': 'electronicbaffle', 'cost': 1}, ],
            MOD_CANON: [
                        {'name': 'Guidance Chips', 'canon_name': 'guidancechips', 'cost': 0},
        {'name': 'Long-Range Scanners', 'canon_name': 'longrangescanners', 'cost': 0},

            ]

}

if __name__ == "__main__":
    for ship in ship_canon_names:
        pilots = ship_pilots[ship]
        for pilot in pilots:
            if pilot.has_key( 'canon_name'):
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

