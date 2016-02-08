import collections
from sqlalchemy import and_, func
import sqlalchemy
from sqlalchemy.dialects import mysql
from persistence import Faction, ArchtypeList, ShipPilot, Pilot, Tourney, TourneyList, Ship

COUNT_MEASURE       = 'COUNT_MEASURE'
POINT_COST_MEASURE  = 'POINT_COST_MEASURE'
FACTION_SHIP_ROLLUP = 'FACTION_SHIP_ROLLUP'


class HighChartLineGraphOptions:
    def __init__(self, title, yaxis_label, subtitle='', chart_type=None, plot_options=None ):
        self.options = {
            'title': {
                'text': title,
                'x': -20 #center
            },
            'subtitle': {
                'text': subtitle,
                'x': -20
            },
            'yAxis': {
                'title': {
                    'text': yaxis_label,
                },
                'plotLines': [
                    {
                        'value': 0,
                        'width': 1,
                        'color': '#808080'
                    }
                ]
            },
           'tooltip': {
                'valueSuffix': ''
            },

            'xAxis': {
                'categories' : [],
                'tickerPlacement' :'on',
                'title' : { 'enabled': "false" }
            }
        }
        if plot_options:
            self.options['plot_options']=plot_options

        if chart_type is not None:
            self.options['chart'] = chart_type

    def get_options(self):
        return self.options


class FactionTotalHighChartOptions:
    def __init__(self, ship_pilot_time_series_data):

        hclgo = HighChartLineGraphOptions(title="Faction Total",
                                          yaxis_label="Ships taken" )
        self.options = hclgo.get_options()
        series = {}
        for year in ship_pilot_time_series_data.summary.keys():
            for month in ship_pilot_time_series_data.summary[year].keys():
                year_mo = str(year) + "-" + str(month)
                self.options['xAxis']['categories'].append( year_mo )
                summary = ship_pilot_time_series_data.summary[year][month]
                factions = summary['faction']


                for faction in factions.keys():
                    if not series.has_key(faction):
                        series[faction] = { 'name': faction, 'data':[] }
                    series[faction]['data'].append( factions[faction])

                #if data is missing for the faction (which happend pre-scum release,
                #add it in

                if not factions.has_key(Faction.SCUM.description):
                    if not series.has_key(Faction.SCUM.description):
                        series[Faction.SCUM.description] = { 'name': Faction.SCUM.description, 'data':[] }
                    series[Faction.SCUM.description]['data'].append( 0 )
        self.options['series'] = []
        for faction in series.keys():
            self.options['series'].append(series[faction])

class ShipTotalHighchartOptions:

    def __init__(self, ship_pilot_time_series_data):
        hclgo = HighChartLineGraphOptions(title="Ship Total", yaxis_label="Ships taken")
        self.options = hclgo.get_options()
        series = {}
        series['total'] = { 'type': 'area', 'name': 'Total', 'data':[]}
        for year in ship_pilot_time_series_data.summary.keys():
            for month in ship_pilot_time_series_data.summary[year].keys():
                year_mo = str(year) + "-" + str(month)
                self.options['xAxis']['categories'].append( year_mo )
                summary = ship_pilot_time_series_data.summary[year][month]
                series['total']['data'].append(summary['total'])
        self.options['series'] = []
        self.options['series'].append(series['total'])

class ShipHighchartOptions:
    def __init__(self, ship_pilot_time_series_data, ships_by_faction):

        hclgo = HighChartLineGraphOptions(title="Ship-by-Ship Total",
                                          yaxis_label="Ships taken" )
        self.options = hclgo.get_options()
        series = {}
        for year in ship_pilot_time_series_data.summary.keys():
            for month in ship_pilot_time_series_data.summary[year].keys():
                year_mo = str(year) + "-" + str(month)
                self.options['xAxis']['categories'].append( year_mo )
                summary = ship_pilot_time_series_data.summary[year][month]
                ships = summary['ships']

                for ship in ships.keys():
                    if not series.has_key(ship):
                        series[ship] = { 'name': ship, 'data':[] }
                    series[ship]['data'].append( ships[ship])

                #backfill data if its missing
                for rec in ships_by_faction:
                    faction = rec[0]
                    sname   = rec[1].description
                    if not series.has_key(sname):
                        series[sname] = {'name': sname, 'data': []}
                    if not ships.has_key(sname):
                        series[sname]['data'].append(0)

        self.options['series'] = []
        for ship in series.keys():
            self.options['series'].append(series[ship])

