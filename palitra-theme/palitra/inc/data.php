<?php
/**
 * Data helpers: brands and the catalog tree (cached).
 *
 * @package palitra
 */

defined( 'ABSPATH' ) || exit;

/** Country of origin shown on brand cards and brand pages. */
function palitra_brand_countries() {
	return array(
		'unison colour'   => 'Великобритания',
		'michael harding' => 'Великобритания',
		'winsor&newton'   => 'Великобритания',
		'winsor & newton' => 'Великобритания',
		'terry ludwig'    => 'США',
		'panpastel'       => 'США',
		'jack richeson'   => 'США',
		"general's"       => 'США',
		'daniel smith'    => 'США',
		'schmincke'       => 'Германия',
		'lyra'            => 'Германия',
		'sennelier'       => 'Франция',
		'rembrandt'       => 'Нидерланды',
		'royal talens'    => 'Нидерланды',
		'van gogh'        => 'Нидерланды',
		'old holland'     => 'Нидерланды',
		'holbein'         => 'Япония',
		'art spectrum'    => 'Австралия',
		'mount vision'    => 'Непал',
	);
}

function palitra_brand_country( $name ) {
	$map = palitra_brand_countries();
	$key = function_exists( 'mb_strtolower' ) ? mb_strtolower( trim( $name ) ) : strtolower( trim( $name ) );
	return isset( $map[ $key ] ) ? $map[ $key ] : '';
}

/** URL of the brand's logo bundled in assets/brands/{slug}.png, or ''. */
function palitra_brand_logo( $name ) {
	$slug = function_exists( 'mb_strtolower' ) ? mb_strtolower( trim( $name ) ) : strtolower( trim( $name ) );
	$slug = str_replace( array( "'", '’', '.' ), '', $slug );
	$slug = preg_replace( '/[^a-z0-9]+/', '-', $slug );
	$slug = trim( $slug, '-' );
	if ( '' === $slug ) {
		return '';
	}
	$file = '/assets/brands/' . $slug . '.png';
	return file_exists( get_stylesheet_directory() . $file ) ? get_stylesheet_directory_uri() . $file : '';
}

/* -------------------------------------------------------------------------
 * Catalog visibility: follow WooCommerce «Скрывать отсутствующие товары».
 * ---------------------------------------------------------------------- */

function palitra_hide_out_of_stock() {
	return 'yes' === get_option( 'woocommerce_hide_out_of_stock_items' );
}

/** tax_query clause that removes hidden products (and out-of-stock ones when WooCommerce hides them). */
function palitra_visibility_clause() {
	$terms = array( 'exclude-from-catalog' );
	if ( palitra_hide_out_of_stock() ) {
		$terms[] = 'outofstock';
	}
	return array(
		'taxonomy' => 'product_visibility',
		'field'    => 'name',
		'terms'    => $terms,
		'operator' => 'NOT IN',
	);
}

/** IDs of all products a customer can see in the catalog. */
function palitra_visible_product_ids() {
	static $ids = null;
	if ( null === $ids ) {
		$ids = get_posts(
			array(
				'post_type'      => 'product',
				'post_status'    => 'publish',
				'fields'         => 'ids',
				'posts_per_page' => -1,
				'no_found_rows'  => true,
				'tax_query'      => array( palitra_visibility_clause() ), // phpcs:ignore WordPress.DB.SlowDBQuery
			)
		);
	}
	return $ids;
}

/** Brand slug => number of visible products. */
function palitra_brand_counts() {
	$cached = get_transient( 'palitra_brand_counts_v1' );
	if ( is_array( $cached ) ) {
		return $cached;
	}
	$counts = array();
	$ids    = palitra_visible_product_ids();
	if ( $ids && taxonomy_exists( 'product_brand' ) ) {
		$rel = wp_get_object_terms( $ids, 'product_brand', array( 'fields' => 'all_with_object_id' ) );
		if ( ! is_wp_error( $rel ) ) {
			foreach ( $rel as $t ) {
				$counts[ $t->slug ] = ( $counts[ $t->slug ] ?? 0 ) + 1;
			}
		}
	}
	set_transient( 'palitra_brand_counts_v1', $counts, 12 * HOUR_IN_SECONDS );
	return $counts;
}

