# OCI Price List MCP Server

## 概要

このプロジェクトは、Oracle Cloud Infrastructure (OCI) の価格情報を取得するための MCP (Model Context Protocol) サーバーです。FastMCPを使用して実装されており、OCIサービスの価格を日本円（JPY）で取得することができます。

## 主な機能

- **OCI価格取得ツール**: OCIサービスの価格リストAPIから、指定されたサービス名とメトリクス名に基づいて価格情報を取得
- **日本円対応**: 価格は日本円（JPY）で表示
- **従量課金（PAYG）価格**: Pay-As-You-Goモデルの価格を取得

## 技術スタック

- **Python 3.x**
- **FastMCP**: MCPサーバーの実装フレームワーク
- **httpx**: HTTP通信ライブラリ
- **MCP (Model Context Protocol)**: AI/LLMとの統合のためのプロトコル

## セットアップ

### 必要要件

- Python 3.x
- pip

### インストール

1. リポジトリをクローン:
```bash
git clone https://github.com/tniita/hello-mcp.git
cd hello-mcp
```

2. 依存関係をインストール:
```bash
pip install -r requirements.txt
```

## 使用方法

### MCPサーバーの起動

```bash
python main.py
```

サーバーは標準入出力（stdio）を使用して通信します。

### get_price_list ツールの使用

このツールは以下のパラメータを受け取ります：

- **service_name**: OCIのサービス名
  - 例: `Cloud Infrastructure Kubernetes Engine (OKE)`, `Autonomous Database`, `OCI Streaming`
  - 注意: "OCI", "Oracle Cloud Infrastructure", "Cloud Infrastructure"などのバリエーションが存在します

- **metrics_name**: OCIのメトリクス名
  - 例: `Virtual Node`, `Gigabytes of Data Transferred`
  - 注意: "xx per hour"や"xx per GB"などのバリエーションが存在します

### テストスクリプト

`test.py`を実行して、APIの動作を確認できます：

```bash
python test.py
```

このスクリプトは、OKE（Kubernetes Engine）のVirtual Nodeの価格を取得する例を示しています。

## プロジェクト構成

```
hello-mcp/
├── main.py              # MCPサーバーのメインファイル
├── test.py              # テスト用スクリプト
├── requirements.txt     # Python依存関係
├── README.md            # このファイル
├── renovate.json        # Renovate設定
└── azure-pipelines.yml  # Azure Pipelines設定
```

## API仕様

### データソース

Oracle Cloud Infrastructure の価格リストAPI:
```
https://apexapps.oracle.com/pls/apex/cetools/api/v1/products/
```

### レスポンス形式

- 価格が見つかった場合: `float` 型の価格値（日本円）
- 価格が見つからない場合: `0.0`
- エラーが発生した場合: `0.0`

## エラーハンドリング

- JSONパースエラー: エラーメッセージを出力し、`0.0`を返す
- 一般的な例外: エラーメッセージを出力し、`0.0`を返す
- サービスが見つからない場合: `0.0`を返す
- JPY通貨が見つからない場合: `0.0`を返す

## ライセンス

このプロジェクトのライセンス情報については、リポジトリの管理者にお問い合わせください。

## 貢献

プルリクエストやイシューの報告を歓迎します。

## 関連リンク

- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Oracle Cloud Infrastructure](https://www.oracle.com/cloud/)
