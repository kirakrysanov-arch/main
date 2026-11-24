<?php
/**
 * Pure helpers (no WordPress calls) — easy to test in isolation.
 *
 * @package palitra-ozon-sync
 */

defined( 'ABSPATH' ) || exit;

final class POS_Logic {

	/**
	 * /v4/product/info/stocks items → offer_id => available FBS stock (present − reserved, never below 0).
	 * Accepts both the current shape (stocks[].type = "fbs"/"fbo"/…) and entries without a type.
	 *
	 * @param array $items
	 * @return array<string,int>
	 */
	public static function parse_stocks( array $items ) {
		$out = array();
		foreach ( $items as $it ) {
			if ( empty( $it['offer_id'] ) ) {
				continue;
			}
			$sum   = 0;
			$found = false;
			foreach ( (array) ( $it['stocks'] ?? array() ) as $st ) {
				$type = strtolower( (string) ( $st['type'] ?? 'fbs' ) );
				if ( 'fbs' !== $type && 'rfbs' !== $type ) {
					continue; // FBO stock lives in Ozon's warehouses — not ours to sell from the site.
				}
				$found = true;
				$sum  += max( 0, (int) ( $st['present'] ?? 0 ) - (int) ( $st['reserved'] ?? 0 ) );
			}
			$out[ (string) $it['offer_id'] ] = $found ? $sum : 0;
		}
		return $out;
	}

	/**
	 * Rows [offer_id, stock] → batches of ≤100 for /v2/products/stocks.
	 *
	 * @param array      $rows         each: ['offer_id' => string, 'stock' => int]
	 * @param int|string $warehouse_id
	 * @return array<int, array<int, array>>
	 */
	public static function build_push_batches( array $rows, $warehouse_id ) {
		$items = array();
		$seen  = array();
		foreach ( $rows as $r ) {
			$offer = (string) ( $r['offer_id'] ?? '' );
			if ( '' === $offer || isset( $seen[ $offer ] ) ) {
				continue;
			}
			$seen[ $offer ] = true;
			$items[]        = array(
				'offer_id'     => $offer,
				'stock'        => max( 0, (int) $r['stock'] ),
				'warehouse_id' => (int) $warehouse_id,
			);
		}
		return array_chunk( $items, 100 );
	}

	/**
	 * /v2/products/stocks response → offer_id => ['ok' => bool, 'stock' => int, 'error' => string].
	 */
	public static function parse_push_result( $data ) {
		$out = array();
		foreach ( (array) ( $data['result'] ?? array() ) as $r ) {
			$offer = (string) ( $r['offer_id'] ?? '' );
			if ( '' === $offer ) {
				continue;
			}
			$errors = array();
			foreach ( (array) ( $r['errors'] ?? array() ) as $e ) {
				$errors[] = trim( ( $e['code'] ?? '' ) . ' ' . ( $e['message'] ?? '' ) );
			}
			$out[ $offer ] = array(
				'ok'    => ! empty( $r['updated'] ) && ! $errors,
				'stock' => (int) ( $r['stock'] ?? 0 ),
				'error' => $errors ? implode( '; ', $errors ) : ( empty( $r['updated'] ) ? 'не обновлено' : '' ),
			);
		}
		return $out;
	}

	/** /v1/warehouse/list → [['id' => int, 'name' => string]] */
	public static function parse_warehouses( $data ) {
		$out = array();
		foreach ( (array) ( $data['result'] ?? array() ) as $w ) {
			if ( isset( $w['warehouse_id'] ) ) {
				$out[] = array(
					'id'   => (string) $w['warehouse_id'],
					'name' => (string) ( $w['name'] ?? ( 'Склад ' . $w['warehouse_id'] ) ),
				);
			}
		}
		return $out;
	}
}
