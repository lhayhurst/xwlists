from flask import url_for
from markupsafe import Markup
from sqlalchemy.dialects import mysql
from sqlalchemy import or_, BigInteger
from decoder import decode

REGIONAL = 'Regional'
STORE_CHAMPIONSHIP = 'Store championship'
NATIONAL_CHAMPIONSHIP = 'Nationals'

ELIMINATION = 'elimination'

SWISS = 'swiss'

__author__ = 'lhayhurst'

import random

from sqlalchemy.orm import relationship
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ColumnElement, ClauseElement, literal
from sqlalchemy.sql.elements import _clause_element_as_expr

from myapp import db_connector
from xwingmetadata import XWingMetaData
import xwingmetadata

from decl_enum import DeclEnum
from sqlalchemy import Column, Integer, String, func, Date, and_, desc, Boolean, DateTime
from sqlalchemy import ForeignKey

#rollup help
#see https://groups.google.com/forum/#!msg/sqlalchemy/Pj5T8hO_ibQ/LrmBcIBxnNwJ
class rollup(ColumnElement):
    def __init__(self, *elements):
        self.elements = [_clause_element_as_expr(e) for e in elements]

@compiles(rollup, "mysql")
def _mysql_rollup(element, compiler, **kw):
    return "%s WITH ROLLUP" % (', '.join([compiler.process(e, **kw) for e in element.elements]))

class Match(ClauseElement):
    def __init__(self, columns, value):
        self.columns = columns
        self.value = literal(value)

@compiles(Match)
def _match(element, compiler, **kw):
    return "MATCH (%s) AGAINST (%s IN BOOLEAN MODE)" % (
               ", ".join(compiler.process(c, **kw) for c in element.columns),
               compiler.process(element.value)
             )



#TABLES

tourney_table = "tourney"
list_table = "list"
ship_table = "ship"
pilot_table = "pilot"
ship_pilot_table = "ship_pilot"
ship_type_table = "ship_type"
upgrade_table   = "upgrade"
ship_upgrade_table = "ship_upgrade"
ship_pilot_upgrade_table = "ship_pilot_upgrade_table"
tourney_list_table = "tourney_list"
tlist_table = 'tlist'
tourney_round = "tourney_round"
tourney_result = "tourney_result"
event_table = "event"
archtype_list_table = "list_archtype"
tag_table = "tag"
tag_to_archtype_table = "archtype_tag"

Base = db_connector.get_base()


class RoundType(DeclEnum):
    ELIMINATION     = "Elimination", "Elimination"
    PRE_ELIMINATION = 'Pre-Elimination', 'Pre-Elimination'

#factions changed in 0.3.0 of the xws spec.
class Faction(DeclEnum):
    IMPERIAL = "imperial", "Galactic Empire"
    REBEL    = "rebel", "Rebel Alliance"
    SCUM     = "scum", "Scum and Villainy"

class UpgradeType(DeclEnum):
    TITLE = xwingmetadata.TITLE_CANON, xwingmetadata.TITLE
    DROID = xwingmetadata.DROID_CANON, xwingmetadata.DROID
    CREW  = xwingmetadata.CREW_CANON, xwingmetadata.CREW
    EPT   = xwingmetadata.EPT_CANON, xwingmetadata.EPT
    MOD    = xwingmetadata.MOD_CANON, xwingmetadata.MOD
    SYSTEM = xwingmetadata.SYSTEM_CANON, xwingmetadata.SYSTEM
    BOMB_MINES = xwingmetadata.BOMB_CANON, xwingmetadata.BOMB
    CANNON = xwingmetadata.CANNON_CANON, xwingmetadata.CANNON
    TURRET = xwingmetadata.TURRET_CANON, xwingmetadata.TURRET
    TORPEDO = xwingmetadata.TORPEDO_CANON, xwingmetadata.TORPEDO
    MISSILE = xwingmetadata.MISSILE_CANON, xwingmetadata.MISSILE
    SALVAGED_ASTROMECH_DROID = xwingmetadata.SALVAGED_ASTROMECH_DROID_CANON, xwingmetadata.SALVAGED_ASTROMECH_DROID
    ILLICIT = xwingmetadata.ILLICIT_CANON, xwingmetadata.ILLICIT
    TECH = xwingmetadata.TECH_CANON, xwingmetadata.TECH

