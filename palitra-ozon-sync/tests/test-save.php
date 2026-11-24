<?php
// Simulates: fill Client-Id + API key, click «Сохранить и проверить подключение».
define( 'ABSPATH', __DIR__ ); define( 'MINUTE_IN_SECONDS', 60 ); define( 'HOUR_IN_SECONDS', 3600 ); define( 'DAY_IN_SECONDS', 86400 );
$O = array(); $T = array(); $CRON = array(); $REDIRECT = '';
function get_option( $k, $d = false ) { global $O; return $O[ $k ] ?? $d; }
function update_option( $k, $v, $a = null ) { global $O; $O[ $k ] = $v; return true; }
function get_transient( $k ) { global $T; return $T[ $k ] ?? false; } function set_transient( $k, $v, $e ) { global $T; $T[ $k ] = $v; } function delete_transient( $k ) { global $T; unset( $T[ $k ] ); }
function wp_next_scheduled( $h ) { global $CRON; return $CRON[ $h ] ?? false; } function wp_schedule_event( $t, $r, $h ) { global $CRON; $CRON[ $h ] = $t; } function wp_clear_scheduled_hook( $h ) { global $CRON; unset( $CRON[ $h ] ); }
function add_action( ...$a ) {} function add_filter( ...$a ) {} function register_activation_hook( ...$a ) {} function register_deactivation_hook( ...$a ) {} function plugin_basename( $f ) { return 'x'; }
function current_user_can( $c ) { return true; } function check_admin_referer( $a ) { return true; } function wp_unslash( $x ) { return $x; }
function sanitize_text_field( $s ) { return trim( strip_tags( (string) $s ) ); } function sanitize_key( $s ) { return preg_replace( '/[^a-z0-9_\-]/', '', strtolower( (string) $s ) ); }
function admin_url( $p ) { return '/wp-admin/' . $p; } function wp_list_pluck( $a, $k ) { return array_column( $a, $k ); }
class StopRedirect extends Exception {} function wp_safe_redirect( $u ) { global $REDIRECT; $REDIRECT = $u; throw new StopRedirect(); }
function is_wp_error( $x ) { return $x instanceof WP_Error; } class WP_Error { private $m; function __construct( $c, $m ) { $this->m = $m; } function get_error_message() { return $this->m; } }
function wp_json_encode( $x ) { return json_encode( $x ); }
$SENT_HEADERS = array();
function wp_remote_post( $url, $args ) { global $SENT_HEADERS; $SENT_HEADERS = $args['headers'];
	return array( 'code' => 200, 'body' => json_encode( array( 'result' => array( array( 'warehouse_id' => 1020000555, 'name' => 'Мой склад FBS' ) ) ) ) ); }
function wp_remote_retrieve_response_code( $r ) { return $r['code']; } function wp_remote_retrieve_body( $r ) { return $r['body']; }
require __DIR__ . '/../palitra-ozon-sync.php';
$fail = 0; function check( $n, $g, $w ) { global $fail; if ( $g === $w ) echo "ok   $n\n"; else { $fail++; echo "FAIL $n\n  got:  " . var_export( $g, true ) . "\n  want: " . var_export( $w, true ) . "\n"; } }

$_POST = array( 'client_id' => ' 123456 ', 'api_key' => 'abc-key', 'warehouse_id' => '', 'interval' => '15', 'dry_run' => '1', 'pull_enabled' => '1', 'push_enabled' => '1', 'then' => 'test' );
try { Palitra_Ozon_Sync::handle_save(); } catch ( StopRedirect $e ) {}
$s = Palitra_Ozon_Sync::settings();
check( 'client id saved', $s['client_id'], '123456' );
check( 'key saved', $s['api_key'], 'abc-key' );
check( 'headers sent to Ozon', $SENT_HEADERS['Client-Id'] . '|' . $SENT_HEADERS['Api-Key'], '123456|abc-key' );
check( 'warehouses cached', get_transient( 'pos_warehouses' ), array( array( 'id' => '1020000555', 'name' => 'Мой склад FBS' ) ) );
check( 'redirect shows ok', (bool) strpos( $REDIRECT, 'done=ok' ), true );

// Saving again with the key field left empty keeps the stored key
$_POST['api_key'] = ''; $_POST['then'] = ''; $_POST['warehouse_id'] = '1020000555';
try { Palitra_Ozon_Sync::handle_save(); } catch ( StopRedirect $e ) {}
$s = Palitra_Ozon_Sync::settings();
check( 'empty key keeps old', $s['api_key'], 'abc-key' );
check( 'warehouse saved', $s['warehouse_id'], '1020000555' );
check( 'pull scheduled', isset( $CRON['pos_pull_event'] ), true );
echo $fail ? "\n$fail FAILED\n" : "\nall passed\n"; exit( $fail ? 1 : 0 );
