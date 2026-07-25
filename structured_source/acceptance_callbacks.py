"""One recurring callback for each current SSM acceptance criterion."""


def _callback(code):
    def run(context):
        return context.evidence_for(code)
    return run


CALLBACKS = {
    "ssp.SSM-AC-01.authority-registry": _callback("SSM-AC-01"),
    "ssp.SSM-AC-02.xml-format-metadata": _callback("SSM-AC-02"),
    "ssp.SSM-AC-03.pdf-evidence": _callback("SSM-AC-03"),
    "ssp.SSM-AC-04.authored-markdown": _callback("SSM-AC-04"),
    "ssp.SSM-AC-05.relation-reference": _callback("SSM-AC-05"),
    "ssp.SSM-AC-06.conversion-interface": _callback("SSM-AC-06"),
    "ssp.SSM-AC-07.assurance-separation": _callback("SSM-AC-07"),
    "ssp.SSM-AC-08.commands-writes-efficiency": _callback("SSM-AC-08"),
    "ssp.SSM-AC-09.audit-final-snapshot": _callback("SSM-AC-09"),
    "ssp.SSM-AC-10.implementation-closure": _callback("SSM-AC-10"),
}
