from dataclasses import dataclass
from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, Field, Extra # type: ignore


class CollectorsModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="id")
    name: str = Field(..., alias="name")
    host: str = Field(..., alias="host")
    port: int = Field(..., alias="port")
    interval_seconds: Literal[60, 300, 900, 1800, 3600] = Field(..., alias="intervalSeconds")
    enabled: Optional[bool] = Field(alias="enabled")


class Operator(BaseModel):
    id: int
    name: str
    logo: Optional["Logo"]
    radio_operator_id: int = Field(alias="radioOperatorId")
    notes: Optional[str]
    contact_person: Optional[str] = Field(alias="contactPerson")
    email: Optional[str]
    time_zone: str = Field(..., alias="timeZone")
    fcc_or_id: Optional[str] = Field(alias="fccOrId")
    sla_profiles: List["SlaProfile"] = Field(alias="slaProfiles")
    sas_provider: Optional[str] = Field(alias="sasProvider")
    custom_attribute_name1: Optional[str] = Field(alias="customAttributeName1")
    custom_attribute_name2: Optional[str] = Field(alias="customAttributeName2")
    software_tags: List[str] = Field(..., alias="softwareTags")
    preferred_bn_enabled: bool = Field(..., alias="preferredBnEnabled")
    auto_reconnect_to_preferred_bn_enabled: Optional[bool] = Field(alias="autoReconnectToPreferredBnEnabled")
    telemetry_collector_id: Optional[str] = Field(alias="telemetryCollectorId")
    telemetry_collector: Optional[CollectorsModel] = Field(alias="telemetryCollector")
    telemetry_enabled: Optional[bool] = Field(alias="telemetryEnabled")
    telemetry_collector_details: Optional[CollectorsModel] = Field(alias="telemetryCollectorDetails")


class Logo(BaseModel):
    url: Optional[str]
    data: Optional[str]


class SlaProfile(BaseModel):
    profile_id: str = Field(..., alias="profileId")
    name: str
    peak_burst_size: int = Field(..., alias="peakBurstSize")
    peak_rate_mbps: int = Field(..., alias="peakRateMbps")


Logo.update_forward_refs()
SlaProfile.update_forward_refs()
Operator.update_forward_refs()


@dataclass
class SectorAncestry:
    id: int
    name: int

    @staticmethod
    def from_dict(obj: Any) -> "SectorAncestry":
        _id = obj.get("id")
        _name = obj.get("name")
        return SectorAncestry(_id, _name)


@dataclass
class SiteAncestry:
    id: int
    name: str
    marketId: int
    marketName: str
    networkProfile: int
    notes: str
    contactPerson: str
    email: str
    address: str
    latitude: int
    longitude: int

    @staticmethod
    def from_dict(obj: Any) -> "SiteAncestry":
        _id = obj.get("id")
        _name = obj.get("name")
        _marketId = obj.get("marketId")
        _marketName = obj.get("marketName")
        _networkProfile = obj.get("networkProfile")
        _notes = obj.get("notes")
        _contactPerson = obj.get("contactPerson")
        _email = obj.get("email")
        _address = obj.get("address")
        _latitude = obj.get("latitude")
        _longitude = obj.get("longitude")
        return SiteAncestry(
            _id,
            _name,
            _marketId,
            _marketName,
            _networkProfile,
            _notes,
            _contactPerson,
            _email,
            _address,
            _latitude,
            _longitude,
        )


@dataclass
class CellAncestry:
    id: int
    name: int

    @staticmethod
    def from_dict(obj: Any) -> "CellAncestry":
        _id = obj.get("id")
        _name = obj.get("name")
        return CellAncestry(_id, _name)


