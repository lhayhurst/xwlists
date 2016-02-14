import collections
import operator

from persistence import Faction

COUNT_MEASURE       = 'COUNT_MEASURE'
POINT_COST_MEASURE  = 'POINT_COST_MEASURE'
FACTION_SHIP_ROLLUP = 'FACTION_SHIP_ROLLUP'

releases = {
    "2012-9" : "Wave 1",
    "2013-2" : "Wave 2",
    "2013-9" : "Wave 3",
    "2014-2" : "Wave 4",
    "2014-6" : "Wave 5",
    "2015-2" : "Wave 6",
    "2015-8" : "Wave 7",
    "2015-11": "Wave 8 (T-70, Tie/FO)",
    "2014-3" : "Imperial Aces",
    "2014-9" : "Rebel Aces",
    "2014-4" : "Rebel Transport",
    "2014-5" : "Tantive IV",
    "2015-6" : "Imperial Raider",
    "2015-12" : "Imperial Assault Carrier",
}

class HighChartGraph:
    def __init__(self):
        self.options = {}
        self.categories_lookup = {}
        self.category_index = 0

    def get_options(self):
        return self.options

    def num_categories(self):
        return len(self.categories_lookup.keys())

    def add_series(self, series):
        self.options['series'].append(series)

    def finalize(self):
        #backfill any missing data
        num_categories = self.num_categories()
        for series in self.options['series']:
            data    = series['data']
            if len(data) < num_categories:
                fill_count = num_categories - len(data)
                while fill_count > 0:
                    data.insert(0, 0)
                    fill_count -= 1


    def add_plot_line(self,year_mo, position):
        text = releases[year_mo]
        xAxis = self.options['xAxis']
        if releases.has_key(year_mo):
            xAxis['plotLines'].append(
                {
                    'color' : 'red',
                    'value' : position,
                    'width' : 2,
                    'label' : {
                        'text': text,
                        'verticalAlign': 'left',
                        'textAlign': 'top'
                    }
                }
            )

    def add_category(self, year_mo):
        if not self.categories_lookup.has_key(year_mo):
            self.categories_lookup[year_mo] = self.category_index
            self.category_index += 1
            xAxis = self.options['xAxis']
            xAxis['categories'].append( year_mo )
            if releases.has_key(year_mo):
                self.add_plot_line(year_mo, len(xAxis['categories'])-1)
        return self.categories_lookup[year_mo]

class HighChartAreaGraphOptions(HighChartGraph):

    def __init__(self, title, yaxis_label, subtitle='', chart_type=None, plot_options=None ):
        HighChartGraph.__init__(self)
        self.options = {
        'chart': {
            'type': 'area'
        },
        'title': {
            'text': title,
        },
        'subtitle': {
            'text': subtitle
        },
        'xAxis': {
            'categories': [],
            'tickmarkPlacement': 'on',
            'title': {
                'enabled': 'false'
            },
            'plotLines' : [],
        },
        'yAxis': {
            'title': {
                'text': yaxis_label
            }
        },
        'tooltip': {
            'pointFormat': '<span style="color:{series.color}">{series.name}</span>: <b>{point.percentage:.1f}%</b> ({point.y:,.0f})<br/>',
            'shared': 'true'
        },
        'plotOptions': {
            'area': {
                'stacking': 'percent',
                'lineColor': '#ffffff',
                'lineWidth': 1,
                'marker': {
                    'lineWidth': 1,
                    'lineColor': '#ffffff'
                }
            }
        },
        'series': []
    }



class HighChartLineGraphOptions(HighChartGraph):
    def __init__(self, title, yaxis_label, subtitle='', chart_type=None, is_area=False):
        HighChartGraph.__init__(self)
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
                'title' : { 'enabled': "false" },
                'plotLines' : [],
            },
            'series': [],
            'plotOptions' : {}

        }

        if chart_type is not None:
            self.options['chart'] = chart_type

        if is_area:
            plotOptions = self.options['plotOptions']
            plotOptions = {
                 'area': {
                        'fillColor': {
                            'linearGradient': {
                                'x1': 0,
                                'y1': 0,
                                'x2': 0,
                                'y2': 1
                            },
                            'stops': [
                                [0, "#7cb5ec"],
                                [1, "#7cb6ef"]
                            ],
                        },
                        'marker': {
                            'radius': 2
                        },
                        'lineWidth': 1,
                        'states': {
                            'hover': {
                                'lineWidth': 1
                            }
                        },
                        'threshold': ""
                    }
                }

