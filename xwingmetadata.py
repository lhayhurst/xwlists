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

upgrades = { DROID: (
                    {'name':'R2 Astromech', 'cost': 1},
                    {'name':'R5 Astromech', 'cost': 1},
                    {'name':'R4-D6', 'cost': 1},
                    {'name':'R5-K6','cost': 2},
                    {'name':'R3-A2', 'cost': 2},
                    {'name':'R7 Astromech', 'cost': 2},
                    {'name':'R2-F2',  'cost': 3},
                    {'name': 'R5-D8', 'cost': 3},
                    {'name':'R5-P9', 'cost': 3},
                    {'name':'R7-T1', 'cost': 3},
                    {'name': 'R2-D2', 'cost': 4},
                    ),
             TITLE: (
                    {'name':'Outrider', 'cost': 5},
                    {'name':'Moldy Crow',  'cost': 3},
                    {'name':'ST-321',  'cost': 3},
                    {'name':'Dauntless',  'cost': 2},
                    {'name':'Millennium Falcon', 'cost': 1},
                    {'name':'Slave 1', 'cost': 0},
                    {'name':'Royal Guard TIE',  'cost': 0},
                    {'name':'A-Wing Test Pilot',  'cost': 0},
                    ),
             SYSTEM: (
                   {'name':'Sensor Jammer', 'cost':4 },
                   {'name':'Advanced Sensors', 'cost': 3 },
                   {'name':'Fire-Control System','cost' : 2 },
                   {'name':'Enhanced Scopes', 'cost' : 1 }
             )
}


