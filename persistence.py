__author__ = 'lhayhurst'

from flask import url_for
from geopy import Nominatim
from markupsafe import Markup
import sqlalchemy
from sqlalchemy.dialects import mysql
from sqlalchemy import or_, BigInteger
from decoder import decode
import random
from sqlalchemy.orm import relationship
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql import ClauseElement, literal
from myapp import db_connector, rollup
from xwingmetadata import XWingMetaData
import xwingmetadata
from decl_enum import DeclEnum
from sqlalchemy import Column, Integer, String, func, Date, and_, desc, Boolean, DateTime
from sqlalchemy import ForeignKey

REGIONAL = 'Regional'
STORE_CHAMPIONSHIP = 'Store championship'
NATIONAL_CHAMPIONSHIP = 'Nationals'
ELIMINATION = 'elimination'
SWISS = 'swiss'


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
    TIE_ADVANCED_PROTOTYPE = xwingmetadata.TIE_ADVANCED_PROTOTYPE_CANON_NAME, xwingmetadata.TIE_ADVANCED_PROTOTYPE
    G1A_STARFIGHTER = xwingmetadata.G1A_STARFIGHTER_CANON_NAME, xwingmetadata.G1A_STARFIGHTER
    ATTACK_SHUTTLE = xwingmetadata.ATTACK_SHUTTLE_CANON_NAME, xwingmetadata.ATTACK_SHUTTLE
    VCX100 = xwingmetadata.VCX100_CANON_NAME, xwingmetadata.VCX100
    JUMPMASTER_5000 = xwingmetadata.JUMPMASTER_5000_CANON_NAME, xwingmetadata.JUMPMASTER_5000_
    TIE_SF_FIGHTER = xwingmetadata.TIE_SF_FIGHTER_CANON_NAME, xwingmetadata.TIE_SF_FIGHTER
    ARC_170 = xwingmetadata.ARC_170_CANON_NAME, xwingmetadata.ARC_170
    PROTECTORATE_STARFIGHTER = xwingmetadata.PROTECTORATE_STARFIGHTER_CANON_NAME, xwingmetadata.PROTECTORATE_STARFIGHTER
    LANCER_CLASS_PURSUIT_CRAFT = xwingmetadata.LANCER_CLASS_PURSUIT_CRAFT_CANON_NAME, xwingmetadata.LANCER_CLASS_PURSUIT_CRAFT
    U_WING = xwingmetadata.U_WING_CANON_NAME, xwingmetadata.U_WING
    UPSILON_CLASS_SHUTTLE = xwingmetadata.UPSILON_CLASS_SHUTTLE_CANON_NAME, xwingmetadata.UPSILON_CLASS_SHUTTLE

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
    ship_id = Column(Integer, ForeignKey('{0}.id'.format(ship_table)))
    upgrade_id = Column(Integer, ForeignKey('{0}.id'.format(upgrade_table) ) )
    upgrade = relationship( Upgrade.__name__, uselist=False)
    ship    = relationship( Ship.__name__, back_populates="upgrades")

league_table = "league"
class League(Base):
    __tablename__ = league_table
    id            = Column(Integer, primary_key=True)
    name          = Column(String(128))
    def get_name(self):
        return decode( self.name )
    challonge_name = Column(String(128))
    tiers         = relationship( "Tier", back_populates="league", cascade="all,delete,delete-orphan")


tier_table = "league_tier"
class Tier(Base):
    __tablename__    = tier_table
    id               = Column(Integer, primary_key=True)
    league_id        = Column(Integer, ForeignKey( '{0}.id'.format(league_table) ) )
    name             = Column(String(128))
    def get_name(self):
        return decode( self.name )
    challonge_name             = Column(String(128))
    players           = relationship( "TierPlayer", back_populates="tier", cascade="all,delete,delete-orphan")

    league           = relationship( League.__name__, back_populates="tiers")
    matches       = relationship( "LeagueMatch", back_populates="tier", cascade="all,delete,delete-orphan")
    divisions        = relationship( "Division", back_populates="tier", cascade="all,delete,delete-orphan")

    def get_challonge_url(self):
        return "http://xwingvassal.challonge.com/" + self.challonge_name

    def get_challonge_name(self):
        return "%s-%s" % ( self.league.challonge_name, self.challonge_name)

