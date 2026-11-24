/**
 * Палитра — подсказки при оформлении заказа (DaData Suggestions API).
 * Город → улица и дом в этом городе → индекс заполняется сам. Плюс имя, фамилия, email.
 */
( function () {
	'use strict';

	var cfg = window.palitraSuggest || {};
	if ( ! cfg.token ) {
		return;
	}
	var API = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/';
	var state = { cityFias: '', settlementFias: '', cityName: '' };

	function $( id ) {
		return document.getElementById( id );
	}

	function request( type, body ) {
		return fetch( API + type, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				Accept: 'application/json',
				Authorization: 'Token ' + cfg.token
			},
			body: JSON.stringify( body )
		} ).then( function ( r ) {
			return r.ok ? r.json() : { suggestions: [] };
		} ).then( function ( j ) {
			return j.suggestions || [];
		} ).catch( function () {
			return [];
		} );
	}

	/* Tell WooCommerce the address changed, so delivery is recalculated. */
	function changed( input ) {
		if ( window.jQuery ) {
			window.jQuery( input ).trigger( 'change' );
		} else {
			input.dispatchEvent( new Event( 'change', { bubbles: true } ) );
		}
	}

	function setValue( input, value ) {
		if ( input && typeof value === 'string' && value !== '' && input.value !== value ) {
			input.value = value;
			changed( input );
		}
	}

	/**
	 * Attach a suggestion dropdown to an input.
	 * opts.fetch(query) -> Promise<suggestions>, opts.label(s) -> text, opts.pick(s, input)
	 */
	function attach( input, opts ) {
		if ( ! input || input.dataset.plSuggest ) {
			return;
		}
		input.dataset.plSuggest = '1';
		input.setAttribute( 'autocomplete', opts.autocomplete || 'off' );

		var wrap = input.parentNode;
		wrap.classList.add( 'pl-suggest' );
		var list = document.createElement( 'ul' );
		list.className = 'pl-suggest__list';
		list.setAttribute( 'role', 'listbox' );
		list.hidden = true;
		wrap.appendChild( list );

		var items = [];
		var active = -1;
		var timer = null;
		var seq = 0;

		function close() {
			list.hidden = true;
			active = -1;
		}

		function render() {
			list.innerHTML = '';
			items.forEach( function ( s, i ) {
				var li = document.createElement( 'li' );
				li.className = 'pl-suggest__item' + ( i === active ? ' is-active' : '' );
				li.setAttribute( 'role', 'option' );
				li.textContent = opts.label( s );
				li.addEventListener( 'mousedown', function ( e ) {
					e.preventDefault();
					choose( i );
				} );
				list.appendChild( li );
			} );
			list.hidden = items.length === 0;
		}

		function choose( i ) {
			var s = items[ i ];
			if ( ! s ) {
				return;
			}
			close();
			opts.pick( s, input );
			if ( opts.keepOpen && opts.keepOpen( s ) ) {
				input.focus();
				search();
			}
		}

		function search() {
			var q = input.value.trim();
			if ( q.length < ( opts.min || 2 ) ) {
				items = [];
				render();
				return;
			}
			var my = ++seq;
			opts.fetch( q ).then( function ( res ) {
				if ( my !== seq ) {
					return;
				}
				items = res.slice( 0, 7 );
				active = -1;
				render();
			} );
		}

		input.addEventListener( 'input', function () {
			clearTimeout( timer );
			timer = setTimeout( search, 220 );
		} );
		input.addEventListener( 'focus', function () {
			if ( input.value.trim().length >= ( opts.min || 2 ) ) {
				search();
			}
		} );
		input.addEventListener( 'blur', function () {
			setTimeout( close, 120 );
		} );
		input.addEventListener( 'keydown', function ( e ) {
			if ( list.hidden ) {
				return;
			}
			if ( e.key === 'ArrowDown' ) {
				e.preventDefault();
				active = Math.min( active + 1, items.length - 1 );
				render();
			} else if ( e.key === 'ArrowUp' ) {
				e.preventDefault();
				active = Math.max( active - 1, 0 );
				render();
			} else if ( e.key === 'Enter' && active >= 0 ) {
				e.preventDefault();
				choose( active );
			} else if ( e.key === 'Escape' ) {
				close();
			}
		} );
	}

	function cityOf( d ) {
		return d.city || d.settlement || d.area || d.region || '';
	}

	function locations() {
		if ( state.settlementFias ) {
			return [ { settlement_fias_id: state.settlementFias } ];
		}
		if ( state.cityFias ) {
			return [ { city_fias_id: state.cityFias } ];
		}
		var city = ( $( 'billing_city' ) || {} ).value || '';
		return city ? [ { city: city } ] : [ { country_iso_code: 'RU' } ];
	}

	function init() {
		var city = $( 'billing_city' );
		var street = $( 'billing_address_1' );
		var postcode = $( 'billing_postcode' );

		/* City */
		attach( city, {
			fetch: function ( q ) {
				return request( 'address', {
					query: q,
					count: 7,
					from_bound: { value: 'city' },
					to_bound: { value: 'settlement' },
					locations: [ { country_iso_code: 'RU' } ]
				} );
			},
			label: function ( s ) {
				return s.value;
			},
			pick: function ( s, input ) {
				var d = s.data || {};
				state.cityFias = d.city_fias_id || '';
				state.settlementFias = d.settlement_fias_id || '';
				setValue( input, cityOf( d ) );
				if ( d.postal_code ) {
					setValue( postcode, d.postal_code );
				}
				if ( street && ! street.value ) {
					street.focus();
				}
			}
		} );
		if ( city ) {
			city.addEventListener( 'input', function () {
				state.cityFias = '';
				state.settlementFias = '';
			} );
		}

		/* Street + house (inside the chosen city); fills the postcode */
		attach( street, {
			min: 2,
			fetch: function ( q ) {
				return request( 'address', {
					query: q,
					count: 7,
					from_bound: { value: 'street' },
					to_bound: { value: 'flat' },
					restrict_value: true,
					locations: locations()
				} );
			},
			label: function ( s ) {
				return s.value;
			},
			pick: function ( s, input ) {
				var d = s.data || {};
				input.value = s.value + ( d.house ? '' : ', ' );
				changed( input );
				if ( d.postal_code ) {
					setValue( postcode, d.postal_code );
				}
				var c = cityOf( d );
				if ( c && city && ! city.value ) {
					setValue( city, c );
				}
			},
			keepOpen: function ( s ) {
				return ! ( s.data && s.data.house );
			}
		} );

		/* Name and surname */
		[ [ 'billing_first_name', 'NAME' ], [ 'billing_last_name', 'SURNAME' ] ].forEach( function ( f ) {
			attach( $( f[ 0 ] ), {
				min: 1,
				autocomplete: f[ 1 ] === 'NAME' ? 'given-name' : 'family-name',
				fetch: function ( q ) {
					return request( 'fio', { query: q, count: 5, parts: [ f[ 1 ] ] } );
				},
				label: function ( s ) {
					return s.value;
				},
				pick: function ( s, input ) {
					input.value = s.value;
					changed( input );
				}
			} );
		} );

		/* Email (completes the domain) */
		attach( $( 'billing_email' ), {
			min: 2,
			autocomplete: 'email',
			fetch: function ( q ) {
				return request( 'email', { query: q, count: 5 } );
			},
			label: function ( s ) {
				return s.value;
			},
			pick: function ( s, input ) {
				input.value = s.value;
				changed( input );
			}
		} );
	}

	if ( document.readyState === 'loading' ) {
		document.addEventListener( 'DOMContentLoaded', init );
	} else {
		init();
	}
	/* WooCommerce may re-render the checkout; re-attach if inputs were replaced. */
	if ( window.jQuery ) {
		window.jQuery( document.body ).on( 'updated_checkout', init );
	}
}() );