ships = {X_WING: ( {'name': 'Wedge Antilles', 'cost': 29, 'upgrades': [DROID, TORPEDO, MOD, EPT]},
                   {'name': 'Luke Skywalker', 'cost': 28, 'upgrades': [DROID, TORPEDO, MOD, EPT]},
                   {'name': 'Wes Janson', 'cost': 29, 'upgrades': [DROID, TORPEDO, MOD, EPT]},
                   {'name': 'Jek Porkins', 'cost': 26, 'upgrades': [DROID, TORPEDO, MOD, EPT]},
                   {'name': 'Red Squadron Pilot', 'cost': 23, 'upgrades': [DROID, TORPEDO, MOD]},
                   {'name': 'Garven Dreis', 'cost': 26, 'upgrades': [DROID, TORPEDO, MOD]},
                   {'name': 'Rookie Pilot', 'cost': 21, 'upgrades': [DROID, TORPEDO, MOD]},
                   {'name': 'Biggs Darklighter', 'cost': 25, 'upgrades': [DROID, TORPEDO, MOD]},
                   {'name': 'Hobbie" Klivian', 'cost': 25, 'upgrades': [DROID, TORPEDO, MOD]},
                   {'name': 'Tarn Mison', 'cost': 23, 'upgrades': [DROID, TORPEDO, MOD]} ),

         Y_WING: ({'name': 'Horton Salm', 'cost': 25, 'upgrades': [TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD]},
                  {'name': 'Gray Squadron Pilot', 'cost': 20,
                   'upgrades': [TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD]},
                  {'name': 'Dutch Vander', 'cost': 23, 'upgrades': [TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD]},
                  {'name': 'Gold Squadron Pilot', 'cost': 18,
                   'upgrades': [TITLE, DROID, TORPEDO, TORPEDO, TURRET, MOD]} ),

         A_WING: ({'name': 'Tycho Celchu', 'cost': 26, 'upgrades': [TITLE, MISSILE, EPT, MOD]},
                  {'name': 'Green Sq. Pilot', 'cost': 19, 'upgrades': [TITLE, MISSILE, EPT, MOD]},
                  {'name': 'Arvel Crynyd', 'cost': 23, 'upgrades': [TITLE, MISSILE, MOD]},
                  {'name': 'Prototype Pilot', 'cost': 17, 'upgrades': [TITLE, MISSILE, MOD]},
                  {'name': 'Gemmer Sojan', 'cost': 22, 'upgrades': [TITLE, MISSILE, MOD]},
                  {'name': 'Jake Farrell', 'cost': 24, 'upgrades': [TITLE, MISSILE, EPT, MOD]} ),

         YT_1300: ({'name': 'Han Solo', 'cost': 46, 'upgrades': [EPT, MISSILE, TITLE, MOD, CREW, CREW]},
                   {'name': 'Chewbacca', 'cost': 42, 'upgrades': [EPT, MISSILE, TITLE, MOD, CREW, CREW]},
                   {'name': 'Lando Calrissian', 'cost': 44, 'upgrades': [EPT, MISSILE, TITLE, MOD, CREW, CREW]},
                   {'name': 'Outer Rim Smuggler', 'cost': 27, 'upgrades': [CREW, CREW, TITLE, MOD]} ),

         B_WING: ({'name': 'Ten Numb', 'cost': 31, 'upgrades': [SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD]},
                  {'name': 'Keyan Farlander', 'cost': 29, 'upgrades': [SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD]},
                  {'name': 'Ibtisam', 'cost': 28, 'upgrades': [SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD]},
                  {'name': 'Nera Dantels', 'cost': 26, 'upgrades': [SYSTEM, CANNON, TORPEDO, TORPEDO, EPT, MOD]},
                  {'name': 'Dagger Sq. Pilot', 'cost': 24, 'upgrades': [SYSTEM, CANNON, TORPEDO, TORPEDO, MOD]},
                  {'name': 'Blue Sq. Pilot', 'cost': 22, 'upgrades': [SYSTEM, CANNON, TORPEDO, TORPEDO, MOD]} ),

         HWK_290: ({'name': 'Jan Ors', 'cost': 25, 'upgrades': [EPT, TURRET, CREW, TITLE, MOD]},
                   {'name': 'Kyle Katarn', 'cost': 21, 'upgrades': [EPT, TURRET, CREW, TITLE, MOD]},
                   {'name': 'Roark Garnet', 'cost': 19, 'upgrades': [TURRET, CREW, TITLE, MOD]},
                   {'name': 'Rebel Operative', 'cost': 16, 'upgrades': [TURRET, CREW, TITLE, MOD]} ),


         E_WING: ({'name': 'Corran Horn', 'cost': 35, 'upgrades': [DROID, TORPEDO, SYSTEM, EPT, MOD]},
                  {'name': 'Etahn A\'Baht', 'cost': 32, 'upgrades': [DROID, TORPEDO, SYSTEM, EPT, MOD]},
                  {'name': 'Blackmoon Squadron Pilot', 'cost': 29, 'upgrades': [DROID, TORPEDO, SYSTEM, MOD]},
                  {'name': 'Knave Squadron Pilot', 'cost': 27, 'upgrades': [DROID, TORPEDO, SYSTEM, MOD]} ),

         Z95_HEADHUNTER: ({'name': 'Airen Cracken', 'cost': 19, 'upgrades': [MISSILE, EPT, MOD]},
                          {'name': 'Lt. Blount', 'cost': 17, 'upgrades': [MISSILE, EPT, MOD]},
                          {'name': 'Tala Squadron Pilot', 'cost': 13, 'upgrades': [MISSILE, MOD]},
                          {'name': 'Bandit Squadron Pilot', 'cost': 12, 'upgrades': [MISSILE, MOD]} ),

         YT_2400: ( {'name': 'Dash Rendar', 'cost': 36, 'upgrades': [EPT, CANNON, MISSILE, CREW, TITLE, MOD]},
                    {'name': 'Leebo', 'cost': 34, 'upgrades': [EPT, CANNON, MISSILE, CREW, TITLE, MOD]},
                    {'name': 'Eaden Vrill', 'cost': 32, 'upgrades': [CANNON, MISSILE, CREW, TITLE, MOD]},
                    {'name': 'Wild Space Fringer', 'cost': 30, 'upgrades': [CANNON, MISSILE, CREW, TITLE, MOD]} ),

         TIE_FIGHTER: ( {'name': 'Howlrunner', 'cost': 18, 'upgrades': [EPT, MOD]},
                        {'name': 'Mauler Mithel', 'cost': 17, 'upgrades': [EPT, MOD]},
                        {'name': 'Dark Curse', 'cost': 16, 'upgrades': [MOD]},
                        {'name': 'Backstabber', 'cost': 16, 'upgrades': [MOD]},
                        {'name': 'Winged Gundark', 'cost': 15, 'upgrades': [MOD]},
                        {'name': 'Night Beast', 'cost': 15, 'upgrades': [MOD]},
                        {'name': 'Black Squadron Pilot', 'cost': 14, 'upgrades': [EPT, MOD]},
                        {'name': 'Obsidian Squadron Pilot', 'cost': 13, 'upgrades': [MOD]},
                        {'name': 'Academy Pilot', 'cost': 12, 'upgrades': [MOD]} ),

         TIE_ADVANCED: ({'name': 'Darth Vader', 'cost': 29, 'upgrades': [MISSILE, EPT, MOD]},
                        {'name': 'Maarek Steel', 'cost': 27, 'upgrades': [MISSILE, EPT, MOD]},
                        {'name': 'Storm Squadron Pilot', 'cost': 23, 'upgrades': [MISSILE, MOD]},
                        {'name': 'Tempest Squadron Pilot', 'cost': 21, 'upgrades': [MISSILE, MOD]} ),

         TIE_INTERCEPTOR: ({'name': 'Soontir Fel', 'cost': 27, 'upgrades': [TITLE, EPT, MOD]},
                           {'name': 'Carnor Jax', 'cost': 26, 'upgrades': [TITLE, EPT, MOD]},
                           {'name': 'Turr Phennir', 'cost': 25, 'upgrades': [TITLE, EPT, MOD]},
                           {'name': 'Tetran Cowall', 'cost': 24, 'upgrades': [TITLE, EPT, MOD]},
                           {'name': 'Kir Kanos', 'cost': 24, 'upgrades': [TITLE, MOD]},
                           {'name': 'Lt. Lorrir', 'cost': 23, 'upgrades': [TITLE, MOD]},
                           {'name': 'Fel\'s Wrath', 'cost': 23, 'upgrades': [TITLE, MOD]},
                           {'name': 'Royal Guard Pilot', 'cost': 22, 'upgrades': [TITLE, EPT, MOD]},
                           {'name': 'Saber Squadron Pilot', 'cost': 21, 'upgrades': [TITLE, EPT, MOD]},
                           {'name': 'Avenger Squadron Pilot', 'cost': 20, 'upgrades': [TITLE, MOD]},
                           {'name': 'Alpha Squadron Pilot', 'cost': 18, 'upgrades': [TITLE, MOD]} ),

         FIRESPRAY_31: ({'name': 'Boba Fett', 'cost': 39, 'upgrades': [MISSILE, CANNON, BOMB, EPT, TITLE, MOD, CREW]},
                        {'name': 'Kath Scarlet', 'cost': 38,
                         'upgrades': [MISSILE, CANNON, BOMB, EPT, TITLE, MOD, CREW]},
                        {'name': 'Krassis Trelix', 'cost': 36, 'upgrades': [MISSILE, CANNON, BOMB, TITLE, MOD, CREW]},
                        {'name': 'Bounty Hunter', 'cost': 33, 'upgrades': [MISSILE, CANNON, BOMB, TITLE, MOD, CREW]}, ),

         LAMBDA_SHUTTLE: ({'name': 'Captain Kagi', 'cost': 27, 'upgrades': [SYSTEM, CANNON, CREW, CREW, TITLE, MOD]},
                          {'name': 'Colonel Jendon', 'cost': 26, 'upgrades': [SYSTEM, CANNON, CREW, CREW, TITLE, MOD]},
                          {'name': 'Captain Yorr', 'cost': 24, 'upgrades': [SYSTEM, CANNON, CREW, CREW, TITLE, MOD]},
                          {'name': 'Omicron Group Pilot', 'cost': 21,
                           'upgrades': [SYSTEM, CANNON, CREW, CREW, TITLE, MOD]} ),

         TIE_BOMBER: (
         {'name': 'Major Rhymer', 'cost': 26, 'upgrades': [TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD, EPT]},
         {'name': 'Captain Jonus', 'cost': 22, 'upgrades': [TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD, EPT]},
         {'name': 'Gamma Squadron. Pilot', 'cost': 18, 'upgrades': [TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD]},
         {'name': 'Scimitar Squadron Pilot', 'cost': 16, 'upgrades': [TORPEDO, TORPEDO, MISSILE, MISSILE, BOMB, MOD]} ),

         TIE_DEFENDER: ({'name': 'Rexler Brath', 'cost': 37, 'upgrades': [MISSILE, CANNON, MOD, EPT]},
                        {'name': 'Col. Vessery', 'cost': 35, 'upgrades': [MISSILE, CANNON, MOD, EPT]},
                        {'name': 'Onyx Squadron Pilot', 'cost': 32, 'upgrades': [MISSILE, CANNON, MOD]},
                        {'name': 'Delta Squadron Pilot', 'cost': 30, 'upgrades': [MISSILE, CANNON, MOD]} ),

         TIE_PHANTOM: ({'name': 'Whisper', 'cost': 32, 'upgrades': [CREW, SYSTEM, MOD, EPT]},
                       {'name': 'Echo', 'cost': 30, 'upgrades': [CREW, SYSTEM, MOD, EPT]},
                       {'name': 'Shadow Squadron Pilot', 'cost': 27, 'upgrades': [CREW, SYSTEM, MOD]},
                       {'name': 'Sigma Squadron Pilot', 'cost': 25, 'upgrades': [CREW, SYSTEM, MOD]} ),

         VT_DECIMATOR: (
         {'name': 'Rear Admiral Chiraneau', 'cost': 46, 'upgrades': [BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD, EPT]},
         {'name': 'Commander Kenkirk', 'cost': 44, 'upgrades': [BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD, EPT]},
         {'name': 'Captain Oicunn', 'cost': 42, 'upgrades': [BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD, EPT]},
         {'name': 'Patrol Leader', 'cost': 40, 'upgrades': [BOMB, CREW, CREW, CREW, TORPEDO, TITLE, MOD]} )}



