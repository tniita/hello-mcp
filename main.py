import httpx
from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("OCI Price List")

PLICE_LIST_URL = "https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/"


@mcp.tool()
def get_price_list(service_name: str) -> float:
    """
    Get the OCI service price with JPY of PAYG by OCI Service Name.

    Args:
    service_name: OCI Service Name
    """

    try:
        # OCIの価格リストを取得
        response = httpx.get(PLICE_LIST_URL, timeout=100)
        if response.status_code == 200:
            items = json.loads(response.text)

        # 指定カテゴリのアイテムをフィルタリング
        target_item = next((item for item in items.get("items", [])
                            if item.get("serviceCategory") == service_name), None)

        if not target_item:
            return 0.0

        # JPY通貨のlocalizationを抽出
        jpy_localization = next((loc for loc in target_item.get("currencyCodeLocalizations", [])
                                 if loc.get("currencyCode") == "JPY"), None)

        if not jpy_localization:
            return 0.0

        # 価格モデルがPAY_AS_YOU_GOの価格を取得
        price_value = next((price.get("value") for price in jpy_localization.get("prices", [])
                           if price.get("model") == "PAY_AS_YOU_GO"), None)

        return price_value

    except json.JSONDecodeError as e:
        print(f"JSONのパースエラー: {e}")
        return 0.0
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 0.0


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
