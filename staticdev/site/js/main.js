
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