@dataclass
class MarketAncestry:
    id: int
    name: str
    regionId: int
    regionName: str
    networkProfile: int
    notes: str
    contactPerson: str
    email: str

    @staticmethod
    def from_dict(obj: Any) -> "MarketAncestry":
        _id = obj.get("id")
        _name = obj.get("name")
        _regionId = obj.get("regionId")
        _regionName = obj.get("regionName")
        _networkProfile = obj.get("networkProfile")
        _notes = obj.get("notes")
        _contactPerson = obj.get("contactPerson")
        _email = obj.get("email")
        return MarketAncestry(
            _id, _name, _regionId, _regionName, _networkProfile, _notes, _contactPerson, _email
        )


@dataclass
class RegionAncestry:
    id: int
    name: str
    operatorId: int
    operatorName: str
    networkProfile: int
    notes: str
    contactPerson: str
    email: str
    regulatoryDomain: str
    regulatoryCountry: str

    @staticmethod
    def from_dict(obj: Any) -> "RegionAncestry":
        _id = obj.get("id")
        _name = obj.get("name")
        _operatorId = obj.get("operatorId")
        _operatorName = obj.get("operatorName")
        _networkProfile = obj.get("networkProfile")
        _notes = obj.get("notes")
        _contactPerson = obj.get("contactPerson")
        _email = obj.get("email")
        _regulatoryDomain = obj.get("regulatoryDomain")
        _regulatoryCountry = obj.get("regulatoryCountry")
        return RegionAncestry(
            _id,
            _name,
            _operatorId,
            _operatorName,
            _networkProfile,
            _notes,
            _contactPerson,
            _email,
            _regulatoryDomain,
            _regulatoryCountry,
        )


class RetailerModel(BaseModel):
    id: int = Field(alias="id")
    name: str = Field(alias="name")
    operator_id: int = Field(alias="operatorId")
    operator_name: str = Field(alias="operatorName")


class CarrierModel(BaseModel):
    frequency: Optional[int]
    channel_width: Optional[int] = Field(alias="channelWidth")
    enabled: Optional[bool]


class SectorModel(BaseModel):
    id: int = Field(alias="id")
    name: str = Field(alias="name")
    network_id: Optional[int] = Field(alias="networkId")
    cell_id: Optional[int] = Field(alias="cellId")
    cell_name: Optional[str] = Field(alias="cellName")
    radio_operator_id: Optional[int] = Field(alias="radioOperatorId")
    network_profile: Optional[Literal[1, 2, 5, 6]] = Field(alias="networkProfile")
    notes: Optional[str] = Field(alias="notes")
    svlan: Optional[str] = Field(default=None, alias="svlan")
    sla_classification_type: Literal["cos-inner", "dscp", ""] = Field(..., alias="slaClassificationType")
    carrier1: Optional["CarrierModel"]
    carrier2: Optional["CarrierModel"]
    rn_transmit_power: Optional[int] = Field(alias="rnTransmitPower")
    bn_transmit_power: Optional[int] = Field(alias="bnTransmitPower")
    preferred_bn_enabled: Optional[bool] = Field(alias="preferredBnEnabled")
    auto_reconnect_to_preferred_bn_enabled: Optional[bool] = Field(alias="autoReconnectToPreferredBnEnabled")
    dhcp_relay_agent_enabled: Optional[bool] = Field(alias="dhcpRelayAgentEnabled")
    circuit_identifier_type: Optional[Literal["MAC_ADDRESS", "SERIAL_NUMBER"]] = Field(
        alias="circuitIdentifierType"
    )
    telemetry_enabled: Optional[bool] = Field(alias="telemetryEnabled")
    telemetry_collector_details: Optional[CollectorsModel] = Field(alias="telemetryCollectorDetails")


class RegionModel(BaseModel):
    id: int = Field(..., alias="id")
    name: str
    operator_id: int = Field(..., alias="operatorId")
    operator_name: Optional[str] = Field(alias="operatorName")
    network_profile: Literal[1, 2, 5, 6] = Field(alias="networkProfile")
    notes: Optional[str]
    contact_person: Optional[str] = Field(alias="contactPerson")
    email: Optional[str]
    regulatory_domain: Literal["FCC"] = Field(alias="regulatoryDomain")
    regulatory_country: Literal["USA", "ZAF"] = Field(alias="regulatoryCountry")


