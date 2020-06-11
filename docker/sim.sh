cd /bridge-sim

# Verification.
./scripts/cli.sh --two-materials --save-to $HOME/gen-data --msl 0.5 verify point-loads
./scripts/cli.sh --two-materials --save-to $HOME/gen-data --msl 0.5 verify pier-settlement
./scripts/cli.sh --two-materials --save-to $HOME/gen-data --msl 0.5 verify temp-loads
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 verify shrinkage
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 verify creep
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 verify temp-effect
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 --parallel 14 verify uls
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 --parallel 14 verify ulm
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 verify strain
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 verify traffic
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 verify responses

# Validation.
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 --parallel 14 validate dynamic
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 --parallel 14 validate r2
# ./scripts/cli.sh --parallel 14 --shorten-paths --save-to $HOME/gen-data --msl 0.5 validate inflines --strain-sensors O
# ./scripts/cli.sh --parallel 14 --shorten-paths --save-to $HOME/gen-data --msl 0.5 validate inflines --strain-sensors T

# Thesis.
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 thesis temp-profile
./scripts/cli.sh --save-to $HOME/gen-data --msl 0.5 thesis temp-contour
