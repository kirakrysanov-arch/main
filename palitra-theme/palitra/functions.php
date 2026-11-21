<?php
/**
 * Палитра — child theme for Storefront.
 *
 * @package palitra
 */

defined( 'ABSPATH' ) || exit;

define( 'PALITRA_VERSION', '1.0.0' );
define( 'PALITRA_OZON_URL', 'https://ozon.ru/s/palitra-3140957' );
define( 'PALITRA_VK_URL', 'https://vk.com/palitra_hobby_art' );
define( 'PALITRA_TIKTOK_URL', 'https://www.tiktok.com/@palitra_artstore' );

/* -------------------------------------------------------------------------
 * Styles
 * ---------------------------------------------------------------------- */

add_action( 'wp_enqueue_scripts', 'palitra_enqueue_styles', 30 );
function palitra_enqueue_styles() {
	$deps = array();
	foreach ( array( 'storefront-style', 'storefront-woocommerce-style' ) as $handle ) {
		if ( wp_style_is( $handle, 'registered' ) ) {
			$deps[] = $handle;
		}
	}
	wp_enqueue_style( 'palitra-style', get_stylesheet_uri(), $deps, PALITRA_VERSION );
}

/* Storefront enqueues the child stylesheet itself; drop its copy so ours (loaded later) wins. */
add_action( 'wp_enqueue_scripts', function () {
	wp_dequeue_style( 'storefront-child-style' );
}, 99 );

/* No Google Fonts: we ship our own fonts with the theme. */
add_filter( 'storefront_google_font_families', '__return_empty_array' );
add_action( 'wp_enqueue_scripts', function () {
	wp_dequeue_style( 'storefront-fonts' );
}, 99 );

add_action( 'wp_head', function () {
	$base = get_stylesheet_directory_uri() . '/assets/fonts/';
	foreach ( array( 'inter-cyrillic-400', 'cormorant-garamond-cyrillic-600' ) as $f ) {
		printf( '<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' . "\n", esc_url( $base . $f . '-normal.woff2' ) );
	}
}, 1 );

/* -------------------------------------------------------------------------
 * Default Storefront colours for this theme
 * ---------------------------------------------------------------------- */

function palitra_colour_defaults() {
	return array(
		'storefront_heading_color'           => '#1a1a1a',
		'storefront_text_color'              => '#3a3a3a',
		'storefront_accent_color'            => '#0f2233',
		'storefront_hero_heading_color'      => '#1a1a1a',
		'storefront_hero_text_color'         => '#3a3a3a',
		'storefront_header_background_color' => '#ffffff',
		'storefront_header_text_color'       => '#3a3a3a',
		'storefront_header_link_color'       => '#1a1a1a',
		'storefront_footer_background_color' => '#f5f4f1',
		'storefront_footer_heading_color'    => '#1a1a1a',
		'storefront_footer_text_color'       => '#5a5a5a',
		'storefront_footer_link_color'       => '#1a1a1a',
		'storefront_button_background_color' => '#111111',
		'storefront_button_text_color'       => '#ffffff',
		'storefront_button_alt_background_color' => '#0f2233',
		'storefront_button_alt_text_color'   => '#ffffff',
	);
}

add_filter( 'storefront_setting_default_values', function ( $defaults ) {
	return array_merge( $defaults, palitra_colour_defaults() );
} );

/* -------------------------------------------------------------------------
 * On activation: colours, front page, sensible shop settings
 * ---------------------------------------------------------------------- */

add_action( 'after_switch_theme', 'palitra_setup_on_activation' );
function palitra_setup_on_activation() {
	foreach ( palitra_colour_defaults() as $mod => $value ) {
		set_theme_mod( $mod, $value );
	}

	// Front page using Storefront's homepage template, only if none is set yet.
	if ( 'page' !== get_option( 'show_on_front' ) || ! get_option( 'page_on_front' ) ) {
		$existing = get_page_by_path( 'glavnaya' );
		$page_id  = $existing ? $existing->ID : wp_insert_post(
			array(
				'post_title'  => 'Главная',
				'post_name'   => 'glavnaya',
				'post_status' => 'publish',
				'post_type'   => 'page',
			)
		);
		if ( $page_id && ! is_wp_error( $page_id ) ) {
			update_post_meta( $page_id, '_wp_page_template', 'template-homepage.php' );
			update_option( 'show_on_front', 'page' );
			update_option( 'page_on_front', $page_id );
		}
	}
}

