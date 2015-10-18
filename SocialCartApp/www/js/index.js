/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */
var app = {
    // Application Constructor
    initialize: function() {
        this.bindEvents();
    },
    // Bind Event Listeners
    //
    // Bind any events that are required on startup. Common events are:
    // 'load', 'deviceready', 'offline', and 'online'.
    bindEvents: function() {
        document.addEventListener('deviceready', this.onDeviceReady, false);
    },
    // deviceready Event Handler
    //
    // The scope of 'this' is the event. In order to call the 'receivedEvent'
    // function, we must explicitly call 'app.receivedEvent(...);'
    onDeviceReady: function() {
        //app.receivedEvent('deviceready');
        //window.location="http://www.socialcart.com/";

        var push = PushNotification.init({ "android": {"senderID": "298895233032", "vibrate": "true", "forceShow": "true", "icon": "icon"} } );

        push.on('registration', function(data) {
            // data.registrationId
            //alert(data.registrationId);
            deviceRegistered(data.registrationId);
        });

        push.on('notification', function(data) {
            alert(data.title + " " + data.message);
        });

        push.on('error', function(e) {
            // e.message
        });
         

    }
}



function deviceRegistered(gcm_key) {
    //alert("Redirection");
    //alert(gcm_key);
    var options = {
        location: 'no',
        clearcache: 'yes',
        zoom: 'no',
    };
    window.open = cordova.InAppBrowser.open;
    var url = "http://limitless-earth-4309.herokuapp.com/?gcm_key=" + gcm_key;
    console.log("Redirecting" + url); 
    var ref = cordova.InAppBrowser.open(url, "_blank", "location=no");
}

app.initialize();
