<?php
/**
 * Plugin Name:       Палитра — синхронизация остатков с Ozon
 * Description:       Синхронизирует остатки товаров между WooCommerce и складом FBS на Ozon. Товары сопоставляются по артикулу (SKU на сайте = артикул на Ozon). Цены не меняются.
 * Version:           1.0.2
 * Requires at least: 6.4
 * Requires PHP:      7.4
 * Author:            Палитра
 * License:           GPL-2.0-or-later
 * Text Domain:       palitra-ozon-sync
 *
 * @package palitra-ozon-sync
 */

defined( 'ABSPATH' ) || exit;

require_once __DIR__ . '/includes/class-pos-logic.php';

final class Palitra_Ozon_Sync {

	const OPT        = 'pos_settings';
	const OPT_LOG    = 'pos_log';
	const OPT_QUEUE  = 'pos_push_queue';
	const OPT_PUSHED = 'pos_recent_push';
	const OPT_STATE  = 'pos_state';
	const CRON_PULL  = 'pos_pull_event';
	const CRON_PUSH  = 'pos_push_event';
	const API        = 'https://api-seller.ozon.ru';
	const PUSH_DELAY = 150;   // seconds; Ozon allows one stock update per product per warehouse every 2 minutes.
	const GUARD      = 600;   // seconds; after pushing, skip pulling that product for 10 minutes.

	/** True while the plugin itself writes stock, so those writes are not pushed back to Ozon. */
	private static $suppress = false;

	public static function init() {
		add_filter( 'cron_schedules', array( __CLASS__, 'schedules' ) );
		add_action( self::CRON_PULL, array( __CLASS__, 'pull' ) );
		add_action( self::CRON_PUSH, array( __CLASS__, 'push' ) );
		add_action( 'woocommerce_product_set_stock', array( __CLASS__, 'on_stock_change' ) );
		add_action( 'woocommerce_variation_set_stock', array( __CLASS__, 'on_stock_change' ) );
		add_action( 'admin_menu', array( __CLASS__, 'menu' ) );
		add_action( 'admin_post_pos_save', array( __CLASS__, 'handle_save' ) );
		add_action( 'admin_post_pos_action', array( __CLASS__, 'handle_action' ) );
		add_filter( 'plugin_action_links_' . plugin_basename( __FILE__ ), array( __CLASS__, 'action_links' ) );
	}

	/* ------------------------------------------------------------------ settings */

	public static function settings() {
		$defaults = array(
			'client_id'    => '',
			'api_key'      => '',
			'warehouse_id' => '',
			'interval'     => 15,
			'dry_run'      => 1,
			'pull_enabled' => 1,
			'push_enabled' => 1,
		);
		$s = get_option( self::OPT, array() );
		return array_merge( $defaults, is_array( $s ) ? $s : array() );
	}

	public static function schedules( $schedules ) {
		foreach ( array( 15, 30, 60 ) as $m ) {
			$schedules[ 'pos_every_' . $m ] = array(
				'interval' => $m * MINUTE_IN_SECONDS,
				'display'  => sprintf( 'Каждые %d минут (Ozon)', $m ),
			);
		}
		return $schedules;
	}

	public static function reschedule() {
		wp_clear_scheduled_hook( self::CRON_PULL );
		$s = self::settings();
		if ( $s['pull_enabled'] && $s['client_id'] && $s['api_key'] ) {
			wp_schedule_event( time() + 60, 'pos_every_' . (int) $s['interval'], self::CRON_PULL );
		}
	}

	public static function activate() {
		self::reschedule();
	}

	public static function deactivate() {
		wp_clear_scheduled_hook( self::CRON_PULL );
		wp_clear_scheduled_hook( self::CRON_PUSH );
	}

	/* ------------------------------------------------------------------ log */

