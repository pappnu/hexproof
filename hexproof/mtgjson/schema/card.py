"""
* MTGJSON Schema: Card
* https://mtgjson.com/data-models/card/
"""
# Standard Library Imports
from typing import Optional, Union

# Third Party Imports
from omnitils.schema import Schema

# Local Imports
from hexproof.mtgjson.schema.foreign_data import ForeignData
from hexproof.mtgjson.schema.identifiers import Identifiers
from hexproof.mtgjson.schema.leadership_skills import LeadershipSkills
from hexproof.mtgjson.schema.legalities import Legalities
from hexproof.mtgjson.schema.purchase_urls import PurchaseUrls
from hexproof.mtgjson.schema.related_cards import RelatedCards
from hexproof.mtgjson.schema.rulings import Rulings
from hexproof.mtgjson.schema.source_products import SourceProducts

"""
* Schemas
"""


class CardAtomic(Schema):
    """Model describing the properties of a single "atomic" card, an oracle-like entity of a card that
        only has evergreen properties that would never change from printing to printing."""
    asciiName: Optional[str] = None
    attractionLights: Optional[list[float]] = None
    colorIdentity: list[str] = []
    colorIndicator: Optional[list[str]] = None
    colors: list[str] = []
    convertedManaCost: float
    defense: Optional[str] = None
    edhrecRank: Optional[float] = None
    edhrecSaltiness: Optional[float] = None
    faceConvertedManaCost: Optional[float] = None
    faceManaValue: Optional[float] = None
    faceName: Optional[str] = None
    firstPrinting: Optional[str] = None
    foreignData: Optional[list[ForeignData]] = None
    hand: Optional[str] = None
    hasAlternativeDeckLimit: bool
    identifiers: Identifiers
    isFunny: Optional[bool] = None
    isReserved: Optional[bool] = None
    keywords: Optional[list[str]] = None
    layout: str
    leadershipSkills: Optional[LeadershipSkills] = None
    legalities: Legalities
    life: Optional[str] = None
    loyalty: Optional[str] = None
    manaCost: Optional[str] = None
    manaValue: float
    name: str
    power: Optional[str] = None
    printings: Optional[list[str]] = None
    purchaseUrls: PurchaseUrls
    relatedCards: RelatedCards
    rulings: Optional[list[Rulings]] = None
    side: Optional[str] = None
    subsets: Optional[list[str]] = None
    subtypes: list[str] = []
    supertypes: list[str] = []
    text: Optional[str] = None
    toughness: Optional[str] = None
    type: str
    types: list[str] = []


class CardDeck(Schema):
    """Model describing the properties of a single card found in a Deck."""
    artist: Optional[str] = None
    artistIds: Optional[list[str]] = None
    asciiName: Optional[str] = None
    attractionLights: Optional[list[float]] = None
    availability: list[str] = []
    boosterTypes: Optional[list[str]] = None
    borderColor: str
    cardParts: Optional[list[str]] = None
    colorIdentity: list[str] = []
    colorIndicator: Optional[list[str]] = None
    colors: list[str] = []
    convertedManaCost: float
    count: float
    defense: Optional[str] = None
    duelDeck: Optional[str] = None
    edhrecRank: Optional[float] = None
    edhrecSaltiness: Optional[float] = None
    faceConvertedManaCost: Optional[float] = None
    faceFlavorName: Optional[str] = None
    faceManaValue: Optional[float] = None
    faceName: Optional[str] = None
    finishes: list[str] = []
    flavorName: Optional[str] = None
    flavorText: Optional[str] = None
    foreignData: Optional[list[ForeignData]] = None
    frameEffects: Optional[list[str]] = None
    frameVersion: str
    hand: Optional[str] = None
    hasAlternativeDeckLimit: Optional[bool] = None
    hasContentWarning: Optional[bool] = None
    hasFoil: bool
    hasNonFoil: bool
    identifiers: Identifiers
    isAlternative: Optional[bool] = None
    isFoil: bool
    isFullArt: Optional[bool] = None
    isFunny: Optional[bool] = None
    isOnlineOnly: Optional[bool] = None
    isOversized: Optional[bool] = None
    isPromo: Optional[bool] = None
    isRebalanced: Optional[bool] = None
    isReprint: Optional[bool] = None
    isReserved: Optional[bool] = None
    isStarter: Optional[bool] = None
    isStorySpotlight: Optional[bool] = None
    isTextless: Optional[bool] = None
    isTimeshifted: Optional[bool] = None
    keywords: Optional[list[str]] = None
    language: str
    layout: str
    leadershipSkills: Optional[LeadershipSkills] = None
    legalities: Legalities
    life: Optional[str] = None
    loyalty: Optional[str] = None
    manaCost: Optional[str] = None
    manaValue: float
    name: str
    number: str
    originalPrintings: Optional[list[str]] = None
    originalReleaseDate: Optional[str] = None
    originalText: Optional[str] = None
    originalType: Optional[str] = None
    otherFaceIds: Optional[list[str]] = None
    power: Optional[str] = None
    printings: Optional[list[str]] = None
    promoTypes: Optional[list[str]] = None
    purchaseUrls: PurchaseUrls
    rarity: str
    relatedCards: Optional[RelatedCards] = None
    rebalancedPrintings: Optional[list[str]] = None
    rulings: Optional[list[Rulings]] = None
    securityStamp: Optional[str] = None
    setCode: str
    side: Optional[str] = None
    signature: Optional[str] = None
    sourceProducts: Optional[SourceProducts] = None
    subsets: Optional[list[str]] = None
    subtypes: list[str] = []
    supertypes: list[str] = []
    text: Optional[str] = None
    toughness: Optional[str] = None
    type: str
    types: list[str] = []
    uuid: str
    variations: Optional[list[str]] = None
    watermark: Optional[str] = None