class CellModel(BaseModel):
    id: int = Field(alias="id")
    name: str
    network_id: int = Field(alias="networkId")
    site_id: int = Field(alias="siteId")
    site_name: str = Field(alias="siteName")
    radio_set_id: int = Field(alias="radioSetId")
    notes: str
    network_profile: Optional[Literal[1, 2, 5, 6]] = Field(alias="networkProfile")
    band: str
    is_cbrs_cell: bool = Field(..., alias="isCbrsCell")


class MarketModel(BaseModel):
    id: int = Field(alias="id")
    name: str
    region_id: int = Field(alias="regionId")
    region_name: str = Field(alias="regionName")
    network_profile: Optional[int] = Field(alias="networkProfile")
    notes: str
    contact_person: str = Field(alias="contactPerson")
    email: str


class SiteModel(BaseModel):
    id: int = Field(alias="id")
    name: str
    market_id: int = Field(alias="marketId")
    market_name: str = Field(alias="marketName")
    address: Optional[str]
    latitude: int
    longitude: int
    network_profile: Optional[Literal[1, 2, 5, 6]] = Field(alias="networkProfile")
    notes: Optional[str]
    contact_person: Optional[str] = Field(alias="contactPerson")
    email: Optional[str]
    regulatory_domain: Optional[Literal["FCC"]] = Field(alias="regulatoryDomain")
    regulatory_country: Optional[Literal["USA", "ZAF"]] = Field(alias="regulatoryCountry")


class ConfigModel(BaseModel):
    # TODO: Need to add handling for custom attributes
    # Since their key name is not fixed it is little tricky
    # Refer: https://stackoverflow.com/questions/69617489/can-i-get-incoming-extra-fields-from-pydantic
    heightAgl: int = Field(default=None, alias="heightAgl")
    antennaAzimuth: int = Field(default=None, alias="antennaAzimuth")
    tilt: int = Field(default=None, alias="tilt")
    latitude: float = Field(default=None)
    hierarchy: "Hierarchy" = Field(default=None)
    first_seen_time_seconds: int = Field(default=None, alias="firstSeenTimeSeconds")
    retailer_id: int = Field(default=None, alias="retailerId")
    slaprofile: str = Field(default=None, alias="sla-profile")
    data_vlan: int = Field(default=None)
    hostname: str = Field(default=None)
    mac_address: str = Field(default=None, alias="macAddress")
    retailer_name: str = Field(default=None, alias="retailerName")
    connected_bn: Optional[str] = Field(default=None, alias="connectedBn")
    software_version: str = Field(default=None, alias="softwareVersion")
    longitude: float = Field(default=None)
    primary_bn: str = Field(default=None, alias="primaryBn")

    class Config:
        extra = Extra.allow


class Hierarchy(BaseModel):
    sector: "Cell_Market_Operator_Region_Sector_Site"
    cell: "Cell_Market_Operator_Region_Sector_Site"
    site: "Cell_Market_Operator_Region_Sector_Site"
    market: "Cell_Market_Operator_Region_Sector_Site"
    region: "Cell_Market_Operator_Region_Sector_Site"
    operator: "Cell_Market_Operator_Region_Sector_Site"


class Cell_Market_Operator_Region_Sector_Site(BaseModel):
    id_: int = Field(..., alias="id")
    name: str


class DeviceConfigModel(BaseModel):
    serial_no: str = Field(..., alias="serialNumber")
    config: "ConfigModel"


class BulkUpdateErrorModel(BaseModel):
    message: str
    code: int
    status: Optional[str]


class BulkUpdateSuccessModel(BaseModel):
    data: str


class BulkUpdateFailureModel(BaseModel):
    data: str
    error: BulkUpdateErrorModel


class BulkUpdateResponseModel(BaseModel):
    # In pydantic default values are implemented correctly and every instance gets its own copy
    success_list: List[BulkUpdateSuccessModel] = Field(default=[], alias="successList")
    failure_list: List[BulkUpdateFailureModel] = Field(default=[], alias="failureList")


