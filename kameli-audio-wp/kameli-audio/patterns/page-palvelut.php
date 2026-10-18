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

echo kameli_audio_hero( 'Palvelut', 'Palvelumme', 'Tarjoamme ammattitason audiopalveluita monipuolisiin tarpeisiin.' );

echo kameli_audio_section_open( 'valkoinen' )
	. kameli_audio_section_head(
		'Mitä teemme',
		'Ääniratkaisut tapahtumiin ja tuotantoihin',
		'Olemme erikoistuneet tarjoamaan huippuluokan ääniratkaisuja kaikenlaisiin tapahtumiin ja tuotantoihin. Olipa kyseessä yritystilaisuus, yksityisjuhla tai musiikkituotanto, meillä on osaaminen ja välineet tehdä siitä ikimuistoinen. Ota yhteyttä, niin suunnitellaan yhdessä täydellinen äänielämys!'
	)
	. kameli_audio_service_cards()
	. kameli_audio_section_close();

echo kameli_audio_why_us();
echo kameli_audio_case_studies_section();
echo kameli_audio_cta();
echo kameli_audio_contact_section();
