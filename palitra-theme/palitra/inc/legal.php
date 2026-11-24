<?php
/**
 * Legal pages for a Russian online shop: business details in the Customizer,
 * draft pages created automatically, checkout consents.
 *
 * Pages use the shortcode [palitra_info key="..."] so details are entered once.
 *
 * @package palitra
 */

defined( 'ABSPATH' ) || exit;

/** Business detail fields: key => [label, placeholder]. */
function palitra_info_fields() {
	return array(
		'ip_name'      => array( 'ИП (полностью)', 'ИП Иванова Анна Сергеевна' ),
		'inn'          => array( 'ИНН', '123456789012' ),
		'ogrnip'       => array( 'ОГРНИП', '312345678901234' ),
		'address'      => array( 'Адрес регистрации ИП', 'г. Москва, ул. …' ),
		'email'        => array( 'Email для покупателей', 'info@palitrart.ru' ),
		'phone'        => array( 'Телефон', '+7 900 000-00-00' ),
		'hours'        => array( 'Часы ответа на сообщения', 'пн–пт, 10:00–19:00 (МСК)' ),
		'ship_days'    => array( 'Срок отправки заказа', '1–2 рабочих дня' ),
		'return_pvz'   => array( 'Адрес пункта выдачи Ozon для возвратов', 'г. Москва, ул. …, пункт выдачи Ozon' ),
		'return_name'  => array( 'Получатель возвратов (ФИО)', 'Иванова Анна Сергеевна' ),
		'return_phone' => array( 'Телефон получателя возвратов', '+7 900 000-00-00' ),
	);
}

function palitra_info( $key ) {
	$v = get_theme_mod( 'palitra_info_' . $key, '' );
	return is_string( $v ) ? trim( $v ) : '';
}

/* [palitra_info key="inn"] — value, or a visible marker for admins / a dash for visitors. */
add_shortcode( 'palitra_info', function ( $atts ) {
	$atts   = shortcode_atts( array( 'key' => '' ), $atts );
	$fields = palitra_info_fields();
	$key    = sanitize_key( $atts['key'] );
	$val    = palitra_info( $key );
	if ( '' !== $val ) {
		if ( 'email' === $key ) {
			return '<a href="mailto:' . esc_attr( antispambot( $val ) ) . '">' . esc_html( antispambot( $val ) ) . '</a>';
		}
		if ( in_array( $key, array( 'phone', 'return_phone' ), true ) ) {
			return '<a href="tel:' . esc_attr( preg_replace( '/[^\d+]/', '', $val ) ) . '">' . esc_html( $val ) . '</a>';
		}
		return esc_html( $val );
	}
	$label = isset( $fields[ $key ] ) ? $fields[ $key ][0] : $key;
	return current_user_can( 'edit_theme_options' )
		? '<mark style="background:#ffe08a">[заполните: ' . esc_html( $label ) . ']</mark>'
		: '—';
} );

/* Customizer: «Реквизиты и контакты (Палитра)». */
add_action( 'customize_register', function ( $wp_customize ) {
	$wp_customize->add_section( 'palitra_info', array(
		'title'       => 'Реквизиты и контакты (Палитра)',
		'priority'    => 31,
		'description' => 'Эти данные автоматически подставляются в страницы «Доставка и оплата», «Возврат», «Публичная оферта», «Политика конфиденциальности», «Согласие на обработку персональных данных» и «Контакты и реквизиты».',
	) );
	foreach ( palitra_info_fields() as $key => $f ) {
		$wp_customize->add_setting( 'palitra_info_' . $key, array( 'sanitize_callback' => 'sanitize_text_field' ) );
		$wp_customize->add_control( 'palitra_info_' . $key, array(
			'label'       => $f[0],
			'section'     => 'palitra_info',
			'type'        => 'text',
			'input_attrs' => array( 'placeholder' => $f[1] ),
		) );
	}
} );

/* ------------------------------------------------------------------ pages */

