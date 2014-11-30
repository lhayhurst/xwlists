import random
import re
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from myapp import db_connector
from xwingmetadata import XWingMetaData
import xwingmetadata


__author__ = 'lhayhurst'

import time
from decl_enum import DeclEnum
from sqlalchemy import Column, Integer, String, DateTime, Table, desc, Float, asc, func, Date, MetaData
from sqlalchemy import ForeignKey


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


Base = db_connector.get_base()

class Faction(DeclEnum):
    IMPERIAL = "Imperial", "Imperial"
    REBEL    = "Rebel", "Rebel"

class UpgradeType(DeclEnum):
    TITLE = xwingmetadata.TITLE, xwingmetadata.TITLE
    DROID = xwingmetadata.DROID, xwingmetadata.DROID,
    CREW  = xwingmetadata.CREW, xwingmetadata.CREW
    EPT   = xwingmetadata.EPT, xwingmetadata.EPT
    MOD    = xwingmetadata.MOD, xwingmetadata.MOD
    SYSTEM = xwingmetadata.SYSTEM, xwingmetadata.SYSTEM
    BOMB_MINES = xwingmetadata.BOMB, xwingmetadata.BOMB
    CANNON = xwingmetadata.CANNON, xwingmetadata.CANNON
    TURRET = xwingmetadata.TURRET, xwingmetadata.TURRET
    TORPEDO = xwingmetadata.TORPEDO, xwingmetadata.TORPEDO
    MISSILE = xwingmetadata.MISSILE, xwingmetadata.MISSILE

class ShipType(DeclEnum):
    XWING =  xwingmetadata.X_WING, xwingmetadata.X_WING
    YWING =  xwingmetadata.Y_WING,  xwingmetadata.Y_WING
    AWING =  xwingmetadata.A_WING, xwingmetadata.A_WING
    BWING = xwingmetadata.B_WING, xwingmetadata.A_WING
    EWING  = xwingmetadata.E_WING, xwingmetadata.E_WING
    YT1300 = xwingmetadata.YT_1300, xwingmetadata.YT_1300
    YT2400 = xwingmetadata.YT_2400, xwingmetadata.YT_2400
    HWK290 = xwingmetadata.HWK_290, xwingmetadata.HWK_290
    Z95    = xwingmetadata.Z95_HEADHUNTER, xwingmetadata.Z95_HEADHUNTER
    TIEFIGHTER = xwingmetadata.TIE_FIGHTER, xwingmetadata.TIE_FIGHTER
    TIEADVANCED = xwingmetadata.TIE_ADVANCED, xwingmetadata.TIE_ADVANCED
    TIEINTERCEPTOR = xwingmetadata.TIE_INTERCEPTOR, xwingmetadata.TIE_INTERCEPTOR
    FIRESPRAY = xwingmetadata.FIRESPRAY_31, xwingmetadata.FIRESPRAY_31
    LAMDA = xwingmetadata.LAMBDA_SHUTTLE, xwingmetadata.LAMBDA_SHUTTLE
    TIEBOMBER = xwingmetadata.TIE_BOMBER, xwingmetadata.TIE_BOMBER
    TIEDEFENDER = xwingmetadata.TIE_DEFENDER, xwingmetadata.TIE_DEFENDER
    TIEPHANTOM = xwingmetadata.TIE_PHANTOM, xwingmetadata.TIE_PHANTOM
    DECIMATOR = xwingmetadata.VT_DECIMATOR, xwingmetadata.VT_DECIMATOR

class Pilot(Base):
    __tablename__ = pilot_table
    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True)
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
    upgrade_type = Column(UpgradeType.db_type())
    name = Column(String( 128 ))
    cost = Column(Integer)


class Ship(Base):
    __tablename__ = ship_table
    id = Column(Integer, primary_key=True)
    ship_pilot_id = Column(Integer, ForeignKey('{0}.id'.format(ship_pilot_table)))
    list_id = Column(Integer, ForeignKey('{0}.id'.format(list_table)))  #parent
    ship_pilot = relationship(ShipPilot.__name__, uselist=False)
    upgrades = relationship( "ShipUpgrade", back_populates="ship")

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
    ship_id = Column(Integer, ForeignKey('{0}.id'.format(ship_table)))
    upgrade_id = Column(Integer, ForeignKey('{0}.id'.format(upgrade_table) ) )
    ship    = relationship( Ship.__name__, back_populates="upgrades")
    upgrade = relationship( Upgrade.__name__, uselist=False)


