

$(document).ready(function(){



  var projectDetailVue = new Vue({
      el: '#projectDetailVue',
      mixins: [COMMON_MIXIN],
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
          
      },
      methods: {
          saveProject: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/",
                  type: 'PUT',
                  success: function(data) {
                      $.notify("Project saved.", "success");
                      that.project = data;
                  },
                  data: that.project
              });
          },
          addSystem: function() {
              var that = this;
              $.post("/api/v1/projects/" + this.projectID + "/systems/", that.systemForm, function(data) {
                  $.notify("System added.", "success");

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
          loadProjectApps: function() {
              var that = this;
              $.ajax({
                  url: "/api/v1/projects/" + this.projectID + "/apps/",
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
                  $.notify("Application added.", "success");
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

                      $.notify("Application removed.", "info");
                  }
              });
          },
      },
      computed: {
          filteredApps: function() {
              return this.filterData(this.apps, this.projectApps, 'app.id');
          },
      },
      mounted: function() {
          var urlInfo = this.extractURLInfo();
          this.projectID = urlInfo['projectID'];
          this.loadProject();
          this.loadSystems();
          this.loadProjectApps();
          this.loadApps();
      }
  });

});