class ShipTotalHighchartOptions:

    def __init__(self, ship_pilot_time_series_data,show_as_count=False):
        hclgo = None
        self.show_as_count = show_as_count
        yaxis_label = "Number of ships taken"
        if show_as_count == False:
            yaxis_label = "Points spent on ships"
        hclgo = HighChartLineGraphOptions(title="Total",
                                          yaxis_label=yaxis_label,
                                          is_area=True)

        self.options = hclgo.get_options()
        self.hclgo = hclgo
        self.finalize(ship_pilot_time_series_data)

    def finalize(self,ship_pilot_time_series_data):
        data = ship_pilot_time_series_data.grand_total_data
        series = { 'name': 'Total', 'type': 'area', 'data': []}
        for year_mo in data.keys():
            self.hclgo.add_category(year_mo)
            series['data'].append( data[year_mo] )
        self.hclgo.add_series(series)
        self.hclgo.finalize()



class FactionTotalHighChartOptions:
    def __init__(self, ship_pilot_time_series_data,show_as_percentage=True,show_as_count=False):
        self.show_as_count=show_as_count
        hclgo = None

        yaxis_label = "Number of ships taken"
        if show_as_count == False:
            yaxis_label = "Points spent on ships"
        if not show_as_percentage:
            hclgo = HighChartLineGraphOptions(title="Faction Total",
                                              yaxis_label=yaxis_label )
        else:
            hclgo = HighChartAreaGraphOptions(title="Faction Percentage", yaxis_label=yaxis_label)
        self.options = hclgo.get_options()
        self.hclgo = hclgo
        self.finalize(ship_pilot_time_series_data)

    def finalize(self,ship_pilot_time_series_data):
        data = ship_pilot_time_series_data.faction_data
        for faction in data.keys():
            series = { 'name': faction, 'data': []}
            for year_mo in data[faction].keys():
                self.hclgo.add_category(year_mo)
                series['data'].append( data[faction][year_mo])
            self.hclgo.add_series(series)
        self.hclgo.finalize()

class ShipHighchartOptions:
    def __init__(self, ship_pilot_time_series_data,
                 ships_and_factions,
                 show_as_count=False,
                 show_as_percentage=True,
                 rebel_checked=True,
                 scum_checked=True,
                 imperial_checked=True):

        hclgo = None

        yaxis_label = "Number of ships taken"
        if show_as_count == False:
            yaxis_label = "Points spent on ships"

        if not show_as_percentage:
            hclgo = HighChartLineGraphOptions(title="Ship-by-Ship Total",
                                              yaxis_label=yaxis_label)
        else:
            hclgo = HighChartAreaGraphOptions(title="Ship-by-Ship Total", yaxis_label=yaxis_label)
        self.options = hclgo.get_options()
        self.hlcgo = hclgo
        self.finalize(ship_pilot_time_series_data,ships_and_factions,imperial_checked,rebel_checked,scum_checked)

    def finalize(self, ship_pilot_time_series_data,ships_and_factions,imperial_checked, rebel_checked, scum_checked ):
        ships_factions = {}
        for rec in ships_and_factions:
            faction = rec[0]
            sname   = rec[1].description
            if not ships_factions.has_key(sname):
                ships_factions[sname] = []
            ships_factions[sname].append(faction)

        data = ship_pilot_time_series_data.ship_data
        all_series = {}
        for faction in data.keys():
            for ship in data[faction].keys():
                disambiguated_ship_name = None
                if len(ships_factions[ship]) > 1:
                    disambiguated_ship_name = self.disambiguate_ship_by_faction(faction,ship)
                else:
                    disambiguated_ship_name = ship
                series = { 'name': disambiguated_ship_name,
                           'data': [],
                            'visible': self.check_visible(faction, imperial_checked, rebel_checked, scum_checked) }
                for year_mo in data[faction][ship].keys():
                    self.hlcgo.add_category(year_mo)
                    val = data[faction][ship][year_mo]
                    series['data'].append(val)
                all_series[disambiguated_ship_name] = series

        # #sort the series from biggest to smallest based the last months value
        unsorted = {}
        for ship in all_series.keys():
            ship_series = all_series[ship]
            last_value = ship_series['data'][-1]
            unsorted[ship]=last_value

        sorted_ships = sorted(unsorted.items(), key=operator.itemgetter(1))
        for ship_last_val in reversed(sorted_ships):
            ship = ship_last_val[0]
            self.hlcgo.add_series( all_series[ship])

        self.hlcgo.finalize()


    def disambiguate_ship_by_faction(self, faction, sname):
        return sname + "( " + faction + " )"

    def check_visible(self, faction, imperial_checked, rebel_checked, scum_checked):
        if rebel_checked == False and faction == Faction.REBEL.description:
            return 0
        if imperial_checked == False and faction == Faction.IMPERIAL.description:
            return 0
        if scum_checked == False and faction == Faction.SCUM.description:
            return 0
        return 1