class ShipType(DeclEnum):
    XWING =  xwingmetadata.X_WING_CANON, xwingmetadata.X_WING
    YWING =  xwingmetadata.Y_WING_CANON,  xwingmetadata.Y_WING
    AWING =  xwingmetadata.A_WING_CANON, xwingmetadata.A_WING
    BWING = xwingmetadata.B_WING_CANON, xwingmetadata.B_WING
    EWING  = xwingmetadata.E_WING_CANON, xwingmetadata.E_WING
    YT1300 = xwingmetadata.YT_1300_CANON, xwingmetadata.YT_1300
    YT2400 = xwingmetadata.YT_2400_CANON, xwingmetadata.YT_2400
    HWK290 = xwingmetadata.HWK_290_CANON, xwingmetadata.HWK_290
    Z95    = xwingmetadata.Z95_HEADHUNTER_CANON, xwingmetadata.Z95_HEADHUNTER
    TIEFIGHTER = xwingmetadata.TIE_FIGHTER_CANON, xwingmetadata.TIE_FIGHTER
    TIEADVANCED = xwingmetadata.TIE_ADVANCED_CANON, xwingmetadata.TIE_ADVANCED
    TIEINTERCEPTOR = xwingmetadata.TIE_INTERCEPTOR_CANON, xwingmetadata.TIE_INTERCEPTOR
    FIRESPRAY = xwingmetadata.FIRESPRAY_31_CANON, xwingmetadata.FIRESPRAY_31
    LAMDA = xwingmetadata.LAMBDA_SHUTTLE_CANON, xwingmetadata.LAMBDA_SHUTTLE
    TIEBOMBER = xwingmetadata.TIE_BOMBER_CANON, xwingmetadata.TIE_BOMBER
    TIEDEFENDER = xwingmetadata.TIE_DEFENDER_CANON, xwingmetadata.TIE_DEFENDER
    TIEPHANTOM = xwingmetadata.TIE_PHANTOM_CANON, xwingmetadata.TIE_PHANTOM
    DECIMATOR = xwingmetadata.VT_DECIMATOR_CANON, xwingmetadata.VT_DECIMATOR
    STARVIPER = xwingmetadata.STAR_VIPER_CANON, xwingmetadata.STAR_VIPER
    AGGRESSOR = xwingmetadata.AGGRESSOR_CANON, xwingmetadata.AGGRESSOR
    M3_A_INTERCEPTOR = xwingmetadata.M3_A_INTERCEPTOR_CANON, xwingmetadata.M3_A_INTERCEPTOR
    YV_666 = xwingmetadata.YV_666_FREIGHTER_CANON_NAME, xwingmetadata.YV_666_FREIGHTER
    TIE_PUNISHER = xwingmetadata.TIE_PUNISHER_CANON_NAME, xwingmetadata.TIE_PUNISHER
    KWING = xwingmetadata.K_WING_CANON_NAME, xwingmetadata.K_WING
    KIHRAXZ_FIGHTER = xwingmetadata.KIHRAXZ_FIGHTER_CANON_NAME, xwingmetadata.KIHRAXZ_FIGHTER
    T_70 = xwingmetadata.T_70_CANON_NAME, xwingmetadata.T_70
    TIE_FO_FIGHTER = xwingmetadata.TIE_FO_FIGHTER_CANON_NAME, xwingmetadata.TIE_FO_FIGHTER
    
class Event(Base):
    __tablename__ = event_table
    id = Column( Integer, primary_key=True)
    remote_address = Column( String(32))
    event_date = Column( DateTime )
    event = Column( String(32))
    event_details = Column( String(256))

    def get_event_details(self):
        if self.event_details is None or len(self.event_details) == 0:
            return ""
        else:
            return decode( self.event_details )

class Pilot(Base):
    __tablename__ = pilot_table
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    canon_name = Column(String(128), unique=True)
    cost = Column(Integer)
    pilot_skill = Column(Integer)

class ShipPilot(Base):
    __tablename__ = ship_pilot_table
    id            = Column(Integer, primary_key=True)
    ship_type     = Column(ShipType.db_type())
    pilot_id      = Column(Integer, ForeignKey('{0}.id'.format(pilot_table)))
    pilot = relationship(Pilot.__name__, uselist=False)

class Upgrade(Base):
    __tablename__ = upgrade_table
    id = Column(Integer, primary_key=True)
    upgrade_type = Column(UpgradeType.db_type(), unique=True)
    name = Column(String( 128 ), unique=True)
    canon_name = Column(String( 128 ), unique=True)
    cost = Column(Integer, unique=True)



class Ship(Base):
    __tablename__ = ship_table
    id = Column(Integer, primary_key=True)
    ship_pilot_id = Column(Integer, ForeignKey('{0}.id'.format(ship_pilot_table)))
    archtype_id = Column( Integer, ForeignKey('{0}.id'.format(archtype_list_table)))
    #tlist_id = Column(Integer, ForeignKey('{0}.id'.format(tourney_list_table)))  #parent
    ship_pilot = relationship(ShipPilot.__name__, uselist=False)
    upgrades = relationship( "ShipUpgrade", back_populates="ship")
    #tlist    = relationship("TourneyList", uselist=False)
    archtype = relationship("ArchtypeList", uselist=False)


    def get_upgrade(self, upgrade_name ):

        ret = []

        num_upgrades = 1

        if "." in upgrade_name:
            a = upgrade_name.split('.')
            upgrade_name = a[0]
            num_upgrades = int(a[1])

        for ship_upgrade in self.upgrades:
            upgrade = ship_upgrade.upgrade
            if upgrade is not None:
                if upgrade.upgrade_type.description == upgrade_name:
                    ret.append( upgrade.name)

        if num_upgrades > len(ret):
            return ""
        elif len(ret) == 0:
            return ""
        return ret[ num_upgrades - 1  ]

class ShipUpgrade(Base):
    __tablename__ = ship_upgrade_table
    id = Column(Integer, primary_key=True)
    ship_id = Column(Integer, ForeignKey('{0}.id'.format(ship_table))) #todo: change to ship id
    upgrade_id = Column(Integer, ForeignKey('{0}.id'.format(upgrade_table) ) )
    upgrade = relationship( Upgrade.__name__, uselist=False)
    ship    = relationship( Ship.__name__, back_populates="upgrades")



