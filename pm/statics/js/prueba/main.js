$(document).ready(function(){
						   
//  Settings for countdown date and time			   
						   
	$("#countdown").CountingDown({
		date: "01 August 2014 00:00:00"  // Enter your countdown date and time
	});
	
//===========================================================	

       jQuery("#subscribe").validationEngine({
		scroll: false,
		ajaxFormValidation: true,
		ajaxFormValidationURL: "contact/subscribe.php",
		onBeforeAjaxFormValidation: function () {
			$("#ajax").show();
		},
		onAjaxFormComplete: function () {
			$('#listo').html("<p>Thank you!</p>")
                .hide()
                .fadeIn(1000);
		}
	});
	 jQuery("#contact_form").validationEngine({
		scroll: false,
		ajaxFormValidation: true,
		ajaxFormValidationURL: "contact/contact.php",
		onBeforeAjaxFormValidation: function () {
			$("#ajax").show();
		},
		onAjaxFormComplete: function () {
			$('#listo1').html("<p>Thank you!</p>")
                .hide()
                .fadeIn(1000);
		}
	});
	 
	 
//===========================================================
	 
//--Settings for picassa gallery 


	jQuery('.picasagallery').picasagallery( {
		username: 'alan.hamlett',
		// Your Picasa public username
    hide_albums: [
			'Profile Photos',
			'Scrapbook Photos',
			'Instant Upload',
			'Photos from posts'
		],
		// hidden album names
    link_to_picasa: false,
		// true to display link to original album on Google Picasa
    thumbnail_width: '180',
		// width of album and photo thumbnails
    thumbnail_cropped: true,
		// use cropped format (square)
    title: 'Home ',
		// title shown above album list
    inline: false,
		// true to display photos inline instead of using the fancybox plugin
	});

//===========================================================
	 
//--Settings for twitter feeds

twitterFetcher.fetch('401283174652583936', 'example1',3, true);  // Enter twitter widget ID in '------' here 

function handleTweets(tweets){
    var x = tweets.length;
    var n = 0;
    var html = '<ul>';
    while(n < x) {
      html += '<li>' + tweets[n] + '</li>';
      n++;
    }
    html += '</ul>';
}



});