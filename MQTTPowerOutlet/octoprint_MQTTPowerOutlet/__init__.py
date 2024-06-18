from __future__ import absolute_import

import octoprint.plugin
import flask
import sys

class MqttpoweroutletPlugin(octoprint.plugin.StartupPlugin,
	octoprint.plugin.SettingsPlugin,
	octoprint.plugin.AssetPlugin,
	octoprint.plugin.TemplatePlugin,
	octoprint.plugin.SimpleApiPlugin
):

	def get_settings_defaults(self):
		return dict(
				topics ="octoprint/plugin/poweroutlet/pub",
				btn_1 = dict(msgON = "ON", msgOFF = "OFF", state = False, icon="icon-home"),
				btn_2 = dict(msgON = "ON", msgOFF = "OFF", state = False, icon="icon-home"),
				btn_3 = dict(msgON = "ON", msgOFF = "OFF", state = False, icon="icon-home"),
				btn_4 = dict(msgON = "ON", msgOFF = "OFF", state = False, icon="icon-home"),
				ptn_1 = dict(msgON = "ON", msgOFF = "OFF", state = False, icon="icon-home")
		)

	
	def on_after_startup(self):
		helpers = self._plugin_manager.get_helpers("mqtt", "mqtt_publish", "mqtt_subscribe", "mqtt_unsubscribe")
		if helpers:
			if "mqtt_publish" in helpers:
				self.mqtt_publish = helpers["mqtt_publish"]
			if "mqtt_subscribe" in helpers:
				self.mqtt_subscribe = helpers["mqtt_subscribe"]
			if "mqtt_unsubscribe" in helpers:
				self.mqtt_unsubscribe = helpers["mqtt_unsubscribe"]
			
			try:			
				self.mqtt_publish("octoprint/plugin/poweroutlet/pub", "MQTT TEST.")
			except:
				self._plugin_manager.send_plugin_message(self._identifier, dict(noMQTT=True))

	def _on_mqtt_subscription(self, topic, message, retained=None, qos=None, *args, **kwargs):
		self.mqtt_publish("octoprint/plugin/poweroutlet/pub", "echo: " + message)

	##~~ AssetPlugin mixin

	def get_assets(self):
		return {
			"js": ["js/MQTTPowerOutlet.js"],
			"css": ["css/MQTTPowerOutlet.css"],
			"less": ["less/MQTTPowerOutlet.less"]
		}

	def toggle(self, n):
		
		btn_key = f"btn_{n}"
		btn_settings = self._settings.get([btn_key])
		self._logger.info("before: %s", self._settings.get([btn_key]))

		btn_settings["state"] = not btn_settings["state"]
		
		self._settings.set([btn_key], btn_settings)
		self._logger.info("after: %s", btn_settings)
		
		
		if btn_settings["state"]:
			self.mqtt_publish(self._settings.get(["topics"]), btn_settings["msgON"])
		else: 
			self.mqtt_publish(self._settings.get(["topics"]), btn_settings["msgOFF"])

	##API
	def get_api_commands(self):
		return dict(toggle_btn=["n_btn"])

	def on_api_command(self, command, data):
		#import flask
		
		if command == "toggle_btn":
			self._logger.info("Button toggled is {n_btn}".format(**data))
			self.toggle(int("{n_btn}".format(**data)))

	##~~ Softwareupdate hook

	def get_update_information(self):
		return {
			"MQTTPowerOutlet": {
				"displayName": "Mqttpoweroutlet Plugin",
				"displayVersion": self._plugin_version,

				# version check: github repository
				"type": "github_release",
				"user": "rodgalv",
				"repo": "MQTTPowerOutlet",
				"current": self._plugin_version,

				# update method: pip
				"pip": "https://github.com/rodgalv/MQTTPowerOutlet/archive/{target_version}.zip",
			}
		}


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "MQTT Power Outlet"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = MqttpoweroutletPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}