class Tourney(Base):
    __tablename__ = tourney_table
    id = Column(Integer, primary_key=True)
    tourney_name      = Column(String(128))
    tourney_date      = Column(Date)
    tourney_type      = Column(String(128))
    round_length      = Column(Integer)
    email             = Column(String(128))
    entry_date        = Column(Date)
    participant_count = Column(Integer)
    locked            = Column(Boolean)
    api_token         = Column(String(128))
    format            = Column(String(128))

    tourney_lists   = relationship( "TourneyList", back_populates="tourney", cascade="all,delete,delete-orphan" )
    rounds          = relationship( "TourneyRound", back_populates="tourney", order_by="asc(TourneyRound.round_num)", cascade="all,delete,delete-orphan")
    rankings        = relationship( "TourneyRanking", back_populates="tourney", order_by="asc(TourneyRanking.rank)", cascade="all,delete,delete-orphan")
    tourney_players = relationship( "TourneyPlayer", back_populates="tourney", cascade="all,delete,delete-orphan")
    sets            = relationship( "TourneySet", back_populates="tourney", cascade="all,delete,delete-orphan")
    venue           = relationship( "TourneyVenue", back_populates="tourney", cascade="all,delete,delete-orphan", uselist=False)

    def is_standard_format(self):
        return self.format == 'Standard - 100 Point Dogfight'

    def get_tourney_name_as_url(self):

        ret = '<a href="' + url_for('get_tourney_details', tourney_id=self.id, ) +  '">' + self.get_tourney_name() + "</a>"
        return Markup(ret)

    def reset_rounds(self, session ):
        goners = []
        for round in self.rounds:
            session.delete(round)
            goners.append(round)
        for goner in goners:
            self.rounds.remove(goner)
        session.commit()


    def get_round(self, round_type, round_num):
        for round in self.rounds:
            if round.round_type == round_type and round.round_num == round_num:
                return round
        return None

    def get_player_by_name(self, player_name):
        for player in self.tourney_players:
            if player.player_name == player_name:
                return player
        return None

    def get_player_by_id(self, player_id):
        for player in self.tourney_players:
            if player.id == player_id:
                return player
        return None

    def total_list_count(self):
        return self.participant_count

    def num_entered_lists(self):
        count = 0
        for list in self.tourney_lists:
            if list.points() > 0:
                count = count + 1
        return count

    def get_tourney_name(self):
        return decode(self.tourney_name)

    def is_store_championship(self):
        return self.tourney_type == 'Store championship'

    def had_championship_cut(self):
        for r in self.rankings:
            if r.elim_rank is not None:
                return True
        return False

    def all_lists_entered(self):
        for tl in self.tourney_lists:
            if len(tl.ships) == 0:
                return False
        return True

    def get_pre_elimination_rounds(self):
        ret = [r for r in self.rounds if r.round_type == RoundType.PRE_ELIMINATION]
        return ret

    def get_elim_rounds(self):
        ret =  [r for r in self.rounds if r.round_type == RoundType.ELIMINATION]
        return ret


    def get_descending_elim_rounds(self):
        ret =  [r for r in self.rounds if r.round_type == RoundType.ELIMINATION]
        return ret

    def headline(self):
        return "{0}".format(self.id)

    def venue_string(self):
        ret = ""
        if self.venue is not None:
            if self.venue.venue is not None:
                ret = self.venue.venue
            if self.venue.city is not None:
                ret = ret + "/" + self.venue.city
            if self.venue.state is not None:
                ret = ret + "/" + self.venue.state
            if self.venue.country is not None:
                ret = ret + "/" + self.venue.country
        else:
            ret = "Unknown"
        return decode(ret)

tourney_player_table = "tourney_player"
class TourneyPlayer(Base):
    __tablename__    = tourney_player_table
    id               = Column( Integer, primary_key=True)
    tourney_id       = Column(Integer, ForeignKey('{0}.id'.format(tourney_table)))
    player_name      = Column(String(128))
    tourney          = relationship( Tourney.__name__, back_populates="tourney_players")
    tourney_lists    = relationship( "TourneyList", back_populates='player')
    result           = relationship("TourneyRanking", back_populates='player', uselist=False )

    def get_first_tourney_list(self):
        if self.tourney_lists:
            return self.tourney_lists[0]
        return None

    def get_player_name(self):
        return decode(self.player_name)




class ArchtypeList(Base):
     __tablename__    = archtype_list_table
     id               = Column( Integer, primary_key=True)
     name             = Column(String(128))
     faction          = Column(Faction.db_type())
     points           = Column(Integer)
     pretty           = Column(String(1024))
     hashkey          = Column(BigInteger)
     ships            = relationship(Ship.__name__,uselist=True)
     tourney_lists    = relationship("TourneyList", uselist=True)
     tags             = relationship("ArchtypeTag", uselist=True)

     def pretty_print_list(self):

        ret = ""
        for ship in self.ships:
            ret = ret + ship.ship_pilot.pilot.name
            i = 1
            if ship.upgrades is not None:
                for ship_upgrade in ship.upgrades:
                    if ship_upgrade.upgrade is not None:
                        ret = ret + " + " + ship_upgrade.upgrade.name
            if i < len(self.ships):
                ret = ret + '<br>'
            i = i + 1
        points = 0
        if self.points is not None:
            points = self.points
        ret = ret + "(%d)" % ( points )
        return ret

     def num_lists(self):
         return len(self.tourney_lists)

     def get_performance_stats(self, pm, url_root):
         summary = []
         wins = 0
         losses = 0
         draws = 0
         total = 0
         points_killed = 0
         points_lost = 0
         points_killable = 0
         points_losable = 0
         pretty_print = None

         for list in self.tourney_lists:
             if not list.tourney.is_standard_format():
                 continue
             if list.points() is None or list.points() == 0:
                 continue
             list_id = list.id
             results = pm.get_round_results_for_list(list_id)
             for result in results:
                 total = total + 1
                 if result.draw:
                     draws = draws + 1
                 elif result.winner_id == list_id:
                     wins = wins + 1
                 elif result.loser_id == list.id:
                     losses = losses + 1

                 if result.list1_id == list_id:
                     points_killed = points_killed + result.get_list1_score()
                     pk = result.get_list2_points()
                     if pk == 0:
                         pk = 100  # assume default -- missing the other list

                     points_killable = points_killable + pk
                     points_lost = points_lost + result.get_list2_score()

                 elif result.list2_id == list_id:
                     points_killed = points_killed + result.get_list2_score()

                     pk = result.get_list1_points()
                     if pk == 0:
                         pk = 100  # assume default -- missing the other list
                     points_killable = points_killable + pk
                     points_lost = points_lost + result.get_list1_score()

                 points_losable = points_losable + list.points()

         if total == 0:
             return {}

         perc = 0
         points_for_eff = 0
         points_against_eff = 0

         if total > 0:
             perc = float(wins) / float(total)

         if points_killable > 0:
             points_for_eff = float(points_killed) / (points_killable)

         if points_losable > 0:
             points_against_eff = float(points_losable - points_lost) / float(points_losable)
             if points_against_eff < 0:
                 points_against_eff = 0

         return {'pretty_print' : self.pretty_print(manage_list=0, manage_archtype=0, url_root=url_root),
                 'total' :"{:,}".format(total),
                 'wins': "{:,}".format(wins),
                 'losses': "{:,}".format(losses),
                 'draws': "{:,}".format(draws),
                 'total': "{:,}".format(total),
                 'perc': "{:.2%}".format(perc),
                 'points_for': "{:,}".format(points_killed) + "/" + "{:,}".format(points_killable),
                 'points_against': "{:,}".format(points_losable - points_lost) + "/" + "{:,}".format(
                     points_losable),
                 'points_for_efficiency': "{:.2%}".format(points_for_eff),
                 'point_against_efficiency': "{:.2%}".format(points_against_eff)}



     def pretty_print(self,url_root, manage_list=0,manage_archtype=1):
        return self.tourney_lists[0].pretty_print(url_root, manage_archtype=manage_archtype,manage_list=manage_list)

     @staticmethod
     def generate_hash_key(ships):
        liststring = ""
        ship_strings    = []
        pilot_strings   = []
        upgrade_strings = []
        for ship in ships:
            sp = ship.ship_pilot
            ship_strings.append( str( sp.ship_type ))
            pilot_strings.append( sp.pilot.canon_name )
            for supgrade in ship.upgrades:
                if supgrade.upgrade is not None:
                    upgrade_strings.append( supgrade.upgrade.canon_name )
        key = None
        liststring = ""
        for s in sorted(ship_strings):
            liststring = liststring + s
        for p in sorted(pilot_strings):
            liststring = liststring + p
        for u in sorted(upgrade_strings):
            liststring = liststring + u

        if len(liststring) == 0:
            key = 0
        else:
            key = hash(liststring)

        return key

     def pretty_print_tags(self):
         ret = ""
         for t in self.tags:
             ret = ret + t.tag.tagtext + ", "
         return ret

     def get_tags(self):
         ret = []
         for t in self.tags:
             ret.append(t.tag.tagtext)
         return ret