class SectorDetail(BaseModel):
    id_: int = Field(..., alias="id")
    name: str
    network_id: int = Field(..., alias="networkId")
    dhcp_relay_agent_enabled: Optional[bool] = Field(alias="dhcpRelayAgentEnabled")


class CellDetail(BaseModel):
    id_: int = Field(..., alias="id")
    name: str
    network_id: int = Field(..., alias="networkId")
    is_cbrs_cell: bool = Field(..., alias="isCbrsCell")


class Site(BaseModel):
    id_: int = Field(..., alias="id")
    name: str
    latitude: Optional[int]
    longitude: Optional[int]


class Cell_Market_Operator_Region_Sector(BaseModel):
    id_: int = Field(..., alias="id")
    name: Union[int, str]


class Ancestry(BaseModel):
    sector: "Cell_Market_Operator_Region_Sector"
    sector_details: "SectorDetail" = Field(..., alias="sectorDetails")
    cell: "Cell_Market_Operator_Region_Sector"
    cell_details: "CellDetail" = Field(..., alias="cellDetails")
    site: "Site"
    market: "Cell_Market_Operator_Region_Sector"
    region: "Cell_Market_Operator_Region_Sector"
    operator: "Cell_Market_Operator_Region_Sector"


class Device(BaseModel):
    radioOperatorId: Optional[int] = Field(alias="radioOperatorId")
    networkProfile: Optional[int] = Field(alias="networkProfile")
    regulatoryDomain: Optional[str] = Field(alias="regulatoryDomain")
    regulatoryCountry: Optional[str] = Field(alias="regulatoryCountry")
    radioSetId: Optional[int] = Field(alias="radioSetId")
    radioCellId: Optional[int] = Field(alias="radioCellId")
    band: Optional[str]
    radioSectorId: Optional[int] = Field(alias="radioSectorId")
    slaClassificationType: Optional[str] = Field(alias="slaClassificationType")
    muteMode: Optional[bool] = Field(alias="muteMode")
    managementSubnetMask: Optional[int] = Field(alias="managementSubnetMask")

    id: str = Field(..., alias="id")
    serialNumber: str = Field(..., alias="serialNumber")
    macAddress: Optional[str] = Field(alias="macAddress")
    type_: str = Field(..., alias="type")
    sectorId: int = Field(..., alias="sectorId")
    retailerId: int = Field(..., alias="retailerId")
    retailerName: Optional[str] = Field(alias="retailerName")
    softwareVersion: Optional[str] = Field(alias="softwareVersion")
    ip: Optional[str] = Field(alias="ip")
    port: Optional[str]
    endpoints: "Endpoint"
    transportSecurity: bool = Field(..., alias="transportSecurity")
    authenticated: bool
    insecureMode: bool = Field(..., alias="insecureMode")
    masterId: Optional[str] = Field(alias="masterId")
    masterName: Optional[str] = Field(alias="masterName")
    installParams: Optional[dict] = Field(alias="installParams")
    bootTimeSeconds: int = Field(..., alias="bootTimeSeconds")
    uptimeSeconds: int = Field(..., alias="uptimeSeconds")
    losRange: Optional[float] = Field(alias="losRange")
    bootId: Optional[str] = Field(alias="bootId")
    lastUpdateTimeSeconds: int = Field(..., alias="lastUpdateTimeSeconds")
    connected: bool = Field(..., alias="connected")
    reachable: str = Field(..., alias="connected")
    linkState: Optional[str] = Field(alias="linkState")
    partNumber: Optional[str] = Field(alias="partNumber")
    loginBanner: Optional[str] = Field(alias="loginBanner")
    activeBank: Optional[str] = Field(alias="activeBank")
    currentBank: Optional[str] = Field(alias="currentBank")
    bootReason: Optional[str] = Field(alias="bootReason")
    rebootMessage: Optional[str] = Field(alias="rebootMessage")

    rfBoardSerialNumber: Optional[str] = Field(None, alias="rfBoardSerialNumber")
    rfBoardPartNumber: Optional[str] = Field(None, alias="rfBoardPartNumber")
    digiBoardSerialNumber: Optional[str] = Field(None, alias="digiBoardSerialNumber")
    digiBoardPartNumber: Optional[str] = Field(None, alias="digiBoardPartNumber")
    radioNetworkUp: Optional[bool] = Field(None, alias="radioNetworkUp")
    managementSubnet: Optional[str] = Field(None, alias="managementSubnet")
    svLan: Optional[str] = Field(None, alias="svLan")

    latitude: Optional[int] = None
    longitude: Optional[int] = None
    heightAgl: Optional[int] = Field(None, alias="heightAgl")
    antennaDowntilt: Optional[int] = Field(None, alias="antennaDowntilt")
    tilt: Optional[int] = None
    antennaAzimuth: Optional[int] = Field(None, alias="antennaAzimuth")
    rnTransmitPower: Optional[int] = Field(None, alias="rnTransmitPower")
    bnTransmitPower: Optional[int] = Field(None, alias="bnTransmitPower")
    preferredBnEnabled: Optional[bool] = Field(None, alias="preferredBnEnabled")
    autoReconnectToPreferredBnEnabled: Optional[bool] = Field(None, alias="autoReconnectToPreferredBnEnabled")
    preferredBnSearchTimeoutSeconds: Optional[int] = Field(None, alias="preferredBnSearchTimeoutSeconds")

    ancestry: "Ancestry"
    lastChangeReason: Optional[str] = Field(alias="lastChangeReason")
    lastChangeReasonMessage: Optional[str] = Field(alias="lastChangeReasonMessage")
    softwareBanks: List["SoftwareBank"] = Field(..., alias="softwareBanks")
    sectorName: str = Field(..., alias="sectorName")
    isOrphan: bool = Field(..., alias="isOrphan")
    configPushEnabled: bool = Field(..., alias="configPushEnabled")
    savedConfig: "DeviceSavedConfig" = Field(..., alias="savedConfig")
    configMismatch: bool = Field(..., alias="configMismatch")
    hostName: Optional[str] = Field(alias="hostName")
    carrier1: "CarrierModel"
    carrier2: "CarrierModel"
    slaProfile: Optional[str] = Field(alias="slaProfile")
    slaProfiles: Optional[List["SlaProfile"]] = Field([], alias="slaProfiles")
    dataVlan: Optional[int] = Field(alias="dataVlan")
    managementVlan: Optional[int] = Field(alias="managementVlan")
    notes: Optional[str]
    isCbrsDevice: bool = Field(..., alias="isCbrsDevice")
    cpiId: Optional[str] = Field(alias="cpiId")
    firstSeenTimeSeconds: int = Field(..., alias="firstSeenTimeSeconds")
    updatedBy: Optional[str] = Field(alias="updatedBy")
    bnPriorityList: Optional[List["BnPriorityList"]] = Field(alias="bnPriorityList")
    preferredBn: Optional[str] = Field(alias="preferredBn")
    lastDisconnectTimeNanos: Optional[int] = Field(alias="lastDisconnectTimeNanos")
    downDurationMillis: Optional[int] = Field(alias="downDurationMillis")
    excludeDurationMillis: Optional[int] = Field(alias="excludeDurationMillis")
    connectionUptimeSeconds: Optional[int] = Field(alias="connectionUptimeSeconds")
    dhcpRelayAgentEnabled: Optional[bool] = Field(alias="dhcpRelayAgentEnabled")
    remoteIdentifierType: Optional[Literal["MAC_ADDRESS", "SERIAL_NUMBER"]] = Field(
        alias="remoteIdentifierType"
    )
    circuitIdentifierType: Optional[Literal["MAC_ADDRESS", "SERIAL_NUMBER"]] = Field(
        alias="circuitIdentifierType"
    )
    version: int
    telemetryCollector: Optional[CollectorsModel] = Field(alias="telemetryCollector")
    telemetryEnabled: Optional[bool] = Field(alias="telemetryEnabled")


