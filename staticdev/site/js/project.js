

$(document).ready(function(){

  var projectDetailVue = new Vue({
      el: '#projectDetailVue',
      data: {
          projectID: null,
          systems: [],
          project: {
              name: '',
              description: ''
          },
          projectApps: [],
          selectedApp: '',
          appPosts: [],
          addAppForm: {
              app: '',
              project: '',
          },
          systemForm: {
              name: '',
              system_type: '',
              repo_info: '',
              environment_config: '',
              staging_info: '',
              production_info: '',
              api_info: '',
              documentation: '',
              deployment_type: ''
          },
          apps: [],
          deploymentTypes: MODELS.deploymentTypes,
          systemTypes: MODELS.systemTypes,
      },
      methods: {
          loadProject: function(projectID) {
              var that = this;
              $.get("/api/v1/projects/" + projectID, function(data) {
                  that.project = data;
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
          loadSystems: function(projectID) {
              var that = this;
              $.get("/api/v1/projects/" + projectID + "/systems/", function(data) {
                  that.systems = data['results'];
              });
          },
          saveProject: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/",
                  type: 'PUT',
                  success: function(data) {
                      alert("Saved!");
                      that.project = data;
                  },
                  data: that.project
              });
          },
          addSystem: function() {
              var that = this;
              $.post("/api/v1/projects/" + this.projectID + "/systems/", that.systemForm, function(data) {
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
                  projectID: path[path.length - 1 - trailingPad]
              };
          },
          loadProjectApps: function(projectID) {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + projectID + "/apps/",
                  type: 'GET',
                  success: function(data) {
                      that.projectApps = data['results'];
                  }
              });
          },
          onChangeSelectedApp: function($event) {
              if (this.selectedApp == '') {
                  return;
              }
              this.loadAppPosts();
          },
          setSelectedApp: function(app) {
              this.selectedApp = app;
              this.loadAppPosts;
          },
          loadAppPosts: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/apps/" + this.selectedApp.id + "/posts/",
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
          addApplication: function() {
              var that = this;
              var payload = {
                  app: this.addAppForm.app,
                  project: this.projectID
              }
              $.post("/api/v1/projects/" + this.projectID + "/apps/", payload, function(data) {

                  that.loadProjectApps(that.projectID);
                  $('#addApplicationModal').modal('hide');
              });
          },
          removeApplication: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/apps/" + this.selectedApp.id + "/",
                  type: 'DELETE',
                  success: function() {

                      that.selectedApp = '';
                      that.loadProjectApps(that.projectID);
                      $('#removeApplicationModal').modal('hide');
                  }
              });
          },
      },
      computed: {
          filteredApps: function() {
              var filtered = [];
              var existing = {};
              for (var i = 0; i < this.projectApps.length; i++) {
                  var projectApp = this.projectApps[i];
                  existing[projectApp.app.id] = true;
              }
              for (var j = 0; j < this.apps.length; j++) {
                  if (!(this.apps[j].id in existing)) {
                      filtered.push(this.apps[j])
                  }
              }

              return filtered;
          },
      },
      mounted: function() {
          var urlInfo = this.extractURLInfo();
          this.projectID = urlInfo['projectID'];
          this.loadProject(urlInfo['projectID']);
          this.loadSystems(urlInfo['projectID']);
          this.loadProjectApps(urlInfo['projectID']);
          this.loadApps();
      }
  });

});