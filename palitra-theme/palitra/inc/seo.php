<?php
/**
 * Lightweight SEO: titles, meta descriptions, Open Graph, brand/category intros.
 * Steps aside automatically when Yoast, Rank Math, AIOSEO or SEOPress is active.
 *
 * @package palitra
 */

defined( 'ABSPATH' ) || exit;

function palitra_seo_plugin_active() {
	return defined( 'WPSEO_VERSION' ) || class_exists( 'RankMath' ) || defined( 'AIOSEO_VERSION' ) || defined( 'SEOPRESS_VERSION' );
}

/** Russian brand names and short intros for brand pages. */
function palitra_brand_ru() {
	return array(
		'unison colour'   => array( 'Юнисон Колор', 'Пастель Unison Colour (Юнисон) изготавливают вручную в Нортумберленде, Англия. Палитра славится сложными природными оттенками и мягкой, но плотной текстурой.' ),
		'terry ludwig'    => array( 'Терри Людвиг', 'Terry Ludwig (Терри Людвиг) — американская мастерская ручной мягкой пастели. Квадратные палочки с высокой концентрацией пигмента дают насыщенный бархатистый штрих.' ),
		'schmincke'       => array( 'Шминке', 'Schmincke (Шминке) — немецкий производитель художественных красок, работающий с 1881 года. Мягкая пастель Schmincke известна очень мягкой текстурой и чистотой цвета.' ),
		'sennelier'       => array( 'Сеннелье', 'Sennelier (Сеннелье, Сенелье) — парижский дом художественных материалов, основанный в 1887 году: пастель, масляные стики, гуашь, бумага для пастели.' ),
		'rembrandt'       => array( 'Рембрандт', 'Rembrandt (Рембрандт) — профессиональная серия нидерландской компании Royal Talens. Мягкая пастель Rembrandt отличается высокой светостойкостью.' ),
		'royal talens'    => array( 'Роял Таленс', 'Royal Talens (Роял Таленс) — нидерландский производитель художественных материалов, основанный в 1899 году.' ),
		'van gogh'        => array( 'Ван Гог', 'Van Gogh (Ван Гог) — серия качественных материалов для художников от Royal Talens, Нидерланды.' ),
		'winsor&newton'   => array( 'Винзор энд Ньютон', 'Winsor & Newton (Винзор энд Ньютон, Виндзор и Ньютон) — британский производитель красок для художников с 1832 года.' ),
		'winsor & newton' => array( 'Винзор энд Ньютон', 'Winsor & Newton (Винзор энд Ньютон, Виндзор и Ньютон) — британский производитель красок для художников с 1832 года.' ),
		'michael harding' => array( 'Майкл Хардинг', 'Michael Harding (Майкл Хардинг) — лондонский производитель профессиональных масляных и акварельных красок с высокой концентрацией пигмента.' ),
		'panpastel'       => array( 'ПанПастель', 'PanPastel (ПанПастель, Пан Пастель) — сухая пастель в кюветах, которая наносится спонжами и смешивается как краска, почти без пыли.' ),
		'jack richeson'   => array( 'Джек Ричесон', 'Jack Richeson (Джек Ричесон) — американский производитель художественных материалов; ручная пастель Richeson Handrolled собрана в наборы по тону.' ),
		'holbein'         => array( 'Хольбейн', 'Holbein (Хольбейн, Холбейн) — японский производитель профессиональных красок; гуашь Irodori передаёт традиционные японские цвета.' ),
		'art spectrum'    => array( 'Арт Спектрум', 'Art Spectrum (Арт Спектрум) — австралийский производитель пастели и пастельной бумаги Colourfix.' ),
		'old holland'     => array( 'Олд Холланд', 'Old Holland (Олд Холланд) — нидерландский производитель масляных красок высшего класса по классическим рецептурам.' ),
		'daniel smith'    => array( 'Дэниел Смит', 'Daniel Smith (Дэниел Смит) — американская акварель с необычными минеральными и гранулирующими пигментами.' ),
		'j. luda'         => array( 'Джей Люда', 'J. Luda (Джей Люда) — мягкая пастель ручной работы с плотным насыщенным пигментом.' ),
		'mount vision'    => array( 'Маунт Вижн', 'Mount Vision (Маунт Вижн) — мягкая пастель ручной работы из Непала, крупные палочки с щедрым количеством пигмента.' ),
		'lyra'            => array( 'Лира', 'LYRA (Лира) — немецкий производитель карандашей и материалов для рисования с 1806 года.' ),
		"general's"       => array( 'Дженералс', "General's (Дженералс) — американский производитель карандашей для художников с 1889 года." ),
	);
}

