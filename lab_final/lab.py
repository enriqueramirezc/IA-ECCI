# Andrés Camacho, Anthony Sanchez, Enrique Ramírez

from pathlib import Path
import numpy as np
from gensim.models import KeyedVectors
from scipy.cluster.hierarchy import fcluster, dendrogram
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


# Parte 1

DIR = Path(__file__).parent
MODELO = DIR / "SBW-vectors-300-min5.txt"
CACHE = DIR / "vectores_anexo.npz"

PALABRAS = [ # estas palabras las puse con claude
    'abandono', 'abatimiento', 'adoración', 'afán', 'afecto', 'aflicción',
    'agitación', 'agonía', 'agradecimiento', 'agravación', 'aislamiento',
    'alarma', 'alborozo', 'alegría', 'alerta', 'algarabía', 'alienación',
    'alivio', 'amargura', 'amor', 'angustia', 'anhelo', 'ansia', 'ansiedad',
    'antipatía', 'añoranza', 'aprecio', 'aprensión', 'arrebato',
    'arrepentimiento', 'asco', 'asombro', 'atención', 'atracción',
    'aversión', 'bochorno', 'cariño', 'cascarrabias', 'cautivación', 'celo',
    'choque', 'cólera', 'compasión', 'concordia', 'conmoción',
    'consideración', 'consternación', 'contentamiento', 'contento',
    'cuidado', 'culpa', 'decepción', 'deleite', 'depresión', 'derrotismo',
    'desagrado', 'desahogo', 'desaliento', 'desamparo', 'desanimado',
    'descuido', 'desdén', 'deseo', 'desesperación', 'despecho', 'desprecio',
    'dicha', 'disfrute', 'disgusto', 'diversión', 'dolor', 'duelo',
    'emoción', 'empatía', 'enamoramiento', 'encaprichamiento', 'enojo',
    'entretenimiento', 'entusiasmo', 'envidia', 'esperanza',
    'estupefacción', 'euforia', 'exaltación', 'exasperación', 'excitación',
    'éxtasis', 'fascinación', 'felicidad', 'ferocidad', 'fervor',
    'frustración', 'furia', 'gozo', 'gruñón', 'gusto', 'herido', 'histeria',
    'horror', 'hostilidad', 'humillación', 'incertidumbre', 'indignación',
    'infelicidad', 'inquietud', 'inseguridad', 'insulto', 'ira',
    'irritabilidad', 'jocosidad', 'jovialidad', 'júbilo', 'lástima',
    'lujuria', 'luto', 'malhumor', 'malicia', 'melancolía', 'miedo',
    'miseria', 'molestia', 'mortificación', 'negligencia', 'nerviosismo',
    'nostalgia', 'odio', 'optimismo', 'orgullo', 'oscuridad', 'pánico',
    'pasión', 'pavor', 'pena', 'pesimismo', 'placer', 'plenitud',
    'preocupación', 'rabia', 'rechazo', 'regocijo', 'remordimiento',
    'rencor', 'repugnancia', 'repulsión', 'resentimiento', 'satisfacción',
    'sentimentalismo', 'simpatía', 'sobresalto', 'soledad', 'sorpresa',
    'sufrimiento', 'suplicio', 'suspenso', 'susto', 'temor', 'ternura',
    'terror', 'tormento', 'tristeza', 'triunfo', 'venganza', 'vergüenza',
    'victoria',
]


# La idea de usar caché se tomó de claude.
def cargar_vectores():
    # verificar si ya se tiene el cache para no volver a hacer todo denuevo
    if CACHE.exists():
        datos = np.load(CACHE)
        return list(datos["palabras"]), datos["X"]

    # si no se tiene en caché, entonces se lee el modelo para conseguir los vectores de las 163 palabras.
    palabras = PALABRAS
    modelo = KeyedVectors.load_word2vec_format(MODELO, binary=False)

    faltantes = [p for p in palabras if p not in modelo]
    if faltantes:
        print("No están en el modelo:", faltantes)

    palabras = [p for p in palabras if p in modelo]
    X = np.array([modelo[p] for p in palabras])
    np.savez(CACHE, palabras=np.array(palabras), X=X)
    return palabras, X

# Cabe resaltar que la palabra cautivación no aparece

# parte 2

def distancia_euclidiana(a, b):
    return np.sqrt(np.sum((a - b) ** 2))


# Misma fórmula que src/clustering_cosenos.py; solo se usa para el dendrograma de coseno
def distancia_coseno(a, b):
    return 1 - np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Parte 3
# Se recibe la matriz x con las palabras y numeros, el k son los grupos, se recibe funcion de distancia...

