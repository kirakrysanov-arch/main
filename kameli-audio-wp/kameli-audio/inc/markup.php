<?php
/**
 * Apufunktiot, jotka tuottavat toistuvien osioiden lohkomerkinnän (hero, kortit,
 * palvelurivit, toimintakehote, yhteydenotto). Lohkomallit (patterns/) kokoavat sivut näistä.
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
 * Lohkon kommentin attribuutit JSON-muodossa.
 *
 * @param array $attrs Attribuutit.
 */
function kameli_audio_attrs( $attrs ) {
	return $attrs ? ' ' . wp_json_encode( $attrs, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) : '';
}

/**
 * Ryhmälohko.
 *
 * @param string $inner   Sisältö.
 * @param string $class   Lisäluokat.
 * @param string $align   "", "wide" tai "full".
 */
function kameli_audio_group( $inner, $class = '', $align = '' ) {
	$attrs = array();
	$cls   = 'wp-block-group';
	if ( $align ) {
		$attrs['align'] = $align;
		$cls           .= ' align' . $align;
	}
	if ( $class ) {
		$attrs['className'] = $class;
		$cls               .= ' ' . $class;
	}
	$attrs['layout'] = array( 'type' => 'default' );
	return "\n" . '<!-- wp:group' . kameli_audio_attrs( $attrs ) . ' -->' . "\n"
		. '<div class="' . $cls . '">' . $inner . '</div>' . "\n"
		. '<!-- /wp:group -->' . "\n";
}

/**
 * Tumma yläosa: yläotsake, H1-otsikko ja alaotsikko. Aaltoviiva piirretään CSS:llä.
 *
 * @param string $eyebrow     Pieni yläotsake.
 * @param string $title       H1-otsikko.
 * @param string $subtitle    Alaotsikko.
 * @param bool   $subtitle_h2 Näytetäänkö alaotsikko H2-otsikkona (muuten kappale).
 */
function kameli_audio_hero( $eyebrow, $title, $subtitle, $subtitle_h2 = false ) {
	if ( $subtitle_h2 ) {
		$sub = "\n" . '<!-- wp:heading {"className":"kameli-alaotsikko","fontSize":"large"} -->' . "\n"
			. '<h2 class="wp-block-heading kameli-alaotsikko has-large-font-size">' . esc_html( $subtitle ) . '</h2>' . "\n"
			. '<!-- /wp:heading -->' . "\n";
	} else {
		$sub = kameli_audio_paragraph( esc_html( $subtitle ), 'lead', 'kameli-alaotsikko' );
	}
	return kameli_audio_section_open( 'hiili', '', 'kameli-hero' )
		. kameli_audio_group(
			kameli_audio_paragraph( esc_html( $eyebrow ), '', 'kameli-eyebrow' )
			. kameli_audio_heading( $title, 1 )
			. $sub,
			'kameli-hero__sisalto',
			'wide'
		)
		. kameli_audio_section_close();
}

/**
 * Osion aloitus: täysleveä ryhmä valitulla taustalla.
 *
 * @param string $background Värin slug (valkoinen, vaalea, hiili, yo, vihrea).
 * @param string $anchor     Valinnainen HTML-ankkuri.
 * @param string $class      Valinnainen lisäluokka.
 */
