ivyMods.set_iEdit.blogSite = function(){

	var pageDescSettings = {
		modName: 'blogSite',
		saveBt: {
			attrValue: "save description",
			methName: "save_descPage"
		}
	};
	iEdit.add_bttsConf( {
		aboutDesc:  pageDescSettings,
		blogDesc: pageDescSettings,
		archiveDesc: pageDescSettings,
		sponsorsDesc: pageDescSettings,
		awardsDesc: pageDescSettings
	});
}

ivyMods.blogSite = {

    sel: {
       records: "*[class$=SGrecord] , *[class$=record]",
       recordArchive_content: "*[class~=SGrecord-archive] *[class$=content]:not(.ELMcontent)",
	    selectedFilters : 'filters-selected',
	    hoverFilters : 'filters-hover',
	    filtersPanel: function(filterId) {return "#" + filterId + "_panel"; }
    },
	//general usage
    showMoreText: function(){
	     $('*[id^=more]').on('showMore',function(){
		     //alert('in show more');
		     $(this).slideDown();
	     });
        $(".showMore").live('click',function ()
        {
            var moretext    = $(this).attr('id');
            var jqMoretext  = $("#"+moretext+"_text");
            var visibleStat = jqMoretext.is(':visible');

            if (visibleStat ==true) {

                jqMoretext.slideUp();
                $(this).html("More");

                var scrollAt = $(this).data('scrollat')
                //console.log("scrollAt "+scrollAt );
                $(window).scrollTop(scrollAt);

            } else {
                var scrollAt = $(window).scrollTop();
                //console.log("scrollAt "+scrollAt );
                $(this)
                    .html("Less")
                    .data('scrollat', scrollAt);
                //jqMoretext.slideDown();
	            jqMoretext.trigger('showMore');

            }
        });
    },

	 metricsImg: function(jqImgContainer, proportion){
		 // de la imgMetricsContainer
		 var imgMC = {};
		 imgMC.h = jqImgContainer.height();
		 imgMC.w = jqImgContainer.width();
		 imgMC.newH = imgMC.w / proportion;


	   /* console.log(' Container  ' );
	    console.log(' height = ' + imgMC.h);
	    console.log(' width = ' + imgMC.w);
	    console.log(' NEWheight = ' + imgMC.newH + '\n');*/
		 return imgMC;


	 },
	 /**
	 * Documenteaza!!!
	 * @param jqImg
	 * @param imgMC
	 * @param proportion
	 */
	 resizeImg: function(jqImg, imgMC, proportion) {

 		 //console.log("blacksea.js - resizeImg :poze gasite "+ jqImg.attr('src') );
		 jqImg.parent().css('height', imgMC.newH + 'px');

		 var imgProportion = jqImg.width() / jqImg.height();
		 if(imgProportion > proportion) {
		     jqImg.css('height', imgMC.newH + 'px');
	    }
	},
	 resizeImgContainer: function(selector,  proportion){
		//alert("resizeImgContainer cu "+proportion);
	   var imgs = $(selector +' img').reverse();
		var imgMC = this.metricsImg(imgs.first().parent(), proportion);
		imgs.each(function(){
			 //proportion = ~1.63157894737
		    ivyMods.blogSite.resizeImg($(this), imgMC, proportion);

	   });

   },

	 //specfic
	 resizeImgs_profile: function(){
		this.resizeImgContainer('.mainFeaturedImg-profilePhoto ', 219/125);
		$(window).resize(function() {
	      ivyMods.blogSite.resizeImgContainer('.mainFeaturedImg-profilePhoto ', 219/125);
      });
	 },
	 enforceStyling: function(){
     //toate elementele vor fi stripuite de style
     $(this.sel.records)
         .find('*[class$=content], *[class$=lead], *[class$=blogPrev-lead], *[class$=blogPrev-content]')
         .find('*').not('div,img').attr("style",'');
	 },

	 // i think this shoul be moved in blogRecord.js
	 /**
	 * stick bar ( use asset sticky.js)
	 * for css details look in blogSite.css
	 *
	 * @param selector - selectorul pe care se face sticky
	 * @param replaceClass - pt wraperul stickerului ,
	 * se va pune doar cand se face sticky
	 */
	 stickyBar: function(selector, stickyClass) {

		var jqSelector = $(selector);
		if(jqSelector.length) {
			jqSelector.sticky({
					getWidthFrom: $('#sticky-container'),
					wrapperClassName: 'wrapSticky',
					className: stickyClass,
					topSpacing: 35
				});
		}

	},
	 stickBars : function(){

		this.stickyBar('#sticky-archive', 'sticked-archive');
		this.stickyBar('#sticky-blog', 'sticked-blog');

		$('.topbar').sticky({
			getWidthFrom: $('body'),
			wrapperClassName: 'wrapSticky-topbar',
			className: 'sticked-topbar',
			topSpacing: 0
		});
	 },

    init: function (){
        this.showMoreText();
        this.enforceStyling();
	     // daca a fost inclus pluginul de sticky bar
	     if(typeof  $.fn.sticky == 'function') {
	   	   this.stickBars();
		  }

        this.resizeImgs_profile();



    }
};

$(document).ready(function() {

    ivyMods.blogSite.init();

    var PanelOpen = true;

    setTimeout(function(){
            $(".manifesttext").slideUp();
            $(".controlmanifest").html("Show manifesto");
            PanelOpen=false;
            }, 1000);

    setTimeout(function(){
            $("#chisinau").css("display", "block");
            }, 2000);

    setTimeout(function(){
            $("#baku").css("display", "block");
            }, 2700);

    $(".controlmanifest").click(function () {

        if (PanelOpen ==true) {
            $(".manifesttext").slideUp();
            $(this).html("Show manifesto");
            PanelOpen=false;
            $(".onTheMap").css("display","block");
        } else {
            $(".manifesttext").slideDown();
            $(this).html("Close manifesto");
            PanelOpen=true;
            $(".onTheMap").css("display","none");
            }

    });

  	 $(".onTheMap").hover(
  	 	function(){
  	 	    var place = $(this).attr('id');
  	 	    $("#"+place+"_place").show();
  	 	},
  	 	function () {
             var place = $(this).attr('id');
  	 	    $("#"+place+"_place").hide();
  	 	}
  	 );
    $(".mainFeaturedImg").hover(
       function(){
          var number=$(this).attr('id');
          $("#"+number+"_Thumb").show();
        },
    	  function () {
    	 	var number = $(this).attr('id');
    		$("#"+number+"_Thumb").hide();
       }
    );
});