/* -------------------------------------------------------------------------
 * Shop grid
 * ---------------------------------------------------------------------- */

add_filter( 'loop_shop_columns', function () {
	return 3;
}, 20 );

add_filter( 'loop_shop_per_page', function () {
	return 24;
}, 20 );

add_filter( 'storefront_related_products_args', function ( $args ) {
	$args['posts_per_page'] = 4;
	$args['columns']        = 4;
	return $args;
} );

/* Nicer placeholder while products have no photos. */
add_filter( 'woocommerce_placeholder_img_src', function () {
	return get_stylesheet_directory_uri() . '/assets/placeholder.svg';
} );

/* -------------------------------------------------------------------------
 * Header: announcement bar
 * ---------------------------------------------------------------------- */

add_action( 'storefront_before_header', function () {
	?>
	<div class="palitra-topbar">
		<div class="col-full">
			<span>Доставка по всей России</span>
			<span class="palitra-topbar__dot" aria-hidden="true">·</span>
			<span>Новые поступления каждую неделю</span>
			<span class="palitra-topbar__dot" aria-hidden="true">·</span>
			<a href="<?php echo esc_url( PALITRA_OZON_URL ); ?>" target="_blank" rel="noopener">Мы на Ozon →</a>
		</div>
	</div>
	<?php
} );

/* -------------------------------------------------------------------------
 * Small inline art: a row of pastel sticks
 * ---------------------------------------------------------------------- */

function palitra_sticks_svg( array $colours, $class = '' ) {
	$n   = count( $colours );
	$w   = 26;
	$gap = 8;
	$vw  = $n * $w + ( $n - 1 ) * $gap;
	$out = sprintf( '<svg class="%s" viewBox="0 0 %d 120" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">', esc_attr( $class ), $vw );
	foreach ( $colours as $i => $c ) {
		$x    = $i * ( $w + $gap );
		$y    = ( $i % 2 ) ? 14 : 4;
		$out .= sprintf( '<rect x="%d" y="%d" width="%d" height="%d" rx="7" fill="%s"/>', $x, $y, $w, 112 - $y, esc_attr( $c ) );
		$out .= sprintf( '<rect x="%d" y="%d" width="%d" height="22" fill="#fff" opacity=".22"/>', $x, $y + 40, $w );
	}
	return $out . '</svg>';
}