# etiqueta las palabras en 4 grupos
def kmeans(X, k, distancia, max_iter=100, n_init=10, semilla=42):
    rng = np.random.default_rng(semilla)
    mejores_etiquetas, mejor_costo = None, np.inf

    # ejecucion del algoritmo
    for _ in range(n_init):
        # Inicio: k palabras al azar como centroides
        centroides = X[rng.choice(len(X), k, replace=False)].copy()    # se agarran 4 palabras random
        etiquetas = None

        for _ in range(max_iter):
            # Asignar cada palabra al centroide más cercano
            nuevas = np.array([ #esta parte la hizo claude
                np.argmin([distancia(x, c) for c in centroides]) for x in X
            ])
            if etiquetas is not None and np.array_equal(nuevas, etiquetas):
                break
            etiquetas = nuevas

            # Se mueven los centros
            for j in range(k):
                miembros = X[etiquetas == j]
                if len(miembros) > 0:
                    centroides[j] = miembros.mean(axis=0)

        # Se mide qué tan buena es la solucion
        costo = sum(distancia(x, centroides[e]) ** 2 for x, e in zip(X, etiquetas))
        if costo < mejor_costo:
            mejor_costo, mejores_etiquetas = costo, etiquetas

    return mejores_etiquetas


# estos son los grupos:
'''
Grupo 0 (62 palabras):
amargura, antipatía, aprensión, arrebato, arrepentimiento, asco, asombro, aversión, bochorno, compasión, conmoción, consternación, culpa, decepción, derrotismo, desagrado, desaliento, desanimado, desdén, despecho, desprecio, disgusto, empatía, encaprichamiento, enojo, envidia, estupefacción, exasperación, ferocidad, frustración, furia, hostilidad, humillación, indignación, inquietud, insulto, ira, lástima, malhumor, malicia, miedo, molestia, nerviosismo, odio, pánico, pavor, pesimismo, preocupación, rabia, rechazo, remordimiento, rencor, repugnancia, repulsión, resentimiento, simpatía, sobresalto, sorpresa, temor, tristeza, venganza, vergüenza

Grupo 1 (26 palabras):
abandono, agravación, aislamiento, alarma, alerta, alivio, atención, choque, cólera, consideración, cuidado, desahogo, desamparo, descuido, dicha, duelo, herido, incertidumbre, inseguridad, luto, negligencia, pena, suspenso, susto, triunfo, victoria

Grupo 2 (48 palabras):
adoración, afán, afecto, agradecimiento, alborozo, alegría, algarabía, amor, anhelo, ansia, añoranza, aprecio, atracción, cariño, cascarrabias, celo, concordia, contentamiento, contento, deleite, deseo, disfrute, diversión, emoción, entretenimiento, entusiasmo, esperanza, euforia, exaltación, fascinación, felicidad, fervor, gozo, gruñón, gusto, jocosidad, jovialidad, júbilo, nostalgia, optimismo, orgullo, pasión, placer, plenitud, regocijo, satisfacción, sentimentalismo, ternura

Grupo 3 (27 palabras):
abatimiento, aflicción, agitación, agonía, alienación, angustia, ansiedad, depresión, desesperación, dolor, enamoramiento, excitación, éxtasis, histeria, horror, infelicidad, irritabilidad, lujuria, melancolía, miseria, mortificación, oscuridad, soledad, sufrimiento, suplicio, terror, tormento
'''

# Cabe resaltar que en algunos casos, hay palabras que tiene poco que ver con el resto de lsa de ese grupo. Por ejemplo, 
# el grupo 3 tiene que ver con sufrimiento, pero en ese grupo aparecen "enamoramiento"

# parte 4. Se agrupan palabran en familias con hac
def hac(X, distancia):

    # Esto lo hizo claude. Son las distancias entre grupos
    n = len(X)
    D = np.full((2 * n - 1, 2 * n - 1), np.inf)
    for i in range(n):
        for j in range(i + 1, n):
            D[i, j] = D[j, i] = distancia(X[i], X[j])

    tam = {i: 1 for i in range(n)}  # grupos que hay y sus tamaños
    Z = []

    for nuevo in range(n, 2 * n - 1):
        # Buscar los dos grupos más cercanos y unirlos
        a, b = (int(i) for i in np.unravel_index(np.argmin(D), D.shape))
        tam[nuevo] = tam[a] + tam[b]
        Z.append([a, b, D[a, b], tam[nuevo]])

        # distancia máxima del grupo nuevo a los demás
        for c in tam:
            if c not in (a, b, nuevo):
                D[nuevo, c] = D[c, nuevo] = max(D[a, c], D[b, c])


        # Los grupos que se unieron se desactivan. No se vuelven a elegir.
        D[a, :] = D[:, a] = D[b, :] = D[:, b] = np.inf
        del tam[a], tam[b]

    return np.array(Z)

