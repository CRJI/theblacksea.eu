//DOAR FUNCTII GENERALE !!!! cu parametrii !!!!!

//==============================[ jQuery - extensions ]=====================================
// reverse an array's order

$.fn.widthHeight = function(width, height){
	this.width(width);
	this.height(height);
}

$.fn.reverse = [].reverse;

$.fn.collectData = function () {

	var selector = arguments.length > 0 ? arguments[0]
		: "input[type=text] ,input[type=hidden] ,input[type=checkbox], input[type=submit] , textarea, select";

	var data = {};
	if (this.length == 1) {

		this.find(selector).map(function () {
			var input_Name = $(this).attr('name');
			var input_Value = $(this).val();
			data[input_Name] = input_Value;
		});
		//console.log("Am apelat pluginul de jquery collectData ");
	} else {
		console.log("jquery - plugin  collectData dar au fost selectate 2 formuri");
	}

	return data;
}

$.fn.maxHeight = function () {

	var max = 0;
	this.each(
		function () {
			max = Math.max(max, $(this).height());
		}
	);
	return max;
}

$.fn.minHeight = function () {

	var min = 3000;
	this.each(
		function () {
			min = Math.min(min, $(this).height());
		}
	);
	return min;
}

$.fn.exists = function () {
	return this.length !== 0;
}

/**
 * source can be:
 * --------------------
 *
 * - object
 * 1. source = [ {'label': 'calatorii', 'value': '1'},{}];
 *
 * 2. source = [ "calatorii", "caravana"];
 *
 * 3. source = {scriptPath: fwm.ajaxProxy,
 *              sendData: {ajaxReqFile: '', otherData}
 *             }
 * - string
 * 4. source = 'path to return json'
 *
 *
 * select can be:
 * ----------------------
 *
 *  multiple - source is a plain json
 *
 *  key => source = [{value: '', lable: ''}, {}, {}]
 *
 *  multipleKey - to be done ( like multiple + key );

 */
$.fn.ivyAutocomplete = function (source, minLength, select) {
	//console.log('constructor this ' +this.constructor);

	var jqThis = this;

	//======================================[ source ]==========================
	function split(val) {
		return val.split(/,\s*/);
	}

	function extractLast(term) {
		return split(term).pop();
	}

	function sourceRemote(request, response) {

		var searchTerm = extractLast(request.term);
		//console.log('sourceRemote request.term = '+request.term);

		// daca termentul cautat are cel putin caracterele necesare cerute
		if (searchTerm.length >= optAutocomplete.minLength) {
			$.post(
				source.scriptPath,
				$.extend(source.sendData, {searchTerm: searchTerm}),
				function (data) {
					// delegate back to autocomplete, but extract the last term
					if (data) {
						response($.ui.autocomplete.filter(data, searchTerm));
					} else {
						console.log('sourceRemote nu s-a primit nici un json pt autocomplete' +
							 " s-a apelat scritptul = " + source.scriptPath +
							' sendData.ajaxReqFile = ' + source.sendData.ajaxReqFile
						);
					}
				},
				"json"
			);
		}
	}

	function _handle_source() {

		//console.log('ivyAutocomplete sursa este '+ typeof source + ' si este  =  '+ source);
		if (typeof source == 'string') {
			return source;
		}
		if (typeof source == 'object') {

			if (typeof source.scriptPath != 'undefined'
				|| typeof source.sendData != 'undefined'
				) {
				var defSource = {path: fmw.ajaxProxy, sendData: {}};
				$.extend(true, source, defSource);
				return sourceRemote;

			} else {
				return source;
			}
		}
		console.log("_handle_source : Nu s-a gasit o sursa");
		return false;
	}

	//=======================================[ select ]=========================
	function selectMultiple(event, ui) {
		var terms = split(this.value);
		// remove the current input
		terms.pop();
		// add the selected item
		terms.push(ui.item.value);
		// add placeholder to get the comma-and-space at the end
		terms.push("");
		this.value = terms.join(", ");
		return false;

	}

	function prepareSelectKey() {
		//console.log('constructor jqThis ' +jqThis.constructor);
		var inputName = jqThis.attr('name');
		var inputValue = jqThis.attr('value');
		jqThis.after(
			"<input type='hidden' value='' name='" + inputName + "'>"
		);
		jqThis.attr('name', inputName + "_dummy");

	}

	function selectKey(event, ui) {
		this.value = ui.item.label;
		var inputName = this.name.replace('_dummy', '');
		$('input[type=hidden][name=' + inputName + ']').val(ui.item.value);

		return false;
	}

	function _handle_select() {
		if (typeof select == 'undefined') {
			return false;
		}
		if (select == 'multiple') {
			return selectMultiple;
		}
		if (select == 'key') {
			prepareSelectKey();
			return selectKey;
		}
		return false;
	}

	//=======================================[ optAutocomplete ]================
	var optAutocomplete = {};

	var sourceStat = _handle_source();
	if (sourceStat) {
		optAutocomplete.source = sourceStat;
	}

	var selectStat = _handle_select();
	if (selectStat) {
		optAutocomplete.select = selectStat;
	}

	optAutocomplete.minLength = (typeof minLength == 'undefined') ? ''
		: minLength;

	optAutocomplete.focus = function () {
		return false;
		/* prevent value inserted on focus */
	}


	//=======================================[ ui-autocomplete ]================
	// don't navigate away from the field on tab when selecting an item
	this
		.bind("keydown", function (event) {
			if (event.keyCode === $.ui.keyCode.TAB &&
				$(this).data("autocomplete").menu.active) {
				event.preventDefault();
			}
		})
		.autocomplete(optAutocomplete);

	/**
	 * // un exemplu cu array predefinit
	 source: function( request, response ) {
           // delegate back to autocomplete, but extract the last term
           response( $.ui.autocomplete.filter(
               availableTags, extractLast( request.term ) ) );
       },
	 */

}

