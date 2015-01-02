from collections import OrderedDict
from flask import url_for
from sqlalchemy.dialects import mysql
from sqlalchemy.sql.operators import ColumnOperators

__author__ = 'lhayhurst'

import random

from sqlalchemy.orm import relationship
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ColumnElement
from sqlalchemy.sql.elements import _clause_element_as_expr

from myapp import db_connector
from xwingmetadata import XWingMetaData
import xwingmetadata




from decl_enum import DeclEnum
from sqlalchemy import Column, Integer, String, func, Date, and_, desc
from sqlalchemy import ForeignKey

#rollup help
#see https://groups.google.com/forum/#!msg/sqlalchemy/Pj5T8hO_ibQ/LrmBcIBxnNwJ
class rollup(ColumnElement):
    def __init__(self, *elements):
        self.elements = [_clause_element_as_expr(e) for e in elements]

@compiles(rollup, "mysql")
def _mysql_rollup(element, compiler, **kw):
    return "%s WITH ROLLUP" % (', '.join([compiler.process(e, **kw) for e in element.elements]))


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

Base = db_connector.get_base()

class RoundType(DeclEnum):
    ELIMINATION     = "Elimination", "Elimination"
    PRE_ELIMINATION = 'Pre-Elimination', 'Pre-Elimination'

class Faction(DeclEnum):
    IMPERIAL = "empire", "Galactic Empire"
    REBEL    = "rebels", "Rebel Alliance"
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

class Pilot(Base):
    __tablename__ = pilot_table
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
    canon_name = Column(String(128), unique=True)
    cost = Column(Integer)

class ShipPilot(Base):
    __tablename__ = ship_pilot_table
    id = Column(Integer, primary_key=True)
    ship_type = Column(ShipType.db_type())
    pilot_id = Column(Integer, ForeignKey('{0}.id'.format(pilot_table)))
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
    tlist_id = Column(Integer, ForeignKey('{0}.id'.format(tourney_list_table)))  #parent
    ship_pilot = relationship(ShipPilot.__name__, uselist=False)
    upgrades = relationship( "ShipUpgrade", back_populates="ship")
    tlist    = relationship("TourneyList", uselist=False)

    def get_upgrade(self, upgrade_name ):

        ret = []

        num_upgrades = 1

        if "." in upgrade_name:
            a = upgrade_name.split('.')
            upgrade_name = a[0]
            num_upgrades = int(a[1])

        for ship_upgrade in self.upgrades:
            upgrade = ship_upgrade.upgrade
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
    tourney_name    = Column(String(128))
    tourney_date    = Column(Date)
    tourney_type    = Column(String(128))
    round_length    = Column(Integer)
    tourney_lists   = relationship( "TourneyList", back_populates="tourney", cascade="all,delete,delete-orphan" )
    rounds          = relationship( "TourneyRound", back_populates="tourney", order_by="asc(TourneyRound.round_num)", cascade="all,delete,delete-orphan")
    rankings        = relationship( "TourneyRanking", back_populates="tourney", order_by="asc(TourneyRanking.rank)", cascade="all,delete,delete-orphan")
    tourney_players = relationship( "TourneyPlayer", back_populates="tourney", cascade="all,delete,delete-orphan")
    sets            = relationship( "TourneySet", back_populates="tourney", cascade="all,delete,delete-orphan")
    venue           = relationship( "TourneyVenue", back_populates="tourney", cascade="all,delete,delete-orphan", uselist=False)


    def get_pre_elimination_rounds(self):
        ret = [r for r in self.rounds if r.round_type == RoundType.PRE_ELIMINATION]
        return ret

    def get_elim_rounds(self):
        ret =  [r for r in self.rounds if r.round_type == RoundType.ELIMINATION]
        return ret


    def get_descending_elim_rounds(self):
        ret =  [r for r in self.rounds if r.round_type == RoundType.ELIMINATION]
        ret.reverse()
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
        return ret

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


class TourneyList(Base):
    __tablename__    = tourney_list_table
    id               = Column( Integer, primary_key=True)
    tourney_id       = Column(Integer, ForeignKey('{0}.id'.format(tourney_table)))
    player_id        = Column(Integer, ForeignKey('{0}.id'.format(tourney_player_table)))
    image            = Column(String(128))
    name             = Column(String(128))
    faction          = Column(Faction.db_type())
    points           = Column(Integer)
    player           = relationship( TourneyPlayer.__name__, uselist=False)
    tourney          = relationship( Tourney.__name__, back_populates="tourney_lists")
    ships            = relationship(Ship.__name__, cascade="all,delete,delete-orphan")

