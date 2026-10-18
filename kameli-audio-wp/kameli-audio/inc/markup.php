<?php
/**
 * Apufunktiot, jotka tuottavat toistuvien osioiden lohkomerkinnän (hero, kortit,
 * listat, toimintakehote, yhteydenotto). Lohkomallit (patterns/) kokoavat sivut näistä.
 *
 * @package kameli-audio
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Teeman kuvan osoite.
 *
 * @param string $file Tiedostonimi assets/images-kansiossa.
 */
function kameli_audio_image( $file ) {
	return esc_url( get_theme_file_uri( 'assets/images/' . $file ) );
}

/**
 * Sivun osoite polun perusteella (esim. "palvelut/yritykset").
 * Jos sivua ei vielä ole, palautetaan oletusosoite.
 *
 * @param string $path Sivun polku.
 */
function kameli_audio_page_url( $path ) {
	$page = get_page_by_path( $path );
	return esc_url( $page ? get_permalink( $page ) : home_url( '/' . trailingslashit( $path ) ) );
}

/**
 * Musta yläosa sivun otsikolla ja alaotsikolla.
 *
 * @param string $title       H1-otsikko.
 * @param string $subtitle    Alaotsikko.
 * @param bool   $subtitle_h2 Näytetäänkö alaotsikko H2-otsikkona (muuten kappale).
 */
function kameli_audio_hero( $title, $subtitle, $subtitle_h2 = false ) {
	$out  = '<!-- wp:group {"align":"full","className":"kameli-hero","style":{"spacing":{"padding":{"top":"var:preset|spacing|60","bottom":"var:preset|spacing|60"}}},"backgroundColor":"musta","textColor":"valkoinen","layout":{"type":"constrained"}} -->' . "\n";
	$out .= '<div class="wp-block-group alignfull kameli-hero has-valkoinen-color has-musta-background-color has-text-color has-background" style="padding-top:var(--wp--preset--spacing--60);padding-bottom:var(--wp--preset--spacing--60)">';
	$out .= kameli_audio_heading( $title, 1, true );
	if ( $subtitle_h2 ) {
		$out .= "\n\n" . '<!-- wp:heading {"textAlign":"center","className":"kameli-alaotsikko","fontSize":"large"} -->' . "\n";
		$out .= '<h2 class="wp-block-heading has-text-align-center kameli-alaotsikko has-large-font-size">' . esc_html( $subtitle ) . '</h2>' . "\n";
		$out .= '<!-- /wp:heading -->';
	} else {
		$out .= "\n\n" . '<!-- wp:paragraph {"align":"center","className":"kameli-alaotsikko","fontSize":"large"} -->' . "\n";
		$out .= '<p class="has-text-align-center kameli-alaotsikko has-large-font-size">' . esc_html( $subtitle ) . '</p>' . "\n";
		$out .= '<!-- /wp:paragraph -->';
	}
	$out .= '</div>' . "\n" . '<!-- /wp:group -->' . "\n\n";
	return $out;
}

/**
 * Osion aloitus: täysleveä ryhmä valitulla taustalla.
 *
 * @param string $background Värin slug (valkoinen, vaalea, musta).
 * @param string $anchor     Valinnainen HTML-ankkuri.
 */
