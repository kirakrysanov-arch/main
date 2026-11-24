<?php
/**
 * Homepage sections, brands page, catalog chips, product details, footer.
 *
 * @package palitra
 */

defined( 'ABSPATH' ) || exit;

/* =========================================================================
 * Homepage (Storefront "Homepage" template)
 * ====================================================================== */

add_action( 'init', function () {
	remove_action( 'homepage', 'storefront_homepage_content', 10 );
	remove_action( 'homepage', 'storefront_product_categories', 20 );
	remove_action( 'homepage', 'storefront_featured_products', 40 );
	remove_action( 'homepage', 'storefront_popular_products', 50 );
	remove_action( 'homepage', 'storefront_on_sale_products', 60 );
	remove_action( 'homepage', 'storefront_best_selling_products', 70 );
	// Storefront's own "Shop by Brand" block (WooCommerce Brands) duplicates «Покупайте по брендам».
	remove_action( 'homepage', 'storefront_woocommerce_brands_homepage_section', 80 );
	// …and its brand line on product pages duplicates the theme's brand link.
	remove_action( 'woocommerce_single_product_summary', 'storefront_woocommerce_brands_single', 4 );
} );

add_filter( 'storefront_recent_products_args', function ( $args ) {
	$args['title']   = 'Новые поступления';
	$args['limit']   = 8;
	$args['columns'] = 4;
	return $args;
} );

/**
 * Hero photo: Customizer choice, else the largest photo of a Unison Colour
 * pastel set, else of any pastel product. Never a drawing.
 */
function palitra_hero_image() {
	static $cache = null;
	if ( null !== $cache ) {
		return $cache;
	}
	$cache = false;
	$id    = (int) get_theme_mod( 'palitra_hero_image' );
	if ( $id ) {
		$src = wp_get_attachment_image_url( $id, 'full' );
		if ( $src ) {
			$cache = array( 'src' => $src, 'link' => palitra_shop_url() );
			return $cache;
		}
	}
	$queries = array();
	if ( taxonomy_exists( 'product_brand' ) ) {
		$queries[] = array( array( 'taxonomy' => 'product_brand', 'field' => 'name', 'terms' => 'Unison Colour' ) );
	}
	$queries[] = array( array( 'taxonomy' => 'product_cat', 'field' => 'name', 'terms' => 'Пастель', 'include_children' => true ) );
	foreach ( $queries as $tax ) {
		$ids = get_posts(
			array(
				'post_type'      => 'product',
				'post_status'    => 'publish',
				'fields'         => 'ids',
				'posts_per_page' => 1,
				'no_found_rows'  => true,
				'tax_query'      => array_merge( array( 'relation' => 'AND' ), $tax, array( palitra_visibility_clause() ) ), // phpcs:ignore WordPress.DB.SlowDBQuery
				'meta_key'       => '_price', // phpcs:ignore WordPress.DB.SlowDBQuery
				'orderby'        => 'meta_value_num',
				'order'          => 'DESC',
				'meta_query'     => array( array( 'key' => '_thumbnail_id', 'compare' => 'EXISTS' ) ), // phpcs:ignore WordPress.DB.SlowDBQuery
			)
		);
		if ( $ids ) {
			$src = get_the_post_thumbnail_url( $ids[0], 'large' );
			if ( $src ) {
				$cache = array( 'src' => $src, 'link' => get_permalink( $ids[0] ) );
				return $cache;
			}
		}
	}
	return $cache;
}

/* Customizer: choose the home page banner photo. */
add_action( 'customize_register', function ( $wp_customize ) {
	$wp_customize->add_section( 'palitra_home', array( 'title' => 'Главная страница (Палитра)', 'priority' => 30 ) );
	$wp_customize->add_setting( 'palitra_hero_image', array( 'sanitize_callback' => 'absint' ) );
	$wp_customize->add_control( new WP_Customize_Media_Control( $wp_customize, 'palitra_hero_image', array(
		'label'     => 'Фото в баннере',
		'section'   => 'palitra_home',
		'mime_type' => 'image',
	) ) );
} );

