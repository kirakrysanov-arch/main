<?php
/**
 * Aloitussisältö: kun teema otetaan käyttöön ensimmäisen kerran, luodaan sivut
 * (Etusivu, Palvelut, Yritykset, Yksityiset, Artistit, Ota yhteyttä, Blogi),
 * blogin kategoriat (Asiakastarinat, Artikkelit) ja luonnokset, päävalikko,
 * ja asetetaan Etusivu sivuston etusivuksi ja Blogi julkaisujen sivuksi.
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
		'blogi'                => array( 'Blogi', '' ),
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
 * Onko asetuksen osoittama sivu olemassa ja julkaistu?
 *
 * @param string $option page_on_front tai page_for_posts.
 */
function kameli_audio_option_page_ok( $option ) {
	$page = get_post( (int) get_option( $option ) );
	return $page && 'page' === $page->post_type && 'publish' === $page->post_status;
}

/**
 * Luo puuttuvat teeman sivut, blogin, valikon ja etusivuasetuksen. Ajetaan joka kerta, kun
 * teema otetaan käyttöön: jos sivuja on poistettu, ne luodaan uudelleen. Olemassa olevia
 * sivuja ei muuteta.
 */
function kameli_audio_create_starter_content() {
	// Siistit osoitteet (esim. /palvelut/yritykset/), jos sivustolla on vielä oletusmuoto.
	global $wp_rewrite;
	if ( '' === get_option( 'permalink_structure' ) ) {
		$wp_rewrite->set_permalink_structure( '/%postname%/' );
		// Kategoriat ja avainsanat rekisteröitiin tällä pyynnöllä vielä ilman siistejä osoitteita;
		// rekisteröidään uudelleen, jotta /category/…/-osoitteet tulevat sääntöihin.
		create_initial_taxonomies();
		flush_rewrite_rules( false );
	}

	$created = kameli_audio_create_missing_pages( array_keys( kameli_audio_starter_pages() ) );

	// Kategoriat ennen sisältöä, jotta etusivun Asiakastarinat-listaus osoittaa oikeaan kategoriaan.
	kameli_audio_setup_blog();

	// Sisältö vasta nyt, kun kaikki sivut ja niiden osoitteet ovat olemassa.
	$pages = kameli_audio_starter_pages();
	foreach ( $created as $path => $id ) {
		if ( '' === $pages[ $path ][1] ) {
			continue;
		}
		wp_update_post(
			array(
				'ID'           => $id,
				'post_content' => wp_slash( kameli_audio_render_pattern_file( $pages[ $path ][1] ) ),
			)
		);
		update_post_meta( $id, '_kameli_sisalto_versio', KAMELI_AUDIO_CONTENT_VERSION );
	}

	// Etusivu etusivuksi, jos etusivua ei ole asetettu tai se on poistettu.
	$front = get_page_by_path( 'etusivu' );
	if ( $front && ( 'page' !== get_option( 'show_on_front' ) || ! kameli_audio_option_page_ok( 'page_on_front' ) ) ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', $front->ID );
	}

	kameli_audio_create_navigation();
	update_option( 'kameli_audio_starter_done', 1 );
	update_option( 'kameli_audio_version', KAMELI_AUDIO_VERSION );

	// Varmistetaan, ettei tämän pyynnön aikana tallentunut vajaita osoitesääntöjä.
	delete_option( 'rewrite_rules' );
}
add_action( 'after_switch_theme', 'kameli_audio_create_starter_content' );

/**
 * Teeman päivityksen jälkeen (uusi zip ladattu käytössä olevan teeman päälle) sama tarkistus
 * kerran: puuttuvat sivut, blogi ja valikko luodaan. Olemassa olevia sivuja ei muuteta.
 */
