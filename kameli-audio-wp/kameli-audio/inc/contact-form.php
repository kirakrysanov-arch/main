<?php
/**
 * Yhteydenottolomake: lyhytkoodi [kameli_yhteydenotto], lähetyksen käsittely,
 * viestien tallennus hallintapaneeliin (Yhteydenotot) ja sähköposti-ilmoitus.
 *
 * Viestit tallennetaan aina WordPressiin, joten ne eivät katoa, vaikka
 * palvelimen sähköpostin lähetys ei toimisi.
 *
 * @package kameli-audio
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const KAMELI_AUDIO_MESSAGE_TYPE = 'kameli_viesti';

/**
 * Viestien tallennus omana sisältötyyppinään (näkyy vain hallinnassa).
 */
function kameli_audio_register_message_type() {
	register_post_type(
		KAMELI_AUDIO_MESSAGE_TYPE,
		array(
			'labels'          => array(
				'name'          => 'Yhteydenotot',
				'singular_name' => 'Yhteydenotto',
				'all_items'     => 'Kaikki yhteydenotot',
				'edit_item'     => 'Yhteydenotto',
				'search_items'  => 'Hae yhteydenotoista',
				'not_found'     => 'Ei yhteydenottoja.',
			),
			'public'          => false,
			'show_ui'         => true,
			'show_in_menu'    => true,
			'menu_position'   => 25,
			'menu_icon'       => 'dashicons-email-alt',
			'supports'        => array( 'title', 'editor' ),
			'capability_type' => 'post',
			'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
			'map_meta_cap'    => true,
		)
	);
}
add_action( 'init', 'kameli_audio_register_message_type' );

/**
 * Sähköpostiosoite, johon ilmoitukset lähetetään.
 */
function kameli_audio_contact_recipient() {
	$email = get_option( 'kameli_audio_contact_email' );
	return is_email( $email ) ? $email : get_option( 'admin_email' );
}

/**
 * Asetus kohdassa Asetukset → Yleiset: yhteydenottojen vastaanottaja.
 */
function kameli_audio_register_settings() {
	register_setting(
		'general',
		'kameli_audio_contact_email',
		array(
			'type'              => 'string',
			'sanitize_callback' => 'sanitize_email',
			'default'           => '',
		)
	);
	add_settings_field(
		'kameli_audio_contact_email',
		'<label for="kameli_audio_contact_email">Yhteydenottojen vastaanottaja</label>',
		function () {
			printf(
				'<input type="email" id="kameli_audio_contact_email" name="kameli_audio_contact_email" value="%s" class="regular-text" placeholder="%s" /><p class="description">Yhteydenottolomakkeen viestit lähetetään tähän osoitteeseen. Jos kenttä on tyhjä, käytetään ylläpitäjän sähköpostia.</p>',
				esc_attr( get_option( 'kameli_audio_contact_email' ) ),
				esc_attr( get_option( 'admin_email' ) )
			);
		},
		'general'
	);
}
add_action( 'admin_init', 'kameli_audio_register_settings' );

/**
 * Nykyisen sivun osoite (myös blogin listaus- ja kategoriasivuilla), johon lomakkeen jälkeen palataan.
 */
function kameli_audio_current_url() {
	global $wp;
	if ( is_singular() ) {
		return get_permalink();
	}
	return home_url( $wp && $wp->request ? trailingslashit( $wp->request ) : '/' );
}

/**
 * Lomakkeen HTML.
 */
function kameli_audio_contact_form_shortcode() {
	$status = isset( $_GET['yhteydenotto'] ) ? sanitize_key( wp_unslash( $_GET['yhteydenotto'] ) ) : ''; // phpcs:ignore WordPress.Security.NonceVerification.Recommended

	ob_start();

	if ( 'kiitos' === $status ) {
		echo '<div class="kameli-lomake-ilmoitus kameli-lomake-ilmoitus--ok" role="status"><strong>Kiitos viestistäsi!</strong> Palaamme asiaan mahdollisimman pian.</div>';
	} elseif ( 'virhe' === $status ) {
		echo '<div class="kameli-lomake-ilmoitus kameli-lomake-ilmoitus--virhe" role="alert">Viestin lähetys ei onnistunut. Tarkista, että nimi, sähköposti ja viesti on täytetty, ja yritä uudelleen.</div>';
	}

	$privacy_url = get_privacy_policy_url();
	?>
	<form class="kameli-lomake" method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
		<input type="hidden" name="action" value="kameli_yhteydenotto" />
		<input type="hidden" name="kameli_paluu" value="<?php echo esc_url( kameli_audio_current_url() ); ?>" />
		<?php wp_nonce_field( 'kameli_yhteydenotto', 'kameli_nonce' ); ?>

		<p class="kameli-lomake__kentta">
			<label for="kameli-nimi">Nimi <span aria-hidden="true">*</span></label>
			<input id="kameli-nimi" type="text" name="kameli_nimi" placeholder="Nimesi" autocomplete="name" required maxlength="200" />
		</p>
		<p class="kameli-lomake__kentta">
			<label for="kameli-sahkoposti">Sähköposti <span aria-hidden="true">*</span></label>
			<input id="kameli-sahkoposti" type="email" name="kameli_sahkoposti" placeholder="nimi@esimerkki.fi" autocomplete="email" required maxlength="200" />
		</p>
		<p class="kameli-lomake__kentta">
			<label for="kameli-puhelin">Puhelinnumero</label>
			<input id="kameli-puhelin" type="tel" name="kameli_puhelin" placeholder="+358 40 123 4567" autocomplete="tel" maxlength="50" />
		</p>
		<p class="kameli-lomake__kentta">
			<label for="kameli-viesti">Viesti <span aria-hidden="true">*</span></label>
			<textarea id="kameli-viesti" name="kameli_viesti" rows="6" placeholder="Kerro projektistasi tai tapahtumastasi…" required maxlength="5000"></textarea>
		</p>
		<p class="kameli-lomake__ansa" aria-hidden="true">
			<label for="kameli-verkkosivu">Jätä tämä kenttä tyhjäksi</label>
			<input id="kameli-verkkosivu" type="text" name="kameli_verkkosivu" tabindex="-1" autocomplete="off" />
		</p>
		<p class="kameli-lomake__huomautus">
			Käytämme tietojasi vain yhteydenottoosi vastaamiseen.
			<?php if ( $privacy_url ) : ?>
				<a href="<?php echo esc_url( $privacy_url ); ?>">Tietosuojaseloste</a>
			<?php endif; ?>
		</p>
		<p>
			<button type="submit" class="wp-element-button kameli-lomake__laheta">Lähetä viesti</button>
		</p>
	</form>
	<?php
	return ob_get_clean();
}
add_shortcode( 'kameli_yhteydenotto', 'kameli_audio_contact_form_shortcode' );