//==============================[ ivyMods ]=====================================
/* Aici vor sta functiile modulelor */
// pus in core / footer
if (typeof ivyMods == 'undefined') {

	var ivyMods = {
		set_iEdit: {
			//modName : function(){}
		}
	};
}

//=============================[ framework related functions ]==================
var fmw = {};

fmw.admin = 0;
fmw.idT = 0;
fmw.idC = 0;
fmw.lg = 'ro';
fmw.urlGet = {};
fmw.ajaxProxy = 'procesSCRIPT.php';
fmw.ajaxReqFile = 'ajaxReqFile';
fmw.sessionId = $.cookie("PHPSESSID");
//console.log("sessionId " + fmw.sessionId );
fmw.pubPath = '';
fmw.liveEdit = false;
/**
 * fmw.pubUrl
 */

/**
 * Use case :
 *  <input type='button'  value='more settings' onclick='fmw.toggle(\"form[id^=EDITform] .admin-extras\"); return false;' />
 *
 * @param selection - will toggle the selection requested
 * @return {Boolean}
 */
fmw.toggle = function (selection, opt) {
	/**
	 * opt : {
     *  caller : '',
     *  class: [classClick,  class ],
     *  value: [valueClick, valueDef]
     *  }
	 */
	opt = fmw.isset(opt) ? opt : {};
	var defaults = {
		caller: '',
		class: ['', ''],
		value: ['', '']

	};


	$(selection).toggle();
	$.extend(true, opt, defaults);

	if (opt.caller != '') {
		var visible = $(selection).is(":visible");
		//console.log("element is "+ (visible ? "visible" : "notvisible"));

		if (opt.class != '') {
			opt.caller.attr('class', (visible ? opt.class[1] : opt.class[0]));
			//console.log( opt.selector.attr('class') + " "+ opt.class[1]);
		}

		// in cazul acesta se presupune din prima ca callerul este un input
		if (opt.value != '') {
			opt.caller.attr('class', (visible ? opt.value[1] : opt.value[0]));
		}

	}
	return false;
}
fmw.isset = function (variable) {
	if (typeof  variable == 'undefined') {
		return false;
	} else {

		return true;
	}
}
// not working good dont know yet why
fmw.notempty = function (variable) {
	if (!fmw.isset(variable)) {
		return false;
	}
	if (variable == 0 || variable == '') {
		return false;
	}
	return true;
}