function palitra_legal_pages() {
	$i = function ( $k ) {
		return '[palitra_info key="' . $k . '"]';
	};
	$site = 'palitrart.ru';

	$delivery = <<<HTML
<h2>Оплата</h2>
<p>Заказы оплачиваются онлайн банковской картой или через Систему быстрых платежей (СБП) с помощью сервиса Ozon Pay (АО «Озон Банк»). Данные карты вводятся на защищённой странице платёжного сервиса — магазин их не получает и не хранит.</p>
<p>После оплаты на ваш email приходит электронный кассовый чек в соответствии с 54-ФЗ.</p>
<h2>Доставка</h2>
<p>Мы доставляем заказы только через <strong>Ozon Доставку</strong> в пункты выдачи и постаматы Ozon по всей России. Пункт выдачи вы выбираете при оформлении заказа.</p>
<ul>
<li>Отправка заказа: {$i('ship_days')} после оплаты.</li>
<li>Срок и стоимость доставки зависят от выбранного пункта выдачи и показываются при оформлении заказа.</li>
<li>Когда заказ прибудет в пункт выдачи, Ozon пришлёт уведомление. Срок хранения заказа в пункте выдачи определяется правилами Ozon.</li>
</ul>
<h2>Отказ от заказа в пункте выдачи</h2>
<p>Вы можете отказаться от заказа при получении в пункте выдачи. В этом случае деньги за товар и доставку вернутся автоматически на карту или счёт, с которого была оплата.</p>
<p>Условия возврата уже полученного товара — на странице «Возврат».</p>
<h2>Вопросы</h2>
<p>Email: {$i('email')}, телефон: {$i('phone')} ({$i('hours')}).</p>
HTML;

	$returns = <<<HTML
<p>Возврат товара осуществляется в соответствии с Законом РФ «О защите прав потребителей» и Правилами продажи товаров дистанционным способом.</p>
<h2>Товар надлежащего качества</h2>
<p>Вы можете вернуть товар надлежащего качества в течение <strong>7 дней</strong> после его получения, если сохранены его товарный вид, потребительские свойства, упаковка и документ, подтверждающий покупку (кассовый чек или номер заказа).</p>
<h2>Товар ненадлежащего качества</h2>
<p>Если товар оказался с недостатком, вы вправе потребовать его замены, уменьшения цены или возврата денег. Требования принимаются в сроки, установленные законом. Пожалуйста, приложите к обращению фото недостатка.</p>
<h2>Как вернуть товар</h2>
<ol>
<li>Напишите нам на {$i('email')} или позвоните по телефону {$i('phone')}: укажите номер заказа, товар и причину возврата.</li>
<li>Отправьте товар через <strong>Ozon Доставку</strong> (отправка посылки из любого пункта выдачи Ozon, оформляется в приложении Ozon) в пункт выдачи по адресу: <strong>{$i('return_pvz')}</strong>. Получатель: <strong>{$i('return_name')}</strong>, телефон {$i('return_phone')}.</li>
<li>После получения и проверки товара мы вернём деньги на карту или счёт, с которого была оплата, в течение <strong>10 дней</strong> с даты вашего требования.</li>
</ol>
<p>При возврате товара надлежащего качества стоимость обратной доставки не возмещается. Если товар ненадлежащего качества, расходы на его возврат мы компенсируем.</p>
<h2>Отказ в пункте выдачи</h2>
<p>Если вы отказались от заказа прямо в пункте выдачи Ozon, деньги за товар и доставку вернутся автоматически — ничего делать не нужно.</p>
HTML;

	$offer = <<<HTML
<p>Редакция от [дата публикации]</p>
<h2>1. Общие положения</h2>
<p>1.1. Настоящий документ является публичной офертой (ст. 437 ГК РФ) {$i('ip_name')} (ИНН {$i('inn')}, ОГРНИП {$i('ogrnip')}), далее — «Продавец», и содержит условия продажи товаров дистанционным способом через сайт {$site} (далее — «Сайт») любому физическому лицу (далее — «Покупатель»).</p>
<p>1.2. Акцептом оферты (ст. 438 ГК РФ) является оформление и оплата заказа на Сайте. С момента акцепта договор купли-продажи считается заключённым.</p>
<p>1.3. Отношения сторон регулируются Гражданским кодексом РФ, Законом РФ «О защите прав потребителей» и Правилами продажи товаров дистанционным способом.</p>
<h2>2. Предмет договора</h2>
<p>2.1. Продавец обязуется передать Покупателю товар, указанный в заказе, а Покупатель — оплатить и принять его.</p>
<p>2.2. Описание, фото и характеристики товара приведены на Сайте. Цвет на фото может незначительно отличаться от реального из-за настроек экрана.</p>
<h2>3. Цена и оплата</h2>
<p>3.1. Цены указаны на Сайте в рублях. Цена товара фиксируется в момент оформления заказа.</p>
<p>3.2. Оплата производится онлайн через сервис Ozon Pay (банковская карта или СБП). Обязательство по оплате считается исполненным с момента подтверждения платежа. Покупатель получает электронный кассовый чек на email.</p>
<h2>4. Доставка и передача товара</h2>
<p>4.1. Доставка осуществляется через Ozon Доставку в выбранный Покупателем пункт выдачи Ozon. Сроки и стоимость доставки указываются при оформлении заказа. Срок отправки — {$i('ship_days')} после оплаты.</p>
<p>4.2. Право собственности и риск случайной гибели товара переходят к Покупателю в момент получения товара в пункте выдачи.</p>
<h2>5. Возврат и обмен</h2>
<p>5.1. Возврат товара осуществляется на условиях, опубликованных на странице «Возврат» Сайта, и в соответствии с законодательством РФ. Возврат денежных средств производится тем же способом, которым была произведена оплата, в течение 10 дней с даты требования.</p>
<h2>6. Ответственность</h2>
<p>6.1. Стороны несут ответственность в соответствии с законодательством РФ. Продавец не отвечает за задержки доставки, вызванные обстоятельствами непреодолимой силы.</p>
<h2>7. Персональные данные</h2>
<p>7.1. Обработка персональных данных Покупателя осуществляется в соответствии с Политикой конфиденциальности и на основании согласия на обработку персональных данных, опубликованных на Сайте.</p>
<h2>8. Реквизиты Продавца</h2>
<p>{$i('ip_name')}<br>ИНН {$i('inn')}<br>ОГРНИП {$i('ogrnip')}<br>Адрес: {$i('address')}<br>Email: {$i('email')}<br>Телефон: {$i('phone')}</p>
HTML;

	$privacy = <<<HTML
<p>Редакция от [дата публикации]</p>
<h2>1. Общие положения</h2>
<p>1.1. Настоящая Политика определяет порядок обработки и защиты персональных данных пользователей сайта {$site} (далее — «Сайт») в соответствии с Федеральным законом № 152-ФЗ «О персональных данных».</p>
<p>1.2. Оператор персональных данных: {$i('ip_name')}, ИНН {$i('inn')}, ОГРНИП {$i('ogrnip')}, адрес: {$i('address')}, email: {$i('email')} (далее — «Оператор»).</p>
<h2>2. Какие данные мы обрабатываем</h2>
<ul>
<li>фамилия, имя;</li>
<li>номер телефона и адрес электронной почты;</li>
<li>выбранный пункт выдачи Ozon и данные заказа;</li>
<li>данные учётной записи на Сайте (если вы её создали);</li>
<li>технические данные: cookie, IP-адрес, сведения о браузере.</li>
</ul>
<p>Данные банковских карт обрабатывает платёжный сервис Ozon Pay; Оператор их не получает и не хранит.</p>
<h2>3. Цели обработки</h2>
<ul>
<li>оформление, оплата и доставка заказов, возвраты;</li>
<li>направление кассовых чеков и уведомлений о заказе;</li>
<li>связь с покупателем по вопросам заказа;</li>
<li>обеспечение работы Сайта.</li>
</ul>
<h2>4. Правовые основания</h2>
<p>Обработка осуществляется для исполнения договора купли-продажи, стороной которого является пользователь, и на основании согласия пользователя на обработку персональных данных.</p>
<h2>5. Передача данных третьим лицам</h2>
<p>Для выполнения заказа данные передаются только в необходимом объёме: ООО «Интернет Решения» (Ozon) — для доставки; АО «Озон Банк» (Ozon Pay) — для приёма оплаты и формирования чеков; хостинг-провайдеру Сайта — для хранения данных. Иным лицам данные передаются только в случаях, предусмотренных законом.</p>
<h2>6. Хранение и защита</h2>
<p>Персональные данные граждан РФ записываются, хранятся и обрабатываются с использованием баз данных, находящихся на территории Российской Федерации. Оператор принимает необходимые правовые, организационные и технические меры для защиты данных.</p>
<p>Данные хранятся не дольше, чем этого требуют цели обработки и законодательство (в том числе налоговое и бухгалтерское), после чего уничтожаются.</p>
<h2>7. Права пользователя</h2>
<p>Вы вправе получить сведения об обработке ваших данных, потребовать их уточнения, блокирования или уничтожения, а также отозвать согласие на обработку, направив запрос на {$i('email')}. Ответ направляется в срок, установленный законом.</p>
<h2>8. Cookie</h2>
<p>Сайт использует cookie, необходимые для работы корзины и оформления заказа. Вы можете отключить cookie в настройках браузера, но тогда оформление заказа может стать недоступным.</p>
HTML;

	$consent = <<<HTML
<p>Оформляя заказ, регистрируясь или отправляя форму на сайте {$site}, я свободно, своей волей и в своём интересе даю согласие {$i('ip_name')} (ИНН {$i('inn')}, ОГРНИП {$i('ogrnip')}, адрес: {$i('address')}) на обработку моих персональных данных на следующих условиях.</p>
<p><strong>Перечень данных:</strong> фамилия, имя; номер телефона; адрес электронной почты; выбранный пункт выдачи; данные заказа.</p>
<p><strong>Цели:</strong> оформление, оплата, доставка и возврат заказа; направление кассовых чеков и уведомлений по заказу; связь со мной по вопросам заказа.</p>
<p><strong>Действия с данными:</strong> сбор, запись, систематизация, накопление, хранение, уточнение, извлечение, использование, передача (предоставление) ООО «Интернет Решения» (Ozon) для доставки и АО «Озон Банк» (Ozon Pay) для приёма оплаты, обезличивание, блокирование, удаление, уничтожение — с использованием средств автоматизации и без них.</p>
<p><strong>Срок:</strong> согласие действует до достижения целей обработки или до его отзыва. Я могу отозвать согласие, направив письмо на {$i('email')}.</p>
<p>Порядок обработки данных описан в Политике конфиденциальности.</p>
HTML;

	$contacts = <<<HTML
<h2>Контакты</h2>
<p>Email: {$i('email')}<br>Телефон: {$i('phone')}<br>Отвечаем: {$i('hours')}</p>
<p>Мы также продаём на Ozon: <a href="https://ozon.ru/s/palitra-3140957">магазин «Палитра» на Ozon</a>.</p>
<h2>Адрес для возвратов</h2>
<p>Пункт выдачи Ozon: {$i('return_pvz')}<br>Получатель: {$i('return_name')}, телефон {$i('return_phone')}</p>
<h2>Реквизиты</h2>
<p>{$i('ip_name')}<br>ИНН {$i('inn')}<br>ОГРНИП {$i('ogrnip')}<br>Адрес: {$i('address')}</p>
HTML;

	return array(
		'dostavka-i-oplata'                       => array( 'Доставка и оплата', $delivery ),
		'vozvrat'                                 => array( 'Возврат', $returns ),
		'oferta'                                  => array( 'Публичная оферта', $offer ),
		'politika-konfidencialnosti'              => array( 'Политика конфиденциальности', $privacy ),
		'soglasie-na-obrabotku-personalnyh-dannyh' => array( 'Согласие на обработку персональных данных', $consent ),
		'kontakty'                                => array( 'Контакты и реквизиты', $contacts ),
	);
}

