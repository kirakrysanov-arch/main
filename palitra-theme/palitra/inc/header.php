<?php
/**
 * Header: top bar, logo + search + cart, catalog mega menu, mobile drawer.
 *
 * @package palitra
 */

defined( 'ABSPATH' ) || exit;

add_action( 'init', 'palitra_replace_storefront_header' );
function palitra_replace_storefront_header() {
	foreach ( array(
		'storefront_header_container'                 => 0,
		'storefront_skip_links'                       => 5,
		'storefront_social_icons'                     => 10,
		'storefront_site_branding'                    => 20,
		'storefront_secondary_navigation'             => 30,
		'storefront_product_search'                   => 40,
		'storefront_header_container_close'           => 41,
		'storefront_primary_navigation_wrapper'       => 42,
		'storefront_primary_navigation'               => 50,
		'storefront_header_cart'                      => 60,
		'storefront_primary_navigation_wrapper_close' => 68,
	) as $fn => $prio ) {
		remove_action( 'storefront_header', $fn, $prio );
	}
	add_action( 'storefront_header', 'palitra_header', 10 );
}

add_action( 'storefront_before_header', 'palitra_topbar' );
function palitra_topbar() {
	?>
	<div class="pl-topbar">
		<div class="col-full pl-topbar__inner">
			<span>Доставка по всей России</span>
			<span class="pl-topbar__sep" aria-hidden="true"></span>
			<span class="pl-hide-sm">Только оригинальная продукция</span>
			<span class="pl-topbar__sep pl-hide-sm" aria-hidden="true"></span>
			<a href="<?php echo esc_url( PALITRA_OZON_URL ); ?>" target="_blank" rel="noopener">Мы на Ozon</a>
		</div>
	</div>
	<?php
}

function palitra_cart_link_html() {
	if ( ! function_exists( 'WC' ) || ! function_exists( 'wc_get_cart_url' ) ) {
		return '';
	}
	$count = ( WC()->cart ) ? (int) WC()->cart->get_cart_contents_count() : 0;
	return sprintf(
		'<a class="pl-cart" href="%1$s" aria-label="%2$s">%3$s<span class="pl-cart__count%4$s">%5$s</span></a>',
		esc_url( wc_get_cart_url() ),
		esc_attr( 'Корзина, ' . palitra_count_label( $count ) ),
		palitra_icon( 'cart' ),
		$count ? '' : ' is-empty',
		$count > 99 ? '99+' : (string) $count
	);
}

/* Keep the header counter in sync after AJAX add-to-cart. */
add_filter( 'woocommerce_add_to_cart_fragments', function ( $fragments ) {
	$fragments['a.pl-cart'] = palitra_cart_link_html();
	return $fragments;
} );