/** Preferred order of top-level categories in the menu. */
function palitra_category_order() {
	return array( 'Пастель', 'Масляные краски', 'Акварель', 'Гуашь', 'Акриловые краски', 'Бумага', 'Карандаши и кисти' );
}

function palitra_plural( $n, $one, $few, $many ) {
	$n    = abs( (int) $n );
	$n10  = $n % 10;
	$n100 = $n % 100;
	if ( 1 === $n10 && 11 !== $n100 ) {
		return $one;
	}
	if ( $n10 >= 2 && $n10 <= 4 && ( $n100 < 10 || $n100 >= 20 ) ) {
		return $few;
	}
	return $many;
}

function palitra_count_label( $n ) {
	return $n . ' ' . palitra_plural( $n, 'товар', 'товара', 'товаров' );
}

function palitra_shop_url() {
	return function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/' );
}

function palitra_brands_page_url() {
	$page = get_page_by_path( 'brendy' );
	return $page ? get_permalink( $page ) : palitra_shop_url();
}

/**
 * All brands with products, A–Z.
 *
 * @return array[] name, slug, url, count, country
 */
if ( ! function_exists( 'palitra_get_brands' ) ) {
	function palitra_get_brands() {
		if ( ! taxonomy_exists( 'product_brand' ) ) {
			return array();
		}
		$terms = get_terms(
			array(
				'taxonomy'   => 'product_brand',
				'hide_empty' => true,
			)
		);
		if ( is_wp_error( $terms ) ) {
			return array();
		}
		$out    = array();
		$counts = palitra_brand_counts();
		foreach ( $terms as $t ) {
			$url = get_term_link( $t );
			if ( is_wp_error( $url ) || empty( $counts[ $t->slug ] ) ) {
				continue; // no products a customer can see
			}
			$out[] = array(
				'name'    => $t->name,
				'slug'    => $t->slug,
				'url'     => $url,
				'count'   => (int) $counts[ $t->slug ],
				'country' => palitra_brand_country( $t->name ),
				'logo'    => palitra_brand_logo( $t->name ),
			);
		}
		usort(
			$out,
			function ( $a, $b ) {
				return strnatcasecmp( $a['name'], $b['name'] );
			}
		);
		return $out;
	}
}

/**
 * Top-level categories with children and the brands inside each category.
 *
 * @return array[] name, slug, url, count, children[], brands[]
 */
