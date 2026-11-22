<?php
/**
 * "Новинка" (new) products: badge + home page section driven by the product tag «новинка».
 * To mark a product as new, add the tag «новинка» to it in the product editor.
 *
 * @package palitra
 */

defined( 'ABSPATH' ) || exit;

/** The «новинка» product tag term, or null. */
function palitra_new_tag() {
	static $term = false;
	if ( false !== $term ) {
		return $term;
	}
	$term = null;
	foreach ( array( 'новинка', 'Новинка', 'новинки', 'new' ) as $name ) {
		$t = get_term_by( 'name', $name, 'product_tag' );
		if ( $t && ! is_wp_error( $t ) ) {
			$term = $t;
			break;
		}
	}
	return $term;
}

function palitra_is_new( $product_id ) {
	$t = palitra_new_tag();
	return $t ? has_term( (int) $t->term_id, 'product_tag', $product_id ) : false;
}

/* Badge on product cards (shop, categories, home) — sits on the photo. */
add_action( 'woocommerce_before_shop_loop_item_title', 'palitra_loop_new_badge', 9 );
function palitra_loop_new_badge() {
	if ( palitra_is_new( get_the_ID() ) ) {
		echo '<span class="pl-badge-new">Новинка</span>';
	}
}

/* Badge on the product page, above the brand and title. */
add_action( 'woocommerce_single_product_summary', 'palitra_single_new_badge', 3 );
function palitra_single_new_badge() {
	if ( palitra_is_new( get_the_ID() ) ) {
		echo '<span class="pl-badge-new pl-badge-new--inline">Новинка</span>';
	}
}

/**
 * Up to $limit «новинка» products, newest first, interleaved by brand so every
 * brand shows up in the home page block.
 */
function palitra_new_product_ids( $limit = 8 ) {
	$t = palitra_new_tag();
	if ( ! $t ) {
		return array();
	}
	$ids = get_posts(
		array(
			'post_type'      => 'product',
			'post_status'    => 'publish',
			'fields'         => 'ids',
			'posts_per_page' => 200,
			'no_found_rows'  => true,
			'orderby'        => 'date',
			'order'          => 'DESC',
			'tax_query'      => array( // phpcs:ignore WordPress.DB.SlowDBQuery
				array(
					'taxonomy' => 'product_tag',
					'field'    => 'term_id',
					'terms'    => (int) $t->term_id,
				),
			),
		)
	);
	if ( empty( $ids ) ) {
		return array();
	}
	// Products with a photo first, then group by brand and take them round-robin.
	usort(
		$ids,
		function ( $a, $b ) {
			return (int) ! has_post_thumbnail( $a ) - (int) ! has_post_thumbnail( $b );
		}
	);
	$groups = array();
	foreach ( $ids as $id ) {
		$brand              = palitra_product_brand( $id );
		$key                = $brand ? $brand['name'] : '—';
		$groups[ $key ][]   = $id;
	}
	$out = array();
	while ( count( $out ) < $limit && $groups ) {
		foreach ( array_keys( $groups ) as $key ) {
			if ( count( $out ) >= $limit ) {
				break;
			}
			$out[] = array_shift( $groups[ $key ] );
			if ( empty( $groups[ $key ] ) ) {
				unset( $groups[ $key ] );
			}
		}
	}
	return $out;
}

/* Home page: replace Storefront's "recent products" with the «новинка» selection. */
add_action( 'init', function () {
	remove_action( 'homepage', 'storefront_recent_products', 30 );
} );

add_action( 'homepage', 'palitra_home_new', 30 );
function palitra_home_new() {
	$ids = palitra_new_product_ids( 8 );
	$t   = palitra_new_tag();
	$all = '';
	if ( $ids && $t ) {
		$link = get_term_link( $t );
		$all  = is_wp_error( $link ) ? '' : $link;
		$sc   = '[products ids="' . implode( ',', array_map( 'intval', $ids ) ) . '" orderby="post__in" columns="4" limit="8"]';
	} else {
		// Nothing tagged yet: fall back to the latest products.
		$sc = '[products orderby="date" order="DESC" columns="4" limit="8"]';
	}
	$html = do_shortcode( $sc );
	if ( false === strpos( $html, 'product' ) ) {
		return;
	}
	echo '<section class="pl-section storefront-product-section pl-new">';
	palitra_section_head( 'Новые поступления', $all, $all ? 'Все новинки' : '' );
	echo $html; // phpcs:ignore WordPress.Security.EscapeOutput
	echo '</section>';
}

/* Nicer title for the «новинка» tag page. */
add_filter( 'woocommerce_page_title', function ( $title ) {
	$t = palitra_new_tag();
	if ( $t && function_exists( 'is_product_tag' ) && is_product_tag( $t->term_id ) ) {
		return 'Новые поступления';
	}
	return $title;
}, 5 );
