
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