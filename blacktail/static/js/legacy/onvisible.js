/*
Copyright (C) 2012 de Flotte Maxence

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
*/

/*
 * @version 0.1
 */

jQuery.fn.visibilityListener = function(options) {
	// Defaults vars
	var defaults = {
		checkOnLoad: true,
		frequency: 200
	};
	// Extend our default options with those provided.
	var opts = jQuery.extend(defaults, options);
	
	var elts = jQuery(this);
	var visibleElements = [];
	var completeVisibleElements = [];
	var hiddenElements = [];
	
	var fireEvents = function()
	{
		var tmpVisibleElements = [];
		var tmpCompleteVisibleElements = [];
		var tmpHiddenElements = [];
		
		elts.each(function(it) {
			var offsetNO = jQuery(this).offset();
			var offsetNE = {
				top: offsetNO.top,
				left: offsetNO.left + jQuery(this).width()
			};
			var offsetSO = {
				top: offsetNO.top + jQuery(this).height(),
				left: offsetNO.left
			};
			var offsetSE = {
				top: offsetNO.top + jQuery(this).height(),
				left: offsetNO.left + jQuery(this).width()
			};
			if (pointVisible(offsetNO) || pointVisible(offsetNE) || pointVisible(offsetSO) || pointVisible(offsetSE)) {
				if (jQuery(this).is(':visible')) {
					if (jQuery.inArray(it, visibleElements) === -1) {
						jQuery(this).trigger('visible');
						console.log('visible');
					}
					tmpVisibleElements.push(it);
					if (pointVisible(offsetNO) && pointVisible(offsetNE) && pointVisible(offsetSO) && pointVisible(offsetSE)) {
						if (jQuery.inArray(it, completeVisibleElements) === -1) {
							jQuery(this).trigger('fullyvisible');
						}
						tmpCompleteVisibleElements.push(it);
					} else {
						if (jQuery.inArray(it, completeVisibleElements) === -1) {
							jQuery(this).trigger('partiallyvisible');
						}
					}
				}
			} else {
				if (jQuery(this).is(':visible')) {
					if (jQuery.inArray(it, hiddenElements) === -1) {
						jQuery(this).trigger('hidden');
					}
					tmpHiddenElements.push(it);
				}
			}
		});
		visibleElements = tmpVisibleElements.slice();
		completeVisibleElements = tmpCompleteVisibleElements.slice();
		hiddenElements = tmpHiddenElements.slice();
	}
	
	var pointVisible = function(point) {
		if (point.left > jQuery(document).scrollLeft()
			&& point.left < jQuery(document).scrollLeft() + jQuery(window).width()
			&& point.top > jQuery(document).scrollTop()
			&& point.top < jQuery(document).scrollTop() + jQuery(window).height()
		) {
			return true;
		}
		return false;
	}
	
	if (!opts.checkOnLoad) {
		elts.each(function(it) {
			var offsetNO = jQuery(this).offset();
			var offsetNE = {
				top: offsetNO.top,
				left: offsetNO.left + jQuery(this).width()
			}
			var offsetSO = {
				top: offsetNO.top + jQuery(this).height(),
				left: offsetNO.left
			}
			var offsetSE = {
				top: offsetNO.top + jQuery(this).height(),
				left: offsetNO.left + jQuery(this).width()
			}
			if (pointVisible(offsetNO) || pointVisible(offsetNE) || pointVisible(offsetSO) || pointVisible(offsetSE)) {
				if (jQuery(this).is(':visible')) {
					visibleElements.push(it);
					if (pointVisible(offsetNO) && pointVisible(offsetNE) && pointVisible(offsetSO) && pointVisible(offsetSE)) {
						completeVisibleElements.push(it);
					}
				}
			} else {
				if (jQuery(this).is(':visible')) {
					hiddenElements.push(it);
				}
			}
		});
	}
	
	window.setInterval(function() {
		fireEvents();
	}, opts.frequency);
}