division_table = "league_division"
class Division(Base):
    __tablename__     = division_table
    id                = Column(Integer, primary_key=True)
    tier_id           = Column(Integer, ForeignKey( '{0}.id'.format(tier_table) ) )
    name              = Column(String(128))
    challonge_name    = Column(String(128))

    def get_name(self):
        return decode( self.name )
    tier              = relationship( Tier.__name__, back_populates="divisions")
    players           = relationship( "TierPlayer", back_populates="division", cascade="all,delete,delete-orphan")


    def get_ranking(self):
        results = []
        for p in self.players:
            results.append(p.get_stats())
        sorted_stats = reversed(sorted(results, key = lambda stat: (stat['wins'], stat['mov']) ))
        ret = []
        i = 1
        for ss in sorted_stats:
            ret.append( {
                            'player' : ss['player'],
                            'player_rank': i,
                            'player_wins': ss['wins'],
                            'player_losses': ss['losses'],
                            'player_draws': ss['draws'],
                            'player_mov' : ss['mov'] } )
            i = i+1
        return ret



tier_player_table = "tier_player"
class TierPlayer(Base):
    __tablename__ = tier_player_table
    id                = Column(Integer, primary_key=True)
    challonge_id      = Column(Integer)
    group_id   = Column(Integer)
    tier_id       = Column(Integer, ForeignKey( '{0}.id'.format(tier_table) ) )
    division_id   = Column(Integer, ForeignKey( '{0}.id'.format(division_table) )  )
    division      = relationship("Division",uselist=False)
    tier          = relationship( "Tier ", uselist=False)
    name              = Column(String(128))
    person_name = Column(String(128))
    email_address = Column(String(128))
    timezone = Column(String(128))
    reddit_handle = Column(String(128))
    challengeboards_handle = Column(String(128))
    checked_in        = Column(Boolean)
    matches           = relationship("LeagueMatch", primaryjoin="or_(TierPlayer.id==LeagueMatch.player1_id,TierPlayer.id==LeagueMatch.player2_id)")

    def get_url(self):
        url = url_for('league_player', player_id=self.id)
        return Markup('<a href="' + url + '">' + self.get_name() +'</a>')



    def get_name(self):
        if self.name is None:
            return ""
        return decode( self.name )

    def get_stats(self):
        ret = { 'wins':0, 'losses':0, 'draws':0, 'total':0, 'rebs':0, 'imps':0, 'scum':0, 'killed':0, 'lost':0, 'mov':0 }
        for m in self.matches:
            if m.is_complete():
                ret['total'] +=1
                if m.player_won(self):
                    ret['wins'] += 1
                    ret['mov'] += 100 + ( m.points_killed(self) - m.points_lost(self))
                elif m.player_lost(self):
                    ret['losses'] += 1
                    ret['mov'] += 100 - ( m.points_lost(self) - m.points_killed(self))
                else:
                    ret['draws'] += 1
                    ret['mov'] += 100
                list_played = m.get_list(self)
                if list_played is not None:
                    if list_played.is_rebel():
                        ret['rebs'] +=1
                    elif list_played.is_imperial():
                        ret['imps'] +=1
                    elif list_played.is_scum():
                        ret['scum'] +=1
                ret['killed'] += m.points_killed( self )
                ret['lost'] += m.points_lost( self )
        ret['player'] = self
        return ret

