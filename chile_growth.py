import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# This makes out plots higher resolution, which makes them easier to see while building
plt.rcParams['figure.dpi'] = 100
gdp = pd.read_csv('data/gdp_growth.csv')



chile = gdp[gdp['Code'] == 'CHL']
chile = chile.T
chile = chile.iloc[2:].reset_index()  # Convierte el índice en columna y elimina la fila del encabezado
chile.columns = ["año", "gdp"]  # Renombra las columnas
chile = chile.iloc[:-1]  # Elimina la última fila
chile = chile.dropna()  # Elimina columnas completamente vacías
chile["año"] = chile["año"].astype(float)  # Convierte el año en entero

# Agregando data de los últimos años
new_data = pd.DataFrame([[2021, 11.7], [2022, 2.4], [2023, -0.53], [2024, 0.7]], 
                        columns=["año", "gdp"])

chile = pd.concat([chile, new_data], ignore_index=True)

print(chile)


# Calcular la suma acumulativa
chile["gdp_sum"] = chile["gdp"].cumsum()


# Seleccionar un rango de columnas por nombre y calcular el promedio individualmente
world = gdp.loc[:, "1961":"2020"].mean()

# Convertir Series a DataFrame
world = world.reset_index()
world.columns = ["año", "gdp"]  # Renombrar columnas
world["año"] = world["año"].astype(float)  # Convierte el año en entero

# Agregar un nuevo índice numérico
world.index.name = "índice"

# Agregando data de los últimos años
last_years = pd.DataFrame([[2021, 6.0], [2022, 3.2], [2023, 3.0], [2024, 3.1]], 
                        columns=["año", "gdp"])

world = pd.concat([world, last_years], ignore_index=True)

world["gdp_sum"] = world["gdp"].cumsum()


print(world)


# Setup plot size.
fig, ax = plt.subplots(figsize=(8,4))

# Create grid 
# Zorder tells it which layer to put it on. We are setting this to 1 and our data to 2 so the grid is behind the data.
ax.grid(which="major", axis='y', color='#758D99', alpha=0.6, zorder=1)


ax.plot(chile['año'], 
        chile['gdp_sum'], 
        color='#3EBCD2',
        linewidth=3)


ax.plot(world['año'], 
        world['gdp_sum'], 
        color='#006BA2',
        linewidth=3)


# Remove splines. Can be done one at a time or can slice with a list.
ax.spines[['top','right','left']].set_visible(False)



# Add labels for Chile and Wolrd
ax.text(x=.4, y=.285, s='Chile', transform=fig.transFigure, size=10, alpha=.9)
ax.text(x=.3, y=.45, s='Mundial', transform=fig.transFigure, size=10, alpha=.9)


# Add in line and tag
ax.plot([0.12, .9],                  # Set width of line
        [.98, .98],                  # Set height of line
        transform=fig.transFigure,   # Set location relative to plot
        clip_on=False, 
        color='#E3120B', 
        linewidth=.6)
ax.add_patch(plt.Rectangle((0.12,.98),                 # Set location of rectangle by lower left corder
                           0.04,                       # Width of rectangle
                           -0.02,                      # Height of rectangle. Negative so it goes down.
                           facecolor='#E3120B', 
                           transform=fig.transFigure, 
                           clip_on=False, 
                           linewidth = 0))

# Add in title and subtitle
ax.text(x=0.12, y=.91, s="PIB de Chile", transform=fig.transFigure, ha='left', fontsize=13, weight='bold', alpha=.8)
ax.text(x=0.12, y=.86, s="Comparado con el crecimiento promedio mundial", transform=fig.transFigure, ha='left', fontsize=11, alpha=.8)

# Set source text
ax.text(x=0.12, y=0.01, s="""Source: "GDP of all countries(1960-2020)" via Kaggle.com""", transform=fig.transFigure, ha='left', fontsize=9, alpha=.7)




# Export plot as high resolution PNG
plt.savefig('images/chile_growth.png',    # Set path and filename
            dpi = 300,                     # Set dots per inch
            bbox_inches="tight",           # Remove extra whitespace around plot
            facecolor='white')             # Set background color to white
