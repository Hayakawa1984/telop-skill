# telop — Claude Code テロップスキル

Claude Codeに「テロップつけて」と言うだけで動画に日本語テロップを自動付与するスキルです。

## できること

- 🎙️ **AI文字起こし** — OpenAI Whisper（mediumモデル）で高精度な日本語音声認識
- ✂️ **自動分割** — 画面に入りきらない長いセリフを自然な位置（助詞・読点）で自動分割
- 👀 **確認ステップ** — SRTファイルをデスクトップに保存し、焼き込み前に編集・確認できる
- 🎬 **字幕焼き込み** — 白文字＋黒縁取りでくっきり読めるテロップを動画に直接焼き込み
- ✂️ **末尾カット** — 最後の字幕が終わった時点で動画をトリム（黒画面を自動削除）

## 使い方

セットアップ後、Claude Codeで：

```
@動画ファイル.mp4 テロップつけて
```

または

```
テロップつけて
```

と言うだけ。あとはClaudeが全部やってくれます。

## セットアップ

### 1. 必要パッケージをインストール

```bash
pip3 install openai-whisper imageio-ffmpeg
```

> **初回実行時**にWhisperのmediumモデル（約1.4GB）が自動ダウンロードされます。

### 2. スキルをインストール

```bash
# リポジトリをクローン
git clone https://github.com/YOUR_USERNAME/telop-skill.git

# スキルフォルダにコピー
cp -r telop-skill/telop ~/.claude/skills/telop
```

### 3. Claude Codeを再起動

スキルが認識されます。

## ファイル構成

```
telop/
├── SKILL.md              # スキル本体（Claudeへの指示書）
└── scripts/
    ├── transcribe.py     # Whisper文字起こし＆SRT生成
    └── burn_subtitles.py # ffmpegで字幕焼き込み＆トリム
```

## 動作フロー

```
① 動画ファイルを指定
  ↓
② Whisperで文字起こし → SRTファイル生成（長い行は自動分割）
  ↓
③ SRTをデスクトップに保存 → あなたが確認・修正
  ↓
④「OK」と返信
  ↓
⑤ テロップ焼き込み＋末尾の黒画面カット
  ↓
⑥ {元ファイル名}_final.mp4 完成
```

## カスタマイズ

### フォントサイズ・スタイルを変える

`scripts/burn_subtitles.py` の `STYLE` 変数を編集：

```python
STYLE = "FontName=Hiragino Sans,FontSize=22,..."
```

| パラメータ | 説明 |
|-----------|------|
| `FontName` | フォント名（例: `Arial`、`Noto Sans JP`） |
| `FontSize` | 文字サイズ（デフォルト: 22） |
| `PrimaryColour` | 文字色（BBGGRR形式、白=`&H00FFFFFF`） |
| `Outline` | 縁取りの太さ（デフォルト: 2） |
| `MarginV` | 下からの余白（デフォルト: 30） |

### 1行の最大文字数を変える

`scripts/transcribe.py` の `main()` 内：

```python
max_chars = int(sys.argv[3]) if len(sys.argv) > 3 else 25  # ← ここを変更
```

## 動作環境

- macOS（Apple Silicon / Intel どちらも対応）
- Python 3.9以上
- Claude Code

> **Windows・Linuxについて**: `imageio-ffmpeg` はWindows/Linuxにも対応していますが、フォント（`Hiragino Sans`はmacOS専用）の変更が必要です。

## ライセンス

MIT
