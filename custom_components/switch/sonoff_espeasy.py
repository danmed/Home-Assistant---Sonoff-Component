"""
Support for customised Sonoff Wifi switch's running ESPEasy.
For more details about this platform, please refer to the documentation at
https://github.com/danmed/Home-Assistant---Sonoff-Component
"""
import logging

import requests
import voluptuous as vol

from homeassistant.components.switch import SwitchDevice, PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_HOST, CONF_NAME, CONF_PORT, CONF_PATH, CONF_USERNAME, CONF_PASSWORD,
    CONF_SWITCHES)
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

SWITCH_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_NAME): cv.string,
    vol.Optional(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_SWITCHES): vol.Schema({cv.slug: SWITCH_SCHEMA}),
})


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices_callback, discovery_info=None):
    """Set up Sonoff Wifi switches."""
    switches = config.get('switches', {})
    devices = []

    for dev_name, properties in switches.items():
        devices.append(
            SonoffSwitch(
 hass,
                properties.get(CONF_NAME, dev_name),
                properties.get(CONF_HOST, None),
                properties.get(CONF_USERNAME, None),
                properties.get(CONF_PASSWORD)))

    add_devices_callback(devices)


class SonoffSwitch(SwitchDevice):
    """Representation of a Sonoff Wifi switch."""

    def __init__(self, hass, name, host, user, passwd):
        """Initialize the device."""
        self._hass = hass
        self._name = name
        self._state = False
        self._url = 'http://{}'.format(host)
        if user is not None:
            self._auth = (user, passwd)
        else:
            self._auth = None

    def _switch(self, newstate):
        """Switch on or off."""
        _LOGGER.info("Switching to state: %s", newstate)

        try:
            req = requests.get('{}/control?cmd=gpio,12,{}'.format(self._url, newstate),
                               auth=self._auth, timeout=5)
            return req.json()['mode'] == "output"
        except requests.RequestException:
            _LOGGER.error("Switching failed")

    def _query_state(self):
        """Query switch state."""
        _LOGGER.info("Querying state from: %s", self._url)

        try:
            req = requests.get('{}/control?cmd=status,gpio,12'.format(self._url),
                               auth=self._auth, timeout=5)
            return req.json()['state'] == 1
        except requests.RequestException:
            _LOGGER.error("State query failed")

    @property
    def should_poll(self):
        """Return the polling state."""
        return True

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    def update(self):
        """Update device state."""
        self._state = self._query_state()

    def turn_on(self, **kwargs):
        """Turn the device on."""
        if self._switch('1'):
            self._state = True

    def turn_off(self, **kwargs):
        """Turn the device off."""
        if self._switch('0'):
            self._state = False
