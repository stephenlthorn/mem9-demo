# recordings/

Holds `demo.mp4`, the MP4 fallback played by `./demo.sh --replay` when conference wifi is hostile.

`.mp4` files are gitignored. Re-record locally per the runbook.

## How to record

1. Run `./demo.sh` live end-to-end once, confirm all three screens are healthy.
2. On macOS, `cmd+shift+5` → "Record Selected Portion" → capture the full booth dashboard window.
3. Save as `recordings/demo.mp4`.
4. Verify with `./demo.sh --replay`.
