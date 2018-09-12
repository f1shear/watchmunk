$(document).ready(function(){

	  var systemDetailVue = new Vue({
      el: '#systemDetailVue',
      mixins: [COMMON_MIXIN],
      data: {
          projectID: null,
          systemID: null,
          integrations: [],
          project: null,
          system: {
              name: '',
              system_type: '',
              repo_info: '',
              environment_config: '',
              staging_info: '',
              production_info: '',
              api_info: '',
              documentation: '',
              deployment_type: '',
              author: {},
          },
          systemAccessList: [],
          systemApps: [],
          systemDependencies: [],
          users: [],
          systems: [],
          selectedApp: '',
          appPosts: [],

          addAppForm: {
              app: '',
              system: '',
          }
      },
      methods: {
          saveSystem: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/",
                  type: 'PUT',
                  success: function(data) {
                      $.notify("System saved.", "success");
                      that.system = data;
                  },
                  data: that.system
              });
          },
          addSystem: function() {
              var that = this;
              $.post("/api/v1/projects/" + this.projectID + "/systems/", that.system, function(data) {
                  
                  that.loadSystems(that.projectID);
                  $('#addSystemModal').modal('hide');
                  $.notify("System added.", "success");
              });
          },
          extractURLInfo: function() {
              var path = window.location.pathname.split('/');
              var trailingPad = 0;
              if (path[path.length - 1] == '') {
                  trailingPad = 1;
              }
              return {
                  systemID: path[path.length - 1 - trailingPad],
                  projectID: path[path.length - 3 - trailingPad],
              };
          },
          loadSystemApps: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/apps/",
                  type: 'GET',
                  success: function(data) {
                      that.systemApps = data['results'];
                  }
              });
          },
          
          setSelectedApp: function(app) {
              this.selectedApp = app;
              this.loadAppPosts();
          },
          loadAppPosts: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/apps/" + this.selectedApp.id + "/posts/",
                  type: 'GET',
                  success: function(data) {
                      var appPosts = data['results'];
                      var template = that.selectedApp.app.message_template;
                      that.appPosts = [];

                      for (var i = 0; i < appPosts.length; i++) {

                          var post = JSON.parse(appPosts[i].post);
                          msg = Mustache.render(template, post);
                          that.appPosts.push(msg);
                      }
                  }
              });
          },
          loadAccessList: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/accesses/",
                  type: 'GET',
                  success: function(data) {
                      that.systemAccessList = data['results'];
                  }
              });
          },
          loadDependencies: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/dependencies/",
                  type: 'GET',
                  success: function(data) {
                      that.systemDependencies = data['results'];
                  }
              });
          },
          addDependency: function(sys) {
              var that = this;
              var payload = {
                  system: this.system.id,
                  depends_on: sys.id
              }

              $.post("/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/dependencies/", payload, function(data) {
                  $.notify("Dependency added.", "success");
                  that.loadDependencies();
              });

          },
          removeDependency: function(dep) {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/dependencies/" + dep.id + "/",
                  type: 'DELETE',
                  success: function() {
                      $.notify("Dependency removed.", "info");
                      that.loadDependencies();
                  }
              });
          },
          addAccess: function(user) {

              var that = this;
              var payload = {
                  system: this.system.id,
                  user: user.id
              }

              $.post("/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/accesses/", payload, function(data) {
                  $.notify("Access added.", "success");
                  that.loadAccessList();
              });

          },
          removeAccess: function(access) {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/accesses/" + access.id + "/",
                  type: 'DELETE',
                  success: function() {
                      $.notify("Access removed.", "info");
                      that.loadAccessList();
                  }
              });

          },
          modifyAccess: function($event, access){
            var payload = {
              moderator: access.moderator
            }

            $.ajax({
              url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/accesses/" + access.id + "/",
              type: 'PATCH',
              success: function(data) {
                  $.notify("Access modified.", "success");
              },
              data: payload
            });

          },
          addApplication: function() {
              var that = this;
              var payload = {
                  app: this.addAppForm.app,
                  system: this.systemID
              }

              $.post("/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/apps/", payload, function(data) {
                  that.loadSystemApps(that.projectID, that.systemID);
                  $('#addApplicationModal').modal('hide');
                  $.notify("Application added.", "success");
              });

          },
          removeApplication: function() {

              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/apps/" + this.selectedApp.id + "/",
                  type: 'DELETE',
                  success: function() {

                      that.selectedApp = '';
                      that.loadSystemApps(that.projectID, that.systemID);
                      $('#removeApplicationModal').modal('hide');
                      $.notify("Application removed.", "info");
                  }
              });
          }

      },

      computed: {
          filteredSystems: function() {
              return this.filterData(this.systems, this.systemDependencies, 'depends_on.id');
          },

          filteredApps: function() {
              return this.filterData(this.apps, this.systemApps, 'app.id');
          },
          filteredUsers: function() {
              return this.filterData(this.users, this.systemAccessList, 'user.id');
          },
      },
      mounted: function() {
          var urlInfo = this.extractURLInfo();

          this.projectID = urlInfo['projectID'];
          this.systemID = urlInfo['systemID'];
          this.loadApps();
          this.loadProject();
          this.loadSystem();
          this.loadSystemApps();
          this.loadUsers();
          this.loadSystems();
          this.loadAccessList();
          this.loadDependencies();
      }
  });

});