class SoftwareBank(BaseModel):
    name: str
    software_version: str = Field(..., alias="softwareVersion")


class Endpoint(BaseModel):
    grpc: "Grpc_Http_Ssh_Web"
    http: "Grpc_Http_Ssh_Web"
    web: "Grpc_Http_Ssh_Web"
    ssh: "Grpc_Http_Ssh_Web"


class Grpc_Http_Ssh_Web(BaseModel):
    ip: str = Field(default=None)
    port: int = Field(default=None)


class BnPriorityList(BaseModel):
    serial_number: str = Field(..., alias="serialNumber")
    preferred_network_id: str = Field(..., alias="preferredNetworkId")
    connected_time_seconds: int = Field(..., alias="connectedTimeSeconds")


@dataclass
class Sector:
    id: str
    name: str
    networkId: int
    cellId: int
    cellName: str
    radioOperatorId: int
    slaClassificationType: str

    @staticmethod
    def from_dict(obj: Any) -> "Sector":
        _id = obj.get("id")
        _name = obj.get("name")
        _networkId = obj.get("networkId")
        _cellId = obj.get("cellId")
        _cellName = obj.get("cellName")
        _radioOperatorId = obj.get("radioOperatorId")
        _slaClassificationType = obj.get("slaClassificationType")
        return Sector(_id, _name, _networkId, _cellId, _cellName, _radioOperatorId, _slaClassificationType)


