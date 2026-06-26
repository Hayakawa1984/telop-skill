---
name: telop
description: 動画ファイルにテロップ（字幕）を自動でつけるスキル。Whisperで音声を文字起こしし、長い行を自然な位置で分割してSRTファイルを生成。ユーザーが確認・修正できるよう一時停止し、OKが出たらテロップを焼き込んで末尾の黒画面をカットした最終動画を出力する。ユーザーが「テロップつけて」「字幕をつけて」「テロップ」「/telop」と言ったとき、または動画ファイルに字幕・テロップを追加したいと言ったときは必ずこのスキルを使うこと。
---

# テロップ付け スキル

動画に日本語テロップを自動付与する。Whisper文字起こし → SRT確認 → 字幕焼き込み → 末尾トリムの順で進む。

## ステップ1: 動画ファイルの特定

ユーザーが動画ファイルを @メンション または説明していれば、そのパスを使う。不明な場合はデスクトップで `.mp4` `.mov` `.m4v` を探して確認する。

```bash
ls ~/Desktop/*.mp4 ~/Desktop/*.mov ~/Desktop/*.m4v 2>/dev/null
```

## ステップ2: Whisperで文字起こし＆SRT生成

```bash
SKILL_DIR=$(python3 -c "import pathlib; print(pathlib.Path('~/.claude/skills/telop').expanduser())")
VIDEONAME=$(basename "{video_path}" | sed 's/\.[^.]*$//')
SRT_PATH="$HOME/Desktop/${VIDEONAME}_subtitles.srt"

python3 "${SKILL_DIR}/scripts/transcribe.py" \
  "{video_path}" \
  "${SRT_PATH}"
```

- `{video_path}` は実際のファイルパスに置き換える
- 出力SRTは `~/Desktop/{動画名}_subtitles.srt` に保存される
- 25文字を超える行は自動的に自然な位置で2行に分割される

## ステップ3: ユーザーへ確認依頼

スクリプトが完了したら、ユーザーにこう伝える：

> `{動画名}_subtitles.srt` をデスクトップに保存したで。テキストエディタで開いて内容を確認・修正してな。問題なければ「OK」と言ってくれたら字幕を焼き込むけん！

**ここで必ず止まってユーザーの返答を待つこと。**

## ステップ4: 字幕焼き込み＆末尾トリム

ユーザーが「OK」「大丈夫」「いいよ」などの確認を返したら実行する。

```bash
SKILL_DIR=$(python3 -c "import pathlib; print(pathlib.Path('~/.claude/skills/telop').expanduser())")
VIDEONAME=$(basename "{video_path}" | sed 's/\.[^.]*$//')
SRT_PATH="$HOME/Desktop/${VIDEONAME}_subtitles.srt"
OUTPUT_PATH="$HOME/Desktop/${VIDEONAME}_final.mp4"

python3 "${SKILL_DIR}/scripts/burn_subtitles.py" \
  "{video_path}" \
  "${SRT_PATH}" \
  "${OUTPUT_PATH}"
```

## ステップ5: 完了報告

完成したら出力ファイルパスとテロップ件数を伝える。