'''
Grupo 0 (60 palabras):
afán, afecto, agradecimiento, alarma, alborozo, alegría, alerta, algarabía, amor, anhelo, ansia, añoranza, aprecio, arrepentimiento, cariño, cascarrabias, choque, cólera, compasión, contentamiento, contento, deleite, desanimado, deseo, duelo, emoción, empatía, enamoramiento, encaprichamiento, entusiasmo, esperanza, exaltación, fascinación, felicidad, fervor, gozo, gruñón, gusto, herido, inquietud, jocosidad, jovialidad, júbilo, luto, malicia, melancolía, mortificación, nostalgia, orgullo, pasión, placer, plenitud, preocupación, regocijo, remordimiento, satisfacción, sentimentalismo, ternura, triunfo, victoria

Grupo 1 (12 palabras):
agravación, aislamiento, alivio, atención, celo, concordia, consideración, cuidado, desahogo, dicha, pena, suspenso

Grupo 2 (83 palabras):
abandono, abatimiento, aflicción, agitación, agonía, alienación, amargura, angustia, ansiedad, antipatía, aprensión, arrebato, asco, asombro, aversión, bochorno, conmoción, consternación, culpa, decepción, depresión, derrotismo, desagrado, desaliento, desamparo, descuido, desdén, desesperación, despecho, desprecio, disgusto, dolor, enojo, envidia, estupefacción, euforia, exasperación, ferocidad, frustración, furia, histeria, horror, hostilidad, humillación, incertidumbre, indignación, infelicidad, inseguridad, insulto, ira, irritabilidad, lástima, lujuria, malhumor, miedo, miseria, molestia, negligencia, nerviosismo, odio, optimismo, oscuridad, pánico, pavor, pesimismo, rabia, rechazo, rencor, repugnancia, resentimiento, simpatía, sobresalto, soledad, sorpresa, sufrimiento, suplicio, susto, temor, terror, tormento, tristeza, venganza, vergüenza

Grupo 3 (8 palabras):
adoración, atracción, disfrute, diversión, entretenimiento, excitación, éxtasis, repulsión
'''


# parte 5. Las gráficas las hizo claude
COLORES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
MARCADORES = ["o", "s", "^", "D"]


def graficar_grupos(X, resultados, archivo):
    pca = PCA(n_components=2)
    P = pca.fit_transform(X)
    var = pca.explained_variance_ratio_ * 100

    fig, axes = plt.subplots(
        1, len(resultados), figsize=(6.5 * len(resultados), 6),
        sharex=True, sharey=True, squeeze=False,
    )
    for ax, (titulo, etiquetas) in zip(axes[0], resultados):
        for g in range(4):
            m = etiquetas == g
            ax.scatter(P[m, 0], P[m, 1], s=55, c=COLORES[g], marker=MARCADORES[g],
                       edgecolors="white", linewidths=1,
                       label=f"Grupo {g} ({m.sum()} palabras)")
        ax.set_title(titulo)
        ax.set_xlabel(f"PC1 ({var[0]:.1f}% de la varianza)")
        ax.set_ylabel(f"PC2 ({var[1]:.1f}% de la varianza)")
        ax.grid(alpha=0.2)
        ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(DIR / archivo, dpi=150)
    plt.close(fig)


def graficar_dendrograma(Z, palabras, titulo, archivo, etiqueta_x, mostrar_corte=True):
    fig, ax = plt.subplots(figsize=(10, 26))
    dendrogram(Z, labels=[str(p) for p in palabras], orientation="left",
               leaf_font_size=8, color_threshold=0,
               above_threshold_color="#555555", ax=ax)
    if mostrar_corte:
        corte = (Z[-4, 2] + Z[-3, 2]) / 2  # altura donde quedan 4 grupos
        ax.axvline(corte, color="#e34948", linestyle="--", label="Corte: 4 grupos")
        ax.legend(frameon=False, loc="upper left")
    ax.set_title(titulo)
    ax.set_xlabel(etiqueta_x)
    fig.tight_layout()
    fig.savefig(DIR / archivo, dpi=150)
    plt.close(fig)


if __name__ == "__main__":
    palabras, X = cargar_vectores()

    et_kmeans = kmeans(X, 4, distancia_euclidiana)
    Z = hac(X, distancia_euclidiana)
    et_hac = fcluster(Z, 4, criterion="maxclust") - 1

    graficar_grupos(X, [("K-means, distancia euclidiana", et_kmeans),
                        ("HAC, distancia euclidiana", et_hac)],
                    "grupos_euclidiana.png")
    graficar_dendrograma(Z, palabras, "HAC, distancia euclidiana",
                         "dendrograma_euclidiana.png",
                         "Distancia euclidiana máxima entre grupos (enlace completo)")

    # Dendrograma para la parte de coseno
    Z_cos = hac(X, distancia_coseno)
    graficar_dendrograma(Z_cos, palabras, "HAC, distancia coseno",
                         "dendrograma_coseno.png",
                         "Distancia coseno máxima entre grupos (enlace completo)",
                         mostrar_corte=False)

    for nombre, et in [("K-means", et_kmeans), ("HAC", et_hac)]:
        print(f"\n===== {nombre} =====")
        for g in range(4):
            grupo = [str(p) for p, e in zip(palabras, et) if e == g]
            print(f"\nGrupo {g} ({len(grupo)} palabras):")
            print(", ".join(grupo))
