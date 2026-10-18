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

// Puhelinnumerot ja kuvat ovat paikkamerkkejä, jotka korvataan oikeilla.
echo kameli_audio_hero( 'Ota yhteyttä', 'Olemme täällä auttamassa audioprojektissasi', 'Odotamme yhteydenottoasi ja toteutamme audioprojektisi vuosien kokemuksella, ammattitaidolla ja intohimolla.' );

echo kameli_audio_section_open( 'valkoinen' )
	. kameli_audio_group( kameli_audio_paragraph( 'Tiimimme', '', 'kameli-eyebrow' ), 'kameli-osion-alku', 'wide' )
	. kameli_audio_columns(
		array(
			kameli_audio_person_card(
				'Juha Pöysä',
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
		),
		array(),
		'kameli-tiimi'
	)
	. kameli_audio_section_close();

echo kameli_audio_contact_section( 'Lähetä viesti' );