	public static function log( $level, $msg ) {
		$log = get_option( self::OPT_LOG, array() );
		if ( ! is_array( $log ) ) {
			$log = array();
		}
		array_unshift( $log, array( time(), $level, $msg ) );
		update_option( self::OPT_LOG, array_slice( $log, 0, 300 ), false );
	}

	private static function state( $key, $value = null ) {
		$st = get_option( self::OPT_STATE, array() );
		if ( null === $value ) {
			return isset( $st[ $key ] ) ? $st[ $key ] : null;
		}
		$st[ $key ] = $value;
		update_option( self::OPT_STATE, $st, false );
		return $value;
	}

	/* ------------------------------------------------------------------ Ozon API */

	/**
	 * @return array{0:int,1:mixed}|WP_Error  [HTTP code, decoded body]
	 */
	public static function api( $path, $body ) {
		$s = self::settings();
		if ( ! $s['client_id'] || ! $s['api_key'] ) {
			return new WP_Error( 'pos_no_keys', 'Не указаны Client-Id и API-ключ Ozon.' );
		}
		$res = wp_remote_post(
			self::API . $path,
			array(
				'timeout' => 30,
				'headers' => array(
					'Client-Id'    => $s['client_id'],
					'Api-Key'      => $s['api_key'],
					'Content-Type' => 'application/json',
				),
				'body'    => wp_json_encode( (object) $body ),
			)
		);
		if ( is_wp_error( $res ) ) {
			return $res;
		}
		return array( (int) wp_remote_retrieve_response_code( $res ), json_decode( wp_remote_retrieve_body( $res ), true ) );
	}

	private static function api_error_text( $r ) {
		if ( is_wp_error( $r ) ) {
			return $r->get_error_message();
		}
		$msg = is_array( $r[1] ) && isset( $r[1]['message'] ) ? $r[1]['message'] : '';
		return 'HTTP ' . $r[0] . ( $msg ? ': ' . $msg : '' );
	}

	/**
	 * Warehouse list. Tries the current and the older API version and accepts either
	 * response shape; logs Ozon's raw answer when nothing usable comes back.
	 */
	public static function warehouses() {
		$errors = array();
		foreach ( array( array( '/v2/warehouse/list', array( 'limit' => 200 ) ), array( '/v1/warehouse/list', array() ) ) as $try ) {
			$r = self::api( $try[0], $try[1] );
			if ( is_wp_error( $r ) ) {
				return new WP_Error( 'pos_api', $r->get_error_message() );
			}
			if ( 401 === $r[0] || 403 === $r[0] ) {
				return new WP_Error( 'pos_api', self::api_error_text( $r ) . ' — проверьте Client-Id, API-ключ и права ключа.' );
			}
			if ( 200 !== $r[0] ) {
				$errors[] = $try[0] . ': ' . self::api_error_text( $r );
				continue;
			}
			$list = POS_Logic::parse_warehouses( $r[1] );
			if ( $list ) {
				return $list;
			}
			$raw      = wp_json_encode( $r[1] );
			$errors[] = $try[0] . ': складов не найдено, ответ Ozon: ' . ( function_exists( 'mb_substr' ) ? mb_substr( $raw, 0, 300 ) : substr( $raw, 0, 300 ) );
		}
		return new WP_Error( 'pos_api', implode( ' | ', $errors ) );
	}

	/** All FBS stock on Ozon: offer_id => available (present − reserved). */
	public static function fetch_ozon_stocks() {
		$all    = array();
		$cursor = '';
		for ( $page = 0; $page < 50; $page++ ) {
			$body = array(
				'filter' => array( 'visibility' => 'ALL' ),
				'limit'  => 1000,
			);
			if ( '' !== $cursor ) {
				$body['cursor'] = $cursor;
			}
			$r = self::api( '/v4/product/info/stocks', $body );
			if ( is_wp_error( $r ) || 200 !== $r[0] ) {
				return new WP_Error( 'pos_api', self::api_error_text( $r ) );
			}
			$items = isset( $r[1]['items'] ) ? $r[1]['items'] : array();
			$all  += POS_Logic::parse_stocks( $items );
			$next  = isset( $r[1]['cursor'] ) ? (string) $r[1]['cursor'] : '';
			if ( empty( $items ) || '' === $next || $next === $cursor ) {
				break;
			}
			$cursor = $next;
		}
		return $all;
	}

