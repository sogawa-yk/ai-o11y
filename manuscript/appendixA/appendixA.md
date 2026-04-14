# 付録A クエリ言語チートシート

第17章までで本編は完結した。付録A〜Cは実務中に引ける早見表である。本付録はPromQL／TraceQL／LogQLの代表的な逆引きパターンと、コーディングエージェントへの指示テンプレートをまとめる。クエリ言語の文法網羅が目的ではなく、「やりたいこと→書き方」の対応を即座に引けるようにすることを目的とする。

## A.1 PromQL逆引き

*表A.1: PromQLパターン逆引き。`$service` はGrafanaテンプレート変数想定、時間窓は `[5m]` が基本*

| やりたいこと | PromQL例 |
|------------|---------|
| リクエスト数の毎秒レート | `sum(rate(travel_helper_requests_total{job=~"$service"}[5m]))` |
| エンドポイント別のp95レイテンシ | `histogram_quantile(0.95, sum by (le, endpoint) (rate(travel_helper_request_duration_milliseconds_bucket{job=~"$service"}[5m])))` |
| エラー率（errors/requests） | `sum(rate(travel_helper_errors_total[5m])) / clamp_min(sum(rate(travel_helper_requests_total[5m])), 1)` |
| ツール別エラー合計 | `sum by (tool) (rate(travel_helper_tool_errors_total[5m]))` |
| 単調増加Counterの時刻あたり増分 | `rate(travel_helper_requests_total[5m])` |
| パーセンタイル（p50/p95/p99） | `histogram_quantile(0.50|0.95|0.99, sum by (le) (rate(<metric>_bucket[5m])))` |
| ラベルによる絞り込み | `<metric>{label="value", otherLabel=~"regex.*"}` |
| ラベルで合算／分割 | `sum by (<label>) (<expr>)` ／ `sum without (<label>) (<expr>)` |
| 最大値／最小値 | `max_over_time(<metric>[1h])` ／ `min_over_time(<metric>[1h])` |
| 急増検知（直近10分 vs 過去1時間） | `rate(<metric>[10m]) / rate(<metric>[1h]) > 2` |
| ゼロ除算回避 | 分母に `clamp_min(..., 1)` |

Counter名は Prometheus側では `_total` サフィックス、Histogramは `_bucket` / `_sum` / `_count` サフィックスが自動付与される。unit指定がある場合は `_seconds_bucket` / `_milliseconds_bucket` のように単位サフィックスも付く（実環境で確認する）。

## A.2 TraceQL逆引き

*表A.2: TraceQLパターン逆引き。`{ ... }` はspan matcher、複数条件は `&&` で結合*

| やりたいこと | TraceQL例 |
|------------|----------|
| 特定サービスの直近トレース | `{ service.name="travel-helper-ch13" }` |
| 特定Span名のトレース | `{ name="stage.plan" }` |
| 所要時間が閾値を超えるspan | `{ service.name="travel-helper-ch13" && duration > 500ms }` |
| エラーステータスのspan | `{ service.name="travel-helper-ch13" && status=error }` |
| 複数条件（AND）の組み合わせ | `{ service.name="travel-helper-ch13" && status=error && name =~ "stage.*" }` |
| 属性による絞り込み | `{ gen_ai.request.model="xai.grok-3" }` |
| span属性の正規表現 | `{ name =~ "tool\\..*" }` |
| トレース全体の所要時間で絞る | `{ trace:duration > 2s }` |
| 結果件数制限 | 末尾に `\| limit(20)` |
| 特定Trace IDを直接開く | Grafana Explore検索窓にTrace IDを直接入力 |

ソートはTraceQL単独では汎用的な構文がないため、GrafanaのTracesテーブル列ヘッダ（Duration等）でクリックして並び替える運用が現実的。

## A.3 LogQL逆引き

*表A.3: LogQLパターン逆引き。ラベル絞り込み→フィルタ／パーサー→集計、の3段構造が基本*

| やりたいこと | LogQL例 |
|------------|--------|
| サービス名でログ絞り込み | `{service_name="travel-helper-ch13"}` |
| 複数ラベルで絞り込み | `{service_name="...", level="ERROR"}` |
| 単純文字列フィルタ | `{service_name="..."} |= "ERROR"` |
| 正規表現フィルタ | `{service_name="..."} |~ "decided items=\\d+"` |
| 除外フィルタ | `{service_name="..."} != "healthz"` |
| JSON属性でフィルタ | `{service_name="..."} | json | trace_id="abc123..."` |
| logfmtで属性解析 | `{...} | logfmt | level="error"` |
| ログ件数レート | `sum by (service_name) (rate({service_name=~".+"}[5m]))` |
| 特定文字列の発生頻度 | `rate({...} |= "timeout" [5m])` |
| trace_idに紐付くログ | `{service_name="..."} | json | trace_id="<hex>"` |
| 時間範囲指定 | Grafanaの time picker またはAPI引数で制御 |

OTel Logsが `| json` パイプで `trace_id` / `span_id` / `severity_text` 等の構造化属性として現れるのがポイント。

## A.4 コーディングエージェントへの指示テンプレート

*表A.4: Grafanaクエリ／ダッシュボード作成をエージェントに依頼する際の指示テンプレート*

| 依頼したいこと | 指示テンプレート |
|--------------|----------------|
| 時系列グラフ作成 | 「`<サービス>` の `<メトリクス名>` を過去 `<時間>`、`<窓>` のローリング窓でrps時系列グラフにするPromQLを書いて」 |
| パーセンタイル | 「`<サービス>` の `<Histogram名>` のp`<値>`を `<時間>` で描画するPromQLを書いて」 |
| エラー率 | 「`<サービス>` のエラー率（errors/requests）を過去 `<時間>` で描画するPromQLを書いて」 |
| Histogramのヒートマップ | 「`<サービス>` の `<Histogram名>` を時間軸 vs レイテンシ軸のヒートマップで描画するPromQLを書いて」 |
| トレース検索 | 「直近 `<時間>`、`<サービス>` でstatus=error、duration> `<閾値>` のトレースを TraceQL で絞り込んで」 |
| 特定Span名の絞り込み | 「`<サービス>` の `<Span名>` を含むトレース一覧を TraceQL で書いて」 |
| ログ→Trace横断 | 「trace_id=`<hex>` に紐付くログを時刻順で表示するLogQLを書いて」 |
| ログ発生頻度 | 「`<サービス>` のERROR発生頻度を5分窓で時系列表示するLogQLを書いて」 |
| ダッシュボード生成 | 「`<サービス>` について rps / p95 latency / error rate / recent traces の4パネル構成のGrafanaダッシュボードJSONを生成して」 |
| アラート作成 | 「`<メトリクス>` が5分間 `<閾値>` を超えたらアラートを発火するPrometheus Alerting Ruleを書いて」 |

指示に含める最小情報は次の4点である。(1) 時間範囲、(2) 対象ラベル（service name／endpoint等）、(3) 集計単位（1m／5m等の窓）、(4) 可視化形式（時系列／表／ヒートマップ等）。この4点が揃えば、エージェントは正しいクエリを生成できる。

---

次の付録Bでは、本書で扱ったOTel Python SDKの主要APIを早見表として集約する。
