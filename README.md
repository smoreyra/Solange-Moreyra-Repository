# Exploratory Data Analysis con Python - Music Genre

En el presente trabajo a partir de un data set sobre géneros de música, obtenido de la plataforma Kaggle, se analizará la data que presenta para realizar conclusiones y hacerla lo suficientemente robusta para una posterior modelización. El análisis fue realizado en Visual Studio mediante una notebook (archivo .ipynb).

En primer lugar se importaron las librerías necesarias: NumPy, Pandas, Seaborn y Matplotlib. Luego se cargó el data set desde el formato CSV (comma separated values) a un pandas data frame. Mediante un shape se obtienen las dimensiones del data frame, y con las funciones head() y tail() las primeras y últimas filas del data frame, respectivamente. A partir de esto se puede observar que el data set esta compuesto por 50005 filas y 18 columnas con los siguientes nombres: isntance_id, artist_name, track_name, popularity, acousticness, danceability, duration_ms, energy, intrumentalness, key, liveness, loudness, mode, speechiness, tempo, obteained_date, valence, music_genre. Luego se aplicó la función describe() para obtener diferentes estadísticos de las columnas numéricas como la cantidad, la media, el desvío estándar el valor mínimo, el cuartil 0.25, 0.50, 0.75 y el valor máximo. 

El que presenta mayor correlación positiva es entre energy y loudness con un valor de coeficiente de correlación de 0,84 y el segundo con mayor correlación positiva es entre valence y danceability con un coeficiente de 0,43. Por otro lado el que presenta mayor correlación negativa es entre energy y acousticness con un coeficiente de -0,73 y el segundo es entre instrumentalness y loudnes con un coeficient ede -0,53.

Se analizaron los siguientes datos:
