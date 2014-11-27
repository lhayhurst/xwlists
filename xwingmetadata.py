__author__ = 'lhayhurst'

VT_DECIMATOR = 'VT-49 Decimator'
TIE_PHANTOM = 'TIE Phantom'
TIE_DEFENDER = 'TIE Defender'
TIE_BOMBER = 'TIE Bomber'
LAMBDA_SHUTTLE = 'Lambda Shuttle'
FIRESPRAY_31 = 'Firespray-31'
TIE_INTERCEPTOR = 'TIE Interceptor'
TIE_ADVANCED = 'TIE Advanced'
TIE_FIGHTER = 'TIE Fighter'
YT_2400 = 'YT-2400'
Z95_HEADHUNTER = 'Z-95 Headhunter'
E_WING = 'E-Wing'
HWK_290 = 'HWK-290'
B_WING = 'B-Wing'
YT_1300 = 'YT-1300'
A_WING = 'A-Wing'
Y_WING = 'Y-Wing'
X_WING = 'X-Wing'

DROID = 'Astromech Droid'
TORPEDO = 'Torpedo'
MOD = "Modification"
EPT = "Elite Pilot Talent"
TITLE = "Title"
TURRET = "Turret Weapon"
MISSILE = "Missile"
CREW = "Crew"
SYSTEM = "System"
CANNON = "Cannon"
BOMB = "Bomb"

SHIP_SIZE = 'SHIP_SIZE'
SHIP_TYPE = 'SHIP_TYPE'
SMALL_SHIP = "SMALL_SHIP"
LARGE_SHIP = "LARGE_SHIP"
PER_SQUAD = "PER_SQUAD"
UNIQUE = "UNIQUE"
REBEL = "Rebel"
IMPERIAL = "Imperial"
FACTION = "FACTION"
ADD_EPT = "ADD_EPT"

PER_SQUAD_UNIQUE_CONSTRAINT = {'type': PER_SQUAD, 'value': UNIQUE}
REBEL_FACTION_CONSTRAINT = {'type': FACTION, 'value': REBEL}
IMPERIAL_FACTION_CONSTRAINT = {'type': FACTION, 'value': IMPERIAL}

