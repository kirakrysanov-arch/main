# ApiShip for WooCommerce — Palitra patch

Base: official ApiShip WooCommerce module 1.8.0 (https://github.com/apiship/woocommerce-module, GPL-3.0).

Changes (`palitra-apiship.patch`):
1. Cash on delivery only for the «cod» payment method — Ozon Pay orders are prepaid (calculator + order creation).
2. Pickup-point map (coordinates from DaData, Yandex geocoder as fallback): centres on the customer's street, marks «Ваш адрес», zooms to the 3 nearest points and opens the nearest one; adds a street search box; pickup markers in the shop colour.
3. Version 1.8.0.3 so browsers load the new map script.

`wpapiship-map.min.js` is a copy of the patched `wpapiship-map.js`.
Do not update the plugin from WordPress without re-applying this patch.
