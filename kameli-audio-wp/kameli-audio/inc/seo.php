<?php
/**
 * Hakukoneoptimointi ilman lisäosia: hakutulosotsikko ja -kuvaus jokaiselle sivulle ja
 * julkaisulle (muokattavissa editorin alaosan "Hakukoneet (SEO)" -laatikosta), jakokuvat
 * (Open Graph) LinkedIniin ja Facebookiin sekä yritystiedot Googlelle etusivulla.
 *
 * Jos sivustolle asennetaan Yoast SEO, The SEO Framework, Rank Math tai All in One SEO,
 * teema jättää nämä niiden hoidettaviksi.
 *
 * @package kameli-audio
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Teeman sivujen valmiit hakutulosotsikot ja -kuvaukset (polku => array( otsikko, kuvaus )).
 * Kirjoitettu hakusanojen mukaan, joilla asiakkaat palveluita etsivät.
 */
function kameli_audio_seo_defaults() {
	return array(
		'etusivu'             => array(
			'Kameli Audio – tapahtumatekniikka ja äänitysstudio, Vantaa',
			'Äänentoisto, valot ja tapahtumatekniikka yritystapahtumiin, juhliin ja keikoille sekä äänitysstudio Vantaan Hakkilassa. Pyydä tarjous!',
		),
		'palvelut'            => array(
			'Palvelut: äänentoisto, valot ja studio | Kameli Audio',
			'Tapahtumatekniikkaa yrityksille ja juhliin sekä live- ja studiotuotantoja artisteille. Suunnittelusta purkuun pääkaupunkiseudulla.',
		),
		'palvelut/yritykset'  => array(
			'Äänentoisto ja valot yritystapahtumiin | Kameli Audio',
			'Tapahtumatekniikka pikkujouluihin, seminaareihin, lanseerauksiin ja asiakastilaisuuksiin: äänentoisto, mikitys ja valot suunnittelusta purkuun.',
		),
		'palvelut/yksityiset' => array(
			'Äänentoisto ja valot häihin ja juhliin | Kameli Audio',
			'Äänentoisto ja valaistus häihin, merkkipäiville ja juhliin. Tekniikka asennetaan ja puretaan teidän aikataulunne mukaan. Pyydä tarjous!',
		),
		'palvelut/artistit'   => array(
			'Äänitysstudio, miksaus ja keikkamiksaus | Kameli Audio',
			'Äänitys Oasis Studiolla Vantaan Hakkilassa, miksaus ja masterointi sekä live-tuotannot: PA-treenit, kiertueiden valmistelu ja keikkamiksaus.',
		),
		'ota-yhteytta'        => array(
			'Ota yhteyttä ja pyydä tarjous | Kameli Audio',
			'Kerro tapahtumastasi tai projektistasi, niin palaamme asiaan. Juha Pöysä ja Sakari Juntura – Kameli Audio, Oasis Studio, Hakkila, Vantaa.',
		),
		'blogi'               => array(
			'Blogi ja asiakastarinat | Kameli Audio',
			'Asiakastarinoita toteutuksistamme, vinkkejä tapahtumien tekniikan suunnitteluun ja kurkistuksia tuotantojen taakse.',
		),
	);
}

/**
 * Onko jokin SEO-lisäosa käytössä?
 */
function kameli_audio_seo_plugin_active() {
	return defined( 'WPSEO_VERSION' ) || defined( 'THE_SEO_FRAMEWORK_VERSION' ) || defined( 'RANK_MATH_VERSION' ) || defined( 'AIOSEO_VERSION' );
}

/**
 * Asettaa teeman sivuille valmiit hakutulosotsikot ja -kuvaukset, jos niitä ei ole vielä annettu.
 */
function kameli_audio_apply_seo_defaults() {
	foreach ( kameli_audio_seo_defaults() as $path => $seo ) {
		$page = get_page_by_path( $path );
		if ( ! $page ) {
			continue;
		}
		if ( '' === (string) get_post_meta( $page->ID, '_kameli_seo_title', true ) ) {
			update_post_meta( $page->ID, '_kameli_seo_title', $seo[0] );
		}
		if ( '' === (string) get_post_meta( $page->ID, '_kameli_seo_desc', true ) ) {
			update_post_meta( $page->ID, '_kameli_seo_desc', $seo[1] );
		}
	}
}