fmw.asyncConf = function (options) {

	/**
	 * options:
	 - dataSend: {
            ajaxReqFile : '', //direct file to access
            modName: '',
            methName: ''
      }
	 - callBack :  {fn: '',context: this, args: []}
	 - restoreCore : true /false
	 * */

	this.callBack = {"fn": 'dummy', "context": this, "args": []};
	this.restoreCore = false;
	this.dataSend = {};
	$.extend(true, this, options);

	if (this.restoreCore) {
		this.dataSend.sessionId = fmw.sessionId;
	}

	// ================================[ methods ]===============================
	this.callBackFn = function (callBack, data) {

		//console.log("GEN.js - tring to callback " + data);
		if (!fmw.isset(callBack)) {
			callBack = {};
		}
		callBack = $.extend(true, {}, this.callBack, callBack);

		if (typeof callBack.fn == 'function') {

			//console.log("callBackFn: is a function function "+ callBack.fn);

			callBack.args.push(data);
			callBack.fn.apply(callBack.context, callBack.args);
		} else {
			console.log("callBackFn: not a function function " + callBack.fn
				// + "\n data primita = "+ data
			);
		}
	}
	/**
	 * use case:
	 *
	 * var asyncsConf = new fmw.asyncConf({...});
	 * asyncConf
	 *    .fnpost(postData, callBack)
	 *    .done(function(data{}));
	 *
	 * @param dataSend
	 * @param callBack
	 * @returns {*}
	 */
	this.fnpost = function (dataSend, callBack) {

		if (!fmw.isset(dataSend)) {
			dataSend = {};
		}
		dataSend = $.extend(true, {}, dataSend, this.dataSend);
		//console.log(dataSend);

		var thisObj = this;
		var jqxhr = $.post(fmw.ajaxProxy, dataSend, function (data) {

			thisObj.callBackFn.call(thisObj, callBack, data);
			//console.log("GEN.js - apparantly it works");
		});

		return jqxhr;
	}
	this.fnload = function (jQmod, dataSend, callBack) {

		if (typeof jQmod == 'undefined') {
			console.log("fmw.asyncConf - Selectorul folosit nu a fost bun");

		} else {
			if (!fmw.isset(dataSend)) {
				dataSend = {};
			}
			var thisObj = this;
			dataSend = $.extend(true, {}, dataSend, this.dataSend);
			jQmod.load(fmw.ajaxProxy, dataSend, function () {
				thisObj.callBackFn(callBack);
			});
		}
	}

}
fmw.KCFinder_popUp = function (options) {

	/**
	 * opt= { callBackFn, jqmod_img }
	 * */
	var defaults = {
		callBackFn: '',
		jqmod_img: ''
	}
	var opt = $.extend(true, {}, defaults, options);

	window.KCFinder = {
		callBack: function (url) {
			//field.value = url;
			console.log("fmw.KCFinder_popUp - " + url);
			if (typeof opt.callBackFn == 'function') {
				opt.newUrl = url;
				opt.callBackFn.call(this, opt);
			} else {
				// carrousel callback function
				console.log("fmw.KCFinder_popUp - " + 'functia cu numele '
					+ opt.callBackFn + ' nu exista'
				);
				/*   if(opt.jqmod_img != '')
				 {
				 //alert(opt.jqmod_img.attr('src'));
				 opt.jqmod_img.attr('src',url);
				 }*/
				popUp_remove();
				window.KCFinder = null;
			}
		}
	};

	//@todo: schimbat pe noul fmw.popup
/*	var popUpKCF = new popUp_call(
		{ content: "<div id='kcfinder_div'>" +
			'<iframe name="kcfinder_iframe" src="/assets/kcfinder/browse.php?type=images" ' +
			'frameborder="0" width="100%" height="450px" marginwidth="0" marginheight="0" scrolling="no" />' +
			"</div>",

			widthPop: '900', heightPop: '500'
		});*/
	fmw.popUp.init(
	{ content: "<div id='kcfinder_div'>" +
			'<iframe name="kcfinder_iframe" src="/assets/kcfinder/browse.php?type=images" ' +
			'frameborder="0" width="100%" height="450px" marginwidth="0" marginheight="0" scrolling="no" />' +
			"</div>",

			widthPop: '900', heightPop: '500'
	});


	//fmw.popUp.  popUp_content

	// variabila popUPKCF - poate ar trebui sa ii dau unset somehow

}
fmw.openKCFinder_popUp = function (callBackFn) {

	window.KCFinder = {
		callBack: function (url) {
			//field.value = url;
			console.log("fmw.openKCFinder_popUp" + url);
			if (callBackFn != '') {
				if (typeof callBackFn == 'function') {
					callBackFn.call(this, url);  // carrousel callback function

				} else {
					console.log("fmw.openKCFinder_popUp" + ' - functia cu numele '
						+ callBackFn + ' nu pare sa fie o functie declarata'
					);
				}
			}
			popUp_remove();
			window.KCFinder = null;
		}
	};
	//@todo: pune pe noul pop-ul al frameworkului
	var popUpKCF = new popUp_call(
		{ content: "<div id='kcfinder_div'>" +
			'<iframe name="kcfinder_iframe" src="/assets/kcfinder/browse.php?type=images" ' +
			'frameborder="0" width="100%" height="450px" marginwidth="0" marginheight="0" scrolling="no" />' +
			"</div>",

			widthPop: '900', heightPop: '500'
		});

	// variabila popUPKCF - poate ar trebui sa ii dau unset somehow

}
fmw.queryData = function (queryString) {
	/*

	 QueryData.js

	 A function to parse data from a query string

	 Created by Stephen Morley - http://code.stephenmorley.org/ - and released under
	 the terms of the CC0 1.0 Universal legal code:

	 http://creativecommons.org/publicdomain/zero/1.0/legalcode

	 */

	/* Creates an object containing data parsed from the specified query string. The
	 * parameters are:
	 *
	 * queryString        - the query string to parse. The query string may start
	 *                      with a question mark, spaces may be encoded either as
	 *                      plus signs or the escape sequence '%20', and both
	 *                      ampersands and semicolons are permitted as separators.
	 *                      This optional parameter defaults to query string from
	 *                      the page URL.
	 */
	// if a query string wasn't specified, use the query string from the URL
	if (queryString == undefined) {
		queryString = location.search ? location.search : '';
	}

	// remove the leading question mark from the query string if it is present
	if (queryString.charAt(0) == '?') queryString = queryString.substring(1);

	// check whether the query string is empty
	if (queryString.length > 0) {

		// replace plus signs in the query string with spaces
		queryString = queryString.replace(/\+/g, ' ');

		// split the query string around ampersands and semicolons
		var queryComponents = queryString.split(/[&;]/g);

		// loop over the query string components
		for (var index = 0; index < queryComponents.length; index++) {

			// extract this component's key-value pair
			var keyValuePair = queryComponents[index].split('=');
			var key = decodeURIComponent(keyValuePair[0]);
			var value = keyValuePair.length > 1
				? decodeURIComponent(keyValuePair[1])
				: '';


			// altered by Ioana
			if (typeof this[key] == 'undefined') {
				// store the value
				this[key] = value;

			} else if (typeof this[key] == 'object') {
				// daca este obiect => este array
				this[key].push(value);

			} else {
				// daca nu este undefined si nu este inca obiect
				var man = this[key];
				delete this[key];
				this[key] = [];
				this[key].push(man);
				this[key].push(value);
			}

		}

	}

}