if ( ! function_exists( 'palitra_get_menu_tree' ) ) {
	function palitra_get_menu_tree() {
		$cached = get_transient( 'palitra_menu_tree_v4' );
		if ( is_array( $cached ) ) {
			return $cached;
		}

		$tops = get_terms(
			array(
				'taxonomy'   => 'product_cat',
				'parent'     => 0,
				'hide_empty' => false,
			)
		);
		if ( is_wp_error( $tops ) ) {
			return array();
		}

		$default_cat = (int) get_option( 'default_product_cat' );
		$order       = array_flip( palitra_category_order() );
		$tree        = array();

		foreach ( $tops as $top ) {
			if ( (int) $top->term_id === $default_cat ) {
				continue;
			}
			$url = get_term_link( $top );
			if ( is_wp_error( $url ) ) {
				continue;
			}

			$ids = get_posts(
				array(
					'post_type'      => 'product',
					'post_status'    => 'publish',
					'fields'         => 'ids',
					'posts_per_page' => -1,
					'no_found_rows'  => true,
					'tax_query'      => array( // phpcs:ignore WordPress.DB.SlowDBQuery
						'relation' => 'AND',
						array(
							'taxonomy'         => 'product_cat',
							'field'            => 'term_id',
							'terms'            => $top->term_id,
							'include_children' => true,
						),
						palitra_visibility_clause(),
					),
				)
			);
			if ( empty( $ids ) ) {
				continue;
			}
			// Visible products per sub-category.
			$child_counts = array();
			$crel         = wp_get_object_terms( $ids, 'product_cat', array( 'fields' => 'all_with_object_id' ) );
			if ( ! is_wp_error( $crel ) ) {
				foreach ( $crel as $ct ) {
					$child_counts[ $ct->term_id ] = ( $child_counts[ $ct->term_id ] ?? 0 ) + 1;
				}
			}

			$children = array();
			$kids     = get_terms(
				array(
					'taxonomy'   => 'product_cat',
					'parent'     => $top->term_id,
					'hide_empty' => true,
				)
			);
			if ( ! is_wp_error( $kids ) ) {
				foreach ( $kids as $k ) {
					$kurl = get_term_link( $k );
					if ( ! is_wp_error( $kurl ) && ! empty( $child_counts[ $k->term_id ] ) ) {
						$children[] = array(
							'name'  => $k->name,
							'slug'  => $k->slug,
							'url'   => $kurl,
							'count' => (int) $child_counts[ $k->term_id ],
						);
					}
				}
			}

			$brands = array();
			if ( taxonomy_exists( 'product_brand' ) ) {
				$rel = wp_get_object_terms( $ids, 'product_brand', array( 'fields' => 'all_with_object_id' ) );
				if ( ! is_wp_error( $rel ) ) {
					foreach ( $rel as $b ) {
						if ( ! isset( $brands[ $b->slug ] ) ) {
							$brands[ $b->slug ] = array(
								'name'  => $b->name,
								'slug'  => $b->slug,
								'url'   => add_query_arg( 'product_brand', $b->slug, $url ),
								'count' => 0,
							);
						}
						$brands[ $b->slug ]['count']++;
					}
				}
				$brands = array_values( $brands );
				usort(
					$brands,
					function ( $a, $b ) {
						return strnatcasecmp( $a['name'], $b['name'] );
					}
				);
			}

			$tree[] = array(
				'name'     => $top->name,
				'slug'     => $top->slug,
				'url'      => $url,
				'count'    => count( $ids ),
				'children' => $children,
				'brands'   => $brands,
				'image'    => palitra_category_image( $top, $ids ),
				'_order'   => isset( $order[ $top->name ] ) ? $order[ $top->name ] : 100 + count( $tree ),
			);
		}

		usort(
			$tree,
			function ( $a, $b ) {
				return $a['_order'] - $b['_order'];
			}
		);

		set_transient( 'palitra_menu_tree_v4', $tree, 12 * HOUR_IN_SECONDS );
		return $tree;
	}
}


/**
 * Image for a category card: the category's own thumbnail if set,
 * otherwise the photo of its most expensive product that has one.
 */
function palitra_category_image( $term, $ids ) {
	$thumb = (int) get_term_meta( $term->term_id, 'thumbnail_id', true );
	if ( $thumb ) {
		$url = wp_get_attachment_image_url( $thumb, 'woocommerce_thumbnail' );
		if ( $url ) {
			return $url;
		}
	}
	if ( empty( $ids ) ) {
		return '';
	}
	$pick = get_posts(
		array(
			'post_type'      => 'product',
			'post_status'    => 'publish',
			'fields'         => 'ids',
			'posts_per_page' => 1,
			'no_found_rows'  => true,
			'post__in'       => array_map( 'intval', $ids ),
			'meta_key'       => '_price', // phpcs:ignore WordPress.DB.SlowDBQuery
			'orderby'        => 'meta_value_num',
			'order'          => 'DESC',
			'meta_query'     => array( // phpcs:ignore WordPress.DB.SlowDBQuery
				array(
					'key'     => '_thumbnail_id',
					'compare' => 'EXISTS',
				),
			),
			'tax_query'      => array( palitra_visibility_clause() ), // phpcs:ignore WordPress.DB.SlowDBQuery
		)
	);
	if ( empty( $pick ) ) {
		return '';
	}
	$url = get_the_post_thumbnail_url( $pick[0], 'woocommerce_thumbnail' );
	return $url ? $url : '';
}