	/* ------------------------------------------------------------------ pull: Ozon → site */

	public static function pull( $manual = false ) {
		$s = self::settings();
		if ( ! $manual && ! $s['pull_enabled'] ) {
			return;
		}
		if ( get_transient( 'pos_pull_lock' ) ) {
			return;
		}
		set_transient( 'pos_pull_lock', 1, 5 * MINUTE_IN_SECONDS );

		$stocks = self::fetch_ozon_stocks();
		if ( is_wp_error( $stocks ) ) {
			self::log( 'error', 'Чтение остатков Ozon: ' . $stocks->get_error_message() );
			delete_transient( 'pos_pull_lock' );
			return;
		}

		$recent  = get_option( self::OPT_PUSHED, array() );
		$queue   = get_option( self::OPT_QUEUE, array() );
		$changed = 0;
		$same    = 0;
		$skipped = 0;
		$missing = array();

		foreach ( $stocks as $offer_id => $available ) {
			$pid = wc_get_product_id_by_sku( $offer_id );
			if ( ! $pid ) {
				$missing[] = $offer_id;
				continue;
			}
			if ( isset( $queue[ $pid ] ) || ( isset( $recent[ $pid ] ) && time() - $recent[ $pid ] < self::GUARD ) ) {
				$skipped++; // a site change for this product is on its way to Ozon
				continue;
			}
			$product = wc_get_product( $pid );
			if ( ! $product ) {
				continue;
			}
			$current = $product->managing_stock() ? (int) $product->get_stock_quantity() : null;
			if ( $current === (int) $available ) {
				$same++;
				continue;
			}
			$changed++;
			$label = $product->get_name() . ' (' . $offer_id . ')';
			if ( $s['dry_run'] ) {
				self::log( 'test', sprintf( 'Изменил бы остаток на сайте: %s — %s → %d', $label, null === $current ? 'не учитывается' : $current, $available ) );
				continue;
			}
			self::$suppress = true;
			if ( ! $product->managing_stock() ) {
				$product->set_manage_stock( true );
			}
			$product->set_stock_quantity( (int) $available );
			$product->save();
			self::$suppress = false;
			self::log( 'info', sprintf( 'Остаток на сайте обновлён по Ozon: %s — %s → %d', $label, null === $current ? 'не учитывался' : $current, $available ) );
		}

		$summary = sprintf(
			'%sСинхронизация с Ozon: товаров на Ozon %d, изменено %d, без изменений %d, пропущено (ждут отправки на Ozon) %d, нет на сайте %d.',
			$s['dry_run'] ? '[Тестовый режим] ' : '',
			count( $stocks ),
			$changed,
			$same,
			$skipped,
			count( $missing )
		);
		if ( $missing ) {
			$summary .= ' Нет на сайте: ' . implode( ', ', array_slice( $missing, 0, 10 ) ) . ( count( $missing ) > 10 ? '…' : '' );
		}
		self::log( 'info', $summary );
		self::state( 'last_pull', time() );
		delete_transient( 'pos_pull_lock' );
	}

	/* ------------------------------------------------------------------ push: site → Ozon */

	public static function on_stock_change( $product ) {
		if ( self::$suppress ) {
			return;
		}
		$s = self::settings();
		if ( ! $s['push_enabled'] || ! $s['warehouse_id'] ) {
			return;
		}
		$id = is_object( $product ) ? $product->get_id() : (int) $product;
		if ( ! $id ) {
			return;
		}
		$queue        = get_option( self::OPT_QUEUE, array() );
		$queue[ $id ] = time();
		update_option( self::OPT_QUEUE, $queue, false );
		if ( ! wp_next_scheduled( self::CRON_PUSH ) ) {
			wp_schedule_single_event( time() + self::PUSH_DELAY, self::CRON_PUSH );
		}
	}