upgrades = {
    CREW: (
        {'name': 'Intelligence Agent', 'cost': 1},
        {'name': 'Mercenary Copilot', 'cost': 2},
        {'name': 'Saboteur', 'cost': 2},
        {'name': 'Tactician', 'cost': 2},
        {'name': 'Weapons Engineer', 'cost': 3},
        {'name': 'Recon Specialist', 'cost': 3},
        {'name': 'Navigator', 'cost': 3},
        {'name': 'Flight Instructor', 'cost': 4},
        {'name': 'Gunner', 'cost': 5},
        {'name': 'Nien Nunb', 'cost': 1, 'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Han Solo', 'cost': 2, 'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT ),},
        {'name': 'Jan Ors', 'cost': 2, 'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT ),},
        {'name': 'Dash Rendar', 'cost': 2, 'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Leebo', 'cost': 2, 'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT ),},
        {'name': 'C-3PO', 'cost': 3, 'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Kyle Katarn', 'cost': 3, 'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Lando Calrissian', 'cost': 3,
         'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Chewbacca', 'cost': 4, 'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Leia Organa', 'cost': 4, 'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'R2-D2', 'cost': 4, 'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Luke Skywalker', 'cost': 7, 'constraints': ( REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Moff Jerjerrod', 'cost': 2,
         'constraints': ( IMPERIAL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT ),},
        {'name': 'Darth Vader', 'cost': 3, 'constraints': ( IMPERIAL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT ),},
        {'name': 'Rebel Captive', 'cost': 3,
         'constraints': ( IMPERIAL_FACTION_CONSTRAINT ),},
        {'name': 'Fleet Officer', 'cost': 3,
         'constraints': ( IMPERIAL_FACTION_CONSTRAINT  ),},
        {'name': 'Mara Jade', 'cost': 3, 'constraints': ( IMPERIAL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT ),},
        {'name': 'Ysanne Isard', 'cost': 4,
         'constraints': ( IMPERIAL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT ),},
    ),
    DROID: (
        {'name': 'R2 Astromech', 'cost': 1},
        {'name': 'R5 Astromech', 'cost': 1},
        {'name': 'R4-D6', 'cost': 1, 'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, )},
        {'name': 'R5-K6', 'cost': 2, 'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, )},
        {'name': 'R3-A2', 'cost': 2, 'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, )},
        {'name': 'R7 Astromech', 'cost': 2},
        {'name': 'R2-F2', 'cost': 3, 'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, )},
        {'name': 'R5-D8', 'cost': 3, 'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, )},
        {'name': 'R5-P9', 'cost': 3, 'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, )},
        {'name': 'R7-T1', 'cost': 3, 'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, )},
        {'name': 'R2-D2', 'cost': 4, 'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, )}
    ),
    TITLE: (
        {'name': 'Slave 1', 'cost': 0, 'constraints': ( {'type': SHIP_TYPE, 'value': FIRESPRAY_31})},
        {'name': 'Royal Guard TIE', 'cost': 0,
         'action': {'type': 'ADD_UPGRADE', 'value': MOD},
         'constraints': ( {'type': SHIP_TYPE, 'value': TIE_INTERCEPTOR})},
        {'name': 'A-Wing Test Pilot', 'cost': 0,
         'constraints': ({'type': SHIP_TYPE, 'value': A_WING}),
         'action': {'type': 'ADD_UPGRADE', 'value': EPT}},
        {'name': 'Millennium Falcon', 'cost': 1, 'constraints': ({'type': SHIP_TYPE, 'value': YT_1300})},
        {'name': 'Dauntless', 'cost': 2, 'constraints': ( {'type': SHIP_TYPE, 'value': VT_DECIMATOR})},
        {'name': 'Moldy Crow', 'cost': 3, 'constraints': ( {'type': SHIP_TYPE, 'value': HWK_290} )},
        {'name': 'ST-321', 'cost': 3, 'constraints': ( {'type': SHIP_TYPE, 'value': LAMBDA_SHUTTLE} )},
        {'name': 'Outrider', 'cost': 5, 'constraints': ( {'type': SHIP_TYPE, 'value': YT_2400} )},
    ),
    SYSTEM: (
        {'name': 'Enhanced Scopes', 'cost': 1},
        {'name': 'Fire-Control System', 'cost': 2},
        {'name': 'Advanced Sensors', 'cost': 3},
        {'name': 'Sensor Jammer', 'cost': 4},
    ),
    TURRET: (
        {'name': 'Blaster Turret', 'cost': 4},
        {'name': 'Ion Cannon Turret', 'cost': 5},
    ),
    TORPEDO: (
        {'name': 'Flechette Torpedoes', 'cost': 2},
        {'name': 'Proton Torpedos', 'cost': 4},
        {'name': 'Ion Torpedoes', 'cost': 5},
        {'name': 'Advanced Proton Torpedoes', 'cost': 6},
    ),
    BOMB: (
        {'name': 'Seismic Charges', 'cost': 2},
        {'name': 'Proximity Mines', 'cost': 3},
        {'name': 'Proton Bombs', 'cost': 5},
    ),
    CANNON: (
        {'name': 'Ion Cannon', 'cost': 3},
        {'name': 'AutoBlaster', 'cost': 5},
        {'name': 'Heavy Laser Cannon', 'cost': 7},
    ),
    MISSILE: (
        {'name': 'Chardaan Refit', 'cost': -2, 'constraints': ({'type': SHIP_TYPE, 'value': A_WING})},
        {'name': 'Ion Pulse Missle', 'cost': 3},
        {'name': 'Proton Rockets', 'cost': 3},
        {'name': 'Concussion Missiles', 'cost': 4},
        {'name': 'Cluster Missiles', 'cost': 4},
        {'name': 'Assault Missiles', 'cost': 5},
        {'name': 'Homing Missiles', 'cost': 5},
    ),
    MOD: (
        {'name': 'Munitions Failsafe', 'cost': 1},
        {'name': 'Tactical Jammer', 'cost': 1, 'constraints': ( {'type': SHIP_SIZE, 'value': LARGE_SHIP})},
        {'name': 'Targeting Computer', 'cost': 2},
        {'name': 'Anti-Pursuit Lasers', 'cost': 2, 'constraints': ( {'type': SHIP_SIZE, 'value': LARGE_SHIP} )},
        {'name': 'Stygium Particle Accelerator', 'cost': 2,
         'constraints': ( {'type': SHIP_TYPE, 'value': TIE_PHANTOM} )},
        {'name': 'Advanced Cloaking Device', 'cost': 3, 'constraints': ( {'type': SHIP_TYPE, 'value': TIE_PHANTOM})},
        {'name': 'Experimental Interface', 'cost': 3},
        {'name': 'B-Wing/E2', 'cost': 3, 'constraints': ( {'type': SHIP_TYPE, 'value': B_WING} )},
        {'name': 'Stealth Device', 'cost': 3},
        {'name': 'Hull Upgrade', 'cost': 3},
        {'name': 'Shield Upgrade', 'cost': 4},
        {'name': 'Counter-Measures', 'cost': 3, 'constraints': ( {'type': SHIP_SIZE, 'value': LARGE_SHIP} )},
        {'name': 'Engine Upgrade', 'cost': 4},
    ),

    EPT:
        ( {'name': 'Adrenaline Rush', 'cost': 1},
          {'name': 'Deadeye', 'cost': 1},
          {'name': 'Determination', 'cost': 1},
          {'name': 'Draw Their Fire', 'cost': 1},
          {'name': 'Veteran Instincts', 'cost': 1},
          {'name': 'Swarm Tactics', 'cost': 2},
          {'name': 'Squad Leader', 'cost': 2},
          {'name': 'Expert Handling', 'cost': 2},
          {'name': 'Elusiveness', 'cost': 2},
          {'name': 'Wingman', 'cost': 2},
          {'name': 'Decoy', 'cost': 2},
          {'name': 'Lone Wolf', 'cost': 2},
          {'name': 'Stay on Target', 'cost': 2},
          {'name': 'Intimidation', 'cost': 2},
          {'name': 'Push the Limit', 'cost': 3},
          {'name': 'Marksmanship', 'cost': 3},
          {'name': 'Daredevil', 'cost': 3},
          {'name': 'Outmaneuver', 'cost': 3},
          {'name': 'Predator', 'cost': 3},
          {'name': 'Ruthlessness', 'cost': 3},
          {'name': 'Expose', 'cost': 4},
          {'name': 'Opportunist', 'cost': 4},

        ),
}

ships = {X_WING: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Wedge Antilles', 'cost': 29,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (DROID, TORPEDO, MOD, EPT)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Luke Skywalker', 'cost': 28,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (DROID, TORPEDO, MOD, EPT)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Wes Janson', 'cost': 29,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (DROID, TORPEDO, MOD, EPT)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Jek Porkins', 'cost': 26,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (DROID, TORPEDO, MOD, EPT)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Red Squadron Pilot', 'cost': 23,
                   'upgrades': (DROID, TORPEDO, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Garven Dreis', 'cost': 26,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (DROID, TORPEDO, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Rookie Pilot', 'cost': 21,
                   'upgrades': (DROID, TORPEDO, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Biggs Darklighter', 'cost': 25,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (DROID, TORPEDO, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Hobbie" Klivian', 'cost': 25,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (DROID, TORPEDO, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Tarn Mison', 'cost': 23,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (DROID, TORPEDO, MOD)} ),

         Y_WING: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Horton Salm', 'cost': 25,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Gray Squadron Pilot', 'cost': 20,
                   'upgrades': (TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Dutch Vander', 'cost': 23,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Gold Squadron Pilot', 'cost': 18,
                   'upgrades': (TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD)} ),

         A_WING: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Tycho Celchu', 'cost': 26,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (TITLE, MISSILE, EPT, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Green Sq. Pilot', 'cost': 19,
                   'upgrades': (TITLE, MISSILE, EPT, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Arvel Crynyd', 'cost': 23,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (TITLE, MISSILE, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Prototype Pilot', 'cost': 17,
                   'upgrades': (TITLE, MISSILE, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Gemmer Sojan', 'cost': 22,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (TITLE, MISSILE, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Jake Farrell', 'cost': 24,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (TITLE, MISSILE, EPT, MOD)} ),

         YT_1300: ({'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Han Solo', 'cost': 46,
                    'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                    'upgrades': (EPT, MISSILE, TITLE, MOD, CREW, CREW)},
                   {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Chewbacca', 'cost': 42,
                    'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                    'upgrades': (EPT, MISSILE, TITLE, MOD, CREW, CREW)},
                   {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Lando Calrissian', 'cost': 44,
                    'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                    'upgrades': (EPT, MISSILE, TITLE, MOD, CREW, CREW)},
                   {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Outer Rim Smuggler', 'cost': 27,
                    'upgrades': (CREW, CREW, TITLE, MOD)} ),

         B_WING: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Ten Numb', 'cost': 31,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Keyan Farlander', 'cost': 29,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Ibtisam', 'cost': 28,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Nera Dantels', 'cost': 26,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Dagger Sq. Pilot', 'cost': 24,
                   'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Blue Sq. Pilot', 'cost': 22,
                   'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, MOD)} ),

         HWK_290: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Jan Ors', 'cost': 25,
                    'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                    'upgrades': (EPT, TURRET, CREW, TITLE, MOD)},
                   {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Kyle Katarn', 'cost': 21,
                    'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                    'upgrades': (EPT, TURRET, CREW, TITLE, MOD)},
                   {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Roark Garnet', 'cost': 19,
                    'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                    'upgrades': (TURRET, CREW, TITLE, MOD)},
                   {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Rebel Operative', 'cost': 16,
                    'upgrades': (TURRET, CREW, TITLE, MOD)} ),


         E_WING: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Corran Horn', 'cost': 35,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (DROID, TORPEDO, SYSTEM, EPT, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Etahn A\'Baht', 'cost': 32,
                   'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                   'upgrades': (DROID, TORPEDO, SYSTEM, EPT, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Blackmoon Squadron Pilot', 'cost': 29,
                   'upgrades': (DROID, TORPEDO, SYSTEM, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Knave Squadron Pilot', 'cost': 27,
                   'upgrades': (DROID, TORPEDO, SYSTEM, MOD)} ),

         Z95_HEADHUNTER: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Airen Cracken', 'cost': 19,
                           'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                           'upgrades': (MISSILE, EPT, MOD)},
                          {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Lt. Blount', 'cost': 17,
                           'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                           'upgrades': (MISSILE, EPT, MOD)},
                          {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Tala Squadron Pilot', 'cost': 13,
                           'upgrades': (MISSILE, MOD)},
                          {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Bandit Squadron Pilot', 'cost': 12,
                           'upgrades': (MISSILE, MOD)} ),

         YT_2400: ({'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Dash Rendar', 'cost': 36,
                    'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                    'upgrades': (EPT, CANNON, MISSILE, CREW, TITLE, MOD)},
                   {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Leebo', 'cost': 34,
                    'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                    'upgrades': (EPT, CANNON, MISSILE, CREW, TITLE, MOD)},
                   {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Eaden Vrill', 'cost': 32,
                    'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                    'upgrades': (CANNON, MISSILE, CREW, TITLE, MOD)},
                   {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Wild Space Fringer', 'cost': 30,
                    'upgrades': (CANNON, MISSILE, CREW, TITLE, MOD)} ),

         TIE_FIGHTER: (
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Howlrunner', 'cost': 18,
              'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ), 'upgrades': (EPT, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Mauler Mithel', 'cost': 17,
              'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ), 'upgrades': (EPT, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Dark Curse', 'cost': 16,
              'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ), 'upgrades': (MOD,'' )},
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Backstabber', 'cost': 16,
              'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ), 'upgrades': (MOD,'' )},
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Winged Gundark', 'cost': 15,
              'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ), 'upgrades': (MOD,)},
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Night Beast', 'cost': 15,
              'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ), 'upgrades': (MOD,)},
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Black Squadron Pilot', 'cost': 14,
              'upgrades': (EPT, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Obsidian Squadron Pilot', 'cost': 13,
              'upgrades': (MOD,'')},
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Academy Pilot', 'cost': 13, 'upgrades': (MOD,) }
         ),

         TIE_ADVANCED: ({'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Darth Vader', 'cost': 29,
                         'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                         'upgrades': (MISSILE, EPT, MOD)},
                        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Maarek Steel', 'cost': 27,
                         'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                         'upgrades': (MISSILE, EPT, MOD)},
                        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Storm Squadron Pilot', 'cost': 23,
                         'upgrades': (MISSILE, MOD)},
                        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Tempest Squadron Pilot', 'cost': 21,
                         'upgrades': (MISSILE, MOD)} ),

         TIE_INTERCEPTOR: ({'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Soontir Fel', 'cost': 27,
                            'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                            'upgrades': (TITLE, EPT, MOD)},
                           {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Carnor Jax', 'cost': 26,
                            'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                            'upgrades': (TITLE, EPT, MOD)},
                           {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Turr Phennir', 'cost': 25,
                            'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                            'upgrades': (TITLE, EPT, MOD)},
                           {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Tetran Cowall', 'cost': 24,
                            'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                            'upgrades': (TITLE, EPT, MOD)},
                           {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Kir Kanos', 'cost': 24,
                            'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                            'upgrades': (TITLE, MOD)},
                           {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Lt. Lorrir', 'cost': 23,
                            'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                            'upgrades': (TITLE, MOD)},
                           {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Fel\'s Wrath', 'cost': 23,
                            'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                            'upgrades': (TITLE, MOD)},
                           {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Royal Guard Pilot', 'cost': 22,
                            'upgrades': (TITLE, EPT, MOD)},
                           {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Saber Squadron Pilot', 'cost': 21,
                            'upgrades': (TITLE, EPT, MOD)},
                           {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Avenger Squadron Pilot', 'cost': 20,
                            'upgrades': (TITLE, MOD)},
                           {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Alpha Squadron Pilot', 'cost': 18,
                            'upgrades': (TITLE, MOD)} ),

         FIRESPRAY_31: ({'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Boba Fett', 'cost': 39,
                         'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                         'upgrades': (MISSILE, CANNON, BOMB, EPT, TITLE, MOD, CREW)},
                        {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Kath Scarlet', 'cost': 38,
                         'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                         'upgrades': (MISSILE, CANNON, BOMB, EPT, TITLE, MOD, CREW)},
                        {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Krassis Trelix', 'cost': 36,
                         'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                         'upgrades': (MISSILE, CANNON, BOMB, TITLE, MOD, CREW)},
                        {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Bounty Hunter', 'cost': 33,
                         'upgrades': (MISSILE, CANNON, BOMB, TITLE, MOD, CREW)}, ),

         LAMBDA_SHUTTLE: ({'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Captain Kagi', 'cost': 27,
                           'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                           'upgrades': (SYSTEM, CANNON, CREW, CREW, TITLE, MOD)},
                          {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Colonel Jendon', 'cost': 26,
                           'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                           'upgrades': (SYSTEM, CANNON, CREW, CREW, TITLE, MOD)},
                          {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Captain Yorr', 'cost': 24,
                           'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                           'upgrades': (SYSTEM, CANNON, CREW, CREW, TITLE, MOD)},
                          {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Omicron Group Pilot', 'cost': 21,
                           'upgrades': (SYSTEM, CANNON, CREW, CREW, TITLE, MOD)} ),

         TIE_BOMBER: (
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Major Rhymer', 'cost': 26,
              'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
              'upgrades': (TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD, EPT)},
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Captain Jonus', 'cost': 22,
              'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
              'upgrades': (TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD, EPT)},
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Gamma Squadron. Pilot', 'cost': 18,
              'upgrades': (TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Scimitar Squadron Pilot', 'cost': 16,
              'upgrades': (TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD)} ),

         TIE_DEFENDER: ({'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Rexler Brath', 'cost': 37,
                         'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                         'upgrades': (MISSILE, CANNON, MOD, EPT)},
                        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Col. Vessery', 'cost': 35,
                         'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                         'upgrades': (MISSILE, CANNON, MOD, EPT)},
                        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Onyx Squadron Pilot', 'cost': 32,
                         'upgrades': (MISSILE, CANNON, MOD)},
                        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Delta Squadron Pilot', 'cost': 30,
                         'upgrades': (MISSILE, CANNON, MOD)} ),

         TIE_PHANTOM: ({'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Whisper', 'cost': 32,
                        'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                        'upgrades': (CREW, SYSTEM, MOD, EPT)},
                       {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Echo', 'cost': 30,
                        'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
                        'upgrades': (CREW, SYSTEM, MOD, EPT)},
                       {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Shadow Squadron Pilot', 'cost': 27,
                        'upgrades': (CREW, SYSTEM, MOD)},
                       {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Sigma Squadron Pilot', 'cost': 25,
                        'upgrades': (CREW, SYSTEM, MOD)} ),

         VT_DECIMATOR: (
             {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Rear Admiral Chiraneau', 'cost': 46,
              'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
              'upgrades': (BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD, EPT)},
             {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Commander Kenkirk', 'cost': 44,
              'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
              'upgrades': (BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD, EPT)},
             {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Captain Oicunn', 'cost': 42,
              'constraints': ( PER_SQUAD_UNIQUE_CONSTRAINT, ),
              'upgrades': (BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD, EPT)},
             {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Patrol Leader', 'cost': 40,
              'upgrades': (BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD)} )}


class XWingMetaData:
    def is_rebel(self):
        self.is_rebel = True
        print ("is rebel")

    def is_imperial(self):
        self.is_rebel = False
        print ("is imp")

    def ships(self):
        return ships.keys()

    def upgrades(self):
        return upgrades

    def ships_full(self):
        return ships

    def pilots_for_ship(self, ship):
        return ships(ship)

    def droids(self):
        return self.upgrades()(DROID)

    def system_upgrades(self):
        return self.upgrades()(SYSTEM)

    def titles(self):
        return self.upgrades()(TITLE)

    def crew(self):
        return self.upgrades()(CREW)

    def epts(self):
        return self.upgrades()(EPT)

    def mods(self):
        return self.upgrades()(MOD)

    def bomb_mines(self):
        return self.upgrades()(BOMB)

    def cannons(self):
        return self.upgrades()(CANNON)

    def torpedos(self):
        return self.upgrades()(TORPEDO)

    def missiles(self):
        return self.upgrades()(MISSILE)

    def turrets(self):
        return self.upgrades()(TURRET)


class XWingList:
    def get_ship_for_id(self, id, request_form):
        ship = {}
        for k in request_form.keys():
            if k.endswith(id) and request_form(k) is not None and len(request_form(k)) > 0:
                ship[k] = request_form(k)
        return ship

    def get_ships_submitted(self, request_form):

        ret = []
        #8 ships is the most you can have, for now :-)
        for id in range(0, 7, 1):
            id = str(id)
            ship = self.get_ship_for_id(id, request_form)
            if len(ship.keys()) > 0:
                ret.append(ship)
        return ret

    def __init__(self, request_form):
        self.ships_submitted = self.get_ships_submitted(request_form)