add_action( 'homepage', 'palitra_home_hero', 5 );
function palitra_home_hero() {
	$tree   = palitra_get_menu_tree();
	$pastel = palitra_shop_url();
	foreach ( $tree as $c ) {
		if ( 'Пастель' === $c['name'] ) {
			$pastel = $c['url'];
		}
	}
	?>
	<section class="pl-hero">
		<div class="pl-hero__text">
			<p class="pl-kicker">Художественные материалы</p>
			<h1 class="pl-hero__title">Профессиональная пастель и&nbsp;краски</h1>
			<p class="pl-hero__lead">Unison Colour, Terry Ludwig, Schmincke, Sennelier, PanPastel, Michael Harding и другие мастерские — с доставкой по всей России.</p>
			<div class="pl-hero__actions">
				<a class="button" href="<?php echo esc_url( $pastel ); ?>">Смотреть пастель</a>
				<a class="button pl-button-ghost" href="<?php echo esc_url( palitra_brands_page_url() ); ?>">Все бренды</a>
			</div>
		</div>
		<?php $hero = palitra_hero_image(); ?>
		<?php if ( $hero ) : ?>
			<a class="pl-hero__art" href="<?php echo esc_url( $hero['link'] ); ?>" tabindex="-1" aria-hidden="true">
				<img src="<?php echo esc_url( $hero['src'] ); ?>" alt="" loading="eager" fetchpriority="high">
			</a>
		<?php endif; ?>
	</section>
	<?php
}

add_action( 'homepage', 'palitra_home_usp', 8 );
function palitra_home_usp() {
	$items = array(
		array( 'truck', 'Доставка Ozon по России', 'В пункты выдачи Ozon' ),
		array( 'shield', 'Оригинальная продукция', 'Напрямую от производителей' ),
		array( 'spark', 'Новинки каждую неделю', 'Редкие наборы и лимитки' ),
		array( 'chat', 'Поможем с выбором', 'Подберём материалы под задачу' ),
	);
	echo '<section class="pl-usp" aria-label="Преимущества"><ul>';
	foreach ( $items as $i ) {
		printf(
			'<li>%s<span><strong>%s</strong><small>%s</small></span></li>',
			palitra_icon( $i[0] ), // phpcs:ignore
			esc_html( $i[1] ),
			esc_html( $i[2] )
		);
	}
	echo '</ul></section>';
}

function palitra_section_head( $title, $link_url = '', $link_text = '' ) {
	echo '<div class="pl-section__head"><h2 class="pl-section__title">' . esc_html( $title ) . '</h2>';
	if ( $link_url ) {
		echo '<a class="pl-section__link" href="' . esc_url( $link_url ) . '">' . esc_html( $link_text ) . ' ' . palitra_icon( 'arrow' ) . '</a>'; // phpcs:ignore
	}
	echo '</div>';
}

function palitra_brand_card( $b ) {
	$logo = isset( $b['logo'] ) ? $b['logo'] : palitra_brand_logo( $b['name'] );
	if ( $logo ) {
		$mark = sprintf( '<img src="%s" alt="" loading="lazy" decoding="async">', esc_url( $logo ) );
	} else {
		$words = preg_split( '/[\s&.]+/u', trim( $b['name'] ), -1, PREG_SPLIT_NO_EMPTY );
		$init  = '';
		foreach ( array_slice( $words, 0, 2 ) as $w ) {
			$init .= function_exists( 'mb_substr' ) ? mb_strtoupper( mb_substr( $w, 0, 1 ) ) : strtoupper( substr( $w, 0, 1 ) );
		}
		$mark = '<span class="pl-brand__mono" aria-hidden="true">' . esc_html( $init ) . '</span>';
	}
	return sprintf(
		'<a class="pl-brand" href="%1$s"><span class="pl-brand__logo">%5$s</span><span class="pl-brand__name">%2$s</span>%6$s<span class="pl-brand__meta">%3$s%4$s</span></a>',
		esc_url( $b['url'] ),
		esc_html( $b['name'] ),
		$b['country'] ? esc_html( $b['country'] ) . ' · ' : '',
		esc_html( palitra_count_label( $b['count'] ) ),
		$mark, // phpcs:ignore WordPress.Security.EscapeOutput -- built above with escaping.
		( function_exists( 'palitra_brand_ru_info' ) && ( $ru = palitra_brand_ru_info( $b['name'] ) ) ) ? '<span class="pl-brand__ru">' . esc_html( $ru[0] ) . '</span>' : ''
	);
}

