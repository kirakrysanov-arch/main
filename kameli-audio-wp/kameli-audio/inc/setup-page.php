<?php
/**
 * Asennussivu (Ulkoasu → Kameli Audio -asennus) sivustoille, joilla oli jo sisältöä
 * ennen teemaa: näyttää, mitkä teeman sivut puuttuvat tai sisältävät vielä vanhaa sisältöä,
 * ja korvaa valitut sivut teeman sisällöllä. Vanha sisältö jää sivun versiohistoriaan.
 *
 * @package kameli-audio
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Sivupohjien tekstien versio. Kasvatetaan, kun teeman sivujen tekstejä muutetaan, jotta
 * asennussivu tarjoaa päivitettyjä tekstejä jo luoduille sivuille.
 */
const KAMELI_AUDIO_CONTENT_VERSION = 2;

/**
 * Teeman sivujen tila.
 *
 * @return array[] Polku => array( title, file, page (WP_Post|null), state ).
 *                 state: "ok", "vanha" (vanha sisältö), "paivitys" (teeman sivu, uudemmat
 *                 tekstit saatavilla) tai "puuttuu".
 */
function kameli_audio_page_states() {
	$states = array();
	foreach ( kameli_audio_starter_pages() as $path => $page ) {
		$post  = get_page_by_path( $path );
		$state = 'ok';
		if ( ! $post || 'trash' === $post->post_status ) {
			$post  = null;
			$state = 'puuttuu';
		} elseif ( '' === $page[1] ) {
			// Blogi-sivun sisältöä ei näytetä; tärkeää on, että se on julkaisujen sivu.
			$state = (int) get_option( 'page_for_posts' ) === $post->ID ? 'ok' : 'vanha';
		} elseif ( false === strpos( $post->post_content, 'kameli-' ) ) {
			$state = 'vanha';
		} elseif ( (int) get_post_meta( $post->ID, '_kameli_sisalto_versio', true ) < KAMELI_AUDIO_CONTENT_VERSION ) {
			$state = 'paivitys';
		}
		if ( 'etusivu' === $path && $post && 'ok' === $state && ( 'page' !== get_option( 'show_on_front' ) || (int) get_option( 'page_on_front' ) !== $post->ID ) ) {
			$state = 'vanha';
		}
		$states[ $path ] = array(
			'title' => $page[0],
			'file'  => $page[1],
			'page'  => $post,
			'state' => $state,
		);
	}
	return $states;
}

/**
 * Onko asennus kesken (jokin teeman sivu puuttuu tai on vanha)?
 */
function kameli_audio_setup_incomplete() {
	foreach ( kameli_audio_page_states() as $state ) {
		if ( 'ok' !== $state['state'] ) {
			return true;
		}
	}
	return false;
}

/**
 * Valikkokohta.
 */
function kameli_audio_setup_menu() {
	add_theme_page( 'Kameli Audio -asennus', 'Kameli Audio -asennus', 'manage_options', 'kameli-audio-asennus', 'kameli_audio_setup_page' );
}
add_action( 'admin_menu', 'kameli_audio_setup_menu' );

/**
 * Ilmoitus hallinnan etusivulla ja teemasivulla, kun asennus on kesken.
 */
function kameli_audio_setup_notice() {
	$screen = get_current_screen();
	if ( ! current_user_can( 'manage_options' ) || ! $screen || ! in_array( $screen->id, array( 'dashboard', 'themes' ), true ) ) {
		return;
	}
	if ( ! kameli_audio_setup_incomplete() ) {
		return;
	}
	printf(
		'<div class="notice notice-warning"><p><strong>Kameli Audio:</strong> osa teeman sivuista puuttuu, sisältää vielä vanhan sivuston sisältöä tai niihin on saatavilla päivitetyt tekstit. <a href="%s">Viimeistele asennus →</a></p></div>',
		esc_url( admin_url( 'themes.php?page=kameli-audio-asennus' ) )
	);
}
add_action( 'admin_notices', 'kameli_audio_setup_notice' );

/**
 * Asennussivun HTML.
 */
