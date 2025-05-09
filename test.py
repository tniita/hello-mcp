import json
import httpx

PLICE_LIST_URL = "https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/"

try:
    response = httpx.get(PLICE_LIST_URL, timeout=100)
    # items = json.loads(response)
    print(response.text)

    # 指定カテゴリのアイテムをフィルタリング
    target_item = next((item for item in items.get("items", [])
                        if item.get("serviceCategory") == "Exadata Exascale Infrastructure"), None)

    # JPY通貨のlocalizationを抽出
    jpy_localization = next((loc for loc in target_item.get("currencyCodeLocalizations", [])
                            if loc.get("currencyCode") == "JPY"), None)

    price_value = next((price.get("value") for price in jpy_localization.get("prices", [])
                        if price.get("model") == "PAY_AS_YOU_GO"), None)

    print(price_value)

except json.JSONDecodeError as e:
    print(f"JSONのパースエラー: {e}")
except Exception as e:
    print(f"エラーが発生しました: {e}")
