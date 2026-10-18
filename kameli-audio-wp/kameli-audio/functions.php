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
 * Kortti-tyyli ryhmälohkolle: ohut musta reunus ja pyöristetyt kulmat.
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