crew = ('Luke Skywalker',
        'Gunner',
        'Chewbacca',
        'Leia Organa',
        'R2-D2',
        'Flight Instructor',
        'Ysanne Isard',
        'C-3PO',
        'Darth Vader',
        'Rebel Captive',
        'Weapons Engineer',
        'Recon Specialist',
        'Navigator',
        'Kyle Katarn',
        'Lando Calrissian',
        'Fleet Officer',
        'Mara Jade',
        'Han Solo',
        'Mercenary Copilot',
        'Saboteur',
        'Tactician',
        'Jan Ors',
        'Dash Rendar',
        'Leebo',
        'Moff Jerjerrod',
        'Nien Nunb',
        'Intelligence Agent')

epts = ('Expose',
        'Opportunist',
        'Push the Limit',
        'Marksmanship',
        'Daredevil',
        'Outmaneuver',
        'Predator',
        'Ruthlessness',
        'Swarm Tactics',
        'Squad Leader',
        'Expert Handling',
        'Elusiveness',
        'Wingman',
        'Decoy',
        'Lone Wolf',
        'Stay on Target',
        'Intimidation',
        'Veteran Instincts',
        'Draw Their Fire',
        'Determination',
        'Deadeye',
        'Adrenaline Rush')


mods = ('Combat Retrofit',
        'Shield Upgrade',
        'Engine Upgrade',
        'Advanced Cloaking Device',
        'Stealth Device',
        'Hull Upgrade',
        'Counter-Measures',
        'Experimental Interface',
        'Anti-Pursuit Lasers',
        'Targeting Computer',
        'Stygium Particle Accelerator',
        'Munitions Failsafe',
        'B-Wing/E2',
        'Tactical Jammer')



