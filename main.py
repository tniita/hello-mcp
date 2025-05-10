import httpx
from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("OCI Price List")

PRICE_LIST = "https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/"


@mcp.tool()
def get_price_list(service_name: str, metrics_name: str) -> float:
    """
    Get the OCI service price with JPY of PAYG by OCI Service Name and metrics name.

    Args:
    service_name: OCI Service Name
    metrics_name: OCI Service Name of Billing Metrics
    """

    try:
        # OCIの価格リストを取得
        response = httpx.get(PRICE_LIST, timeout=100)
        if response.status_code == 200:
            items = json.loads(response.text)

        service_items = items.get("items", [])
        for item in service_items:
            if service_name in item.get("serviceCategory", "") and metrics_name.title() in item.get("metricName", ""):
                target_item = item
                break

        if not target_item:
            return 0.0

        # JPY通貨のlocalizationを抽出
        if not (jpy_localization := next((loc for loc in target_item.get("currencyCodeLocalizations", [])
                                          if loc.get("currencyCode") == "JPY"), None)):
            return 0.0

        # 価格モデルがPAY_AS_YOU_GOの価格を取得
        return next((price.get("value") for price in jpy_localization.get("prices", [])
                    if price.get("model") == "PAY_AS_YOU_GO"), None)

    except json.JSONDecodeError as e:
        print(f"JSONのパースエラー: {e}")
        return 0.0
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return 0.0


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