function palitra_brand_ru_info( $name ) {
	$key = function_exists( 'mb_strtolower' ) ? mb_strtolower( html_entity_decode( trim( $name ), ENT_QUOTES ) ) : strtolower( trim( $name ) );
	$key = str_replace( '’', "'", $key );
	$map = palitra_brand_ru();
	return isset( $map[ $key ] ) ? $map[ $key ] : null;
}

/** Short intros for top-level categories. */
function palitra_category_intro( $name ) {
	$map = array(
		'Пастель'           => 'Мягкая и сухая пастель ручной работы от лучших мастерских мира: Unison Colour (Юнисон), Terry Ludwig (Терри Людвиг), Schmincke (Шминке), Sennelier (Сеннелье), Rembrandt, PanPastel, Jack Richeson, Art Spectrum. Наборы и отдельные цвета с доставкой по России.',
		'Масляные краски'   => 'Профессиональные масляные краски и масляные стики: Michael Harding (Майкл Хардинг), Winsor & Newton (Винзор энд Ньютон), Old Holland, Sennelier. Наборы и отдельные тубы.',
		'Акварель'          => 'Акварельные краски в тубах и кюветах: Michael Harding, Winsor & Newton, Daniel Smith, Van Gogh. Наборы для пейзажа, ботаники и скетчинга.',
		'Гуашь'             => 'Художественная гуашь Holbein Irodori и Sennelier: плотные матовые цвета для иллюстрации и живописи.',
		'Акриловые краски'  => 'Профессиональные акриловые краски Schmincke PRIMAcryl.',
		'Бумага'            => 'Бумага для пастели с зерном, которая держит несколько слоёв и хорошо подходит для растушёвки.',
		'Карандаши и кисти' => 'Карандаши LYRA и General\'s, кисти Van Gogh для акварели.',
	);
	return isset( $map[ $name ] ) ? $map[ $name ] : '';
}

/* ---------- Titles ---------- */

add_filter( 'pre_get_document_title', 'palitra_seo_title', 20 );
function palitra_seo_title( $title ) {
	if ( palitra_seo_plugin_active() ) {
		return $title;
	}
	if ( is_singular( 'product' ) ) {
		$t = get_post_meta( get_queried_object_id(), 'pl_seo_title', true );
		if ( $t ) {
			return $t;
		}
	}
	if ( function_exists( 'is_tax' ) && is_tax( 'product_brand' ) ) {
		$term = get_queried_object();
		$ru   = palitra_brand_ru_info( $term->name );
		return $term->name . ( $ru ? ' (' . $ru[0] . ')' : '' ) . ' — купить с доставкой по России | ' . get_bloginfo( 'name' );
	}
	if ( function_exists( 'is_product_category' ) && is_product_category() ) {
		$term = get_queried_object();
		return $term->name . ' — купить в интернет-магазине | ' . get_bloginfo( 'name' );
	}
	return $title;
}

/* ---------- Description + Open Graph ---------- */

function palitra_seo_description() {
	if ( is_singular( 'product' ) ) {
		$id = get_queried_object_id();
		$d  = get_post_meta( $id, 'pl_seo_description', true );
		if ( ! $d ) {
			$d = wp_strip_all_tags( get_the_excerpt( $id ) );
		}
		return $d;
	}
	if ( function_exists( 'is_tax' ) && is_tax( 'product_brand' ) ) {
		$term = get_queried_object();
		$ru   = palitra_brand_ru_info( $term->name );
		if ( $ru ) {
			return $ru[1];
		}
		return wp_strip_all_tags( term_description( $term ) );
	}
	if ( function_exists( 'is_product_category' ) && is_product_category() ) {
		$term = get_queried_object();
		$d    = wp_strip_all_tags( term_description( $term ) );
		if ( ! $d ) {
			$d = palitra_category_intro( $term->name );
		}
		if ( ! $d && $term->parent ) {
			$parent = get_term( $term->parent, 'product_cat' );
			$d      = $term->name . ( $parent && ! is_wp_error( $parent ) ? ' — ' . mb_strtolower( $parent->name ) : '' ) . ' в магазине «Палитра»: оригинальные материалы для художников, бесплатная доставка Ozon по всей России.';
		}
		return $d;
	}
	if ( function_exists( 'is_product_tag' ) && is_product_tag() ) {
		$term = get_queried_object();
		if ( function_exists( 'palitra_new_tag' ) && palitra_new_tag() && (int) palitra_new_tag()->term_id === (int) $term->term_id ) {
			return 'Новые поступления в магазине «Палитра»: свежие наборы пастели и красок Unison Colour, Terry Ludwig, J. Luda, Michael Harding. Бесплатная доставка Ozon.';
		}
		return 'Купить: ' . $term->name . ' — художественные материалы в магазине «Палитра». Оригинальная продукция, бесплатная доставка Ozon по всей России.';
	}
	if ( function_exists( 'is_shop' ) && is_shop() ) {
		return 'Каталог магазина «Палитра»: профессиональная пастель, масляные и акварельные краски, гуашь, бумага и кисти от Unison Colour, Terry Ludwig, Schmincke, Sennelier, PanPastel, Michael Harding. Бесплатная доставка Ozon.';
	}
	if ( is_page() && ! is_front_page() ) {
		$text = wp_strip_all_tags( strip_shortcodes( (string) get_post_field( 'post_content', get_queried_object_id() ) ) );
		$text = trim( preg_replace( '/\s+/u', ' ', $text ) );
		if ( mb_strlen( $text ) > 40 ) {
			$cut = mb_substr( $text, 0, 155 );
			return preg_replace( '/\s+\S*$/u', '', $cut ) . '…';
		}
		return get_the_title() . ' — магазин художественных материалов «Палитра».';
	}
	if ( is_front_page() ) {
		return 'Палитра — магазин художественных материалов: пастель Unison, Terry Ludwig, Schmincke, Sennelier, PanPastel, краски Michael Harding, Winsor & Newton. Доставка по всей России.';
	}
	if ( is_page( 'brendy' ) ) {
		return 'Все бренды художественных материалов в магазине «Палитра» от А до Я: пастель, масляные и акварельные краски, гуашь, бумага.';
	}
	return '';
}

