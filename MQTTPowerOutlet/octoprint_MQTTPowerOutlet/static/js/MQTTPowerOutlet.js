/*
 * View model for MQTTPowerOutlet
 *
 * Author: Rodrigo Galvao Barros Silva
 * License: AGPLv3
 */
$(function() {
    function MqttpoweroutletViewModel(parameters) {
        var self = this;

        // assign the injected parameters, e.g.:
        self.loginStateViewModel = parameters[0];
        self.settingsViewModel = parameters[1];
        
        self.topics = ko.observable();
        self.btn_1 = ko.observableArray();
        self.btn_2 = ko.observableArray();
        self.btn_3 = ko.observableArray();
        self.btn_4 = ko.observableArray();
        self.ptn_1 = ko.observableArray();
       

self.sendMsg = function(data) {
   
    $.ajax({
        url: API_BASEURL + "plugin/MQTTPowerOutlet",
        type: "POST",
        dataType: "json",
        data: JSON.stringify({
            command: "toggle_btn",
            n_btn: data			
        }),
        contentType: "application/json; charset=UTF-8"
    }).done(function(response){console.log(response);});
}


self.getAdditionalControls = function() {

    var buttons = [
        { name: "Power", type: "section", layout: "horizontal", children: [
            {type: "javascript", javascript: function() { self.sendMsg(1); }, name: "Printer", enabled: "true", icon: "fas fa-plug icon"},//icon does not work!
            {type: "javascript", javascript: function() { self.sendMsg(2); }, name: "Fan", enabled: true},
            {type: "javascript", javascript: function() { self.sendMsg(3); }, name: "o",  enabled: "true"},
            {type: "javascript", javascript: function() { self.sendMsg(4); }, name: "*",  enabled: "false"},

        ]}
    ];

return buttons;
};
        // TODO: Implement your plugin's view model here.
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: MqttpoweroutletViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [  "loginStateViewModel", "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_MQTTPowerOutlet, #tab_plugin_MQTTPowerOutlet, ...
        elements: [ "#settings_plugin_MQTTPowerOutlet"]
    });
});
