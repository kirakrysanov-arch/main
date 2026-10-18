<?php
/**
 * Title: Sivu: Artistit
 * Slug: kameli-audio/page-artistit
 * Categories: kameli-audio
 * Post Types: page
 * Block Types: core/post-content
 * Viewport Width: 1280
 *
 * @package kameli-audio
 */

// LUONNOS: tämän sivun tekstit ovat paikkamerkkejä, jotka korvataan lopullisilla.
echo kameli_audio_hero( 'Bändit & artistit', 'Studiotallennus, miksaus ja masterointi – esituotannosta valmiiseen masteriin.', true );

echo kameli_audio_section_open( 'valkoinen' )
	. kameli_audio_service_block(
		'Esituotanto ja sovitus',
		'Hyvä äänite alkaa ennen ensimmäistä otosta. Käymme biisit läpi kanssasi ja tuomme tarvittaessa tuoreen näkökulman sovituksiin, sanoituksiin ja rakenteisiin.',
		array(
			'Biisien ja sovitusten läpikäynti ennen studiota',
			'Muusikon ja lauluntekijän näkökulma tuotantoon',
			'Selkeä suunnitelma äänityspäiville',
		)
	)
	. kameli_audio_section_close();

echo kameli_audio_section_open( 'vaalea' )
	. kameli_audio_service_block(
		'Äänitys Kameli Studiolla',
		'Äänitämme Kameli Studiolla Vantaan Hakkilassa. Rento ilmapiiri ja ammattitason välineet auttavat saamaan esityksestä parhaan irti.',
		array(
			'Bändit, soolosoittajat ja laulajat',
			'Kokonaiset levyt, EP:t ja yksittäiset singlet',
			'Ääniteknikko, joka on itsekin esiintyjä',
		)
	)
	. kameli_audio_section_close();

echo kameli_audio_section_open( 'valkoinen' )
	. kameli_audio_service_block(
		'Miksaus ja masterointi',
		'Viimeistelemme kappaleesi julkaisukuntoon – myös silloin, kun raidat on äänitetty muualla.',
		array(
			'Miksaus omista tai meillä äänitetyistä raidoista',
			'Masterointi suoratoistopalveluihin, radioon ja fyysisille formaateille',
			'Kommentointikierrokset, kunnes lopputulos on oikea',
		)
	)
	. kameli_audio_section_close();

echo kameli_audio_why_us();
echo kameli_audio_cta();
echo kameli_audio_contact_section( 'Ota yhteyttä', 'valkoinen' );
