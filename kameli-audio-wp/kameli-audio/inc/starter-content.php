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
		// Kategoriat ja avainsanat rekisteröitiin tällä pyynnöllä vielä ilman siistejä osoitteita;
		// rekisteröidään uudelleen, jotta /category/…/-osoitteet tulevat sääntöihin.
		create_initial_taxonomies();
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

	if ( isset( $created['etusivu'] ) && ! get_option( 'page_on_front' ) ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', $created['etusivu'] );
	}

	kameli_audio_create_navigation();

	// Varmistetaan, ettei tämän pyynnön aikana tallentunut vajaita osoitesääntöjä.
	delete_option( 'rewrite_rules' );
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
		'blogi'               => '',
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

/**
 * Blogi: kategoriat, Blogi-sivu julkaisujen sivuksi ja luonnosjulkaisut.
 * Ajetaan kerran; myös sivustoille, joilla teeman aiempi versio on jo käytössä.
 */
function kameli_audio_setup_blog() {
	if ( get_option( 'kameli_audio_blog_done' ) ) {
		return;
	}
	update_option( 'kameli_audio_blog_done', 1 );

	$categories = array(
		'asiakastarinat' => array( 'Asiakastarinat', 'Referenssit: toteutuksia asiakkaidemme tapahtumista ja tuotannoista.' ),
		'artikkelit'     => array( 'Artikkelit', 'Vinkkejä tapahtumien tekniikan suunnitteluun ja kurkistuksia tuotantojen taakse.' ),
	);
	$ids        = array();
	foreach ( $categories as $slug => $category ) {
		$term = get_term_by( 'slug', $slug, 'category' );
		if ( ! $term ) {
			$term = wp_insert_term( $category[0], 'category', array( 'slug' => $slug, 'description' => $category[1] ) );
			$ids[ $slug ] = is_wp_error( $term ) ? 0 : (int) $term['term_id'];
		} else {
			$ids[ $slug ] = (int) $term->term_id;
		}
	}

	// Uudet julkaisut menevät oletuksena Artikkeleihin eivätkä "Luokittelemattomiin".
	if ( $ids['artikkelit'] ) {
		update_option( 'default_category', $ids['artikkelit'] );
	}

	$blog = get_page_by_path( 'blogi' );
	if ( ! $blog ) {
		$blog_id = wp_insert_post(
			array(
				'post_type'   => 'page',
				'post_status' => 'publish',
				'post_title'  => 'Blogi',
				'post_name'   => 'blogi',
			)
		);
		$blog    = $blog_id && ! is_wp_error( $blog_id ) ? get_post( $blog_id ) : null;
	}
	if ( $blog && ! get_option( 'page_for_posts' ) ) {
		update_option( 'page_for_posts', $blog->ID );
	}

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

/**
 * Sivustot, joilla teema otettiin käyttöön ennen blogia: blogi lisätään kerran hallinnan puolella.
 */
function kameli_audio_maybe_setup_blog() {
	if ( get_option( 'kameli_audio_starter_done' ) && ! get_option( 'kameli_audio_blog_done' ) && current_user_can( 'manage_options' ) ) {
		kameli_audio_setup_blog();
	}
}
add_action( 'admin_init', 'kameli_audio_maybe_setup_blog' );