function kameli_audio_check_after_update() {
	if ( KAMELI_AUDIO_VERSION === get_option( 'kameli_audio_version' ) || ! current_user_can( 'manage_options' ) ) {
		return;
	}
	update_option( 'kameli_audio_version', KAMELI_AUDIO_VERSION );
	kameli_audio_create_starter_content();
}
add_action( 'admin_init', 'kameli_audio_check_after_update' );

/**
 * Luo annetuista teeman sivuista ne, joita ei ole (vanhemmat ennen lapsia).
 *
 * @param string[] $paths Sivujen polut.
 * @return int[] Luodut sivut: polku => tunniste.
 */
function kameli_audio_create_missing_pages( $paths ) {
	$pages   = kameli_audio_starter_pages();
	$created = array();
	foreach ( $paths as $path ) {
		$existing = get_page_by_path( $path );
		if ( $existing && 'trash' !== $existing->post_status ) {
			continue;
		}
		$parent = '.' !== dirname( $path ) ? get_page_by_path( dirname( $path ) ) : null;
		$id     = wp_insert_post(
			array(
				'post_type'   => 'page',
				'post_status' => 'publish',
				'post_title'  => $pages[ $path ][0],
				'post_name'   => basename( $path ),
				'post_parent' => $parent ? $parent->ID : 0,
			)
		);
		if ( $id && ! is_wp_error( $id ) ) {
			$created[ $path ] = $id;
		}
	}
	return $created;
}

/**
 * Päävalikko teeman sivuista. Jos Päävalikko on jo olemassa, sen linkit päivitetään
 * (esim. kun sivuja on poistettu ja luotu uudelleen). Navigaatiolohko käyttää tätä valikkoa.
 */