fmw.popUp = {
	/**
	 * CALL it like this
	 *
	 *  fmw.popUp.init(
	 *    {
     *
     *     // optional
     *
     *      pathGet
     *       pathLoad: ''
     *       dataSend: ''
     *       procesSCRIPT : ''
     *
     *     // properties
     *
     *       headerName  : ''
     *       widthPop    : ''
     *       heightPop   : ''
     *       completeFunc: ''
     *
     *       content     : ''
     *  })
	 * */
	/*MAN's
	 *
	 * // un template care are nevoie de o randare complexa
	 * // ex: acces la alte module, la BD etc...
	 * // de aceea e posibil sa fie nevoie de core => procesSCRIPT
	 *
	 * opt.pathLoad
	 * opt.dataSend {ajaxReqFile : '', alteVars: '', modName: '', methName: ''}
	 * opt.ajaxProxy
	 *
	 * //un template care trebuie sa ii fie luat asa cum este
	 * // ii se poate trimite si un dataSend
	 *
	 * opt.pathGet
	 * opt.dataSend
	 *
	 * opt.callbackFn: {
	 *   fn: 'functia',
	 *   context: 'obiectul in care sa fie cotextul',
	 *   args: 'lista/ array cu argumentele trimise catre functie'
	 *   }
	 *
	 * */

	init: function (opt) {

		// properties
		/*
		 this.headerName   = opt.headerName;
		 this.widthPop     = opt.widthPop;
		 this.heightPop    = opt.heightPop;
		 this.callbackFn  = opt.callbackFn;
		 this.content      = opt.content;
		 this.draggable    = opt.draggable
		 */

		//this.popUp_loadContent ;//???
		// defaults
		this.popUp_remove();
		this.ajaxProxy = fmw.ajaxProxy;
		this.closeBtn = 'button'; // or it could be submit
		this.dataSend = { sessionId: fmw.sessionId};
      this.draggable = false;

		// incorporate options
		$.extend(true, this, opt);

		//______________________________________[ set html TMPL]_________________________________________________

		this.popUp_set_htmlTml();
		//console.log(this.popUpContent);
		// ini stuff
		if (typeof this.content != 'undefined') {
			this.popUp_content(this.content);
			//console.log(this.content);
		} else if (typeof opt.pathGet != 'undefined') {

			var dataSend = typeof opt.dataSend == 'undefined' ? '' : opt.dataSend;
			//console.log('GEN.js - Datele trimise'+ dataSend);
			$.get(opt.pathGet, dataSend, function (data) {
				fmw.popUp.popUp_content(data);
			});

		} else {

			//Daca scriptul meu de process este acelasi cu cel default atunci facem aranjamentele necesare
			/*  this.ajaxProxy = (typeof opt.ajaxProxy != 'undefined' || typeof opt.ajaxProxy == 'null' )
			 ? opt.ajaxProxy
			 : fmw.ajaxProxy;

			 this.dataSend = { sessionId : $.cookie("PHPSESSID")};
			 this.dataSend     = opt.dataSend instanceof object
			 ? opt.dataSend
			 : {};

			 this.dataSend     = (this.ajaxProxy == fmw.ajaxProxy && typeof opt.ajaxReqFile != 'undefined')
			 ? $.extend(this.dataSend, {ajaxReqFile : opt.ajaxReqFile})
			 : this.dataSend;*/

			this.popUp_load();
		}
	},
	popUp_load: function () {

		/* var testSendData = '';
		 for(var i in this.dataSend) {
		 testSendData += " name = "+ i + "value = "+ this.dataSend[i] + '\n';
		 }*/
		//_____________________________________[ set load ]__________________________________________________
		/* console.log('ajaxProxy '+this.ajaxProxy
		 + '\n\n dataSend '+ testSendData
		 + '\n\n ajaxReqFile '+this.ajaxReqFile
		 //  + '\n\n completeFunc '+this.completeFunc + ' length'+this.completeFunc.length
		 //   + '\n\n type '+(typeof this.completeFunc)
		 );*/

		// pentru ca this is not in the scope inside setTimeout function
		var mod = this;
		setTimeout(function () {
			$('#popUp #popUp-content')
				.load(
				mod.ajaxProxy,
				mod.dataSend,
				function () {
					mod.popUp_callback();
				}
			);
		}, 250);
		// alert( this.completeFunc);
	},
	popUp_content: function (content) {
		$.when(
				$('#popUp #popUp-content')
					.html(content)
			).then(
				this.popUp_callback()
			);

		// this.popUp_callback();
		//aceaasta procedura ar trebui pusa si ea intr-o metoda
		// callback function?
	},
	popUp_set_htmlTml: function () {
		var popUp =
			$('body').prepend
				("<div id='popUp-canvas'>" +
					"<div id='popUp'>" +
					"<div id='popUp-header'>" +
					"<span>" + this.headerName + "</span>" +
					(this.closeBtn == 'button'
						? "<input  type='button' value='x' id='popUp-close' onclick='fmw.popUp.popUp_remove();' class='close ivy'>"
						: "<input type='submit'  name= 'closePopup' value='close and refresh' class='close ivy' form='closePopup'  >" +
						   "<form method='post' action='' id='closePopup'></form>"

					)+

					"</div>" +
					"<div id='popUp-content'></div>" +
					"</div>" +
					"</div>")
				.find('#popUp');
		var popUpContent = popUp.find('#popUp-content');

		if (this.widthPop) {
			popUp.css('width', this.widthPop + 'px');
		}
		if (this.heightPop) {
			popUp.css('height', this.heightPop + 'px');
		}

		var popupContent_height = popUpContent.height() / 2;
		var topPopup = (window.innerHeight - popUp.height()) / 2 - 50;
		var margin_left = popUp.width() / 2;

		popUp.css('top', topPopup + 'px');
		popUp.css('margin-left', '-' + margin_left + 'px');


		//console.log(topPopup);
		popUpContent.append(
			"<img alt='preloader' src='fw/GENERAL/core/css/img/ajax-loader.gif' " +
				"style='display: block; margin: 0px auto; padding-top:" + popupContent_height + "px;'>");

		// daca am setat optiunea de draggable ( atentia aceasta necesita jqueryUI.draggable)
		if(this.draggable) {
			popUp.draggable();
		}

		/*console.log("popUp \n" +
		 " width = " + popUp.width() + "\n" +
		 " height = " + popUp.height() + "\n" +
		 " windowH = " + $(window).height() + "\n" +
		 " topPopup = " + topPopup + "\n\n"
		 );*/

		//return popUpContent;
	},
	popUp_remove: function () {
		//alert('in Remove popUp');
		//alert('Am reusit sa selectez '+$('body #popUP-canvas').attr('id'));
		$('body #popUp-canvas').remove();
	},
	popUp_callback: function () {
		// alert('this is the callBack '+ this.completeFunc);
		if (typeof this.callbackFn != 'undefined'
			&& typeof this.callbackFn.fn == 'function') {
			var context = this;
			var args = [];
			if (typeof this.callbackFn.context != 'undefined') {
				context = this.callbackFn.context;
			}
			if (typeof this.callbackFn.args != 'undefined') {
				args = this.callbackFn.args;
			}


			this.callbackFn.fn.apply(context, args);
		}
	}

};

fmw.img = {
	changePic: function (param) {
		param.jqObj_img.attr('src', param.newUrl);
		param.jqObj_img.parent().next('input[type=hidden]').val(param.newUrl);
	},

	loadPic: function (id) {
		//alert($('img#'+id).attr('src'));
		//var jqImg = $('img#'+id);
		fmw.KCFinder_popUp({
			jqObj_img: $('img#' + id),      //img-ul al carui url va fi schimbat cu noua imagine aleasa
			callBackFn: fmw.img.changePic   //functie apelata dupa ce a fost selectata o imagine
		})
	}
}


fmw.getData = new fmw.queryData();
//nu stiu daca asta ar trebui mereu apelata
// sau ar trebui sa fie relativ la proiect

var procesSCRIPT_file = fmw.ajaxProxy;                 // intermediaza requesturile scripurilor .js


$(document).ready(function () {

	console.log("Tring to parse the Get");
	for (var getName in fmw.getData) {
		console.log("$_GET['" + getName + "'] = " + fmw.getData[getName]);
	}
});
