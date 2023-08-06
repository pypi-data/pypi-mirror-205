import scipy.special as spe
import numpy as np

# LAGUERRE FUNCTIONS
def radial(n: int, l: int, r: np.ndarray) -> np.ndarray:

	"""
	Função que calcula os valores do polinômio de Laguerre para cada r dado.
	
	Lembrando que deve-se ter:
		1. n > 0.
		2. l = n - 1.

	args:
		n (int): número quântico principal.

		l (int): número quântico secundário.

		r (np.ndarray): valores de r no eixo x.

	returns:
		um np.ndarray contendo os valores do polinômio de Laguerre para cada r.

	"""

	# LAGUERRE FUNCTIONS
	coeff = np.sqrt((2/n)**3*spe.factorial(n-l-1)/(2*n*spe.factorial(n+l)))
	laguerre = spe.assoc_laguerre(2*r/n, n-l-1, 2*l+1)
	full = coeff * np.exp(-r/n) * (2*r/n)**l * laguerre

	return full

# SPHERICAL HARMONICS
def angular(m: int, l: int, theta: np.ndarray, phi: np.ndarray) -> np.ndarray:

	"""
	Função que calcula os valores da parte real do polinômio de Legendre para cada 
	phi e theta dado.

	Lebrando que deve-se ter:
		1. abs(M) <= l.
		2. l >= 0.

	args:
		m (int): ordem do harmônico.

		l (int): grau do harmônico.

		theta (np.ndarray): valores do ângulo theta. Deve estar entre [0, 2*np.pi].

		phi (np.ndarray): valores do ângulo phi. Deve estar entre [0, np.pi].

	returns:
		a parte real de um np.ndarray do polinômio de Legendre (Yml) 
		para os valores de m e l.

	"""

	return spe.sph_harm(m, l, theta, phi).real