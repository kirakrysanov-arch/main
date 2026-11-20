# Four SEO articles (Finnish). Block-markup builder + content.
# Format per post: slug, title, excerpt, featured media id, body (list of blocks: ('p', text) / ('h2', text) / ('ul', [items]) / ('ol', [items]))

YRITYKSET = 'https://www.kameliaudio.fi/palvelut/yritykset/'
YHTEYS = 'https://www.kameliaudio.fi/ota-yhteytta/'
KOKOUS = 'https://www.kameliaudio.fi/aanentoisto-kokouksiin-ja-konferensseihin/'

CTA = ('p', f'<strong>Tarvitsetteko ääniteknikon seuraavaan tilaisuuteen?</strong> Kameli Audio hoitaa äänentoiston tapahtumiin Uudellamaalla ja sen ulkopuolella. Lue lisää <a href="{YRITYKSET}">ääniteknikosta yritystapahtumiin</a> tai <a href="{YHTEYS}">ota yhteyttä</a> – kerro päivä, paikka ja ohjelma, niin palaamme asiaan.')

POSTS = [
    dict(
        slug='aaniteknikko-tapahtumaan',
        title='Ääniteknikko tapahtumaan – milloin sitä tarvitaan ja mitä hän tekee?',
        excerpt='Milloin tapahtumaan kannattaa varata ääniteknikko, mitä teknikko tekee ennen tilaisuutta ja sen aikana, ja miten hänet tilataan? Käytännön opas tapahtuman järjestäjälle.',
        media=290,
        body=[
            ('p', 'Moni tapahtuman järjestäjä miettii samaa: tarvitaanko ääniteknikkoa, jos tilassa on jo kaiuttimet ja mikrofonit? Vastaus riippuu tilaisuudesta – mutta useammin kuin uskoisi, kyllä. Laitteet eivät tee tilaisuudesta onnistunutta, vaan se, että joku hoitaa niitä koko ajan.'),
            ('p', 'Tässä artikkelissa käymme läpi, milloin <strong>ääniteknikko tapahtumaan</strong> kannattaa varata, mitä teknikko oikeastaan tekee ja miten tilaus etenee.'),
            ('h2', 'Milloin ääniteknikko kannattaa varata?'),
            ('p', 'Nyrkkisääntö: jos tilaisuudessa on enemmän kuin yksi puhuja, yleisöä on yli muutama kymmenen tai ohjelmassa on videoita, musiikkia tai esiintyjiä, teknikosta on hyötyä. Erityisesti näissä tilanteissa:'),
            ('ul', [
                'Kick-offit ja henkilöstöpäivät, joissa johto puhuu koko henkilöstölle',
                'Seminaarit ja konferenssit, joissa on useita puhujia, paneeleja tai kysymysosuuksia',
                'Tilaisuudet, joissa on etäpuhujia tai jotka striimataan',
                'Yritysjuhlat ja pikkujoulut, joissa on puheita, juontaja ja esiintyjiä',
                'Lanseeraukset ja asiakastilaisuudet, joissa kaiken pitää toimia ensimmäisellä kerralla',
            ]),
            ('h2', 'Mitä ääniteknikko tekee ennen tilaisuutta?'),
            ('p', 'Suurin osa teknikon työstä tapahtuu ennen kuin ensimmäinen vieras saapuu. Hyvin valmisteltu tilaisuus näyttää yleisölle siltä, ettei tekniikkaa ole ollenkaan.'),
            ('ul', [
                'Käy ohjelman läpi järjestäjän kanssa: puhujat, paneelit, videot, musiikit ja aikataulu',
                'Tarkistaa tilan laitteet ja tuo tarvittaessa lisää kalustoa',
                'Vaihtaa paristot ja tarkistaa langattomien mikrofonien taajuudet',
                'Testaa jokaisen esittäjän tietokoneen äänen ja kuvan',
                'Säätää äänen niin, että puhe kuuluu takariveille asti ilman kiertoa',
            ]),
            ('h2', 'Entä tilaisuuden aikana?'),
            ('p', 'Tilaisuuden aikana teknikko seuraa ohjelmaa ja reagoi heti. Hän avaa oikean mikrofonin oikealla hetkellä, säätää äänen jokaisen puhujan mukaan, käynnistää videot ja musiikit sekä korjaa ongelmat ennen kuin yleisö ehtii huomata niitä.'),
            ('p', 'Ilman teknikkoa ongelmia hoitaa yleensä se, joka sattuu olemaan lähimpänä – usein hotellin tai tilan henkilökunta, jolla on samaan aikaan muutakin tehtävää. Silloin ohjelma pysähtyy, ja puhuja jää odottamaan lavalle.'),
            ('h2', 'Tarvitaanko omat laitteet?'),
            ('p', 'Ei välttämättä. Monissa hotelleissa ja kokoustiloissa on hyvät äänilaitteet, ja ääniteknikko voi käyttää niitä. Jos tilan kalusto ei riitä tilaisuuden kokoon tai ohjelmaan, teknikko tuo puuttuvat laitteet mukanaan. Tämä kannattaa selvittää jo tarjousvaiheessa.'),
            ('h2', 'Näin tilaat ääniteknikon tapahtumaan'),
            ('ol', [
                'Kerro päivämäärä, paikka, arvioitu osallistujamäärä ja ohjelman pääkohdat.',
                'Teknikko selvittää tilan laitteet ja tekee tarjouksen.',
                'Ennen tilaisuutta käydään ohjelma ja aikataulu läpi.',
                'Tilaisuuspäivänä teknikko on paikalla hyvissä ajoin ennen vieraita ja lähtee vasta, kun kaikki on valmista.',
            ]),
            ('p', 'Mitä aiemmin teknikko on mukana, sitä helpompaa kaikki on – erityisesti kiireisinä kausina, kuten tammi–helmikuun kick-off-kaudella ja pikkujouluaikaan.'),
            CTA,
        ],
    ),
    dict(
        slug='kick-offin-aanentoisto',
        title='Kick-offin äänentoisto: 7 asiaa, jotka kannattaa varmistaa etukäteen',
        excerpt='Kick-offissa johto kertoo suunnan koko henkilöstölle – silloin jokaisen puheenvuoron pitää kuulua. Seitsemän käytännön vinkkiä kick-offin äänentoistoon.',
        media=303,
        body=[
            ('p', 'Kick-off on vuoden tärkeimpiä sisäisiä tilaisuuksia. Johto kertoo suunnan, tiimit palkitaan ja illalla juhlitaan. Silti äänentoisto jää usein viime hetkeen – ja juuri ääni on se, minkä jokainen osallistuja huomaa, jos se ei toimi.'),
            ('p', 'Olemme olleet mukana monissa yritysten kick-offeissa hotelleissa ja tapahtumapaikoissa. Nämä seitsemän asiaa ratkaisevat useimmiten, onnistuuko <strong>äänentoisto tapahtumassa</strong>.'),
            ('h2', '1. Kuka hoitaa äänen tilaisuuden aikana?'),
            ('p', 'Tärkein kysymys ei ole, mitä laitteita tilassa on, vaan kuka käyttää niitä. Jos vastaus on "hotellin henkilökunta" tai "joku meistä", varaudu siihen, että ongelmatilanteessa ohjelma pysähtyy. Ääniteknikko koko päiväksi on pieni osa kick-offin budjettia.'),
            ('h2', '2. Langattomat mikrofonit ja paristot'),
            ('p', 'Langaton mikrofoni, joka sammuu kesken toimitusjohtajan puheenvuoron, on klassikko. Paristot vaihdetaan ennen tilaisuutta, varamikrofoni on valmiina ja taajuudet on tarkistettu, jotta mikrofonit eivät häiritse toisiaan.'),
            ('h2', '3. Esitysten ääni'),
            ('p', 'Video soi puhujan läppäristä, mutta ei kaiuttimista. Jokaisen esittäjän kone kannattaa testata etukäteen – myös se, joka tuodaan paikalle viisi minuuttia ennen omaa vuoroa.'),
            ('h2', '4. Kuuluvuus takariveille'),
            ('p', 'Isossa salissa ääni ei kanna takariveille pelkillä kattokaiuttimilla. Kaiuttimet sijoitetaan niin, että puhe kuuluu kaikkialle ilman, että eturivissä on liian kovaa.'),
            ('h2', '5. Paneelit ja kysymysosuudet'),
            ('p', 'Paneelikeskustelussa jokaisella puhujalla on oma mikrofoni, ja yleisökysymyksiin tarvitaan kiertävä mikrofoni. Muuten kysymykset eivät kuulu muille – eikä tallenteelle.'),
            ('h2', '6. Musiikit ja siirtymät'),
            ('p', 'Sisääntulomusiikit, palkintojenjaot ja videoinsertit tekevät kick-offista tilaisuuden eikä pelkkää kokousta. Ne toimivat, kun joku seuraa käsikirjoitusta ja käynnistää jokaisen oikealla hetkellä.'),
            ('h2', '7. Päivästä iltaan'),
            ('p', 'Moni kick-off jatkuu illallisella ja juhlalla. Kun sama teknikko hoitaa sekä päivän ohjelman että illan puheet ja esiintyjät, siirtymä sujuu ilman uusia asennuksia ja yllätyksiä.'),
            ('h2', 'Muistilista kick-offin järjestäjälle'),
            ('ul', [
                'Ääniteknikko paikalla koko tilaisuuden ajan',
                'Ohjelma ja puhujalista teknikolle viimeistään viikkoa ennen',
                'Esitykset ja videot yhdellä koneella tai testattuna etukäteen',
                'Varamikrofoni ja kiertävä mikrofoni kysymyksiin',
                'Aikaa äänitestille ennen kuin vieraat saapuvat',
            ]),
            ('p', f'Lue myös: <a href="{KOKOUS}">Äänentoisto kokouksiin ja konferensseihin</a>.'),
            CTA,
        ],
    ),
    dict(
        slug='aanitekniikka-seminaariin',
        title='Äänitekniikka seminaariin – tarkistuslista järjestäjälle',
        excerpt='Mitä äänitekniikkaa seminaariin tarvitaan? Tarkistuslista mikrofoneista, kaiuttimista, esitysten äänestä, etäpuhujista ja tallennuksesta.',
        media=476,
        body=[
            ('p', 'Seminaarissa sisältö on pääosassa – ja sisältö välittyy äänen kautta. Jos osallistujat eivät kuule puhujaa, paraskaan esitys ei auta. Tämä tarkistuslista auttaa selvittämään, mitä <strong>äänitekniikkaa seminaariin</strong> tarvitaan ja mitä kannattaa kysyä tilan tarjoajalta.'),
            ('h2', 'Mikrofonit'),
            ('ul', [
                'Montako puhujaa on lavalla yhtä aikaa?',
                'Käsimikrofoni vai mikroportti? Mikroportti jättää kädet vapaaksi, käsimikrofoni on varmempi vaihtuvilla puhujilla.',
                'Paneeliin oma mikrofoni jokaiselle osallistujalle',
                'Kiertävä mikrofoni yleisökysymyksiin',
                'Varamikrofoni ja varaparistot',
            ]),
            ('h2', 'Kaiuttimet ja kuuluvuus'),
            ('p', 'Pienessä kokoushuoneessa tilan omat kaiuttimet riittävät usein. Isommassa salissa ääni pitää jakaa niin, että se kuuluu tasaisesti koko tilaan. Kysy tilan tarjoajalta, kattavatko kaiuttimet koko salin vai vain etuosan.'),
            ('h2', 'Esitysten ääni'),
            ('ul', [
                'Tuleeko esitysten ääni (videot, äänitteet) kaiuttimista?',
                'Millä liitännällä puhujien koneet kytketään?',
                'Kuka testaa koneet ennen tilaisuutta?',
            ]),
            ('h2', 'Etäpuhujat ja striimaus'),
            ('p', 'Hybridiseminaarissa sama ääni kulkee sekä salin kaiuttimiin että verkkoyleisölle. Etäpuhujan ääni pitää saada saliin, ja salin ääni etäpuhujalle – ilman kaikua. Tämä on tilanne, jossa ääniteknikko on lähes välttämätön.'),
            ('h2', 'Tallennus'),
            ('p', 'Jos seminaari tallennetaan, ääni kannattaa ottaa suoraan äänipöydästä eikä kameran mikrofonista. Silloin tallenteen puhe on selkeää.'),
            ('h2', 'Kuka hoitaa tekniikan seminaarin aikana?'),
            ('p', 'Tarkistuslistan tärkein kohta on viimeinen: kuka on paikalla, jos jokin ei toimi? Monessa tilassa laitteet ovat hyvät, mutta tilaisuuden aikana niitä ei hoida kukaan. Ääniteknikko testaa kaiken etukäteen, avaa mikrofonit oikeaan aikaan ja korjaa ongelmat heti.'),
            ('h2', 'Seminaarin äänitekniikka – lyhyt muistilista'),
            ('ol', [
                'Puhujien ja paneelin mikrofonit',
                'Kiertävä mikrofoni kysymyksiin',
                'Kuuluvuus koko saliin',
                'Esitysten ääni testattuna',
                'Etäpuhujat ja striimaus, jos tarpeen',
                'Ääniteknikko paikalla koko tilaisuuden ajan',
            ]),
            CTA,
        ],
    ),
    dict(
        slug='aaniteknikko-kokoukseen-hotellissa',
        title='Ääniteknikko kokoukseen hotellissa – kuka hoitaa äänen, kun mikrofoni pettää?',
        excerpt='Hotellin kokoustilan laitteet ovat usein hyvät, mutta tilaisuuden aikana niitä ei hoida kukaan. Miksi ääniteknikko kokoukseen kannattaa – järjestäjän ja hotellin näkökulmasta.',
        media=51,
        body=[
            ('p', 'Tilanne on tuttu monesta hotellin kokoustilasta: sali on hieno, laitteet modernit ja kahvit valmiina. Sitten ensimmäinen puhuja nousee lavalle, mikrofoni ei toimi, ja paikalle kiirehtii hotellin työntekijä, joka samaan aikaan vastaa myös tarjoilusta ja seuraavasta varauksesta.'),
            ('p', 'Kyse ei ole huonosta palvelusta. Hotellin henkilökunnan työ on majoitus, ravintola ja asiakaspalvelu – ei äänitekniikka. Siksi <strong>ääniteknikko kokoukseen</strong> on usein se puuttuva palanen.'),
            ('h2', 'Järjestäjän näkökulma'),
            ('p', 'Kokouksen järjestäjälle tärkeintä on, että ohjelma etenee ja jokainen osallistuja kuulee. Kun teknikko on paikalla:'),
            ('ul', [
                'mikrofonit ja esitykset on testattu ennen kuin vieraat saapuvat',
                'puhujien vaihdot sujuvat ilman taukoja',
                'ongelmat korjataan heti, eikä järjestäjän tarvitse juosta hakemaan apua',
                'järjestäjä voi keskittyä vieraisiin ja ohjelmaan',
            ]),
            ('h2', 'Hotellin ja tapahtumapaikan näkökulma'),
            ('p', 'Tapahtumapaikalle ääniteknikko on tapa parantaa asiakaskokemusta ilman omaa teknistä henkilökuntaa. Teknikon voi tarjota asiakkaille lisäpalveluna kokouspaketin yhteydessä:'),
            ('ul', [
                'henkilökunta voi keskittyä omaan työhönsä',
                'asiakkaat saavat sujuvan tilaisuuden ja antavat parempaa palautetta',
                'talon omat laitteet ovat ammattilaisen käytössä',
                'isompiin tilaisuuksiin saadaan tarvittaessa lisäkalustoa',
            ]),
            ('h2', 'Milloin teknikko kannattaa varata kokoukseen?'),
            ('p', 'Pieneen palaveriin teknikkoa ei tarvita. Mutta kun osallistujia on kymmeniä, puhujia on useita, ohjelmassa on videoita tai etäyhteyksiä – tai kun kyse on tilaisuudesta, jonka pitää onnistua – teknikko on halpa vakuutus.'),
            ('h2', 'Kysy tätä, kun varaat kokoustilaa'),
            ('ol', [
                'Mitä äänilaitteita salissa on?',
                'Onko tilaisuuden aikana paikalla joku, joka osaa käyttää niitä?',
                'Voiko oman ääniteknikon tuoda, ja saako hän käyttää talon laitteita?',
                'Missä on äänipöytä ja miten puhujien koneet kytketään?',
            ]),
            ('p', f'Lue myös: <a href="{KOKOUS}">Äänentoisto kokouksiin ja konferensseihin</a>.'),
            ('p', '<strong>Edustatko hotellia tai tapahtumapaikkaa?</strong> Toimimme mielellämme tapahtumapaikkojen luottoteknikkona Uudellamaalla ja sen ulkopuolella. Ota yhteyttä, niin kerromme, miten yhteistyö toimii.'),
            CTA,
        ],
    ),
]


def blocks(body):
    out = []
    for kind, val in body:
        if kind == 'p':
            out.append(f'<!-- wp:paragraph -->\n<p>{val}</p>\n<!-- /wp:paragraph -->')
        elif kind == 'h2':
            out.append(f'<!-- wp:heading -->\n<h2 class="wp-block-heading">{val}</h2>\n<!-- /wp:heading -->')
        elif kind in ('ul', 'ol'):
            items = '\n\n'.join(f'<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->' for i in val)
            attr = ' {"ordered":true}' if kind == 'ol' else ''
            out.append(f'<!-- wp:list{attr} -->\n<{kind} class="wp-block-list">{items}</{kind}>\n<!-- /wp:list -->')
    return '\n\n'.join(out)
