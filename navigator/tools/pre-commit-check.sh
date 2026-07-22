#!/bin/sh
# Generated-file discipline (TDD §10.15): local pre-commit
# rebuild-and-compare. Rebuilds each edition's candidate derivation and
# byte-compares it against the committed dist candidate; a mismatch means
# dist artifacts were hand-edited or sources changed without a rebuild.
set -e
cd "$(dirname "$0")/../.."
for ed in na af; do
  python3 - "$ed" <<'EOF'
import json, sys
sys.path.insert(0, "navigator")
from lib import gateway, model, render
ed = sys.argv[1]
boot = gateway.ContentGateway(".")
allow = json.loads(boot.read_text("navigator/editions/%s.json" % ed))
gw = gateway.ContentGateway(".", allowlist=allow["declaredTransitiveInputs"])
m = model.EditionModel(gw, "navigator/editions/%s.json" % ed)
html = render.render(m, mode="candidate")
path = "navigator/dist/candidate_" + m.edition["artifactName"]
with open(path, "rb") as fh:
    committed = fh.read()
if committed != html:
    raise SystemExit("%s: dist candidate does not match a rebuild — "
                     "regenerate before committing" % ed)
print("%s: rebuild-and-compare OK" % ed)
EOF
done