@dataclass
class AutoUpgrade:
    id: str
    schedule: str
    durationMinutes: int
    timeZone: str
    disableAutoUpgrade: bool
    minBnSoftware: str
    minRnSoftware: str
    emailIds: List[str]
    operatorId: int
    regionId: int
    sectorId: int
    createdBy: str
    updatedBy: str
    createTimeMillis: int
    updateTimeMillis: int
    inherited: bool
    inheritedFrom: str

    @staticmethod
    def from_dict(obj: Any) -> "AutoUpgrade":
        _id = obj.get("id")
        _schedule = obj.get("schedule")
        _durationMinutes = obj.get("durationMinutes")
        _timeZone = obj.get("timeZone")
        _disableAutoUpgrade = obj.get("disableAutoUpgrade")
        _minBnSoftware = obj.get("minBnSoftware")
        _minRnSoftware = obj.get("minRnSoftware")
        _emailIds = obj.get("emailIds")
        _operatorId = obj.get("operatorId")
        _regionId = obj.get("regionId")
        _sectorId = obj.get("sectorId")
        _createdBy = obj.get("createdBy")
        _updatedBy = obj.get("updatedBy")
        _createTimeMillis = obj.get("createTimeMillis")
        _updateTimeMillis = obj.get("updateTimeMillis")
        _inherited = obj.get("inherited")
        _inheritedFrom = obj.get("inheritedFrom")
        return AutoUpgrade(
            _id,
            _schedule,
            _durationMinutes,
            _timeZone,
            _disableAutoUpgrade,
            _minBnSoftware,
            _minRnSoftware,
            _emailIds,
            _operatorId,
            _regionId,
            _sectorId,
            _createdBy,
            _updatedBy,
            _createTimeMillis,
            _updateTimeMillis,
            _inherited,
            _inheritedFrom,
        )