league_match_table = "league_match"
class LeagueMatch(Base):
    __tablename__       = league_match_table
    id                  = Column(Integer, primary_key=True)
    player1_id          = Column(Integer, ForeignKey( '{0}.id'.format(tier_player_table) ) )
    player2_id          = Column(Integer, ForeignKey( '{0}.id'.format(tier_player_table) ) )
    tier_id           = Column(Integer, ForeignKey( '{0}.id'.format(tier_table) ) )
    challonge_match_id  = Column(Integer)
    player1_score       = Column(Integer)
    player2_score       = Column(Integer)
    state               = Column(String(45))
    player1_list_url    = Column(String(2048))
    player2_list_url    = Column(String(2048))
    challonge_attachment_url = Column(String(2048))
    updated_at          = Column(String(128))

    tier             = relationship( Tier.__name__, uselist=False)
    player1             = relationship( TierPlayer.__name__, uselist=False, foreign_keys='LeagueMatch.player1_id')
    player2             = relationship( TierPlayer.__name__, uselist=False, foreign_keys='LeagueMatch.player2_id')
    player1_list_id     = Column(Integer, ForeignKey( '{0}.id'.format(archtype_list_table) ) )
    player2_list_id     = Column(Integer, ForeignKey( '{0}.id'.format(archtype_list_table) ) )
    player1_list        = relationship("ArchtypeList", uselist=False,foreign_keys='LeagueMatch.player1_list_id')
    player2_list        = relationship("ArchtypeList", uselist=False,foreign_keys='LeagueMatch.player2_list_id')
    subscriptions       = relationship("EscrowSubscription",
                                       back_populates='match',cascade="all,delete,delete-orphan")

    def reset_escrow_url(self,player_id):
        ret = '<a href="' + url_for('reset_match_escrow', match_id=self.id, player_id=player_id,_external=True ) +  '">link</a>'
        return Markup(ret)

    def delete_partial_escrow(self,player_id):
        player_id = long(player_id)
        for s in self.subscriptions:
            if s.observer.id == player_id:
                s.partial_notified = False
        if self.player1.id == player_id:
            self.player1_list = None
            self.player1_list_url = None
        elif self.player2.id == player_id:
            self.player2_list = None
            self.player2_list_url = None

    def get_delete_url(self):
        ret = '<a href="' + url_for('delete_match', match_id=self.id ) +  '">Delete</a>'
        return Markup(ret)

    def unsubscribe_escrow(self,player_id):
        ret = '<a href="' + url_for('unsubscribe_escrow', match_id=self.id,player_id=player_id,_external=True ) +  '">Unsubscribe</a>'
        return Markup(ret)

    def get_subscriber_email_addresses(self):
        ret = ""
        for s in self.subscriptions:
            ret += s.observer.email_address + ","
        return ret

    def points_killed(self, player):
        if self.player1 is not None and player.id == self.player1.id:
            return self.player1_score
        if self.player2 is not None and player.id == self.player2.id:
            return self.player2_score
        return 0

    def points_lost(self, player):
        if self.player1 is not None and player.id == self.player1.id:
            return self.player2_score
        if self.player2 is not None and player.id == self.player2.id:
            return self.player1_score
        return 0

    def get_list(self, player):
        if self.player1 is not None and player.id == self.player1.id:
            return self.player1_list
        if self.player2 is not None and player.id == self.player2.id:
            return self.player2_list
        return None

    def get_winner(self):
        winner = None
        if self.is_complete():
            if self.player1_score > self.player2_score:
                winner = self.player1
            elif self.player2_score > self.player1_score:
                winner = self.player2
        return winner

    def was_draw(self):
        return self.is_complete() and self.player1_score == self.player2_score

    def player_lost(self,player):
        if self.was_draw():
            return False
        return self.player_won(player) == False

    def player_won(self, player):
        winner = self.get_winner()
        if winner is not None:
            if winner == player:
                return True
            else:
                return False
        return False

    def is_complete(self):
        return self.state is not None and self.state == "complete"

    def get_player_list_text_with_link(self, player_id):
        #both lists have been submitted
        if  player_id == self.player1_id:
            return self.get_player1_list_url() + self.player1_list_text()
        else:
            return self.get_player2_list_url() + self.player2_list_text()

    def get_player_list_display(self, player_id, player_list_id,player_name,no_entry=False):
        if self.is_complete():
            if player_list_id is not None:
                return self.get_player_list_text_with_link(player_id)
            else:
                if no_entry:
                    return "List has not been entered"
                else:
                    url = url_for('escrow', match_id=self.id, player_id=player_id)
                    return '<a href="' + url + '">Enter ' + player_name + '\'s list</a>'
        if self.needs_escrow():
            if player_list_id is not None:
                #partial escrow
                return "Has been escrowed"
            else:
                if no_entry:
                    return "List has not been entered"
                else:
                    url = url_for('escrow', match_id=self.id, player_id=player_id)
                    return '<a href="' + url + '">Escrow ' + player_name + '\'s list</a>'
        else:
            return self.get_player_list_text_with_link(player_id)

    def get_player1_list_display(self,no_entry=False):
        return self.get_player_list_display(self.player1_id,
                                            self.player1_list_id,
                                            self.player1.get_name(),no_entry)

    def get_player2_list_display(self,no_entry=False):
        return self.get_player_list_display(self.player2_id,
                                            self.player2_list_id,
                                            self.player2.get_name(),
                                            no_entry)

    def get_player_escrow_text(self, player_id):
        #scenarios
        #neither player has submitted
        if self.player1_list is None and self.player2_list is None:
            return "<br>"

        #player 1 has submitted and player 2 hasn't
        if self.player1_list is not None and self.player2_list is None:
            if player_id == self.player1_id:
                return "Waiting for Player2 to submit their list"
            else:
                return "<br>"

        #player 2 has submitted and player 1 hasn't
        if self.player1_list is None and self.player2_list is not None:
            if player_id == self.player1_id:
                return "<br>"
            else:
                return "Waiting for Player1 to submit their list"

        #both lists have been submitted
        if  player_id == self.player1_id:
            return self.get_player1_list_url() + self.player1_list_text()
        else:
            return self.get_player2_list_url() + self.player2_list_text()

    def get_player1_escrow_text(self):
        return self.get_player_escrow_text(self.player1_id)

    def get_player2_escrow_text(self):
        return self.get_player_escrow_text(self.player2_id)

    def is_complete(self):
        return self.state is not None and self.state == 'complete'

    def get_vlog_url(self):
        if self.challonge_attachment_url is not None:
            return '<a href="http://' + self.challonge_attachment_url + '">Download</a><br>'
        return "None"

    def set_archtype(self, player_id, archtype):
        if player_id == self.player1_id:
            self.player1_list = archtype
        elif player_id == self.player2_id:
            self.player2_list = archtype

    def get_player1_list_url(self):
        return self.get_player_list_url(self.player1_id)

    def get_player2_list_url(self):
        return self.get_player_list_url(self.player2_id)

    def get_player_list_url(self, player_id):
        if self.player1_id == player_id and self.player1_list_url is not None:
            return '<a href="' + self.player1_list_url + '">Link</a><br>'
        elif self.player2_id == player_id and self.player2_list_url is not None:
            return '<a href="' + self.player2_list_url + '">Link</a><br>'
        return "List not yet submitted"

    def set_url(self, player_id, player_list_url):
        if self.player1_id == player_id:
            self.player1_list_url = player_list_url
        elif self.player2_id == player_id:
            self.player2_list_url = player_list_url

    def partial_escrow(self):
        if self.player1_list is not None:
            return self.player1
        if self.player2_list is not None:
            return self.player2
        return None

    def needs_escrow(self):
        return self.player1_list is None or self.player2_list is None

    def player1_list_text(self):
        if self.player1_list is not None:
            return self.player1_list.pretty_print_list()
        return "<br>"

    def player2_list_text(self):
        if self.player2_list is not None:
            return self.player2_list.pretty_print_list()
        return "<br>"

