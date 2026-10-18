<?php
/**
 * Aloitussisältö: kun teema otetaan käyttöön ensimmäisen kerran, luodaan sivut
 * (Etusivu, Palvelut, Yritykset, Yksityiset, Artistit, Ota yhteyttä),
 * päävalikko ja asetetaan Etusivu sivuston etusivuksi.
 *
 * Olemassa olevia sivuja ei muuteta: jos samalla osoitteella on jo sivu, se ohitetaan.
 *
 * @package kameli-audio
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Luotavat sivut. Avain on sivun polku, arvo [otsikko, lohkomallin tiedosto].
 */
function kameli_audio_starter_pages() {
	return array(
		'etusivu'              => array( 'Etusivu', 'page-etusivu.php' ),
		'palvelut'             => array( 'Palvelut', 'page-palvelut.php' ),
		'palvelut/yritykset'   => array( 'Yritykset', 'page-yritykset.php' ),
		'palvelut/yksityiset'  => array( 'Yksityiset', 'page-yksityiset.php' ),
		'palvelut/artistit'    => array( 'Artistit', 'page-artistit.php' ),
		'ota-yhteytta'         => array( 'Ota yhteyttä', 'page-ota-yhteytta.php' ),
	);
}

/**
 * Lohkomallitiedoston sisältö merkintänä. Ajetaan vasta kun sivut on luotu,
 * jotta sivujen väliset linkit osoittavat oikeisiin osoitteisiin.
 *
 * @param string $file Tiedostonimi patterns-kansiossa.
 */
function kameli_audio_render_pattern_file( $file ) {
	ob_start();
	include get_theme_file_path( 'patterns/' . $file );
	return trim( ob_get_clean() );
}

/**
 * Luo sivut, valikon ja etusivuasetuksen.
 */
function kameli_audio_create_starter_content() {
	if ( get_option( 'kameli_audio_starter_done' ) ) {
		return;
	}
	update_option( 'kameli_audio_starter_done', 1 );

	// Siistit osoitteet (esim. /palvelut/yritykset/), jos sivustolla on vielä oletusmuoto.
	global $wp_rewrite;
	if ( '' === get_option( 'permalink_structure' ) ) {
		$wp_rewrite->set_permalink_structure( '/%postname%/' );
		flush_rewrite_rules( false );
	}

	$created = array();
	foreach ( kameli_audio_starter_pages() as $path => $page ) {
		if ( get_page_by_path( $path ) ) {
			continue;
		}
		$parent_path = dirname( $path );
		$parent      = '.' !== $parent_path ? get_page_by_path( $parent_path ) : null;
		$id          = wp_insert_post(
			array(
				'post_type'   => 'page',
				'post_status' => 'publish',
				'post_title'  => $page[0],
				'post_name'   => basename( $path ),
				'post_parent' => $parent ? $parent->ID : 0,
			)
		);
		if ( $id && ! is_wp_error( $id ) ) {
			$created[ $path ] = $id;
		}
	}

	// Sisältö vasta nyt, kun kaikki sivut ja niiden osoitteet ovat olemassa.
	$pages = kameli_audio_starter_pages();
	foreach ( $created as $path => $id ) {
		wp_update_post(
			array(
				'ID'           => $id,
				'post_content' => wp_slash( kameli_audio_render_pattern_file( $pages[ $path ][1] ) ),
			)
		);
	}

	if ( isset( $created['etusivu'] ) && ! get_option( 'page_on_front' ) ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', $created['etusivu'] );
	}

	kameli_audio_create_navigation();
}
add_action( 'after_switch_theme', 'kameli_audio_create_starter_content' );

/**
 * Päävalikko. Navigaatiolohko käyttää automaattisesti uusinta valikkoa.
 */
function kameli_audio_create_navigation() {
	$items = array(
		'palvelut'            => '',
		'palvelut/yritykset'  => '',
		'palvelut/yksityiset' => '',
		'palvelut/artistit'   => '',
		'ota-yhteytta'        => 'kameli-nav-painike',
	);

	$content = '';
	foreach ( $items as $path => $class ) {
		$page = get_page_by_path( $path );
		if ( ! $page ) {
			continue;
		}
		$attrs = array(
			'label' => $page->post_title,
			'type'  => 'page',
			'id'    => $page->ID,
			'url'   => get_permalink( $page ),
			'kind'  => 'post-type',
		);
		if ( $class ) {
			$attrs['className'] = $class;
		}
		$content .= '<!-- wp:navigation-link ' . wp_json_encode( $attrs, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . ' /-->' . "\n";
	}

	if ( '' === $content ) {
		return;
	}

	wp_insert_post(
		array(
			'post_type'    => 'wp_navigation',
			'post_status'  => 'publish',
			'post_title'   => 'Päävalikko',
			'post_content' => wp_slash( trim( $content ) ),
		)
	);
}
