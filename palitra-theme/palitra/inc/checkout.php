<?php
/**
 * Cart & checkout: free delivery, short checkout form, clean layout.
 *
 * @package palitra
 */

defined( 'ABSPATH' ) || exit;

/* -------------------------------------------------------------------------
 * 1. Free delivery on every order.
 *    The shop pays Ozon; the customer sees «бесплатно».
 * ---------------------------------------------------------------------- */

add_filter( 'woocommerce_package_rates', 'palitra_free_delivery_rates', 100 );
function palitra_free_delivery_rates( $rates ) {
	foreach ( $rates as $rate ) {
		$rate->set_cost( 0 );
		$rate->set_taxes( array() );
		$label = (string) $rate->get_label();
		// ApiShip ends the label with ", цена от" (WooCommerce would add the price after it).
		$label = preg_replace( '/,?\s*цена от\s*:?\s*$/u', '', $label );
		if ( false === mb_stripos( $label, 'бесплатн' ) ) {
			$label .= ' — бесплатно';
		}
		$rate->set_label( $label );
	}
	return $rates;
}

/* -------------------------------------------------------------------------
 * 2. Short checkout form.
 *    Delivery goes to an Ozon pickup point, so no street address is needed:
 *    name, phone, email, city, region, postcode.
 * ---------------------------------------------------------------------- */

/* One address only (the "ship to a different address" block is not needed). */
add_filter( 'woocommerce_cart_needs_shipping_address', '__return_false' );

add_filter( 'woocommerce_default_address_fields', 'palitra_address_fields', 20 );
function palitra_address_fields( $fields ) {
	unset( $fields['company'], $fields['address_1'], $fields['address_2'] );

	$order = array(
		'first_name' => 10,
		'last_name'  => 20,
		'country'    => 40,
		'city'       => 50,
		'state'      => 60,
		'postcode'   => 70,
	);
	foreach ( $order as $key => $priority ) {
		if ( isset( $fields[ $key ] ) ) {
			$fields[ $key ]['priority'] = $priority;
		}
	}
	if ( isset( $fields['city'] ) ) {
		$fields['city']['label']       = 'Город';
		$fields['city']['placeholder'] = 'Например, Москва';
		$fields['city']['class']       = array( 'form-row-wide' );
	}
	unset( $fields['state'] );
	if ( isset( $fields['city'] ) ) {
		$fields['city']['class'] = array( 'form-row-first' );
	}
	if ( isset( $fields['postcode'] ) ) {
		$fields['postcode']['label'] = 'Индекс';
		$fields['postcode']['class'] = array( 'form-row-last' );
	}
	return $fields;
}

/* Russia: same rules in the address JS (it overrides labels/required per country). */
add_filter( 'woocommerce_get_country_locale', function ( $locale ) {
	$locale['RU'] = array_merge(
		isset( $locale['RU'] ) ? $locale['RU'] : array(),
		array(
			'city'     => array( 'label' => 'Город', 'priority' => 50 ),
			'state'    => array( 'required' => false, 'hidden' => true ),
			'postcode' => array( 'label' => 'Индекс', 'required' => true, 'priority' => 70 ),
		)
	);
	return $locale;
} );

add_filter( 'woocommerce_billing_fields', 'palitra_billing_fields', 20 );
function palitra_billing_fields( $fields ) {
	if ( isset( $fields['billing_phone'] ) ) {
		$fields['billing_phone']['required']    = true;
		$fields['billing_phone']['label']       = 'Телефон';
		$fields['billing_phone']['placeholder'] = '+7 900 000-00-00';
		$fields['billing_phone']['priority']    = 25;
		$fields['billing_phone']['class']       = array( 'form-row-first' );
	}
	if ( isset( $fields['billing_email'] ) ) {
		$fields['billing_email']['label']       = 'Email';
		$fields['billing_email']['priority']    = 26;
		$fields['billing_email']['class']       = array( 'form-row-last' );
	}
	if ( isset( $fields['billing_country'] ) ) {
		$fields['billing_country']['class'][] = 'pl-hidden-field';
	}
	return $fields;
}

/* No order comments field. */
add_filter( 'woocommerce_enable_order_notes_field', '__return_false' );

/* Headings in Russian shop wording. */
add_filter( 'gettext', function ( $translation, $text, $domain ) {
	if ( 'woocommerce' !== $domain ) {
		return $translation;
	}
	switch ( $text ) {
		case 'Billing details':
		case 'Billing &amp; Shipping':
			return 'Контакты и доставка';
		case 'Additional information':
			return 'Комментарий';
		case 'Your order':
			return 'Ваш заказ';
		case 'Place order':
			return 'Оплатить заказ';
	}
	return $translation;
}, 20, 3 );

add_filter( 'woocommerce_order_button_text', function () {
	return 'Перейти к оплате';
} );

/* Nothing extra on the page: no coupon box, no long privacy paragraph,
   no separate "terms" checkbox (acceptance is stated next to the button). */
add_action( 'wp', function () {
	if ( ! function_exists( 'is_checkout' ) || ! is_checkout() ) {
		return;
	}
	remove_action( 'woocommerce_before_checkout_form', 'woocommerce_checkout_coupon_form', 10 );
	remove_action( 'woocommerce_checkout_terms_and_conditions', 'wc_checkout_privacy_policy_text', 20 );
	remove_action( 'storefront_before_content', 'woocommerce_breadcrumb', 10 );
} );
add_filter( 'woocommerce_checkout_show_terms', '__return_false' );

add_action( 'woocommerce_review_order_before_submit', function () {
	$offer = get_page_by_path( 'oferta', OBJECT, 'page' );
	$link  = $offer ? '<a href="' . esc_url( get_permalink( $offer ) ) . '" target="_blank" rel="noopener">публичной оферты</a>' : 'публичной оферты';
	echo '<p class="pl-checkout-note">Нажимая «Перейти к оплате», вы принимаете условия ' . $link . '. Доставка — бесплатно, в выбранный пункт выдачи Ozon.</p>'; // phpcs:ignore
}, 20 );

/* -------------------------------------------------------------------------
 * 3. Full-width cart & checkout (no catalogue sidebar).
 * ---------------------------------------------------------------------- */

add_action( 'wp', function () {
	if ( function_exists( 'is_cart' ) && ( is_cart() || is_checkout() ) ) {
		remove_action( 'storefront_sidebar', 'storefront_get_sidebar', 10 );
	}
} );

add_filter( 'body_class', function ( $classes ) {
	if ( function_exists( 'is_cart' ) && ( is_cart() || is_checkout() ) ) {
		$classes[] = 'storefront-full-width-content';
		$classes[] = 'pl-checkout-page';
	}
	return $classes;
} );

/* -------------------------------------------------------------------------
 * 4. Cart: no address / delivery calculator — the address and the pickup
 *    point are entered once, at checkout. The cart just says delivery is free.
 * ---------------------------------------------------------------------- */

add_filter( 'pre_option_woocommerce_enable_shipping_calc', function () {
	return 'no';
} );

add_filter( 'woocommerce_cart_ready_to_calc_shipping', function ( $ready ) {
	return ( function_exists( 'is_cart' ) && is_cart() ) ? false : $ready;
} );

add_action( 'woocommerce_cart_totals_before_order_total', function () {
	echo '<tr class="pl-cart-delivery"><th>Доставка</th><td data-title="Доставка"><strong>Бесплатно</strong><br><small>Пункт выдачи Ozon выберете при оформлении заказа</small></td></tr>';
} );