/** Create missing legal pages as drafts (never overwrites existing pages). */
function palitra_create_legal_pages() {
	foreach ( palitra_legal_pages() as $slug => $page ) {
		if ( get_page_by_path( $slug, OBJECT, 'page' ) ) {
			continue;
		}
		wp_insert_post(
			array(
				'post_title'   => $page[0],
				'post_name'    => $slug,
				'post_status'  => 'draft',
				'post_type'    => 'page',
				'post_content' => $page[1],
			)
		);
	}
	// Use our page as the WordPress privacy page unless a published one is already set.
	$priv    = get_page_by_path( 'politika-konfidencialnosti', OBJECT, 'page' );
	$current = (int) get_option( 'wp_page_for_privacy_policy' );
	if ( $priv && ( ! $current || 'publish' !== get_post_status( $current ) ) ) {
		update_option( 'wp_page_for_privacy_policy', $priv->ID );
	}
	// WooCommerce «Условия» page = the public offer.
	$offer = get_page_by_path( 'oferta', OBJECT, 'page' );
	if ( $offer && ! (int) get_option( 'woocommerce_terms_page_id' ) ) {
		update_option( 'woocommerce_terms_page_id', $offer->ID );
	}
}

/* Admin reminder while details are missing or pages are still drafts. */
add_action( 'admin_notices', function () {
	if ( ! current_user_can( 'edit_pages' ) ) {
		return;
	}
	$missing = array();
	foreach ( array( 'ip_name', 'inn', 'ogrnip', 'email', 'phone', 'return_pvz' ) as $k ) {
		if ( '' === palitra_info( $k ) ) {
			$missing[] = palitra_info_fields()[ $k ][0];
		}
	}
	$drafts = array();
	foreach ( palitra_legal_pages() as $slug => $page ) {
		$p = get_page_by_path( $slug, OBJECT, 'page' );
		if ( $p && 'publish' !== $p->post_status ) {
			$drafts[] = '<a href="' . esc_url( get_edit_post_link( $p->ID ) ) . '">' . esc_html( $page[0] ) . '</a>';
		}
	}
	if ( ! $missing && ! $drafts ) {
		return;
	}
	echo '<div class="notice notice-warning"><p><strong>Палитра — обязательные страницы магазина.</strong> ';
	if ( $missing ) {
		echo 'Заполните реквизиты в <a href="' . esc_url( admin_url( 'customize.php?autofocus[section]=palitra_info' ) ) . '">Внешний вид → Настроить → Реквизиты и контакты</a>: ' . esc_html( implode( ', ', $missing ) ) . '. ';
	}
	if ( $drafts ) {
		echo 'Проверьте и опубликуйте черновики: ' . wp_kses_post( implode( ', ', $drafts ) ) . '.';
	}
	echo '</p></div>';
} );