/**
 * Sivu tai julkaisu, jota nyt katsotaan (blogin etusivulla Blogi-sivu).
 */
function kameli_audio_seo_object_id() {
	if ( is_home() && get_option( 'page_for_posts' ) ) {
		return (int) get_option( 'page_for_posts' );
	}
	if ( is_front_page() && get_option( 'page_on_front' ) ) {
		return (int) get_option( 'page_on_front' );
	}
	return is_singular() ? (int) get_queried_object_id() : 0;
}

/**
 * Hakutulosotsikko: oma, sitten tuodun julkaisun (The SEO Framework / Yoast) arvo.
 *
 * @param int $id Sivun tai julkaisun tunniste.
 */
function kameli_audio_seo_title( $id ) {
	foreach ( array( '_kameli_seo_title', '_genesis_title', '_yoast_wpseo_title' ) as $key ) {
		$value = trim( (string) get_post_meta( $id, $key, true ) );
		if ( '' !== $value && false === strpos( $value, '%%' ) ) {
			return $value;
		}
	}
	return '';
}

/**
 * Hakutuloskuvaus: oma, tuotu, tiivistelmä tai sisällön alku (enintään noin 155 merkkiä).
 *
 * @param int $id Sivun tai julkaisun tunniste.
 */
function kameli_audio_seo_description( $id ) {
	foreach ( array( '_kameli_seo_desc', '_genesis_description', '_yoast_wpseo_metadesc' ) as $key ) {
		$value = trim( (string) get_post_meta( $id, $key, true ) );
		if ( '' !== $value && false === strpos( $value, '%%' ) ) {
			return $value;
		}
	}
	$post = get_post( $id );
	if ( ! $post ) {
		return '';
	}
	$text = $post->post_excerpt ? $post->post_excerpt : wp_strip_all_tags( strip_shortcodes( excerpt_remove_blocks( $post->post_content ) ) );
	$text = trim( preg_replace( '/\s+/', ' ', $text ) );
	if ( mb_strlen( $text ) > 155 ) {
		$text = rtrim( mb_substr( $text, 0, 152 ), " ,.;:–-" ) . '…';
	}
	return $text;
}

/**
 * Selaimen ja hakutulosten otsikko.
 *
 * @param string $title Oletusotsikko.
 */
function kameli_audio_document_title( $title ) {
	if ( kameli_audio_seo_plugin_active() ) {
		return $title;
	}
	$id = kameli_audio_seo_object_id();
	if ( $id ) {
		$custom = kameli_audio_seo_title( $id );
		if ( '' !== $custom ) {
			return $custom;
		}
	}
	return $title;
}
add_filter( 'pre_get_document_title', 'kameli_audio_document_title' );

/**
 * Kuvaus, jakokuvat ja yritystiedot sivun <head>-osaan.
 */
function kameli_audio_seo_head() {
	if ( kameli_audio_seo_plugin_active() || is_404() || is_search() ) {
		return;
	}

	$id          = kameli_audio_seo_object_id();
	$description = '';
	$url         = '';
	$type        = 'website';
	$image       = get_theme_file_uri( 'assets/images/jakokuva.png' );

	if ( $id ) {
		$description = kameli_audio_seo_description( $id );
		$url         = is_front_page() ? home_url( '/' ) : get_permalink( $id );
		if ( is_single() ) {
			$type = 'article';
		}
		if ( has_post_thumbnail( $id ) ) {
			$image = get_the_post_thumbnail_url( $id, 'large' );
		}
	} elseif ( is_category() || is_tag() ) {
		$description = wp_strip_all_tags( term_description() );
		$url         = get_term_link( get_queried_object() );
	}

	$title = wp_get_document_title();

	if ( '' !== $description ) {
		printf( '<meta name="description" content="%s" />' . "\n", esc_attr( $description ) );
	}
	$og = array(
		'og:locale'    => 'fi_FI',
		'og:type'      => $type,
		'og:site_name' => get_bloginfo( 'name' ),
		'og:title'     => $title,
		'og:description' => $description,
		'og:url'       => is_wp_error( $url ) ? '' : $url,
		'og:image'     => $image,
	);
	foreach ( $og as $property => $content ) {
		if ( '' !== (string) $content ) {
			printf( '<meta property="%s" content="%s" />' . "\n", esc_attr( $property ), esc_attr( $content ) );
		}
	}
	echo '<meta name="twitter:card" content="summary_large_image" />' . "\n";

	if ( is_front_page() ) {
		kameli_audio_business_schema();
	}
}
add_action( 'wp_head', 'kameli_audio_seo_head', 1 );

