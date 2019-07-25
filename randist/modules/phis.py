from sympy import simplify, lambdify, integrate
# from sympy import sympify, lambdify, integrate
from sympy.abc import p, q
from scipy.integrate import dblquad

class Phi:
    def __init__(self, name, phi_pq=None, phi_p=None, phi_q=None, symbolic=True, eps=1e-7):
        self.name = name
        self.eps = eps
        self.symbolic = symbolic

        if symbolic:
            self.phi_pq_S = phi_pq
            self.phi_p_S = phi_p
            self.phi_q_S = phi_q
            self.__gen_phi()
        else:
            self.phi_p_N = lambda p: phi_p(p)
            self.phi_q_N = lambda q: phi_q(q)
            self.phi_pq_N = lambda q, p: phi_pq(p, q)
            self.phi_qcp_N = lambda q, p: phi_pq(p, q) / phi_p(p)

        if self.__check() is False:
            raise Exception('input phi does not integrate to one')
        
    def __gen_phi(self):
        if self.phi_p_S is not None and self.phi_q_S is not None and self.phi_pq_S is not None:
            self.phi_p_S = simplify(self.phi_p_S)
            self.phi_q_S = simplify(self.phi_q_S)
            self.phi_pq_S = simplify(self.phi_pq_S)
            self.phi_qcp_S = self.phi_q_S
        elif self.phi_p_S is not None and self.phi_q_S is not None:
            # self.phi_p_S = sympify(self.phi_p_S)
            # self.phi_q_S = sympify(self.phi_q_S)
            self.phi_p_S = simplify(self.phi_p_S)
            self.phi_q_S = simplify(self.phi_q_S)
            self.phi_pq_S = simplify(self.phi_p_S * self.phi_q_S)
            self.phi_qcp_S = self.phi_q_S
        elif self.phi_pq_S is not None:
            # self.phi_pq_S = sympify(self.phi_pq_S)
            self.phi_pq_S = simplify(self.phi_pq_S)
            self.phi_p_S = simplify(integrate(self.phi_pq_S, (q, 0 , 1)))
            self.phi_q_S = simplify(integrate(self.phi_pq_S, (p, 0 , 1)))
            self.phi_qcp_S = simplify(self.phi_pq_S / self.phi_p_S)
        else:
            raise Exception('please provide both phi_p and phi_q, or the joint pdf phi_pq.')

        self.phi_p_N = lambdify(p, self.phi_p_S)
        self.phi_q_N = lambdify(q, self.phi_q_S)
        self.phi_pq_N = lambdify((q, p), self.phi_pq_S)
        self.phi_qcp_N = lambdify((q, p), self.phi_qcp_S)

    def __check(self):
        phi_tot = dblquad(self.phi_pq_N, 0, 1, lambda p: 0, lambda p: 1)[0]
        if abs(phi_tot - 1) < self.eps:
            phi_one = True
        else:
            phi_one = False
        return phi_one