function kameli_audio_section_open( $background = 'valkoinen', $anchor = '', $class = '' ) {
	$attrs = array();
	if ( $anchor ) {
		$attrs['anchor'] = $anchor;
	}
	$attrs['align'] = 'full';
	if ( $class ) {
		$attrs['className'] = $class;
	}
	$attrs['style']           = array(
		'spacing' => array(
			'padding' => array(
				'top'    => 'var:preset|spacing|70',
				'bottom' => 'var:preset|spacing|70',
			),
		),
	);
	$attrs['backgroundColor'] = $background;
	$classes                  = 'wp-block-group alignfull' . ( $class ? ' ' . $class : '' ) . ' has-' . $background . '-background-color has-background';
	if ( in_array( $background, array( 'hiili', 'yo' ), true ) ) {
		$attrs['textColor'] = 'valkoinen';
		$classes           .= ' has-valkoinen-color has-text-color';
	}
	$attrs['layout'] = array( 'type' => 'constrained' );
	$id              = $anchor ? ' id="' . esc_attr( $anchor ) . '"' : '';
	return '<!-- wp:group' . kameli_audio_attrs( $attrs ) . ' -->' . "\n"
		. '<div' . $id . ' class="' . $classes . '" style="padding-top:var(--wp--preset--spacing--70);padding-bottom:var(--wp--preset--spacing--70)">';
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
 * @param string $text  Teksti.
 * @param int    $level Otsikkotaso.
 * @param string $class Lisäluokka.
 */
function kameli_audio_heading( $text, $level = 2, $class = '' ) {
	$attrs = array();
	$cls   = 'wp-block-heading';
	if ( 2 !== $level ) {
		$attrs['level'] = $level;
	}
	if ( $class ) {
		$attrs['className'] = $class;
		$cls               .= ' ' . $class;
	}
	return "\n" . '<!-- wp:heading' . kameli_audio_attrs( $attrs ) . ' -->' . "\n"
		. '<h' . $level . ' class="' . $cls . '">' . esc_html( $text ) . '</h' . $level . '>' . "\n"
		. '<!-- /wp:heading -->' . "\n";
}

/**
 * Kappale.
 *
 * @param string $text  Teksti (sallittu: linkit, lihavointi).
 * @param string $extra Valinnaiset asetukset: "small", "lead".
 * @param string $class Lisäluokka.
 */
function kameli_audio_paragraph( $text, $extra = '', $class = '' ) {
	$attrs   = array();
	$classes = array();
	$opts    = array_filter( explode( ' ', $extra ) );
	if ( $class ) {
		$attrs['className'] = $class;
		$classes[]          = $class;
	}
	if ( in_array( 'small', $opts, true ) ) {
		$attrs['fontSize'] = 'small';
		$classes[]         = 'has-small-font-size';
	}
	if ( in_array( 'lead', $opts, true ) ) {
		$attrs['fontSize'] = 'large';
		$classes[]         = 'has-large-font-size';
	}
	$cls = $classes ? ' class="' . implode( ' ', $classes ) . '"' : '';
	return "\n" . '<!-- wp:paragraph' . kameli_audio_attrs( $attrs ) . ' -->' . "\n"
		. '<p' . $cls . '>' . wp_kses_post( $text ) . '</p>' . "\n"
		. '<!-- /wp:paragraph -->' . "\n";
}

/**
 * Luettelo.
 *
 * @param string[] $items Rivit.
 * @param string   $class Lisäluokka.
 */
function kameli_audio_list( $items, $class = 'kameli-lista' ) {
	$out = "\n" . '<!-- wp:list' . kameli_audio_attrs( array( 'className' => $class ) ) . ' -->' . "\n" . '<ul class="wp-block-list ' . $class . '">';
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
	return "\n" . '<!-- wp:image' . kameli_audio_attrs( $attrs ) . ' -->' . "\n"
		. '<figure class="wp-block-image size-full is-resized' . ( $class ? ' ' . $class : '' ) . '"><img src="' . kameli_audio_image( $file ) . '" alt="' . esc_attr( $alt ) . '" style="width:' . esc_attr( $width ) . '"/></figure>' . "\n"
		. '<!-- /wp:image -->' . "\n";
}

/**
 * Kortti (ryhmä Kortti-tyylillä).
 *
 * @param string $inner Sisältö.
 * @param string $class Lisäluokka.
 */
function kameli_audio_card( $inner, $class = '' ) {
	return kameli_audio_group( $inner, trim( 'is-style-kortti ' . $class ) );
}

/**
 * Sarakkeet.
 *
 * @param string[] $columns Sarakkeiden sisällöt.
 * @param string[] $widths  Valinnaiset leveydet, esim. array( '40%', '60%' ).
 * @param string   $class   Lisäluokka.
 */
function kameli_audio_columns( $columns, $widths = array(), $class = '' ) {
	$attrs = array( 'align' => 'wide' );
	if ( $class ) {
		$attrs['className'] = $class;
	}
	$attrs['style'] = array(
		'spacing' => array(
			'blockGap' => array(
				'left' => 'var:preset|spacing|50',
				'top'  => 'var:preset|spacing|40',
			),
		),
	);
	$out = "\n" . '<!-- wp:columns' . kameli_audio_attrs( $attrs ) . ' -->' . "\n"
		. '<div class="wp-block-columns alignwide' . ( $class ? ' ' . $class : '' ) . '">';
	foreach ( array_values( $columns ) as $i => $column ) {
		if ( ! empty( $widths[ $i ] ) ) {
			$out .= '<!-- wp:column {"width":"' . $widths[ $i ] . '"} -->' . "\n" . '<div class="wp-block-column" style="flex-basis:' . $widths[ $i ] . '">';
		} else {
			$out .= '<!-- wp:column -->' . "\n" . '<div class="wp-block-column">';
		}
		$out .= $column . '</div>' . "\n" . '<!-- /wp:column -->' . "\n\n";
	}
	return rtrim( $out ) . '</div>' . "\n" . '<!-- /wp:columns -->' . "\n";
}

/**
 * Osion otsikkoalue: yläotsake, H2 ja valinnainen johdanto.
 *
 * @param string $eyebrow Yläotsake.
 * @param string $title   Otsikko.
 * @param string $text    Johdanto.
 */
function kameli_audio_section_head( $eyebrow, $title, $text = '' ) {
	return kameli_audio_group(
		kameli_audio_paragraph( esc_html( $eyebrow ), '', 'kameli-eyebrow' )
		. kameli_audio_heading( $title, 2, 'kameli-osio-otsikko' )
		. ( $text ? kameli_audio_paragraph( $text, 'lead', 'kameli-johdanto' ) : '' ),
		'kameli-osion-alku',
		'wide'
	);
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
		kameli_audio_image_block( $icon, '44px', '', 'kameli-ikoni' )
		. kameli_audio_heading( $title, 3 )
		. kameli_audio_paragraph( $text )
		. kameli_audio_paragraph( '<a class="kameli-lue-lisaa" href="' . $url . '">Lue lisää</a>' ),
		'kameli-palvelukortti'
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
		),
		array(),
		'kameli-korttirivi'
	);
}

