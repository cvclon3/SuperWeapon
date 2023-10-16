from railgun.railgun import Railgun
from railgun.shell import Shell
from railgun.target import Target

rg44 = Railgun(
    {
        'Dispersion': 0.5,  # 0.02 for __func2
        'V_Deviation': 0.15  # 0.00 for __func2
    }
)
bolt44 = Shell(110, 950, 0.003)
target = Target((1150, 10), (1250, 10), (1250, -10), (1150, -10))

rg44.locate((1, -1, 0), (1, 1, 0), (1, -1))
rg44.load(bolt44)
rg44.rotate(45, 30)

if __name__ == "__main__":
    rg44.fire(target=target)