function kameli_audio_create_navigation() {
	$items = array(
		'palvelut'            => '',
		'palvelut/yritykset'  => '',
		'palvelut/yksityiset' => '',
		'palvelut/artistit'   => '',
		'blogi'               => '',
		'ota-yhteytta'        => 'kameli-nav-painike',
	);

	$content = '';
	foreach ( $items as $path => $class ) {
		$page = get_page_by_path( $path );
		if ( ! $page || 'publish' !== $page->post_status ) {
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

	$menus = get_posts(
		array(
			'post_type'   => 'wp_navigation',
			'title'       => 'Päävalikko',
			'numberposts' => 1,
		)
	);
	$menu  = array(
		'post_type'    => 'wp_navigation',
		'post_status'  => 'publish',
		'post_title'   => 'Päävalikko',
		'post_content' => wp_slash( trim( $content ) ),
	);
	if ( $menus ) {
		// Jätetään itse muokattu valikko rauhaan, jos kaikki sen sivulinkit ovat yhä voimassa.
		preg_match_all( '/"id":(\d+)/', $menus[0]->post_content, $linked );
		$broken = ! $linked[1];
		foreach ( $linked[1] as $linked_id ) {
			$linked_page = get_post( (int) $linked_id );
			if ( ! $linked_page || 'publish' !== $linked_page->post_status ) {
				$broken = true;
			}
		}
		if ( ! $broken ) {
			return;
		}
		$menu['ID'] = $menus[0]->ID;
		wp_update_post( $menu );
	} else {
		wp_insert_post( $menu );
	}
}

/**
 * Blogi: kategoriat, Blogi-sivu julkaisujen sivuksi ja (vain kerran) luonnosjulkaisut.
 * Turvallinen ajaa monta kertaa: luo vain puuttuvat asiat.
 */
function kameli_audio_setup_blog() {
	$categories = array(
		'asiakastarinat' => array( 'Asiakastarinat', 'Referenssit: toteutuksia asiakkaidemme tapahtumista ja tuotannoista.' ),
		'artikkelit'     => array( 'Artikkelit', 'Vinkkejä tapahtumien tekniikan suunnitteluun ja kurkistuksia tuotantojen taakse.' ),
	);
	$ids        = array();
	foreach ( $categories as $slug => $category ) {
		$term = get_term_by( 'slug', $slug, 'category' );
		if ( ! $term ) {
			$term         = wp_insert_term( $category[0], 'category', array( 'slug' => $slug, 'description' => $category[1] ) );
			$ids[ $slug ] = is_wp_error( $term ) ? 0 : (int) $term['term_id'];
		} else {
			$ids[ $slug ] = (int) $term->term_id;
		}
	}

	// Uudet julkaisut menevät oletuksena Artikkeleihin eivätkä "Luokittelemattomiin".
	if ( $ids['artikkelit'] && ! get_option( 'kameli_audio_blog_done' ) ) {
		update_option( 'default_category', $ids['artikkelit'] );
	}

	$created = kameli_audio_create_missing_pages( array( 'blogi' ) );
	$blog    = get_page_by_path( 'blogi' );
	if ( $blog && ( isset( $created['blogi'] ) || ! kameli_audio_option_page_ok( 'page_for_posts' ) ) ) {
		update_option( 'page_for_posts', $blog->ID );
	}

	if ( get_option( 'kameli_audio_blog_done' ) ) {
		return;
	}
	update_option( 'kameli_audio_blog_done', 1 );

	// WordPressin oma esimerkkijulkaisu luonnokseksi, jos sitä ei ole muokattu.
	$hello = get_post( 1 );
	if ( $hello && 'post' === $hello->post_type && 'publish' === $hello->post_status && $hello->post_modified_gmt === $hello->post_date_gmt ) {
		wp_update_post( array( 'ID' => 1, 'post_status' => 'draft' ) );
	}

	kameli_audio_create_draft_posts( $ids );
	kameli_audio_add_blog_to_navigation( $blog );
}

/**
 * Luonnokset: asiakastarinoiden pohjat ja artikkelit projektisuunnitelman videoaiheista.
 * Luonnokset eivät näy sivustolla ennen julkaisua.
 *
 * @param int[] $ids Kategorioiden tunnisteet.
 */
function kameli_audio_create_draft_posts( $ids ) {
	$case_study = kameli_audio_render_pattern_file( 'asiakastarina.php' );
	$drafts     = array(
		array( 'Asiakastarina: [yritystapahtuma]', 'asiakastarinat', $case_study ),
		array( 'Asiakastarina: [yksityisjuhla]', 'asiakastarinat', $case_study ),
		array( 'Asiakastarina: [bändin äänitys]', 'asiakastarinat', $case_study ),
		array(
			'5 asiaa, jotka kaatavat yritystapahtuman äänimaailman – ja miten ne vältetään',
			'artikkelit',
			kameli_audio_draft_article(
				'Tapahtuman ääni huomataan yleensä vasta, kun jokin menee pieleen. Nämä viisi asiaa näemme useimmin – ja ne ovat kaikki vältettävissä.',
				array( 'Puhetta ei kuule takariveillä', 'Kierto eli mikrofonin kiertävä vinkuna', 'Soundcheck jää väliin', 'Kalusto ei sovi tilaan', 'Kukaan ei vastaa äänestä tapahtuman aikana' )
			),
		),
		array(
			'Miksi äänenlaatu vaikuttaa suoraan asiakaskokemukseen?',
			'artikkelit',
			kameli_audio_draft_article(
				'Yritystapahtumassa ääni on osa brändiä: vieras muistaa, kuuliko hän puheenvuorot ja tuntuiko ilta huolitellulta.',
				array( 'Ääni ratkaisee, mitä viestistä jää mieleen', 'Huono ääni väsyttää yleisön', 'Eri tilaisuudet, eri tarpeet: promo, keynote, lanseeraus' )
			),
		),
		array(
			'Mitä tapahtuu, kun varaat PA-palvelun meiltä?',
			'artikkelit',
			kameli_audio_draft_article(
				'Kuljetuksesta purkuun: näin tapahtuman äänentoisto etenee, kun Kameli Audio on mukana.',
				array( 'Suunnittelu ja tilan kartoitus', 'Kuljetus ja kasaus', 'Soundcheck ja miksaus tapahtuman aikana', 'Purku' )
			),
		),
		array(
			'3 asiaa, jotka fiksaan jokaisessa tapahtumassa',
			'artikkelit',
			kameli_audio_draft_article(
				'Juhan tarkistuslista: kolme asiaa, jotka hoidetaan joka keikalla tilaisuuden koosta riippumatta.',
				array( '[Asia 1]', '[Asia 2]', '[Asia 3]' )
			),
		),
		array(
			'4 ääniasiaa, jotka kannattaa ottaa huomioon tapahtumaa suunniteltaessa',
			'artikkelit',
			kameli_audio_draft_article(
				'Kun ääni otetaan mukaan suunnitteluun ajoissa, tapahtumapäivänä ei tarvitse improvisoida.',
				array( '[Asia 1]', '[Asia 2]', '[Asia 3]', '[Asia 4]' )
			),
		),
	);

	foreach ( $drafts as $draft ) {
		$existing = get_posts(
			array(
				'post_type'   => 'post',
				'post_status' => 'any',
				'title'       => $draft[0],
				'numberposts' => 1,
			)
		);
		if ( $existing ) {
			continue;
		}
		wp_insert_post(
			array(
				'post_type'     => 'post',
				'post_status'   => 'draft',
				'post_title'    => $draft[0],
				'post_content'  => wp_slash( $draft[2] ),
				'post_category' => ! empty( $ids[ $draft[1] ] ) ? array( $ids[ $draft[1] ] ) : array(),
			)
		);
	}
}

/**
 * Artikkeliluonnoksen runko: ingressi, ohje ja väliotsikot.
 *
 * @param string   $lead     Ingressi.
 * @param string[] $sections Väliotsikot.
 */
function kameli_audio_draft_article( $lead, $sections ) {
	$out = kameli_audio_paragraph( esc_html( $lead ), 'lead' )
		. kameli_audio_paragraph( '<em>Luonnos: kirjoitetaan saman aiheen LinkedIn-videon pohjalta. Lisää video tähän (YouTube- tai Vimeo-linkki omalle rivilleen) ja kirjoita kunkin väliotsikon alle 2–4 virkettä.</em>' );
	foreach ( $sections as $section ) {
		$out .= kameli_audio_heading( $section ) . kameli_audio_paragraph( '[Teksti]' );
	}
	return $out . kameli_audio_paragraph( 'Tarvitsetteko äänituotannon seuraavaan tapahtumaan? <a href="#yhteydenotto">Laita viestiä</a>, niin katsotaan päivät.' );
}

/**
 * Lisää Blogi-linkin olemassa olevaan päävalikkoon ennen Ota yhteyttä -painiketta.
 *
 * @param WP_Post|null $blog Blogi-sivu.
 */
function kameli_audio_add_blog_to_navigation( $blog ) {
	if ( ! $blog ) {
		return;
	}
	$menus = get_posts(
		array(
			'post_type'   => 'wp_navigation',
			'title'       => 'Päävalikko',
			'numberposts' => 1,
		)
	);
	if ( ! $menus || false !== strpos( $menus[0]->post_content, '"id":' . $blog->ID . ',' ) ) {
		return;
	}
	$link = '<!-- wp:navigation-link ' . wp_json_encode(
		array(
			'label' => 'Blogi',
			'type'  => 'page',
			'id'    => $blog->ID,
			'url'   => get_permalink( $blog ),
			'kind'  => 'post-type',
		),
		JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE
	) . ' /-->';
	$content = $menus[0]->post_content;
	$pos     = strpos( $content, '<!-- wp:navigation-link {"label":"Ota yhteyttä"' );
	$content = false === $pos ? $content . "\n" . $link : substr_replace( $content, $link . "\n", $pos, 0 );
	wp_update_post(
		array(
			'ID'           => $menus[0]->ID,
			'post_content' => wp_slash( $content ),
		)
	);
}