function kameli_audio_section_open( $background = 'valkoinen', $anchor = '' ) {
	$attrs = array(
		'align'           => 'full',
		'style'           => array(
			'spacing' => array(
				'padding' => array(
					'top'    => 'var:preset|spacing|60',
					'bottom' => 'var:preset|spacing|60',
				),
			),
		),
		'backgroundColor' => $background,
		'layout'          => array( 'type' => 'constrained' ),
	);
	$id = '';
	if ( $anchor ) {
		$attrs = array( 'anchor' => $anchor ) + $attrs;
		$id    = ' id="' . esc_attr( $anchor ) . '"';
	}
	$classes = 'wp-block-group alignfull has-' . $background . '-background-color has-background';
	if ( 'musta' === $background ) {
		$attrs['textColor'] = 'valkoinen';
		$classes           .= ' has-valkoinen-color has-text-color';
	}
	return '<!-- wp:group ' . wp_json_encode( $attrs, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . ' -->' . "\n"
		. '<div' . $id . ' class="' . $classes . '" style="padding-top:var(--wp--preset--spacing--60);padding-bottom:var(--wp--preset--spacing--60)">';
}

/**
 * Osion lopetus.
 */
function kameli_audio_section_close() {
	return '</div>' . "\n" . '<!-- /wp:group -->' . "\n\n";
}

/**
 * Otsikkolohko.
 *
 * @param string $text     Teksti.
 * @param int    $level    Otsikkotaso.
 * @param bool   $centered Keskitetäänkö.
 */
function kameli_audio_heading( $text, $level = 2, $centered = false ) {
	$attrs = array();
	$class = 'wp-block-heading';
	if ( $centered ) {
		$attrs['textAlign'] = 'center';
		$class             .= ' has-text-align-center';
	}
	if ( 2 !== $level ) {
		$attrs['level'] = $level;
	}
	$json = $attrs ? ' ' . wp_json_encode( $attrs ) : '';
	return "\n" . '<!-- wp:heading' . $json . ' -->' . "\n"
		. '<h' . $level . ' class="' . $class . '">' . esc_html( $text ) . '</h' . $level . '>' . "\n"
		. '<!-- /wp:heading -->' . "\n";
}

/**
 * Kappale.
 *
 * @param string $text     Teksti (sallittu: linkit, lihavointi).
 * @param string $extra    Valinnaiset lisäasetukset: "center", "small", "harmaa", "lead".
 */
function kameli_audio_paragraph( $text, $extra = '' ) {
	$attrs   = array();
	$classes = array();
	$opts    = array_filter( explode( ' ', $extra ) );
	if ( in_array( 'center', $opts, true ) ) {
		$attrs['align'] = 'center';
		$classes[]      = 'has-text-align-center';
	}
	if ( in_array( 'harmaa', $opts, true ) ) {
		$attrs['textColor'] = 'harmaa';
		$classes[]          = 'has-harmaa-color has-text-color';
	}
	if ( in_array( 'small', $opts, true ) ) {
		$attrs['fontSize'] = 'small';
		$classes[]         = 'has-small-font-size';
	}
	if ( in_array( 'lead', $opts, true ) ) {
		$attrs['fontSize'] = 'large';
		$classes[]         = 'has-large-font-size';
	}
	$json  = $attrs ? ' ' . wp_json_encode( $attrs ) : '';
	$class = $classes ? ' class="' . implode( ' ', $classes ) . '"' : '';
	return "\n" . '<!-- wp:paragraph' . $json . ' -->' . "\n"
		. '<p' . $class . '>' . wp_kses_post( $text ) . '</p>' . "\n"
		. '<!-- /wp:paragraph -->' . "\n";
}

/**
 * Luettelo.
 *
 * @param string[] $items Rivit.
 */
function kameli_audio_list( $items ) {
	$out = "\n" . '<!-- wp:list -->' . "\n" . '<ul class="wp-block-list">';
	foreach ( $items as $item ) {
		$out .= '<!-- wp:list-item -->' . "\n" . '<li>' . wp_kses_post( $item ) . '</li>' . "\n" . '<!-- /wp:list-item -->';
	}
	return $out . '</ul>' . "\n" . '<!-- /wp:list -->' . "\n";
}

/**
 * Kuva teeman kansiosta.
 *
 * @param string $file  Tiedostonimi.
 * @param string $width Leveys, esim. "44px".
 * @param string $alt   Vaihtoehtoinen teksti.
 * @param string $class Lisäluokka.
 */
function kameli_audio_image_block( $file, $width, $alt = '', $class = '' ) {
	$attrs = array(
		'width'           => $width,
		'sizeSlug'        => 'full',
		'linkDestination' => 'none',
	);
	if ( $class ) {
		$attrs['className'] = $class;
	}
	return "\n" . '<!-- wp:image ' . wp_json_encode( $attrs ) . ' -->' . "\n"
		. '<figure class="wp-block-image size-full is-resized' . ( $class ? ' ' . $class : '' ) . '"><img src="' . kameli_audio_image( $file ) . '" alt="' . esc_attr( $alt ) . '" style="width:' . esc_attr( $width ) . '"/></figure>' . "\n"
		. '<!-- /wp:image -->' . "\n";
}

/**
 * Kortti (ryhmä Kortti-tyylillä).
 *
 * @param string $inner Sisältö.
 */
function kameli_audio_card( $inner ) {
	return '<!-- wp:group {"className":"is-style-kortti","layout":{"type":"constrained"}} -->' . "\n"
		. '<div class="wp-block-group is-style-kortti">' . $inner . '</div>' . "\n"
		. '<!-- /wp:group -->';
}

/**
 * Sarakkeet: jokainen alkio on yhden sarakkeen sisältö.
 *
 * @param string[] $columns Sarakkeiden sisällöt.
 */
function kameli_audio_columns( $columns ) {
	$out = "\n" . '<!-- wp:columns {"align":"wide","style":{"spacing":{"blockGap":{"left":"var:preset|spacing|40","top":"var:preset|spacing|40"}}}} -->' . "\n"
		. '<div class="wp-block-columns alignwide">';
	foreach ( $columns as $column ) {
		$out .= '<!-- wp:column -->' . "\n" . '<div class="wp-block-column">' . $column . '</div>' . "\n" . '<!-- /wp:column -->' . "\n\n";
	}
	return rtrim( $out ) . '</div>' . "\n" . '<!-- /wp:columns -->' . "\n";
}

/**
 * Palvelukortti: ikoni, otsikko, lyhyt kuvaus ja "Lue lisää" -linkki.
 *
 * @param string $icon  Ikonin tiedostonimi.
 * @param string $title Otsikko.
 * @param string $text  Kuvaus.
 * @param string $url   Linkki.
 */
function kameli_audio_service_card( $icon, $title, $text, $url ) {
	return kameli_audio_card(
		kameli_audio_image_block( $icon, '40px' )
		. kameli_audio_heading( $title, 3 )
		. kameli_audio_paragraph( $text, 'small harmaa' )
		. kameli_audio_paragraph( '<a class="kameli-lue-lisaa" href="' . $url . '"><strong>Lue lisää →</strong></a>', 'small' )
	);
}

/**
 * Kolme palvelukorttia: yritykset, yksityiset, artistit.
 */
function kameli_audio_service_cards() {
	return kameli_audio_columns(
		array(
			kameli_audio_service_card( 'ikoni-yritykset.svg', 'Yritystapahtumat', 'Ammattimaiset äänipalvelut konferensseihin, messuille ja yritystilaisuuksiin.', kameli_audio_page_url( 'palvelut/yritykset' ) ),
			kameli_audio_service_card( 'ikoni-yksityiset.svg', 'Yksityistapahtumat', 'Tee juhlastasi ikimuistoinen parhaalla mahdollisella äänentoistolla.', kameli_audio_page_url( 'palvelut/yksityiset' ) ),
			kameli_audio_service_card( 'ikoni-artistit.svg', 'Bändit & Artistit', 'Studiotallennus, miksaus ja masterointi ammattilaisille.', kameli_audio_page_url( 'palvelut/artistit' ) ),
		)
	);
}

/**
 * Palvelukuvaus palvelusivuille: otsikko, leipäteksti ja luettelo.
 *
 * @param string   $title  Otsikko.
 * @param string   $body   Leipäteksti.
 * @param string[] $items  Luettelon rivit.
 * @param string   $after  Valinnainen loppukappale.
 */
function kameli_audio_service_block( $title, $body, $items, $after = '' ) {
	$out = kameli_audio_heading( $title )
		. kameli_audio_paragraph( $body )
		. kameli_audio_list( $items );
	if ( $after ) {
		$out .= kameli_audio_paragraph( $after );
	}
	return $out;
}

/**
 * "Miksi valita Kameli Audio" -osio.
 *
 * @param string $background Taustaväri.
 */
function kameli_audio_why_us( $background = 'vaalea' ) {
	return kameli_audio_section_open( $background )
		. kameli_audio_heading( 'Miksi valita Kameli Audio' )
		. kameli_audio_list(
			array(
				'Ammattitason kalusto ja kokemus sekä pienistä että suurista tapahtumista',
				'Suunnittelu ja toteutus tilan, ohjelman ja yleisömäärän mukaan',
				'Joustava, selkeä ja ihmisläheinen tekemisen tapa',
				'Esiintyjänä ja muusikkona toimiva ääniteknikko, joka ymmärtää sekä esiintyjän että järjestäjän näkökulman',
			)
		)
		. kameli_audio_section_close();
}

/**
 * Musta toimintakehotekaista "Pyydä tarjous" -painikkeella.
 *
 * @param string $text Painikkeen teksti.
 */
function kameli_audio_cta( $text = 'Pyydä tarjous' ) {
	return kameli_audio_section_open( 'musta' )
		. "\n" . '<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->' . "\n"
		. '<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"valkoinen","textColor":"musta"} -->' . "\n"
		. '<div class="wp-block-button"><a class="wp-block-button__link has-musta-color has-valkoinen-background-color has-text-color has-background wp-element-button" href="#yhteydenotto">' . esc_html( $text ) . '</a></div>' . "\n"
		. '<!-- /wp:button --></div>' . "\n"
		. '<!-- /wp:buttons -->' . "\n"
		. kameli_audio_section_close();
}

/**
 * Yhteydenottolomake-osio (ankkuri #yhteydenotto).
 *
 * @param string $title      Otsikko.
 * @param string $background Taustaväri.
 */
function kameli_audio_contact_section( $title = 'Ota yhteyttä', $background = 'vaalea' ) {
	return kameli_audio_section_open( $background, 'yhteydenotto' )
		. kameli_audio_heading( $title, 2, true )
		. "\n" . '<!-- wp:shortcode -->' . "\n" . '[kameli_yhteydenotto]' . "\n" . '<!-- /wp:shortcode -->' . "\n"
		. kameli_audio_section_close();
}

/**
 * Henkilökortti Ota yhteyttä -sivulle.
 *
 * @param string $name  Nimi.
 * @param string $role  Tehtävänimike.
 * @param string $bio   Lyhyt kuvaus.
 * @param string $phone Puhelinnumero.
 * @param string $email Sähköposti.
 */
function kameli_audio_person_card( $name, $role, $bio, $phone, $email ) {
	$tel = preg_replace( '/[^0-9+]/', '', $phone );
	return kameli_audio_card(
		kameli_audio_image_block( 'henkilo-paikkamerkki.svg', '160px', $name, 'kameli-henkilokuva' )
		. kameli_audio_heading( $name, 3, true )
		. kameli_audio_paragraph( '<strong>' . esc_html( $role ) . '</strong>', 'center small' )
		. kameli_audio_paragraph( esc_html( $bio ), 'center small harmaa' )
		. "\n" . '<!-- wp:separator {"backgroundColor":"reuna"} -->' . "\n"
		. '<hr class="wp-block-separator has-text-color has-reuna-color has-alpha-channel-opacity has-reuna-background-color has-background"/>' . "\n"
		. '<!-- /wp:separator -->' . "\n"
		. kameli_audio_paragraph( '<a class="kameli-puhelin" href="tel:' . esc_attr( $tel ) . '">' . esc_html( $phone ) . '</a>', 'center small' )
		. kameli_audio_paragraph( '<a class="kameli-sahkoposti" href="mailto:' . esc_attr( $email ) . '">' . esc_html( $email ) . '</a>', 'center small' )
	);
}
