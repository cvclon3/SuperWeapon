from railgun.railgun import Railgun
from railgun.shell import Shell
from railgun.target import Target

rg44 = Railgun(
    {
        'Dispersion': 0.02,
        'V_Deviation': 0.0
    }
)
bolt44 = Shell(weight=110, velocity=950, aerodyn_coef=0.003)
target = Target((1150, 10), (1250, 10), (1250, -10), (1150, -10))

rg44.locate((1, -1, 0), (1, 1, 0), (1, 1))
rg44.load(bolt44)
rg44.rotate(-45, 30)

if __name__ == "__main__":
    rg44.fire(target=target)
