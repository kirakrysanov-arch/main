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

echo kameli_audio_hero( 'Palvelumme', 'Tarjoamme ammattitason audiopalveluita monipuolisiin tarpeisiin' );

echo kameli_audio_section_open( 'valkoinen' )
	. kameli_audio_paragraph( 'Olemme erikoistuneet tarjoamaan huippuluokan ääniratkaisuja kaikenlaisiin tapahtumiin ja tuotantoihin. Olipa kyseessä yritystilaisuus, yksityisjuhla tai musiikkituotanto, meillä on osaaminen ja välineet tehdä siitä ikimuistoinen. Ota yhteyttä, niin suunnitellaan yhdessä täydellinen äänielämys!', 'center' )
	. kameli_audio_section_close();

echo kameli_audio_section_open( 'vaalea' )
	. kameli_audio_service_cards()
	. kameli_audio_section_close();

echo kameli_audio_cta();
echo kameli_audio_contact_section();