function palitra_header() {
	$tree   = palitra_get_menu_tree();
	$brands = palitra_get_brands();
	$home   = home_url( '/' );
	$acct   = function_exists( 'wc_get_page_permalink' ) ? wc_get_page_permalink( 'myaccount' ) : '';
	?>
	<a class="skip-link screen-reader-text" href="#content">Перейти к содержимому</a>
	<div class="pl-header">
		<div class="col-full pl-header__row">
			<button type="button" class="pl-burger" aria-controls="pl-drawer" aria-expanded="false" aria-label="Открыть меню"><?php echo palitra_icon( 'menu' ); // phpcs:ignore ?></button>

			<a class="pl-logo" href="<?php echo esc_url( $home ); ?>" rel="home">
				<span class="pl-logo__mark" aria-hidden="true"><?php echo palitra_sticks_svg( array( '#e8b4b8', '#f2d0a4', '#a8c69f', '#9db4d6' ), 'pl-logo__svg' ); // phpcs:ignore ?></span>
				<span class="pl-logo__text"><?php echo esc_html( get_bloginfo( 'name' ) ); ?></span>
			</a>

			<form class="pl-search" role="search" method="get" action="<?php echo esc_url( $home ); ?>">
				<label class="screen-reader-text" for="pl-search-input">Поиск по товарам</label>
				<input id="pl-search-input" type="search" name="s" value="<?php echo esc_attr( get_search_query() ); ?>" placeholder="Поиск: бренд, набор, цвет…" autocomplete="off">
				<input type="hidden" name="post_type" value="product">
				<button type="submit" aria-label="Искать"><?php echo palitra_icon( 'search' ); // phpcs:ignore ?></button>
			</form>

			<div class="pl-header__actions">
				<?php if ( $acct ) : ?>
					<a class="pl-action pl-action--account" href="<?php echo esc_url( $acct ); ?>" aria-label="Личный кабинет"><?php echo palitra_icon( 'user' ); // phpcs:ignore ?></a>
				<?php endif; ?>
				<div class="pl-action pl-action--cart"><?php echo palitra_cart_link_html(); // phpcs:ignore ?></div>
			</div>
		</div>

		<nav class="pl-nav" aria-label="Каталог">
			<div class="col-full">
				<ul class="pl-nav__list">
					<?php if ( $brands ) : ?>
						<li class="pl-nav__item pl-nav__item--brands">
							<a class="pl-nav__link" href="<?php echo esc_url( palitra_brands_page_url() ); ?>">Бренды <?php echo palitra_icon( 'chevron' ); // phpcs:ignore ?></a>
							<div class="pl-mega pl-mega--brands">
								<div class="col-full">
									<p class="pl-mega__title">Все бренды</p>
									<ul class="pl-mega__brands">
										<?php foreach ( $brands as $b ) : ?>
											<li><a href="<?php echo esc_url( $b['url'] ); ?>"><span><?php echo esc_html( $b['name'] ); ?></span><small><?php echo (int) $b['count']; ?></small></a></li>
										<?php endforeach; ?>
									</ul>
									<a class="pl-mega__all" href="<?php echo esc_url( palitra_brands_page_url() ); ?>">Все бренды от А до Я <?php echo palitra_icon( 'arrow' ); // phpcs:ignore ?></a>
								</div>
							</div>
						</li>
					<?php endif; ?>

					<?php foreach ( $tree as $cat ) : ?>
						<li class="pl-nav__item">
							<a class="pl-nav__link" href="<?php echo esc_url( $cat['url'] ); ?>"><?php echo esc_html( $cat['name'] ); ?> <?php echo palitra_icon( 'chevron' ); // phpcs:ignore ?></a>
							<div class="pl-mega">
								<div class="col-full pl-mega__grid">
									<div class="pl-mega__col">
										<p class="pl-mega__title"><?php echo esc_html( $cat['name'] ); ?></p>
										<ul class="pl-mega__list">
											<li><a href="<?php echo esc_url( $cat['url'] ); ?>"><strong>Все товары</strong><small><?php echo (int) $cat['count']; ?></small></a></li>
											<?php foreach ( $cat['children'] as $child ) : ?>
												<li><a href="<?php echo esc_url( $child['url'] ); ?>"><span><?php echo esc_html( $child['name'] ); ?></span><small><?php echo (int) $child['count']; ?></small></a></li>
											<?php endforeach; ?>
										</ul>
									</div>
									<?php if ( $cat['brands'] ) : ?>
										<div class="pl-mega__col pl-mega__col--wide">
											<p class="pl-mega__title">Бренды</p>
											<ul class="pl-mega__list pl-mega__list--cols">
												<?php foreach ( $cat['brands'] as $b ) : ?>
													<li><a href="<?php echo esc_url( $b['url'] ); ?>"><span><?php echo esc_html( $b['name'] ); ?></span><small><?php echo (int) $b['count']; ?></small></a></li>
												<?php endforeach; ?>
											</ul>
										</div>
									<?php endif; ?>
									<a class="pl-mega__promo" href="<?php echo esc_url( $cat['url'] ); ?>">
										<?php echo palitra_sticks_svg( palitra_category_colours( $cat['name'] ), 'pl-mega__art' ); // phpcs:ignore ?>
										<span><?php echo esc_html( $cat['name'] ); ?></span>
										<small><?php echo esc_html( palitra_count_label( $cat['count'] ) ); ?> <?php echo palitra_icon( 'arrow' ); // phpcs:ignore ?></small>
									</a>
								</div>
							</div>
						</li>
					<?php endforeach; ?>
				</ul>
			</div>
		</nav>
	</div>

	<div id="pl-drawer" class="pl-drawer" hidden>
		<div class="pl-drawer__panel" role="dialog" aria-modal="true" aria-label="Меню">
			<div class="pl-drawer__head">
				<span class="pl-logo__text"><?php echo esc_html( get_bloginfo( 'name' ) ); ?></span>
				<button type="button" class="pl-drawer__close" aria-label="Закрыть меню"><?php echo palitra_icon( 'close' ); // phpcs:ignore ?></button>
			</div>
			<?php if ( $brands ) : ?>
				<details class="pl-drawer__group">
					<summary>Бренды <?php echo palitra_icon( 'chevron' ); // phpcs:ignore ?></summary>
					<ul>
						<?php foreach ( $brands as $b ) : ?>
							<li><a href="<?php echo esc_url( $b['url'] ); ?>"><?php echo esc_html( $b['name'] ); ?> <small><?php echo (int) $b['count']; ?></small></a></li>
						<?php endforeach; ?>
						<li><a class="pl-drawer__all" href="<?php echo esc_url( palitra_brands_page_url() ); ?>">Все бренды от А до Я</a></li>
					</ul>
				</details>
			<?php endif; ?>
			<?php foreach ( $tree as $cat ) : ?>
				<details class="pl-drawer__group">
					<summary><?php echo esc_html( $cat['name'] ); ?> <?php echo palitra_icon( 'chevron' ); // phpcs:ignore ?></summary>
					<ul>
						<li><a class="pl-drawer__all" href="<?php echo esc_url( $cat['url'] ); ?>">Все товары <small><?php echo (int) $cat['count']; ?></small></a></li>
						<?php foreach ( $cat['children'] as $child ) : ?>
							<li><a href="<?php echo esc_url( $child['url'] ); ?>"><?php echo esc_html( $child['name'] ); ?> <small><?php echo (int) $child['count']; ?></small></a></li>
						<?php endforeach; ?>
						<?php if ( $cat['brands'] ) : ?>
							<li class="pl-drawer__label">Бренды</li>
							<?php foreach ( $cat['brands'] as $b ) : ?>
								<li><a href="<?php echo esc_url( $b['url'] ); ?>"><?php echo esc_html( $b['name'] ); ?> <small><?php echo (int) $b['count']; ?></small></a></li>
							<?php endforeach; ?>
						<?php endif; ?>
					</ul>
				</details>
			<?php endforeach; ?>
			<div class="pl-drawer__links">
				<a href="<?php echo esc_url( PALITRA_OZON_URL ); ?>" target="_blank" rel="noopener">Магазин на Ozon</a>
				<?php if ( $acct ) : ?>
					<a href="<?php echo esc_url( $acct ); ?>">Личный кабинет</a>
				<?php endif; ?>
			</div>
		</div>
	</div>
	<?php
}
