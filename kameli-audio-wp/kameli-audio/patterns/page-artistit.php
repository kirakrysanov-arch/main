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
echo kameli_audio_hero( 'Artistit', 'Bändit & artistit', 'Live- ja studiotuotannot saman katon alla – demoista valmiisiin julkaisuihin.', true );

echo kameli_audio_service_rows(
	'Mitä tarjoamme',
	array(
		array(
			'Esituotanto ja sovitus',
			'Hyvä äänite alkaa ennen ensimmäistä otosta. Käymme biisit läpi kanssasi ja tuomme tuoreen näkökulman sovituksiin, sanoituksiin ja rakenteisiin.',
			array(
				'Biisien ja sovitusten läpikäynti ennen studiota',
				'Muusikon ja lauluntekijän näkökulma tuotantoon',
				'Laaditaan valmis tuotantosuunnitelma aikatauluineen',
			)
		),
		array(
			'Äänitys Oasis Studiolla',
			'Äänitämme Oasis Studiollamme Vantaan Hakkilassa. Rento ilmapiiri ja ammattitason välineet auttavat saamaan esityksestä parhaan irti.',
			array(
				'Bändit, soolosoittajat ja laulajat',
				'Pitkäsoitot, EP:t sekä singlejulkaisut',
				'Studiomestari, joka on itsekin esiintyjä',
			)
		),
		array(
			'Miksaus ja masterointi',
			'Viimeistelemme kappaleesi julkaisukuntoon – myös silloin, kun raidat on äänitetty muualla.',
			array(
				'Miksaus omista tai meillä äänitetyistä raidoista',
				'Masterointi suoratoistopalveluihin, radioon ja fyysisille formaateille',
				'Kommentointikierrokset, kunnes lopputulos on oikea',
			)
		),
		array(
			'Live-tuotannot',
			'Teemme myös live-tuotantoja. Autamme bändiä valmistautumaan keikoille ja kiertueille niin, että soundi on kohdallaan jo ensimmäisestä illasta lähtien.',
			array(
				'PA-treenit',
				'Kiertueiden valmistelu',
				'Soundien hakeminen keikkoja varten',
			)
		),
	)
);

echo kameli_audio_why_us();
echo kameli_audio_cta();
echo kameli_audio_contact_section();