add_action( 'wp_head', 'palitra_seo_head', 2 );
function palitra_seo_head() {
	if ( palitra_seo_plugin_active() ) {
		return;
	}
	$desc = trim( preg_replace( '/\s+/u', ' ', (string) palitra_seo_description() ) );
	if ( function_exists( 'mb_substr' ) && mb_strlen( $desc ) > 170 ) {
		$desc = rtrim( mb_substr( $desc, 0, 167 ) ) . '…';
	}
	if ( $desc ) {
		printf( '<meta name="description" content="%s">' . "\n", esc_attr( $desc ) );
	}

	$title = wp_get_document_title();
	$url   = '';
	$image = '';
	$type  = 'website';
	if ( is_singular() ) {
		$url = get_permalink();
		if ( has_post_thumbnail() ) {
			$image = get_the_post_thumbnail_url( null, 'large' );
		}
		if ( is_singular( 'product' ) ) {
			$type = 'product';
		}
	} elseif ( is_tax() || is_category() ) {
		$link = get_term_link( get_queried_object() );
		$url  = is_wp_error( $link ) ? '' : $link;
	} elseif ( is_front_page() ) {
		$url = home_url( '/' );
	}
	echo '<meta property="og:locale" content="ru_RU">' . "\n";
	printf( '<meta property="og:site_name" content="%s">' . "\n", esc_attr( get_bloginfo( 'name' ) ) );
	printf( '<meta property="og:type" content="%s">' . "\n", esc_attr( $type ) );
	printf( '<meta property="og:title" content="%s">' . "\n", esc_attr( $title ) );
	if ( $desc ) {
		printf( '<meta property="og:description" content="%s">' . "\n", esc_attr( $desc ) );
	}
	if ( $url ) {
		printf( '<meta property="og:url" content="%s">' . "\n", esc_url( $url ) );
	}
	if ( $image ) {
		printf( '<meta property="og:image" content="%s">' . "\n", esc_url( $image ) );
	}
	echo '<meta name="twitter:card" content="summary_large_image">' . "\n";
}

/* ---------- Visible intros on brand & category pages ---------- */

add_action( 'woocommerce_archive_description', 'palitra_archive_intro', 15 );
function palitra_archive_intro() {
	if ( function_exists( 'is_tax' ) && is_tax( 'product_brand' ) ) {
		$term = get_queried_object();
		if ( term_description( $term ) ) {
			return; // WooCommerce already prints the term description.
		}
		$ru = palitra_brand_ru_info( $term->name );
		if ( $ru ) {
			echo '<div class="term-description pl-intro"><p>' . esc_html( $ru[1] ) . '</p></div>';
		}
	} elseif ( function_exists( 'is_product_category' ) && is_product_category() ) {
		$term = get_queried_object();
		if ( term_description( $term ) || 0 !== (int) $term->parent ) {
			return;
		}
		$intro = palitra_category_intro( $term->name );
		if ( $intro ) {
			echo '<div class="term-description pl-intro"><p>' . esc_html( $intro ) . '</p></div>';
		}
	}
}

/* Russian brand name next to the brand title, e.g. "Sennelier · Сеннелье". */
add_filter( 'woocommerce_page_title', function ( $title ) {
	if ( function_exists( 'is_tax' ) && is_tax( 'product_brand' ) ) {
		$ru = palitra_brand_ru_info( $title );
		if ( $ru ) {
			$title .= ' <span class="pl-title-ru">' . esc_html( $ru[0] ) . '</span>';
		}
	}
	return $title;
} );

/* Let shop search find Russian brand names ("Сеннелье") via the product description (already default). */
