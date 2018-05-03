ivyMods.blogArticle = function(jqContainer){

	// ============================[ methods or collection of methods ]==========
	/**
	 * returneaza un array cu datele despre imaginile gasite in content
	 * @param jqCont
	 * @returns {Array}
	 */
	var get_RecordPics = function(){
		var recordPics = new Array();
      var src = '';
      var alt = '';
      var srcBig = '';

		//console.log("get_RecordPics");
      imgs.map(function(){

		       srcBig = $(this).attr('src');
             src    = srcBig.replace(sel.basePathPic, sel.thumbPathPic);
             alt    = $(this).attr('alt');
		       /*console.log(" 1img = "+ $(this).attr('src')
              +  ' '
              + ' sel.basePathPic = '
              + sel.basePathPic
             );*/

             recordPics.push( {srcBig: srcBig, src: src, alt: alt} );

	      });
		//console.log("nr.recordPics = "+ recordPics.length);
      /*var test = '';
      alert(recordPics.length);
      for( var key in recordPics) test += recordPics[key]+'\n\n';
      alert(test);*/

      return recordPics;
	};
	var set_recordPicsExif = function(){


	};
	var galleria = {
		jq: {},

		metrics: function(article){
			var  metrics = {};
			metrics.width  = article.width();
			metrics.height = (metrics.width*0.65)+31;
			//console.log('metrics width x height = '+ metrics.width + 'x'+ metrics.height);
			if(metrics.width && metrics.height) {
				return metrics;

			} else{
				return false;
			}

		},

		refreshMetrics: function(article){

			var metrics = this.metrics(article);
			$('*[id^=gallery-container-]').map(function(){
				$(this).widthHeight(metrics.width, metrics.height);
			});
		},

		popupMetrics : function(){

			/*alert('a ajuns pana aici ');*/

			 var marginLeft = galleria.jq.width() / 2;

			 var scrollTop = $(window).scrollTop();
			 var top = (window.innerHeight - this.jq.height()) / 2 + scrollTop - 50;

			 this.jq.css('margin-left', marginLeft);
			 this.jq.css('top', top);

		},

		create :  function(){

			 colectorPics.find("a").on('click', function(){

				 // =========================[ construieste dom-ul pt galleria ]====
				 /**
				  * Testeaza si retine cea mai mare inaltime
				  * ( intre cea a browserului si cea a lui body)
				  * @type {Number}
				  */
				 var windowHeight = window.innerHeight;
				 var bodyHeight = $('body').height();
				 var canvasHeight = windowHeight > bodyHeight ? windowHeight : bodyHeight;

				 /**
				  * Adauga partea de dom in care va sta galleria
				  */
				 $('body').append(
	             "<div id='galleria-container'>" +
		             "<div id='galleria-canvas' style='height: "+canvasHeight+"px; '></div>" +
	                "<div id='galleria' ></div>" +
	             "</div>"
	          );

				 //==============================[ start galleria ]=================
				 /**
				  * Apeleaza si configureaza galeria
				  * - sa porneasca de la imaginea care a fost apasata
				  * - sa preia imaginile sursa din containerul de imagini sursa
				 * */
				 var indexImage = $(this).data('indexImage');
				 //console.log('createGalleria - indexImage = '+indexImage);
				 Galleria.configure({
					 show: $(this).data('indexImage')
				 });

				 Galleria.run('#galleria',{
					 dataSource: '#'+galleriaID,
					 imageCrop: false,
                     idleMode: false,
					 fullscreenCrop: false
				 });

				 /**
				  * ==========================[resize galleria]=====================
				 *  cumva nu imi merge functia asta nu stiu de ce???
				 */
				 this.jq = $('#galleria');

				 // galleria.popupMetrics();
				 var marginLeft = this.jq.width() / 2;

				 var scrollTop = $(window).scrollTop();
				 var top = (window.innerHeight - this.jq.height()) / 2 + scrollTop - 50;

				 this.jq.css('margin-left', marginLeft);
				 this.jq.css('top', top);

				 /**
				  * close button
				  * adauga butonul de closeGalleria care va face remove la tot domul de galleria
				  */
				 this.jq.prepend(
					 "<div class='galleria-bar-close'>" +
						 "<input type='button' class='' value='close' id='galleria-close'" +
						 " onclick=\"$('#galleria-container').remove();\">" +
					 "</div>"
				 );

				 // stop from bubbling
				 return false;

			 });
		},

		get_tmplThumbPics : function() {

		    /**
		     * <div id="galleria">
		         <a href="/img/large1.jpg"><img src="/img/thumb1.jpg" data-title="My title" data-description="My description"></a>
		         <a href="/img/large2.jpg"><img src="/img/thumb2.jpg" data-title="Another title" data-description="My <em>HTML</em> description"></a>
		     </div>

		     using:
		     recordPics.push( {srcBig: srcBig, src: src, alt: alt} );

		     */
	        var htmlPics = '';
		     var indexImage = 0;
	        for( var key in recordPics) {
	            htmlPics += "<a class='container-photoThumbs' " +
	                            "' href='" + recordPics[key].srcBig + "'" +
	                            " data-index-image='"+indexImage+"'"+
		                      ">" +
	                                "<img class='photoThumbs' " +
	                                    "src='" + recordPics[key].src + "'" +
	                                    "data-title='" + recordPics[key].alt + "' " +
	                                 //   "data-description='" + recordPics[key].alt + "' " +
		                              "/>" +
	                        "</a>" ;
		        indexImage++;
	        }
	        //alert(htmlPics);
	        return htmlPics;
      },

		set_thumbPics: function(){

	     // seteaza html-ul pozelor
       var htmlThumbPics = this.get_tmplThumbPics();

        // ascunde pozele care trec de 9
        colectorPics
	        .append(htmlThumbPics).find('*[class^=container-photoThumbs]:gt(8)').hide();

      }
	};

	// ============================[ properties and collections of props ]=======
	//defaults
	var css =  { cls: { picCaption: 'storyCaption' }, ids: {} };
	var limitSet = 10;
	var sel =  {
        basePathPic : "/RES/uploads/images/",
        thumbPathPic : "/RES/uploads/.thumbs/images/",
        colectorPics : '*[class$=thumbRecordPics]',
	     sideContent:      "*[class$=pulledQuotes]",
		  containers:    '*[class$=lead] , *[class$=content]',
		  //[class^=EDeditor] inportant deoarece altfel va face ref la ELMcontent
        imgs:          '*[class$=lead] img, *[class$=content]:not(.ELMcontent) img',
        iframes:       '*[class$=lead] iframe, *[class$=content]:not(.ELMcontent) iframe',
        article:       'div[class$=SGrecord]',
        articlesBlog:  'div[class~=blogPrevRec]',
	     blogSet:       function(blogSet){return '*[class^=blogSet_'+blogSet+'] '; },
        // gallery :      '*[class$=thumbRecordPics] a.fancybox',
        galleria :      '*[class$=thumbRecordPics]',
        liveEdit:      '.ELMcontent',
        adminAuthors: 'form #adminAuthors',
	     getNext_blogRecords: "input[class$=getNext_blogRecords]",
	     content: "*[class$=content]"
   };

   //obtained
	var jq           =  jqContainer;
	var containerWidth = jq.width();
	var containers   =  jqContainer.find(sel.containers).not('.ELMcontent');
	//alert('containers = ' + containers.length  );
	// imaginile din interiorul contentului si leadului
	var imgs       =  containers.find('img');
	var imgsResize = imgs.map(function(){
		 var imgWidth =  $(this).width();
	    if(imgWidth > (containerWidth/4)*3){
		    return this;
	    }
	});


	console.log("imgs found = "+imgs.length);
	//var imgs         =  containers.find('img');
	// iframeurile din content si lead ex: youtube etc..
	var iframes      =  containers.find('iframe');
	// unde anume vor fi puse imaginile thumbnal
	var colectorPics =  jqContainer.find(sel.colectorPics);
	// id-ul galleriei din cadrul containerului
	var galleriaID   =  jqContainer.find(sel.galleria).attr('id');
	var liveEditStat =  jqContainer.find(sel.liveEdit).length;
	// preia json cu pozele pt galerie
	var recordPics   = get_RecordPics();

	//=========================== [public properties and methods]================
	return {
		htmlThumbPics: '',
	   jq: jq,
	   imgs : imgs,
		imgsResize : imgsResize,
		iframes : iframes,
	   colectorPics: colectorPics,
	   galleriaID : galleriaID,
	   liveEditStat: liveEditStat,
	   recordPics : recordPics,
		limitSet : limitSet,
		css: css,
	   sel: sel,

		galleria: {
			//set_containerPics_galleria: function(){
			set_containerPics: function(){
		     //thumb pics
		     galleria.set_thumbPics();
		     galleria.create();
		   },
			//on window resize
			refreshMetrics: function(article){

				var metrics = this.gallery_metrics(article);
				$('*[id^=gallery-container-]').map(function(){
					$(this).widthHeight(metrics.width, metrics.height);
				});
			},
			article: function(jqContent){

				var counter = 1;
				var metrics = galleria.metrics(jqContent);
				if(!metrics) return ;

				/*console.log("Metrics for "+galleriaID +" width + height =   "
					+metrics.width+' '+ metrics.height);*/

				jq.find('.gallery').map(function(){
					 var idGallerySub = 'gallery-container-'+galleriaID+'-'+counter;
					 $(this).clone()
						.attr('id', idGallerySub)
						.removeClass('gallery')
							.insertBefore($(this));

					 // resize gallery
					$('#'+idGallerySub).widthHeight(metrics.width, metrics.height);

					 //refresh gallery size
					var obj = galleria;
					$(window).resize(function(){
						obj.refreshMetrics(jqContent);
					});
					 //run gallery
					Galleria.run('#'+idGallerySub, {
                        imageCrop: false,
                        idleMode: false
                    });
					counter++;
				});
		   }
		},
	   /**
	   * set alt atribute as caption for images according to the design
	   * and only if the site is not in liveEdit state
	   * @param jqCont
	   */
      captionContentPics: function(){

        if(liveEditStat != 0) return;
        imgs.map(function(){
             var caption = $(this).attr('alt');
             if(caption) {
                 var cls = css.cls;
                 $(this).after(
                    "<div class='"+ cls.picCaption+"'>"
                        +caption
                    +"</div>"
                 );
             }
        });

    },
      resize_iframes: function(){

	    var containerWidth = jq.width();
	    var width = 560;
       var height = 315;
       var proportion =   height/width;

       iframes.map(function(){
	       var ifClass = $(this).attr('class');

	       if($(this).hasClass("fullScreen")) {

		       var windowWidth = window.innerWidth;
		       var marginRight = (containerWidth - windowWidth) / 2;
		       //alert("windowWidth = "+ windowWidth + " marginRight = "+marginRight);
		       $(this).width(windowWidth);
		       $(this).css('margin-right', marginRight);
	       } else {
	            $(this).width(containerWidth);
               $(this).height(containerWidth * proportion);
	       }
	        $(this).addClass('pull-right');
           /* console.log(
                  "container = " + containerWidth
                + "\n height = " + (containerWidth * proportion)
                +"\n"
            );*/
       });
    },
      resizeContentPics: function(){
        console.log("Resized pics | containerWidth " + containerWidth );
	      imgsResize.map(function()
        {
	        //console.log("containerwidth "+containerWidth);

	         var imgWidth =  $(this).width();
	         //if(imgWidth > (containerWidth/4)*3){
		         console.log("image width " + $(this).attr('src') + ' = ' + $(this).width());
		         $(this).css('height','initial');
		         $(this).width(containerWidth);
		         $(this).addClass('pull-right');
	         //}

        });
    }
	}
};
