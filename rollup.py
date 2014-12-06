import xwingmetadata

COUNT_MEASURE       = 'COUNT_MEASURE'
POINT_COST_MEASURE  = 'POINT_COST_MEASURE'
FACTION_SHIP_ROLLUP = 'FACTION_SHIP_ROLLUP'

class Rollup:

    def __init__(self,pm):
        self.pm = pm

    def title(self):
        if not self.use_points:
            return ": %d samples" % ( self.grand_count)
        else:
            return ": %s points spent" % ( "{:,}".format(self.grand_sum ) )

    def to_float(self, dec):
        return float("{0:.2f}".format( float(dec) * float(100)))

    def rollup_by_ship_faction(self, use_points):
        self.use_points = use_points
        rollups = self.pm.get_ship_faction_rollups()
        self.grand_count   = 0
        self.grand_sum     = 0
        self.factions = {}
        self.ships         = {}

        for row in rollups['pilots']:
            faction = row[0]
            ship    = row[1]
            cnt     = row[2]
            cost    = row[3]
            if faction is None and ship is None:
                #grand total
                self.grand_count = cnt
                self.grand_sum   = cost
            elif faction is not None and ship is None:
                #faction total
                self.factions[faction.description] = { 'cnt' : cnt, 'cost': cost }
            else:
                #ship total
                self.ships[ ship.description ] = { 'faction': faction.description, 'cnt': cnt, 'cost': cost}

        ret = []
        faction_drilldowns = {}
        for faction in self.factions.keys():
            drilldown = {
              'name': faction,
              'categories': [],
              'data' : [],
              'color' : None
            }

            faction_drilldowns[ faction ] = drilldown

            ratio = 0.0
            if not use_points:
                ratio = self.to_float( self.to_float( self.factions[faction]['cnt'] ) / self.to_float(self.grand_count) )
            else:
                ratio = self.to_float( self.to_float( self.factions[faction]['cost'] ) / self.to_float(self.grand_sum) )

            ret.append( { 'y' : ratio,
                         'color' : None,
                         'drilldown' : drilldown
                        })
        for ship in self.ships.keys():
            val       = self.ships[ship]
            faction   = val['faction']
            drilldown = faction_drilldowns[faction]
            drilldown[ 'categories'].append( ship )
            ratio = 0.0
            if not use_points:
                ratio = self.to_float( self.to_float( val['cnt'] ) / self.to_float( self.grand_count ) )
            else:
                ratio = self.to_float( self.to_float( val['cost'] ) / self.to_float( self.grand_sum ) )
            drilldown[ 'data' ].append( ratio )

        return ret