class List(Base):
    __tablename__ = list_table
    id = Column(Integer, primary_key=True)
    name   = Column(String(128))
    faction     = Column(Faction.db_type())
    ships       = relationship(Ship.__name__)
    points      = Column(Integer)


class Tourney(Base):
    __tablename__ = tourney_table
    id = Column(Integer, primary_key=True)
    tourney_name  = Column(String(128))
    tourney_date  = Column(Date)
    tourney_type  = Column(String(128))
    tourney_lists = relationship( "TourneyList", back_populates="tourney", order_by="asc(TourneyList.tourney_standing)")

class TourneyList(Base):
    __tablename__ = tourney_list_table
    id               = Column( Integer, primary_key=True)
    tourney_id       = Column(Integer, ForeignKey('{0}.id'.format(tourney_table)))
    list_id          = Column(Integer, ForeignKey('{0}.id'.format(list_table)))
    player_name      = Column(String(128))
    tourney_standing = Column(Integer)
    tourney_elim_standing  = Column(Integer)
    image            = Column(String(128))
    list             = relationship( List.__name__, uselist=False)
    tourney          = relationship( Tourney.__name__, back_populates="tourney_lists")

    def player_name_stripped(self):
        regex = re.compile('[^a-zA-Z ]')
        return regex.sub('', self.player_name)





