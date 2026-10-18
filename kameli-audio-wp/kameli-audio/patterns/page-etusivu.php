<?php
/**
 * Title: Sivu: Etusivu
 * Slug: kameli-audio/page-etusivu
 * Categories: kameli-audio
 * Post Types: page
 * Block Types: core/post-content
 * Viewport Width: 1280
 *
 * @package kameli-audio
 */

// LUONNOS: etusivun tekstit ovat paikkamerkkejä, jotka korvataan lopullisilla.
?>
<!-- wp:cover {"url":"<?php echo kameli_audio_image( 'kuva-paikkamerkki.svg' ); ?>","dimRatio":60,"overlayColor":"musta","isUserOverlayColor":true,"minHeight":560,"contentPosition":"center center","isDark":true,"align":"full","className":"kameli-etusivu-hero","layout":{"type":"constrained"}} -->
<div class="wp-block-cover alignfull is-dark kameli-etusivu-hero" style="min-height:560px"><img class="wp-block-cover__image-background" alt="" src="<?php echo kameli_audio_image( 'kuva-paikkamerkki.svg' ); ?>" data-object-fit="cover"/><span aria-hidden="true" class="wp-block-cover__background has-musta-background-color has-background-dim-60 has-background-dim"></span><div class="wp-block-cover__inner-container"><!-- wp:heading {"textAlign":"center","level":1} -->
<h1 class="wp-block-heading has-text-align-center">Ääni, joka kantaa.</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"align":"center","fontSize":"large"} -->
<p class="has-text-align-center has-large-font-size">Tapahtumien äänentoistoa ja studiotuotantoa Vantaan Hakkilasta – yrityksille, yksityisille ja artisteille.</p>
<!-- /wp:paragraph -->

<!-- wp:buttons {"layout":{"type":"flex","justifyContent":"center"}} -->
<div class="wp-block-buttons"><!-- wp:button {"backgroundColor":"valkoinen","textColor":"musta"} -->
<div class="wp-block-button"><a class="wp-block-button__link has-musta-color has-valkoinen-background-color has-text-color has-background wp-element-button" href="#yhteydenotto">Pyydä tarjous</a></div>
<!-- /wp:button -->

<!-- wp:button {"className":"is-style-outline"} -->
<div class="wp-block-button is-style-outline"><a class="wp-block-button__link wp-element-button" href="<?php echo kameli_audio_page_url( 'palvelut' ); ?>">Tutustu palveluihin</a></div>
<!-- /wp:button --></div>
<!-- /wp:buttons --></div></div>
<!-- /wp:cover -->

<?php
echo kameli_audio_section_open( 'valkoinen' )
	. kameli_audio_heading( 'Tapahtumatekniikkaa ja studiotuotantoa saman katon alta', 2, true )
	. kameli_audio_paragraph( 'Kameli Audio hoitaa tapahtumasi äänen suunnittelusta purkuun ja vie musiikkisi esituotannosta valmiiksi masteriksi. Olipa kyseessä yritystilaisuus, yksityisjuhla tai bändin äänitys, saat kokeneen tekijän, joka kuuntelee sekä sinua että tilaa.', 'center' )
	. kameli_audio_section_close();

echo kameli_audio_section_open( 'vaalea' )
	. kameli_audio_heading( 'Palvelumme', 2, true )
	. kameli_audio_service_cards()
	. kameli_audio_section_close();

echo kameli_audio_why_us( 'valkoinen' );

echo kameli_audio_section_open( 'vaalea' )
	. kameli_audio_heading( 'Keitä olemme', 2, true )
	. kameli_audio_paragraph( 'Kameli Audion takana ovat Juha ja Sakari. Juha vastaa tapahtumatekniikasta ja studiotuotannoista, Sakari hallinnosta ja tilauksista – ja tuo studioon muusikon ja lauluntekijän näkökulman.', 'center' )
	. kameli_audio_paragraph( '<a href="' . kameli_audio_page_url( 'ota-yhteytta' ) . '"><strong>Tutustu tiimiin →</strong></a>', 'center' )
	. kameli_audio_section_close();

echo kameli_audio_cta();
echo kameli_audio_contact_section( 'Ota yhteyttä', 'valkoinen' );
