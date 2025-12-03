export BASEPATH=$(pwd)
export MODERNWARFAREREPO=$BASEPATH/mw3
export SEARCHPATH=$MODERNWARFAREREPO/main
export ZONEPATH=$MODERNWARFAREREPO/zone/english
export EXTRAASSETPATH1=$BASEPATH/zone_raw/patch1
export EXTRAASSETPATH2=$BASEPATH/zone_raw/patch2
export EXTRAASSETPATH3=$BASEPATH/zone_raw/patch3
export EXTRAASSETPATH4=$BASEPATH/zone_raw/patch4
# Build all patch files with extra asset search paths
# Before running this script, make sure to edit the patch.ff, patch1.ff, patch2.ff, patch3.ff in zone_raw/ to include all STR files.
# YOU MUST RUN UNLINKER FIRST TO CREATE "zone_dump/" and then copy "zone_dump/zone_raw/" contents into "zone_dump/"



./Linker -v   --load $ZONEPATH/patch.ff   --base-folder "$(pwd)"     --output-folder "./zone_out"   patch --add-asset-search-path $EXTRAASSETPATH1
./Linker -v   --load $ZONEPATH/patch.ff   --base-folder "$(pwd)"     --output-folder "./zone_out"   patch1 --add-asset-search-path $EXTRAASSETPATH2
./Linker -v   --load $ZONEPATH/patch.ff   --base-folder "$(pwd)"     --output-folder "./zone_out"   patch2 --add-asset-search-path $EXTRAASSETPATH3
./Linker -v   --load $ZONEPATH/patch.ff   --base-folder "$(pwd)"     --output-folder "./zone_out"   patch3 --add-asset-search-path $EXTRAASSETPATH4
./Linker -v   --load $ZONEPATH/patch.ff   --base-folder "$(pwd)"     --output-folder "./zone_out"   patch4