/* ------------------------------------------------------------------ checkout consents */

function palitra_consent_label() {
	return 'Я даю согласие на обработку персональных данных';
}

/* Block checkout (WooCommerce 8.9+): required checkbox via the Additional Checkout Fields API. */
add_action( 'woocommerce_init', function () {
	if ( ! function_exists( 'woocommerce_register_additional_checkout_field' ) ) {
		return;
	}
	try {
		woocommerce_register_additional_checkout_field(
			array(
				'id'            => 'palitra/pd-consent',
				'label'         => palitra_consent_label() . ' (документ «Согласие на обработку персональных данных» — внизу сайта)',
				'location'      => 'order',
				'type'          => 'checkbox',
				'required'      => true,
				'error_message' => 'Чтобы оформить заказ, подтвердите согласие на обработку персональных данных.',
			)
		);
	} catch ( Throwable $e ) {
		// Older/newer API shape — the classic checkout fallback below still works.
		unset( $e );
	}
} );

/* Classic checkout fallback: checkbox with a link + validation. */
add_action( 'woocommerce_review_order_before_submit', function () {
	$p   = get_page_by_path( 'soglasie-na-obrabotku-personalnyh-dannyh', OBJECT, 'page' );
	$url = $p ? get_permalink( $p ) : '';
	echo '<p class="form-row validate-required" style="margin-bottom:12px"><label class="woocommerce-form__label woocommerce-form__label-for-checkbox checkbox">';
	echo '<input type="checkbox" class="woocommerce-form__input woocommerce-form__input-checkbox input-checkbox" name="palitra_pd_consent" value="1"> ';
	echo '<span>' . esc_html( palitra_consent_label() ) . ( $url ? ' (<a href="' . esc_url( $url ) . '" target="_blank" rel="noopener">согласие</a>)' : '' ) . '</span> <abbr class="required" title="обязательно">*</abbr>';
	echo '</label></p>';
} );
add_action( 'woocommerce_checkout_process', function () {
	if ( empty( $_POST['palitra_pd_consent'] ) ) { // phpcs:ignore WordPress.Security.NonceVerification
		wc_add_notice( 'Чтобы оформить заказ, подтвердите согласие на обработку персональных данных.', 'error' );
	}
} );