	public static function push() {
		$s     = self::settings();
		$queue = get_option( self::OPT_QUEUE, array() );
		if ( ! $queue ) {
			return;
		}
		update_option( self::OPT_QUEUE, array(), false );

		$rows = array();
		foreach ( array_keys( $queue ) as $pid ) {
			$p = wc_get_product( $pid );
			if ( ! $p || ! $p->get_sku() || ! $p->managing_stock() ) {
				continue;
			}
			$rows[] = array(
				'id'       => $pid,
				'offer_id' => $p->get_sku(),
				'stock'    => (int) $p->get_stock_quantity(),
				'name'     => $p->get_name(),
			);
		}
		if ( ! $rows ) {
			return;
		}

		if ( $s['dry_run'] ) {
			foreach ( $rows as $r ) {
				self::log( 'test', sprintf( 'Отправил бы на Ozon: %s (%s) — остаток %d', $r['name'], $r['offer_id'], max( 0, $r['stock'] ) ) );
			}
			return;
		}

		$recent = get_option( self::OPT_PUSHED, array() );
		foreach ( POS_Logic::build_push_batches( $rows, $s['warehouse_id'] ) as $batch ) {
			$r = self::api( '/v2/products/stocks', array( 'stocks' => $batch ) );
			if ( is_wp_error( $r ) || 200 !== $r[0] ) {
				// Put these back and try again later (e.g. rate limit).
				$q = get_option( self::OPT_QUEUE, array() );
				foreach ( $batch as $b ) {
					$pid       = wc_get_product_id_by_sku( $b['offer_id'] );
					$q[ $pid ] = time();
				}
				update_option( self::OPT_QUEUE, $q, false );
				wp_schedule_single_event( time() + 5 * MINUTE_IN_SECONDS, self::CRON_PUSH );
				self::log( 'error', 'Отправка остатков на Ozon не удалась, повторю через 5 минут: ' . self::api_error_text( $r ) );
				continue;
			}
			$sent = array_column( $batch, 'stock', 'offer_id' );
			foreach ( POS_Logic::parse_push_result( $r[1] ) as $offer_id => $res ) {
				$res['stock'] = $sent[ $offer_id ] ?? $res['stock'];
				if ( $res['ok'] ) {
					$pid = wc_get_product_id_by_sku( $offer_id );
					if ( $pid ) {
						$recent[ $pid ] = time();
					}
					self::log( 'info', sprintf( 'Остаток отправлен на Ozon: %s — %d', $offer_id, $res['stock'] ) );
				} else {
					self::log( 'error', sprintf( 'Ozon не принял остаток для %s: %s', $offer_id, $res['error'] ) );
				}
			}
		}
		// Forget old push timestamps.
		foreach ( $recent as $pid => $t ) {
			if ( time() - $t > self::GUARD ) {
				unset( $recent[ $pid ] );
			}
		}
		update_option( self::OPT_PUSHED, $recent, false );
	}

	/* ------------------------------------------------------------------ admin */

	public static function menu() {
		add_submenu_page( 'woocommerce', 'Синхронизация с Ozon', 'Ozon: остатки', 'manage_woocommerce', 'palitra-ozon-sync', array( __CLASS__, 'page' ) );
	}

	public static function action_links( $links ) {
		array_unshift( $links, '<a href="' . esc_url( admin_url( 'admin.php?page=palitra-ozon-sync' ) ) . '">Настройки</a>' );
		return $links;
	}