escrow_subscription_table = 'escrow_subscription'
class EscrowSubscription(Base):
    __tablename__ = escrow_subscription_table
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey( '{0}.id'.format(league_match_table) ) )
    observer_id = Column(Integer, ForeignKey( '{0}.id'.format(tier_player_table) ) )
    match                = relationship( LeagueMatch.__name__, uselist=False,back_populates='subscriptions')
    observer             = relationship( TierPlayer.__name__, uselist=False)
    notified             = Column(Boolean)
    partial_notified     = Column(Boolean)


tourney_venue_table_name = 'tourney_venue'

class Tourney(Base):
    __tablename__ = tourney_table
    id = Column(Integer, primary_key=True)
    venue_id          = Column(Integer, ForeignKey( '{0}.id'.format(tourney_venue_table_name) ) )
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
    #venue           = relationship( "TourneyVenue", back_populates="tourney", cascade="all,delete,delete-orphan", uselist=False)
    venue           = relationship( "TourneyVenue", back_populates="tourneys",  uselist=False)

    def get_country(self):
        if self.venue is None:
            return "Unknown"
        return self.venue.get_country()

    def get_venue_url(self):
        if self.venue:
            return self.venue.venue_url()
        return ""

    def get_state(self):
        if self.venue is None:
            return "Unknown"
        return self.venue.get_state()

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
            if self.venue.city is not None:
                ret = ret + "/" + self.venue.city
            if self.venue.state is not None:
                ret = ret + "/" + self.venue.state
            if self.venue.country is not None:
                ret = ret + "/" + self.venue.country
        else:
            ret = "Unknown"
        return decode(ret)

    def venue_name(self):
        if self.venue is not None:
            return self.venue.get_name()
        return "Unknown"

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

     def is_rebel(self):
         if self.faction is not None and self.faction == Faction.REBEL:
             return True
         return False

     def is_imperial(self):
         if self.faction is not None and self.faction == Faction.IMPERIAL:
             return True
         return False

     def is_scum(self):
         if self.faction is not None and self.faction == Faction.SCUM:
             return True
         return False

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
        strings = []
        for ship in ships:
            sp = ship.ship_pilot
            if sp is not None and sp.ship_type is not None:
                strings.append( str( sp.ship_type ))
            if sp is not None and sp.pilot is not None:
                strings.append( sp.pilot.canon_name )
            for supgrade in ship.upgrades:
                if supgrade.upgrade is not None:
                    strings.append( supgrade.upgrade.canon_name )
        liststring = ""
        for s in (strings):
            liststring = liststring + s

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
    player           = relationship( TourneyPlayer.__name__, uselist=False)
    tourney          = relationship( Tourney.__name__, back_populates="tourney_lists")
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


    def versus(self, archtype_id, url_root):
        if self.list1.archtype_list.id == archtype_id:
            return self.list2.pretty_print(manage_list=0, enter_list=0, url_root=url_root)
        return self.list1.pretty_print(manage_list=0, enter_list=0, url_root=url_root)

    def both_lists_recorded(self):
        return self.list1.archtype_list is not None and self.list2.archtype_list is not None

    def get_result_and_score_for_archtype(self, archtype_id):
        return self.get_result_for_archtype(archtype_id) + " " + self.get_score_for_archtype(archtype_id)

    def get_result_for_archtype(self,archtype_id):
        list_id = None
        if self.list1.archtype_list.id == archtype_id:
            list_id = self.list1.id
        else:
            list_id = self.list2.id

        if self.draw is not None and self.draw==True:
            return "drew"

        if self.winner_id == list_id:
            return "won"
        return "lost"

    def get_score_for_archtype(self, archtype_id):
        if self.list1.archtype_list.id == archtype_id:
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

