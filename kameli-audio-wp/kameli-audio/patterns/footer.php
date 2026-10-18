<?php
/**
 * Title: Alatunniste
 * Slug: kameli-audio/footer
 * Categories: kameli-audio
 * Inserter: no
 *
 * @package kameli-audio
 */

?>
<!-- wp:group {"align":"full","className":"kameli-footer","style":{"spacing":{"padding":{"top":"var:preset|spacing|60","bottom":"var:preset|spacing|40"}}},"backgroundColor":"hiili","textColor":"vaalea-teksti","layout":{"type":"constrained"}} -->
<div class="wp-block-group alignfull kameli-footer has-vaalea-teksti-color has-hiili-background-color has-text-color has-background" style="padding-top:var(--wp--preset--spacing--60);padding-bottom:var(--wp--preset--spacing--40)"><!-- wp:columns {"align":"wide"} -->
<div class="wp-block-columns alignwide"><!-- wp:column {"width":"40%"} -->
<div class="wp-block-column" style="flex-basis:40%"><!-- wp:image {"width":"110px","sizeSlug":"full","linkDestination":"none"} -->
<figure class="wp-block-image size-full is-resized"><img src="<?php echo kameli_audio_image( 'kameli-audio-logo.png' ); ?>" alt="Kameli Audio" style="width:110px"/></figure>
<!-- /wp:image -->

<!-- wp:paragraph {"fontSize":"small"} -->
<p class="has-small-font-size">Tapahtumatekniikkaa ja studiotuotantoa Vantaan Hakkilasta.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:paragraph {"className":"kameli-eyebrow"} -->
<p class="kameli-eyebrow">Sivut</p>
<!-- /wp:paragraph -->

<!-- wp:list {"className":"kameli-linkkilista"} -->
<ul class="wp-block-list kameli-linkkilista"><!-- wp:list-item -->
<li><a href="<?php echo kameli_audio_page_url( 'palvelut/yritykset' ); ?>">Yritykset</a></li>
<!-- /wp:list-item --><!-- wp:list-item -->
<li><a href="<?php echo kameli_audio_page_url( 'palvelut/yksityiset' ); ?>">Yksityiset</a></li>
<!-- /wp:list-item --><!-- wp:list-item -->
<li><a href="<?php echo kameli_audio_page_url( 'palvelut/artistit' ); ?>">Artistit</a></li>
<!-- /wp:list-item --><!-- wp:list-item -->
<li><a href="<?php echo kameli_audio_page_url( 'blogi' ); ?>">Blogi</a></li>
<!-- /wp:list-item --></ul>
<!-- /wp:list --></div>
<!-- /wp:column -->

<!-- wp:column -->
<div class="wp-block-column"><!-- wp:paragraph {"className":"kameli-eyebrow"} -->
<p class="kameli-eyebrow">Yhteystiedot</p>
<!-- /wp:paragraph -->

<!-- wp:list {"className":"kameli-linkkilista"} -->
<ul class="wp-block-list kameli-linkkilista"><!-- wp:list-item -->
<li><a href="mailto:juha@kameliaudio.fi">juha@kameliaudio.fi</a></li>
<!-- /wp:list-item --><!-- wp:list-item -->
<li><a href="mailto:sakari@kameliaudio.fi">sakari@kameliaudio.fi</a></li>
<!-- /wp:list-item --><!-- wp:list-item -->
<li>Kameli Studio, Hakkila, Vantaa</li>
<!-- /wp:list-item --></ul>
<!-- /wp:list --></div>
<!-- /wp:column --></div>
<!-- /wp:columns -->

<!-- wp:paragraph {"className":"kameli-copyright","fontSize":"small"} -->
<p class="kameli-copyright has-small-font-size">© <?php echo esc_html( gmdate( 'Y' ) ); ?> Kameli Audio. Kaikki oikeudet pidätetään.</p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->
