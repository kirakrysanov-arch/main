<?php
/**
 * Title: Asiakastarina (pohja)
 * Slug: kameli-audio/asiakastarina
 * Categories: kameli-audio
 * Post Types: post
 * Block Types: core/post-content
 * Description: Pohja referenssille: faktalaatikko, lähtötilanne, ratkaisu, lopputulos ja asiakkaan palaute.
 *
 * @package kameli-audio
 */

$kameli_facts = array(
	'Asiakas'   => '[Yrityksen tai asiakkaan nimi]',
	'Tilaisuus' => '[Esim. henkilöstöjuhla, 250 henkeä]',
	'Paikka'    => '[Tapahtumapaikka, kaupunki]',
	'Palvelut'  => '[Esim. PA, mikitys, miksaus]',
);
$kameli_cols = array();
foreach ( $kameli_facts as $kameli_label => $kameli_value ) {
	$kameli_cols[] = kameli_audio_paragraph( esc_html( $kameli_label ), '', 'kameli-eyebrow' )
		. kameli_audio_paragraph( '<strong>' . esc_html( $kameli_value ) . '</strong>' );
}

echo kameli_audio_paragraph( '[Ingressi: yksi tai kaksi virkettä siitä, mikä tilaisuus oli ja mikä siinä onnistui. Tämä näkyy myös blogin listauksessa.]', 'lead' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
echo kameli_audio_group( kameli_audio_columns( $kameli_cols, array(), 'kameli-faktat__rivi' ), 'kameli-faktat' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
echo kameli_audio_heading( 'Lähtötilanne' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
echo kameli_audio_paragraph( '[Mitä asiakas tarvitsi? Millainen tila, ohjelma ja yleisö? Mitkä olivat haasteet – esimerkiksi aikataulu, akustiikka tai monta puhujaa?]' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
echo kameli_audio_heading( 'Ratkaisu' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
echo kameli_audio_paragraph( '[Miten suunnittelitte ja toteutitte äänen? Mitä kalustoa käytettiin ja miksi?]' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
echo kameli_audio_list( array( '[Esim. kaiutinjärjestelmä mitoitettuna tilaan]', '[Esim. langattomat mikrofonit puhujille]', '[Esim. ääniteknikko paikalla koko illan]' ) ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
echo kameli_audio_heading( 'Lopputulos' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
echo kameli_audio_paragraph( '[Mitä saavutettiin? Konkreettiset asiat toimivat parhaiten: kuinka moni kuuli, mikä sujui, mitä asiakas sanoi jälkikäteen.]' ); // phpcs:ignore WordPress.Security.EscapeOutput.OutputNotEscaped
?>

<!-- wp:quote {"className":"kameli-lainaus"} -->
<blockquote class="wp-block-quote kameli-lainaus"><!-- wp:paragraph -->
<p>[Asiakkaan palaute lainauksena.]</p>
<!-- /wp:paragraph --><cite>[Nimi, titteli, yritys]</cite></blockquote>
<!-- /wp:quote -->