bombs_mines = ( 'Proton Bombs', 'Proximity Mines', 'Seismic Charges')

cannons = ('Heavy Laser Cannon', 'AutoBlaster', 'Ion Cannon')

missiles = ('Assault Missiles',
            'Homing Missiles',
            'Concussion Missiles',
            'Cluster Missiles',
            'Ion Pulse Missle',
            'Proton Rockets',
            'Chardaan Refit')

torpedos = ('Advanced Proton Torpedoes',
            'Ion Torpedoes',
            'Proton Torpedos',
            'Flechette Torpedoes')

turrets = ('Ion Cannon Turret', 'Blaster Turret')


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
        return ships[ship]

    def droids(self):
        return self.upgrades()[DROID]

    def system_upgrades(self):
        return self.upgrades()[SYSTEM]

    def titles(self):
        return self.upgrades()[TITLE]


    def crew(self):
        return crew

    def epts(self):
        return epts


    def mods(self):
        return mods


    def bomb_mines(self):
        return bombs_mines

    def cannons(self):
        return cannons

    def torpedos(self):
        return torpedos

    def missiles(self):
        return missiles

    def turrets(self):
        return turrets


class XWingList:
    def get_ship_for_id(self, id, request_form):
        ship = {}
        for k in request_form.keys():
            if k.endswith(id) and request_form[k] is not None and len(request_form[k]) > 0:
                ship[k] = request_form[k]
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

        self.player = request_form['player']
        self.faction = request_form['faction']
        self.points = request_form['points']

        self.ships_submitted = self.get_ships_submitted(request_form)