/**
 * Palvelurivi palvelusivuille: otsikko vasemmalla, leipäteksti ja luettelo oikealla.
 *
 * @param string   $title Otsikko.
 * @param string   $body  Leipäteksti.
 * @param string[] $items Luettelon rivit.
 * @param string   $after Valinnainen loppukappale.
 */
function kameli_audio_service_block( $title, $body, $items, $after = '' ) {
	return kameli_audio_columns(
		array(
			kameli_audio_heading( $title, 2, 'kameli-palvelurivi__otsikko' ),
			kameli_audio_paragraph( $body, 'lead' )
				. kameli_audio_list( $items )
				. ( $after ? kameli_audio_paragraph( $after ) : '' ),
		),
		array( '38%', '62%' ),
		'kameli-palvelurivi'
	);
}

/**
 * Palvelurivit yhtenä valkoisena osiona.
 *
 * @param string $eyebrow Yläotsake.
 * @param array  $rows    Taulukko kameli_audio_service_block-argumenteista.
 */
function kameli_audio_service_rows( $eyebrow, $rows ) {
	$out = kameli_audio_section_open( 'valkoinen' )
		. kameli_audio_group( kameli_audio_paragraph( esc_html( $eyebrow ), '', 'kameli-eyebrow' ), 'kameli-osion-alku', 'wide' );
	foreach ( $rows as $row ) {
		$out .= call_user_func_array( 'kameli_audio_service_block', $row );
	}
	return $out . kameli_audio_section_close();
}

/**
 * "Miksi valita Kameli Audio" -osio tummalla taustalla.
 */