class Tag(Base):
    __tablename__ = tag_table
    id = Column(Integer, primary_key=True)
    tagtext = Column(String(128))

class ArchtypeTag(Base):
    __tablename__ = tag_to_archtype_table
    id               = Column(Integer, primary_key=True)
    archtype_id      = Column(Integer, ForeignKey('{0}.id'.format(archtype_list_table)))
    tag_id           = Column(Integer, ForeignKey('{0}.id'.format(tag_table)))
    archtype         = relationship(ArchtypeList.__name__, uselist=False, back_populates="tags")
    tag              = relationship(Tag.__name__, uselist=False)


class TourneyList(Base):
    __tablename__    = tourney_list_table
    id               = Column( Integer, primary_key=True)
    tourney_id       = Column(Integer, ForeignKey('{0}.id'.format(tourney_table)))
    archtype_id      = Column(Integer, ForeignKey('{0}.id'.format(archtype_list_table)))
    player_id        = Column(Integer, ForeignKey('{0}.id'.format(tourney_player_table)))
    image            = Column(String(128))
    #name             = Column(String(128))
    #hashkey          = Column(BigInteger)
    #faction          = Column(Faction.db_type())
    #points           = Column(Integer)
    player           = relationship( TourneyPlayer.__name__, uselist=False)
    tourney          = relationship( Tourney.__name__, back_populates="tourney_lists")
    #ships            = relationship(Ship.__name__, cascade="all,delete,delete-orphan")
    archtype_list    = relationship(ArchtypeList.__name__, back_populates="tourney_lists")

    def hashkey(self):
        if self.archtype_list is not None:
            return self.archtype_list.hashkey

    def points(self):
        if self.archtype_list is not None:
            return self.archtype_list.points
        return 0

    def faction(self):
        if self.archtype_list is not None:
            return self.archtype_list.faction
        return None

    def set_points(self, points):
        self.archtype_list.points = points

    def set_faction(self, faction):
        self.archtype_list.faction = faction

    def name(self):
        if self.archtype_list is not None:
            return self.archtype_list.name
        return None

    def ships(self):
        if self.archtype_list is not None:
            return self.archtype_list.ships
        return []

    @staticmethod
    def fast_url_for(url_root, endpoint, **values):
        url = url_root + endpoint + "?"
        kvp = ""
        lv = len(values)
        i  = 1
        for v in values:
            kvp = kvp + v + "=" + str(values[v])
            if i < lv:
                kvp = kvp + "&"
            i += 1
        return url + kvp

    def pretty_print(self, url_root, manage_list=1, show_results=0, enter_list=1, manage_archtype=0):
        if len(self.ships()) == 0: #no list
            if self.tourney.locked == False and enter_list:
                ret = '<a rel="nofollow" href="' + TourneyList.fast_url_for(url_root, 'enter_list', tourney_id=self.tourney_id, tourney_list_id=self.id) + '">Enter list</a>'
                return ret
            else:
                return ""
        ret = self.archtype_list.pretty
        urls = ""
        #url for is simply too slow :-(
        if not self.tourney.locked and manage_list:
            urls = urls + '<br><a href="' + TourneyList.fast_url_for( url_root, 'display_list', tourney_list_id=str(self.id), )
            urls = urls + '"rel="nofollow">Manage list</a>'
        if show_results:
            urls = urls + '<br><a href="' +  TourneyList.fast_url_for(url_root,'show_results', id=str(self.archtype_id ))
            urls = urls + '">Show results</a>'
        if manage_archtype:
            urls = urls + '<br><a href="' +  TourneyList.fast_url_for(url_root,'archtype', id=str(self.archtype_id ))
            urls = urls + '">Manage archtype</a>'

        return ret + urls


