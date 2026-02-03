# 就業規則RAGチャットボット (Local RAG Project)

本プロジェクトは、市区町村の公開データ（例規集）をソースとし、完全ローカル環境で動作する就業規則回答チャットボットを構築するプロジェクトです。

## 1. プロジェクト概要
RAG（Retrieval-Augmented Generation）の一連のプロセス（データ収集・前処理・ベクトル化・推論・評価）を、シングルホスト（HP Z620）上で完結させることを目的としています。

- **ターゲット:** 山口県熊毛郡上関町、大阪府豊中市 等の例規データ
- **主な技術:** Dify, Ollama, SLM (Gemma-2, Llama-3), Python

## 2. システム構成
[Image of RAG system architecture with Dify and Ollama on a single server]

- **Hardware:** HP Z620 (RAM: 64GB)
- **Engine:** [Ollama](https://ollama.com/) (SLM Inference)
- **Orchestration:** [Dify](https://dify.ai/) (Docker Compose)
- **Language:** Python 3.10+

## 3. フォルダ構成
```text
.
├── docker/                 # DifyおよびOllamaの実行環境（docker-compose）
├── src/                    # Pythonソースコード
│   ├── scraper/            # 自治体サイトからのHTML抽出
│   ├── processor/          # Markdown変換およびチャンク最適化
│   └── utils/              # 共通ユーティリティ
├── data/                   # ローカルデータ（.gitignore対象）
│   ├── raw/                # 取得した生データ
│   └── processed/          # Dify投入用Markdown
├── docs/                   # 要件定義書・設計書
├── tests/                  # 30件の正解データによる精度評価
└── README.md               # 本ドキュメント