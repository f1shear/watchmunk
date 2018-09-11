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
          systemModerators: [],
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
                      alert("Saved!");
                      that.project = data;
                  },
                  data: that.system
              });
          },
          addSystem: function() {
              var that = this;
              $.post("/api/v1/projects/" + this.projectID + "/systems/", that.system, function(data) {
                  alert("Added System!");
                  that.loadSystems(that.projectID);
                  $('#addSystemModal').modal('hide');
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
          loadModerators: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/moderators/",
                  type: 'GET',
                  success: function(data) {
                      that.systemModerators = data['results'];
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

                  that.loadDependencies();
              });

          },
          removeDependency: function(dep) {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/dependencies/" + dep.id + "/",
                  type: 'DELETE',
                  success: function() {

                      that.loadDependencies();
                  }
              });
          },
          addModerator: function(user) {

              var that = this;
              var payload = {
                  system: this.system.id,
                  moderator: user.id
              }

              $.post("/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/moderators/", payload, function(data) {

                  that.loadModerators();
              });

          },
          removeModerator: function(mod) {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/systems/" + this.systemID + "/moderators/" + mod.id + "/",
                  type: 'DELETE',
                  success: function() {

                      that.loadModerators();
                  }
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
              return this.filterData(this.users, this.systemModerators, 'moderator.id');
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
          this.loadModerators();
          this.loadDependencies();
      }
  });

});