tourney_round_table = "tourney_round"
class TourneyRound(Base):
    __tablename__ = tourney_round_table
    id            = Column(Integer, primary_key=True)
    tourney_id    = Column(Integer, ForeignKey('{0}.id'.format(tourney_table)))
    round_num     = Column(Integer)
    round_type    = Column(RoundType.db_type())
    results       = relationship( "RoundResult", back_populates="round", cascade="all,delete,delete-orphan")
    tourney       = relationship( Tourney.__name__, back_populates="rounds")

    def round_type_str(self):
        if self.round_type == RoundType.PRE_ELIMINATION:
            return SWISS
        elif self.round_type == RoundType.ELIMINATION:
            return ELIMINATION
        return None

    def is_pre_elim(self):
        return self.round_type == RoundType.PRE_ELIMINATION

    def is_elim(self):
        return self.round_type == RoundType.ELIMINATION


    def get_win_or_draw_result(self, winner, loser, was_draw):
        for result in self.results:
            if was_draw == result.draw and result.winner.id == winner.id and result.loser.id == loser.id:
               return result
        return None

    def get_bye_result(self, winner):
        for result in self.results:
            if result.bye == True and result.winner == winner:
                return result
        return None


tourney_ranking_table = "tourney_ranking"
class TourneyRanking(Base):
    __tablename__      = tourney_ranking_table
    id                 = Column(Integer, primary_key=True)
    tourney_id         = Column(Integer, ForeignKey('{0}.id'.format(tourney_table)))
    player_id          = Column(Integer, ForeignKey('{0}.id'.format(tourney_player_table)))
    score              = Column(Integer)
    mov                = Column(Integer)
    sos                = Column(Integer)
    rank               = Column(Integer)
    elim_rank          = Column(Integer)
    dropped            = Column(Boolean)
    tourney            = relationship( Tourney.__name__, back_populates="rankings")
    player             = relationship( TourneyPlayer.__name__, uselist=False)

    def pretty_print(self, url_root, manage_list=1):
        for tourney_list in self.tourney.tourney_lists:
            if tourney_list.player.id == self.player_id:
                return tourney_list.pretty_print(url_root=url_root, manage_list=manage_list)
        return ""

    def get_player_info(self):
        if self.dropped:
            return self.player.player_name + " (dropped)"
        return self.player.player_name


round_result_table = "round_result"
class RoundResult(Base):
    __tablename__   = round_result_table

    id            = Column(Integer, primary_key=True)
    round_id      = Column(ForeignKey('{0}.id'.format(tourney_round_table)))
    list1_id      = Column(ForeignKey('{0}.id'.format(tourney_list_table)))
    list2_id      = Column(ForeignKey('{0}.id'.format(tourney_list_table)))
    winner_id     = Column(ForeignKey('{0}.id'.format(tourney_list_table)))
    loser_id      = Column(ForeignKey('{0}.id'.format(tourney_list_table)))
    bye           = Column(Boolean)
    draw          = Column(Boolean)

    list1_score   = Column(Integer)
    list2_score   = Column(Integer)
    round         = relationship( TourneyRound.__name__, back_populates="results")
    list1         = relationship( TourneyList.__name__, foreign_keys='RoundResult.list1_id',  uselist=False)
    list2         = relationship( TourneyList.__name__, foreign_keys='RoundResult.list2_id',  uselist=False)
    winner        = relationship( TourneyList.__name__, foreign_keys='RoundResult.winner_id', uselist=False)
    loser         = relationship( TourneyList.__name__, foreign_keys='RoundResult.loser_id',  uselist=False)

    def edit(self, player1_score, player2_score, result):
        self.list1_score = player1_score
        self.list2_score = player2_score
        if result == "beat":
            #player 1 beat player 2
            self.winner = self.list1
            self.loser  = self.list2
            self.draw   = False
            self.bye    = False
        elif result == "lost to":
            self.winner = self.list2
            self.loser  = self.list1
            self.draw   = False
            self.bye    = False
        elif result == "drew":
            self.draw = True
            self.bye  = False


    def versus(self, hashkey):
        if self.list1.hashkey == hashkey:
            return self.list2.pretty_print(manage_list=0, enter_list=0)
        return self.list1.pretty_print(manage_list=0, enter_list=0)

    def get_result_and_score_for_hashkey(self, hashkey):
        return self.get_result_for_hashkey(hashkey) + " " + self.get_score_for_hashkey(hashkey)

    def get_result_for_hashkey(self,hashkey):
        list_id = None
        if self.list1.hashkey == hashkey:
            list_id = self.list1.id
        else:
            list_id = self.list2.id

        if self.draw is not None and self.draw==True:
            return "drew"

        if self.winner_id == list_id:
            return "won"
        return "lost"

    def get_score_for_hashkey(self, hashkey):
        if self.list1.hashkey == hashkey:
            return "%d-%d" % ( self.list1_score, self.list2_score)
        return "%d-%d" % ( self.list2_score, self.list1_score)


    def get_result(self):
        if self.bye is not None and self.bye==True:
            return "had a bye"
        if self.draw is not None and self.draw==True:
            return "drew"
        if self.winner.id == self.list1.id:
            return "beat"
        return "lost to"

    def get_result_for_json(self):
        if self.bye is not None and self.bye==True:
            return "bye"
        if self.draw is not None and self.draw==True:
            return "draw"
        return "win"

    def player1_name(self):
        return decode(self.list1.player.player_name)

    def player2_name(self):
        if self.list2 is None:
            return ""
        return decode(self.list2.player.player_name)

    def list2_pretty_print(self, manage_lists=1):
        if self.list2 is None:
            return ""
        return self.list2.pretty_print(manage_lists)

    def winning_score(self):
        if self.winner.id == self.list1.id:
            return self.list1_score
        return self.list2_score

    def losing_score(self):
        if self.loser.id == self.list1.id:
            return self.list1_score
        return self.list2_score

    def get_list1_score(self):
        if self.list1_score is None:
            return 0
        return self.list1_score

    def get_list2_score(self):
        if self.list2_score is None:
            return 0
        return self.list2_score

    def get_list1_points(self):
        if self.list1.points() is None:
            return 100
        return self.list1.points()

    def get_list2_points(self):
        if self.list2.points() is None:
            return 100
        return self.list2.points()

    def get_winner_list_url(self):
        url = url_for( 'display_list', tourney_list_id=self.winner.id )
        return url

    def get_loser_list_url(self):
        url = url_for( 'display_list', tourney_list_id=self.loser.id )
        return url