function palitra_flush_menu_cache() {
	delete_transient( 'palitra_menu_tree_v4' );
	delete_transient( 'palitra_brand_counts_v1' );
}
/* Out of stock / back in stock (incl. the Ozon sync) and the WooCommerce hide setting. */
add_action( 'woocommerce_product_set_stock_status', 'palitra_flush_menu_cache' );
add_action( 'woocommerce_variation_set_stock_status', 'palitra_flush_menu_cache' );
add_action( 'update_option_woocommerce_hide_out_of_stock_items', 'palitra_flush_menu_cache' );
add_action( 'save_post_product', 'palitra_flush_menu_cache' );
add_action( 'updated_post_meta', function ( $mid, $post_id, $key ) {
	if ( '_thumbnail_id' === $key && 'product' === get_post_type( $post_id ) ) {
		palitra_flush_menu_cache();
	}
}, 10, 3 );
add_action( 'added_post_meta', function ( $mid, $post_id, $key ) {
	if ( '_thumbnail_id' === $key && 'product' === get_post_type( $post_id ) ) {
		palitra_flush_menu_cache();
	}
}, 10, 3 );
add_action( 'deleted_post', 'palitra_flush_menu_cache' );
add_action( 'woocommerce_product_import_inserted_product_object', 'palitra_flush_menu_cache' );
foreach ( array( 'created_product_cat', 'edited_product_cat', 'delete_product_cat', 'created_product_brand', 'edited_product_brand', 'delete_product_brand' ) as $palitra_hook ) {
	add_action( $palitra_hook, 'palitra_flush_menu_cache' );
}

/* -------------------------------------------------------------------------
 * Brand sync: WooCommerce's CSV importer does not fill the built-in
 * "Бренды" (product_brand) list, so we copy each product's «Бренд»
 * attribute into it. Runs in the admin, after imports and on save.
 * ---------------------------------------------------------------------- */

function palitra_brand_attribute_taxonomy() {
	if ( ! function_exists( 'wc_get_attribute_taxonomies' ) ) {
		return '';
	}
	foreach ( wc_get_attribute_taxonomies() as $attr ) {
		$label = function_exists( 'mb_strtolower' ) ? mb_strtolower( $attr->attribute_label ) : strtolower( $attr->attribute_label );
		if ( in_array( $label, array( 'бренд', 'brand', 'производитель' ), true ) ) {
			return wc_attribute_taxonomy_name( $attr->attribute_name );
		}
	}
	return '';
}

function palitra_sync_product_brand( $product_id ) {
	if ( ! taxonomy_exists( 'product_brand' ) ) {
		return false;
	}
	$tax = palitra_brand_attribute_taxonomy();
	if ( ! $tax || ! taxonomy_exists( $tax ) ) {
		return false;
	}
	$current = wp_get_object_terms( $product_id, 'product_brand', array( 'fields' => 'ids' ) );
	if ( ! is_wp_error( $current ) && ! empty( $current ) ) {
		return false; // Already has a brand: never overwrite manual choices.
	}
	$names = wp_get_object_terms( $product_id, $tax, array( 'fields' => 'names' ) );
	if ( is_wp_error( $names ) || empty( $names ) ) {
		return false;
	}
	$ids = array();
	foreach ( $names as $name ) {
		$term = term_exists( $name, 'product_brand' );
		if ( ! $term ) {
			$term = wp_insert_term( $name, 'product_brand' );
		}
		if ( ! is_wp_error( $term ) && $term ) {
			$ids[] = (int) ( is_array( $term ) ? $term['term_id'] : $term );
		}
	}
	if ( $ids ) {
		wp_set_object_terms( $product_id, $ids, 'product_brand' );
		return true;
	}
	return false;
}

