"""Definition class."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

from .exceptions import HttpRequestError, ServiceNotFoundError, TimeoutExceededError
from .util import get_attr, retry, set_attr

if TYPE_CHECKING:
    from .services import AudiService


_LOGGER = logging.getLogger(__name__)


class VehicleDataResponse:
    """Status class."""

    IDS = {
        "0x0": "UNKNOWN",
        "0x0101010001": "UTC_TIME",
        "0x0101010002": "UTC_TIME_AND_KILOMETER_STATUS",
        "0x0202": "ACTIVE_INSTRUMENT_CLUSTER_WARNING",
        "0x0203010001": "MAINTENANCE_INTERVAL_DISTANCE_TO_OIL_CHANGE",
        "0x0203010002": "MAINTENANCE_INTERVAL_TIME_TO_OIL_CHANGE",
        "0x0203010003": "MAINTENANCE_INTERVAL_DISTANCE_TO_INSPECTION",
        "0x0203010004": "MAINTENANCE_INTERVAL_TIME_TO_INSPECTION",
        "0x0203010005": "WARNING_OIL_CHANGE",
        "0x0203010006": "MAINTENANCE_INTERVAL_ALARM_INSPECTION",
        "0x0203010007": "MAINTENANCE_INTERVAL_MONTHLY_MILEAGE",
        "0x0204040001": "OIL_LEVEL_AMOUNT_IN_LITERS",
        "0x0204040002": "OIL_LEVEL_MINIMUM_WARNING",
        "0x0204040003": "OIL_LEVEL_DIPSTICKS_PERCENTAGE",
        "0x0204040004": "OIL_DISPLAY",
        "0x0204040005": "OIL_LEVEL_VALID",
        "0x0204040006": "OIL_LEVEL_PERCENTAGE",
        "0x02040C0001": "ADBLUE_RANGE",
        "0x02040C0002": "SRC_NO_DRIVEABILITY",
        "0x0301010001": "LIGHT_STATUS",
        "0x0301020001": "TEMPERATURE_OUTSIDE",
        "0x0301030001": "BRAKING_STATUS",
        "0x0301030002": "STATE_OF_CHARGE",
        "0x0301030003": "BEM_OK",
        "0x0301030005": "TOTAL_RANGE",
        "0x0301030006": "PRIMARY_RANGE",
        "0x0301030007": "PRIMARY_DRIVE",
        "0x0301030008": "SECONDARY_RANGE",
        "0x0301030009": "SECONDARY_DRIVE",
        "0x030103000A": "TANK_LEVEL_IN_PERCENTAGE",
        "0x030103000D": "TANK_LEVEL_ERROR",
        "0x0301040001": "LOCK_STATE_LEFT_FRONT_DOOR",
        "0x0301040002": "OPEN_STATE_LEFT_FRONT_DOOR",
        "0x0301040003": "SAFETY_STATE_LEFT_FRONT_DOOR",
        "0x0301040004": "LOCK_STATE_LEFT_REAR_DOOR",
        "0x0301040005": "OPEN_STATE_LEFT_REAR_DOOR",
        "0x0301040006": "SAFETY_STATE_LEFT_REAR_DOOR",
        "0x0301040007": "LOCK_STATE_RIGHT_FRONT_DOOR",
        "0x0301040008": "OPEN_STATE_RIGHT_FRONT_DOOR",
        "0x0301040009": "SAFETY_STATE_RIGHT_FRONT_DOOR",
        "0x030104000A": "LOCK_STATE_RIGHT_REAR_DOOR",
        "0x030104000B": "OPEN_STATE_RIGHT_REAR_DOOR",
        "0x030104000C": "SAFETY_STATE_RIGHT_REAR_DOOR",
        "0x030104000D": "LOCK_STATE_TRUNK_LID",
        "0x030104000E": "OPEN_STATE_TRUNK_LID",
        "0x030104000F": "SAFETY_STATE_TRUNK_LID",
        "0x0301040010": "LOCK_STATE_HOOD",
        "0x0301040011": "OPEN_STATE_HOOD",
        "0x0301040012": "SAFETY_STATE_HOOD",
        "0x0301050001": "STATE_LEFT_FRONT_WINDOW",
        "0x0301050002": "POSITION_LEFT_FRONT_WINDOW",
        "0x0301050003": "STATE_LEFT_REAR_WINDOW",
        "0x0301050004": "POSITION_LEFT_REAR_WINDOW",
        "0x0301050005": "STATE_RIGHT_FRONT_WINDOW",
        "0x0301050006": "POSITION_RIGHT_FRONT_WINDOW",
        "0x0301050007": "STATE_RIGHT_REAR_WINDOW",
        "0x0301050008": "POSITION_RIGHT_REAR_WINDOW",
        "0x0301050009": "STATE_DECK",
        "0x030105000A": "POSITION_DECK",
        "0x030105000B": "STATE_SUN_ROOF_MOTOR_COVER",
        "0x030105000C": "POSITION_SUN_ROOF_MOTOR_COVER",
        "0x030105000D": "STATE_SUN_ROOF_REAR_MOTOR_COVER_3",
        "0x030105000E": "POSITION_SUN_ROOF_REAR_MOTOR_COVER_3",
        "0x030105000F": "STATE_SERVICE_FLAP",
        "0x0301050011": "STATE_SPOILER",
        "0x0301050012": "POSITION_SPOILER",
        "0x0301060001": "TYRE_PRESSURE_LEFT_FRONT_CURRENT_VALUE",
        "0x0301060002": "TYRE_PRESSURE_LEFT_FRONT_DESIRED_VALUE",
        "0x0301060003": "TYRE_PRESSURE_LEFT_REAR_CURRENT_VALUE",
        "0x0301060004": "TYRE_PRESSURE_LEFT_REAR_DESIRED_VALUE",
        "0x0301060005": "TYRE_PRESSURE_RIGHT_FRONT_CURRENT_VALUE",
        "0x0301060006": "TYRE_PRESSURE_RIGHT_FRONT_DESIRED_VALUE",
        "0x0301060007": "TYRE_PRESSURE_RIGHT_REAR_CURRENT_VALUE",
        "0x0301060008": "TYRE_PRESSURE_RIGHT_REAR_DESIRED_VALUE",
        "0x0301060009": "TYRE_PRESSURE_SPARE_TYRE_CURRENT_VALUE",
        "0x030106000A": "TYRE_PRESSURE_SPARE_TYRE_DESIRED_VALUE",
        "0x030106000B": "TYRE_PRESSURE_LEFT_FRONT_TYRE_DIFFERENCE",
        "0x030106000C": "TYRE_PRESSURE_LEFT_REAR_TYRE_DIFFERENCE",
        "0x030106000D": "TYRE_PRESSURE_RIGHT_FRONT_TYRE_DIFFERENCE",
        "0x030106000E": "TYRE_PRESSURE_RIGHT_REAR_TYRE_DIFFERENCE",
        "0x030106000F": "TYRE_PRESSURE_SPARE_TYRE_DIFFERENCE",
    }

    def __init__(self, data: dict[str, str], has_pin: bool = False) -> None:
        """Initialize."""
        self.data: dict[str, Any] = data
        self.has_pin = has_pin
        self.measure_time = None
        self.send_time = None
        self.send_time_utc = None
        self.measure_mileage = None
        self.send_mileage = None
        self._vehicle_data = self._get_attributes()

    @property
    def is_supported(self) -> bool:
        """Supported status."""
        return self.attributes is not None

    @property
    def attributes(self) -> Any:
        """Attributes properties."""
        return self._vehicle_data

    def _get_attributes(self) -> dict[str, dict[str, Any]]:
        _attributes: dict[str, Any] = {}

        default = get_attr(
            self.data, "CurrentVehicleDataByRequestResponse.vehicleData.data"
        )
        vehicle_data = get_attr(
            self.data, "StoredVehicleDataResponse.vehicleData.data", default
        )
        if vehicle_data is None:
            return _attributes

        for raw_data in vehicle_data:
            for raw_field in raw_data.get("field", {}):
                ids = raw_field.get("id")
                value = raw_field.get("value")
                unit = raw_field.get("unit")
                if ids == "0x0101010001":
                    self.measure_time = raw_field.get("tsCarCaptured")
                    self.send_time = raw_field.get("tsCarSent")
                    self.send_time_utc = raw_field.get("tsCarSentUtc")
                    self.measure_mileage = raw_field.get("milCarCaptured")
                    self.send_mileage = raw_field.get("milCarSent")
                    _attributes.update(set_attr("LAST_UPDATE_TIME", self.send_time_utc))

                if identity := self.IDS.get(ids):
                    _attributes.update(set_attr(identity, value, unit))
                else:
                    _LOGGER.error("%s not found", ids)

        # Append meta sensors
        _attributes.update(self._metadatas(_attributes))

        return _attributes

    @staticmethod
    def _metadatas(attributes: dict[str, dict[str, Any]]) -> dict[Any, dict[str, Any]]:
        _metadatas = {}
        _attributes = attributes
        trunk_open = get_attr(_attributes, "trunk_open") is not None
        trunk_unlocked = get_attr(_attributes, "trunk_unlocked") is not None

        # Windows open status
        left_check = get_attr(_attributes, "open_left_front_windows.value")
        left_rear_check = get_attr(_attributes, "open_left_rear_windows.value")
        right_check = get_attr(_attributes, "open_right_front_windows.value")
        right_rear_check = get_attr(_attributes, "open_right_rear_windows.value")
        any_window_open = (
            left_check and left_rear_check and right_check and right_rear_check
        )
        if (
            left_check is not None
            and left_rear_check is not None
            and right_check is not None
            and right_rear_check is not None
        ):
            _metadatas.update(set_attr("ANY_WINDOW_OPEN", any_window_open))

        # Doors open status
        left_check = get_attr(_attributes, "unlock_left_front_door.value")
        left_rear_check = get_attr(_attributes, "unlock_left_rear_door.value")
        right_check = get_attr(_attributes, "unlock_right_front_door.value")
        right_rear_check = get_attr(_attributes, "unlock_right_rear_door.value")
        any_door_unlocked = (
            left_check and left_rear_check and right_check and right_rear_check
        )
        if bool_any_door_unlocked := (
            left_check is not None
            and left_rear_check is not None
            and right_check is not None
            and right_rear_check is not None
        ):
            _metadatas.update(set_attr("ANY_DOOR_UNLOCKED", any_door_unlocked))

        # Doors open status
        left_check = get_attr(_attributes, "open_left_front_door.value")
        left_rear_check = get_attr(_attributes, "open_left_rear_door.value")
        right_check = get_attr(_attributes, "open_right_front_door.value")
        right_rear_check = get_attr(_attributes, "open_right_rear_door.value")
        any_door_open = (
            left_check and left_rear_check and right_check and right_rear_check
        )
        if bool_any_door_open := (
            left_check is not None
            and left_rear_check is not None
            and right_check is not None
            and right_rear_check is not None
        ):
            _metadatas.update(set_attr("ANY_DOOR_OPEN", any_door_open))

        # Door trunk status
        if (
            bool_any_door_open
            and bool_any_door_unlocked
            and trunk_open
            and trunk_unlocked
        ):
            if any_door_open and trunk_open:
                _metadatas.update(set_attr("DOORS_TRUNK_STATUS", "Open"))
            elif any_door_unlocked and trunk_unlocked:
                _metadatas.update(set_attr("DOORS_TRUNK_STATUS", "Closed"))
            else:
                _metadatas.update(set_attr("DOORS_TRUNK_STATUS", "Locked"))

        # Tyre pressure status
        left_check = get_attr(_attributes, "tyre_pressure_left_front.value")
        left_rear_check = get_attr(_attributes, "tyre_pressure_left_rear.value")
        right_check = get_attr(_attributes, "tyre_pressure_right_front.value")
        right_rear_check = get_attr(_attributes, "tyre_pressure_right_rear.value")
        spare_check = get_attr(_attributes, "tyre_pressure_spare.value")
        any_tyre_pressure = (
            left_check
            and left_rear_check
            and right_check
            and right_rear_check
            and spare_check
        )
        if (
            left_check is not None
            and left_rear_check is not None
            and right_check is not None
            and right_rear_check is not None
            and spare_check is not None
        ):
            _metadatas.update(set_attr("ANY_TYRE_PRESSURE", any_tyre_pressure))

        return _metadatas


@dataclass
class PreheaterDataResponse:
    """Preheater class."""

    data: dict[str, Any]

    @property
    def is_supported(self) -> bool:
        """Supported status."""
        return self.attributes is not None

    @property
    def attributes(self) -> dict[Any, dict[str, Any]]:
        """Attributes properties."""
        _attributes = {}
        report = get_attr(self.data, "statusResponse.climatisationStateReport")
        if report:
            _attributes.update(set_attr("PREHEATER_STATE", report))
            _attributes.update(
                set_attr("PREHEATER_ACTIVE", report.get("climatisationState"))
            )
            _attributes.update(
                set_attr("PREHEATER_DURATION", report.get("climatisationDuration"))
            )
            _attributes.update(
                set_attr("PREHEATER_REMAINING", report.get("remainingClimateTime"))
            )

        return _attributes


@dataclass
class ChargerDataResponse:
    """Charger class."""

    data: dict[str, Any]

    @property
    def is_supported(self) -> bool:
        """Supported status."""
        return (
            get_attr(self.data, "charger.settings") is not None
            or get_attr(self.data, "charger.status") is not None
        )

    @property
    def attributes(self) -> dict[Any, dict[str, Any]]:
        """Attributes properties."""
        _attributes = {}
        _settings = get_attr(self.data, "charger.settings")
        _status = get_attr(self.data, "charger.status")
        _charging_status = get_attr(self.data, "charger.status.chargingStatusData")
        _cruising_status = get_attr(self.data, "charger.status.cruisingRangeStatusData")

        _attributes.update(
            set_attr(
                "MAX_CHARGE_CURRENT", get_attr(_settings, "maxChargeCurrent.content")
            )
        )
        _attributes.update(
            set_attr(
                "CHARGING_STATE", get_attr(_charging_status, "chargingState.content")
            )
        )
        _attributes.update(
            set_attr(
                "ACTUAL_CHARGE_RATE",
                get_attr(_charging_status, "actualChargeRate.content"),
            )
        )
        _attributes.update(
            set_attr(
                "ACTUAL_CHARGE_RATE_UNIT",
                get_attr(_charging_status, "chargeRateUnit.content"),
            )
        )
        _attributes.update(
            set_attr(
                "CHARGING_POWER", get_attr(_charging_status, "chargingPower.content")
            )
        )
        _attributes.update(
            set_attr(
                "CHARGING_MODE", get_attr(_charging_status, "chargingMode.content")
            )
        )
        _attributes.update(
            set_attr("ENERGY_FLOW", get_attr(_charging_status, "energyFlow.content"))
        )
        _attributes.update(
            set_attr(
                "PRIMARY_ENGINE_TYPE",
                get_attr(_cruising_status, "engineTypeFirstEngine.content"),
            )
        )
        _attributes.update(
            set_attr(
                "SECONDARY_ENGINE_TYPE",
                get_attr(_cruising_status, "engineTypeSecondEngine.content"),
            )
        )
        _attributes.update(
            set_attr("HYBRID_RANGE", get_attr(_cruising_status, "hybridRange.content"))
        )
        _attributes.update(
            set_attr(
                "PRIMARY_ENGINE_RANGE",
                get_attr(_cruising_status, "primaryEngineRange.content"),
            )
        )
        _attributes.update(
            set_attr(
                "SECONDARY_ENGINE_RANGE",
                get_attr(_cruising_status, "secondaryEngineRange.content"),
            )
        )
        _attributes.update(
            set_attr(
                "STATE_OF_CHARGE",
                get_attr(_status, "batteryStatusData.stateOfCharge.content"),
            )
        )
        _attributes.update(
            set_attr(
                "PLUG_STATE", get_attr(_status, "plugStatusData.plugState.content")
            )
        )
        _attributes.update(
            set_attr("PLUG_LOCK", get_attr(_status, "plugStatusData.lockState.content"))
        )
        _attributes.update(
            set_attr(
                "REMAINING_CHARGING_TIME",
                get_attr(_status, "batteryStatusData.remainingChargingTime.content"),
            )
        )

        return _attributes


@dataclass
class ClimaterDataResponse:
    """Climater class."""

    data: dict[str, Any]

    @property
    def is_supported(self) -> bool:
        """Supported status."""
        return self.attributes is not None

    @property
    def attributes(self) -> dict[Any, dict[str, Any]]:
        """Attributes properties."""
        _attributes = {}
        _settings = get_attr(self.data, "climater.settings")
        _status = get_attr(self.data, "climater.status")
        _attributes.update(
            set_attr(
                "CLIMATISATION_STATE",
                get_attr(
                    _status,
                    "climatisationStatusData.climatisationState.content",
                ),
            )
        )
        _attributes.update(
            set_attr(
                "OUTDOOR_TEMPERATURE",
                get_attr(
                    _status,
                    "temperatureStatusData.outdoorTemperature.content",
                ),
            )
        )
        _attributes.update(
            set_attr(
                "CLIMATISATION_HEATER_SRC",
                get_attr(_settings, "heaterSource.content"),
            )
        )
        _attributes.update(
            set_attr(
                "CLIMATISATION_TARGET_TEMP",
                get_attr(_settings, "targetTemperature.content"),
            )
        )

        return _attributes


@dataclass
class DestinationDataResponse:
    """Destination."""

    data: dict[str, Any]

    @property
    def is_supported(self) -> bool:
        """Supported status."""
        return self.attributes is not None

    @property
    def attributes(self) -> dict[Any, dict[str, Any]]:
        """Attributes properties."""
        _attributes = {}
        _attributes = self.data
        return _attributes


@dataclass
class HistoryDataResponse:
    """Destination."""

    data: dict[str, Any]

    @property
    def is_supported(self) -> bool:
        """Supported status."""
        return self.attributes is not None

    @property
    def attributes(self) -> dict[Any, dict[str, Any]]:
        """Attributes properties."""
        _attributes = {}
        _attributes = self.data
        return _attributes


@dataclass
class UsersDataResponse:
    """Destination."""

    data: dict[str, Any]

    @property
    def is_supported(self) -> bool:
        """Supported status."""
        return self.attributes is not None

    @property
    def attributes(self) -> dict[Any, dict[str, Any]]:
        """Attributes properties."""
        _attributes = {}
        _attributes = self.data
        return _attributes


@dataclass
class PositionDataResponse:
    """Position class."""

    data: dict[str, Any]

    @property
    def is_supported(self) -> bool:
        """Supported status."""
        return get_attr(self.data, "findCarResponse.Position") is not None

    @property
    def attributes(self) -> dict[Any, dict[str, Any]]:
        """Attributes properties."""
        _attributes = {}
        car = self.data.get("findCarResponse", {})
        position = car.get("Position", {})
        if coordinate := position.get("carCoordinate"):
            value = {
                "latitude": coordinate["latitude"] / 1000000,
                "longitude": coordinate["longitude"] / 1000000,
                "timestamp": position["timestampCarSentUTC"],
                "parktime": car.get("parkingTimeUTC", position["timestampCarSentUTC"]),
            }
            _attributes.update(set_attr("POSITION", value))
        return _attributes


@dataclass
class TripDataResponse:
    """Trip class."""

    data: dict[str, Any]

    @property
    def is_supported(self) -> bool:
        """Supported status."""
        return self.data is not None

    @property
    def attributes(self) -> dict[str, Any]:
        """Attributes properties."""
        trip_id = self.data["tripID"]
        average_electricengine_consumption = (
            (float(self.data["averageElectricEngineConsumption"]) / 10)
            if "averageElectricEngineConsumption" in self.data
            else None
        )
        average_fuel_consumption = (
            float(self.data["averageFuelConsumption"]) / 10
            if "averageFuelConsumption" in self.data
            else None
        )
        average_speed = (
            int(self.data["averageSpeed"]) if "averageSpeed" in self.data else None
        )
        mileage = int(self.data["mileage"]) if "mileage" in self.data else None
        start_mileage = (
            int(self.data["startMileage"]) if "startMileage" in self.data else None
        )
        travel_time = (
            int(self.data["traveltime"]) if "traveltime" in self.data else None
        )
        timestamp = self.data["timestamp"] if "timestamp" in self.data else None
        overall_mileage = (
            int(self.data["overallMileage"]) if "overallMileage" in self.data else None
        )

        return {
            "tripID": trip_id,
            "averageElectricEngineConsumption": average_electricengine_consumption,
            "averageFuelConsumption": average_fuel_consumption,
            "averageSpeed": average_speed,
            "mileage": mileage,
            "startMileage": start_mileage,
            "traveltime": travel_time,
            "timestamp": timestamp,
            "overallMileage": overall_mileage,
        }


class Vehicle:
    """Vehicle class."""

    def __init__(self, data: Any, audi_service: AudiService) -> None:
        """Initialize."""
        self._audi_service = audi_service
        self.vin = data.get("vin")
        self.csid = data.get("csid")
        self.model = get_attr(data, "vehicle.media.longName", "")
        self.model_year = get_attr(data, "vehicle.core.modelYear")
        if (nickname := data.get("nickname")) is not None and len(nickname) > 0:
            self.title = nickname
        else:
            self.title = get_attr(data, "vehicle.media.shortName", self.vin)

        self.states: dict[Any, dict[str, Any]] = {}
        self.support_charger: bool | None = None
        self.support_climater: bool | None = None
        self.support_position: bool | None = None
        self.support_preheater: bool | None = None
        self.support_trip_cyclic: bool | None = None
        self.support_trip_long: bool | None = None
        self.support_trip_short: bool | None = None
        self.support_vehicle: bool | None = None

    async def async_fetch_data(self) -> bool:
        """Update."""
        info = ""
        try:
            info = "status"
            await self.async_update_vehicle()
            info = "position"
            await self.async_update_position()
            info = "climater"
            await self.async_update_climater()
            info = "charger"
            await self.async_update_charger()
            info = "preheater"
            await self.async_update_preheater()
            for kind in ["short", "long", "cyclic"]:
                info = kind
                await self.async_update_tripdata(kind)
        except Exception as error:  # pylint: disable=broad-except
            _LOGGER.error(
                "Unable to update vehicle data %s of %s: %s",
                info,
                self.vin,
                str(error).rstrip("\n"),
            )
            return False
        return True

    @retry(exceptions=TimeoutExceededError, tries=3, delay=2)
    async def async_update_vehicle(self) -> None:
        """Update vehicle status."""
        if self.support_vehicle is not False:
            try:
                result = await self._audi_service.async_get_vehicle(self.vin)
                if result.is_supported:
                    self.states.update(result.attributes)
            except ServiceNotFoundError as error:
                if error.args[0] in (401, 403, 502):
                    self.support_vehicle = False
                else:
                    _LOGGER.error(
                        "Unable to obtain the vehicle  status report of %s: %s",
                        self.vin,
                        str(error).rstrip("\n"),
                    )
            except HttpRequestError as error:
                _LOGGER.error(
                    "Unable to obtain the vehicle  status report of %s: %s",
                    self.vin,
                    str(error).rstrip("\n"),
                )
            else:
                self.support_vehicle = result.is_supported

    @retry(exceptions=TimeoutExceededError, tries=3, delay=2)
    async def async_update_position(self) -> None:
        """Update vehicle position."""
        if self.support_position is not False:
            try:
                result = await self._audi_service.async_get_stored_position(self.vin)
                if result.is_supported:
                    self.states.update(result.attributes)
            except ServiceNotFoundError as error:
                if error.args[0] in (401, 403, 502):
                    self.support_position = False
                # If error is 204 is returned, the position is currently not available
                elif error.args[0] != 204:
                    _LOGGER.error(
                        "Unable to update the vehicle position of %s: %s",
                        self.vin,
                        str(error).rstrip("\n"),
                    )
            except HttpRequestError as error:
                _LOGGER.error(
                    "Unable to obtain the vehicle position of %s: %s",
                    self.vin,
                    str(error).rstrip("\n"),
                )
            else:
                self.support_position = result.is_supported

    @retry(exceptions=TimeoutExceededError, tries=3, delay=2)
    async def async_update_climater(self) -> None:
        """Update vehicle climater."""
        if self.support_climater is not False:
            try:
                result = await self._audi_service.async_get_climater(self.vin)
                if result.is_supported:
                    self.states.update(result.attributes)
            except ServiceNotFoundError as error:
                if error.args[0] in (401, 403, 502):
                    self.support_climater = False
                else:
                    _LOGGER.error(
                        "Unable to obtain the vehicle climatisation state for %s: %s",
                        self.vin,
                        str(error).rstrip("\n"),
                    )
            except HttpRequestError as error:
                _LOGGER.error(
                    "Unable to obtain the vehicle climatisation state for %s: %s",
                    self.vin,
                    str(error).rstrip("\n"),
                )
            else:
                self.support_climater = result.is_supported

    @retry(exceptions=TimeoutExceededError, tries=3, delay=2)
    async def async_update_preheater(self) -> None:
        """Update vehicle preheater."""
        if self.support_preheater is not False:
            try:
                result = await self._audi_service.async_get_preheater(self.vin)
                if result.is_supported:
                    self.states.update(result.attributes)
            except ServiceNotFoundError as error:
                if error.args[0] in (401, 403, 502):
                    self.support_preheater = False
                else:
                    _LOGGER.error(
                        "Unable to obtain the vehicle preheater state for %s: %s",
                        self.vin,
                        str(error).rstrip("\n"),
                    )
            except HttpRequestError as error:
                _LOGGER.error(
                    "Unable to obtain the vehicle preheater state for %s: %s",
                    self.vin,
                    str(error).rstrip("\n"),
                )
            else:
                self.support_preheater = result.is_supported

    @retry(exceptions=TimeoutExceededError, tries=3, delay=2)
    async def async_update_charger(self) -> None:
        """Update vehicle charger."""
        if self.support_charger is not False:
            try:
                result = await self._audi_service.async_get_charger(self.vin)
                if result.is_supported:
                    self.states.update(result.attributes)
            except ServiceNotFoundError as error:
                if error.args[0] in (401, 403, 502):
                    self.support_charger = False
                else:
                    _LOGGER.error(
                        "Unable to obtain the vehicle charger state for %s: %s",
                        self.vin,
                        str(error).rstrip("\n"),
                    )
            except HttpRequestError as error:
                _LOGGER.error(
                    "Unable to obtain the vehicle charger state for %s: %s",
                    self.vin,
                    str(error).rstrip("\n"),
                )
            else:
                self.support_charger = result.is_supported

    @retry(exceptions=TimeoutExceededError, tries=3, delay=2)
    async def async_update_tripdata(
        self, kind: Literal["short", "long", "cyclic"]
    ) -> None:
        """Update vehicle trip."""
        if getattr(self, f"support_trip_{kind}") is not False:
            try:
                td_cur, td_rst = await self._audi_service.async_get_tripdata(
                    self.vin, kind
                )
                if td_cur.is_supported:
                    self.states.update(
                        set_attr(f"trip_{kind}_current", td_cur.attributes)
                    )

                if td_rst.is_supported:
                    self.states.update(
                        set_attr(f"trip_{kind}_reset", td_rst.attributes)
                    )
            except ServiceNotFoundError as error:
                if error.args[0] in (400, 401, 403, 502):
                    setattr(self, f"support_trip_{kind}", False)
                else:
                    _LOGGER.error(
                        "Unable to obtain the vehicle %s tripdata of %s: %s",
                        kind,
                        self.vin,
                        str(error).rstrip("\n"),
                    )
            except HttpRequestError as error:
                _LOGGER.error(
                    "Unable to obtain the vehicle %s tripdata of %s: %s",
                    kind,
                    self.vin,
                    str(error).rstrip("\n"),
                )
            else:
                setattr(self, f"support_trip_{kind}", True)
