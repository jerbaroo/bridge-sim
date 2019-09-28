"""Plot responses on a bridge."""
from fem.responses import FEMResponses
from plot import plt


def plot_contour_deck(fem_responses: FEMResponses, y: float = -0.5):
    """Contour plot of responses on the deck of the bridge."""
    X, Z, H = [], [], []  # 2D arrays, of x and y coordinates, and height.
    for x in fem_responses.xs:
        X.append([])
        Z.append([])
        H.append([])
        for z in fem_responses.zs[x][y]:
            X[-1].append(x)
            Z[-1].append(z)
            H[-1].append(fem_responses.responses[0][x][y][z].value)
    cs = plt.contourf(X, Z, H)
    plt.colorbar(cs)
    # plt.show()