class PersistenceManager:

    db_connector = None

    def __init__(self, db_connector):
        self.db_connector = db_connector

    def create_schema(self):
        print("creating schema")
        self.db_connector.get_base().metadata.create_all(self.db_connector.get_engine())

    #this guy is a hack just to fix my schema issues.  I really need to use alembic.
    def create_upgrade_table(self):
        meta = MetaData()

        upgrade = Table(upgrade_table, meta,
                        Column('id', Integer, primary_key=True),
                        Column('upgrade_type', UpgradeType.db_type() ),
                        Column('name', String(128)),
                        Column('cost', Integer) )

        upgrade.create( self.db_connector.get_engine() )

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


    def get_faction_breakout(self):

        session  =  self.db_connector.get_session()
        subq =  session.query( func.count(List.faction ).label('total_factions') ).\
            filter(TourneyList.tourney_id == Tourney.id).\
            filter(List.id == TourneyList.list_id).subquery()

        ret = session.query(
            List.faction, func.count(List.faction).label("sub_total") / subq.c.total_factions ).\
            filter(TourneyList.tourney_id == Tourney.id).\
            filter(List.id == TourneyList.list_id).\
            group_by(List.faction)

        return ret


    def get_ship_breakout(self):

        session = self.db_connector.get_session()
        subq    = session.query( func.sum(Pilot.cost ).label('total_ships') ).\
            filter(TourneyList.tourney_id == Tourney.id).\
            filter(List.id == TourneyList.list_id).\
            filter( Ship.list_id == List.id ).\
            filter( Ship.ship_pilot_id == ShipPilot.id).subquery()

        ret = session.query(
            List.faction, ShipPilot.ship_type, func.count(List.faction).label("sub_total") / subq.c.total_ships ).\
             filter(TourneyList.tourney_id == Tourney.id).\
             filter(List.id == TourneyList.list_id).\
             filter(Ship.list_id == List.id).\
             filter(Ship.ship_pilot_id == ShipPilot.id ).\
             group_by(List.faction, ShipPilot.ship_type)

        return ret

    def get_ship_pilot_breakout(self):

        session = self.db_connector.get_session()
        subq    = session.query( func.count(Ship.ship_pilot_id ).label('total_ships') ).\
            filter(TourneyList.tourney_id == Tourney.id).\
            filter(List.id == TourneyList.list_id).\
            filter( Ship.list_id == List.id ).\
            filter( Ship.ship_pilot_id == ShipPilot.id).subquery()

        ret = self.db_connector.get_session().query(
            List.faction, ShipPilot.ship_type, Pilot.name,
            func.count(List.faction) / subq.c.total_ships).\
            filter(TourneyList.tourney_id == Tourney.id).\
            filter(List.id == TourneyList.list_id).\
            filter(Ship.list_id == List.id).\
            filter(Ship.ship_pilot_id == ShipPilot.id ).\
            filter( ShipPilot.pilot_id == Pilot.id).\
            group_by(List.faction, ShipPilot.ship_type, Pilot.name)
        return ret

    def get_upgrade_type_breakout(self):
        session = self.db_connector.get_session()
        subq    = session.query( func.count(ShipUpgrade.id ).label('total_upgrades') ).subquery()

        ret = session.query(
            Upgrade.upgrade_type, func.count(ShipUpgrade.id).label("sub_total") / subq.c.total_upgrades ).\
            filter( ShipUpgrade.upgrade_id == Upgrade.id ).\
            group_by(Upgrade.upgrade_type)

        return ret

    def get_upgrade_breakout(self):
        session = self.db_connector.get_session()
        subq    = session.query( func.count(ShipUpgrade.id ).label('total_upgrades') ).subquery()

        ret = session.query(
            Upgrade.upgrade_type, Upgrade.name, func.count(ShipUpgrade.id).label("sub_total") / subq.c.total_upgrades ).\
            filter(ShipUpgrade.upgrade_id == Upgrade.id).\
            group_by(Upgrade.upgrade_type, Upgrade.name)

        return ret

    def get_tourney(self,tourney_name):
        return self.db_connector.get_session().query(Tourney).filter_by(tourney_name=tourney_name).first()

    def get_tourney_by_id(self,tourney_id):
        return self.db_connector.get_session().query(Tourney).filter_by(id=tourney_id).first()


    def delete_tourney(self, tourney_name):
        tourney = self.get_tourney( tourney_name)
        for list in tourney.tourney_lists:
            self.db_connector.get_session().delete(list)
        self.db_connector.get_session().delete(tourney)
        self.db_connector.get_session().commit()

    def delete_tourney_list_details(self, tourney_list):

        for ship in tourney_list.list.ships:
            for su in ship.upgrades:
                self.db_connector.get_session().delete(su)
            self.db_connector.get_session().delete(ship)
        self.db_connector.get_session().delete(tourney_list.list)
        tourney_list.list = None
        self.db_connector.get_session().commit()


    def get_tourney_list(self,tourney_list_id):
        return self.db_connector.get_session().query(TourneyList).filter_by(id=tourney_list_id).first()


    def get_ship_pilot(self, ship_type, pilot):
        if ship_type == None and pilot == None:
            return self.db_connector.get_session().query(ShipPilot, Pilot).all()
        else:
            return \
            self.db_connector.get_session().query(ShipPilot, Pilot).filter_by(ship_type=ShipType.from_string(ship_type)). \
                filter(ShipPilot.pilot_id == Pilot.id). \
                filter(pilot == Pilot.name).first()[0]


    def get_random_tourney_list(self, tourney):
        session = self.db_connector.get_session()
        query = session.query(Tourney, TourneyList).\
                        filter(TourneyList.tourney_id == Tourney.id).\
                        filter(TourneyList.list_id == None )
        rowcount = int(query.count())
        randomRow = query.offset( int( rowcount * random.random() ) ).first()
        if randomRow is None:
            return None
        return randomRow[1]

    def get_tourney_summary(self):
        session = self.db_connector.get_session()
        tourney_lists = session.query(TourneyList).all()

        ret = {}

        for tl in tourney_lists:
            tourney_name = tl.tourney.tourney_name
            if not ret.has_key(tourney_name):
                ret[tourney_name] = { 'num_entered' : 0, 'num_not_entered' : 0, 'tourney': tl.tourney}
            if tl.list_id is None:
                ret[tourney_name]['num_not_entered'] += 1
            else:
                ret[tourney_name]['num_entered'] += 1
        return ret


