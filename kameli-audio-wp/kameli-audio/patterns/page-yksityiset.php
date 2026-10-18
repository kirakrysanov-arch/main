<?php
/**
 * Title: Sivu: Yksityiset
 * Slug: kameli-audio/page-yksityiset
 * Categories: kameli-audio
 * Post Types: page
 * Block Types: core/post-content
 * Viewport Width: 1280
 *
 * @package kameli-audio
 */

// LUONNOS: tämän sivun tekstit ovat paikkamerkkejä, jotka korvataan lopullisilla.
echo kameli_audio_hero( 'Yksityiset', 'Yksityistilaisuudet & juhlat', 'Tee juhlastasi ikimuistoinen parhaalla mahdollisella äänentoistolla.', true );

echo kameli_audio_service_rows(
	'Mitä tarjoamme',
	array(
		array(
			'Häät',
			'Hääpäivänä jokaisen sanan pitää kuulua ja jokaisen kappaleen soida juuri oikein. Suunnittelemme äänentoiston vihkimisestä illan viimeiseen tanssiin, jotta te voitte keskittyä juhlimiseen.',
			array(
				'Vihkiminen ja puheet kuuluvat selkeästi myös takariveille',
				'Musiikki soi tasaisesti koko illan ajan',
				'Tekniikka asennetaan ja puretaan huomaamattomasti',
			)
		),
		array(
			'Merkkipäivät ja perhejuhlat',
			'Syntymäpäivät, valmistujaiset ja muut merkkipäivät ansaitsevat äänen, joka tukee tunnelmaa eikä varasta huomiota. Mitoitamme ratkaisun tilan ja vierasmäärän mukaan.',
			array(
				'Langattomat mikrofonit puheisiin ja ohjelmanumeroihin',
				'Taustamusiikki ja tanssimusiikki samasta järjestelmästä',
				'Selkeä hinta ja suunnitelma etukäteen',
			)
		),
		array(
			'Pienkonsertit ja yhdistysten tilaisuudet',
			'Kotikonsertti, kylätapahtuma tai yhdistyksen juhla – autamme pienemmissäkin tilaisuuksissa, jotta esiintyjät ja yleisö saavat parhaan mahdollisen kokemuksen.',
			array(
				'Äänentoisto esiintyjille ja juontajalle',
				'Ääniteknikko paikalla koko tilaisuuden ajan',
				'Neuvoa ja ideoita jo suunnitteluvaiheessa',
			)
		),
	)
);

echo kameli_audio_why_us();
echo kameli_audio_cta();
echo kameli_audio_contact_section();
