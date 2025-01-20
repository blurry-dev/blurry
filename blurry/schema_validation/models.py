"""
Partial Schema.org types adjusted to match Google structured data specifications:

https://developers.google.com/search/docs/appearance/structured-data/search-gallery
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import AnyUrl
from pydantic import BaseModel
from pydantic import Field


Boolean = Literal["True"] | Literal["False"]


class FamilyFriendlyMixin:
    isFamilyFriendly: Boolean | None = None


class Thing(BaseModel):
    type_: str = Field(default="Thing", alias="@type", frozen=True)
    additionalType: str | None = None
    alternateName: str | None = None
    description: str | None = None
    disambiguatingDescription: str | None = None
    # identifier: PropertyValue | str | None = None
    image: ImageObject | str | None = None
    mainEntityOfPage: CreativeWork | str | None = None
    name: str | None = None
    # potentialAction: Action | None = None
    sameAs: str | None = None
    # subjectOf: CreativeWork | Event | None = None
    url: AnyUrl | None = None  # url is required but is added dynamically by Blurry


class Intangible(Thing):
    type_: str = Field(default="Intangible", alias="@type", frozen=True)


class Quantity(Intangible):
    type_: str = Field(default="Quantity", alias="@type", frozen=True)


class Duration(Quantity):
    type_: str = Field(default="Duration", alias="@type", frozen=True)


class ListItem(Thing):
    type_: str = Field(default="ListItem", alias="@type", frozen=True)
    item: Thing
    nextItem: ListItem | None = None
    position: int | str | None = None
    previousItem: ListItem | None = None


class ItemList(Intangible):
    type_: str = Field(default="ItemList", alias="@type", frozen=True)
    itemListElement: list[ListItem | str | Thing]


class Enumeration(Intangible):
    type_: str = Field(default="Enumeration", alias="@type", frozen=True)


class StructuredValue(Intangible):
    type_: str = Field(default="StructuredValue", alias="@type", frozen=True)


class GeoMixin:
    address: PostalAddress | str | None = None
    addressCountry: Country | str | None = None
    elevation: str | int | None = None
    postalCode: str | None = None


class GeoCoordinates(Intangible, GeoMixin):
    type_: str = Field(default="GeoCoordinates", alias="@type", frozen=True)
    latitude: float | str | None = None
    longitude: float | str | None = None


class GeoShape(Intangible, GeoMixin):
    type_: str = Field(default="GeoShape", alias="@type", frozen=True)
    box: str | None = None
    circle: str | None = None
    line: str | None = None
    polygon: str | None = None


class OpeningHoursSpecification(Intangible):
    type_: str = Field(default="OpeningHoursSpecification", alias="@type", frozen=True)
    # closes: Time
    # dayOfWeek: DayOfWeek
    # opens: Time
    validFrom: datetime | None = None
    validThrough: datetime | None = None


class ContactPoint(Intangible):
    type_: str = Field(default="ContactPoint", alias="@type", frozen=True)
    contactType: str | None = None
    email: str | None = None
    faxNumber: str | None = None
    # hoursAvailable: OpeningHoursSpecification | None = None
    productSupported: Product | str | None = None
    telephone: str | None = None


class PostalAddress(ContactPoint):
    type_: str = Field(default="PostalAddress", alias="@type", frozen=True)
    addressCountry: Country | str
    addressLocality: str
    addressRegion: str
    postOfficeBoxNumber: str | None = None
    postalCode: str
    streetAddress: str


class Rating(Intangible):
    type_: str = Field(default="Rating", alias="@type", frozen=True)
    author: Organization | Person | None = None
    bestRating: int | str | None = None
    ratingExplanation: str | None = None
    ratingValue: int | float | str
    reviewAspect: str | None = None
    worstRating: int | str | None = None


class AggregateRating(Rating):
    type_: str = Field(default="AggregateRating", alias="@type", frozen=True)
    itemReviewed: Thing
    ratingCount: int
    reviewCount: int | None = None


class Specialty(Enumeration):
    type_: str = Field(default="Specialty", alias="@type", frozen=True)


class SpeakableSpecification(Intangible):
    type_: str = Field(default="SpeakableSpecification", alias="@type", frozen=True)
    cssSelector: str | None = None
    xpath: str | None = None


class Place(Thing):
    type_: str = Field(default="Place", alias="@type", frozen=True)
    address: PostalAddress | str
    geo: GeoCoordinates | GeoShape | None = None
    publicAccess: Boolean | None = None
    smokingAllowed: Boolean | None = None


class AdministrativeArea(Place):
    type_: str = Field(default="AdministrativeArea", alias="@type", frozen=True)


class Country(Place):
    type_: str = Field(default="Country", alias="@type", frozen=True)


class Product(Thing, FamilyFriendlyMixin):
    type_: str = Field(default="Product", alias="@type", frozen=True)
    # additionalProperty = PropertyValue | None = None
    aggregateRating: AggregateRating | None = None
    asin: str | None = None
    # audience: Audience | None = None
    award: str | None = None
    brand: Brand | Organization | None = None
    # category: CategoryCode | PhysicalActivityCategory | str | Thing | None = None
    color: str | None = None
    colorSwatch: ImageObject | str | None = None
    countryOfAssembly: str | None = None
    countryOfLastProcessing: str | None = None
    countryOfOrigin: Country | None = None
    # depth: Distance | QuantitiveValue | None = None
    # funding: Grant | None = None
    gtin: str | None = None
    gtin12: str | None = None
    gtin13: str | None = None
    gtin14: str | None = None
    gtin8: str | None = None
    # hasAdultConsideration: AdultOrientedEnumeration | None = None
    # hasCertification: Certification | list[Certification] | None
    logo: ImageObject | None = None
    productID: str | None = None
    sku: str | None = None
    slogan: str | None = None
    review: Review | None = None


class Person(Thing):
    type_: str = Field(default="Person", alias="@type", frozen=True)
    additionalName: str | None = None
    affiliation: Organization | None = None
    # agentInteractionStatistic: InteractionCounter | None = None
    email: str | None = None
    familyName: str | None = None
    givenName: str | None = None
    honorificPrefix: str | None = None
    honorificSuffix: str | None = None
    name: str  # pyright: ignore
    telephone: str | None = None
    worksFor: Organization | None = None


class Organization(Intangible):
    type_: str = Field(default="Organization", alias="@type", frozen=True)
    name: str  # pyright: ignore


class LocalBusiness(Organization, Place):
    type_: str = Field(default="LocalBusiness", alias="@type", frozen=True)
    currenciesAccepted: str | None = None
    name: str  # pyright: ignore
    openingHours: OpeningHoursSpecification | None = None
    paymentAccepted: str | None = None
    address: PostalAddress | str
    priceRange: str | None = None


class FoodEstablishment(LocalBusiness):
    type_: str = Field(default="FoodEstablishment", alias="@type", frozen=True)
    acceptsReservations: AnyUrl | Boolean
    # hasMenu: Menu | AnyUrl | Boolean
    servesCuisine: str
    starRating: Rating | None = None


class Restaurant(LocalBusiness):
    type_: str = Field(default="FoodEstablishment", alias="@type", frozen=True)


class Brand(Thing):
    type_: str = Field(default="Brand", alias="@type", frozen=True)
    aggregateRating: AggregateRating | None = None
    logo: ImageObject | str | None = None
    review: Review | None = None
    slogan: str | None = None


class CreativeWork(Thing, FamilyFriendlyMixin):
    type_: str = Field(default="CreativeWork", alias="@type", frozen=True)
    abstract: str | None = None
    accessMode: str | None = None
    accessModeSufficient: ItemList | None = None
    accessibilityAPI: str | None = None
    accessibilityControl: str | None = None
    accessibilityFeature: str | None = None
    accessibilityHazard: str | None = None
    accessibilitySummary: str | None = None
    accountablePerson: Person | None = None
    acquireLicensePage: CreativeWork | str | None = None
    aggregateRating: AggregateRating | None = None
    alternativeHeadline: str | None = None
    archivedAt: str | WebPage | None = None
    # assesses: DefinedTerm  or Text
    associatedMedia: MediaObject | None = None
    # audience: Audience | None = None
    # audio: AudioObject | Clip | MusicRecording | None = None
    author: Organization | Person | None = None
    award: str | None = None
    character: Person | None = None
    citation: CreativeWork | str | None = None
    # comment: Comment | None = None
    commentCount: int | None = None
    conditionsOfAccess: str | None = None
    # contentLocation: Place | None = None
    contentRating: Rating | str | None = None
    contentReferenceTime: datetime | None = None
    contributor: Organization | Person | None = None
    copyrightHolder: Organization | Person | None = None
    copyrightNotice: str | None = None
    copyrightYear: int | None = None
    # correction: CorrectionComment | str | None = None
    countryOfOrigin: Country | None = None
    # creativeWorkStatus: DefinedTerm | str | None = None
    creator: Organization | Person | None = None
    creditText: str | None = None
    dateCreated: datetime | None = None
    dateModified: datetime | None = None
    datePublished: datetime | None = None
    # digitalSourceType: IPTCDigitalSourceEnumeration | None = None
    discussionUrl: AnyUrl | None = None
    editEIDR: str | None = None
    editor: Person | None = None
    # educationalAlignment: AlignmentObject | None = None
    # educationalLevel: DefinedTerm | str | None = None
    # educationalUse: DefinedTerm | str | None = None
    encoding: MediaObject | None = None
    encodingFormat: str | None = None
    exampleOfWork: CreativeWork | None = None
    # expires: Date or DateTime | None = None
    funder: Organization | Person | None = None
    genre: str | None = None
    hasPart: CreativeWork | str | None = None
    headline: str | None = None
    # inLanguage: Language | str | None = None
    # interactionStatistic: InteractionCounter | None = None
    interactivityType: str | None = None
    # interpretedAsClaim: Claim | None = None
    isAccessibleForFree: Boolean | None = None
    isBasedOn: CreativeWork | Product | str | None = None
    isPartOf: CreativeWork | str | None = None
    # keywords: DefinedTerm | str | None = None
    # learningResourceType: DefinedTerm | str | None = None
    license: CreativeWork | str | None = None
    # locationCreated: Place | None = None
    mainEntity: Thing | list[Thing] | None = None
    maintainer: Organization | Person | None = None
    material: Product | str | None = None
    # materialExtent: QuantitativeValue | str | None = None
    mentions: Thing | None = None
    # offers: Demand | Offer | list[Demand | Offer] | None = None
    # pattern: DefinedTerm | str | None = None
    position: int | str | None = None
    producer: Organization | Person | None = None
    provider: Organization | Person | None = None
    # publication: PublicationEvent | None = None
    publisher: Organization | Person | None = None
    publisherImprint: Organization | None = None
    publishingPrinciples: CreativeWork | str | None = None
    # recordedAt: Event | None = None
    # releasedEvent: PublicationEvent | None = None
    review: Review | None = None
    schemaVersion: str | None = None
    # sdDatePublished
    # sdLicense
    # sdPublisher
    # size
    sourceOrganization: Organization | None = None
    # spatial: Place | None = None
    # spatialCoverage: Place | None = None
    sponsor: Organization | Person | None = None
    # teaches: DefinedTerm | str | None = None
    temporal: datetime | str | None = None
    temporalCoverage: datetime | str | None = None
    text: str | None = None
    thumbnail: ImageObject | None = None
    thumbnailUrl: AnyUrl | None = None
    # timeRequired: Duration | None = None
    translationOfWork: CreativeWork | None = None
    translator: Organization | Person | None = None
    typicalAgeRange: str | None = None
    usageInfo: CreativeWork | str | None = None
    version: int | float | str | None = None
    # video: Clip | VideoObject | None = None
    workExample: CreativeWork | None = None
    workTranslation: CreativeWork | None = None


class MediaObject(CreativeWork):
    type_: str = Field(default="MediaObject", alias="@type", frozen=True)
    associatedArticle: NewsArticle | None = None
    bitrate: str | None = None
    contentSize: str | None = None
    contentUrl: AnyUrl | None = None
    # duration: Duration | None = None
    embedUrl: AnyUrl | None = None
    encodesCreativeWork: CreativeWork | None = None
    encodingFormat: str | None = None
    # endTime: DateTime or Time | None = None
    # height: Distance or QuantitativeValue | None = None
    # ineligibleRegion: GeoShape or Place or Text | None = None
    # interpretedAsClaim: Claim | None = None
    playerType: str | None = None
    productionCompany: Organization | None = None
    # regionsAllowed: Place | list[Place] | None = None
    # requiresSubscription: Boolean | MediaSubscription | None = None
    sha256: str | None = None
    # startTime: DateTime or Time | None = None
    # uploadDate: DateTime or Time | None = None
    # height: Distance  or QuantitativeValue | None = None


class ImageObject(MediaObject):
    type_: str = Field(default="ImageObject", alias="@type", frozen=True)
    caption: MediaObject | str | None = None
    embeddedTextCaption: str | None = None
    # exifData: PropertyValue | Text | None
    representativeOfPage: Boolean | None = None


class WebSite(CreativeWork):
    type_: str = Field(default="WebSite", alias="@type", frozen=True)
    issn: str | None = None


class WebContent(CreativeWork):
    type_: str = Field(default="WebContent", alias="@type", frozen=True)


class Article(CreativeWork):
    type_: str = Field(default="Article", alias="@type", frozen=True)
    author: Organization | Person  # pyright: ignore to narrow the type
    datePublished: datetime  # pyright: ignore to narrow the type
    headline: str  # pyright: ignore to narrow the type
    image: ImageObject | str | list[ImageObject | str]  # pyright: ignore to permit Google's recommendation


class Blog(CreativeWork):
    type_: str = Field(default="Blog", alias="@type", frozen=True)
    blogPost: BlogPosting | None = None
    issn: str | None = None


class Comment(CreativeWork):
    type_: str = Field(default="Comment", alias="@type", frozen=True)


class HowTo(CreativeWork):
    type_: str = Field(default="HowTo", alias="@type", frozen=True)
    # estimatedCost: MonetaryAmount | str | None = None
    # performTime: Duration | None = None
    # prepTime: Duration | None = None
    # step: CreativeWork | HowToSection | HowToStep | str
    # supply: HowToSupply | str
    # tool: HowToTool | str
    # totalTime: Duration | None = None
    # yield: QuantitativeValue | str | None = None


class Recipe(HowTo):
    type_: str = Field(default="Recipe", alias="@type", frozen=True)
    # cookTime: Duration | None = None
    cookingMethod: str | None = None
    image: ImageObject | str  # pyright: ignore
    name: str  # pyright: ignore
    # nutrition: NutritionInformation
    recipeCategory: str
    recipeCuisine: str
    recipeIngredient: str | list[str]
    # recipeInstructions: CreativeWork | ItemList | str | list[HowToStep] | list[HowToSection]
    # recipeYield: QuantitativeValue | str = None
    # suitableForDiet: RestrictedDiet | None = None


class Question(Comment):
    type_: str = Field(default="Question", alias="@type", frozen=True)
    acceptedAnswer: Answer | ItemList
    answerCount: int | None = None
    eduQuestionType: str | None = None
    name: str  # pyright: ignore
    parentItem: Comment | CreativeWork | None = None
    suggestedAnswer: Answer | ItemList | None = None


class Answer(Comment):
    answerExplanation: Comment | WebContent
    parentItem: Comment | CreativeWork | None = None
    text: str  # pyright: ignore


class NewsArticle(Article):
    type_: str = Field(default="NewsArticle", alias="@type", frozen=True)
    dateline: str | None = None
    printColumn: str | None = None
    printEdition: str | None = None
    printPage: str | None = None
    printSection: str | None = None


class SocialMediaPosting(Article):
    type_: str = Field(default="SocialMediaPosting", alias="@type", frozen=True)
    sharedContent: CreativeWork | None = None


class BlogPosting(SocialMediaPosting):
    type_: str = Field(default="BlogPosting", alias="@type", frozen=True)


class WebPageElement(CreativeWork):
    type_: str = Field(default="WebPageElement", alias="@type", frozen=True)
    cssSelector: str | None = None
    xpath: str | None = None


class WebPage(CreativeWork):
    type_: str = Field(default="WebPage", alias="@type", frozen=True)
    # breadcrumb: BreadcrumbList | Text | None
    lastReviewed: datetime | None = None
    mainContentOfPage: WebPageElement | None = None
    primaryImageOfPage: ImageObject | None = None
    relatedLink: str | None = None
    reviewedBy: Organization | Person | None = None
    significantLink: str | None = None
    speakable: SpeakableSpecification | None = None
    specialty: Specialty | None = None


class AboutPage(WebPage):
    type_: str = Field(default="AboutPage", alias="@type", frozen=True)


class ContactPage(WebPage):
    type_: str = Field(default="ContactPage", alias="@type", frozen=True)


class CheckoutPage(WebPage):
    type_: str = Field(default="CheckoutPage", alias="@type", frozen=True)


class CollectionPage(WebPage):
    type_: str = Field(default="CollectionPage", alias="@type", frozen=True)


class FAQPage(WebPage):
    type_: str = Field(default="FAQPage", alias="@type", frozen=True)
    mainEntity: list[Question]  # pyright: ignore for Google compatibility


class ItemPage(WebPage):
    type_: str = Field(default="ItemPage", alias="@type", frozen=True)


class ProfilePage(WebPage):
    type_: str = Field(default="ProfilePage", alias="@type", frozen=True)
    mainEntity: Person | Organization  # pyright: ignore


class QAPage(WebPage):
    type_: str = Field(default="QAPage", alias="@type", frozen=True)


class SearchResultsPage(WebPage):
    type_: str = Field(default="SearchResultsPage", alias="@type", frozen=True)


class SoftwareApplication(CreativeWork):
    type_: str = Field(default="SoftwareApplication", alias="@type", frozen=True)
    applicationCategory: str | None = None
    applicationSubCategory: str | None = None
    applicationSuite: str | None = None
    availableOnDevice: str | None = None
    countriesNotSupported: str | None = None
    countriesSupported: str | None = None
    downloadUrl: AnyUrl | None = None
    featureList: str | None = None
    fileSize: str | None = None
    installUrl: AnyUrl | None = None
    memoryRequirements: str | None = None
    operatingSystem: str | None = None
    permissions: str | None = None
    processorRequirements: str | None = None
    releaseNotes: str | None = None
    screenshot: ImageObject | str | None = None
    softwareAddon: SoftwareApplication | None = None
    softwareHelp: CreativeWork | None = None
    softwareRequirements: str | None = None
    softwareVersion: str | None = None
    storageRequirements: str | None = None
    # supportingData: DataFeed | None = None


class WebApplication(SoftwareApplication):
    type_: str = Field(default="WebApplication", alias="@type", frozen=True)
    browserRequirements: str | None


class Review(CreativeWork):
    type_: str = Field(default="Review", alias="@type", frozen=True)
    associatedClaimReview: Review | None = None
    associatedMediaReview: Review | None = None
    associatedReview: Review | None = None
    itemReviewed: Thing | None = None
    negativeNotes: ItemList | ListItem | str | WebContent | None = None
    positiveNotes: ItemList | ListItem | str | WebContent | None = None
    reviewAspect: str | None = None
    reviewBody: str | None = None
    reviewRating: Rating