add_action( 'homepage', 'palitra_home_brands', 20 );
function palitra_home_brands() {
	$brands = palitra_get_brands();
	if ( ! $brands ) {
		return;
	}
	usort(
		$brands,
		function ( $a, $b ) {
			return $b['count'] - $a['count'];
		}
	);
	echo '<section class="pl-section">';
	palitra_section_head( 'Покупайте по брендам', palitra_brands_page_url(), 'Все бренды' );
	echo '<div class="pl-brands-grid">';
	foreach ( array_slice( $brands, 0, 12 ) as $b ) {
		echo palitra_brand_card( $b ); // phpcs:ignore
	}
	echo '</div></section>';
}

add_action( 'homepage', 'palitra_home_categories', 40 );
function palitra_home_categories() {
	$tree = palitra_get_menu_tree();
	if ( ! $tree ) {
		return;
	}
	echo '<section class="pl-section">';
	palitra_section_head( 'Каталог', palitra_shop_url(), 'Все товары' );
	echo '<div class="pl-cats">';
	foreach ( $tree as $c ) {
		$art = ! empty( $c['image'] )
			? sprintf( '<img src="%s" alt="%s" loading="lazy" decoding="async">', esc_url( $c['image'] ), esc_attr( $c['name'] ) )
			: '<span class="pl-cat__word" aria-hidden="true">' . esc_html( $c['name'] ) . '</span>';
		printf(
			'<a class="pl-cat%5$s" href="%1$s"><span class="pl-cat__art">%2$s</span><span class="pl-cat__name">%3$s</span><span class="pl-cat__count">%4$s</span></a>',
			esc_url( $c['url'] ),
			$art, // phpcs:ignore
			esc_html( $c['name'] ),
			esc_html( palitra_count_label( $c['count'] ) ),
			! empty( $c['image'] ) ? ' has-photo' : ' no-photo'
		);
	}
	echo '</div></section>';
}

add_action( 'homepage', 'palitra_home_about', 80 );
function palitra_home_about() {
	?>
	<section class="pl-section pl-about">
		<div class="pl-about__text">
			<h2 class="pl-section__title">О магазине «Палитра»</h2>
			<p>Мы продаём материалы для рисования и живописи и специализируемся на пастели, акварельных и масляных красках и бумаге. В ассортименте — лучшие мастерские мягкой и масляной пастели: Terry Ludwig, Schmincke, Unison Colour, Sennelier. Эксклюзивно у нас — краски Michael Harding.</p>
			<p>Большая часть ассортимента постоянная, но некоторые наборы бывают только один раз. Новинки поступают каждую неделю.</p>
		</div>
		<div class="pl-about__stats">
			<?php
			$brands = palitra_get_brands();
			$total  = 0;
			foreach ( palitra_get_menu_tree() as $c ) {
				$total += $c['count'];
			}
			?>
			<div><strong><?php echo (int) count( $brands ); ?></strong><span>брендов</span></div>
			<div><strong><?php echo (int) $total; ?></strong><span>товаров в наличии</span></div>
			<div><strong>1–2</strong><span>дня на отправку</span></div>
		</div>
	</section>
	<?php
}

/* =========================================================================
 * Brands A–Z page: [palitra_brands]
 * ====================================================================== */

add_shortcode( 'palitra_brands', 'palitra_brands_shortcode' );
function palitra_brands_shortcode() {
	$brands = palitra_get_brands();
	if ( ! $brands ) {
		return '<p>Бренды появятся здесь, когда у товаров будет указан бренд.</p>';
	}
	$groups = array();
	foreach ( $brands as $b ) {
		$letter = function_exists( 'mb_strtoupper' ) ? mb_strtoupper( mb_substr( $b['name'], 0, 1 ) ) : strtoupper( substr( $b['name'], 0, 1 ) );
		if ( ! preg_match( '/\p{L}/u', $letter ) ) {
			$letter = '#';
		}
		$groups[ $letter ][] = $b;
	}
	ksort( $groups );
	ob_start();
	echo '<div class="pl-az">';
	echo '<nav class="pl-az__letters" aria-label="Алфавит">';
	foreach ( array_keys( $groups ) as $l ) {
		printf( '<a href="#brand-%1$s">%2$s</a>', esc_attr( rawurlencode( $l ) ), esc_html( $l ) );
	}
	echo '</nav>';
	foreach ( $groups as $l => $items ) {
		printf( '<section class="pl-az__group" id="brand-%1$s"><h2 class="pl-az__letter">%2$s</h2><div class="pl-brands-grid">', esc_attr( rawurlencode( $l ) ), esc_html( $l ) );
		foreach ( $items as $b ) {
			echo palitra_brand_card( $b ); // phpcs:ignore
		}
		echo '</div></section>';
	}
	echo '</div>';
	return ob_get_clean();
}