class ShipPilotTimeSeriesData:
    def __init__(self, pm):
        self.pm = pm
        session = self.pm.db_connector.get_session()

        filters = [
            TourneyList.tourney_id == Tourney.id ,
            ArchtypeList.id == TourneyList.archtype_id,
            Ship.archtype_id == ArchtypeList.id ,
            Ship.ship_pilot_id == ShipPilot.id ,
            ShipPilot.pilot_id == Pilot.id
        ]

        sql = session.query(
            sqlalchemy.extract('year', Tourney.tourney_date).label("year"),
            sqlalchemy.extract('month', Tourney.tourney_date).label("month"),
            sqlalchemy.extract('day', Tourney.tourney_date).label("day"),
            Tourney.tourney_type,
            ArchtypeList.faction,
            ShipPilot.ship_type,
            Pilot.name.label('pilot'),
            func.count(TourneyList.id).label("count")).\
            filter( and_(*filters)).\
            group_by( sqlalchemy.extract('year', Tourney.tourney_date),
                      sqlalchemy.extract('month', Tourney.tourney_date),
                      sqlalchemy.extract('day', Tourney.tourney_date),
                      ArchtypeList.faction,
                      ShipPilot.ship_type,
                      Pilot.name).\
            statement.compile(dialect=mysql.dialect())

        connection = self.pm.db_connector.get_engine().connect()
        time_series_data = connection.execute(sql)

        summary = collections.OrderedDict()
        for tsd in time_series_data:
            year    = int(tsd['year'])
            month   = int(tsd['month'])
            ship    = tsd['ship_type'].description
            pilot   = tsd['pilot']
            faction = tsd['faction'].description
            count   = int(tsd['count'])

            if not summary.has_key(year):
                summary[year] = collections.OrderedDict()

            if not summary[year].has_key(month):
                summary[year][month] = {}

            s = summary[year][month]

            if not s.has_key('total'):
                s['total'] = 0
            s['total'] += count

            if not s.has_key('faction'):
                s['faction'] = {}
            if not s['faction'].has_key(faction):
                s['faction'][faction] = 0
            s['faction'][faction] += count

            if not s.has_key('ships'):
                s['ships'] = {}

            if not s['ships'].has_key(ship):
                s['ships'][ship] = 0
            s['ships'][ship] += count

        self.summary = summary
        self.line_items = time_series_data