@dataclass
class PolicySector:
    id: int
    name: str
    networkId: int
    cellId: int
    cellName: str
    radioOperatorId: int
    networkProfile: int
    notes: str
    svLan: str
    slaClassificationType: str
    carrier1: dict
    carrier2: dict
    rnTransmitPower: int
    bnTransmitPower: int
    preferredBnEnabled: bool

    @staticmethod
    def from_dict(obj: Any) -> "PolicySector":
        _id = obj.get("id")
        _name = obj.get("name")
        _networkId = obj.get("networkId")
        _cellId = obj.get("cellId")
        _cellName = obj.get("cellName")
        _radioOperatorId = obj.get("radioOperatorId")
        _networkProfile = obj.get("networkProfile")
        _notes = obj.get("notes")
        _svLan = obj.get("svLan")
        _slaClassificationType = obj.get("slaClassificationType")
        _carrier1 = obj.get("carrier1")
        _carrier2 = obj.get("carrier2")
        _rnTransmitPower = obj.get("rnTransmitPower")
        _bnTransmitPower = obj.get("bnTransmitPower")
        _preferredBnEnabled = obj.get("preferredBnEnabled")
        return PolicySector(
            _id,
            _name,
            _networkId,
            _cellId,
            _cellName,
            _radioOperatorId,
            _networkProfile,
            _notes,
            _svLan,
            _slaClassificationType,
            _carrier1,
            _carrier2,
            _rnTransmitPower,
            _bnTransmitPower,
            _preferredBnEnabled,
        )


class DeviceSavedConfig(BaseModel):
    hostname: Optional[str] = Field(alias="hostName")
    mutemode: Optional[bool] = Field(alias="muteMode")
    sla_profile: Optional[str] = Field(alias="slaProfile")
    management_subnet: Optional[str] = Field(alias="managementSubnet")
    latitude: Optional[int] = Field(alias="latitude")
    longitude: Optional[int] = Field(alias="longitude")
    height_agl: Optional[int] = Field(alias="heightAgl")
    antenna_down_tilt: Optional[int] = Field(alias="antennaDowntilt")
    tilt: Optional[int] = Field(alias="tilt")
    antenna_azimuth: Optional[int] = Field(alias="antennaAzimuth")
    data_vlan: Optional[int] = Field(alias="dataVlan")
    preferred_bn: Optional[str] = Field(alias="preferredBn")
    cpi_id: Optional[str] = Field(alias="cpiId")


ConfigModel.update_forward_refs()
SectorModel.update_forward_refs()
Hierarchy.update_forward_refs()
Cell_Market_Operator_Region_Sector_Site.update_forward_refs()
BnPriorityList.update_forward_refs()
Grpc_Http_Ssh_Web.update_forward_refs()
Endpoint.update_forward_refs()
SoftwareBank.update_forward_refs()
DeviceSavedConfig.update_forward_refs()
Device.update_forward_refs()


class BulkDeleteFailureSuccessModel(BaseModel):
    data: str
    error: Optional["Error"] = None


class Error(BaseModel):
    code: int
    message: str
    status: Optional[str]


BulkDeleteFailureSuccessModel.update_forward_refs()


class SetPreferredBNFailureSuccessModel(BaseModel):
    data: "SetPreferredBnModel"
    error: Optional["Error"] = None


class SetPreferredBnModel(BaseModel):
    rn_serial_number: str = Field(..., alias="rnSerialNumber")
    preferred_bn: str = Field(..., alias="preferredBn")


SetPreferredBNFailureSuccessModel.update_forward_refs()

from typing import Type, List, Dict, Tuple, Union, Optional,get_type_hints

from faker import Faker
from pydantic import BaseModel

import dataclasses

fake = Faker()

def generate_fake_data(cls):
    fake_data = {}
    type_hints = get_type_hints(cls)
    for attribute_name in type_hints:
        attribute_type = type_hints[attribute_name]
        if attribute_type == str:
            fake_data[attribute_name] = fake.word()
        elif attribute_type == int:
            fake_data[attribute_name] = fake.random_int()
        elif attribute_type == float:
            fake_data[attribute_name] = fake.pyfloat()
        elif attribute_type == bool:
            fake_data[attribute_name] = fake.boolean()
        elif attribute_type == List[str]:
            fake_data[attribute_name] = [fake.word() for _ in range(3)]
        elif attribute_type == List[int]:
            fake_data[attribute_name] = [fake.random_int() for _ in range(3)]
        elif attribute_type == List[float]:
            fake_data[attribute_name] = [fake.pyfloat() for _ in range(3)]
        elif attribute_type == List[bool]:
            fake_data[attribute_name] = [fake.boolean() for _ in range(3)]
        elif attribute_type == Dict[str, str]:
            fake_data[attribute_name] = {fake.word(): fake.word() for _ in range(3)}
        elif attribute_type == Dict[str, int]:
            fake_data[attribute_name] = {fake.word(): fake.random_int() for _ in range(3)}
        elif attribute_type == Dict[str, float]:
            fake_data[attribute_name] = {fake.word(): fake.pyfloat() for _ in range(3)}
        elif attribute_type == Dict[str, bool]:
            fake_data[attribute_name] = {fake.word(): fake.boolean() for _ in range(3)}
        elif dataclasses.is_dataclass(attribute_type):
            fake_data[attribute_name] = generate_fake_data(attribute_type)
    return cls(**fake_data)


