from railgun.railgun import Railgun
from railgun.shell import Shell
from railgun.target import Target

rg44 = Railgun(
    {
        'Dispersion': 1,
        'V_Deviation': 0.15
    }
)
bolt44 = Shell(weight=110, velocity=950, aerodyn_coef=0.007)
target = Target((650, 10), (750, 10), (750, -10), (650, -10))

rg44.locate((1, -1, 0), (1, 1, 0), (1, 1))
rg44.load(bolt44)
rg44.rotate(-45, 30)

rg44.fire(target=target)
