def dist1(self, X):
    X = dia_matrix(X).todense()
    distmat_ = squareform(pdist(X, 'euclidean'))
    return distmat_
'''
    
def dist2(self, X):
    H = np.tile(np.diag(np.dot(X, X.T)), (X.shape[0], 1))
    G = np.dot(X, X.T)
    distmat_ = (H - 2 * G + H.T) ** 0.5
    return distmat_

def dist3(self, X):
    def single_dist(spoint, X):
        dataSetSize = X.shape[0]
        print(dataSetSize)
        diffMat = np.tile(spoint,(dataSetSize,1))-X
        sqDiffMat = diffMat ** 2
        sqDistances = sqDiffMat.sum(axis=1)
        distances = sqDistances ** 0.5
        return distances
    distmat_ = np.zeros((X.shape[0], X.shape[0]))
    for i in range(X.shape[0]):
        distmat_[i] = single_dist(X[i], X)
        print('{0} done'.format(i))
    return distmat_

def dist4(self, X):
    def single_dist(spoint, X):
        diffMat = spoint-X
        sqDiffMat = diffMat ** 2
        sqDistances = sqDiffMat.sum()
        distances = sqDistances ** 0.5
        return distances
    distmat_ = np.zeros((X.shape[0], X.shape[0]))
    for i in range(X.shape[0]):
        for j in range(i+1, X.shape[0]):
            x = single_dist(X[i], X[j])
            distmat_[i][j] = x
            print('{0}, {1} done'.format(i, j))
    distmat_ = distmat_ + distmat_.T
    return distmat_
