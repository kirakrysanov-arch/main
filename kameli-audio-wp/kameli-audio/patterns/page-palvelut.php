<?php
/**
 * Title: Sivu: Palvelut
 * Slug: kameli-audio/page-palvelut
 * Categories: kameli-audio
 * Post Types: page
 * Block Types: core/post-content
 * Viewport Width: 1280
 *
 * @package kameli-audio
 */

echo kameli_audio_hero( 'Palvelut', 'Palvelumme', 'Tarjoamme ammattitason tapahtumatekniikkaa ja studiopalveluita monipuolisiin tarpeisiin.' );

echo kameli_audio_section_open( 'valkoinen' )
	. kameli_audio_section_head(
		'Mitä teemme',
		'Tekniikkaratkaisut tapahtumiin ja tuotantoihin',
		'Olemme erikoistuneet äänentoistoon tapahtumiin ja äänituotantoon. Ääniteknikkomme hoitaa äänen kokouksissa, seminaareissa, kick-offeissa ja juhlissa alusta loppuun – tilan omilla laitteilla tai omalla kalustollamme. Artisteille teemme live- ja studiotuotantoja omalla Oasis Studiollamme. Ota yhteyttä, niin suunnitellaan tilaisuutesi ääni yhdessä!'
	)
	. kameli_audio_service_cards()
	. kameli_audio_section_close();

echo kameli_audio_why_us();
echo kameli_audio_case_studies_section();
echo kameli_audio_cta();
echo kameli_audio_contact_section();
