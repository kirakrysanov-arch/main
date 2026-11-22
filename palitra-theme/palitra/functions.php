<?php
/**
 * Палитра — child theme for Storefront.
 *
 * @package palitra
 */

defined( 'ABSPATH' ) || exit;

define( 'PALITRA_VERSION', '2.6.0' );
define( 'PALITRA_OZON_URL', 'https://ozon.ru/s/palitra-3140957' );
define( 'PALITRA_VK_URL', 'https://vk.com/palitra_hobby_art' );
define( 'PALITRA_TIKTOK_URL', 'https://www.tiktok.com/@palitra_artstore' );

require_once __DIR__ . '/inc/data.php';
require_once __DIR__ . '/inc/header.php';
require_once __DIR__ . '/inc/pages.php';
require_once __DIR__ . '/inc/seo.php';

/* -------------------------------------------------------------------------
 * Assets
 * ---------------------------------------------------------------------- */

add_action( 'wp_enqueue_scripts', 'palitra_enqueue', 30 );
function palitra_enqueue() {
	$deps = array();
	foreach ( array( 'storefront-style', 'storefront-woocommerce-style' ) as $handle ) {
		if ( wp_style_is( $handle, 'registered' ) ) {
			$deps[] = $handle;
		}
	}
	wp_enqueue_style( 'palitra-style', get_stylesheet_uri(), $deps, PALITRA_VERSION );
	wp_enqueue_script( 'palitra', get_stylesheet_directory_uri() . '/assets/js/palitra.js', array(), PALITRA_VERSION, true );
}

add_action( 'wp_enqueue_scripts', function () {
	wp_dequeue_style( 'storefront-child-style' ); // Storefront loads the child stylesheet itself; we load our own copy.
	wp_dequeue_style( 'storefront-fonts' );       // No Google Fonts: Inter ships with the theme.
}, 99 );

add_filter( 'storefront_google_font_families', '__return_empty_array' );

add_action( 'wp_head', function () {
	$base = get_stylesheet_directory_uri() . '/assets/fonts/';
	foreach ( array( 'inter-cyrillic-400', 'inter-cyrillic-600' ) as $f ) {
		printf( '<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n", esc_url( $base . $f . '-normal.woff2' ) );
	}
}, 1 );

/* -------------------------------------------------------------------------
 * Storefront defaults for this theme
 * ---------------------------------------------------------------------- */

function palitra_theme_mods() {
	return array(
		'storefront_layout'                      => 'left',
		'storefront_heading_color'               => '#141414',
		'storefront_text_color'                  => '#2b2b2b',
		'storefront_accent_color'                => '#141414',
		'storefront_header_background_color'     => '#ffffff',
		'storefront_header_text_color'           => '#2b2b2b',
		'storefront_header_link_color'           => '#141414',
		'storefront_footer_background_color'     => '#f6f5f2',
		'storefront_footer_heading_color'        => '#141414',
		'storefront_footer_text_color'           => '#6f6f6f',
		'storefront_footer_link_color'           => '#141414',
		'storefront_button_background_color'     => '#141414',
		'storefront_button_text_color'           => '#ffffff',
		'storefront_button_alt_background_color' => '#141414',
		'storefront_button_alt_text_color'       => '#ffffff',
	);
}

add_filter( 'storefront_setting_default_values', function ( $defaults ) {
	return array_merge( $defaults, palitra_theme_mods() );
} );

/* -------------------------------------------------------------------------
 * One-time setup (runs on activation and after updating the theme)
 * ---------------------------------------------------------------------- */

add_action( 'after_switch_theme', 'palitra_setup' );
add_action( 'admin_init', function () {
	if ( get_option( 'palitra_setup_version' ) !== PALITRA_VERSION ) {
		palitra_setup();
	}
} );

function palitra_setup() {
	foreach ( palitra_theme_mods() as $mod => $value ) {
		set_theme_mod( $mod, $value );
	}

	// Front page with Storefront's homepage template (only if none is set yet).
	if ( 'page' !== get_option( 'show_on_front' ) || ! get_option( 'page_on_front' ) ) {
		$home    = get_page_by_path( 'glavnaya' );
		$home_id = $home ? $home->ID : wp_insert_post(
			array(
				'post_title'  => 'Главная',
				'post_name'   => 'glavnaya',
				'post_status' => 'publish',
				'post_type'   => 'page',
			)
		);
		if ( $home_id && ! is_wp_error( $home_id ) ) {
			update_post_meta( $home_id, '_wp_page_template', 'template-homepage.php' );
			update_option( 'show_on_front', 'page' );
			update_option( 'page_on_front', $home_id );
		}
	}

	// Brands A–Z page.
	if ( ! get_page_by_path( 'brendy' ) ) {
		wp_insert_post(
			array(
				'post_title'   => 'Бренды',
				'post_name'    => 'brendy',
				'post_status'  => 'publish',
				'post_type'    => 'page',
				'post_content' => '[palitra_brands]',
			)
		);
	}

	palitra_flush_menu_cache();
	update_option( 'palitra_setup_version', PALITRA_VERSION );
}

/* -------------------------------------------------------------------------
 * Shop grid
 * ---------------------------------------------------------------------- */

add_filter( 'loop_shop_columns', function () {
	return 4;
}, 20 );

add_filter( 'loop_shop_per_page', function () {
	return 24;
}, 20 );

add_filter( 'storefront_related_products_args', function ( $args ) {
	$args['posts_per_page'] = 4;
	$args['columns']        = 4;
	return $args;
} );

add_filter( 'woocommerce_placeholder_img_src', function () {
	return get_stylesheet_directory_uri() . '/assets/placeholder.svg';
} );

/* Full-width brands page (no sidebar). */
add_filter( 'body_class', function ( $classes ) {
	if ( is_page( 'brendy' ) ) {
		$classes[] = 'pl-page-brands';
	}
	return $classes;
} );