tourney_round_table = "tourney_round"
class TourneyRound(Base):
    __tablename__ = tourney_round_table
    id            = Column(Integer, primary_key=True)
    tourney_id    = Column(Integer, ForeignKey('{0}.id'.format(tourney_table)))
    round_num     = Column(Integer)
    round_type    = Column(RoundType.db_type())
    results       = relationship( "RoundResult", back_populates="round", cascade="all,delete,delete-orphan")
    tourney       = relationship( Tourney.__name__, back_populates="rounds")

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
    tourney            = relationship( Tourney.__name__, back_populates="rankings")
    player             = relationship( TourneyPlayer.__name__, uselist=False)

round_result_table = "round_result"
class RoundResult(Base):
    __tablename__ = round_result_table
    id            = Column(Integer, primary_key=True)
    round_id      = Column(ForeignKey('{0}.id'.format(tourney_round_table)))
    list1_id      = Column(ForeignKey('{0}.id'.format(tourney_list_table)))
    list2_id      = Column(ForeignKey('{0}.id'.format(tourney_list_table)))
    winner_id     = Column(ForeignKey('{0}.id'.format(tourney_list_table)))
    loser_id      = Column(ForeignKey('{0}.id'.format(tourney_list_table)))
    list1_score   = Column(Integer)
    list2_score   = Column(Integer)
    round         = relationship( TourneyRound.__name__, back_populates="results")
    list1         = relationship( TourneyList.__name__, foreign_keys='RoundResult.list1_id',  uselist=False)
    list2         = relationship( TourneyList.__name__, foreign_keys='RoundResult.list2_id',  uselist=False)
    winner        = relationship( TourneyList.__name__, foreign_keys='RoundResult.winner_id', uselist=False)
    loser         = relationship( TourneyList.__name__, foreign_keys='RoundResult.loser_id',  uselist=False)

    def winning_score(self):
        if self.winner.id == self.list1.id:
            return self.list1_score
        return self.list2_score

    def losing_score(self):
        if self.loser.id == self.list1.id:
            return self.list1_score
        return self.list2_score

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

    def get_tourneys(self):
        return self.db_connector.get_session().query(Tourney)


    def get_upgrades(self):
        return self.db_connector.get_session().query(Upgrade).all()

    def get_ship_upgrades(self):
        return self.db_connector.get_session().query(ShipUpgrade).all()


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


    def delete_tourney(self, tourney_name):
        tourney = self.get_tourney( tourney_name)
        if tourney is None:
            return

        self.db_connector.get_session().delete(tourney)
        self.db_connector.get_session().commit()

    def delete_tourney_list_details(self, tourney_list):

        for ship in tourney_list.ships:
            for su in ship.upgrades:
                self.db_connector.get_session().delete(su)
            self.db_connector.get_session().delete(ship)
        tourney_list.faction = None
        tourney_list.points  = None
        tourney_list.shiops  = None
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


    def get_canonical_ship_pilot(self, ship_type, pilot):
            return \
            self.db_connector.get_session().query(ShipPilot, Pilot).filter_by(ship_type=ShipType.from_string(ship_type)). \
                filter(ShipPilot.pilot_id == Pilot.id). \
                filter(pilot == Pilot.canon_name).first()[0]

    def get_ship_pilot(self, ship_type, pilot):
        if ship_type == None and pilot == None:
            return self.db_connector.get_session().query(ShipPilot, Pilot).all()
        else:
            return \
            self.db_connector.get_session().query(ShipPilot, Pilot).filter_by(ship_type=ShipType.from_description(ship_type)). \
                filter(ShipPilot.pilot_id == Pilot.id). \
                filter(pilot == Pilot.name).first()[0]


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

    def get_tourney_summary(self):
        session = self.db_connector.get_session()
        tourney_lists = session.query(TourneyList).join(Tourney).order_by(desc(Tourney.tourney_date)).all()

        ret = OrderedDict()

        for tl in tourney_lists:
            tourney_name = tl.tourney.tourney_name
            if not ret.has_key(tourney_name):
                ret[tourney_name] = { 'num_entered' : 0, 'num_not_entered' : 0, 'tourney': tl.tourney}
            if len(tl.ships) == 0:
                ret[tourney_name]['num_not_entered'] += 1
            else:
                ret[tourney_name]['num_entered'] += 1
        return ret

    def get_ship_pilot_rollup(self, elimination_only):
        session = self.db_connector.get_session()

        filters = [
            TourneyList.tourney_id == Tourney.id ,
            Ship.tlist_id == TourneyList.id ,
            Ship.ship_pilot_id == ShipPilot.id ,
            ShipPilot.pilot_id == Pilot.id
        ]

        if elimination_only:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)


        ship_pilot_rollup_sql = session.query( TourneyList.faction, ShipPilot.ship_type, Pilot.name,
                             func.count( Pilot.id).label("num_pilots"),
                             func.sum( Pilot.cost).label("cost_pilots")).\
                             filter( and_(*filters)).\
            group_by( rollup( TourneyList.faction, ShipPilot.ship_type, Pilot.name) ).\
            statement.compile(dialect=mysql.dialect())

        connection = self.db_connector.get_engine().connect()
        ship_pilot_rollup = connection.execute(ship_pilot_rollup_sql)

        filters = [
            TourneyList.tourney_id == Tourney.id ,
            Ship.tlist_id == TourneyList.id ,
            Ship.ship_pilot_id == ShipPilot.id ,
            ShipPilot.pilot_id == Pilot.id ,
            ShipUpgrade.ship_id == Ship.id ,
            Upgrade.id == ShipUpgrade.upgrade_id,
        ]

        if elimination_only:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)


        upgrade_rollup_sql = session.query( TourneyList.faction, ShipPilot.ship_type, Pilot.name,
                                        func.count( Upgrade.id).label("num_upgrades"),
                                        func.sum( Upgrade.cost).label("cost_upgrades") ).\
                            filter( and_(*filters)).\
            group_by( rollup( TourneyList.faction, ShipPilot.ship_type, Pilot.name) ).\
            statement.compile(dialect=mysql.dialect())

        upgrade_rollup = connection.execute( upgrade_rollup_sql )


        ret = ship_pilot_rollup.fetchall() + upgrade_rollup.fetchall()
        connection.close()
        return ret

    def get_upgrade_rollups(self, elimination_only):

        session = self.db_connector.get_session()

        filters = [
            TourneyList.tourney_id == Tourney.id,
            Ship.tlist_id == TourneyList.id ,
            Ship.ship_pilot_id == ShipPilot.id ,
            ShipPilot.pilot_id == Pilot.id ,
            ShipUpgrade.ship_id == Ship.id,
            Upgrade.id == ShipUpgrade.upgrade_id ,
        ]

        if elimination_only:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)

        upgrade_rollup_sql = session.query( Upgrade.upgrade_type, Upgrade.name,
                                        func.count( Upgrade.id).label("num_upgrades"),
                                        func.sum( Upgrade.cost).label("cost_upgrades") ).\
            filter( and_(*filters)).\
            group_by( rollup( Upgrade.upgrade_type, Upgrade.name) ).\
            statement.compile(dialect=mysql.dialect())

        connection = self.db_connector.get_engine().connect()
        ret = connection.execute(upgrade_rollup_sql)
        return ret

    def get_ship_faction_rollups(self, elimination_only):
        session = self.db_connector.get_session()

        filters = [TourneyList.tourney_id == Tourney.id ,
                        Ship.tlist_id == TourneyList.id,
                        Ship.ship_pilot_id == ShipPilot.id,
                        ShipPilot.pilot_id == Pilot.id ]

        if elimination_only:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)



        faction_ship_rollup_sql = session.query( TourneyList.faction, ShipPilot.ship_type,
                             func.count( Pilot.id).label("num_pilots"),
                             func.sum( Pilot.cost).label("cost_pilots")).\
                             filter( and_(*filters)).\
                             group_by( rollup( TourneyList.faction, ShipPilot.ship_type) ).statement.compile(dialect=mysql.dialect())

        connection = self.db_connector.get_engine().connect()
        faction_ship_rollup = connection.execute(faction_ship_rollup_sql)


        filters = [ TourneyList.tourney_id == Tourney.id,
             Ship.tlist_id == TourneyList.id,
             Ship.ship_pilot_id == ShipPilot.id,
            ShipPilot.pilot_id == Pilot.id ,
             ShipUpgrade.ship_id == Ship.id,
            Upgrade.id == ShipUpgrade.upgrade_id ]

        if elimination_only:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)


        upgrade_rollup_sql = session.query( TourneyList.faction, ShipPilot.ship_type,
                                        func.count( Upgrade.id).label("num_upgrades"),
                                        func.sum( Upgrade.cost).label("cost_upgrades") ).\
            filter( and_(*filters)).\
            group_by( rollup( TourneyList.faction, ShipPilot.ship_type) ).\
            statement.compile(dialect=mysql.dialect())

        upgrade_rollup = connection.execute( upgrade_rollup_sql )
        connection.close()

        ret = faction_ship_rollup.fetchall() + upgrade_rollup.fetchall()
        return ret
