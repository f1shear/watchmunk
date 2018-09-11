$(document).ready(function(){

	  var systemDetailVue = new Vue({
      el: '#systemDetailVue',
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
          deploymentTypes: MODELS.deploymentTypes,
          systemTypes: MODELS.systemTypes,
          selectedApp: '',
          appPosts: [],
          apps: [],
          addAppForm: {
              app: '',
              system: '',
          }
      },
      methods: {
          loadProject: function(projectID) {
              var that = this;
              $.get("/api/v1/projects/" + projectID + "/", function(data) {
                  that.project = data;
              });
          },
          loadSystem: function(projectID, systemID) {
              var that = this;
              $.get("/api/v1/projects/" + projectID + "/systems/" + systemID + "/", function(data) {
                  that.system = data;
              });
          },
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
          loadSystemApps: function(projectID, systemID) {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + projectID + "/systems/" + systemID + "/apps/",
                  type: 'GET',
                  success: function(data) {
                      that.systemApps = data['results'];
                  }
              });
          },
          loadApps: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/apps/",
                  type: 'GET',
                  success: function(data) {
                      that.apps = data['results'];
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
          loadSystems: function(projectID) {
              var that = this;
              $.get("/api/v1/projects/" + projectID + "/systems/", function(data) {
                  that.systems = data['results'];
              });
          },
          loadUsers: function() {
              var that = this;
              $.get("/api/v1/users/", function(data) {
                  that.users = data['results'];
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
              var filtered = [];
              var dependencies_dict = {};

              for (var i = 0; i < this.systemDependencies.length; i++) {
                  var dep = this.systemDependencies[i];
                  dependencies_dict[dep.depends_on.id] = true;
              }

              for (var j = 0; j < this.systems.length; j++) {

                  if (!(this.systems[j].id in dependencies_dict)) {
                      filtered.push(this.systems[j])
                  }

              }

              return filtered;
          },

          filteredApps: function() {
              var filtered = [];
              var existing = {};

              for (var i = 0; i < this.systemApps.length; i++) {
                  var systemApp = this.systemApps[i];
                  existing[systemApp.app.id] = true;
              }

              for (var j = 0; j < this.apps.length; j++) {

                  if (!(this.apps[j].id in existing)) {
                      filtered.push(this.apps[j])
                  }

              }

              return filtered;
          },
          filteredUsers: function() {

              var filtered = [];
              var moderators_dict = {};

              for (var i = 0; i < this.systemModerators.length; i++) {
                  var mod = this.systemModerators[i];
                  moderators_dict[mod.moderator.id] = true;
              }

              for (var j = 0; j < this.users.length; j++) {

                  if (!(this.users[j].id in moderators_dict)) {
                      filtered.push(this.users[j]);
                  }

              }

              return filtered;

          },
      },
      mounted: function() {
          var urlInfo = this.extractURLInfo();

          this.projectID = urlInfo['projectID'];
          this.systemID = urlInfo['systemID'];
          this.loadApps();
          this.loadProject(urlInfo['projectID']);
          this.loadSystem(urlInfo['projectID'], urlInfo['systemID']);
          this.loadSystemApps(urlInfo['projectID'], urlInfo['systemID']);
          this.loadUsers();
          this.loadSystems(urlInfo['projectID']);
          this.loadModerators();
          this.loadDependencies();
      }
  });

});