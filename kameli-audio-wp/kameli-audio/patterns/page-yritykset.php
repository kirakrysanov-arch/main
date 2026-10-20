<?php
/**
 * Title: Sivu: Yritykset
 * Slug: kameli-audio/page-yritykset
 * Categories: kameli-audio
 * Post Types: page
 * Block Types: core/post-content
 * Viewport Width: 1280
 *
 * @package kameli-audio
 */

echo kameli_audio_hero( 'Yritykset', 'Yritystapahtumat & tapahtumajärjestäjät', 'Huolellisesti suunniteltu ääni ja valo luovat tunnelman, varmistavat sujuvuuden ja tekevät tapahtumastasi elämyksen.', true );

echo kameli_audio_service_rows(
	'Mitä tarjoamme',
	array(
		array(
			'Yritysjuhlat ja henkilöstötilaisuudet',
			'Olipa kyseessä satapäinen pikkujoulugaala, henkilöstöpäivän iltaohjelma tai intiimi juhlatilaisuus, varmistamme että saat juhlaasi kokonaisuuden, joka tuntuu huolitellulta ja ammattilaisen käsialalta — ilman, että sinun tarvitsee huolehtia teknisistä yksityiskohdista.',
			array(
				'Puheet, juonnot ja yllätysohjelmat kuuluvat selkeästi kaikkialle tilaan',
				'Musiikki soi halutulla alueella tasaisella volyymilla ja laadukkaasti',
				'Esiintyjät saavat ammattilaistason teknisen tuen, jotta show toimii ja yleisö viihtyy',
			)
		),
		array(
			'Lanseeraukset ja promootiotapahtumat',
			'Kun hetki on tärkeä, ääni ratkaisee. Varmistamme, että tuote- tai palvelulanseerauksesi saa ansaitsemansa huomion täydellisellä äänitekniikalla ja ammattimaisella toteutuksella. Huolehdimme puolestasi:',
			array(
				'Mikityksestä ja lavatekniikasta, jotta puheenvuorot, keskustelut ja demot kuuluvat jokaiseen nurkkaan',
				'Tarkkaan suunnitellusta äänimaisemasta, joka tukee brändiäsi ja hetken dramatiikkaa',
				'Tarvittavan tekniikan paikalle asennuksineen ja purkuineen',
			)
		),
		array(
			'Asiakas- ja sidosryhmätapahtumat',
			'Vakuuta asiakkaasi ja sidosryhmäsi. Asiakas- ja sidosryhmätapahtumissa ääni ei ole vain tekninen yksityiskohta — se on osa yrityksesi brändiä, luottamusta ja tunnelmaa. Huolehdimme, että:',
			array(
				'Puheenvuorot ja keskustelut kuuluvat selkeästi, oli kyseessä johtoryhmän esitys, asiantuntijapuheenvuoro tai fireside chat',
				'Tilaisuuden rytmi ja tunnelma pysyvät hallussa taustamusiikilla, spiikeillä ja äänimaisemalla',
				'Eri ohjelmanumeroiden tekninen toteutus (lavalle poistumiset, videoinsertit, panelistit, yllätysesiintyjät) toimii saumattomasti',
				'VIP-, media- tai kumppanivieraiden odotukset täyttyvät laadukkaalla ja luotettavalla äänituella',
			),
			'Lopputuloksena syntyy tilaisuus, joka tuntuu huolitellulta ja ammattimaiselta — ja jossa yrityksesi tärkeimmät yleisöt saavat kokea, että heistä välitetään.'
		),
	)
);

echo kameli_audio_why_us();
echo kameli_audio_cta();
echo kameli_audio_contact_section();
