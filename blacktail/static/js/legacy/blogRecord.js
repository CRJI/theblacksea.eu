var art = {};
if( typeof ivyMods.blog == 'undefined'  ) {
    ivyMods.blog = { conf: { templateFile: ''} };
}

$.extend ( true, ivyMods.blog ,
{
 	 limitSet : 10,
	 templates: {
		subscribeForm:  "fw/LOCALS/blog/tmpl_bsea/tmpl/subscribeFormular.html"
	 },
    sel      : {
	    subscribeBtt: '#subscribeBsea',
       article:       'div[class$=SGrecord]',
       articlesBlog:  'div[class~=blogPrevRec]',
       getNext_blogRecords: "input[class$=getNext_blogRecords]",
	    blogSet:       function(blogSet){return '*[class^=blogSet_'+blogSet+'] '; },

	    records: "*[class$=SGrecord] , *[class$=record]",
       recordArchive_content: "*[class~=SGrecord-archive] *[class$=content]:not(.ELMcontent)",
       selectedFilters : 'filters-selected',
       hoverFilters : 'filters-hover',
       filtersPanel: function(filterId) {return "#" + filterId + "_panel"; }
    },
	 asyncRecords     : new fmw.asyncConf({
		restoreCore: true,
		dataSend: { modName: 'blog, handler', methName: 'blog_renderData' }
	}),
	 disqus_shortname : 'the-black-sea',
	 //used by onload_article
	 contSize   : {
		 //templateFileName: function(jqcont) {return containerul de referinta pt galleria}
		 'archiveRecord' : function(jqCont){return jqCont.jq;},
		 'blogRecord' :    function(jqCont){
			 var articleContent = jqCont.jq.find('*[class$=content][class^=EDeditor]');
			 return articleContent
		 }
	 },
	 /**
     * apeleaza functiile in functie de templateFileul afisat
     * @type {string}
     */
    tmplManager: {
	   'blog' :          'onload_blog' ,
	   'blogRecord' :    'onload_article',
	   'archiveRecord' : 'onload_article',
		'home':           'onload_home',
		'archive':        'onload_archive'
    },

    // ========================[ event Callbacks ]==============================
	 // archive -filters
	 removeallFilters: function(){
		 $(".imageColumn.filter").removeClass(this.sel.selectedFilters);
		 $(".imageColumn.filter").removeClass(this.sel.hoverFilters);
		 $(".filter_panel").hide();

	 },

	 selectFilter : function(jqFilter){
		 this.removeallFilters();
		 jqFilter.addClass(this.sel.selectedFilters);
		 var filterId = jqFilter.attr('id');
		 $(this.sel.filtersPanel(filterId)).show();

	 },

	 hoverFilter: function(jqFilter){
        if (jqFilter.hasClass(this.sel.selectedFilters)) {

        } else {
	        jqFilter.toggleClass(this.sel.hoverFilters);
        }
	 },

	 bindsFilters: function(){

		 this.selectFilter($('.'+this.sel.selectedFilters));
		 $(".imageColumn.filter").click(function(){
			 ivyMods.blog.selectFilter($(this));
		 });

		 $(".imageColumn.filter").hover(function () {
            ivyMods.blog.hoverFilter($(this));
	     });

	 },

	 //async load for blog articles
    bind_getNext_blogRecords: function(){

	      var loadButton = $(this.sel.getNext_blogRecords);

			loadButton.on('click', function(){

				// atentie se poate culege un vector cu toate datele
				var limitStart = $(this).data('blogLimitstart');
				var limitEnd   = $(this).data('blogLimitend');


				ivyMods.blog.asyncRecords
					.fnpost({"limitStart" : limitStart})
					.done(function(data){


						limitStart += 10;
						loadButton.data('blogLimitstart', limitStart);
						loadButton.parent().before(data);
						ivyMods.blog.set_articlesBlog(limitStart);

						console.log('limit start = '+limitStart + ' limit end = '+limitEnd);
						if(limitStart >= limitEnd) {
							loadButton.next('input[class$=go-topPage]').css('display', 'block');
							loadButton.remove();
						}
					});
				return false;
			});

     },

	 //pt article - comentarii
    disqus_add: function(){
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = '//' + this.disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    },

	 // ================================[ managers ]==============================
    // article
	 resizeMedia_article: function(jqCont){
		 //resizing pics - so they mach the design
		  jqCont.resizeContentPics(jqCont);

        //resizing iframes
        if(jqCont.iframes.length) {

	        jqCont.resize_iframes();
            $(window).resize(function() {
	            jqCont.resize_iframes();

            });
        }
        $(window).resize(function() {
	        jqCont.resizeContentPics();
        });
	 },

	 galleries_article: function(jqCont){
		  // incarca galleria
        Galleria.loadTheme('/assets/galleria/themes/twelve/galleria.twelve.min.js');

        /**
        * daca imaginile gasite sunt > 3 atunci  le facem thumbnailuri si gallery
        * #1 - altfel va fi un spatiu gol daca nu sunt poze
        * #2 - seteaza galeia cu adaugare de thumbnailuri , si create galeria
        */
        if(jqCont.imgs.length >= 3){
            // #1
           jqCont.colectorPics.addClass('space');
           // #2
	        jqCont.galleria.set_containerPics();
        }

         /**
        * daca exista o astfel de functie declara printr-un js inclus
        * va fi apelata ( aici ex: in archivePhotoStory.js
        */
         if(typeof this.manageArticle == 'function') {
            this.manageArticle(jqCont);
         }

        // manage galleries inside article
		  jqCont.galleria.article( this.contSize[this.conf.templateFile](jqCont));

		  // set caption for photos from alt atribute
		  jqCont.captionContentPics();

	 },

	  /**
	 * la loadul unui articol de tip archive/story sau blog
	 */
 	 onload_article: function(){
        // prepare article
        var article = $(this.sel.article)
        if(!article.exists()) {
	        return ;
        }
        // ia datele despte articol
		  var jqCont = new ivyMods.blogArticle(article);

		  this.galleries_article(jqCont);
		  this.resizeMedia_article(jqCont);

        // adauga api-ul de commenturi
   	  if(jqCont.liveEditStat == 0){
			  this.disqus_add();
		  }
	 },

	 //multiple articles
	 /**
	 * la loadul mai multor articole in cazul articolelor din blog
	 * @param blogSet
	 */
	 set_articlesBlog: function(blogSet){

      // blogset = setul de articole , see: blogRecords.html
		 var articlesBlog = $(this.sel.blogSet(blogSet)+this.sel.articlesBlog);
       if(articlesBlog.length == 0) {
	       return ;
       }
       Galleria.loadTheme('/assets/galleria/themes/twelve/galleria.twelve.min.js');
       //Galleria.loadTheme('/assets/galleria/themes/classic/classic.twelve.min.js');

       articlesBlog.map(function()
       {
          var jqCont = new ivyMods.blogArticle($(this));

	       /**
	        * daca imaginile gasite sunt > 3 atunci le facem thumbnailuri si gallery
	        */
           if(jqCont.imgs.length >= 3){
	           jqCont.galleria.set_containerPics();
           }

           // manage galleries inside article
           jqCont.jq
              .find('.blogPrev-content')
                 .on('showMore.gallery',function(){
                    //alert('galleries_articlesBlog '+jqont.galleriaID);
                    $(this).off('showMore.gallery');
		           jqCont.galleria.article( $(this));
                 });

           // set caption for photos
           jqCont.captionContentPics();

           //resizing iframes
           if(jqCont.iframes.length) {
	           jqCont.resize_iframes();
           }
       });

	 },

  	 onload_blog : function(){
		 this.set_articlesBlog('unpublished');
	    this.set_articlesBlog(10);
	    this.bind_getNext_blogRecords();
	 },

    // archive - thumbPictures
	 resizeTumbs_archive: function(){
		 //alert('s-a loadat arhiva sau home si avem sau nu ac');
       ivyMods.blogSite.resizeImgContainer('.mainFeaturedImg > a > ', 248/152);
       $(window).resize(function() {
          ivyMods.blogSite.resizeImgContainer('.mainFeaturedImg > a > ', 248/152);
       });
	 },

	 onload_archive: function(){
		this.resizeTumbs_archive();
		this.bindsFilters();
	 },

	 subscribeButton : function(){
		 $(ivyMods.blog.sel.subscribeBtt).bind('click',
			 function(){
				 //alert('butonul de subscribe a fost apasat');
			  fmw.popUp.init({
            pathGet:  ivyMods.blog.templates.subscribeForm,
            headerName: "Newsletter subscribe",
            widthPop: 350
         });
		 });
	 },

	 onload_home: function(){
		 this.resizeTumbs_archive();
		 this.subscribeButton();
	 },

    init: function(){
	    //console.log('managerul = '+this.tmplManager[this.conf.templateFile]);
	    var manager = '';
	    eval('manager = this.'+this.tmplManager[this.conf.templateFile]);
	    //console.log("manager = "+ manager);

	    if(typeof manager == 'function') {
		    manager.call(this);
	    }
    }
}
);

$(document).ready(function(){
    ivyMods.blog.init();
});