function kameli_audio_setup_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	$states = kameli_audio_page_states();
	$labels = array(
		'ok'      => '<span style="color:#1d7a52">✓ Kunnossa</span>',
		'vanha'    => '<span style="color:#b26200">Vanha sisältö</span>',
		'paivitys' => '<span style="color:#1d5fb3">Uudemmat tekstit saatavilla</span>',
		'puuttuu' => '<span style="color:#b3261e">Puuttuu</span>',
	);
	?>
	<div class="wrap">
		<h1>Kameli Audio -asennus</h1>
		<?php if ( isset( $_GET['valmis'] ) ) : // phpcs:ignore WordPress.Security.NonceVerification.Recommended ?>
			<div class="notice notice-success"><p>Valmis. <a href="<?php echo esc_url( home_url( '/' ) ); ?>" target="_blank">Avaa sivusto →</a></p></div>
		<?php endif; ?>
		<p style="max-width:720px">Teema luo omat sivunsa, mutta ei koskaan muuta olemassa olevia sivuja itsestään. Jos sivustolla oli jo sisältöä ennen teemaa, valitse alta sivut, jotka korvataan teeman sisällöllä. <strong>Vanha sisältö säilyy sivun versiohistoriassa</strong> (sivun muokkausnäkymä → Versiot), joten sen voi palauttaa. Jos versiohistoria on sivustolla pois käytöstä, vanha sisältö tallennetaan luonnokseksi nimellä ”Vanha: …”.</p>

		<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
			<input type="hidden" name="action" value="kameli_audio_asennus" />
			<?php wp_nonce_field( 'kameli_audio_asennus' ); ?>
			<table class="widefat striped" style="max-width:900px">
				<thead>
					<tr>
						<th style="width:2.5em"></th>
						<th>Sivu</th>
						<th>Osoite</th>
						<th>Tila</th>
					</tr>
				</thead>
				<tbody>
				<?php foreach ( $states as $path => $state ) : ?>
					<tr>
						<td>
							<?php if ( 'ok' !== $state['state'] ) : ?>
								<input type="checkbox" name="kameli_sivut[]" value="<?php echo esc_attr( $path ); ?>" id="kameli-<?php echo esc_attr( sanitize_title( $path ) ); ?>" <?php checked( 'paivitys' !== $state['state'] ); ?> />
							<?php endif; ?>
						</td>
						<td><label for="kameli-<?php echo esc_attr( sanitize_title( $path ) ); ?>"><strong><?php echo esc_html( $state['title'] ); ?></strong></label>
							<?php if ( 'etusivu' === $path ) : ?><br /><span class="description">Asetetaan sivuston etusivuksi</span><?php endif; ?>
							<?php if ( 'blogi' === $path ) : ?><br /><span class="description">Asetetaan julkaisujen (blogin) sivuksi</span><?php endif; ?>
						</td>
						<td><code>/<?php echo esc_html( $path ); ?>/</code>
							<?php if ( $state['page'] ) : ?>
								<br /><a href="<?php echo esc_url( get_permalink( $state['page'] ) ); ?>" target="_blank">Näytä</a> · <a href="<?php echo esc_url( get_edit_post_link( $state['page'] ) ); ?>">Muokkaa</a>
							<?php endif; ?>
						</td>
						<td><?php echo $labels[ $state['state'] ]; // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped ?></td>
					</tr>
				<?php endforeach; ?>
				</tbody>
			</table>
			<?php if ( kameli_audio_setup_incomplete() ) : ?>
				<p class="description" style="max-width:720px;margin-top:1em"><strong>Uudemmat tekstit saatavilla</strong> tarkoittaa, että teeman päivityksessä sivun tekstejä on muutettu. Valitse sivu, jos haluat uudet tekstit – huomaa, että sivulle WordPressissä itse tehdyt muutokset korvautuvat (ne jäävät versiohistoriaan). Puuttuvat sivut luodaan. Valikko (Palvelut · Yritykset · Yksityiset · Artistit · Blogi · Ota yhteyttä) luodaan, jos sitä ei vielä ole.</p>
				<?php submit_button( 'Käytä teeman sivuja' ); ?>
			<?php else : ?>
				<p><strong>Kaikki teeman sivut ovat kunnossa.</strong></p>
			<?php endif; ?>
		</form>
	</div>
	<?php
}