function palitra_sync_all_brands() {
	if ( ! taxonomy_exists( 'product_brand' ) || ! palitra_brand_attribute_taxonomy() ) {
		return 0;
	}
	$ids = get_posts(
		array(
			'post_type'      => 'product',
			'post_status'    => array( 'publish', 'draft', 'pending', 'private' ),
			'fields'         => 'ids',
			'posts_per_page' => 500,
			'no_found_rows'  => true,
			'tax_query'      => array( // phpcs:ignore WordPress.DB.SlowDBQuery
				array(
					'taxonomy' => 'product_brand',
					'operator' => 'NOT EXISTS',
				),
			),
		)
	);
	$done = 0;
	foreach ( $ids as $id ) {
		if ( palitra_sync_product_brand( $id ) ) {
			$done++;
		}
	}
	if ( $done ) {
		palitra_flush_menu_cache();
	}
	return $done;
}

/* In the admin at most every 2 minutes, so new imports get brands without any action. */
add_action( 'admin_init', function () {
	if ( wp_doing_ajax() || get_transient( 'palitra_brand_sync_lock' ) ) {
		return;
	}
	set_transient( 'palitra_brand_sync_lock', 1, 2 * MINUTE_IN_SECONDS );
	palitra_sync_all_brands();
} );

/* Right after each product is imported or saved. */
add_action( 'woocommerce_product_import_inserted_product_object', function ( $product ) {
	if ( is_object( $product ) && method_exists( $product, 'get_id' ) ) {
		palitra_sync_product_brand( $product->get_id() );
	}
} );
add_action( 'woocommerce_update_product', 'palitra_sync_product_brand', 20 );

/** First brand of a product (name + url), or null. */
function palitra_product_brand( $product_id ) {
	if ( ! taxonomy_exists( 'product_brand' ) ) {
		return null;
	}
	$terms = get_the_terms( $product_id, 'product_brand' );
	if ( empty( $terms ) || is_wp_error( $terms ) ) {
		return null;
	}
	$url = get_term_link( $terms[0] );
	return array(
		'name' => $terms[0]->name,
		'url'  => is_wp_error( $url ) ? '' : $url,
	);
}

/** Simple line icons used in the header and USP strip. */
function palitra_icon( $name ) {
	$paths = array(
		'search'  => '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
		'cart'    => '<path d="M3 4h2l2.2 10.2a1.5 1.5 0 0 0 1.5 1.2h8.6a1.5 1.5 0 0 0 1.5-1.1L21 8H6.2"/><circle cx="9.5" cy="19.5" r="1.3"/><circle cx="17" cy="19.5" r="1.3"/>',
		'user'    => '<circle cx="12" cy="8" r="4"/><path d="M4 20c1.5-3.5 4.5-5 8-5s6.5 1.5 8 5"/>',
		'menu'    => '<path d="M4 7h16M4 12h16M4 17h16"/>',
		'close'   => '<path d="M6 6l12 12M18 6 6 18"/>',
		'truck'   => '<path d="M3 6h11v9H3zM14 9h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17.5" cy="17.5" r="1.8"/>',
		'shield'  => '<path d="M12 3 5 6v5c0 4.5 3 8 7 10 4-2 7-5.5 7-10V6z"/><path d="m9 12 2 2 4-4"/>',
		'spark'   => '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
		'chat'    => '<path d="M4 5h16v11H9l-5 4z"/>',
		'chevron' => '<path d="m6 9 6 6 6-6"/>',
		'arrow'   => '<path d="M5 12h14M13 6l6 6-6 6"/>',
	);
	if ( ! isset( $paths[ $name ] ) ) {
		return '';
	}
	return '<svg class="pl-icon pl-icon--' . esc_attr( $name ) . '" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' . $paths[ $name ] . '</svg>';
}
