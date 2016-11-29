
import numpy as np
na = np.newaxis

class LinearIsopMap(object):

    def __init__(self):
        pass

    def _l1(self, X):
        return (1.0-X)/2.0
    def _dl1(self, X):
        return -np.ones_like(X)/2.0
    def _l2(self, X):
        return (1.0+X)/2.0
    def _dl2(self, X):
        return np.ones_like(X)/2.0

    def ref_to_phys(self, X, nodes):

        v1 = self._l1(X)
        v2 = self._l2(X)
        v1x, v1y, v1z = v1.T
        v2x, v2y, v2z = v2.T

        P = (v1x*v1y*v1z)[:,na]*nodes[0,:]+\
            (v2x*v1y*v1z)[:,na]*nodes[1,:]+\
            (v1x*v2y*v1z)[:,na]*nodes[2,:]+\
            (v2x*v2y*v1z)[:,na]*nodes[3,:]+\
            (v1x*v1y*v2z)[:,na]*nodes[4,:]+\
            (v2x*v1y*v2z)[:,na]*nodes[5,:]+\
            (v1x*v2y*v2z)[:,na]*nodes[6,:]+\
            (v2x*v2y*v2z)[:,na]*nodes[7,:]

        return P

    def calc_jacb(self, X, nodes):

        v1 = self._l1(X)
        v2 = self._l2(X)
        v1x, v1y, v1z = v1.T
        v2x, v2y, v2z = v2.T

        dv1 = self._dl1(X)
        dv2 = self._dl2(X)
        dv1x, dv1y, dv1z = dv1.T
        dv2x, dv2y, dv2z = dv2.T

        J = np.zeros((len(X),3,3))

        t1x, t2x, t3x = ((dv1x*v1y*v1z)[:,na]*nodes[0,:]+\
                         (dv2x*v1y*v1z)[:,na]*nodes[1,:]+\
                         (dv1x*v2y*v1z)[:,na]*nodes[2,:]+\
                         (dv2x*v2y*v1z)[:,na]*nodes[3,:]+\
                         (dv1x*v1y*v2z)[:,na]*nodes[4,:]+\
                         (dv2x*v1y*v2z)[:,na]*nodes[5,:]+\
                         (dv1x*v2y*v2z)[:,na]*nodes[6,:]+\
                         (dv2x*v2y*v2z)[:,na]*nodes[7,:]).T

        t1y, t2y, t3y = ((v1x*dv1y*v1z)[:,na]*nodes[0,:]+\
                         (v2x*dv1y*v1z)[:,na]*nodes[1,:]+\
                         (v1x*dv2y*v1z)[:,na]*nodes[2,:]+\
                         (v2x*dv2y*v1z)[:,na]*nodes[3,:]+\
                         (v1x*dv1y*v2z)[:,na]*nodes[4,:]+\
                         (v2x*dv1y*v2z)[:,na]*nodes[5,:]+\
                         (v1x*dv2y*v2z)[:,na]*nodes[6,:]+\
                         (v2x*dv2y*v2z)[:,na]*nodes[7,:]).T

        t1z, t2z, t3z = ((v1x*v1y*dv1z)[:,na]*nodes[0,:]+\
                         (v2x*v1y*dv1z)[:,na]*nodes[1,:]+\
                         (v1x*v2y*dv1z)[:,na]*nodes[2,:]+\
                         (v2x*v2y*dv1z)[:,na]*nodes[3,:]+\
                         (v1x*v1y*dv2z)[:,na]*nodes[4,:]+\
                         (v2x*v1y*dv2z)[:,na]*nodes[5,:]+\
                         (v1x*v2y*dv2z)[:,na]*nodes[6,:]+\
                         (v2x*v2y*dv2z)[:,na]*nodes[7,:]).T

        J[:,0,0] = t1x
        J[:,0,1] = t1y
        J[:,0,2] = t1z
        J[:,1,0] = t2x
        J[:,1,1] = t2y
        J[:,1,2] = t2z
        J[:,2,0] = t3x
        J[:,2,1] = t3y
        J[:,2,2] = t3z

        return J