#!/opt/homebrew/bin/fish

set TEMP_DIR $(mktemp -d)
echo using the dir $TEMP_DIR
anki-cli-unofficial load --anki-dir "/Users/jesssmith/Library/Application Support/anki2/User 1" --deck "Computer Science" cards.yaml  $TEMP_DIR/archive.apkg
