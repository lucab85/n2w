// Copyright 2017 Luca Berton
// 
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
// 
//      http://www.apache.org/licenses/LICENSE-2.0
// 
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


(function() {
  'use strict';

  var app = {
    isLoading: true,
    visibleCards: {},
    selectedNumbers: [],
    spinner: document.querySelector('.loader'),
    cardTemplate: document.querySelector('.cardTemplate'),
    container: document.querySelector('.main'),
    addDialog: document.querySelector('.dialog-container'),
  };


  /*****************************************************************************
   *
   * Event listeners for UI elements
   *
   ****************************************************************************/

  document.getElementById('butRefresh').addEventListener('click', function() {
    app.updateN2W();
  });

  document.getElementById('butAdd').addEventListener('click', function() {
    app.toggleAddDialog(true);
  });

  document.getElementById('butAddNumber').addEventListener('click', function() {
	var number = document.getElementById('selectNumberToAdd').value;
    var key = number;
    var label = number;
    if (!app.selectedNumbers) {
      app.selectedNumbers = [];
    }
    app.getN2W(key, label);
    app.selectedNumbers.push({key: key, label: label});
    app.saveselectedNumbers();
    app.toggleAddDialog(false);
  });

  document.getElementById('butAddCancel').addEventListener('click', function() {
    app.toggleAddDialog(false);
  });


  /*****************************************************************************
   *
   * Methods to update/refresh the UI
   *
   ****************************************************************************/

  app.toggleAddDialog = function(visible) {
    if (visible) {
      app.addDialog.classList.add('dialog-container--visible');
    } else {
      app.addDialog.classList.remove('dialog-container--visible');
    }
  };

  app.updateForecastCard = function(data) {
    var dataLastUpdated = new Date(data.created);
    var current = data;

    var card = app.visibleCards[data.key];
    if (!card) {
      card = app.cardTemplate.cloneNode(true);
      card.classList.remove('cardTemplate');
      card.querySelector('.location').textContent = data.label;
      card.removeAttribute('hidden');
      app.container.appendChild(card);
      app.visibleCards[data.key] = card;
    }

    var cardLastUpdatedElem = card.querySelector('.card-last-updated');
    var cardLastUpdated = cardLastUpdatedElem.textContent;
    if (cardLastUpdated) {
      cardLastUpdated = new Date(cardLastUpdated);
      if (dataLastUpdated.getTime() < cardLastUpdated.getTime()) {
        return;
      }
    }
    cardLastUpdatedElem.textContent = data.created;

    card.querySelector('.description').textContent = current.number;
    card.querySelector('.date').textContent = current.created;
    card.querySelector('.current .lang .value').textContent = current.lang;
	card.querySelector('.current .text .value').textContent = current.text;

    if (app.isLoading) {
      app.spinner.setAttribute('hidden', true);
      app.container.removeAttribute('hidden');
      app.isLoading = false;
    }
  };


  /*****************************************************************************
   *
   * Methods for dealing with the model
   *
   ****************************************************************************/

  app.getN2W = function(key, label) {
	var url = 'https://n2w.mrevolution.eu/n2w/api/v1.0/get/' + key;
    if ('caches' in window) {
      caches.match(url).then(function(response) {
        if (response) {
          response.json().then(function updateFromCache(json) {
            var results = json;
            results.key = key;
            results.label = label;
            results.created = json.created;
            app.updateForecastCard(results);
          });
        }
      });
    }
    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
      if (request.readyState === XMLHttpRequest.DONE) {
        if (request.status === 200) {
          var response = JSON.parse(request.response);
          var results = response;
          results.key = key;
          results.label = label;
          results.created = response.created;
          app.updateForecastCard(results);
        }
      } else {
        app.updateForecastCard(initialN2W);
      }
    };
    request.open('GET', url);
    request.send();
  };

  app.updateN2W = function() {
    var keys = Object.keys(app.visibleCards);
    keys.forEach(function(key) {
      app.getN2W(key);
    });
  };

  app.saveselectedNumbers = function() {
    var selectedNumbers = JSON.stringify(app.selectedNumbers);
    localStorage.selectedNumbers = selectedNumbers;
  };

  var initialN2W = {
    key: '1234567',
    label: 'Test number',
    created: '2017-11-07T01:00:00Z',
	number: '42',
	lang: 'it',
	text: 'quarantadue'

  };

  /************************************************************************
   *
   * Code required to start the app
   *
   ************************************************************************/

  app.selectedNumbers = localStorage.selectedNumbers;
  if (app.selectedNumbers) {
    app.selectedNumbers = JSON.parse(app.selectedNumbers);
    app.selectedNumbers.forEach(function(city) {
      app.getN2W(city.key, city.label);
    });
  } else {
    app.updateForecastCard(initialN2W);
    app.selectedNumbers = [
      {key: initialN2W.key, label: initialN2W.label}
    ];
    app.saveselectedNumbers();
  }

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker
             .register('./service-worker.js')
             .then(function() { console.log('Service Worker Registered'); });
  }
})();
