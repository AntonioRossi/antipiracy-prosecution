"""Namespaced recurring callbacks owned by the executable SSM registry."""


def _run(context, criterion):
    return context.run_check(criterion)


def ssm_ac_01(context):
    return _run(context, "SSM-AC-01")


def ssm_ac_02(context):
    return _run(context, "SSM-AC-02")


def ssm_ac_03(context):
    return _run(context, "SSM-AC-03")


def ssm_ac_04(context):
    return _run(context, "SSM-AC-04")


def ssm_ac_05(context):
    return _run(context, "SSM-AC-05")


def ssm_ac_06(context):
    return _run(context, "SSM-AC-06")


def ssm_ac_07(context):
    return _run(context, "SSM-AC-07")


def ssm_ac_08(context):
    return _run(context, "SSM-AC-08")


def ssm_ac_09(context):
    return _run(context, "SSM-AC-09")


def ssm_ac_10(context):
    return _run(context, "SSM-AC-10")


CALLBACKS = {
    "ssp.SSM-AC-01.registry-closure": ssm_ac_01,
    "ssp.SSM-AC-02.xml-identity": ssm_ac_02,
    "ssp.SSM-AC-03.provenance-assets": ssm_ac_03,
    "ssp.SSM-AC-04.relation-closure": ssm_ac_04,
    "ssp.SSM-AC-05.projection-coverage": ssm_ac_05,
    "ssp.SSM-AC-06.human-approvals": ssm_ac_06,
    "ssp.SSM-AC-07.reference-taxonomy": ssm_ac_07,
    "ssp.SSM-AC-08.approved-export": ssm_ac_08,
    "ssp.SSM-AC-09.atomic-reproducibility": ssm_ac_09,
    "ssp.SSM-AC-10.operative-closure": ssm_ac_10,
}