/**
 * Yoast SEO käytössä: Yoast hoitaa otsikot ja kuvaukset, mutta jos sivulle ei ole Yoastissa
 * kirjoitettu omaa otsikkoa tai kuvausta, käytetään teeman hakusanojen mukaan kirjoitettuja.
 * Yoastissa käsin kirjoitettu arvo menee aina edelle.
 *
 * @param string $value     Yoastin arvo.
 * @param string $yoast_key Yoastin oma kenttä.
 * @param string $our_key   Teeman kenttä.
 */
function kameli_audio_yoast_fallback( $value, $yoast_key, $our_key ) {
	$id = kameli_audio_seo_object_id();
	if ( ! $id || '' !== trim( (string) get_post_meta( $id, $yoast_key, true ) ) ) {
		return $value;
	}
	$ours = trim( (string) get_post_meta( $id, $our_key, true ) );
	return '' !== $ours ? $ours : $value;
}
add_filter(
	'wpseo_title',
	function ( $title ) {
		return kameli_audio_yoast_fallback( $title, '_yoast_wpseo_title', '_kameli_seo_title' );
	}
);
add_filter(
	'wpseo_metadesc',
	function ( $desc ) {
		return kameli_audio_yoast_fallback( $desc, '_yoast_wpseo_metadesc', '_kameli_seo_desc' );
	}
);
add_filter(
	'wpseo_opengraph_title',
	function ( $title ) {
		$id = kameli_audio_seo_object_id();
		if ( $id && '' !== trim( (string) get_post_meta( $id, '_yoast_wpseo_opengraph-title', true ) ) ) {
			return $title;
		}
		return kameli_audio_yoast_fallback( $title, '_yoast_wpseo_title', '_kameli_seo_title' );
	}
);
add_filter(
	'wpseo_opengraph_desc',
	function ( $desc ) {
		$id = kameli_audio_seo_object_id();
		if ( $id && '' !== trim( (string) get_post_meta( $id, '_yoast_wpseo_opengraph-description', true ) ) ) {
			return $desc;
		}
		return kameli_audio_yoast_fallback( $desc, '_yoast_wpseo_metadesc', '_kameli_seo_desc' );
	}
);

/**
 * Yritystiedot Googlelle etusivulla myös silloin, kun SEO-lisäosa on käytössä.
 */
function kameli_audio_business_schema_with_plugin() {
	if ( kameli_audio_seo_plugin_active() && is_front_page() ) {
		kameli_audio_business_schema();
	}
}
add_action( 'wp_head', 'kameli_audio_business_schema_with_plugin', 2 );

/**
 * Yritystiedot (schema.org LocalBusiness), joista Google tunnistaa yrityksen, toimialan ja alueen.
 */
