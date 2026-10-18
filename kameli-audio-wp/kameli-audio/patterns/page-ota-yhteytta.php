<?php
/**
 * Title: Sivu: Ota yhteyttä
 * Slug: kameli-audio/page-ota-yhteytta
 * Categories: kameli-audio
 * Post Types: page
 * Block Types: core/post-content
 * Viewport Width: 1280
 *
 * @package kameli-audio
 */

// Puhelinnumerot ja sähköpostit ovat paikkamerkkejä, jotka korvataan oikeilla.
echo kameli_audio_hero( 'Ota yhteyttä', 'Olemme täällä auttamassa audioprojektissasi' );

echo kameli_audio_section_open( 'vaalea' )
	. kameli_audio_paragraph( 'Odotamme yhteydenottoasi ja toteutamme audioprojektisi vuosien kokemuksella, ammattitaidolla ja intohimolla.', 'center' )
	. kameli_audio_heading( 'Tiimimme', 2, true )
	. kameli_audio_columns(
		array(
			kameli_audio_person_card(
				'Juha Pöyry',
				'Vastaava teknikko, studiomestari',
				'Vastaan tapahtumatekniikan toteutuksesta sekä kaluston ylläpidosta. Studion puolella teen äänitetuotannon kaikki vaiheet esituotannosta miksaukseen ja masterointiin.',
				'+358 XX XXX XXXX',
				'juha@kameliaudio.fi'
			),
			kameli_audio_person_card(
				'Sakari Juntura',
				'Hallinto ja tilaukset',
				'Vastaan yrityksen hallinnosta, kuten rahoituksesta, talousasioista ja hankkeiden koordinoinnista. Olen toisinaan Juhan mukana keikoilla ja tapahtumissa. Olen säveltänyt ja kirjoittanut omaa tuotantoa pitkään, ja tarjoan mielelläni biiseille tuoretta näkökulmaa studiossa.',
				'+358 XX XXX XXXX',
				'sakari@kameliaudio.fi'
			),
		)
	)
	. kameli_audio_section_close();

echo kameli_audio_contact_section( 'Lähetä viesti', 'valkoinen' );

echo kameli_audio_section_open( 'vaalea' )
	. '<!-- wp:group {"className":"is-style-kortti kameli-studio","layout":{"type":"constrained","contentSize":"320px"}} -->' . "\n"
	. '<div class="wp-block-group is-style-kortti kameli-studio">'
	. kameli_audio_image_block( 'ikoni-sijainti.svg', '36px', '', 'kameli-keskitetty' )
	. kameli_audio_heading( 'Käy studiolla', 3, true )
	. kameli_audio_paragraph( '<a href="https://www.google.com/maps/search/?api=1&amp;query=Hakkila%2C%20Vantaa">Kameli Studio, Hakkila, Vantaa</a>', 'center harmaa' )
	. '</div>' . "\n" . '<!-- /wp:group -->'
	. kameli_audio_section_close();
