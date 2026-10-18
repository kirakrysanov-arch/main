<?php
/**
 * Kameli Audio -teeman toiminnot.
 *
 * @package kameli-audio
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'KAMELI_AUDIO_VERSION', wp_get_theme( get_template() )->get( 'Version' ) );

require_once get_template_directory() . '/inc/markup.php';
require_once get_template_directory() . '/inc/contact-form.php';
require_once get_template_directory() . '/inc/starter-content.php';
require_once get_template_directory() . '/inc/setup-page.php';

/**
 * Teeman perusasetukset.
 */
function kameli_audio_setup() {
	add_theme_support( 'wp-block-styles' );
	add_theme_support( 'editor-styles' );
	add_theme_support(
		'custom-logo',
		array(
			'height'      => 120,
			'width'       => 120,
			'flex-height' => true,
			'flex-width'  => true,
		)
	);
	add_editor_style( 'assets/css/kameli.css' );
}
add_action( 'after_setup_theme', 'kameli_audio_setup' );

/**
 * Tyylit sivustolle.
 */
function kameli_audio_enqueue() {
	wp_enqueue_style(
		'kameli-audio',
		get_theme_file_uri( 'assets/css/kameli.css' ),
		array(),
		KAMELI_AUDIO_VERSION
	);
}
add_action( 'wp_enqueue_scripts', 'kameli_audio_enqueue' );

/**
 * Oma kategoria lohkomalleille, jotta Kameli Audion osiot löytyvät editorista helposti.
 */
function kameli_audio_pattern_category() {
	register_block_pattern_category(
		'kameli-audio',
		array( 'label' => 'Kameli Audio' )
	);
}
add_action( 'init', 'kameli_audio_pattern_category', 9 );

/**
 * Jos logoa ei ole asetettu (Ulkoasu → Editori), ylätunniste näyttää teeman mukana tulevan logon.
 *
 * @param string $content Lohkon HTML.
 * @param array  $block   Lohko.
 */
function kameli_audio_default_logo( $content, $block ) {
	if ( '' !== trim( $content ) ) {
		return $content;
	}
	$width = isset( $block['attrs']['width'] ) ? (int) $block['attrs']['width'] : 64;
	return sprintf(
		'<div class="wp-block-site-logo"><a href="%s" class="custom-logo-link" rel="home"><img src="%s" class="custom-logo" alt="%s" width="%d" /></a></div>',
		esc_url( home_url( '/' ) ),
		kameli_audio_image( 'kameli-audio-logo.png' ),
		esc_attr( get_bloginfo( 'name' ) ),
		$width
	);
}
add_filter( 'render_block_core/site-logo', 'kameli_audio_default_logo', 10, 2 );

/**
 * Kortti-tyyli ryhmälohkolle.
 */
function kameli_audio_block_styles() {
	register_block_style(
		'core/group',
		array(
			'name'  => 'kortti',
			'label' => 'Kortti',
		)
	);
}
add_action( 'init', 'kameli_audio_block_styles' );
