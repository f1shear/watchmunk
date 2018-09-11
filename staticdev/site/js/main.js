
function csrfSafeMethod(method) {
   // these HTTP methods do not require CSRF protection
   return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function(){
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

MODELS = {

    deploymentTypes: [{
                  'type': 'shared',
                  'label': 'Shared Hosting'
              },
              {
                  'type': 'dedicated',
                  'label': 'Dedicated Server'
              },
              {
                  'type': 'vm',
                  'label': 'Virtual Machine'
              },
              {
                  'type': 'container',
                  'label': 'Container'
              },
              {
                  'type': 'service',
                  'label': 'Service'
              },
          ],
    systemTypes: [{
                  'type': 'worker',
                  'label': 'Worker'
              },
              {
                  'type': 'system',
                  'label': 'System'
              },
              {
                  'type': 'storage',
                  'label': 'Storage'
              },
              {
                  'type': 'queue',
                  'label': 'Queue'
              },
              {
                  'type': 'database',
                  'label': 'Database'
              },
              {
                  'type': 'web',
                  'label': 'Web'
              },
              {
                  'type': 'client/web',
                  'label': 'Web Client'
              },
              {
                  'type': 'client/desktop',
                  'label': 'Desktop Client'
              },
              {
                  'type': 'client/mobile',
                  'label': 'Mobile Client'
              }
          ],

}


API = {
    loadApps: function(callback){

              $.ajax({
                  url: "/api/v1/apps/",
                  type: 'GET',
                  success: function(data) {
                      callback(data);
            }
        });
    }
}


var COMMON_MIXIN = {

    data: {
        apps: [],
        deploymentTypes: MODELS.deploymentTypes,
        systemTypes: MODELS.systemTypes,
    },

    methods: {

        loadApps: function() {
            var that = this;
            API.loadApps(function(data){
                that.apps = data['results'];
            });
          },
        loadUsers: function() {
            var that = this;
            $.get("/api/v1/users/", function(data) {
                that.users = data['results'];
            });
        },
        loadProject: function() {
              var that = this;
              $.get("/api/v1/projects/" + this.projectID + "/", function(data) {
                  that.project = data;
              });
          },
        loadSystem: function() {
            var that = this;
            $.get("/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/", function(data) {
                that.system = data;
            });
        },
        loadSystems: function() {
            var that = this;
            $.get("/api/v1/projects/" + this.projectID + "/systems/", function(data) {
                that.systems = data['results'];
            });
        },
        filterData: function(holderA, holderB, key){
          var filtered = [];
          var existing = {};
          for(var i=0; i<holderB.length; i++){
            var item = holderB[i];
            existing[eval('item.'+key)] = true;
          }
          for(var j=0; j<holderA.length; j++){

            if (!(holderA[j].id in existing)) {
                      filtered.push(holderA[j])
                  }

          }
          return filtered;
        },
    }
}

$(document).ready(function(){

  $.notify.defaults({
    elementPosition: 'bottom right',
    globalPosition: 'top right',
  });

});