/* =========================================================================
 * Catalog pages: chips for sub-categories and brands
 * ====================================================================== */

add_action( 'woocommerce_archive_description', 'palitra_archive_chips', 20 );
function palitra_archive_chips() {
	if ( function_exists( 'is_product_category' ) && is_product_category() ) {
		$term = get_queried_object();
		foreach ( palitra_get_menu_tree() as $cat ) {
			$is_top   = ( $cat['slug'] === $term->slug );
			$is_child = false;
			foreach ( $cat['children'] as $ch ) {
				if ( $ch['slug'] === $term->slug ) {
					$is_child = true;
				}
			}
			if ( ! $is_top && ! $is_child ) {
				continue;
			}
			$active_brand = isset( $_GET['product_brand'] ) ? sanitize_title( wp_unslash( $_GET['product_brand'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification
			if ( $cat['children'] ) {
				echo '<div class="pl-chips" aria-label="Разделы">';
				printf( '<a class="pl-chip%s" href="%s">Все <small>%d</small></a>', $is_top ? ' is-active' : '', esc_url( $cat['url'] ), (int) $cat['count'] );
				foreach ( $cat['children'] as $ch ) {
					printf( '<a class="pl-chip%s" href="%s">%s <small>%d</small></a>', $ch['slug'] === $term->slug ? ' is-active' : '', esc_url( $ch['url'] ), esc_html( $ch['name'] ), (int) $ch['count'] );
				}
				echo '</div>';
			}
			if ( $is_top && count( $cat['brands'] ) > 1 ) {
				echo '<div class="pl-chips pl-chips--brands" aria-label="Бренды"><span class="pl-chips__label">Бренды:</span>';
				foreach ( $cat['brands'] as $b ) {
					$active = ( $active_brand === $b['slug'] );
					printf(
						'<a class="pl-chip%s" href="%s">%s <small>%d</small></a>',
						$active ? ' is-active' : '',
						esc_url( $active ? $cat['url'] : $b['url'] ),
						esc_html( $b['name'] ),
						(int) $b['count']
					);
				}
				echo '</div>';
			}
			break;
		}
	}

	if ( function_exists( 'is_tax' ) && is_tax( 'product_brand' ) ) {
		$term    = get_queried_object();
		$country = palitra_brand_country( $term->name );
		echo '<p class="pl-brand-meta">';
		if ( $country ) {
			echo '<span>' . esc_html( $country ) . '</span>';
		}
		echo '<span>' . esc_html( palitra_count_label( (int) ( palitra_brand_counts()[ $term->slug ] ?? 0 ) ) ) . '</span>';
		echo '<a href="' . esc_url( palitra_brands_page_url() ) . '">Все бренды</a>';
		echo '</p>';

		// Categories this brand appears in.
		$cats = array();
		foreach ( palitra_get_menu_tree() as $cat ) {
			foreach ( $cat['brands'] as $b ) {
				if ( $b['slug'] === $term->slug ) {
					$cats[] = array( $cat, $b['count'] );
				}
			}
		}
		if ( count( $cats ) > 1 ) {
			echo '<div class="pl-chips" aria-label="Разделы бренда">';
			foreach ( $cats as $pair ) {
				printf( '<a class="pl-chip" href="%s">%s <small>%d</small></a>', esc_url( add_query_arg( 'product_brand', $term->slug, $pair[0]['url'] ) ), esc_html( $pair[0]['name'] ), (int) $pair[1] );
			}
			echo '</div>';
		}
	}
}

/* Brand name above the product title in grids. */
add_action( 'woocommerce_shop_loop_item_title', 'palitra_loop_brand', 5 );
function palitra_loop_brand() {
	$b = palitra_product_brand( get_the_ID() );
	if ( $b ) {
		echo '<span class="pl-card__brand">' . esc_html( $b['name'] ) . '</span>';
	}
}

/* Single product: brand link, stock, delivery notes. */
add_action( 'woocommerce_single_product_summary', 'palitra_single_brand', 4 );
function palitra_single_brand() {
	$b = palitra_product_brand( get_the_ID() );
	if ( $b && $b['url'] ) {
		echo '<a class="pl-single__brand" href="' . esc_url( $b['url'] ) . '">' . esc_html( $b['name'] ) . '</a>';
	}
}

add_action( 'woocommerce_single_product_summary', 'palitra_single_notes', 35 );
function palitra_single_notes() {
	?>
	<ul class="pl-single__notes">
		<li><?php echo palitra_icon( 'truck' ); // phpcs:ignore ?><span>Отправка за 1–2 дня. Доставка Ozon в любой пункт выдачи по России.</span></li>
		<li><?php echo palitra_icon( 'shield' ); // phpcs:ignore ?><span>Только оригинальная продукция.</span></li>
		<?php $ret = get_page_by_path( 'vozvrat' ); ?>
		<li><?php echo palitra_icon( 'arrow' ); // phpcs:ignore ?><span>Возврат — через Ozon Доставку<?php if ( $ret && 'publish' === $ret->post_status ) : ?>, <a href="<?php echo esc_url( get_permalink( $ret ) ); ?>">условия возврата</a><?php endif; ?>.</span></li>
	</ul>
	<?php
}

/* =========================================================================
 * Footer
 * ====================================================================== */

add_action( 'init', function () {
	remove_action( 'storefront_footer', 'storefront_credit', 20 );
	remove_action( 'storefront_footer', 'storefront_handheld_footer_bar', 999 );
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
	$privacy = function_exists( 'get_privacy_policy_url' ) ? get_privacy_policy_url() : '';
	$info    = palitra_page_link( array( 'dostavka-i-oplata', 'dostavka', 'oplata' ), 'Доставка и оплата' )
		. palitra_page_link( array( 'vozvrat', 'pravila-vozvrata' ), 'Возврат' )
		. palitra_page_link( array( 'oferta', 'publichnaya-oferta' ), 'Публичная оферта' )
		. ( $privacy ? sprintf( '<li><a href="%s">Политика конфиденциальности</a></li>', esc_url( $privacy ) ) : '' )
		. palitra_page_link( array( 'kontakty', 'contacts' ), 'Контакты' );
	?>
	<div class="pl-footer">
		<div class="pl-footer__brand">
			<img class="pl-logo__img pl-footer__logo" src="<?php echo esc_url( palitra_logo_url() ); ?>" alt="<?php echo esc_attr( get_bloginfo( 'name' ) ); ?>" width="82" height="86">
			<p>Материалы для рисования и живописи: пастель, масляные и акварельные краски, гуашь, бумага.</p>
		</div>
		<div>
			<p class="pl-footer__title">Каталог</p>
			<ul>
				<li><a href="<?php echo esc_url( palitra_brands_page_url() ); ?>">Бренды</a></li>
				<?php foreach ( palitra_get_menu_tree() as $c ) : ?>
					<li><a href="<?php echo esc_url( $c['url'] ); ?>"><?php echo esc_html( $c['name'] ); ?></a></li>
				<?php endforeach; ?>
			</ul>
		</div>
		<div>
			<p class="pl-footer__title">Покупателям</p>
			<ul>
				<?php echo $info; // phpcs:ignore ?>
				<?php if ( function_exists( 'wc_get_page_permalink' ) ) : ?>
					<li><a href="<?php echo esc_url( wc_get_page_permalink( 'myaccount' ) ); ?>">Личный кабинет</a></li>
				<?php endif; ?>
			</ul>
		</div>
		<div>
			<p class="pl-footer__title">Мы в сети</p>
			<ul>
				<li><a href="<?php echo esc_url( PALITRA_OZON_URL ); ?>" target="_blank" rel="noopener">Магазин на Ozon</a></li>
				<li><a href="<?php echo esc_url( PALITRA_VK_URL ); ?>" target="_blank" rel="noopener">ВКонтакте</a></li>
				<li><a href="<?php echo esc_url( PALITRA_TIKTOK_URL ); ?>" target="_blank" rel="noopener">TikTok</a></li>
			</ul>
		</div>
	</div>
	<div class="pl-copyright">© <?php echo esc_html( gmdate( 'Y' ) . ' ' . get_bloginfo( 'name' ) ); ?></div>
	<?php
}
