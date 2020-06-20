
./scripts/cli.sh --msl 10 --shorten-paths thesis crack-zones
./scripts/cli.sh --msl 10 --shorten-paths validate stress-top
./scripts/cli.sh --msl 10 verify crack

# Thesis.
./scripts/cli.sh --msl 10 thesis temp-profile
./scripts/cli.sh --msl 10 thesis temp-contour

# Verification.
./scripts/cli.sh --two-materials --msl 10 verify point-loads
./scripts/cli.sh --two-materials --msl 10 verify pier-settlement
./scripts/cli.sh --two-materials --msl 10 verify temp-loads
./scripts/cli.sh --two-materials --msl 10 verify self-weight
./scripts/cli.sh --msl 10 verify shrinkage
./scripts/cli.sh --msl 10 verify creep
./scripts/cli.sh --msl 10 verify temp-effect
./scripts/cli.sh --msl 10 --parallel 14 verify uls
./scripts/cli.sh --msl 10 --parallel 14 verify ulm
./scripts/cli.sh --msl 10 verify strain
./scripts/cli.sh --msl 10 verify responses
./scripts/cli.sh --msl 10 verify animate
./scripts/cli.sh --msl 10 verify animate-responses
./scripts/cli.sh --msl 10 verify linear-youngs
./scripts/cli.sh --msl 10 verify asphalt

# Validation.
./scripts/cli.sh --msl 10 --parallel 14 validate dynamic
./scripts/cli.sh --msl 10 --parallel 14 --shorten-paths validate r2
./scripts/cli.sh --parallel 14 --shorten-paths  --msl 10 validate inflines --strain-sensors O
./scripts/cli.sh --parallel 14 --shorten-paths  --msl 10 validate inflines --strain-sensors T

