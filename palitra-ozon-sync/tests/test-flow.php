<?php
// End-to-end test with stubbed WordPress/WooCommerce. Run: php tests/test-flow.php
define( 'ABSPATH', __DIR__ ); define( 'MINUTE_IN_SECONDS', 60 ); define( 'HOUR_IN_SECONDS', 3600 );
$O = array(); $T = array(); $CRON = array(); $HOOKS = array(); $API_CALLS = array();
function get_option( $k, $d = false ) { global $O; return $O[ $k ] ?? $d; }
function update_option( $k, $v, $a = null ) { global $O; $O[ $k ] = $v; return true; }
function get_transient( $k ) { global $T; return $T[ $k ] ?? false; }
function set_transient( $k, $v, $e ) { global $T; $T[ $k ] = $v; }
function delete_transient( $k ) { global $T; unset( $T[ $k ] ); }
function wp_next_scheduled( $h ) { global $CRON; return $CRON[ $h ] ?? false; }
function wp_schedule_single_event( $t, $h ) { global $CRON; $CRON[ $h ] = $t; }
function wp_schedule_event( $t, $r, $h ) { global $CRON; $CRON[ $h ] = $t; }
function wp_clear_scheduled_hook( $h ) { global $CRON; unset( $CRON[ $h ] ); }
function add_action( ...$a ) {} function add_filter( ...$a ) {} function register_activation_hook( ...$a ) {} function register_deactivation_hook( ...$a ) {} function plugin_basename( $f ) { return 'x'; }
function is_wp_error( $x ) { return $x instanceof WP_Error; }
class WP_Error { private $m; function __construct( $c, $m ) { $this->m = $m; } function get_error_message() { return $this->m; } }
function wp_json_encode( $x ) { return json_encode( $x ); }
class P { public $id,$sku,$qty,$manage,$name; function __construct($id,$sku,$qty,$manage=true){$this->id=$id;$this->sku=$sku;$this->qty=$qty;$this->manage=$manage;$this->name="Product $id";}
 function get_id(){return $this->id;} function get_sku(){return $this->sku;} function managing_stock(){return $this->manage;} function get_stock_quantity(){return $this->qty;}
 function set_manage_stock($b){$this->manage=$b;} function get_name(){return $this->name;}
 function set_stock_quantity($q){ $this->qty=$q; Palitra_Ozon_Sync::on_stock_change($this); } function save(){} }
$PRODUCTS = array( 1 => new P(1,'Unison Botanical 18',5), 2 => new P(2,'PanPastel 010',3), 3 => new P(3,'Terry Ludwig Blues 30',1,false) );
function wc_get_product_id_by_sku( $s ) { global $PRODUCTS; foreach ( $PRODUCTS as $p ) if ( $p->sku === $s ) return $p->id; return 0; }
function wc_get_product( $id ) { global $PRODUCTS; return $PRODUCTS[ $id ] ?? null; }
// fake Ozon
$OZON = array( 'Unison Botanical 18' => array( 4, 1 ), 'PanPastel 010' => array( 3, 0 ), 'Terry Ludwig Blues 30' => array( 2, 0 ), 'Not on site' => array( 9, 0 ) );
function wp_remote_post( $url, $args ) {
	global $OZON, $API_CALLS; $body = json_decode( $args['body'], true ); $API_CALLS[] = array( $url, $body );
	if ( str_ends_with( $url, '/v4/product/info/stocks' ) ) {
		$items = array(); foreach ( $OZON as $o => $pr ) $items[] = array( 'offer_id' => $o, 'stocks' => array( array( 'type' => 'fbs', 'present' => $pr[0], 'reserved' => $pr[1] ) ) );
		return array( 'code' => 200, 'body' => json_encode( array( 'items' => $items, 'cursor' => '', 'total' => count( $items ) ) ) );
	}
	if ( str_ends_with( $url, '/v2/products/stocks' ) ) {
		$res = array(); foreach ( $body['stocks'] as $s ) { $OZON[ $s['offer_id'] ] = array( $s['stock'], 0 ); $res[] = array( 'offer_id' => $s['offer_id'], 'updated' => true, 'errors' => array() ); }
		return array( 'code' => 200, 'body' => json_encode( array( 'result' => $res ) ) );
	}
	return array( 'code' => 404, 'body' => '{}' );
}
function wp_remote_retrieve_response_code( $r ) { return $r['code']; } function wp_remote_retrieve_body( $r ) { return $r['body']; }
require __DIR__ . '/../palitra-ozon-sync.php';
$fail = 0; function check( $n, $g, $w ) { global $fail; if ( $g === $w ) echo "ok   $n\n"; else { $fail++; echo "FAIL $n\n  got:  " . var_export( $g, true ) . "\n  want: " . var_export( $w, true ) . "\n"; } }