set_table_name = "xwing_set"
class Set(Base):
    __tablename__   = set_table_name
    id              = Column(Integer, primary_key=True)
    set_name        = Column(String(128))

tourney_set_table_name = "tourney_set"
class TourneySet(Base):
    __tablename__      = tourney_set_table_name
    id                 = Column(Integer, primary_key=True)
    tourney_id         = Column(Integer, ForeignKey('{0}.id'.format(tourney_table)))
    set_id             = Column(Integer, ForeignKey('{0}.id'.format(set_table_name)))
    tourney            = relationship( Tourney.__name__, back_populates="sets")
    set                = relationship( Set.__name__,  uselist=False)

tourney_venue_table_name = 'tourney_venue'
class TourneyVenue(Base):
    __tablename__      = tourney_venue_table_name
    id                 = Column(Integer, primary_key=True)
    tourney_id         = Column(Integer, ForeignKey('{0}.id'.format(tourney_table)))
    country            = Column(String(128))
    state              = Column(String(128))
    city               = Column(String(128))
    venue              = Column(String(128))
    tourney            = relationship( Tourney.__name__, back_populates="venue", uselist=False)

class PersistenceManager:

    db_connector = None

    def __init__(self, db_connector):
        self.db_connector = db_connector

    def create_schema(self):
        self.db_connector.get_base().metadata.create_all(self.db_connector.get_engine())


    def drop_schema(self):
        self.db_connector.get_base().metadata.drop_all(self.db_connector.get_engine())


    def populate_reference_tables(self):
        #return True
        session = self.db_connector.get_session()

        pilots = {}
        ship_pilots = []

        m = XWingMetaData()
        all_ships = m.ships_full()
        for ship in all_ships:
            for pilot in all_ships[ship]:
                p = Pilot(name=pilot['name'], cost=pilot['cost'])
                pilots[ pilot['name'] ] = p
        session.add_all( pilots.values() )
        session.commit()

        for ship in all_ships:
            for pilot in all_ships[ship]:
                p =  pilots[pilot['name']]
                sp = ShipPilot( ship_type=ShipType.from_string(ship), pilot=p, pilot_id=p.id)
                ship_pilots.append(sp)
        session.add_all( ship_pilots )
        session.commit()

    def get_summaries(self):

        session           = self.db_connector.get_session()
        num_tourneys      = session.query(func.count(Tourney.id)).first()[0]
        num_lists         = session.query(func.count(TourneyList.id)).\
            filter(and_( ArchtypeList.id == TourneyList.archtype_id, ArchtypeList.points >0 ) ).first()[0]

        archtypes         = self.get_all_archtypes()
        num_total_ships = 0
        num_total_upgrades = 0
        total_points_spent = 0

        # for a in archtypes:
        #     num_archtype_ships    = 0
        #     num_archtype_lists    = 0
        #     num_archtype_upgrades = 0
        #     if a.ships is not None:
        #         num_archtype_ships = len(a.ships)
        #         for ship in a.ships:
        #             if len(ship.upgrades) > 0:
        #                 num_archtype_upgrades = num_archtype_upgrades + len(ship.upgrades)
        #
        #     if a.tourney_lists is not None:
        #         num_archtype_lists = len(a.tourney_lists)
        #         total_points_spent = total_points_spent + num_archtype_lists * a.points
        #         num_total_upgrades = num_total_upgrades + num_archtype_lists * num_archtype_upgrades
        #
        #     if num_archtype_ships > 0 and num_archtype_lists > 0:
        #         num_total_ships = num_total_ships + num_archtype_ships*num_archtype_lists

        return { "tourneys": num_tourneys,
                 "lists": num_lists,
                 "ships": num_total_ships,
                 "upgrades": num_total_upgrades,
                 "points_spent" :  total_points_spent }


    def add_tag(self, archtype, tag_text):
         tag = Tag(tagtext=tag_text)
         self.db_connector.get_session().add( tag )
         archtype_tag = ArchtypeTag( archtype=archtype, tag=tag)
         self.db_connector.get_session().add(archtype_tag)
         self.db_connector.get_session().commit()

    def remove_tag(self, archtype, tag_text):
        for at in archtype.tags:
            if at.tag.tagtext == tag_text:
                archtype.tags.remove( at )
                self.db_connector.get_session().commit()
                break

    def get_all_tags(self):
        all_tags = self.db_connector.get_session().query(Tag).all()
        ret = {}
        for t in all_tags:
            ret[ t.tagtext ] = 1
        return ret.keys()
    def get_tourney_ids(self):
        return self.db_connector.get_session().query(Tourney.id).all()

    def get_events(self):
        return self.db_connector.get_session().query(Event).order_by( Event.id)

    def get_all_lists(self):
        return self.db_connector.get_session().query(TourneyList).all()

    def get_tourneys(self):
        return self.db_connector.get_session().query(Tourney)

    def get_upgrades(self):
        return self.db_connector.get_session().query(Upgrade).all()

    def get_ship_upgrades(self):
        return self.db_connector.get_session().query(ShipUpgrade).all()

    def get_round_results_for_list(self, list_id):
        ret = self.db_connector.get_session().query(RoundResult).filter(
            or_(
                RoundResult.winner_id == list_id,
                RoundResult.loser_id  == list_id)
        )
        return ret.all()


    def get_faction_rollup(self):
        session  =  self.db_connector.get_session()
        subq =  session.query( func.count(TourneyList.faction ).label('total_factions') ).\
             filter(TourneyList.tourney_id == Tourney.id).subquery()

        ret = session.query(
             TourneyList.faction, func.count(TourneyList.faction).label("num_of"), subq.c.total_factions.label("total_of"),
                                  func.count(TourneyList.faction).label("percentage_of") / subq.c.total_factions ).\
             filter(TourneyList.tourney_id == Tourney.id).\
             group_by(TourneyList.faction).order_by( TourneyList.faction.desc())

        return ret

    def get_set(self, set_name):
        return self.db_connector.get_session().query(Set).filter_by(set_name=set_name).first()

    def get_tourney(self,tourney_name):
        return self.db_connector.get_session().query(Tourney).filter_by(tourney_name=tourney_name).first()

    def get_tourney_by_id(self,tourney_id):
        return self.db_connector.get_session().query(Tourney).filter_by(id=tourney_id).first()

    def get_lists_for_archtype(self, archtype_id):
        return self.db_connector.get_session().query(TourneyList, ArchtypeList).\
            filter(TourneyList.archtype_id == ArchtypeList.id).\
            filter(ArchtypeList.id==archtype_id).all()

    def get_result_by_id(self, result_id):
        return self.db_connector.get_session().query(RoundResult).filter_by(id=result_id).first()

    def get_all_hashkeys(self):
         return self.db_connector.get_session().\
            query(TourneyList.hashkey).all()

    def get_archtype(self, id):
        return self.db_connector.get_session().query(ArchtypeList).filter_by(id=id).first()


    def get_archtype_by_hashkey(self, hashkey):
        return self.db_connector.get_session().query(ArchtypeList).filter_by(hashkey=hashkey).first()


    def get_all_archtypes(self):
        return self.db_connector.get_session().query(ArchtypeList).all()

    def get_ranked_archtypes(self, url_root):

        count = func.count('*').label("cnt")
        ret = self.db_connector.get_session().query(ArchtypeList, count).\
            join(TourneyList).\
            group_by(ArchtypeList.id).order_by(count.desc())
        archtypes = ret.all()
        ret = []
        for tuple in archtypes:
            ret.append( [ tuple[0].id, tuple[0].pretty_print( url_root=url_root), tuple[1], tuple[0].pretty_print_tags()])
        return ret

    def delete_tourney(self, tourney_name):
        tourney = self.get_tourney( tourney_name)
        if tourney is None:
            return

        self.db_connector.get_session().delete(tourney)
        self.db_connector.get_session().commit()

    def delete_tourney_by_id(self, tourney_id):
        tourney = self.get_tourney_by_id(tourney_id)
        if tourney is None:
            return

        self.db_connector.get_session().delete(tourney)
        self.db_connector.get_session().commit()

    def delete_tourney_list_details(self, tourney_list):

        #unlink the relationship between this tourney list and its archtype
        tourney_list.archtype_list = None
        tourney_list.archtype_id = None
        self.db_connector.get_session().commit()

    def get_upgrade_canonical(self, upgrade_type, upgrade_name):
        ret = self.db_connector.get_session().query(Upgrade).filter_by(upgrade_type=UpgradeType.from_string(upgrade_type)).\
            filter_by(canon_name=upgrade_name)
        return ret.first()

    def get_upgrade(self, upgrade_type, upgrade_name):
        ret = self.db_connector.get_session().query(Upgrade).filter_by(upgrade_type=UpgradeType.from_description(upgrade_type)).\
            filter_by(name=upgrade_name)
        return ret.first()

    def get_tourney_list(self,tourney_list_id):
        return self.db_connector.get_session().query(TourneyList).filter_by(id=tourney_list_id).first()

    def get_players(self, tourney_id):
        return self.db_connector.get_session().query(TourneyPlayer).filter_by(tourney_id=tourney_id).all()

    def get_ship_type(self, ship_type):
            query = self.db_connector.get_session().query(ShipPilot).filter_by(ship_type=ShipType.from_string(ship_type))
            if query.first() is None:
                return None
            return query.first()[0]

    def get_canonical_ship_pilot(self, ship_type, pilot):
            query = self.db_connector.get_session().query(ShipPilot, Pilot).filter_by(ship_type=ShipType.from_string(ship_type)). \
                filter(ShipPilot.pilot_id == Pilot.id). \
                filter(pilot == Pilot.canon_name)
            if query.first() is None:
                return None
            return query.first()[0]

    def get_ship_pilot(self, ship_type, pilot):
        if ship_type == None and pilot == None:
            return self.db_connector.get_session().query(ShipPilot, Pilot).all()
        else:
            query = self.db_connector.get_session().query(ShipPilot, Pilot).filter_by(ship_type=ShipType.from_description(ship_type)). \
                filter(ShipPilot.pilot_id == Pilot.id). \
                filter(pilot == Pilot.name)
            result_set = query.first()
            if result_set is not None:
                return result_set[0]
            else:
                return None

    def get_random_tourney_list(self, tourney):
        session = self.db_connector.get_session()
        query = session.query(Tourney, TourneyList).\
                        filter(TourneyList.tourney_id == Tourney.id).\
                        filter( Tourney.id == tourney.id).\
                        filter(TourneyList.faction == None )
        rowcount = int(query.count())
        randomRow = query.offset( int( rowcount * random.random() ) ).first()
        if randomRow is None:
            return None
        return randomRow[1]

    def get_ship_pilot_rollup(self, elimination=True,
                              storeChampionships=True,
                              regionalChampionships=True,
                              nationalChampionships=True):
        session = self.db_connector.get_session()

        filters = [
            TourneyList.tourney_id == Tourney.id ,
            ArchtypeList.id == TourneyList.archtype_id,
            Ship.archtype_id == ArchtypeList.id ,
            Ship.ship_pilot_id == ShipPilot.id ,
            ShipPilot.pilot_id == Pilot.id
        ]

        if elimination:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)

        self.apply_tourney_type_filter(filters, nationalChampionships, regionalChampionships, storeChampionships)


        ship_pilot_rollup_sql = session.query( ArchtypeList.faction, ShipPilot.ship_type, Pilot.name,
                             func.count( Pilot.id).label("num_pilots"),
                             func.sum( Pilot.cost).label("cost_pilots")).\
                             filter( and_(*filters)).\
            group_by( rollup( ArchtypeList.faction, ShipPilot.ship_type, Pilot.name) ).\
            statement.compile(dialect=mysql.dialect())

        connection = self.db_connector.get_engine().connect()
        ship_pilot_rollup = connection.execute(ship_pilot_rollup_sql)

        #print "ship pilot rollup sql: " + ship_pilot_rollup_sql.string

        filters = [
            TourneyList.tourney_id == Tourney.id ,
            ArchtypeList.id == TourneyList.archtype_id,
            Ship.archtype_id == ArchtypeList.id ,
            Ship.ship_pilot_id == ShipPilot.id ,
            ShipPilot.pilot_id == Pilot.id ,
            ShipUpgrade.ship_id == Ship.id ,
            Upgrade.id == ShipUpgrade.upgrade_id,
        ]

        if elimination:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)

        self.apply_tourney_type_filter(filters, nationalChampionships, regionalChampionships, storeChampionships)

        upgrade_rollup_sql = session.query( ArchtypeList.faction, ShipPilot.ship_type, Pilot.name,
                                        func.count( Upgrade.id).label("num_upgrades"),
                                        func.sum( Upgrade.cost).label("cost_upgrades") ).\
                            filter( and_(*filters)).\
            group_by( rollup( ArchtypeList.faction, ShipPilot.ship_type, Pilot.name) ).\
            statement.compile(dialect=mysql.dialect())

        #print "ship pilot upgrade rollup sql: " + upgrade_rollup_sql.string
        upgrade_rollup = connection.execute( upgrade_rollup_sql )


        ret = ship_pilot_rollup.fetchall() + upgrade_rollup.fetchall()
        connection.close()
        return ret

    def get_upgrade_rollups(self, elimination_only,
                            storeChampionships=True,
                            regionalChampionships=True,
                            nationalChampionships=True):

        session = self.db_connector.get_session()

        filters = [
            TourneyList.tourney_id == Tourney.id,
            ArchtypeList.id == TourneyList.archtype_id,
            Ship.archtype_id == ArchtypeList.id ,
            Ship.ship_pilot_id == ShipPilot.id ,
            ShipPilot.pilot_id == Pilot.id ,
            ShipUpgrade.ship_id == Ship.id,
            Upgrade.id == ShipUpgrade.upgrade_id ,
        ]

        if elimination_only:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)

        self.apply_tourney_type_filter(filters, nationalChampionships, regionalChampionships, storeChampionships)

        upgrade_rollup_sql = session.query( Upgrade.upgrade_type, Upgrade.name,
                                        func.count( Upgrade.id).label("num_upgrades"),
                                        func.sum( Upgrade.cost).label("cost_upgrades") ).\
            filter( and_(*filters)).\
            group_by( rollup( Upgrade.upgrade_type, Upgrade.name) ).\
            statement.compile(dialect=mysql.dialect())

        #print "get_upgrade_rollups: " + upgrade_rollup_sql.string

        connection = self.db_connector.get_engine().connect()
        ret = connection.execute(upgrade_rollup_sql)
        return ret

    def apply_tourney_type_filter(self, filters, nationalChampionships, regionalChampionships, storeChampionships):

        ors = []
        if nationalChampionships:
            ors.append( Tourney.tourney_type == ('%s' % NATIONAL_CHAMPIONSHIP) )
        if regionalChampionships:
            ors.append( Tourney.tourney_type == ('%s' % REGIONAL) )
        if storeChampionships:
            ors.append(  Tourney.tourney_type == ('%s' % STORE_CHAMPIONSHIP) )
        filters.append( or_( *ors ))

    def get_ship_faction_rollups(self, elimination,
                                 storeChampionships=True,
                                 regionalChampionships=True,
                                 nationalChampionships=True):
        session = self.db_connector.get_session()

        filters = [TourneyList.tourney_id == Tourney.id ,
            ArchtypeList.id == TourneyList.archtype_id,
            Ship.archtype_id == ArchtypeList.id ,
            Ship.ship_pilot_id == ShipPilot.id,
            ShipPilot.pilot_id == Pilot.id ]

        if elimination:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)

        self.apply_tourney_type_filter(filters, nationalChampionships, regionalChampionships, storeChampionships)


        faction_ship_rollup_sql = session.query( ArchtypeList.faction, ShipPilot.ship_type,
                             func.count( Pilot.id).label("num_pilots"),
                             func.sum( Pilot.cost).label("cost_pilots")).\
                             filter( and_(*filters)).\
                             group_by( rollup( ArchtypeList.faction, ShipPilot.ship_type) ).statement.compile(dialect=mysql.dialect())

        #print "faction ship rollup sql: " + faction_ship_rollup_sql.string

        connection = self.db_connector.get_engine().connect()
        faction_ship_rollup = connection.execute(faction_ship_rollup_sql)


        filters = [
            TourneyList.tourney_id == Tourney.id,
            ArchtypeList.id == TourneyList.archtype_id,
            Ship.archtype_id == ArchtypeList.id ,
            Ship.ship_pilot_id == ShipPilot.id,
            ShipPilot.pilot_id == Pilot.id ,
            ShipUpgrade.ship_id == Ship.id,
            Upgrade.id == ShipUpgrade.upgrade_id ]

        if elimination:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)

        self.apply_tourney_type_filter(filters, nationalChampionships, regionalChampionships, storeChampionships)

        upgrade_rollup_sql = session.query( ArchtypeList.faction, ShipPilot.ship_type,
                                        func.count( Upgrade.id).label("num_upgrades"),
                                        func.sum( Upgrade.cost).label("cost_upgrades") ).\
            filter( and_(*filters)).\
            group_by( rollup( ArchtypeList.faction, ShipPilot.ship_type) ).\
            statement.compile(dialect=mysql.dialect())

        upgrade_rollup = connection.execute( upgrade_rollup_sql )
        connection.close()

        ret = faction_ship_rollup.fetchall() + upgrade_rollup.fetchall()
        return ret


