import pandas as pd

from main import rg44, bolt44, target


def line(railgun):
    data = rg44._calc_setup()

    is_hit = target.is_target_hit((data.x_shell, data.y_shell))

    return [
        railgun.x_railgun,
        railgun.y_railgun,
        railgun.alpha,
        railgun.beta,
        bolt44.velocity,
        bolt44.weight,
        bolt44.drag_coef,
        data.x_shell,
        data.y_shell,
        is_hit
    ]


dataset = []

for i in range(100):
    dataset.append(line(rg44))

df = pd.DataFrame(data=dataset, columns=[
    'x_railgun', 'y_railgun', 'alpha', 'beta', 'velocity', 'weight', 'drag_coef', 'x_shell', 'y_shell', 'is_hit'
])

print(df.to_string())
df.to_csv('data.csv')