class Rollup:

    def __init__(self,pm, request_type,
                 eliminationOnly,
                 storeChampionshipsOnly=False,
                 regionalChampionshipsOnly=False,
                 nationalChampionshipsOnly=False,):
        self.pm = pm
        self.top32only = eliminationOnly
        self.storeChampionshipsOnly = storeChampionshipsOnly
        self.regionalChampionshipsOnly = regionalChampionshipsOnly
        self.nationalChampionshipsOnly = nationalChampionshipsOnly

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
        sorted_ret = None
        if self.chart_request_type == 'faction-ship-points' or self.chart_request_type == 'faction-ship-count':
            ret = self._rollup( self.pm.get_ship_faction_rollups(self.top32only,
                                                                 self.storeChampionshipsOnly,
                                                                 self.regionalChampionshipsOnly,
                                                                 self.nationalChampionshipsOnly), has_pilot=False)
            sorted_ret = sorted( ret, key=lambda record: record['faction'])

        elif self.chart_request_type.startswith( 'ship-pilot'):
            ret = self._rollup( self.pm.get_ship_pilot_rollup(self.top32only,
                                                              self.storeChampionshipsOnly,
                                                              self.regionalChampionshipsOnly,
                                                              self.nationalChampionshipsOnly), has_pilot=True)
            sorted_ret = sorted( ret, key=lambda record: record['faction'])

        elif self.chart_request_type.startswith('upgrade_type-upgrade'):
            ret = self._rollup_upgrades( self.pm.get_upgrade_rollups(self.top32only,
                                                                     self.storeChampionshipsOnly,
                                                                     self.regionalChampionshipsOnly,
                                                                     self.nationalChampionshipsOnly))
            sorted_ret = ret

        return sorted_ret

    colors = ["#7cb5ec", "#434348", "#90ed7d"]
    def get_faction_color(self, faction):
        if faction == Faction.IMPERIAL.description:
            return Rollup.colors[1]
        elif faction == Faction.REBEL.description:
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
        for faction_and_ship in self.ships.keys():
            val       = self.ships[faction_and_ship]
            faction   = val['faction']
            drilldown = faction_drilldowns[faction]
            faction, ship = faction_and_ship.split(':')
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
        for faction_and_ship_name in self.ships.keys():
            faction, ship_name = faction_and_ship_name.split( ':')

            drilldown = {
                'name': ship_name,
                'categories': [],
                'data': [],
                'color': self.get_faction_color(faction)
            }

            ship_drilldowns[faction_and_ship_name] = drilldown

            ratio = 0.0
            if not self.use_points:
                ratio = self.to_float(self.to_float(self.ships[faction_and_ship_name]['cnt']) / self.to_float(self.grand_count))
            else:
                ratio = self.to_float(self.to_float(self.ships[faction_and_ship_name]['cost']) / self.to_float(self.grand_sum))

            ret.append({'y': ratio,
                        'faction': faction,
                        'color': self.get_faction_color(faction),
                        'drilldown': drilldown
            })
        for pilot in self.pilots.keys():
            val = self.pilots[pilot]
            ship = val['ship']
            faction = val['faction']
            drilldown = ship_drilldowns[faction+":"+ship]
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
                if self.grand_count == 0:
                    self.grand_count = cnt
                self.grand_sum   += cost
            elif self.is_faction_total( faction, ship, has_pilot, pilot ):
                #faction total
                if not self.factions.has_key(faction.description ):
                    self.factions[faction.description] = { 'cnt' : cnt, 'cost': cost }
                else:
                    href = self.factions[faction.description]
                    href['cost'] += cost
            elif self.is_ship_total( faction, ship, has_pilot, pilot):
                hkey = faction.description + ":" + ship.description
                #ship total
                if not self.ships.has_key(hkey):
                    self.ships[ hkey ] = { 'faction': faction.description, 'cnt': cnt, 'cost': cost}
                else:
                    href = self.ships[hkey]
                    href['cost'] += cost
            else: #full pilot row
                if not self.pilots.has_key( pilot ):
                    self.pilots[ pilot ] = { 'faction': faction.description, 'ship' : ship.description,
                                                         'cnt' : cnt, 'cost': cost, }

                else:
                    href = self.pilots[pilot]
                    href['cost'] += cost

        if has_pilot:
            return self.create_ship_pilot_doughnut_data()
        else:
            return self.create_faction_ship_doughnut_data()

    def _rollup_upgrades(self, rollups):

        self.grand_count   = 0
        self.grand_sum     = 0
        self.factions      = {}
        self.upgrade_types = {}
        self.upgrades      = {}

        for row in rollups:
            upgrade_type = row[0]
            upgrade      = row[1]
            cnt          = row[2]
            cost         = row[3]

            if upgrade_type is None and upgrade is None: #grand total
                #grand total
                self.grand_count += cnt
                self.grand_sum   += cost
            elif upgrade_type is not None and upgrade is None:
                #upgrade_type total
                self.upgrade_types[upgrade_type.description] = { 'cnt' : cnt, 'cost': cost }
            else: #regulary record.
                self.upgrades[ upgrade ] = { 'upgrade_type': upgrade_type, 'upgrade' : upgrade,
                                                     'cnt' : cnt, 'cost': cost, }


        ret = []
        upgrade_type_drilldowns = {}
        for upgrade_type in self.upgrade_types.keys():
            drilldown = {
              'name': upgrade_type,
              'categories': [],
              'data' : [],
              'color' : Rollup.colors[1]
            }

            ut_key = upgrade_type
            upgrade_type_drilldowns[ ut_key ] = drilldown

            ratio = 0.0
            if not self.use_points:
                ratio = self.to_float( self.to_float( self.upgrade_types[ut_key]['cnt'] ) / self.to_float(self.grand_count) )
            else:
                ratio = self.to_float( self.to_float( self.upgrade_types[ut_key]['cost'] ) / self.to_float(self.grand_sum) )

            ret.append( { 'y' : ratio,
                          'name':ut_key,
                         'color' : Rollup.colors[1],
                         'drilldown' : drilldown
                        })
        for upgrade in self.upgrades.keys():
            val       = self.upgrades[upgrade]
            upgrade_type   = val['upgrade_type']
            drilldown = upgrade_type_drilldowns[upgrade_type.description]
            drilldown[ 'categories'].append( upgrade )
            ratio = 0.0
            if not self.use_points:
                ratio = self.to_float( self.to_float( val['cnt'] ) / self.to_float( self.grand_count ) )
            else:
                ratio = self.to_float( self.to_float( val['cost'] ) / self.to_float( self.grand_sum ) )
            drilldown[ 'data' ].append( ratio )

        return ret