function kameli_audio_business_schema() {
	$data = array(
		'@context'    => 'https://schema.org',
		'@type'       => 'LocalBusiness',
		'@id'         => home_url( '/#yritys' ),
		'name'        => 'Kameli Audio',
		'legalName'   => 'Kameli Audio Oy',
		'url'         => home_url( '/' ),
		'logo'        => get_theme_file_uri( 'assets/images/kameli-audio-logo-tumma.png' ),
		'image'       => get_theme_file_uri( 'assets/images/kameli-audio-logo-tumma.png' ),
		'description' => 'Tapahtumatekniikkaa – äänentoisto ja valot – yritystapahtumiin, juhliin ja keikoille sekä äänitys, miksaus ja masterointi Oasis Studiolla Vantaan Hakkilassa.',
		'address'     => array(
			'@type'           => 'PostalAddress',
			'addressLocality' => 'Vantaa',
			'addressRegion'   => 'Uusimaa',
			'addressCountry'  => 'FI',
		),
		'areaServed'  => array( 'Vantaa', 'Helsinki', 'Espoo', 'Uusimaa', 'Suomi' ),
		'knowsAbout'  => array( 'Tapahtumatekniikka', 'Äänentoisto', 'Valotekniikka', 'Äänitys', 'Miksaus', 'Masterointi', 'Keikkamiksaus' ),
		'email'       => kameli_audio_contact_recipient(),
	);
	/**
	 * Yritystietojen muokkaus, esim. puhelinnumero tai sosiaalisen median profiilit:
	 * add_filter( 'kameli_audio_business_schema', function ( $d ) { $d['telephone'] = '+358…'; return $d; } );
	 */
	$data = apply_filters( 'kameli_audio_business_schema', $data );
	echo '<script type="application/ld+json">' . wp_json_encode( $data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . '</script>' . "\n";
}

/**
 * "Hakukoneet (SEO)" -laatikko sivujen ja julkaisujen muokkausnäkymän alaosaan.
 */
function kameli_audio_seo_meta_box() {
	if ( kameli_audio_seo_plugin_active() ) {
		return;
	}
	add_meta_box( 'kameli-seo', 'Hakukoneet (SEO)', 'kameli_audio_seo_meta_box_html', array( 'page', 'post' ), 'normal', 'default' );
}
add_action( 'add_meta_boxes', 'kameli_audio_seo_meta_box' );

/**
 * Laatikon kentät.
 *
 * @param WP_Post $post Muokattava sivu tai julkaisu.
 */
function kameli_audio_seo_meta_box_html( $post ) {
	wp_nonce_field( 'kameli_seo', 'kameli_seo_nonce' );
	$title = kameli_audio_seo_title( $post->ID );
	$desc  = (string) get_post_meta( $post->ID, '_kameli_seo_desc', true );
	if ( '' === $desc ) {
		$desc = trim( (string) get_post_meta( $post->ID, '_genesis_description', true ) );
	}
	?>
	<p style="margin-top:0">Näin sivu näkyy Googlen hakutuloksissa. Käytä sanoja, joilla asiakkaat palveluita etsivät (esim. <em>äänentoisto, häät, Vantaa</em>).</p>
	<p>
		<label for="kameli-seo-otsikko"><strong>Hakutulosotsikko</strong> <span class="description">(suositus enintään 60 merkkiä)</span></label><br />
		<input type="text" id="kameli-seo-otsikko" name="kameli_seo_title" value="<?php echo esc_attr( $title ); ?>" maxlength="90" style="width:100%" placeholder="<?php echo esc_attr( get_the_title( $post ) . ' – ' . get_bloginfo( 'name' ) ); ?>" />
	</p>
	<p>
		<label for="kameli-seo-kuvaus"><strong>Hakutuloskuvaus</strong> <span class="description">(suositus 120–155 merkkiä)</span></label><br />
		<textarea id="kameli-seo-kuvaus" name="kameli_seo_desc" rows="3" maxlength="300" style="width:100%" placeholder="Jos tyhjä, käytetään tekstin alkua."><?php echo esc_textarea( $desc ); ?></textarea>
	</p>
	<?php
}

/**
 * Laatikon tallennus.
 *
 * @param int $post_id Sivun tai julkaisun tunniste.
 */
function kameli_audio_seo_save( $post_id ) {
	if ( ! isset( $_POST['kameli_seo_nonce'] ) || ! wp_verify_nonce( sanitize_key( wp_unslash( $_POST['kameli_seo_nonce'] ) ), 'kameli_seo' ) ) {
		return;
	}
	if ( ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) || ! current_user_can( 'edit_post', $post_id ) ) {
		return;
	}
	$title = isset( $_POST['kameli_seo_title'] ) ? sanitize_text_field( wp_unslash( $_POST['kameli_seo_title'] ) ) : '';
	$desc  = isset( $_POST['kameli_seo_desc'] ) ? sanitize_textarea_field( wp_unslash( $_POST['kameli_seo_desc'] ) ) : '';
	update_post_meta( $post_id, '_kameli_seo_title', $title );
	update_post_meta( $post_id, '_kameli_seo_desc', $desc );
}
add_action( 'save_post', 'kameli_audio_seo_save' );
