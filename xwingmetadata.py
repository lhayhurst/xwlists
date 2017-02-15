import re

__author__ = 'lhayhurst'

VT_DECIMATOR = 'VT-49 Decimator'
VT_DECIMATOR_CANON = 'vt49decimator'
TIE_PHANTOM = 'TIE Phantom'
TIE_PHANTOM_CANON = 'tiephantom'
TIE_PHANTOM_CANON = 'tiephantom'
TIE_DEFENDER = 'TIE Defender'
TIE_DEFENDER_CANON = 'tiedefender'
TIE_BOMBER = 'TIE Bomber'
TIE_BOMBER_CANON = 'tiebomber'
LAMBDA_SHUTTLE = 'Lambda-Class Shuttle'
LAMBDA_SHUTTLE_CANON = 'lambdaclassshuttle'
FIRESPRAY_31 = 'Firespray-31'
FIRESPRAY_31_CANON = 'firespray31'
TIE_INTERCEPTOR = 'TIE Interceptor'
TIE_INTERCEPTOR_CANON = 'tieinterceptor'
TIE_ADVANCED = 'TIE Advanced'
TIE_ADVANCED_CANON = 'tieadvanced'
TIE_FIGHTER = 'TIE Fighter'
TIE_FIGHTER_CANON = 'tiefighter'
YT_2400 = 'YT-2400 Freighter'
YT_2400_CANON = 'yt2400freighter'
Z95_HEADHUNTER = 'Z-95 Headhunter'
Z95_HEADHUNTER_CANON = 'z95headhunter'
E_WING = 'E-Wing'
E_WING_CANON = 'ewing'
HWK_290 = 'HWK-290'
HWK_290_CANON = 'hwk290'
B_WING = 'B-Wing'
B_WING_CANON = 'bwing'
YT_1300 = 'YT-1300'
YT_1300_CANON = 'yt1300'
A_WING = 'A-Wing'
A_WING_CANON = 'awing'
Y_WING = 'Y-Wing'
Y_WING_CANON = 'ywing'
X_WING = 'X-Wing'
X_WING_CANON = 'xwing'
T_70 = 'T-70 X-Wing'
T_70_CANON_NAME = 't70xwing'
TIE_FO_FIGHTER = 'Tie/fo Fighter'
TIE_FO_FIGHTER_CANON_NAME = 'tiefofighter'


# WAVE 6
STAR_VIPER_CANON = 'starviper'
STAR_VIPER = "Star Viper"
AGGRESSOR_CANON = 'aggressor'
AGGRESSOR = 'Aggressor'
M3_A_INTERCEPTOR_CANON = 'm3ainterceptor'
M3_A_INTERCEPTOR = 'M3-A Syck Interceptor'

# WAVE 7
KIHRAXZ_FIGHTER = "Kihraxz Fighter"
KIHRAXZ_FIGHTER_CANON_NAME = 'kihraxzfighter'
TIE_PUNISHER = 'TIE Punisher'
TIE_PUNISHER_CANON_NAME = 'tiepunisher'
YV_666_FREIGHTER = 'YV-666'
YV_666_FREIGHTER_CANON_NAME = 'yv666'
K_WING = 'K-Wing'
K_WING_CANON_NAME = 'kwing'

#wave 8
VCX100 = 'VCX-100'
VCX100_CANON_NAME = 'vcx100'
ATTACK_SHUTTLE = 'Attack Shuttle'
ATTACK_SHUTTLE_CANON_NAME = 'attackshuttle'
TIE_ADVANCED_PROTOTYPE = 'TIE Adv. Prototype'
TIE_ADVANCED_PROTOTYPE_CANON_NAME = 'tieadvprototype'
G1A_STARFIGHTER = 'G-1A Starfighter'
G1A_STARFIGHTER_CANON_NAME = 'g1astarfighter'
JUMPMASTER_5000_CANON_NAME = "jumpmaster5000"
JUMPMASTER_5000_ = "JumpMaster 5000"

#wave 9
TIE_SF_FIGHTER = 'TIE/sf Fighter'
TIE_SF_FIGHTER_CANON_NAME = 'tiesffighter'
ARC_170 = 'ARC-170'
ARC_170_CANON_NAME = 'arc170'
PROTECTORATE_STARFIGHTER = 'Protectorate Starfighter'
PROTECTORATE_STARFIGHTER_CANON_NAME = 'protectoratestarfighter'
LANCER_CLASS_PURSUIT_CRAFT = 'Lancer-craft Pursuit Craft'
LANCER_CLASS_PURSUIT_CRAFT_CANON_NAME = 'lancerclasspursuitcraft'

#wave 10
U_WING = 'U-Wing'
U_WING_CANON_NAME = 'uwing'

UPSILON_CLASS_SHUTTLE = 'Upsilon-Class Shuttle'
UPSILON_CLASS_SHUTTLE_CANON_NAME = 'upsilonclassshuttle'

QUADJUMPER = 'Quadjumper'
QUADJUMPER_CANON_NAME = 'quadjumper'

TIE_STRIKER = 'Tie Striker'
TIE_STRIKER_CANON_NAME = 'tiestriker'

EPT = "Elite Pilot Talent"
EPT_CANON = 'ept'
TITLE = "Title"
TITLE_CANON = 'title'
CREW = "Crew"
CREW_CANON = 'crew'
SYSTEM = 'System'
SYSTEM_CANON = 'system'
MOD = "Modification"
MOD_CANON = 'mod'
DROID = 'Astromech Droid'
DROID_CANON = 'amd'
CANNON = "Cannon"
CANNON_CANON = 'cannon'  # heh
TURRET = "Turret Weapon"
TURRET_CANON = 'turret'
MISSILE = "Missile"
MISSILE_CANON = 'missile'
TORPEDO = 'Torpedo'
TORPEDO_CANON = 'torpedo'
BOMB = "Bomb"
BOMB_CANON = 'bomb'
SALVAGED_ASTROMECH_DROID = 'Salvaged Astromech Droid'
SALVAGED_ASTROMECH_DROID_CANON = 'samd'
ILLICIT = 'Illicit'
ILLICIT_CANON = 'illicit'
TECH = 'Tech'
TECH_CANON = 'tech'

SHIP_SIZE = 'SHIP_SIZE'
SHIP_TYPE = 'SHIP_TYPE'
SMALL_SHIP = "SMALL_SHIP"
LARGE_SHIP = "LARGE_SHIP"
PER_SQUAD = "PER_SQUAD"
UNIQUE = "UNIQUE"
REBEL = "rebel"
IMPERIAL = "imperial"
SCUM = "scum"
FACTION = "FACTION"
ADD_EPT = "ADD_EPT"


# TDO: make this less ganky
def header():
    return ['Tourney', 'tourneyType', 'tourneyDate', 'player', FACTION, 'points', 'swiss_standing', 'elim_standing', \
            'listId', 'Ship', 'Pilot', EPT + ".1", EPT + ".2", TITLE, \
            CREW + ".1", CREW + ".2", CREW + ".3", \
            DROID, SYSTEM, MOD + ".1", MOD + ".2", \
            CANNON, MISSILE + ".1", MISSILE + ".2",
            TORPEDO + ".1", TORPEDO + ".2", BOMB, TURRET, TECH, SALVAGED_ASTROMECH_DROID, ILLICIT]


sets_and_expansions = {'Core Set': [],
                       'Wave 1': ['X-Wing Expansion', 'Y-Wing Expansion', 'TIE Fighter Expansion',
                                  'TIE Advanced x1 Expansion'],
                       'Wave 2': ['A-Wing Expansion', 'YT-1300 Expansion', 'TIE Interceptor Expansion',
                                  'Firespray-31 Expansion'],
                       'Wave 3': ['B-Wing Expansion', 'HWK-290 Expansion', 'Lambda Shuttle Expansion',
                                  'TIE Bomber Expansion', ],
                       'Imperial Aces Expansion': [],
                       'GR-75 Expansion': [],
                       'CR90 Expansion': [],
                       'Imperial Raider Expansion Pack': [],
                       'Wave 4': ['E-Wing Expansion', 'Z-95 Headhunter Expansion', 'TIE Defender Expansion',
                                  'TIE Phantom Expansion'],
                       'Rebel Aces Expansion': [],
                       'Wave 5': ['YT-2400 Expansion', 'VT-49 Decimator Expansion'],
                       'Wave 6': ['Most Wanted Expansion', 'StarViper Expansion', 'IG-2000 Expanson',
                                  'M3-A Interceptor Expansion'],
                       'Wave 7': ['K-Wing Expansion Pack', 'Kiharxz Fighter Expansion Pack',
                                  'Tie Punisher Expansion Pack', 'Hound\'s Tooth Expansion Pack'],
                       'Force Awakens Core Set': [],
                       'Wave 8': ['Punishing One Expansion Pack', 'Ghost Expansion Pack', 'Tie Inquisitor Expansion Pack',
                                  'T-70 X-Wing Expansion Pack,' 'Mist Hunter Expansion Pack', 'TIE/fo Expansion Pack'],
                       'Wave 9': ['Protectorate Starfighter Expansion Pack', 'ARC-170 Expansion Pack', 'Shadow Caster Expansion Pack', 'Special Forces TIE Expansion Pack'],
                       'Wave 10': ['Upsilon-class Shuttle Expansion Pack',
                                   'Sabine\'s TIE Fighter Expansion Pack',
                                   'Quadjumper Expansion Pack',
                                   'U-wing Expansion Pack',
                                   'TIE Striker Expansion Pack']
                       }

formats = {'Standard - 100 Point Dogfight', 'Epic Play - 300 points', 'Escalation'}
format_default = 'Standard - 100 Point Dogfight'

factions = [REBEL, IMPERIAL, SCUM]