/**
 * Lomakkeen lähetyksen käsittely.
 */
function kameli_audio_handle_contact() {
	$back = isset( $_POST['kameli_paluu'] ) ? esc_url_raw( wp_unslash( $_POST['kameli_paluu'] ) ) : '';
	$back = wp_validate_redirect( $back, home_url( '/' ) );

	$redirect = function ( $status ) use ( $back ) {
		wp_safe_redirect( add_query_arg( 'yhteydenotto', $status, $back ) . '#yhteydenotto' );
		exit;
	};

	if ( ! isset( $_POST['kameli_nonce'] ) || ! wp_verify_nonce( sanitize_key( wp_unslash( $_POST['kameli_nonce'] ) ), 'kameli_yhteydenotto' ) ) {
		$redirect( 'virhe' );
	}

	// Roskapostiansa: ihminen ei näe kenttää, botti täyttää sen.
	if ( ! empty( $_POST['kameli_verkkosivu'] ) ) {
		$redirect( 'kiitos' );
	}

	$name    = isset( $_POST['kameli_nimi'] ) ? sanitize_text_field( wp_unslash( $_POST['kameli_nimi'] ) ) : '';
	$email   = isset( $_POST['kameli_sahkoposti'] ) ? sanitize_email( wp_unslash( $_POST['kameli_sahkoposti'] ) ) : '';
	$phone   = isset( $_POST['kameli_puhelin'] ) ? sanitize_text_field( wp_unslash( $_POST['kameli_puhelin'] ) ) : '';
	$message = isset( $_POST['kameli_viesti'] ) ? sanitize_textarea_field( wp_unslash( $_POST['kameli_viesti'] ) ) : '';

	if ( '' === $name || ! is_email( $email ) || '' === $message ) {
		$redirect( 'virhe' );
	}

	$name    = mb_substr( $name, 0, 200 );
	$phone   = mb_substr( $phone, 0, 50 );
	$message = mb_substr( $message, 0, 5000 );

	$body = sprintf(
		"Nimi: %s\nSähköposti: %s\nPuhelin: %s\n\n%s",
		$name,
		$email,
		'' !== $phone ? $phone : '–',
		$message
	);

	wp_insert_post(
		array(
			'post_type'    => KAMELI_AUDIO_MESSAGE_TYPE,
			'post_status'  => 'private',
			'post_title'   => $name . ' (' . $email . ')',
			'post_content' => $body,
		)
	);

	wp_mail(
		kameli_audio_contact_recipient(),
		'Uusi yhteydenotto: ' . $name,
		$body . "\n\n—\nLähetetty sivulta " . $back,
		array( 'Reply-To: ' . $email )
	);

	$redirect( 'kiitos' );
}
add_action( 'admin_post_nopriv_kameli_yhteydenotto', 'kameli_audio_handle_contact' );
add_action( 'admin_post_kameli_yhteydenotto', 'kameli_audio_handle_contact' );

/**
 * Lyhytkoodilohko sivupohjissa (esim. blogin yhteydenotto-osio): WordPress ajaa lyhytkoodit
 * automaattisesti vain sivun sisällössä, joten ajetaan ne myös tässä.
 *
 * @param string $content Lohkon HTML.
 */
function kameli_audio_render_shortcode_block( $content ) {
	return false !== strpos( $content, '[kameli_yhteydenotto' ) ? do_shortcode( $content ) : $content;
}
add_filter( 'render_block_core/shortcode', 'kameli_audio_render_shortcode_block' );