	public static function handle_save() {
		if ( ! current_user_can( 'manage_woocommerce' ) ) {
			wp_die( 'Недостаточно прав.' );
		}
		check_admin_referer( 'pos_save' );
		$old = self::settings();
		$in  = wp_unslash( $_POST ); // phpcs:ignore WordPress.Security.NonceVerification
		$new = array(
			'client_id'    => sanitize_text_field( $in['client_id'] ?? '' ),
			'api_key'      => '' !== trim( (string) ( $in['api_key'] ?? '' ) ) ? sanitize_text_field( $in['api_key'] ) : $old['api_key'],
			'warehouse_id' => preg_replace( '/\D/', '', (string) ( $in['warehouse_id'] ?? '' ) ),
			'interval'     => in_array( (int) ( $in['interval'] ?? 15 ), array( 15, 30, 60 ), true ) ? (int) $in['interval'] : 15,
			'dry_run'      => empty( $in['dry_run'] ) ? 0 : 1,
			'pull_enabled' => empty( $in['pull_enabled'] ) ? 0 : 1,
			'push_enabled' => empty( $in['push_enabled'] ) ? 0 : 1,
		);
		update_option( self::OPT, $new, false );
		self::reschedule();
		if ( $old['dry_run'] && ! $new['dry_run'] ) {
			self::log( 'info', 'Тестовый режим выключен — синхронизация работает по-настоящему.' );
		}
		$then = sanitize_key( $in['then'] ?? '' );
		$arg  = '';
		if ( 'test' === $then ) {
			$arg = self::run_connection_test();
		} elseif ( 'pull' === $then ) {
			delete_transient( 'pos_pull_lock' );
			self::pull( true );
			$arg = 'pulled';
		}
		wp_safe_redirect( admin_url( 'admin.php?page=palitra-ozon-sync&saved=1' . ( $arg ? '&done=' . $arg : '' ) ) );
		exit;
	}

	/** @return string 'ok' | 'fail' */
	private static function run_connection_test() {
		$s = self::settings();
		if ( ! $s['client_id'] || ! $s['api_key'] ) {
			self::log( 'error', 'Проверка подключения: Client-Id или API-ключ не заполнены.' );
			return 'fail';
		}
		$w = self::warehouses();
		if ( is_wp_error( $w ) ) {
			self::log( 'error', 'Проверка подключения: ' . $w->get_error_message() );
			return 'fail';
		}
		set_transient( 'pos_warehouses', $w, DAY_IN_SECONDS );
		self::log( 'info', 'Подключение к Ozon работает. Складов: ' . count( $w ) . ( $w ? ' (' . implode( ', ', wp_list_pluck( $w, 'name' ) ) . ')' : '' ) . '.' );
		return 'ok';
	}

	public static function handle_action() {
		if ( ! current_user_can( 'manage_woocommerce' ) ) {
			wp_die( 'Недостаточно прав.' );
		}
		check_admin_referer( 'pos_action' );
		$do  = sanitize_key( $_POST['do'] ?? '' ); // phpcs:ignore WordPress.Security.NonceVerification
		$arg = '';
		if ( 'test' === $do ) {
			$arg = self::run_connection_test();
		} elseif ( 'pull' === $do ) {
			delete_transient( 'pos_pull_lock' );
			self::pull( true );
			$arg = 'pulled';
		} elseif ( 'clear_log' === $do ) {
			update_option( self::OPT_LOG, array(), false );
		}
		wp_safe_redirect( admin_url( 'admin.php?page=palitra-ozon-sync&done=' . $arg ) );
		exit;
	}

