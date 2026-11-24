<?php
// Run: php tests/test-logic.php
define( 'ABSPATH', __DIR__ );
require __DIR__ . '/../includes/class-pos-logic.php';
$fail = 0;
function check( $name, $got, $want ) {
	global $fail;
	if ( $got === $want ) { echo "ok   $name\n"; } else { $fail++; echo "FAIL $name\n  got:  " . var_export( $got, true ) . "\n  want: " . var_export( $want, true ) . "\n"; }
}

// v4 stocks: FBS counted (present − reserved), FBO ignored, never negative, no stocks → 0
$items = array(
	array( 'offer_id' => 'Unison Botanical 18', 'product_id' => 1, 'stocks' => array(
		array( 'type' => 'fbo', 'present' => 7, 'reserved' => 0 ),
		array( 'type' => 'fbs', 'present' => 5, 'reserved' => 2 ),
	) ),
	array( 'offer_id' => 'PanPastel 010', 'stocks' => array( array( 'type' => 'fbs', 'present' => 1, 'reserved' => 3 ) ) ),
	array( 'offer_id' => 'J. Luda Blue 12', 'stocks' => array() ),
	array( 'offer_id' => 'Two FBS', 'stocks' => array( array( 'type' => 'fbs', 'present' => 2, 'reserved' => 0 ), array( 'type' => 'rfbs', 'present' => 3, 'reserved' => 1 ) ) ),
	array( 'product_id' => 9, 'stocks' => array() ), // no offer_id → skipped
);
check( 'parse_stocks', POS_Logic::parse_stocks( $items ), array( 'Unison Botanical 18' => 3, 'PanPastel 010' => 0, 'J. Luda Blue 12' => 0, 'Two FBS' => 4 ) );

// push batches: ≤100 per batch, no duplicates, no negative stock, warehouse as int
$rows = array();
for ( $i = 0; $i < 205; $i++ ) { $rows[] = array( 'offer_id' => "SKU $i", 'stock' => $i - 1 ); }
$rows[] = array( 'offer_id' => 'SKU 5', 'stock' => 99 ); // duplicate
$b = POS_Logic::build_push_batches( $rows, '22000123' );
check( 'batches count', count( $b ), 3 );
check( 'batch sizes', array_map( 'count', $b ), array( 100, 100, 5 ) );
check( 'first item', $b[0][0], array( 'offer_id' => 'SKU 0', 'stock' => 0, 'warehouse_id' => 22000123 ) );
check( 'dup ignored', $b[0][5]['stock'], 4 );

// push result
$res = POS_Logic::parse_push_result( array( 'result' => array(
	array( 'offer_id' => 'A', 'updated' => true, 'errors' => array() ),
	array( 'offer_id' => 'B', 'updated' => false, 'errors' => array( array( 'code' => 'TOO_MANY_REQUESTS', 'message' => 'wait' ) ) ),
	array( 'offer_id' => 'C', 'updated' => false, 'errors' => array() ),
) ) );
check( 'push A ok', $res['A']['ok'], true );
check( 'push B error', $res['B']['error'], 'TOO_MANY_REQUESTS wait' );
check( 'push C not updated', $res['C']['ok'] . '|' . $res['C']['error'], '|не обновлено' );

// warehouses
check( 'warehouses', POS_Logic::parse_warehouses( array( 'result' => array( array( 'warehouse_id' => 1020000123, 'name' => 'Склад Москва FBS' ), array( 'name' => 'no id' ) ) ) ), array( array( 'id' => '1020000123', 'name' => 'Склад Москва FBS' ) ) );

echo $fail ? "\n$fail FAILED\n" : "\nall passed\n";
exit( $fail ? 1 : 0 );
