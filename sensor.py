import logging
import datetime
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import CONF_NAME
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity

__version__ = '0.0.1'

_LOGGER = logging.getLogger(__name__)

ATTR_STAGE = 'stage'
ATTR_SUMMARY = 'summary'
ATTR_LAST_CHANGE = 'last_change'

CONF_SCHEDULE_URL = 'schedule_url'
CONF_ZONE = 'zone'

DEFAULT_NAME = "Eskom loadshedding status"

ICON = "mdi:transmission-tower"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_SCHEDULE_URL, default=''): cv.string,
    vol.Optional(CONF_ZONE, default=''): cv.string
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the Loadshedding sensor."""
    name = config[CONF_NAME]

    add_devices([LoadSheddingSensor(hass, config, name)], True)


class LoadSheddingSensor(Entity):

    def __init__(self, hass, conf, name):
        self.schedule_url = conf.get(CONF_SCHEDULE_URL)
        self.zone = conf.get(CONF_ZONE)
        self._stage = "Stage 0"
        self._summary = 'Unknown'
        self._state = 'Unknown'
        self._last_change = None
        if name:
            self._name = name
        else:
            self._name = 'Loadshedding sensor'

    @property
    def name(self):
        return self._name


    @property
    def state(self):
        return self._state


    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return {
            ATTR_SUMMARY: self._summary,
            ATTR_STAGE: self._stage,
            ATTR_LAST_CHANGE: self._last_change
        }

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return ICON

    def update(self):
        try:
            api = requests.get('https://loadshedding.eskom.co.za/LoadShedding/GetStatus', timeout=10)
        except OSError:
            _LOGGER.warning("Eskom loadshedding status is not available.")
            return

        if api.status_code == 200:
            state =  abs(int(api.text)) - 1
            if(state != self._state):
                self._state = state
                self._last_change = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
                self._stage = "Stage {}".format(self._state)
            
                if self._state == 0:
                    self._summary = "No loadshedding!"
                else:
                    self._summary = "Stage {} loadshedding.".format(self._state)
        else:
            _LOGGER.warning("Eskom loadshedding status is not available.")