PER_SQUAD_UNIQUE_CONSTRAINT = {'type': PER_SQUAD, 'value': UNIQUE}
REBEL_FACTION_CONSTRAINT = {'type': FACTION, 'value': REBEL}
IMPERIAL_FACTION_CONSTRAINT = {'type': FACTION, 'value': IMPERIAL}
SCUM_FACTION_CONSTRAINT = {'type': FACTION, 'value': SCUM}
XWING_CONSTRAINT = {'type': SHIP_TYPE, 'value': X_WING}
T70_CONSTRAINT = {'type': SHIP_TYPE, 'value': T_70}

# all the x-wing upgrades.
upgrades = {
    CREW: (

        {'name': 'Kylo Ren', 'canon_name': 'kyloren', 'cost': 3, 'constraints': (IMPERIAL_FACTION_CONSTRAINT)},


        {'name': 'Cikatro Vizago', 'canon_name': 'cikatrovizago', 'cost': 0, 'constraints': (SCUM_FACTION_CONSTRAINT)},


        {'name': 'BoShek', 'canon_name': 'boshek', 'cost': 2,},

        {'name': 'Bistan', 'canon_name': 'bistan', 'cost': 2,'constraints': (REBEL_FACTION_CONSTRAINT)},


        {'name': 'Inspiring Recruit', 'canon_name': 'inspiringrecruit', 'cost': 1,},

        {'name': 'Bodhi Rook', 'constraints': (REBEL_FACTION_CONSTRAINT),
         'canon_name': 'bodhirook', 'cost': 1,},

        {'name': 'Baze Malbus', 'constraints': (REBEL_FACTION_CONSTRAINT),
         'canon_name': 'bazemalbus', 'cost': 3,},


        {'name': 'Hotshot Co-Pilot', 'canon_name': 'hotshotcopilot', 'cost': 4,},

        {'name': 'Captain Rex', 'canon_name': 'captainrex', 'cost': 2,
         'constraints': (REBEL_FACTION_CONSTRAINT),},

        {'name': 'General Hux', 'canon_name': 'generalhux', 'cost': 5,
         'constraints': (IMPERIAL_FACTION_CONSTRAINT),},

        {'name': 'Operations Specialist', 'canon_name': 'operationsspecialist', 'cost': 3},

        {'name': 'Cassian Andor', 'canon_name': 'cassianandor', 'cost': 2,
         'constraints': (REBEL_FACTION_CONSTRAINT),},

        {'name': 'Jyn Erso', 'canon_name': 'jynerso', 'cost': 2,
         'constraints': (REBEL_FACTION_CONSTRAINT),},

        {'name': 'Rey', 'canon_name': 'rey', 'cost': 2,
         'constraints': (REBEL_FACTION_CONSTRAINT),},

        {'name': 'Finn', 'canon_name': 'finn', 'cost': 5,
         'constraints': (REBEL_FACTION_CONSTRAINT),},

        {'name': 'Tail Gunner', 'canon_name': 'tailgunner', 'cost': 2 },

        {'name': 'Ketsu Onyo', 'canon_name': 'ketsuonyo', 'cost': 1,
         'constraints': (SCUM_FACTION_CONSTRAINT),},


        {'name': 'IG-88D', 'canon_name': 'ig88d', 'cost': 1,
         'constraints': (SCUM_FACTION_CONSTRAINT),},

        {'name': 'Ketsu Onyo', 'canon_name': 'ketsuonyo', 'cost': 1,
         'constraints': (SCUM_FACTION_CONSTRAINT),},

        {'name': 'Latts Razzi', 'canon_name': 'lattsrazzi', 'cost': 2,
         'constraints': (SCUM_FACTION_CONSTRAINT),},


        {'name': 'Systems Officer', 'canon_name': 'systemsofficer', 'cost': 2,
         'constraints': (IMPERIAL_FACTION_CONSTRAINT),},
        {'name': 'Boba Fett', 'canon_name': 'bobafett', 'cost': 1,
         'constraints': (SCUM_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Gonk', 'canon_name': 'gonk', 'cost': 2,
         'constraints': (SCUM_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Dengar', 'canon_name': 'dengar', 'cost': 3,
         'constraints': (SCUM_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},

        {'name': '4-Lom', 'canon_name': '4lom', 'cost': 1, 'constraints': (SCUM_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Zuckuss', 'canon_name': 'zuckuss', 'cost': 1, 'constraints': (SCUM_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Chopper', 'canon_name': 'chopper', 'cost': 0, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Hera Syndulla', 'canon_name': 'herasyndulla', 'cost': 1, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Zeb Orellios', 'canon_name': 'zeborellios', 'cost': 1, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Sabine Wren', 'canon_name': 'sabinewren', 'cost': 2, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),
         'action': [{'type': 'ADD_UPGRADE', 'value': BOMB}],
         },
        {'name': 'Zeb Orellios', 'canon_name': 'zeborellios', 'cost': 1, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Ezra Bridger', 'canon_name': 'ezrabridger', 'cost': 3, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},
        {'name': 'Kanan Jarrus', 'canon_name': 'kananjarrus', 'cost': 3, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT),},

        {'name': 'Intelligence Agent', 'cost': 1},
        {'name': 'Mercenary Copilot', 'cost': 2},
        {'name': 'Saboteur', 'cost': 2},
        {'name': 'Tactician', 'cost': 2},
        {'name': 'Weapons Engineer', 'cost': 3},
        {'name': 'Recon Specialist', 'cost': 3},
        {'name': 'Navigator', 'cost': 3},
        {'name': 'Flight Instructor', 'cost': 4},
        {'name': 'Gunner', 'cost': 5},
        {'name': 'Nien Nunb', 'cost': 1, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Han Solo', 'cost': 2, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Jan Ors', 'cost': 2, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Dash Rendar', 'cost': 2, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Leebo', 'cost': 2, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'C-3PO', 'cost': 3, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Kyle Katarn', 'cost': 3, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Lando Calrissian', 'cost': 3,
         'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Chewbacca', 'cost': 4, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Leia Organa', 'cost': 4, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'R2-D2', 'cost': 4, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Luke Skywalker', 'cost': 7, 'constraints': (REBEL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Moff Jerjerrod', 'cost': 2,
         'constraints': (IMPERIAL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Darth Vader', 'cost': 3, 'constraints': (IMPERIAL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Rebel Captive', 'cost': 3,
         'constraints': (IMPERIAL_FACTION_CONSTRAINT), },
        {'name': 'Fleet Officer', 'cost': 3,
         'constraints': (IMPERIAL_FACTION_CONSTRAINT), },
        {'name': 'Mara Jade', 'cost': 3, 'constraints': (IMPERIAL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Agent Kallus', 'cost': 2,
         'constraints': (IMPERIAL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Ysanne Isard', 'cost': 4,
         'constraints': (IMPERIAL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'K4 Security Droid', 'cost': 3, 'constraints': (SCUM_FACTION_CONSTRAINT)},
        {'name': 'Greedo', 'cost': 1,
         'constraints': (SCUM_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT), },
        {'name': 'Outlaw Tech', 'cost': 2, 'constraints': (SCUM_FACTION_CONSTRAINT)},
        {'name': 'Emperor Palpatine', 'cost': 8,
         'constraints': (IMPERIAL_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT)},
        {'name': 'Bombardier', 'cost': 1},
        {'name': 'Bossk', 'cost': 2, 'constraints': (SCUM_FACTION_CONSTRAINT, PER_SQUAD_UNIQUE_CONSTRAINT)},
        {'name': 'Tail Gunner', 'cost': 2, },

    ),
    DROID: (

        {'name': 'M9-G8', 'cost': 3,'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT)},
        {'name': 'R2 Astromech', 'cost': 1},
        {'name': 'R5 Astromech', 'cost': 1},
        {'name': 'R3 Astromech', 'cost': 2},
        {'name': 'R4-D6', 'cost': 1, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,)},
        {'name': 'R5-K6', 'cost': 2, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,)},
        {'name': 'R3-A2', 'cost': 2, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,)},
        {'name': 'R7 Astromech', 'cost': 2},
        {'name': 'R2-F2', 'cost': 3, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,)},
        {'name': 'R5-D8', 'cost': 3, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,)},
        {'name': 'R5-P9', 'cost': 3, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,)},
        {'name': 'R7-T1', 'cost': 3, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,)},
        {'name': 'R2-D6', 'cost': 1, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'action': [{'type': 'ADD_UPGRADE', 'value': EPT}]},
        {'name': 'R2-D2', 'cost': 4, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,)},
        {'name': 'BB-8', 'cost': 2, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,)},
        {'name': 'R5-X3', 'cost': 1, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,)},
        {'name': 'Targetting Astromech', 'cost': 2},
        {'name': 'R3 Astromech', 'cost':2}

    ),
    TITLE: (

        {'name': 'Light Scyk Interceptor', 'canon_name': 'lightscykinterceptor', 'cost': -2,
          'constraints': ({'type': SHIP_TYPE, 'value': [M3_A_INTERCEPTOR] } ),},


        {'name': 'Pivot Wing', 'canon_name': 'pivotwing', 'cost': 0,
          'constraints': ({'type': SHIP_TYPE, 'value': [U_WING] } ),},

        {'name': 'Adaptive Ailerons', 'canon_name': 'adaptiveailerons', 'cost': 0,
          'constraints': ({'type': SHIP_TYPE, 'value': [TIE_STRIKER] } ),},

        {'name': 'Sabines Masterpiece', 'cost': 1, 'canon_name' : 'sabinesmasterpiece',
         'constraints': ({'type': SHIP_TYPE, 'value': TIE_FIGHTER}, {'faction': REBEL_FACTION_CONSTRAINT})},


        {'name': 'Kylo Rens Shuttle', 'cost': 2, 'canon_name' : 'kylorensshuttle',
         'constraints': ({'type': SHIP_TYPE, 'value': UPSILON_CLASS_SHUTTLE})},

        {'name': 'Concord Dawn Protector', 'cost': 1, 'canon_name' : 'concorddawnprotector',
         'constraints': ({'type': SHIP_TYPE, 'value': PROTECTORATE_STARFIGHTER})},

        {'name': 'Shadow Caster', 'cost': 3, 'canon_name' : 'shadowcaster',
         'constraints': ({'type': SHIP_TYPE, 'value': LANCER_CLASS_PURSUIT_CRAFT})},

        {'name': 'Alliance Overhaul', 'cost': 0, 'canon_name' : 'allianceoverhaul',
         'constraints': ({'type': SHIP_TYPE, 'value': ARC_170})},


        {'name': 'Special Ops Training', 'cost': 0, 'canon_name' : 'specialopstraining',
         'constraints': ({'type': SHIP_TYPE, 'value': TIE_SF_FIGHTER})},

        {'name': 'Black One', 'cost': 1, 'canon_name' : 'blackone',
         'constraints': ({'type': SHIP_TYPE, 'value': T_70})},


        {'name': 'Punishing One', 'cost': 12, 'canon_name' : 'punishingone',
         'constraints': ({'type': SHIP_TYPE, 'value': JUMPMASTER_5000_})},

        {'name': 'Mist Hunter', 'cost': 0, 'canon_name' : 'misthunter',
         'action': [{'type': 'ADD_UPGRADE', 'value': CANNON}],
         'constraints': ({'type': SHIP_TYPE, 'value': G1A_STARFIGHTER})},

        {'name': 'Ghost', 'cost': 0, 'canon_name' : 'ghost',
         'constraints': ({'type': SHIP_TYPE, 'value': VCX100})},

        {'name': 'Phantom', 'cost': 0, 'canon_name' : 'phantom',
         'constraints': ({'type': SHIP_TYPE, 'value': ATTACK_SHUTTLE})},

        {'name': 'Tie/v1', 'cost': 1, 'canon_name' : 'tiev1',
         'constraints': ({'type': SHIP_TYPE, 'value': TIE_ADVANCED_PROTOTYPE} ) },

        {'name': 'Slave 1', 'cost': 0,
         'action': [{'type': 'ADD_UPGRADE', 'value': TORPEDO}],
         'constraints': ({'type': SHIP_TYPE, 'value': FIRESPRAY_31})},
        {'name': 'Royal Guard TIE', 'cost': 0,
         'action': [{'type': 'ADD_UPGRADE', 'value': MOD}],
         'constraints': ({'type': SHIP_TYPE, 'value': TIE_INTERCEPTOR})},
        {'name': 'A-Wing Test Pilot', 'cost': 0,
         'constraints': ({'type': SHIP_TYPE, 'value': A_WING}),
         'action': [{'type': 'ADD_UPGRADE', 'value': EPT}]},
        {'name': 'Millennium Falcon', 'cost': 1, 'constraints': ({'type': SHIP_TYPE, 'value': YT_1300})},
        {'name': 'Millennium Falcon 2', 'cost': 1, 'constraints': ({'type': SHIP_TYPE, 'value': YT_1300})},
        {'name': 'Dauntless', 'cost': 2, 'constraints': ({'type': SHIP_TYPE, 'value': VT_DECIMATOR})},
        {'name': 'Moldy Crow', 'cost': 3, 'constraints': ({'type': SHIP_TYPE, 'value': HWK_290})},
        {'name': 'ST-321', 'cost': 3, 'constraints': ({'type': SHIP_TYPE, 'value': LAMBDA_SHUTTLE})},
        {'name': 'Outrider', 'cost': 5, 'constraints': ({'type': SHIP_TYPE, 'value': YT_2400})},
        {'name': 'IG-2000', 'canon_name': 'ig2000', 'cost': 0,
         'constraints': ({'type': SHIP_TYPE, 'value': AGGRESSOR})},
        {'name': 'Andrasta', 'canon_name': 'andrasta', 'cost': 0,
         'action': [{'type': 'ADD_UPGRADE', 'value': BOMB}, {'type': 'ADD_UPGRADE', 'value': BOMB}],
         'constraints': ({'type': SHIP_TYPE, 'value': FIRESPRAY_31})},
        {'name': 'Virago', 'canon_name': 'virago', 'cost': 1,
         'action': [{'type': 'ADD_UPGRADE', 'value': SYSTEM}, {'type': 'ADD_UPGRADE', 'value': ILLICIT}],
         'constraints': ({'type': SHIP_TYPE, 'value': STAR_VIPER})},
        {'name': 'BTL-A4 Y-Wing', 'canon_name': 'btla4ywing', 'cost': 0,
         'constraints': ({'type': SHIP_TYPE, 'value': Y_WING})},
        {'name': 'TIE/X1', 'canon_name': 'tiex1', 'cost': 0,
         'action': [{'type': 'ADD_UPGRADE', 'value': SYSTEM}],
         'constraints': ({'type': SHIP_TYPE, 'value': TIE_ADVANCED})},
        {'name': 'Heavy Scyk Interceptor (Cannon)', 'canon_name': 'heavyscykinterceptor', 'cost': 2,
         'action': [{'type': 'ADD_UPGRADE', 'value': CANNON}],
         'constraints': ({'type': SHIP_TYPE, 'value': M3_A_INTERCEPTOR})},
        {'name': 'Heavy Scyk Interceptor (Torpedo)', 'canon_name': 'heavyscykinterceptor', 'cost': 2,
         'action': [{'type': 'ADD_UPGRADE', 'value': TORPEDO}],
         'constraints': ({'type': SHIP_TYPE, 'value': M3_A_INTERCEPTOR})},
        {'name': 'Heavy Scyk Interceptor (Missile)', 'canon_name': 'heavyscykinterceptor', 'cost': 2,
         'action': [{'type': 'ADD_UPGRADE', 'value': MISSILE}],
         'constraints': ({'type': SHIP_TYPE, 'value': M3_A_INTERCEPTOR})},
        {'name': 'Hound\'s Tooth', 'canon_name': 'houndstooth', 'cost': 6,
         'constraints': ({'type': SHIP_TYPE, 'value': YV_666_FREIGHTER})},

        {'name': 'TIE/x7', 'canon_name': 'tiex7', 'cost': -2,
         'constraints': ({'type': SHIP_TYPE, 'value': TIE_DEFENDER})},

        {'name': 'TIE/D', 'canon_name': 'tied', 'cost': 0,
         'constraints': ({'type': SHIP_TYPE, 'value': TIE_DEFENDER})},

        {'name': 'TIE Shuttle', 'canon_name': 'tieshuttle', 'cost': 0,
         'constraints': ({'type': SHIP_TYPE, 'value': TIE_BOMBER}),
         'action': [{'type': 'ADD_UPGRADE', 'value': CREW}, {'type': 'ADD_UPGRADE', 'value': CREW}]},

    ),
    SYSTEM: (
        {'name': 'Collision Detector', 'canon_name': 'collisiondetector', 'cost': 0},
        {'name': 'Electronic Baffle', 'canon_name': 'electronicbaffle', 'cost': 1},
        {'name': 'Enhanced Scopes', 'cost': 1},
        {'name': 'Fire-Control System', 'cost': 2},
        {'name': 'Advanced Sensors', 'cost': 3},
        {'name': 'Accuracy Corrector', 'cost': 3},
        {'name': 'Reinforced Deflectors', 'cost': 3},
        {'name': 'Sensor Jammer', 'cost': 4},
        {'name': 'Advanced Targeting Computer', 'canon_name': 'advtargetingcomputer', 'cost': 5},
        {'name': 'Advanced Targeting Computer', 'canon_name': 'advtargetingcomputer', 'cost': 5},

    ),
    TURRET: (
        {'name': 'Blaster Turret', 'cost': 4},
        {'name': 'Ion Cannon Turret', 'cost': 5},
        {'name': 'Autoblaster Turret', 'cost': 2},
        {'name': 'Dorsal Turret', 'canon_name': 'dorsalturret', 'cost': 3},
        {'name': 'Twin Laser Turret', 'canon_name': 'twinlaserturret', 'cost': 6},
    ),
    TORPEDO: (

        {'name': 'Seismic Torpedoes', 'cost': 2},
        {'name': 'Flechette Torpedoes', 'cost': 2},
        {'name': 'Proton Torpedoes', 'cost': 4},
        {'name': 'Ion Torpedoes', 'cost': 5},
        {'name': 'Advanced Proton Torpedoes', 'cost': 6},
        {'name': 'Bomb Loadout', 'canon_name': 'bombloadout', 'cost': 0,
         'action': [{'type': 'ADD_UPGRADE', 'value': BOMB}],
         'constraints': ({'type': SHIP_TYPE, 'value': Y_WING})},
        {'name': 'Extra Munitions', 'canon_name': 'extramunitions', 'cost': 2},
        {'name': 'Plasma Torpedoes', 'canon_name': 'plasmatorpedoes', 'cost': 3},
    ),

    BOMB: (
        {'name': 'Thermal Detonators', 'cost': 3},
        {'name': 'Seismic Charges', 'cost': 2},
        {'name': 'Proximity Mines', 'cost': 3},
        {'name': 'Proton Bombs', 'cost': 5},
        {'name': 'Cluster Mines', 'canon_name': 'clustermines', 'cost': 4},
        {'name': 'Ion Bombs', 'canon_name': 'ionbombs', 'cost': 2},
        {'name': 'Conner Net', 'canon_name': 'connernet', 'cost': 4}
    ),
    CANNON: (
        {'name': 'Ion Cannon', 'cost': 3},
        {'name': 'AutoBlaster', 'cost': 5},
        {'name': 'Heavy Laser Cannon', 'cost': 7},
        {'name': 'Mangler Cannon', 'cost': 4},
        {'name': 'Flechette Cannon', 'cost': 2},
        {'name': 'Tractor Beam', 'cost': 1}

    ),
    MISSILE: (
        {'name': 'XX-23 S-Thread Tracers', 'cost':1},
        {'name': 'Chardaan Refit', 'cost': -2, 'constraints': ({'type': SHIP_TYPE, 'value': A_WING})},
        {'name': 'Ion Pulse Missiles', 'cost': 3},
        {'name': 'Proton Rockets', 'cost': 3},
        {'name': 'Concussion Missiles', 'cost': 4},
        {'name': 'Cluster Missiles', 'cost': 4},
        {'name': 'Assault Missiles', 'cost': 5},
        {'name': 'Homing Missiles', 'cost': 5},
        {'name': 'Adv. Homing Missiles', 'canon_name': 'advhomingmissiles', 'cost': 3},
    ),
    MOD: (

        {'name': 'Lightweight Frame', 'canon_name': 'lightweightframe', 'cost': 2 },

        {'name': 'Spacetug Tractor Array', 'canon_name': 'spacetugtractorarray', 'cost': 2,
          'constraints': ({'type': SHIP_TYPE, 'value': [QUADJUMPER] } ),},


        {'name': 'Captured TIE', 'canon_name': 'capturedtie', 'cost': 1,
          'constraints': ({'type': SHIP_TYPE, 'value': [TIE_FIGHTER] } ),},
        {'name': 'Smuggling Compartment', 'canon_name': 'smugglingcompartment', 'cost': 0,
           'action': [{'type': 'ADD_UPGRADE', 'value': ILLICIT}, {'type': 'ADD_UPGRADE', 'value': MOD}]
         },
        {'name': 'Gyroscopic Targeting', 'canon_name': 'gyroscopictargeting', 'cost': 2},
        {'name': 'Guidance Chips', 'canon_name': 'guidancechips', 'cost': 0},
        {'name': 'Long-Range Scanners', 'canon_name': 'longrangescanners', 'cost': 0},
        {'name': 'Munitions Failsafe', 'cost': 1},
        {'name': 'Tactical Jammer', 'cost': 1, 'constraints': ({'type': SHIP_SIZE, 'value': LARGE_SHIP})},
        {'name': 'Targeting Computer', 'cost': 2},
        {'name': 'Vectored Thrusters', 'canon_name': 'vectoredthrusters', 'cost': 2},
        {'name': 'Anti-Pursuit Lasers', 'cost': 2, 'constraints': ({'type': SHIP_SIZE, 'value': LARGE_SHIP})},
        {'name': 'Stygium Particle Accelerator', 'cost': 2},
        {'name': 'Advanced Cloaking Device', 'cost': 4, 'constraints': ({'type': SHIP_TYPE, 'value': TIE_PHANTOM})},
        {'name': 'Experimental Interface', 'cost': 3},
        {'name': 'B-Wing/E2', 'cost': 1,
         'action': [{'type': 'ADD_UPGRADE', 'value': CREW}],
         'constraints': ({'type': SHIP_TYPE, 'value': B_WING})},
        {'name': 'Stealth Device', 'cost': 3},
        {'name': 'Hull Upgrade', 'cost': 3},
        {'name': 'Shield Upgrade', 'cost': 4},
        {'name': 'Counter-Measures', 'cost': 3, 'constraints': ({'type': SHIP_SIZE, 'value': LARGE_SHIP})},
        {'name': 'Engine Upgrade', 'cost': 4},
        {'name': 'Autothrusters', 'canon_name': 'autothrusters', 'cost': 2},
        {'name': 'Advanced SLAM', 'canon_name': 'advancedslam', 'cost': 2},
        {'name': 'Twin Ion Engine Mk. II', 'canon_name': 'twinionenginemkii', 'cost': 1},
        {'name': 'Maneuvering Fins', 'canon_name': 'maneuveringfins', 'cost': 1,
         'constraints': ({'type': SHIP_TYPE, 'value': YV_666_FREIGHTER})},
        {'name': 'Ion Projector', 'canon_name': 'ionprojector', 'cost': 2,
         'constraints': ({'type': SHIP_SIZE, 'value': LARGE_SHIP})},
        {'name': 'Integrated Astromech', 'canon_name': 'integratedastromech', 'cost': 0},
    ),

    EPT:
        (
         {'name': 'Expertise', 'cost': 4, 'canon_name':'Expertise'},
         {'name': 'Swarm Leader', 'cost': 3, 'canon_name':'swarmleader'},
         {'name': 'A Score To Settle', 'cost': 0, 'canon_name':'ascoretosettle'},
         {'name': 'Trick Shot', 'cost': 0, 'canon_name':'trickshot'},
         {'name': 'Snap Shot', 'cost': 2, 'canon_name':'snapshot'},
         {'name': 'Fearlessness', 'cost': 1, 'canon_name':'fearlessness'},
         {'name': 'Attanni Mindlink', 'cost': 1, 'canon_name':'attannimindlink'},
         {'name': 'Rage', 'cost': 1, 'canon_name':'rage'},
         {'name': 'Adaptability', 'cost': 0, 'canon_name':'adaptability'},
         {'name': 'Adrenaline Rush', 'cost': 1},
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
         {'name': 'Bodyguard', 'cost': 2},
         {'name': 'Calculation', 'cost': 1},
         {'name': 'Crack Shot', 'canon_name': 'crackshot', 'cost': 1},
         {'name': 'Lightning Reflexes', 'canon_name': 'lightningreflexes', 'cost': 1},
         {'name': 'Wired', 'cost': 1},
         {'name': 'Cool Hand', 'cost': 1},
         {'name': 'Juke', 'cost': 2},

         ),

    ILLICIT: (
        {'name': 'Scavenger Crane', 'canon_name': 'scavengercrane', 'cost': 2},
        {'name': 'EMP Device', 'canon_name': 'empdevice', 'cost': 2},
        {'name': 'Burnout SLAM', 'canon_name': 'burnoutslam', 'cost': 1},
        {'name': 'Rigged Cargo Chute', 'canon_name': 'riggedcargochute', 'cost': 1},
        {'name': 'Black Market Slicer Tools', 'canon_name': 'blackmarketslicertools', 'cost': 1},
        {'name': 'Hot Shot Blaster', 'canon_name': 'hotshotblaster', 'cost': 3},
        {'name': 'Dead Mans Switch', 'canon_name': 'deadmansswitch', 'cost': 2},
        {'name': 'Feedback Array', 'canon_name': 'feedbackarray', 'cost': 2},
        {'name': 'Inertial Dampeners', 'canon_name': 'inertialdampeners', 'cost': 1},
        {'name': 'Glitterstim', 'canon_name': 'glitterstim', 'cost': 2},
        {'name': 'Cloaking Device', 'cost': 2, 'constraints': ({'type': SHIP_SIZE, 'value': SMALL_SHIP})},

    ),

     SALVAGED_ASTROMECH_DROID: (
        {'name': 'Overclocked R4', 'canon_name': 'overclockedr4', 'cost': 1},
        {'name': 'Genius', 'canon_name': 'genius', 'cost': 0},
        {'name': 'R4 Agromech', 'canon_name': 'r4agromech', 'cost': 2},
        {'name': 'R4-B11', 'canon_name': 'r4b11', 'cost': 3},
        {'name': 'R5-P8', 'cost': 3, 'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,)},
        {'name': 'Salvaged Astromech', 'canon_name': 'salvagedastromech', 'cost': 2},
        {'name': 'Unhinged Astromech', 'canon_name': 'unhingedastromech', 'cost': 1},

    ),

    TECH: (
        {'name': 'Hyperwave Comm Scanner', 'canon_name': 'hyperwavecommscanner', 'cost': 1},
        {'name': 'Targeting Synchronizer', 'canon_name': 'targetingsynchronizer', 'cost': 3},
        {'name': 'Primed Thrusters', 'canon_name': 'patternanalyzer', 'cost': 1},
        {'name': 'Pattern Analyzer', 'canon_name': 'patternanalyzer', 'cost': 2},
        {'name': 'Weapons Guidance', 'canon_name': 'weaponsguidance', 'cost': 2},
        {'name': 'Sensor Cluster', 'canon_name': 'sensorcluster', 'cost': 2},
        {'name': 'Comm Relay', 'canon_name': 'commrelay', 'cost': 3},

    )
}

ships = {

    U_WING : (
        {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Blue Squadron Pathfinder',
         'cost': 23, 'canon_name':'bluesquadronpathfinder','upgrades': (SYSTEM, TORPEDO, CREW, CREW, MOD, TITLE ),
         'pilot_skill' : 2,
        },
        {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Heff Tobber',
         'cost': 24, 'canon_name':'hefftobber','upgrades': (SYSTEM, TORPEDO, CREW, CREW, MOD, TITLE ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 3,
        },
        {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Bodhi Rook',
         'cost': 25, 'canon_name':'bodhirook','upgrades': (SYSTEM, TORPEDO, CREW, CREW, MOD, TITLE ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 4,
        },
        {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Cassian Andor',
         'cost': 27, 'canon_name':'cassianandor','upgrades': (EPT, SYSTEM, TORPEDO, CREW, CREW, MOD, TITLE ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 6,
        },
    ),

    TIE_STRIKER : (

        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Imperial Trainee',
         'cost': 17, 'canon_name':'imperialtrainee',
         'upgrades': (MOD ),
         'pilot_skill' : 1,
        },
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Scarif Defender',
         'cost': 18, 'canon_name':'scarifdefender',
         'upgrades': (MOD ),
         'pilot_skill' : 3 ,
        },
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Black Squadron Scout',
         'cost': 20, 'canon_name':'blacksquadronscout',
         'upgrades': (MOD,EPT ),
         'pilot_skill' : 4,
        },

        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Countdown',
         'cost': 20, 'canon_name':'countdown',
         'upgrades': (MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 5,
        },
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Pure Sabacc',
         'cost': 22, 'canon_name':'puresabacc',
         'upgrades': (MOD,EPT ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 6,
        },
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Duchess',
         'cost': 23, 'canon_name':'duchess',
         'upgrades': (MOD,EPT),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 8,
        },
    ),

    QUADJUMPER: (
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Jakku Gunrunner', 'cost': 15, 'canon_name':'jakkugunrunner',
         'upgrades': (CREW, BOMB, TECH, ILLICIT, MOD ),
         'pilot_skill' : 1,
        },

        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Unkar Plutt', 'cost': 17, 'canon_name':'unkarplutt',
         'upgrades': (CREW, BOMB, TECH, ILLICIT, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 3,
        },

        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Constable Zuvio', 'cost': 19, 'canon_name':'constablezuvio',
         'upgrades': (EPT, CREW, BOMB, TECH, ILLICIT, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 7,
        },


    ),


    PROTECTORATE_STARFIGHTER: (

        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Fenn Rau', 'cost': 28, 'canon_name':'fennrau',
         'upgrades': (EPT, TORPEDO, TITLE, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 9,
        },
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Old Teroch', 'cost': 26, 'canon_name':'oldteroch',
         'upgrades': (EPT, TORPEDO, TITLE, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 7,
        },
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Kad Solus', 'cost': 25, 'canon_name':'kadsolus',
         'upgrades': (EPT, TORPEDO, TITLE, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 6,
        },
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Concord Dawn Ace', 'cost': 23, 'canon_name':'concorddawnace',
         'upgrades': (EPT, TORPEDO, TITLE, MOD ),
         'pilot_skill' : 5,
        },
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Concord Dawn Veteran', 'cost': 22, 'canon_name':'concorddawnace',
         'upgrades': (EPT, TORPEDO, TITLE, MOD ),
         'pilot_skill' : 3,
        },
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Zealous Recruit', 'cost': 20, 'canon_name':'zealousrecruit',
         'upgrades': (TORPEDO, TITLE, MOD ),
         'pilot_skill' : 1,
        },
    ),

    TIE_SF_FIGHTER : (
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Zeta Specialist', 'cost': 23, 'canon_name':'zetaspecialist',
         'upgrades': (SYSTEM, MISSILE,TECH, TITLE, MOD ),
         'pilot_skill' : 3,
        },
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Backdraft', 'cost': 27, 'canon_name':'ruthlessfreelancer',
         'upgrades': (EPT, SYSTEM, MISSILE,TECH, TITLE, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 7,
        },
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Quickdraw', 'cost': 29, 'canon_name':'Quickdraw',
         'upgrades': (EPT, SYSTEM, MISSILE,TECH, TITLE, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 9,
        },
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Omega Specialist', 'cost': 25, 'canon_name':'omegaspecialist',
         'upgrades': (EPT, SYSTEM, MISSILE,TECH, TITLE, MOD ),
         'pilot_skill' : 5,
        },
    ),


    ARC_170: (
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Braylen Stramm', 'cost': 25, 'canon_name':'braylenstramm',
         'upgrades': (TORPEDO, CREW, DROID, TITLE, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 3,
        },
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Norra Wexley', 'cost': 29, 'canon_name':'norrawexley',
         'upgrades': (EPT, TORPEDO, CREW, DROID, TITLE, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 7,
        },
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Shara Bey', 'cost': 28, 'canon_name':'sharabey',
         'upgrades': (EPT, TORPEDO, CREW, DROID, TITLE, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 6,
        },
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Thane Kyrell', 'cost': 26, 'canon_name':'thanekyrell',
         'upgrades': (TORPEDO, CREW, DROID, TITLE, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 4,
        },
    ),

    LANCER_CLASS_PURSUIT_CRAFT: (
        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Asajj Ventress', 'cost': 37, 'canon_name':'asajjventress',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, CREW, ILLICIT, ILLICIT, TITLE, MOD ),
         'pilot_skill' : 6,
        },

        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Ketsu Onyo', 'cost': 38, 'canon_name':'ketsuonyo',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, CREW, ILLICIT, ILLICIT, TITLE, MOD ),
         'pilot_skill' : 7,
        },

        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Sabine Wren [Scum]', 'cost': 35,
         'canon_name':'sabinewren-swx56',
         'upgrades': (CREW, ILLICIT, ILLICIT, TITLE, MOD ),
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 5,
        },

        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Shadowport Hunter', 'cost': 33, 'canon_name':'shadowporthunter',
         'upgrades': (CREW, ILLICIT, ILLICIT, TITLE, MOD ),
         'pilot_skill' : 2,
        },

    ),

    JUMPMASTER_5000_ : (
        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Contracted Scout',
         'cost': 25, 'canon_name':'contractedscout',
         'upgrades': (EPT, TORPEDO, TORPEDO, CREW, SALVAGED_ASTROMECH_DROID, ILLICIT,MOD,TITLE ),
         'pilot_skill' : 3,
        },
        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Manaroo',
         'cost': 27, 'canon_name':'Manaroo',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, TORPEDO, TORPEDO, CREW, SALVAGED_ASTROMECH_DROID, ILLICIT,MOD,TITLE ),
         'pilot_skill' : 4,
        },
        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Tel Trevura',
         'cost': 30, 'canon_name':'Tel Trevura',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, TORPEDO, TORPEDO, CREW, SALVAGED_ASTROMECH_DROID, ILLICIT,MOD,TITLE ),
         'pilot_skill' : 7,
        },
        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Dengar',
         'cost': 33, 'canon_name':'Dengar',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, TORPEDO, TORPEDO, CREW, SALVAGED_ASTROMECH_DROID, ILLICIT,MOD,TITLE ),
         'pilot_skill' : 9,
        },
    ),

    G1A_STARFIGHTER : (

        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Ruthless Freelancer', 'cost': 23, 'canon_name':'ruthlessfreelancer',
         'upgrades': (CREW, SYSTEM, ILLICIT, TITLE, MOD ),
         'pilot_skill' : 3,
        },

        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Gand Findsman', 'cost': 25, 'canon_name':'gandfindsman',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, CREW, SYSTEM, ILLICIT, TITLE, MOD ),
         'pilot_skill' : 5,
        },

        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': '4-LOM', 'cost': 27, 'canon_name':'4lom',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, CREW, SYSTEM, ILLICIT, TITLE, MOD ),
         'pilot_skill' : 6,
        },
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Zuckuss', 'cost': 28, 'canon_name':'zuckuss',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, CREW, SYSTEM, ILLICIT, TITLE, MOD ),
         'pilot_skill' : 7,
        },
    ),

    TIE_ADVANCED_PROTOTYPE : (

        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Seinar Test Pilot', 'cost': 16, 'canon_name':'seinartestpilot',
         #'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (MISSILE, TITLE, MOD ),
         'pilot_skill' : 2,
        },
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Baron of the Empire', 'cost': 19, 'canon_name':'baronoftheempire',
         #'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (MISSILE, TITLE, MOD,EPT ),
         'pilot_skill' : 4,
        },

        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Valen Rudor', 'cost': 22, 'canon_name':'valenrudor',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, MISSILE, TITLE, MOD ),
         'pilot_skill' : 6,
        },
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'The Inquisitor', 'cost': 25, 'canon_name':'theinquisitor',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, MISSILE, TITLE, MOD ),
         'pilot_skill' : 8,
        },
    ),


    ATTACK_SHUTTLE: (
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Zeb Orrelios', 'cost': 18, 'canon_name':'zeborrelios',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (TURRET, CREW, TITLE, MOD ),
         'pilot_skill' : 3,
        },
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Ezra Bridger', 'cost': 20, 'canon_name':'ezrabridger',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, TURRET, CREW, TITLE, MOD ),
         'pilot_skill' : 4,
        },
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Sabine Wren', 'cost': 21, 'canon_name':'sabinewren',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, TURRET, CREW, TITLE, MOD ),
         'pilot_skill' : 5,
        },
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Hera Syndulla', 'cost': 22, 'canon_name':'herasyndulla',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (EPT, TURRET, CREW, TITLE, MOD ),
         'pilot_skill' : 7,
        },
    ),


    VCX100: (
        {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Lothal Rebel', 'cost': 35, 'canon_name':'lothalrebel',
         'upgrades': (SYSTEM, TURRET, TORPEDO, TORPEDO, CREW, CREW, TITLE, MOD ),
         'pilot_skill' : 3,
        },

        {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Chopper', 'cost': 37, 'canon_name':'chopper',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (SYSTEM, TURRET, TORPEDO, TORPEDO, CREW, CREW, TITLE, MOD ),
         'pilot_skill' : 4,
        },
        {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Kanan Jarrus', 'cost': 38, 'canon_name':'kananjarrus',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (SYSTEM, TURRET, TORPEDO, TORPEDO, CREW, CREW, TITLE, MOD ),
         'pilot_skill' : 5,
        },
        {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Hera Syndulla', 'cost': 40, 'canon_name':'herasyndulla',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (SYSTEM, TURRET, TORPEDO, TORPEDO, CREW, CREW, TITLE, MOD ),
         'pilot_skill' : 7,
        },

    ),

    T_70:
    (
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Blue Squadron Novice',
         'cost': 24, 'pilot_skill': 2, 'canon_name': 'bluesquadronnovice',
         'upgrades': (TITLE,DROID, TORPEDO, MOD, TECH)},
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Red Squadron Veteran', 'cost': 26,
         'cost': 26, 'pilot_skill': 4, 'canon_name': 'redsquadronveteran',
         'upgrades': (TITLE,DROID, TORPEDO, MOD, TECH, EPT)},
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Blue Ace', 'cost': 27,
         'cost': 27, 'pilot_skill': 5, 'canon_name': 'blueace',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (TITLE,DROID, TORPEDO, MOD, TECH)},
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Red Ace', 'cost': 29,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill': 6, 'canon_name': 'redace',
         'upgrades': (TITLE,DROID, TORPEDO, MOD, TECH)},

        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Ello Asty', 'cost': 30,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill': 7, 'canon_name': 'elloasty',
         'upgrades': (TITLE,DROID, TORPEDO, MOD, EPT, TECH)},

        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Poe Dameron',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'cost': 31, 'pilot_skill': 8, 'canon_name': 'poedameron',
         'upgrades': (TITLE,DROID, TORPEDO, MOD, EPT, TECH)},

        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Poe Dameron (PS9)',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'cost': 33, 'pilot_skill': 9, 'canon_name': 'poedameron-swx57',
         'upgrades': (TITLE, DROID, TORPEDO, MOD, EPT, TECH)},

        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Jess Pava',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'cost': 25, 'pilot_skill': 3, 'canon_name': 'jesspava',
         'upgrades': (TITLE, DROID, TORPEDO, MOD, TECH)},

        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Snap Wexley',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'cost': 28, 'pilot_skill': 6, 'canon_name': 'snapwexley',
         'upgrades': (TITLE, DROID, TORPEDO, MOD, EPT, TECH)},

        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Nien Nunb',
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'cost': 29, 'pilot_skill': 7, 'canon_name': 'niennunb',
         'upgrades': (TITLE, DROID, TORPEDO, MOD, EPT, TECH)},
    ),

    # TODO: Zeta Leader, Episilon Ace,
    TIE_FO_FIGHTER:
        (
            {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Epsilon Squadron Pilot', 'cost': 15,
             'pilot_skill': 1, 'canon_name': 'Epsilonsquadronpilot',
             'constraints': (),
             'upgrades': (MOD, TECH)},
            {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Zeta Squadron Pilot', 'cost': 16,
             'constraints': (),
             'pilot_skill': 3, 'canon_name': 'zetasquadronpilot',
             'upgrades': (MOD, TECH)},
            {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Omega Squadron Pilot', 'cost': 17,
             'pilot_skill': 4, 'canon_name': 'omegasquadronpilot',
             'constraints': (),
             'upgrades': (EPT, MOD, TECH)},
            {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Zeta Ace', 'cost': 18,
             'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT),
             'pilot_skill': 5, 'canon_name': 'zetaace',
             'upgrades': (EPT, MOD, TECH)},
            {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Epsilon Leader', 'cost': 19,
             'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT),
             'pilot_skill': 6, 'canon_name': 'epsilonleader',
             'upgrades': (MOD, TECH)},
            {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Omega Ace', 'cost': 20,
             'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT),
             'pilot_skill': 7, 'canon_name': 'omegaace',
             'upgrades': (EPT, MOD, TECH)
             },
            {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Epsilon Ace', 'cost': 17,
             'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT),
             'pilot_skill': 4, 'canon_name': 'epsilonace',
             'upgrades': (MOD, TECH)
             },
            {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Omega Leader', 'cost': 21,
             'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT),
             'pilot_skill': 8, 'canon_name': 'omegaleader',
             'upgrades': (EPT, MOD, TECH)
             },
            {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Zeta Leader', 'cost': 20,
             'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT),
             'pilot_skill': 8, 'canon_name': 'zetaleader',
             'upgrades': (EPT, MOD, TECH)
             },
        ),

    X_WING: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Wedge Antilles', 'cost': 29,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (DROID, TORPEDO, MOD, EPT)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Luke Skywalker', 'cost': 28,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (DROID, TORPEDO, MOD, EPT)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Wes Janson', 'cost': 29,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (DROID, TORPEDO, MOD, EPT)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Jek Porkins', 'cost': 26,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (DROID, TORPEDO, MOD, EPT)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Red Squadron Pilot', 'cost': 23,
              'upgrades': (DROID, TORPEDO, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Garven Dreis', 'cost': 26,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (DROID, TORPEDO, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Rookie Pilot', 'cost': 21,
              'upgrades': (DROID, TORPEDO, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Biggs Darklighter', 'cost': 25,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (DROID, TORPEDO, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Hobbie Klivian', 'cost': 25,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (DROID, TORPEDO, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Tarn Mison', 'cost': 23,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (DROID, TORPEDO, MOD)}),

    Y_WING: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Horton Salm', 'cost': 25,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Gray Squadron Pilot', 'cost': 20,
              'upgrades': (TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Dutch Vander', 'cost': 23,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Gold Squadron Pilot', 'cost': 18,
              'upgrades': (TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Syndicate Thug', 'canon_name': 'syndicatethug',
              'cost': 18,
              'upgrades': (TITLE, TORPEDO, TORPEDO, TURRET, MOD, SALVAGED_ASTROMECH_DROID)},
             {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Hired Gun', 'canon_name': 'hiredgun', 'cost': 20,
              'upgrades': (TITLE, TORPEDO, TORPEDO, TURRET, MOD, SALVAGED_ASTROMECH_DROID)},

             {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Drea Renthal', 'canon_name': 'drearenthal', 'cost': 22,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (TITLE, TORPEDO, TORPEDO, TURRET, MOD, SALVAGED_ASTROMECH_DROID)},
             {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Kavil', 'canon_name': 'kavil', 'cost': 24,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (EPT, TITLE, TORPEDO, TORPEDO, TURRET, MOD, SALVAGED_ASTROMECH_DROID)},

             ),

    A_WING: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Tycho Celchu', 'cost': 26,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (TITLE, MISSILE, EPT, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Green Squadron Pilot', 'cost': 19,
              'upgrades': (TITLE, MISSILE, EPT, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Arvel Crynyd', 'cost': 23,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (TITLE, MISSILE, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Prototype Pilot', 'cost': 17,
              'upgrades': (TITLE, MISSILE, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Gemmer Sojan', 'cost': 22,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (TITLE, MISSILE, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Jake Farrell', 'cost': 24,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (TITLE, MISSILE, EPT, MOD)}),

    YT_1300: (

              {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Resistance Sympathizer', 'cost': 38,
               'upgrades': (MISSILE, TITLE, MOD, CREW, CREW)},


              {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Han Solo (TFA)', 'cost': 46,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (EPT, MISSILE, TITLE, MOD, CREW, CREW)},

              {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Chewbacca (TFA)', 'cost': 42,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (EPT, MISSILE, TITLE, MOD, CREW, CREW)},


              {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Rey', 'cost': 45,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (EPT, MISSILE, TITLE, MOD, CREW, CREW)},
              {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Han Solo', 'cost': 46,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (EPT, MISSILE, TITLE, MOD, CREW, CREW)},
              {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Chewbacca', 'cost': 42,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (EPT, MISSILE, TITLE, MOD, CREW, CREW)},
              {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Lando Calrissian', 'cost': 44,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (EPT, MISSILE, TITLE, MOD, CREW, CREW)},
              {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Outer Rim Smuggler', 'cost': 27,
               'upgrades': (CREW, CREW, TITLE, MOD)}),

    B_WING: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Ten Numb', 'cost': 31,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Keyan Farlander', 'cost': 29,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Ibtisam', 'cost': 28,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Nera Dantels', 'cost': 26,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Dagger Squadron Pilot', 'cost': 24,
              'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Blue Squadron Pilot', 'cost': 22,
              'upgrades': (SYSTEM, CANNON, TORPEDO, TORPEDO, MOD)}),


    HWK_290: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Jan Ors', 'cost': 25,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (EPT, TURRET, CREW, TITLE, MOD)},
              {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Kyle Katarn', 'cost': 21,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (EPT, TURRET, CREW, TITLE, MOD)},
              {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Roark Garnet', 'cost': 19,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (TURRET, CREW, TITLE, MOD)},
              {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Rebel Operative', 'cost': 16,
               'upgrades': (TURRET, CREW, TITLE, MOD)},
              # scum
              {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Spice Runner', 'cost': 16,
               'canon_name': 'spicerunner',
               'upgrades': (TURRET, CREW, TITLE, MOD, ILLICIT)},
              {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Torkil Mux', 'cost': 19, 'canon_name': 'torkilmux',
               'upgrades': (TURRET, CREW, TITLE, MOD, ILLICIT)},
              {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Dace Bonearm', 'cost': 23,
               'canon_name': 'dacebonearm',
               'upgrades': (EPT, TURRET, CREW, TITLE, MOD, ILLICIT)},
              {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Palob Godalhi', 'cost': 20,
               'canon_name': 'palobgodalhi',
               'upgrades': (EPT, TURRET, CREW, TITLE, MOD, ILLICIT)},

              ),

    E_WING: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Corran Horn', 'cost': 35,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (DROID, TORPEDO, SYSTEM, EPT, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Etahn A\'Baht', 'cost': 32,
              'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (DROID, TORPEDO, SYSTEM, EPT, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Blackmoon Squadron Pilot', 'cost': 29,
              'upgrades': (DROID, TORPEDO, SYSTEM, MOD)},
             {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Knave Squadron Pilot', 'cost': 27,
              'upgrades': (DROID, TORPEDO, SYSTEM, MOD)}),

    Z95_HEADHUNTER: ({'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Airen Cracken', 'cost': 19,
                      'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                      'upgrades': (MISSILE, EPT, MOD)},
                     {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Lt. Blount', 'cost': 17,
                      'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                      'upgrades': (MISSILE, EPT, MOD)},
                     {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Tala Squadron Pilot', 'cost': 13,
                      'upgrades': (MISSILE, MOD)},
                     {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Bandit Squadron Pilot', 'cost': 12,
                      'upgrades': (MISSILE, MOD)},

                     # scum
                     {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Binayre Pirate',
                      'canon_name': 'binayrepirate',
                      'cost': 12,
                      'upgrades': (MISSILE, MOD, ILLICIT)},
                     {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Black Sun Soldier',
                      'canon_name': 'blacksunsoldier',
                      'cost': 13,
                      'upgrades': (MISSILE, MOD, ILLICIT)},
                     {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'KaaTo Leeachos',
                      'canon_name': 'kaatoleeachos',
                      'cost': 15,
                      'upgrades': (EPT, MISSILE, MOD, ILLICIT)},
                     {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'NDru Suhlak',
                      'canon_name': 'ndrusuhlak',
                      'cost': 17,
                      'upgrades': (EPT, MISSILE, MOD, ILLICIT)},
                     ),

    YT_2400: ({'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Dash Rendar', 'cost': 36,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (EPT, CANNON, MISSILE, CREW, TITLE, MOD)},
              {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Leebo', 'cost': 34,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (EPT, CANNON, MISSILE, CREW, TITLE, MOD)},
              {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Eaden Vrill', 'cost': 32,
               'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
               'upgrades': (CANNON, MISSILE, CREW, TITLE, MOD)},
              {'ship_size': LARGE_SHIP, 'faction': REBEL, 'name': 'Wild Space Fringer', 'cost': 30,
               'upgrades': (CANNON, MISSILE, CREW, TITLE, MOD)}),

    TIE_FIGHTER: (

        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Zeb Orrelios (TIE Fighter)', 'cost': 13,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (MOD, TITLE)},


        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Captain Rex', 'cost': 14,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (MOD, TITLE)},

        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Sabine Wren (TIE Fighter)', 'cost': 15,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (EPT, MOD, TITLE)},

        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Ahsoka Tano', 'cost': 17,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (EPT, MOD,TITLE)},


        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Howlrunner', 'cost': 18,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (EPT, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Mauler Mithel', 'cost': 17,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (EPT, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Dark Curse', 'cost': 16,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (MOD,)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Backstabber', 'cost': 16,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (MOD,)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Winged Gundark', 'cost': 15,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (MOD,)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Night Beast', 'cost': 15,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (MOD,)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Black Squadron Pilot', 'cost': 14,
         'upgrades': (EPT, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Obsidian Squadron Pilot', 'cost': 13,
         'upgrades': (MOD,)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Academy Pilot', 'cost': 12, 'upgrades': (MOD,)},

        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Scourge', 'ps': 7, 'cost': 17,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (MOD, EPT)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Wampa', 'ps': 4, 'cost': 14,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (MOD,)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Youngster', 'ps': 6, 'cost': 15,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (MOD, EPT)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Chaser', 'ps': 3, 'cost': 14,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,), 'upgrades': (MOD,)}

    ),


    UPSILON_CLASS_SHUTTLE:
        ({'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Starkiller Base Pilot', 'cost': 30,
              'upgrades': (SYSTEM, CREW, CREW, TECH, TECH, TITLE, MOD)},

         {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Lieutenant Dormitz', 'cost': 31,
              'upgrades': (SYSTEM, CREW, CREW, TECH, TECH, TITLE, MOD)},

         {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Major Stridan', 'cost': 32,'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (SYSTEM, CREW, CREW, TECH, TECH, TITLE, MOD)},

         {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Kylo Ren', 'cost': 34,'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
              'upgrades': (EPT, SYSTEM, CREW, CREW, TECH, TECH, TITLE, MOD)},
                            ),

    TIE_ADVANCED: ({'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Darth Vader', 'cost': 29,
                    'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                    'upgrades': (MISSILE, EPT, MOD, TITLE)},
                   {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Maarek Stele', 'cost': 27,
                    'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                    'upgrades': (MISSILE, EPT, MOD, TITLE)},
                   {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Storm Squadron Pilot', 'cost': 23,
                    'upgrades': (MISSILE, MOD, TITLE)},
                   {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Tempest Squadron Pilot', 'cost': 21,
                    'upgrades': (MISSILE, MOD, TITLE)},

                   {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Commander Alozen', 'cost': 25,
                    'upgrades': (EPT, MISSILE, MOD, TITLE)},

                   {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Juno Eclipse', 'cost': 28,
                    'upgrades': (EPT, MISSILE, MOD, TITLE)},

                   {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Lieutenant Colzet', 'cost': 23,
                    'upgrades': (MISSILE, MOD, TITLE)},

                   {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Zertik Strom', 'cost': 26,
                    'upgrades': (EPT, MISSILE, MOD, TITLE)},

                   ),

    TIE_INTERCEPTOR: ({'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Soontir Fel', 'cost': 27,
                       'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                       'upgrades': (TITLE, EPT, MOD)},
                      {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Carnor Jax', 'cost': 26,
                       'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                       'upgrades': (TITLE, EPT, MOD)},
                      {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Turr Phennir', 'cost': 25,
                       'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                       'upgrades': (TITLE, EPT, MOD)},
                      {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Tetran Cowall', 'cost': 24,
                       'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                       'upgrades': (TITLE, EPT, MOD)},
                      {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Kir Kanos', 'cost': 24,
                       'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                       'upgrades': (TITLE, MOD)},
                      {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Lt. Lorrir', 'cost': 23,
                       'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                       'upgrades': (TITLE, MOD)},
                      {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Fel\'s Wrath', 'cost': 23,
                       'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                       'upgrades': (TITLE, MOD)},
                      {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Royal Guard Pilot', 'cost': 22,
                       'upgrades': (TITLE, EPT, MOD)},
                      {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Saber Squadron Pilot', 'cost': 21,
                       'upgrades': (TITLE, EPT, MOD)},
                      {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Avenger Squadron Pilot', 'cost': 20,
                       'upgrades': (TITLE, MOD)},
                      {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Alpha Squadron Pilot', 'cost': 18,
                       'upgrades': (TITLE, MOD)}),

    FIRESPRAY_31: ({'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Boba Fett', 'cost': 39,
                    'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                    'upgrades': (MISSILE, CANNON, BOMB, EPT, TITLE, MOD, CREW)},
                   {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Kath Scarlet', 'cost': 38,
                    'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                    'upgrades': (MISSILE, CANNON, BOMB, EPT, TITLE, MOD, CREW)},
                   {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Krassis Trelix', 'cost': 36,
                    'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                    'upgrades': (MISSILE, CANNON, BOMB, TITLE, MOD, CREW)},
                   {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Bounty Hunter', 'cost': 33,
                    'upgrades': (MISSILE, CANNON, BOMB, TITLE, MOD, CREW)},
                   {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Mandalorian Mercenary', 'cost': 35,
                    'canon_name': 'mandalorianmercenary',
                    'upgrades': (EPT, ILLICIT, MISSILE, CANNON, BOMB, TITLE, MOD, CREW)},
                   {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Emon Azzameen', 'cost': 36,
                    'canon_name': 'emonazzameen', 'upgrades': (ILLICIT, MISSILE, CANNON, BOMB, TITLE, MOD, CREW)},
                   {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Kath Scarlet', 'cost': 38,
                    'canon_name': 'kathscarlet', 'upgrades': (EPT, ILLICIT, MISSILE, CANNON, BOMB, TITLE, MOD, CREW)},
                   {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Boba Fett', 'cost': 39,
                    'canon_name': 'bobafett', 'upgrades': (EPT, ILLICIT, MISSILE, CANNON, BOMB, TITLE, MOD, CREW)},

                   ),

    LAMBDA_SHUTTLE: ({'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Captain Kagi', 'cost': 27,
                      'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                      'upgrades': (SYSTEM, CANNON, CREW, CREW, TITLE, MOD)},
                     {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Colonel Jendon', 'cost': 26,
                      'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                      'upgrades': (SYSTEM, CANNON, CREW, CREW, TITLE, MOD)},
                     {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Captain Yorr', 'cost': 24,
                      'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                      'upgrades': (SYSTEM, CANNON, CREW, CREW, TITLE, MOD)},
                     {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Omicron Group Pilot', 'cost': 21,
                      'upgrades': (SYSTEM, CANNON, CREW, CREW, TITLE, MOD)}),

    TIE_BOMBER: (
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Gamma Squadron Veteran', 'cost': 19,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 5,
         'canon_name': 'gammasquadronveteran',
         'upgrades': (TITLE, TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD, EPT)},

        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Deathfire', 'cost': 17,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 3,
         'canon_name': 'deathfire',
         'upgrades': (TITLE, TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD)},

        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Tomax Bren', 'cost': 24,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'pilot_skill' : 8,
         'canon_name': 'tomaxbren',
         'upgrades': (TITLE, TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD, EPT)},



        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Major Rhymer', 'cost': 26,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (TITLE, TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD, EPT)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Captain Jonus', 'cost': 22,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (TITLE, TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD, EPT)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Gamma Squadron Pilot', 'cost': 18,
         'upgrades': (TITLE, TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Scimitar Squadron Pilot', 'cost': 16,
         'upgrades': (TITLE, TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD)}),

    TIE_DEFENDER: (
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Glaive Squadron Pilot', 'cost': 34,
                    'upgrades': (TITLE, MISSILE, CANNON, MOD, EPT)
         },
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Countess Ryad', 'cost': 34,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                    'upgrades': (TITLE, MISSILE, CANNON, MOD, EPT)
         },
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Maarek Stele', 'cost': 35,
                    'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                    'upgrades': (TITLE, MISSILE, CANNON, MOD, EPT)
         },

        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Rexler Brath', 'cost': 37,
                    'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                    'upgrades': (TITLE, MISSILE, CANNON, MOD, EPT)
         },
                   {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Colonel Vessery', 'cost': 35,
                    'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                    'upgrades': (TITLE, MISSILE, CANNON, MOD, EPT)},
                   {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Onyx Squadron Pilot', 'cost': 32,
                    'upgrades': (TITLE, MISSILE, CANNON, MOD)},
                   {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Delta Squadron Pilot', 'cost': 30,
                    'upgrades': (TITLE, MISSILE, CANNON, MOD)}),

    TIE_PHANTOM: ({'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Whisper', 'cost': 32,
                   'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                   'upgrades': (CREW, SYSTEM, MOD, EPT)},
                  {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Echo', 'cost': 30,
                   'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
                   'upgrades': (CREW, SYSTEM, MOD, EPT)},
                  {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Shadow Squadron Pilot', 'cost': 27,
                   'upgrades': (CREW, SYSTEM, MOD)},
                  {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Sigma Squadron Pilot', 'cost': 25,
                   'upgrades': (CREW, SYSTEM, MOD)}),

    VT_DECIMATOR: (
        {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Rear Admiral Chiraneau', 'cost': 46,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD, EPT)},
        {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Commander Kenkirk', 'cost': 44,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD, EPT)},
        {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Captain Oicunn', 'cost': 42,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT,),
         'upgrades': (BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD, EPT)},
        {'ship_size': LARGE_SHIP, 'faction': IMPERIAL, 'name': 'Patrol Leader', 'cost': 40,
         'upgrades': (BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD)}
    ),

    AGGRESSOR: (
        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'IG-88A', 'canon_name': 'ig88a', 'cost': 36,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, SCUM_FACTION_CONSTRAINT),
         'upgrades': (EPT, CANNON, CANNON, BOMB, TITLE, SYSTEM, ILLICIT, MOD)},

        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'IG-88B', 'canon_name': 'ig88b', 'cost': 36,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, SCUM_FACTION_CONSTRAINT),
         'upgrades': (EPT, CANNON, CANNON, BOMB, TITLE, SYSTEM, ILLICIT, MOD)},

        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'IG-88C', 'canon_name': 'ig88c', 'cost': 36,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, SCUM_FACTION_CONSTRAINT),
         'upgrades': (EPT, CANNON, CANNON, BOMB, TITLE, SYSTEM, ILLICIT, MOD)},
        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'IG-88D', 'canon_name': 'ig88d', 'cost': 36,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, SCUM_FACTION_CONSTRAINT),
         'upgrades': (EPT, CANNON, CANNON, BOMB, TITLE, SYSTEM, ILLICIT, MOD)},

    ),

    STAR_VIPER: (
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Black Sun Enforcer', 'canon_name': 'blacksunenforcer',
         'cost': 25,
         'upgrades': (TORPEDO, TITLE, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Black Sun Vigo', 'canon_name': 'blacksunvigo', 'cost': 27,
         'upgrades': (TORPEDO, TITLE, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Guri', 'canon_name': 'guri', 'cost': 30,
         'upgrades': (EPT, TORPEDO, TITLE, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Prince Xizor', 'canon_name': 'princexizor', 'cost': 31,
         'upgrades': (EPT, TORPEDO, TITLE, MOD)},

    ),

    M3_A_INTERCEPTOR: (
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Cartel Spacer', 'canon_name': 'cartelspacer', 'cost': 14,
         'upgrades': (TITLE, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Tansarii Point Veteran',
         'canon_name': 'tansariipointveteran', 'cost': 17,
         'upgrades': (EPT, TITLE, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Laetin Ashera', 'canon_name': 'laetinashera', 'cost': 18,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, SCUM_FACTION_CONSTRAINT),
         'upgrades': (TITLE, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Serissu', 'canon_name': 'serissu', 'cost': 20,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, SCUM_FACTION_CONSTRAINT),
         'upgrades': (EPT, TITLE, MOD)},
    ),

    YV_666_FREIGHTER: [
        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Bossk', 'canon_name': 'bossk', 'pilot_skill': 7, 'cost': 35,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, SCUM_FACTION_CONSTRAINT),
         'upgrades': (EPT, CANNON, MISSILE, CREW, CREW, CREW, ILLICIT, TITLE, MOD)},
        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Moralo Eval', 'canon_name': 'moraloeval', 'pilot_skill': 6,
         'cost': 34,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, SCUM_FACTION_CONSTRAINT),
         'upgrades': (CANNON, MISSILE, CREW, CREW, CREW, ILLICIT, TITLE, MOD)},
        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Latts Razzi', 'canon_name': 'lattsrazzi', 'pilot_skill': 5,
         'cost': 33,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, SCUM_FACTION_CONSTRAINT),
         'upgrades': (CANNON, MISSILE, CREW, CREW, CREW, ILLICIT, TITLE, MOD)},
        {'ship_size': LARGE_SHIP, 'faction': SCUM, 'name': 'Trandoshan Slaver', 'canon_name': 'trandoshanslaver',
         'pilot_skill': 7, 'cost': 29,
         'constraints': (SCUM_FACTION_CONSTRAINT),
         'upgrades': (CANNON, MISSILE, CREW, CREW, CREW, ILLICIT, TITLE, MOD)},

    ],
    KIHRAXZ_FIGHTER: [
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Talonbane Cobra', 'canon_name': 'talonbanecobra',
         'pilot_skill': 9, 'cost': 28,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, SCUM_FACTION_CONSTRAINT),
         'upgrades': (EPT, MISSILE, ILLICIT, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Graz The Hunter', 'canon_name': 'grazthehunter',
         'pilot_skill': 6, 'cost': 25,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, SCUM_FACTION_CONSTRAINT),
         'upgrades': (MISSILE, ILLICIT, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Black Sun Ace', 'canon_name': 'blacksunace',
         'pilot_skill': 5, 'cost': 23,
         'constraints': (SCUM_FACTION_CONSTRAINT),
         'upgrades': (EPT, MISSILE, ILLICIT, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': SCUM, 'name': 'Cartel Marauder', 'canon_name': 'cartelmarauder',
         'pilot_skill': 2, 'cost': 20,
         'constraints': (SCUM_FACTION_CONSTRAINT),
         'upgrades': (MISSILE, ILLICIT, MOD)},
    ],
    TIE_PUNISHER: [
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Redline', 'canon_name': 'redline', 'pilot_skill': 7,
         'cost': 27,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, IMPERIAL_FACTION_CONSTRAINT),
         'upgrades': (SYSTEM, TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, BOMB, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Deathrain', 'canon_name': 'Deathrain', 'pilot_skill': 6,
         'cost': 26,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, IMPERIAL_FACTION_CONSTRAINT),
         'upgrades': (SYSTEM, TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, BOMB, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Black Eight Sq. Pilot',
         'canon_name': 'blackeightsqpilot', 'pilot_skill': 4, 'cost': 23,
         'constraints': (IMPERIAL_FACTION_CONSTRAINT),
         'upgrades': (SYSTEM, TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, BOMB, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': IMPERIAL, 'name': 'Cutlass Squadron Pilot',
         'canon_name': 'cutlasssquadronpilot', 'pilot_skill': 2, 'cost': 21,
         'constraints': (IMPERIAL_FACTION_CONSTRAINT),
         'upgrades': (SYSTEM, TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, BOMB, MOD)},
    ],
    K_WING: [
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Miranda Doni', 'canon_name': 'mirandadoni',
         'pilot_skill': 8, 'cost': 29,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, REBEL_FACTION_CONSTRAINT),
         'upgrades': (TURRET, TORPEDO, TORPEDO, MISSILE, CREW, BOMB, BOMB, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Esege Tuketu', 'canon_name': 'esegetuketu',
         'pilot_skill': 6, 'cost': 28,
         'constraints': (PER_SQUAD_UNIQUE_CONSTRAINT, REBEL_FACTION_CONSTRAINT),
         'upgrades': (TURRET, TORPEDO, TORPEDO, MISSILE, CREW, BOMB, BOMB, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Guardian Squadron Pilot',
         'canon_name': 'guardiansquadronpilot', 'pilot_skill': 4, 'cost': 25,
         'constraints': (REBEL_FACTION_CONSTRAINT),
         'upgrades': (TURRET, TORPEDO, TORPEDO, MISSILE, CREW, BOMB, BOMB, MOD)},
        {'ship_size': SMALL_SHIP, 'faction': REBEL, 'name': 'Warden Squadron Pilot',
         'canon_name': 'wardensquadronpilot', 'pilot_skill': 2, 'cost': 23,
         'constraints': (REBEL_FACTION_CONSTRAINT),
         'upgrades': (TURRET, TORPEDO, TORPEDO, MISSILE, CREW, BOMB, BOMB, MOD)},
    ]

}

alpha_num_only_pattern = re.compile('[\W_]+')


# rules
# Take the English-language name as printed on the card
# Check for special case exceptions to these rules (see below)
# Lowercase the name
# Convert non-ASCII characters to closest ASCII equivalent (to remove umlauts, etc.)
# Remove non-alphanumeric characters

def canonize(value):
    # first lower case it
    lc_value = value.lower()

    # then remove non alphanumeric characters
    lc_alphanum_value = alpha_num_only_pattern.sub('', lc_value)

    return lc_alphanum_value


class XWingMetaData:
    def is_rebel(self):
        self.is_rebel = True

    def is_imperial(self):
        self.is_rebel = False

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

    def tech(self):
        return self.upgrades()(TECH)
