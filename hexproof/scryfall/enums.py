"""
* Scryfall Enums
"""
# Standard Library Imports
from dataclasses import dataclass
from omnitils.enums import StrConstant

# Third Party Imports
import yarl

# Constants
__SCRY_SITE__ = yarl.URL('https://scryfall.com')
__SCRY_API__ = yarl.URL('https://api.scryfall.com')

"""
* URL Enums
"""


@dataclass
class ScryURL:
    """Catalogued URL hierarchy for the Scryfall data source."""

    @dataclass
    class Site:
        """Scryfall public facing site endpoints."""
        Main = __SCRY_SITE__
        Sets = Main / 'sets'

    @dataclass
    class API:
        """Scryfall REST API endpoints."""
        Main = __SCRY_API__

        @dataclass
        class Sets:
            """Scryfall API 'Set' object endpoints."""
            All = __SCRY_API__ / 'sets'
            TCGPlayer = All / 'tcgplayer'

        @dataclass
        class Cards:
            """Scryfall API 'Card' object endpoints."""
            Main = __SCRY_API__ / 'cards'
            Named = Main / 'named'
            Search = Main / 'search'

        @dataclass
        class Catalogs:
            """Scryfall API 'Catalog' object endpoints."""
            Main: yarl.URL = __SCRY_API__ / 'catalog'
            CardNames: yarl.URL = Main / 'card-names'
            ArtistNames: yarl.URL = Main / 'artist-names'
            WordBank: yarl.URL = Main / 'word-bank'
            CreatureTypes: yarl.URL = Main / 'creature-types'
            PlaneswalkerTypes: yarl.URL = Main / 'planeswalker-types'
            LandTypes: yarl.URL = Main / 'land-types'
            ArtifactTypes: yarl.URL = Main / 'artifact-types'
            EnchantmentTypes: yarl.URL = Main / 'enchantment-types'
            SpellTypes: yarl.URL = Main / 'spell-types'
            Powers: yarl.URL = Main / 'powers'
            Toughnesses: yarl.URL = Main / 'toughnesses'
            Loyalties: yarl.URL = Main / 'loyalties'
            Watermarks: yarl.URL = Main / 'watermarks'
            KeywordAbilities: yarl.URL = Main / 'keyword-abilities'
            KeywordActions: yarl.URL = Main / 'keyword-actions'
            AbilityWords: yarl.URL = Main / 'ability-words'
            Supertypes: yarl.URL = Main / 'supertypes'

        @dataclass
        class Bulk:
            """Scryfall API bulk data endpoints."""
            All = __SCRY_API__ / 'bulk-data'


"""
* Color Enums
"""


class BorderColor(StrConstant):
    """Border colors as defined by Scryfall."""
    Black = 'black'
    Borderless = 'borderless'
    Gold = 'gold'
    Silver = 'silver'
    White = 'white'


class ManaColor(StrConstant):
    """Mana colors as defined by Scryfall."""
    White = 'W'
    Blue = 'U'
    Black = 'B'
    Red = 'R'
    Green = 'G'
    Colorless = 'C'


"""
* Base Card Definitions
"""


class CardFinishes(StrConstant):
    """Card finishes as defined by Scryfall."""
    Etched = 'etched'
    Foil = 'foil'
    Nonfoil = 'nonfoil'


class CardFrame(StrConstant):
    """Card frames as defined by Scryfall."""
    M93 = '1993'
    M97 = '1997'
    M03 = '2003'
    M15 = '2015'
    Future = 'future'