/**
 * Tallentaa sivun nykyisen sisällön ennen korvaamista: versiohistoriaan, tai jos versiot
 * on poistettu käytöstä, luonnokseksi "Vanha: <otsikko>".
 *
 * @param int $id Sivun tunniste.
 */
function kameli_audio_keep_old_content( $id ) {
	$post = get_post( $id );
	if ( ! $post || '' === trim( $post->post_content ) ) {
		return;
	}
	if ( wp_revisions_enabled( $post ) ) {
		// WordPress tallentaa päivityksessä vain uuden version; tallennetaan nykyinen ensin.
		_wp_put_post_revision( $post );
		return;
	}
	wp_insert_post(
		array(
			'post_type'    => 'page',
			'post_status'  => 'draft',
			'post_title'   => 'Vanha: ' . $post->post_title,
			'post_content' => wp_slash( $post->post_content ),
		)
	);
}

/**
 * Valittujen sivujen luonti tai korvaus.
 */
function kameli_audio_handle_setup() {
	if ( ! current_user_can( 'manage_options' ) ) {
		wp_die( 'Ei oikeuksia.' );
	}
	check_admin_referer( 'kameli_audio_asennus' );

	$selected = isset( $_POST['kameli_sivut'] ) ? array_map( 'sanitize_text_field', wp_unslash( (array) $_POST['kameli_sivut'] ) ) : array();
	$pages    = kameli_audio_starter_pages();
	$selected = array_values( array_intersect( array_keys( $pages ), $selected ) );

	// Kategoriat ja blogi ensin, jotta sivujen sisältö osoittaa oikeisiin kategorioihin.
	kameli_audio_setup_blog();

	// Artikkelit-kategorian kuvaus päivittyi (ääni → tekniikka); päivitetään, jos sitä ei ole muokattu.
	$articles = get_term_by( 'slug', 'artikkelit', 'category' );
	if ( $articles && 'Vinkkejä tapahtumien äänen suunnitteluun ja kurkistuksia tuotantojen taakse.' === $articles->description ) {
		wp_update_term( $articles->term_id, 'category', array( 'description' => 'Vinkkejä tapahtumien tekniikan suunnitteluun ja kurkistuksia tuotantojen taakse.' ) );
	}

	// Ensin kaikki valitut sivut olemassa (vanhemmat ennen lapsia), sitten sisältö.
	$ids = array();
	foreach ( $selected as $path ) {
		$post = get_page_by_path( $path );
		if ( $post && 'trash' !== $post->post_status ) {
			$ids[ $path ] = $post->ID;
			continue;
		}
		$parent       = '.' !== dirname( $path ) ? get_page_by_path( dirname( $path ) ) : null;
		$ids[ $path ] = wp_insert_post(
			array(
				'post_type'   => 'page',
				'post_status' => 'publish',
				'post_title'  => $pages[ $path ][0],
				'post_name'   => basename( $path ),
				'post_parent' => $parent ? $parent->ID : 0,
			)
		);
	}
	foreach ( $ids as $path => $id ) {
		if ( ! $id || is_wp_error( $id ) ) {
			continue;
		}
		$update = array(
			'ID'          => $id,
			'post_status' => 'publish',
		);
		if ( '' !== $pages[ $path ][1] ) {
			kameli_audio_keep_old_content( $id );
			$update['post_content'] = wp_slash( kameli_audio_render_pattern_file( $pages[ $path ][1] ) );
		}
		wp_update_post( $update );
		update_post_meta( $id, '_kameli_sisalto_versio', KAMELI_AUDIO_CONTENT_VERSION );
		if ( 'etusivu' === $path ) {
			update_option( 'show_on_front', 'page' );
			update_option( 'page_on_front', $id );
		}
		if ( 'blogi' === $path ) {
			update_option( 'page_for_posts', $id );
		}
	}

	kameli_audio_create_navigation();

	wp_safe_redirect( admin_url( 'themes.php?page=kameli-audio-asennus&valmis=1' ) );
	exit;
}
add_action( 'admin_post_kameli_audio_asennus', 'kameli_audio_handle_setup' );
