export BASEPATH=$(pwd)
export MODERNWARFAREREPO=$BASEPATH/mw3
export SEARCHPATH=$MODERNWARFAREREPO/main
export ZONEPATH=$MODERNWARFAREREPO/zone/english
export EXTRAASSETPATH1=$BASEPATH/zone_raw/patch_ACT1
export EXTRAASSETPATH2=$BASEPATH/zone_raw/patch_ACT2
export EXTRAASSETPATH3=$BASEPATH/zone_raw/patch_ACT3
# Build all patch files with extra asset search paths
# Before running this script, make sure to clone the zone_raw/patch to zone_raw/patch_ACT{1,2,3}.
# YOU MUST RUN UNLINKER FIRST TO CREATE "zone_dump/" and then copy "zone_dump/zone_raw/" contents into "zone_dump/"


./Linker -v   --load $ZONEPATH/patch.ff   --base-folder "$(pwd)"     --output-folder "./zone_out"   patch_ACT1 --add-asset-search-path $EXTRAASSETPATH1
./Linker -v   --load $ZONEPATH/patch.ff   --base-folder "$(pwd)"     --output-folder "./zone_out"   patch_ACT2 --add-asset-search-path $EXTRAASSETPATH2
./Linker -v   --load $ZONEPATH/patch.ff   --base-folder "$(pwd)"     --output-folder "./zone_out"   patch_ACT3 --add-asset-search-path $EXTRAASSETPATH3