function palitra_category_url( $name ) {
	$term = get_term_by( 'name', $name, 'product_cat' );
	if ( $term && ! is_wp_error( $term ) ) {
		$link = get_term_link( $term );
		if ( ! is_wp_error( $link ) ) {
			return array( $link, (int) $term->count, $term );
		}
	}
	return array( function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/' ), 0, null );
}

function palitra_category_count( $term ) {
	if ( ! $term ) {
		return 0;
	}
	$ids   = get_term_children( $term->term_id, 'product_cat' );
	$total = (int) $term->count;
	if ( ! is_wp_error( $ids ) ) {
		foreach ( $ids as $id ) {
			$child  = get_term( $id, 'product_cat' );
			$total += $child && ! is_wp_error( $child ) ? (int) $child->count : 0;
		}
	}
	return $total;
}

function palitra_plural( $n, $one, $few, $many ) {
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

/* -------------------------------------------------------------------------
 * Homepage sections (Storefront "Homepage" template)
 * ---------------------------------------------------------------------- */

add_action( 'init', function () {
	remove_action( 'homepage', 'storefront_homepage_content', 10 );
	remove_action( 'homepage', 'storefront_product_categories', 20 );
	remove_action( 'homepage', 'storefront_featured_products', 40 );
	remove_action( 'homepage', 'storefront_popular_products', 50 );
	remove_action( 'homepage', 'storefront_on_sale_products', 60 );
	remove_action( 'homepage', 'storefront_best_selling_products', 70 );
} );

add_filter( 'storefront_recent_products_args', function ( $args ) {
	$args['title']   = 'Новые поступления';
	$args['limit']   = 8;
	$args['columns'] = 4;
	return $args;
} );

add_action( 'homepage', 'palitra_home_hero', 5 );
function palitra_home_hero() {
	$shop   = function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/' );
	$pastel = palitra_category_url( 'Пастель' )[0];
	?>
	<section class="palitra-hero">
		<div class="palitra-hero__text">
			<p class="palitra-eyebrow">Художественные материалы</p>
			<h1 class="palitra-hero__title">Пастель и краски от лучших мастерских мира</h1>
			<p class="palitra-hero__lead">Unison Colour, Terry Ludwig, Schmincke, Sennelier, PanPastel, Michael Harding — профессиональные материалы для тех, кто рисует всерьёз.</p>
			<div class="palitra-hero__actions">
				<a class="button palitra-btn-light" href="<?php echo esc_url( $pastel ); ?>">Смотреть пастель</a>
				<a class="palitra-link-light" href="<?php echo esc_url( $shop ); ?>">Весь каталог →</a>
			</div>
		</div>
		<div class="palitra-hero__art" aria-hidden="true">
			<img src="<?php echo esc_url( get_stylesheet_directory_uri() . '/assets/hero.svg' ); ?>" alt="" width="640" height="520">
		</div>
	</section>
	<?php
}

add_action( 'homepage', 'palitra_home_categories', 20 );
function palitra_home_categories() {
	$cats = array(
		'Пастель'           => array( '#e8b4b8', '#f2d0a4', '#a8c69f', '#9db4d6', '#c3a6d8' ),
		'Масляные краски'   => array( '#7a2e2e', '#c8962e', '#2f4f3a', '#24364f', '#d9cbb3' ),
		'Акварель'          => array( '#8fc1d4', '#b9d7a6', '#f4c7a1', '#e6a5b9', '#a9a4d6' ),
		'Гуашь'             => array( '#e2574c', '#f3b23e', '#3e8e6c', '#2f62a7', '#f4efe6' ),
		'Акриловые краски'  => array( '#ff6f59', '#ffd23f', '#3bceac', '#4062bb', '#ee4266' ),
		'Бумага'            => array( '#f6eedc', '#e9dcc2', '#d8c6a5', '#c9b089', '#efe7d6' ),
		'Карандаши и кисти' => array( '#3b3b3b', '#6b6b6b', '#a0743c', '#c49a6c', '#2b2b2b' ),
	);
	echo '<section class="palitra-section palitra-cats"><h2 class="section-title">Каталог</h2><div class="palitra-cats__grid">';
	foreach ( $cats as $name => $colours ) {
		list( $url, , $term ) = palitra_category_url( $name );
		if ( ! $term ) {
			continue;
		}
		$count = palitra_category_count( $term );
		printf(
			'<a class="palitra-cat" href="%1$s"><span class="palitra-cat__art">%2$s</span><span class="palitra-cat__name">%3$s</span><span class="palitra-cat__count">%4$d %5$s</span></a>',
			esc_url( $url ),
			palitra_sticks_svg( $colours, 'palitra-cat__svg' ), // phpcs:ignore WordPress.Security.EscapeOutput
			esc_html( $name ),
			$count,
			esc_html( palitra_plural( $count, 'товар', 'товара', 'товаров' ) )
		);
	}
	echo '</div></section>';
}

add_action( 'homepage', 'palitra_home_brands', 35 );
function palitra_home_brands() {
	if ( ! taxonomy_exists( 'product_brand' ) ) {
		return;
	}
	$brands = get_terms(
		array(
			'taxonomy'   => 'product_brand',
			'hide_empty' => true,
			'orderby'    => 'count',
			'order'      => 'DESC',
		)
	);
	if ( empty( $brands ) || is_wp_error( $brands ) ) {
		return;
	}
	echo '<section class="palitra-section palitra-brands"><h2 class="section-title">Бренды</h2><ul class="palitra-brands__list">';
	foreach ( $brands as $b ) {
		$link = get_term_link( $b );
		if ( is_wp_error( $link ) ) {
			continue;
		}
		printf( '<li><a href="%s">%s</a></li>', esc_url( $link ), esc_html( $b->name ) );
	}
	echo '</ul></section>';
}

add_action( 'homepage', 'palitra_home_about', 80 );
function palitra_home_about() {
	?>
	<section class="palitra-section palitra-about">
		<div class="palitra-about__inner">
			<h2 class="section-title">О нас</h2>
			<p>Компания «Палитра» продаёт материалы для рисования и живописи. Мы специализируемся на пастели, акварельных и масляных красках и бумаге.</p>
			<p>В нашем ассортименте — лучшие бренды мягкой и масляной пастели: Terry Ludwig, Schmincke, Unison Colour, Sennelier. Эксклюзивно у нас — краски Michael Harding, а также Winsor &amp; Newton, Talens Van Gogh, Daniel Smith.</p>
			<p>Большая часть ассортимента постоянная, но некоторые товары бывают только один раз. Новинки поступают еженедельно.</p>
		</div>
	</section>
	<?php
}

/* -------------------------------------------------------------------------
 * Footer
 * ---------------------------------------------------------------------- */

add_action( 'init', function () {
	remove_action( 'storefront_footer', 'storefront_credit', 20 );
} );

function palitra_page_link( $slugs, $label ) {
	foreach ( (array) $slugs as $slug ) {
		$p = get_page_by_path( $slug );
		if ( $p && 'publish' === $p->post_status ) {
			return sprintf( '<li><a href="%s">%s</a></li>', esc_url( get_permalink( $p ) ), esc_html( $label ) );
		}
	}
	return '';
}

add_action( 'storefront_footer', 'palitra_footer', 20 );
function palitra_footer() {
	$shop    = function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'shop' ) : home_url( '/' );
	$privacy = function_exists( 'get_privacy_policy_url' ) ? get_privacy_policy_url() : '';
	$info    = palitra_page_link( array( 'dostavka-i-oplata', 'dostavka', 'oplata' ), 'Доставка и оплата' )
		. palitra_page_link( array( 'vozvrat', 'pravila-vozvrata' ), 'Возврат' )
		. palitra_page_link( array( 'oferta', 'publichnaya-oferta' ), 'Публичная оферта' )
		. ( $privacy ? sprintf( '<li><a href="%s">Политика конфиденциальности</a></li>', esc_url( $privacy ) ) : '' )
		. palitra_page_link( array( 'kontakty', 'contacts' ), 'Контакты' );
	?>
	<div class="palitra-footer">
		<div class="palitra-footer__col palitra-footer__brand">
			<p class="palitra-footer__logo"><?php echo esc_html( get_bloginfo( 'name' ) ); ?></p>
			<p>Материалы для рисования и живописи: пастель, масляные и акварельные краски, гуашь, бумага.</p>
		</div>
		<div class="palitra-footer__col">
			<p class="palitra-footer__title">Покупателям</p>
			<ul>
				<li><a href="<?php echo esc_url( $shop ); ?>">Каталог</a></li>
				<?php echo $info; // phpcs:ignore WordPress.Security.EscapeOutput ?>
			</ul>
		</div>
		<div class="palitra-footer__col">
			<p class="palitra-footer__title">Мы в сети</p>
			<ul>
				<li><a href="<?php echo esc_url( PALITRA_OZON_URL ); ?>" target="_blank" rel="noopener">Магазин на Ozon</a></li>
				<li><a href="<?php echo esc_url( PALITRA_VK_URL ); ?>" target="_blank" rel="noopener">ВКонтакте</a></li>
				<li><a href="<?php echo esc_url( PALITRA_TIKTOK_URL ); ?>" target="_blank" rel="noopener">TikTok</a></li>
			</ul>
		</div>
	</div>
	<div class="palitra-copyright">© <?php echo esc_html( gmdate( 'Y' ) . ' ' . get_bloginfo( 'name' ) ); ?></div>
	<?php
}
