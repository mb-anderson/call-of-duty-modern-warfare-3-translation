export BASEPATH=$(pwd)
export MODERNWARFAREREPO=$BASEPATH/mw3
export SEARCHPATH=$MODERNWARFAREREPO/main
export ZONEPATH=$MODERNWARFAREREPO/zone/english
# Unlink all .ff files in the zone folder
# The output will be in zone_dump/zone_raw/
# I did all ff files because some ff files depend on others, so it's better to have them all unlinked.
# It was development code for find independent assets, but it can be useful for modders to have all ff files unlinked at once.
# I found patch.ff file, that file can disassemble with Unlinker and can able do some modifications, then can compile with Linker.sh script.
# So we are using patch.ff for translations.

for file in "$ZONEPATH"/*.ff; do
    echo "START------------------\n" >> unlinkersh.log
    echo "$file" >> unlinkersh.log
    ./Unlinker "$file" --search-path "$SEARCHPATH" >> unlinkersh.log 2>&1
    echo "END------------------\n\n" >> unlinkersh.log
done

#./Unlinker $ZONEPATH/berlin.ff --search-path $SEARCHPATH --include-assets localize