	public static function page() {
		if ( ! current_user_can( 'manage_woocommerce' ) ) {
			return;
		}
		$s     = self::settings();
		$whs   = get_transient( 'pos_warehouses' );
		$log   = get_option( self::OPT_LOG, array() );
		$next  = wp_next_scheduled( self::CRON_PULL );
		$last  = self::state( 'last_pull' );
		$fmt   = function ( $t ) {
			return $t ? wp_date( 'd.m.Y H:i', $t ) : '—';
		};
		$done  = isset( $_GET['done'] ) ? sanitize_key( $_GET['done'] ) : ''; // phpcs:ignore WordPress.Security.NonceVerification
		?>
		<div class="wrap">
			<h1>Синхронизация остатков с Ozon</h1>
			<?php if ( isset( $_GET['saved'] ) ) : // phpcs:ignore WordPress.Security.NonceVerification ?>
				<div class="notice notice-success is-dismissible"><p>Настройки сохранены.</p></div>
			<?php endif; ?>
			<?php if ( 'ok' === $done ) : ?>
				<div class="notice notice-success is-dismissible"><p>Подключение к Ozon работает. Выберите склад FBS ниже и сохраните.</p></div>
			<?php elseif ( 'fail' === $done ) : ?>
				<div class="notice notice-error is-dismissible"><p>Не удалось подключиться к Ozon — подробности в журнале ниже.</p></div>
			<?php elseif ( 'pulled' === $done ) : ?>
				<div class="notice notice-info is-dismissible"><p>Синхронизация выполнена — результат в журнале ниже.</p></div>
			<?php endif; ?>
			<?php if ( $s['dry_run'] ) : ?>
				<div class="notice notice-warning"><p><strong>Тестовый режим включён.</strong> Плагин ничего не меняет, а только пишет в журнал, что сделал бы. Проверьте журнал и выключите тестовый режим, когда всё выглядит правильно.</p></div>
			<?php endif; ?>

			<p>Остатки сопоставляются по артикулу: <strong>артикул товара на сайте = артикул (offer_id) на Ozon</strong>. Цены не синхронизируются.</p>
			<ul style="list-style:disc;margin-left:20px">
				<li><strong>Ozon → сайт:</strong> раз в <?php echo (int) $s['interval']; ?> минут остаток на сайте = доступный остаток FBS на Ozon (в наличии − в резерве).</li>
				<li><strong>Сайт → Ozon:</strong> при изменении остатка на сайте (заказ, отмена, ручная правка) новый остаток уходит на выбранный склад Ozon примерно через 2,5 минуты.</li>
			</ul>

			<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>">
				<input type="hidden" name="action" value="pos_save">
				<?php wp_nonce_field( 'pos_save' ); ?>
				<table class="form-table" role="presentation">
					<tr>
						<th scope="row"><label for="pos_client">Client-Id</label></th>
						<td><input id="pos_client" name="client_id" type="text" class="regular-text" value="<?php echo esc_attr( $s['client_id'] ); ?>" autocomplete="off">
						<p class="description">Ozon Seller → Настройки → API-ключи.</p></td>
					</tr>
					<tr>
						<th scope="row"><label for="pos_key">API-ключ</label></th>
						<td><input id="pos_key" name="api_key" type="password" class="regular-text" value="" placeholder="<?php echo $s['api_key'] ? '•••••••• (сохранён — оставьте пустым, чтобы не менять)' : ''; ?>" autocomplete="new-password">
						<p class="description"><?php echo $s['api_key'] ? '✅ Ключ сохранён.' : '❌ Ключ ещё не сохранён.'; ?> Нужен ключ с правами на товары и остатки.</p></td>
					</tr>
					<tr>
						<th scope="row"><label for="pos_wh">Склад FBS</label></th>
						<td>
							<?php if ( is_array( $whs ) && $whs ) : ?>
								<select id="pos_wh" name="warehouse_id">
									<option value="">— выберите —</option>
									<?php foreach ( $whs as $w ) : ?>
										<option value="<?php echo esc_attr( $w['id'] ); ?>" <?php selected( (string) $s['warehouse_id'], (string) $w['id'] ); ?>><?php echo esc_html( $w['name'] . ' (' . $w['id'] . ')' ); ?></option>
									<?php endforeach; ?>
								</select>
							<?php else : ?>
								<input id="pos_wh" name="warehouse_id" type="text" class="regular-text" value="<?php echo esc_attr( $s['warehouse_id'] ); ?>" placeholder="ID склада">
								<p class="description">Нажмите «Проверить подключение» — появится список ваших складов.</p>
							<?php endif; ?>
						</td>
					</tr>
					<tr>
						<th scope="row">Как часто проверять Ozon</th>
						<td><select name="interval">
							<?php foreach ( array( 15, 30, 60 ) as $m ) : ?>
								<option value="<?php echo (int) $m; ?>" <?php selected( (int) $s['interval'], $m ); ?>>каждые <?php echo (int) $m; ?> минут</option>
							<?php endforeach; ?>
						</select></td>
					</tr>
					<tr>
						<th scope="row">Направления</th>
						<td>
							<label><input type="checkbox" name="pull_enabled" value="1" <?php checked( $s['pull_enabled'] ); ?>> Ozon → сайт (продажа на Ozon уменьшает остаток на сайте)</label><br>
							<label><input type="checkbox" name="push_enabled" value="1" <?php checked( $s['push_enabled'] ); ?>> Сайт → Ozon (продажа на сайте уменьшает остаток на Ozon)</label>
							<p class="description">Если заказы с сайта через Ozon Pay + Ozon Доставку уже уменьшают остаток на Ozon сами, выключите «Сайт → Ozon», чтобы не списать дважды.</p>
						</td>
					</tr>
					<tr>
						<th scope="row">Тестовый режим</th>
						<td><label><input type="checkbox" name="dry_run" value="1" <?php checked( $s['dry_run'] ); ?>> Только журнал, ничего не менять</label></td>
					</tr>
				</table>
				<p class="submit">
					<button type="submit" name="then" value="" class="button button-primary">Сохранить</button>
					<button type="submit" name="then" value="test" class="button">Сохранить и проверить подключение</button>
					<button type="submit" name="then" value="pull" class="button">Сохранить и синхронизировать сейчас (Ozon → сайт)</button>
				</p>
			</form>
			<p>Последняя синхронизация: <strong><?php echo esc_html( $fmt( $last ) ); ?></strong> · Следующая: <strong><?php echo esc_html( $fmt( $next ) ); ?></strong></p>

			<h2>Журнал</h2>
			<form method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" style="margin-bottom:8px">
				<input type="hidden" name="action" value="pos_action"><input type="hidden" name="do" value="clear_log">
				<?php wp_nonce_field( 'pos_action' ); ?>
				<?php submit_button( 'Очистить журнал', 'link', 'submit', false ); ?>
			</form>
			<table class="widefat striped">
				<thead><tr><th style="width:140px">Время</th><th style="width:80px">Тип</th><th>Сообщение</th></tr></thead>
				<tbody>
				<?php if ( ! $log ) : ?>
					<tr><td colspan="3">Пока пусто.</td></tr>
				<?php else : ?>
					<?php
					$labels = array( 'info' => 'инфо', 'error' => 'ошибка', 'test' => 'тест' );
					foreach ( array_slice( $log, 0, 200 ) as $e ) :
						?>
						<tr>
							<td><?php echo esc_html( $fmt( $e[0] ) ); ?></td>
							<td><?php echo esc_html( $labels[ $e[1] ] ?? $e[1] ); ?></td>
							<td><?php echo esc_html( $e[2] ); ?></td>
						</tr>
					<?php endforeach; ?>
				<?php endif; ?>
				</tbody>
			</table>
		</div>
		<?php
	}
}

register_activation_hook( __FILE__, array( 'Palitra_Ozon_Sync', 'activate' ) );
register_deactivation_hook( __FILE__, array( 'Palitra_Ozon_Sync', 'deactivate' ) );
add_action( 'plugins_loaded', array( 'Palitra_Ozon_Sync', 'init' ) );
