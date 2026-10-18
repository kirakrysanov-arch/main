<?php
/**
 * Title: Blogin kategoriasuodatin
 * Slug: kameli-audio/blogi-suodatin
 * Categories: kameli-audio
 * Inserter: no
 *
 * @package kameli-audio
 */

$kameli_blog_url = get_option( 'page_for_posts' ) ? get_permalink( get_option( 'page_for_posts' ) ) : home_url( '/' );
?>
<!-- wp:group {"align":"wide","className":"kameli-suodatin","layout":{"type":"flex","flexWrap":"wrap"}} -->
<div class="wp-block-group alignwide kameli-suodatin"><!-- wp:paragraph {"className":"kameli-suodatin__kaikki"} -->
<p class="kameli-suodatin__kaikki"><a href="<?php echo esc_url( $kameli_blog_url ); ?>">Kaikki</a></p>
<!-- /wp:paragraph -->

<!-- wp:categories {"className":"kameli-suodatin__kategoriat"} /--></div>
<!-- /wp:group -->
