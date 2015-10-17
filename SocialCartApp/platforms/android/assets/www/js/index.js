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


        
        var pushNotification = window.plugins.pushNotification;
        pushNotification.register(
            successHandler, 
            errorHandler, 
            {
                'senderID':'298895233032',
                'ecb':'onNotificationGCM' // callback function
            }
        );

    },


    // Update DOM on a Received Event
    /*
    receivedEvent: function(id) {
        var parentElement = document.getElementById(id);
        var listeningElement = parentElement.querySelector('.listening');
        var receivedElement = parentElement.querySelector('.received');

        listeningElement.setAttribute('style', 'display:none;');
        receivedElement.setAttribute('style', 'display:block;');

        console.log('Received Event: ' + id);
    } */
};

function successHandler(result) {
//    alert('Success');
//    deviceRegistered(result);
}

function errorHandler(error) {
    alert('Error');
    console.log('Error: '+ error);
}


function onNotificationGCM(e) {
    console.log('Notification Receoved');
    switch(e.event) {
        case 'registered':
            if (e.regid.length > 0){
                alert(e.regid);
                deviceRegistered(e.regid); 
                }
        break;

        case 'message':
            /*
            if (e.foreground){
                // When the app is running foreground. 
                alert('A Social Cart has popped up! Time to add some stuff!')
            } */
        break;

        case 'error':
            console.log('Error: ' + e.msg);
        break;

        default:
          console.log('An unknown event was received');
          break;
    }
}    

function deviceRegistered(gcm_key) {
    alert("Redirection");
    var options = {
        location: 'no',
        clearcache: 'yes',
    };
    window.open = cordova.InAppBrowser.open;
    var url = "http://www.socialcart.com/?gcm_key=" + gcm_key;
    console.log("Redirecting" + url); 
    var ref = cordova.InAppBrowser.open(url, "_blank", "location=no");
}

/*
function deviceRegistered(gcm_key) {
    console.log("Device Registered");
    alert('Yowza');
    $.ajax({
        url: 'http://www.socialcart.com/gcm_key/',
        method: 'POST',
        data: {gcm_key: gcm_key},
        success: function(data){
            console.log(data);
        },
        crossDomain: true,
        cache: false,
        dataType: "json",
    });
}
*/
app.initialize();