// 1) test mode: nothing changes, log has "would change"
update_option( 'pos_settings', array( 'client_id' => '1', 'api_key' => 'k', 'warehouse_id' => '777', 'dry_run' => 1 ) );
Palitra_Ozon_Sync::pull( true );
check( 'dry-run keeps stock', array( $PRODUCTS[1]->qty, $PRODUCTS[3]->qty ), array( 5, 1 ) );
check( 'dry-run logs', count( array_filter( get_option( 'pos_log' ), fn( $e ) => 'test' === $e[1] ) ), 2 );
check( 'dry-run queues nothing', get_option( 'pos_push_queue', array() ), array() );

// 2) live pull: site = Ozon available; pull itself must NOT queue pushes back to Ozon
$O['pos_settings']['dry_run'] = 0;
Palitra_Ozon_Sync::pull( true );
check( 'live pull sets stock', array( $PRODUCTS[1]->qty, $PRODUCTS[2]->qty, $PRODUCTS[3]->qty ), array( 3, 3, 2 ) );
check( 'manage stock switched on', $PRODUCTS[3]->manage, true );
check( 'pull does not echo back', get_option( 'pos_push_queue', array() ), array() );
check( 'missing product reported', (bool) preg_match( '/нет на сайте 1/', get_option( 'pos_log' )[0][2] ), true );

// 3) website sale: stock 3 → 2 queues a push, scheduled ~150s later
$PRODUCTS[1]->set_stock_quantity( 2 );
check( 'sale queued', array_keys( get_option( 'pos_push_queue' ) ), array( 1 ) );
check( 'push scheduled', isset( $CRON['pos_push_event'] ), true );

// 4) a pull before the push runs must not overwrite the fresh sale
Palitra_Ozon_Sync::pull( true );
check( 'guard keeps site sale', $PRODUCTS[1]->qty, 2 );

// 5) push sends stock 2 to Ozon warehouse 777
Palitra_Ozon_Sync::push();
$last = end( $API_CALLS );
check( 'push payload', $last[1]['stocks'], array( array( 'offer_id' => 'Unison Botanical 18', 'stock' => 2, 'warehouse_id' => 777 ) ) );
check( 'queue emptied', get_option( 'pos_push_queue' ), array() );
check( 'ozon updated', $OZON['Unison Botanical 18'][0], 2 );

// 6) within guard window, pull still skips product 1; Ozon sale of PanPastel reduces site stock
$OZON['PanPastel 010'] = array( 1, 0 );
Palitra_Ozon_Sync::pull( true );
check( 'ozon sale reaches site', $PRODUCTS[2]->qty, 1 );
check( 'recently pushed skipped', $PRODUCTS[1]->qty, 2 );

// 7) push disabled → no queue
$O['pos_settings']['push_enabled'] = 0;
$PRODUCTS[2]->set_stock_quantity( 0 );
check( 'push disabled', get_option( 'pos_push_queue' ), array() );

echo $fail ? "\n$fail FAILED\n" : "\nall passed\n"; exit( $fail ? 1 : 0 );
