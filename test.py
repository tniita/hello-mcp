import json
import httpx

PRICE_LIST = "https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/"

try:
    # OCIの価格リストを取得
    response = httpx.get(PRICE_LIST, timeout=100)
    if response.status_code == 200:
        items = json.loads(response.text)

    service_items = items.get("items", [])
    target_item = None
    for item in service_items:
        if "Cloud Infrastructure Kubernetes Engine (OKE)" in item.get("serviceCategory", "") and "Virtual Node".title() in item.get("metricName", ""):
            target_item = item
            break

    if target_item is None:
        print("nothing")

    # JPY通貨のlocalizationを抽出
    if (jpy_localization := next((loc for loc in target_item.get("currencyCodeLocalizations", [])
                                  if loc.get("currencyCode") == "JPY"), None)):

        # 価格モデルがPAY_AS_YOU_GOの価格を取得
        print(next((price.get("value") for price in jpy_localization.get("prices", [])
                    if price.get("model") == "PAY_AS_YOU_GO"), None))

except json.JSONDecodeError as e:
    print(f"JSONのパースエラー: {e}")
except Exception as e:
    print(f"エラーが発生しました: {e}")