class CardFrameEffects(StrConstant):
    """Card frame effects as defined by Scryfall."""
    Legendary = 'legendary'
    Miracle = 'miracle'
    Nyxtouched = 'nyxtouched'
    Draft = 'draft'
    Devoid = 'devoid'
    Tombstone = 'tombstone'
    Colorshifted = 'colorshifted'
    Inverted = 'inverted'
    SunMoonDFC = 'sunmoondfc'
    CompassLandDFC = 'compasslanddfc'
    OriginPWDFC = 'originpwdfc'
    MoonEldraziDFC = 'mooneldrazidfc'
    WaxingAndWaningMoonDFC = 'waxingandwaningmoondfc'
    Showcase = 'showcase'
    ExtendedArt = 'extendedart'
    Companion = 'companion'
    Etched = 'etched'
    Snow = 'snow'
    Lesson = 'lesson'
    ShatteredGlass = 'shatteredglass'
    ConvertDFC = 'convertdfc'
    FanDFC = 'fandfc'
    UpsideDownDFC = 'upsidedowndfc'
    Spree = 'spree'


class CardGame(StrConstant):
    """Card game types as defined by Scryfall."""
    Paper = 'paper'
    Arena = 'arena'
    MTGO = 'mtgo'


class CardLayout(StrConstant):
    """Card frame layouts as defined by Scryfall."""
    Normal = 'normal'
    Split = 'split'
    Flip = 'flip'
    Transform = 'transform'
    ModalDFC = 'modal_dfc'
    Meld = 'meld'
    Leveler = 'leveler'
    Class = 'class'
    Case = 'case'
    Saga = 'saga'
    Adventure = 'adventure'
    Mutate = 'mutate'
    Prototype = 'prototype'
    Battle = 'battle'
    Planar = 'planar'
    Scheme = 'scheme'
    Vanguard = 'vanguard'
    Token = 'token'
    DoubleFacedToken = 'double_faced_token'
    Emblem = 'emblem'
    Augment = 'augment'
    Host = 'host'
    ArtSeries = 'art_series'
    ReversibleCard = 'reversible_card'


class CardImageStatus(StrConstant):
    """Card image status as defined by Scryfall."""
    Missing = 'missing'
    Placeholder = 'placeholder'
    Lowres = 'lowres'
    HighresScan = 'highres_scan'


class CardLegality(StrConstant):
    """Card legalities as defined by Scryfall."""
    Banned = 'banned'
    Legal = 'legal'
    NotLegal = 'not_legal'
    Restricted = 'restricted'


class CardRarity(StrConstant):
    """Card rarities as defined by Scryfall."""
    Common = 'common'
    Uncommon = 'uncommon'
    Rare = 'rare'
    Special = 'special'
    Mythic = 'mythic'
    Bonus = 'bonus'


class CardSecurityStamp(StrConstant):
    """Card security stamps as defined by Scryfall."""
    Oval = 'oval'
    Triangle = 'triangle'
    Acorn = 'acorn'
    Circle = 'circle'
    Arena = 'arena'
    Heart = 'heart'


"""
* Set Enums
"""


class SetType(StrConstant):
    """Set 'types' as defined by Scryfall.

    Notes:
        https://scryfall.com/docs/api/sets
    """
    Core = 'core'
    Expansion = 'expansion'
    Masters = 'masters'
    Eternal = 'eternal'
    Alchemy = 'alchemy'
    Masterpiece = 'masterpiece'
    Arsenal = 'arsenal'
    FromTheVault = 'from_the_vault'
    Spellbook = 'spellbook'
    PremiumDeck = 'premium_deck'
    DuelDeck = 'duel_deck'
    DraftInnovation = 'draft_innovation'
    TreasureChest = 'treasure_chest'
    Commander = 'commander'
    Planechase = 'planechase'
    Archenemy = 'archenemy'
    Vanguard = 'vanguard'
    Funny = 'funny'
    Starter = 'starter'
    Box = 'box'
    Promo = 'promo'
    Token = 'token'
    Memorabilia = 'memorabilia'
    Minigame = 'minigame'


"""
* Migration Enums
"""


class MigrationStrategy(StrConstant):
    """Migration strategies as defined by Scryfall."""
    Merge = 'merge'
    Delete = 'delete'
