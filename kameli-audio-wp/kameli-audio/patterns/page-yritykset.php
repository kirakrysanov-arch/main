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

echo kameli_audio_hero( 'Yritykset', 'Ääniteknikko tapahtumaan ja kokoukseen', 'Ääniteknikko paikalla koko tilaisuuden ajan – kokouksissa, seminaareissa, kick-offeissa ja yritysjuhlissa. Äänentoisto tapahtumiin Uudellamaalla ja sen ulkopuolella.', true );

echo kameli_audio_service_rows(
	'Mitä tarjoamme',
	array(
		array(
			'Ääniteknikko kokoukseen ja seminaariin',
			'Hotellien ja kokoustilojen laitteet ovat usein hyvät, mutta tilaisuuden aikana niitä ei hoida kukaan. Kun mikrofoni pätkii tai esityksen video ei soi, paikalle kiirehtii henkilökunta, jolla on samaan aikaan muutakin tehtävää. Ääniteknikkomme on paikalla alusta loppuun ja huolehtii, että:',
			array(
				'Langattomat mikrofonit, paristot ja taajuudet on tarkistettu ennen kuin vieraat saapuvat',
				'Esittäjien läppärit, videot ja etäpuhujat on testattu etukäteen',
				'Puhe kuuluu selvästi takariveille asti, ilman kiertoa',
				'Ongelmat korjataan heti – ohjelma ei pysähdy tekniikan takia',
			)
		),
		array(
			'Kick-offit ja henkilöstötilaisuudet',
			'Kick-offissa johto kertoo suunnan koko henkilöstölle. Silloin jokaisen puheenvuoron pitää kuulua ja ohjelman edetä aikataulussa – aamun avauksesta illan juhlaan.',
			array(
				'Puheenvuorot, paneelit ja kysymysosuudet langattomilla mikrofoneilla',
				'Musiikit, videot ja palkintojenjaot oikeaan aikaan',
				'Päivän ohjelma ja illan esiintyjät saman teknikon hoidossa',
				'Käytämme tilan omia laitteita tai tuomme tarvittaessa omamme',
			)
		),
		array(
			'Yritysjuhlat, lanseeraukset ja asiakastilaisuudet',
			'Pikkujouluissa, lanseerauksissa sekä asiakas- ja sidosryhmätapahtumissa ääni ei ole vain tekninen yksityiskohta – se on osa yrityksesi brändiä ja tunnelmaa. Huolehdimme, että:',
			array(
				'Puheet, juonnot ja keskustelut kuuluvat selkeästi kaikkialle tilaan',
				'Musiikki soi halutulla alueella tasaisella voimakkuudella',
				'Esiintyjät saavat ammattitason teknisen tuen',
				'Tekniikka asennetaan ja puretaan teidän aikataulunne mukaan',
			)
		),
		array(
			'Hotelleille ja tapahtumapaikoille',
			'Haluatteko tarjota asiakkaillenne ääniteknikon osana kokouspakettia? Toimimme tapahtumapaikkojen luottoteknikkona: teknikko käyttää talon laitteita, asiakkaanne saavat sujuvan tilaisuuden ja henkilökuntanne voi keskittyä omaan työhönsä.',
			array(
				'Yksi yhteyshenkilö teille ja asiakkaillenne',
				'Lisäkalusto isompiin tilaisuuksiin tarvittaessa',
				'Apu myös ruuhkaviikoille, kuten kick-off- ja pikkujoulukaudelle',
			)
		),
	)
);

echo kameli_audio_section_open( 'vaalea' )
	. kameli_audio_section_head( 'Usein kysyttyä', 'Ääniteknikko tapahtumaan – usein kysyttyä' )
	. kameli_audio_heading( 'Tarvitaanko ääniteknikkoa, jos tilassa on omat laitteet?', 3 )
	. kameli_audio_paragraph( 'Usein kyllä. Laitteet eivät ole ongelma, vaan se, ettei kukaan hoida niitä tilaisuuden aikana. Ääniteknikko testaa mikrofonit ja esitykset etukäteen, säätää äänen puhujien mukaan ja korjaa ongelmat heti.' )
	. kameli_audio_heading( 'Mitä äänitekniikkaa seminaariin tarvitaan?', 3 )
	. kameli_audio_paragraph( 'Tyypillisesti langattomat käsi- tai mikroportit puhujille, lisämikrofonit paneeliin ja kysymyksiin, kaiuttimet koko tilan kuuluvuuteen sekä ääni esittäjien tietokoneilta. Mitoitamme tekniikan tilan ja ohjelman mukaan.' )
	. kameli_audio_heading( 'Toimitteko myös Uudenmaan ulkopuolella?', 3 )
	. kameli_audio_paragraph( 'Kyllä. Toimimme pääasiassa Uudellamaalla, mutta tulemme mielellämme myös sen ulkopuolelle.' )
	. kameli_audio_heading( 'Tarjoatteko valotekniikkaa?', 3 )
	. kameli_audio_paragraph( 'Emme. Keskitymme ääneen: äänentoistoon tapahtumiin ja ääniteknikkoon paikan päällä.' )
	. kameli_audio_section_close();

echo kameli_audio_why_us();
echo kameli_audio_case_studies_section();
echo kameli_audio_cta( 'Tarvitsetteko ääniteknikon seuraavaan tilaisuuteen?', 'Kerro päivä, paikka ja ohjelma, niin palaamme asiaan.' );
echo kameli_audio_contact_section();