function kameli_audio_why_us() {
	$tiles = array(
		array( 'Ammattitason kalusto', 'Ammattitason kalusto ja kokemus sekä pienistä että suurista tapahtumista.' ),
		array( 'Suunniteltu tilaasi', 'Suunnittelu ja toteutus tilan, ohjelman ja yleisömäärän mukaan.' ),
		array( 'Ihmisläheinen tapa toimia', 'Joustava, selkeä ja ihmisläheinen tekemisen tapa.' ),
		array( 'Muusikon korvat', 'Esiintyjänä ja muusikkona toimiva ääniteknikko, joka ymmärtää sekä esiintyjän että järjestäjän näkökulman.' ),
	);
	$cols = array();
	foreach ( $tiles as $tile ) {
		$cols[] = kameli_audio_heading( $tile[0], 3, 'kameli-syy__otsikko' ) . kameli_audio_paragraph( $tile[1] );
	}
	return kameli_audio_section_open( 'yo', '', 'kameli-miksi' )
		. kameli_audio_section_head( 'Miksi Kameli Audio', 'Ääni, josta ei tarvitse huolehtia' )
		. kameli_audio_columns( $cols, array(), 'kameli-syyt' )
		. kameli_audio_section_close();
}

/**
 * Hiekanvärinen toimintakehotekaista.
 *
 * @param string $title Otsikko.
 * @param string $text  Teksti.
 */
function kameli_audio_cta( $title = 'Tarvitsetteko äänituotannon seuraavaan tapahtumaan?', $text = 'Laita viestiä, niin katsotaan päivät.' ) {
	return kameli_audio_section_open( 'vihrea', '', 'kameli-cta' )
		. kameli_audio_columns(
			array(
				kameli_audio_heading( $title, 2 ) . kameli_audio_paragraph( esc_html( $text ), 'lead' ),
				"\n" . '<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"right"}} -->' . "\n"
				. '<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"hiili","textColor":"valkoinen"} -->' . "\n"
				. '<div class="wp-block-button"><a class="wp-block-button__link has-valkoinen-color has-hiili-background-color has-text-color has-background wp-element-button" href="#yhteydenotto">Pyydä tarjous</a></div>' . "\n"
				. '<!-- /wp:button --></div>' . "\n"
				. '<!-- /wp:buttons -->' . "\n",
			),
			array( '66%', '34%' ),
			'kameli-cta__rivi'
		)
		. kameli_audio_section_close();
}

/**
 * Yhteydenotto-osio (ankkuri #yhteydenotto): tiedot vasemmalla, lomake oikealla.
 *
 * @param string $title Otsikko.
 */
function kameli_audio_contact_section( $title = 'Kerro tapahtumastasi' ) {
	$info = kameli_audio_paragraph( 'Yhteydenotto', '', 'kameli-eyebrow' )
		. kameli_audio_heading( $title, 2, 'kameli-osio-otsikko' )
		. kameli_audio_paragraph( 'Kerro päivämäärä, paikka ja arvio yleisömäärästä – tai projektistasi studiossa – niin palaamme asiaan.' )
		. kameli_audio_list(
			array(
				'<a href="mailto:juha@kameliaudio.fi">juha@kameliaudio.fi</a>',
				'<a href="mailto:sakari@kameliaudio.fi">sakari@kameliaudio.fi</a>',
				'Kameli Studio, Hakkila, Vantaa',
			),
			'kameli-yhteystiedot'
		);
	$form = kameli_audio_card( "\n" . '<!-- wp:shortcode -->' . "\n" . '[kameli_yhteydenotto]' . "\n" . '<!-- /wp:shortcode -->' . "\n", 'kameli-lomakekortti' );
	return kameli_audio_section_open( 'vaalea', 'yhteydenotto' )
		. kameli_audio_columns( array( $info, $form ), array( '40%', '60%' ), 'kameli-yhteys' )
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
		kameli_audio_image_block( 'henkilo-paikkamerkki.svg', '100%', $name, 'kameli-henkilokuva' )
		. kameli_audio_paragraph( esc_html( $role ), '', 'kameli-eyebrow' )
		. kameli_audio_heading( $name, 3 )
		. kameli_audio_paragraph( esc_html( $bio ) )
		. kameli_audio_list(
			array(
				'<a href="tel:' . esc_attr( $tel ) . '">' . esc_html( $phone ) . '</a>',
				'<a href="mailto:' . esc_attr( $email ) . '">' . esc_html( $email ) . '</a>',
			),
			'kameli-yhteystiedot'
		),
		'kameli-henkilokortti'
	);
}