def generate_fake_data_from_pydentic(model_class: Type[BaseModel]) -> BaseModel:
    fake_data = {}
    for field in model_class.__fields__.values():
        field_type = field.type_
        if field_type is int:
            fake_data[field.name] = fake.random_int()
        elif field_type is float:
            fake_data[field.name] = fake.pyfloat()
        elif field_type is str:
            fake_data[field.name] = fake.word()
        elif field_type is bool:
            fake_data[field.name] = fake.boolean()
        elif issubclass(field_type, BaseModel):
            fake_data[field.name] = generate_fake_data_from_pydentic(field_type)
        elif field_type is List[int]:
            fake_data[field.name] = [fake.random_int() for _ in range(3)]
        elif field_type is List[float]:
            fake_data[field.name] = [fake.pyfloat() for _ in range(3)]
        elif field_type is List[str]:
            fake_data[field.name] = [fake.word() for _ in range(3)]
        elif field_type is List[bool]:
            fake_data[field.name] = [fake.boolean() for _ in range(3)]
        elif field_type.__origin__ is list:
            inner_type = field_type.__args__[0]
            fake_data[field.name] = [generate_fake_data_from_pydentic(inner_type) for _ in range(3)]
        elif field_type is Dict[str, int]:
            fake_data[field.name] = {fake.word(): fake.random_int() for _ in range(3)}
        elif field_type is Dict[str, float]:
            fake_data[field.name] = {fake.word(): fake.pyfloat() for _ in range(3)}
        elif field_type is Dict[str, str]:
            fake_data[field.name] = {fake.word(): fake.word() for _ in range(3)}
        elif field_type is Dict[str, bool]:
            fake_data[field.name] = {fake.word(): fake.boolean() for _ in range(3)}
        elif field_type.__origin__ is dict:
            key_type, value_type = field_type.__args__
            fake_data[field.name] = {generate_fake_data_from_pydentic(key_type): generate_fake_data_from_pydentic(value_type) for _ in range(3)}
        elif field_type is Tuple[int, str]:
            fake_data[field.name] = (fake.random_int(), fake.word())
        elif field_type is Tuple[int, str, bool]:
            fake_data[field.name] = (fake.random_int(), fake.word(), fake.boolean())
        elif field_type is Tuple[int, str, bool, float]:
            fake_data[field.name] = (fake.random_int(), fake.word(), fake.boolean(), fake.pyfloat())
        elif field_type.__origin__ is tuple:
            inner_types = field_type.__args__
            fake_data[field.name] = tuple(generate_fake_data_from_pydentic(inner_type) for inner_type in inner_types)
        elif field_type is Union[int, str]:
            fake_data[field.name] = fake.random_element([fake.random_int(), fake.word()])
        elif field_type is Optional[int]:
            fake_data[field.name] = fake.random_element([fake.random_int(), None])
        elif field_type.__origin__ is Union:
            inner_types = field_type.__args__
            fake_data[field.name] = fake.random_element([generate_fake_data_from_pydentic(inner_type) for inner_type in inner_types])
    return model_class(**fake_data)


fake_d = generate_fake_data_from_pydentic(Device)
print(fake_d)
