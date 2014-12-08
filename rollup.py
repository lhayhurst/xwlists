import xwingmetadata

COUNT_MEASURE       = 'COUNT_MEASURE'
POINT_COST_MEASURE  = 'POINT_COST_MEASURE'
FACTION_SHIP_ROLLUP = 'FACTION_SHIP_ROLLUP'

class Rollup:



    def __init__(self,pm, request_type):
        self.pm = pm
    # ship-pilot-count
    # ship-pilot-points
    # action-ship-count
    # faction-ship-points

        self.chart_request_type = request_type

        if self.chart_request_type.endswith('points'):
            self.use_points = True
        else:
            self.use_points = False

    def title(self):
        if not self.use_points:
            return ": %d samples" % ( self.grand_count)
        else:
            return ": %s points spent" % ( "{:,}".format(self.grand_sum ) )

    def category_at(self, index_of):
        return self.chart_request_type.split('-')[index_of]

    def first_category(self):
        return self.category_at( 0 )

    def second_category(self):
        return self.category_at( 1 )



    def to_float(self, dec):
        return float("{0:.2f}".format( float(dec) * float(100)))

    def rollup(self):
        ret = None
        if self.chart_request_type == 'faction-ship-points' or self.chart_request_type == 'faction-ship-count':
            ret = self._rollup( self.pm.get_ship_faction_rollups(), has_pilot=False)

        elif self.chart_request_type.startswith( 'ship-pilot'):
            ret = self._rollup( self.pm.get_ship_pilot_rollup(), has_pilot=True)

        sorted_ret = sorted( ret, key=lambda record: record['faction'])


        return sorted_ret

    colors = ["#7cb5ec", "#434348", "#90ed7d"]
    def get_faction_color(self, faction):
        if faction == xwingmetadata.IMPERIAL:
            return Rollup.colors[1]
        elif faction == xwingmetadata.REBEL:
            return Rollup.colors[0]
        else:
            return Rollup.colors[2]

    def is_grand_total(self, faction, ship, has_pilot, pilot):
        if has_pilot:
            return faction is None and ship is None and pilot is None
        else:
            return faction is None and ship is None

    def is_faction_total(self, faction, ship, has_pilot, pilot):
        if has_pilot:
            return faction is not None and ship is None and pilot is None
        else:
            return faction is not None and ship is None

    def is_ship_total(self, faction, ship, has_pilot, pilot):
       if has_pilot:
           return faction is not None and ship is not None and pilot is None
       else:
           return faction is not None and ship is not None

    def create_faction_ship_doughnut_data(self):
        ret = []
        faction_drilldowns = {}
        for faction in self.factions.keys():
            drilldown = {
              'name': faction,
              'categories': [],
              'data' : [],
              'color' : self.get_faction_color(faction)
            }

            faction_drilldowns[ faction ] = drilldown

            ratio = 0.0
            if not self.use_points:
                ratio = self.to_float( self.to_float( self.factions[faction]['cnt'] ) / self.to_float(self.grand_count) )
            else:
                ratio = self.to_float( self.to_float( self.factions[faction]['cost'] ) / self.to_float(self.grand_sum) )

            ret.append( { 'y' : ratio,
                          'faction':faction,
                         'color' : self.get_faction_color(faction),
                         'drilldown' : drilldown
                        })
        for ship in self.ships.keys():
            val       = self.ships[ship]
            faction   = val['faction']
            drilldown = faction_drilldowns[faction]
            drilldown[ 'categories'].append( ship )
            ratio = 0.0
            if not self.use_points:
                ratio = self.to_float( self.to_float( val['cnt'] ) / self.to_float( self.grand_count ) )
            else:
                ratio = self.to_float( self.to_float( val['cost'] ) / self.to_float( self.grand_sum ) )
            drilldown[ 'data' ].append( ratio )

        return ret
    def create_ship_pilot_doughnut_data(self):
        ret = []
        ship_drilldowns = {}
        for ship_name in self.ships.keys():
            faction = self.ships[ship_name]['faction']

            drilldown = {
                'name': ship_name,
                'categories': [],
                'data': [],
                'color': self.get_faction_color(faction)
            }

            ship_drilldowns[ship_name] = drilldown

            ratio = 0.0
            if not self.use_points:
                ratio = self.to_float(self.to_float(self.ships[ship_name]['cnt']) / self.to_float(self.grand_count))
            else:
                ratio = self.to_float(self.to_float(self.ships[ship_name]['cost']) / self.to_float(self.grand_sum))

            ret.append({'y': ratio,
                        'faction': faction,
                        'color': self.get_faction_color(faction),
                        'drilldown': drilldown
            })
        for pilot in self.pilots.keys():
            val = self.pilots[pilot]
            ship = val['ship']
            drilldown = ship_drilldowns[ship]
            drilldown['categories'].append(pilot)
            ratio = 0.0
            if not self.use_points:
                ratio = self.to_float(self.to_float(val['cnt']) / self.to_float(self.grand_count))
            else:
                ratio = self.to_float(self.to_float(val['cost']) / self.to_float(self.grand_sum))
            drilldown['data'].append(ratio)
        return ret

    def _rollup(self, rollups, has_pilot):

        self.grand_count   = 0
        self.grand_sum     = 0
        self.factions      = {}
        self.ships         = {}
        self.pilots        = {}

        for row in rollups:
            faction = row[0]
            ship    = row[1]
            pilot   = cnt = cost = None
            if has_pilot:
                pilot   = row[2]
                cnt     = row[3]
                cost    = row[4]
            else:
                cnt     = row[2]
                cost    = row[3]

            if self.is_grand_total( faction, ship, has_pilot, pilot):
                #grand total
                self.grand_count += cnt
                self.grand_sum   += cost
            elif self.is_faction_total( faction, ship, has_pilot, pilot ):
                #faction total
                if not self.factions.has_key(faction.description ):
                    self.factions[faction.description] = { 'cnt' : cnt, 'cost': cost }
                else:
                    href = self.factions[faction.description]
                    href['cnt']  += cnt
                    href['cost'] += cost
            elif self.is_ship_total( faction, ship, has_pilot, pilot):
                #ship total
                if not self.ships.has_key(ship.description):
                    self.ships[ ship.description ] = { 'faction': faction.description, 'cnt': cnt, 'cost': cost}
                else:
                    href = self.ships[ship.description]
                    href['cnt']  += cnt
                    href['cost'] += cost
            else: #full pilot row
                if not self.pilots.has_key( pilot ):
                    self.pilots[ pilot ] = { 'faction': faction.description, 'ship' : ship.description,
                                                         'cnt' : cnt, 'cost': cost, }

                else:
                    href = self.pilots[pilot]
                    href['cnt']  += cnt
                    href['cost'] += cost

        if has_pilot:
            return self.create_ship_pilot_doughnut_data()
        else:
            return self.create_faction_ship_doughnut_data()


