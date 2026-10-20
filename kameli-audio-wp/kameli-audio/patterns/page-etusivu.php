<?php
/**
 * Title: Sivu: Etusivu
 * Slug: kameli-audio/page-etusivu
 * Categories: kameli-audio
 * Post Types: page
 * Block Types: core/post-content
 * Viewport Width: 1280
 *
 * @package kameli-audio
 */

// LUONNOS: etusivun tekstit ovat paikkamerkkejä, jotka korvataan lopullisilla.
$buttons = "\n" . '<!-- wp:buttons -->' . "\n"
	. '<div class="wp-block-buttons"><!-- wp:button -->' . "\n"
	. '<div class="wp-block-button"><a class="wp-block-button__link wp-element-button" href="#yhteydenotto">Pyydä tarjous</a></div>' . "\n"
	. '<!-- /wp:button -->' . "\n\n"
	. '<!-- wp:button {"className":"is-style-outline"} -->' . "\n"
	. '<div class="wp-block-button is-style-outline"><a class="wp-block-button__link wp-element-button" href="' . kameli_audio_page_url( 'palvelut' ) . '">Tutustu palveluihin</a></div>' . "\n"
	. '<!-- /wp:button --></div>' . "\n"
	. '<!-- /wp:buttons -->' . "\n";

echo kameli_audio_section_open( 'hiili', '', 'kameli-hero kameli-hero--etusivu' )
	. kameli_audio_columns(
		array(
			kameli_audio_paragraph( 'Tapahtumatekniikka · Studio', '', 'kameli-eyebrow' )
				. kameli_audio_heading( 'Ääni, joka kantaa.', 1 )
				. kameli_audio_paragraph( 'Tapahtumien teknistä toteutusta sekä studiotuotantoa Vantaan Hakkilasta – yrityksille, yksityisille ja artisteille.', 'lead', 'kameli-alaotsikko' )
				. $buttons,
			kameli_audio_image_block( 'kameli-audio-logo.png', '100%', 'Kameli Audio', 'kameli-hero__logo' ),
		),
		array( '60%', '40%' ),
		'kameli-hero__rivi'
	)
	. kameli_audio_section_close();

echo kameli_audio_section_open( 'valkoinen' )
	. kameli_audio_section_head(
		'Mitä teemme',
		'Tapahtumatekniikkaa ja studiotuotantoa saman katon alta',
		'Hoidamme tapahtumasi tekniikan suunnittelusta purkuun ja viemme musiikkisi esituotannosta valmiiksi masteriksi. Saat kokeneen tekijän, joka kuuntelee sekä sinua että tilaa.'
	)
	. kameli_audio_service_cards()
	. kameli_audio_section_close();

echo kameli_audio_why_us();

echo kameli_audio_section_open( 'valkoinen' )
	. kameli_audio_columns(
		array(
			kameli_audio_paragraph( 'Keitä olemme', '', 'kameli-eyebrow' )
				. kameli_audio_heading( 'Juha ja Sakari', 2, 'kameli-osio-otsikko' ),
			kameli_audio_paragraph( 'Juha vastaa tapahtumatekniikasta ja studiotuotannoista, Sakari hallinnosta ja tilauksista – ja tuo studioon muusikon ja lauluntekijän näkökulman.', 'lead' )
				. kameli_audio_paragraph( '<a class="kameli-lue-lisaa" href="' . kameli_audio_page_url( 'ota-yhteytta' ) . '">Tutustu tiimiin</a>' ),
		),
		array( '38%', '62%' )
	)
	. kameli_audio_section_close();

echo kameli_audio_case_studies_section();
echo kameli_audio_cta();
echo kameli_audio_contact_section();