class TourneyVenue(Base):
    __tablename__      = tourney_venue_table_name
    id                 = Column(Integer, primary_key=True)
    country            = Column(String(128))
    state              = Column(String(128))
    city               = Column(String(128))
    venue              = Column(String(128))
    latitude           = Column(sqlalchemy.types.Numeric)
    longitude          = Column(sqlalchemy.types.Numeric)
    tourneys           = relationship( Tourney.__name__, back_populates="venue")

    def valid_venue(self):
        return self.venue is not None and len(self.venue) > 0

    def get_name(self):
        return decode(self.venue)

    def get_city(self):
        return decode(self.city)

    def get_state(self):
        return decode(self.state)

    def get_country(self):
        return decode(self.country)

    def get_num_events(self):
        return len(self.tourneys)

    def venue_url(self):
        url = url_for('venue', venue_id=self.id)
        return '<a target="_blank" href="' + url + '">' + self.get_name() +'</a>'


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

    def get_league(self, league_name):
        return self.db_connector.get_session().query(League).filter(League.name == league_name).first()

    def get_league_by_id(self, league_id):
        return self.db_connector.get_session().query(League).filter(League.id == league_id).first()

    def get_league_player_by_id(self, player_id):
        return self.db_connector.get_session().query(TierPlayer).filter(TierPlayer.id == player_id).first()

    def get_league_player_by_challonge_id(self, challonge_id):
        return self.db_connector.get_session().\
            query(TierPlayer).\
            filter(TierPlayer.challonge_id == challonge_id).first()


    def get_league_player_by_name(self, challonge_name,tier_id):
        return self.db_connector.get_session().\
            query(TierPlayer).filter(
            TierPlayer.name == challonge_name,
            TierPlayer.tier_id == tier_id).first()


    def get_tier(self, tier_name,league):
        return self.db_connector.get_session().query(Tier).filter(
            Tier.challonge_name == tier_name,
            Tier.league_id == league.id,).first()

    def get_division(self, division_name, league):
        return self.db_connector.get_session().query(Division).filter\
            (Division.name == division_name,
             Division.tier_id == Tier.id,
             Tier.league_id == league.id).first()

    def get_recent_league_matches(self, league):
        query = self.db_connector.get_session().query(LeagueMatch).\
            filter( LeagueMatch.tier_id == Tier.id,
                    Tier.league_id == League.id,
                    League.id == league.id,
                    LeagueMatch.state == "complete").order_by(LeagueMatch.updated_at.desc()).limit(100).all()
        return query

    def get_division_by_id(self,division_id):
        return self.db_connector.get_session().query(Division).filter(Division.id == division_id).first()

    def get_tier_by_id(self, tier_id):
        return self.db_connector.get_session().query(Tier).filter(Tier.id == tier_id).first()

    def get_tier_player_by_group_id(self, challonge_player_group_id):
        return self.db_connector.get_session().\
            query(TierPlayer).filter(TierPlayer.group_id == challonge_player_group_id).first()

    def get_tier_player_by_name(self, player_name, league_name ):
        query =  self.db_connector.get_session().query(TierPlayer).\
            filter(TierPlayer.name == player_name,
                   TierPlayer.tier_id == Tier.id,
                   Tier.league_id == League.id,
                   League.name == league_name
                   )
        return query.first()

    def get_tourney_venues(self):
        ret = []
        for v in self.db_connector.get_session().query(TourneyVenue.venue).distinct():
            ret.append(str(decode(v.venue)))
        return ret

    def get_tourney_venue(self, country,state,city,venue):

        venue =  self.db_connector.get_session().query( TourneyVenue ).\
                    filter(TourneyVenue.country == country,
                    TourneyVenue.state == state,
                    TourneyVenue.city == city,
                    TourneyVenue.venue == venue).first()

        if venue is None:
            venue = TourneyVenue( country=country, state=state, city=city, venue=venue)
            g = Nominatim()
            key = "%s %s %s" % ( city, state, country )
            try:
                l = g.geocode(key)
                if l is not None:
                    venue.latitude  = l.latitude
                    venue.longitude = l.longitude
            except Exception:
                print "Unable to lookup lat/lon for %s " % ( key )
        return venue

    def get_match(self, match_id):
        return self.db_connector.get_session().query(LeagueMatch).\
            filter(LeagueMatch.id == match_id ).first()


    def get_match_by_challonge_id(self, match_result_id):
        return self.db_connector.get_session().query(LeagueMatch).\
            filter(LeagueMatch.challonge_match_id == match_result_id ).first()

    def get_tourneys(self):
        return self.db_connector.get_session().query(Tourney)

    def get_upgrades(self):
        return self.db_connector.get_session().query(Upgrade).all()

    def get_ship_upgrades(self):
        return self.db_connector.get_session().query(ShipUpgrade).all()

    def get_venues(self):
        return self.db_connector.get_session().query(TourneyVenue).all()

    def get_venue_by_id(self, venue_id):
        return self.db_connector.get_session().query(TourneyVenue).filter(TourneyVenue.id == venue_id).first()

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

    def get_tourney_types(self):
        return self.db_connector.get_session().query(Tourney.tourney_type).distinct()

    def get_ships_by_faction(self):
        filters = [
            Ship.archtype_id == ArchtypeList.id,
            ShipPilot.id == Ship.ship_pilot_id
        ]
        recs = self.db_connector.get_session().query(ArchtypeList.faction, ShipPilot.ship_type).\
            filter( and_(*filters) ).distinct().all()
        return recs

    def get_pilots_by_faction(self):
        filters = [
            Ship.archtype_id == ArchtypeList.id,
            ShipPilot.id     == Ship.ship_pilot_id,
            Pilot.id         == ShipPilot.pilot_id
        ]
        recs = self.db_connector.get_session().query(ArchtypeList.faction, Pilot.name).\
            filter( and_(*filters) ).distinct().all()
        return recs


    def delete_all_subscriptions(self):
        num_rows_deleted = self.db_connector.get_session().query(EscrowSubscription).delete()
        return num_rows_deleted

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

    def delete_tourney_by_id(self, tourney_id):
        tourney = self.get_tourney_by_id(tourney_id)
        if tourney is None:
            return

        self.db_connector.get_session().delete(tourney)
        self.db_connector.get_session().commit()

    def archtype_tourney_count(self, archtype):
        ret = self.db_connector.get_session().query(TourneyList.id).\
            filter(TourneyList.archtype_id == ArchtypeList.id).\
            filter(archtype.id == ArchtypeList.id)
        lists = ret.all()
        return len(lists)

    def get_archtype_matches(self, archtype_id):
        ret = self.db_connector.get_session().query(RoundResult).\
            filter(archtype_id == ArchtypeList.id,
            ArchtypeList.id == TourneyList.archtype_id,
            TourneyList.tourney_id == Tourney.id,
            TourneyRound.tourney_id == Tourney.id,
            RoundResult.round_id == TourneyRound.id,
            or_(RoundResult.list1_id == TourneyList.id, RoundResult.list2_id == TourneyList.id))
        results = ret.all()
        return results


    def archtype_league_count(self, archtype):
        ret = self.db_connector.get_session().query(LeagueMatch.id).\
            filter(or_(LeagueMatch.player1_list_id == archtype.id,
                       LeagueMatch.player2_list_id == archtype.id ) )
        lists = ret.all()
        return len(lists)

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
            query = self.db_connector.get_session().query(ShipPilot, Pilot).\
                filter_by(ship_type=ShipType.from_description(ship_type)). \
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

    def commit(self):
        self.db_connector.get_session().commit()

    def get_pilot_skill_time_series(self, tourney_filters, show_the_cut_only,venue_id):

        session = self.db_connector.get_session()

        filters = [
            TourneyList.tourney_id == Tourney.id ,
            ArchtypeList.id == TourneyList.archtype_id,
            Ship.archtype_id == ArchtypeList.id ,
            Ship.ship_pilot_id == ShipPilot.id ,
            ShipPilot.pilot_id == Pilot.id
        ]

        year  = sqlalchemy.extract('year', Tourney.tourney_date)
        month = sqlalchemy.extract('month', Tourney.tourney_date)
        group_by_filters = [
            year,
            month,
            ArchtypeList.faction, ShipPilot.ship_type, Pilot.pilot_skill
        ]

        if venue_id is not None:
            filters.append(Tourney.venue_id == venue_id)
            group_by_filters.append(Tourney.venue_id)

        if show_the_cut_only:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)


        ship_pilot_rollup_sql = session.query(
            year.label("year"),
            month.label("month"),
            ArchtypeList.faction, ShipPilot.ship_type, Pilot.pilot_skill,
                             func.count( Pilot.pilot_skill).label("count")).\
                             filter( and_(*filters)).\
            group_by(*group_by_filters ).\
            statement.compile(dialect=mysql.dialect())

        connection = self.db_connector.get_engine().connect()
        ship_pilot_rollup = connection.execute(ship_pilot_rollup_sql)
        return ship_pilot_rollup


    def get_ship_pilot_rollup(self, tourney_filters,show_the_cut_only,venue_id):

        session = self.db_connector.get_session()

        filters = [
            TourneyList.tourney_id == Tourney.id ,
            ArchtypeList.id == TourneyList.archtype_id,
            Ship.archtype_id == ArchtypeList.id ,
            Ship.ship_pilot_id == ShipPilot.id ,
            ShipPilot.pilot_id == Pilot.id
        ]

        year  = sqlalchemy.extract('year', Tourney.tourney_date)
        month = sqlalchemy.extract('month', Tourney.tourney_date)
        group_by_filters = [ year,
                     month,
                     ArchtypeList.faction,
                     ShipPilot.ship_type,
                     Pilot.name]

        if venue_id is not None:
            filters.append( Tourney.venue_id == venue_id )
            group_by_filters.append(Tourney.venue_id)

        if show_the_cut_only:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)

        if tourney_filters is not None:
            self.apply_tourney_type_filter(filters, tourney_filters)


        ship_pilot_rollup_sql = session.query(
            year.label("year"),
            month.label("month"),
            ArchtypeList.faction, ShipPilot.ship_type, Pilot.name,
                             func.count( Pilot.id).label("num_pilots"),
                             func.sum( Pilot.cost).label("cost_pilots")).\
                             filter( and_(*filters)).\
            group_by( rollup( *group_by_filters ) ).\
            statement.compile(dialect=mysql.dialect())

        connection = self.db_connector.get_engine().connect()
        ship_pilot_rollup = connection.execute(ship_pilot_rollup_sql)
        return ship_pilot_rollup

    def get_upgrade_rollups(self, tourney_filters, show_the_cut_only,venue_id):

        session = self.db_connector.get_session()

        filters = [
            TourneyList.tourney_id == Tourney.id,
            ArchtypeList.id == TourneyList.archtype_id,
            Ship.archtype_id == ArchtypeList.id ,
            Ship.ship_pilot_id == ShipPilot.id,
            ShipPilot.pilot_id == Pilot.id ,
            ShipUpgrade.ship_id == Ship.id,
            Upgrade.id == ShipUpgrade.upgrade_id ]

        group_by_filters = [
            sqlalchemy.extract('year', Tourney.tourney_date).label("year"),
            sqlalchemy.extract('month', Tourney.tourney_date).label("month"),
            ArchtypeList.faction,
            ShipPilot.ship_type,
            Pilot.name,
            Upgrade.upgrade_type,
            Upgrade.name,]

        if venue_id:
            filters.append(Tourney.venue_id == venue_id)
            group_by_filters.append(Tourney.venue_id)

        if show_the_cut_only:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)

        self.apply_tourney_type_filter(filters, tourney_filters)

        upgrade_rollup_sql = session.query(
                        sqlalchemy.extract('year', Tourney.tourney_date).label("year"),
                        sqlalchemy.extract('month', Tourney.tourney_date).label("month"),
                        ArchtypeList.faction,
                        ShipPilot.ship_type,
                        Pilot.name,
                        Upgrade.upgrade_type,
                        Upgrade.name,
                        func.count( Upgrade.id).label("num_upgrades"),
                        func.sum( Upgrade.cost).label("cost_upgrades") ).\
            filter( and_(*filters)).\
            group_by(
                *group_by_filters
            ).\
            statement.compile(dialect=mysql.dialect())

        connection = self.db_connector.get_engine().connect()
        ret = connection.execute(upgrade_rollup_sql)
        connection.close()
        return ret


    def get_pilot_upgrade_rollups(self, tourney_filters, show_the_cut_only,venue_id):

        session = self.db_connector.get_session()

        filters = [
            TourneyList.tourney_id == Tourney.id,
            ArchtypeList.id == TourneyList.archtype_id,
            Ship.archtype_id == ArchtypeList.id ,
            Ship.ship_pilot_id == ShipPilot.id,
            ShipPilot.pilot_id == Pilot.id ,
            ShipUpgrade.ship_id == Ship.id,
            Upgrade.id == ShipUpgrade.upgrade_id ]

        group_by_filters = [sqlalchemy.extract('year', Tourney.tourney_date).label("year"),
                    sqlalchemy.extract('month', Tourney.tourney_date).label("month"),
                    ArchtypeList.faction,
                    ShipPilot.ship_type,
                    Pilot.name]

        if venue_id:
            filters.append(Tourney.venue_id == venue_id)
            group_by_filters.append(Tourney.venue_id)

        if show_the_cut_only:
            filters.append( TourneyRanking.tourney_id == Tourney.id)
            filters.append( TourneyList.player_id == TourneyRanking.player_id)
            filters.append(TourneyRanking.elim_rank != None)

        self.apply_tourney_type_filter(filters, tourney_filters)

        upgrade_rollup_sql = session.query(
                        sqlalchemy.extract('year', Tourney.tourney_date).label("year"),
                        sqlalchemy.extract('month', Tourney.tourney_date).label("month"),
                        ArchtypeList.faction,
                        ShipPilot.ship_type,
                        Pilot.name.label("pilot_name"),
                        func.count( Upgrade.id).label("num_upgrades"),
                        func.sum( Upgrade.cost).label("cost_upgrades") ).\
            filter( and_(*filters)).\
            group_by(
                rollup(
                    *group_by_filters
                )
            ).\
            statement.compile(dialect=mysql.dialect())

        connection = self.db_connector.get_engine().connect()
        ret = connection.execute(upgrade_rollup_sql)
        connection.close()
        return ret

    def apply_tourney_type_filter(self, filters, tourney_filters):

        #if all the values are set to false, then just append 'None' to the filter
        if tourney_filters is None:
            return

        all_false = True
        for tt in tourney_filters.keys():
            if tourney_filters[tt] is True:
                all_false = False
                break

        if all_false:
            filters.append( Tourney.tourney_type == 'None')
            return
        else:
            ors = []
            for tt in tourney_filters.keys():
                if tourney_filters[tt] is True:
                    ors.append( Tourney.tourney_type == ('%s' % tt) )
            filters.append( or_( *ors ))