class CardSet(Schema):
    """Model describing the properties of a single card found in a Set."""
    artist: Optional[str] = None
    artistIds: Optional[list[str]] = None
    asciiName: Optional[str] = None
    attractionLights: Optional[list[float]] = None
    availability: list[str] = []
    boosterTypes: Optional[list[str]] = None
    borderColor: str
    cardParts: Optional[list[str]] = None
    colorIdentity: list[str] = []
    colorIndicator: Optional[list[str]] = None
    colors: list[str] = []
    convertedManaCost: float
    defense: Optional[str] = None
    duelDeck: Optional[str] = None
    edhrecRank: Optional[float] = None
    edhrecSaltiness: Optional[float] = None
    faceConvertedManaCost: Optional[float] = None
    faceFlavorName: Optional[str] = None
    faceManaValue: Optional[float] = None
    faceName: Optional[str] = None
    finishes: list[str] = []
    flavorName: Optional[str] = None
    flavorText: Optional[str] = None
    foreignData: Optional[list[ForeignData]] = None
    frameEffects: Optional[list[str]] = None
    frameVersion: str
    hand: Optional[str] = None
    hasAlternativeDeckLimit: Optional[bool] = None
    hasContentWarning: Optional[bool] = None
    hasFoil: bool
    hasNonFoil: bool
    identifiers: Identifiers
    isAlternative: Optional[bool] = None
    isFullArt: Optional[bool] = None
    isFunny: Optional[bool] = None
    isOnlineOnly: Optional[bool] = None
    isOversized: Optional[bool] = None
    isPromo: Optional[bool] = None
    isRebalanced: Optional[bool] = None
    isReprint: Optional[bool] = None
    isReserved: Optional[bool] = None
    isStarter: Optional[bool] = None
    isStorySpotlight: Optional[bool] = None
    isTextless: Optional[bool] = None
    isTimeshifted: Optional[bool] = None
    keywords: Optional[list[str]] = None
    language: str
    layout: str
    leadershipSkills: Optional[LeadershipSkills] = None
    legalities: Legalities
    life: Optional[str] = None
    loyalty: Optional[str] = None
    manaCost: Optional[str] = None
    manaValue: float
    name: str
    number: str
    originalPrintings: Optional[list[str]] = None
    originalReleaseDate: Optional[str] = None
    originalText: Optional[str] = None
    originalType: Optional[str] = None
    otherFaceIds: Optional[list[str]] = None
    power: Optional[str] = None
    printings: Optional[list[str]] = None
    promoTypes: Optional[list[str]] = None
    purchaseUrls: PurchaseUrls
    rarity: str
    relatedCards: Optional[RelatedCards] = None
    rebalancedPrintings: Optional[list[str]] = None
    rulings: Optional[list[Rulings]] = None
    securityStamp: Optional[str] = None
    setCode: str
    side: Optional[str] = None
    signature: Optional[str] = None
    sourceProducts: Optional[SourceProducts] = None
    subsets: Optional[list[str]] = None
    subtypes: list[str] = []
    supertypes: list[str] = []
    text: Optional[str] = None
    toughness: Optional[str] = None
    type: str
    types: list[str] = []
    uuid: str
    variations: Optional[list[str]] = None
    watermark: Optional[str] = None


class CardSetDeck(Schema):
    """Model describing the properties of a single card found in a Deck (Set)."""
    count: float
    isFoil: Optional[bool] = None
    uuid: str


class CardToken(Schema):
    """Model describing the properties of a single token card found in a Set."""
    artist: Optional[str] = None
    artistIds: Optional[list[str]] = None
    asciiName: Optional[str] = None
    availability: list[str] = []
    boosterTypes: Optional[list[str]] = None
    borderColor: str
    cardParts: Optional[list[str]] = None
    colorIdentity: list[str] = []
    colorIndicator: Optional[list[str]] = None
    colors: list[str] = []
    faceName: Optional[str] = None
    faceFlavorName: Optional[str] = None
    finishes: list[str] = []
    flavorText: Optional[str] = None
    frameEffects: Optional[list[str]] = None
    frameVersion: str
    hasFoil: bool
    hasNonFoil: bool
    identifiers: Identifiers
    isFullArt: Optional[bool] = None
    isFunny: Optional[bool] = None
    isOnlineOnly: Optional[bool] = None
    isPromo: Optional[bool] = None
    isReprint: Optional[bool] = None
    isTextless: Optional[bool] = None
    keywords: Optional[list[str]] = None
    language: str
    layout: str
    loyalty: Optional[str] = None
    name: str
    number: str
    orientation: Optional[str] = None
    originalText: Optional[str] = None
    originalType: Optional[str] = None
    otherFaceIds: Optional[list[str]] = None
    power: Optional[str] = None
    promoTypes: Optional[list[str]] = None
    relatedCards: Optional[RelatedCards] = None
    reverseRelated: Optional[list[str]] = None
    securityStamp: Optional[str] = None
    setCode: str
    side: Optional[str] = None
    signature: Optional[str] = None
    sourceProducts: Optional[list[str]] = None
    subsets: Optional[list[str]] = None
    subtypes: list[str] = []
    supertypes: list[str] = []
    text: Optional[str] = None
    toughness: Optional[str] = None
    type: str
    types: list[str] = []
    uuid: str
    watermark: Optional[str] = None


"""
* Types
"""

Card = Union[CardAtomic, CardDeck, CardSet, CardSetDeck, CardToken]