class ShipPilotTimeSeriesData:
    def __init__(self, pm,tourney_filters=None,show_as_count=False,show_the_cut_only=False):
        self.pm               = pm
        self.grand_total_data = collections.OrderedDict()
        self.faction_data     = collections.OrderedDict()
        self.ship_data        = collections.OrderedDict()

        self.show_as_count     = show_as_count
        self.show_the_cut_only = show_the_cut_only

        self.ship_pilot_time_series_data = pm.get_ship_pilot_rollup(tourney_filters,show_the_cut_only)
        self.upgrade_time_series_data = pm.get_upgrade_rollups( tourney_filters,show_the_cut_only )
        self.visit_time_series_data( self.ship_pilot_time_series_data)
        self.visit_time_series_data(self.upgrade_time_series_data)


    def is_grand_total(self, faction, ship, pilot):
        return faction is None and ship is None and pilot is None

    def is_faction_total(self, faction, ship, pilot):
        return faction is not None and ship is None and pilot is None

    def is_ship_total(self, faction, ship, pilot):
       return faction is not None and ship is not None and pilot is None

    def visit_grand_total(self, year, month, cnt, cost):
        year_mo = str(year) + "-" + str(month)
        datapoint = 0
        if self.show_as_count:
            datapoint = cnt
        else:
            datapoint = cost

        if not self.grand_total_data.has_key( year_mo):
            self.grand_total_data[year_mo] = None

        if self.grand_total_data[year_mo] is None:
            self.grand_total_data[year_mo] = datapoint

        else:
            self.grand_total_data[year_mo] += datapoint

    def visit_ship_total(self, year, month, faction, ship, cnt,cost):
        year_mo = str(year) + "-" + str(month)
        datapoint = 0
        if self.show_as_count:
            datapoint = cnt
        else:
            datapoint = cost

        if not self.ship_data.has_key(faction):
            self.ship_data[faction] = collections.OrderedDict()

        if not self.ship_data[faction].has_key(ship):
            self.ship_data[faction][ship] = collections.OrderedDict()

        if not self.ship_data[faction][ship].has_key(year_mo):
            self.ship_data[faction][ship][year_mo] = 0

        self.ship_data[faction][ship][year_mo] += datapoint

    def visit_pilot_total(self, year, month, faction,ship,pilot,cnt,cost):
        pass

    def visit_faction_total(self, year, month, faction,cnt, cost):
        year_mo = str(year) + "-" + str(month)
        datapoint = 0
        if self.show_as_count:
            datapoint = cnt
        else:
            datapoint = cost

        if not self.faction_data.has_key(faction):
            self.faction_data[faction] = collections.OrderedDict()

        data_by_faction = self.faction_data[faction]

        if not data_by_faction.has_key( year_mo):
            data_by_faction[year_mo] = None

        if data_by_faction[year_mo] is None:
            data_by_faction[year_mo] = datapoint

        else:
            data_by_faction[year_mo] += datapoint

    def visit_time_series_data(self, time_series_data):
        for row in time_series_data:
            year    = row[0]
            month   = row[1]
            faction = row[2]
            ship    = row[3]
            pilot   = row[4]
            cnt     = int(row[5])
            cost    = int(row[6])

            if faction is not None:
                faction = faction.description

            if ship is not None:
                ship = ship.description

            if year is not None and month is not None: #the rollup actually rolls up year and month!
                if self.is_grand_total( faction, ship, pilot):
                    self.visit_grand_total(year, month, cnt, cost)
                elif self.is_faction_total( faction, ship, pilot ):
                    self.visit_faction_total(year, month,faction,cnt, cost)
                elif self.is_ship_total( faction, ship, pilot):
                    self.visit_ship_total( year, month,faction, ship, cnt,cost)
                else: #full pilot row
                    self.visit_pilot_total(year, month,faction,ship,pilot,cnt,cost)


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

