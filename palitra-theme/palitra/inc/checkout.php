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
	if ( isset( $fields['state'] ) ) {
		$fields['state']['label']    = 'Область / край';
		$fields['state']['required'] = false;
		$fields['state']['class']    = array( 'form-row-first' );
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
			'state'    => array( 'label' => 'Область / край', 'required' => false, 'priority' => 60 ),
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
		$fields['billing_phone']['description'] = 'Пришлём SMS, когда заказ прибудет в пункт выдачи Ozon.';
		$fields['billing_phone']['priority']    = 25;
		$fields['billing_phone']['class']       = array( 'form-row-first' );
	}
	if ( isset( $fields['billing_email'] ) ) {
		$fields['billing_email']['label']       = 'Email';
		$fields['billing_email']['description'] = 'Для чека и статуса заказа.';
		$fields['billing_email']['priority']    = 26;
		$fields['billing_email']['class']       = array( 'form-row-last' );
	}
	if ( isset( $fields['billing_country'] ) ) {
		$fields['billing_country']['class'][] = 'pl-hidden-field';
	}
	return $fields;
}

add_filter( 'woocommerce_checkout_fields', function ( $fields ) {
	if ( isset( $fields['order']['order_comments'] ) ) {
		$fields['order']['order_comments']['label']       = 'Комментарий к заказу';
		$fields['order']['order_comments']['placeholder'] = 'Необязательно';
	}
	return $fields;
}, 20 );

/* Headings in Russian shop wording. */
add_filter( 'gettext', function ( $translation, $text, $domain ) {
	if ( 'woocommerce' !== $domain ) {
		return $translation;
	}
	switch ( $text ) {
		case 'Billing details':
		case 'Billing &amp; Shipping':
			return 'Получатель';
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

/* Step labels above the sections. */
add_action( 'woocommerce_checkout_before_customer_details', function () {
	echo '<p class="pl-checkout-steps"><span>1. Получатель</span><span>2. Пункт выдачи Ozon</span><span>3. Оплата</span></p>';
} );

/* Reassurance under the order button. */
add_action( 'woocommerce_review_order_after_submit', function () {
	echo '<ul class="pl-checkout-trust">'
		. '<li>' . palitra_icon( 'truck' ) . '<span>Бесплатная доставка Ozon в пункт выдачи</span></li>' // phpcs:ignore
		. '<li>' . palitra_icon( 'shield' ) . '<span>Безопасная оплата через Ozon Pay, чек на email</span></li>' // phpcs:ignore
		. '</ul>';
} );

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
