""" Written on 4/15/2022 by Abhilasha, Sakshi & Pankti
Module contains functions for Lotka-Volterra Systems aka Predator - Prey Model"""
import os

from numpy.lib.scimath import sqrt

import numpy as np
import matplotlib.pyplot as plt


class Lotka_Volterra(object):
    """
    This class performs the complete analysis of a lotka volterra system,
    a predator - prey model when predator is logistic growth while prey has normal growth
    such as plotting the populations vs time, predator vs prey, finding equilibrium points,
    calculating jacobian, and it's trace and determinant
    Finding the stability of each equilibrium point
    Calculating their eigen values
    Ploting a phase graph and nullclines
    """

    """
    Notation in the module:
    
        x = predator population
        y = prey population
        iv_x = initial population of x
        iv_y = initial population of y
        alpha = predator growth rate
        beta = prey death rate
        dt = timestep
        time = range
        equilibria = set of equilibrium points
        f(x,y) = rate of change of predator population with time (Differential equation)
        g(x,y) = rate of change of prey population with time ( Differential equation)
        """

    def __init__(self, iv_x, iv_y, alpha, beta, dt, time):

        self.time = time
        self.x = np.zeros(self.time)
        self.y = np.zeros(self.time)
        self.alpha = alpha
        self.beta = beta
        self.dt = dt
        self.equilibria = []

    def initial_value(self, iv_x, iv_y):
        """Give initial values of population and returns x and y as initial value"""

        self.x[0] = iv_x
        self.y[0] = iv_y

        """Define system in terms of separated differential equations"""

    def f(self, x, y):
        return self.alpha * x - x ** 2 - x * y

    def g(self, x, y):
        return -self.beta * y + x * y

    def logistic_sys(self):
        """compute and fill lists to give the value of x and y"""
        for i in range(self.time - 1):
            self.x[i + 1] = self.x[i] + (self.f(self.x[i], self.y[i])) * self.dt
            self.y[i + 1] = self.y[i] + (self.g(self.x[i], self.y[i])) * self.dt
        return self.x, self.y

    def plot_system(self, filename='Dynamic Systems and Phase Plot'):
        fig1 = plt.figure(figsize=(15, 5))
        fig1.subplots_adjust(wspace=0.5, hspace=0.3)
        ax1 = fig1.add_subplot(1, 2, 1)
        ax2 = fig1.add_subplot(1, 2, 2)

        ax1.plot(self.x, 'r-', label='predator')
        ax1.plot(self.y, 'b-', label='prey')

        ax1.set_title("Dynamic System in time")
        ax1.set_xlabel("Time")
        ax1.grid()
        ax1.legend(loc='best')

        ax2.plot(self.x, self.y, color="blue")
        ax2.set_xlabel("Predator")
        ax2.set_ylabel("Prey")
        ax2.set_title("Phase Space")
        ax2.grid()

        fig1.savefig(filename, dpi=150)

    def find_equilibrium(self, r):

        """Computing Equilibrium by linearizing the equations and return a list of equilibrium points"""

        for self.x in range(r):
            for self.y in range(r):
                if (self.f(self.x, self.y) == 0) and (self.g(self.x, self.y) == 0):
                    self.equilibria.append((self.x, self.y))
                    print('The system has a equilibrium in (%s,%s)' % (self.x, self.y))
        return self.equilibria

    def plot_nullcline(self, filename='Quiverplot with Nullclines'):
        """
        
        Nullcline Analysis

        """
        fig2 = plt.figure(figsize=(8, 6))
        ax3 = fig2.add_subplot(1, 1, 1)

        # self.x = np.linspace(0, 2, 20)
        # self.y = np.arange(0, 2, 20)

        """plot nullclines"""
        a = self.x
        b = self.alpha - self.x
        ax3.plot(a, b, 'r-', lw=2)  # , label='x-nullcline')
        ax3.axvline(x=0, color='r', lw=2, label='x-nullcline')
        ax3.axhline(y=0, color='b', lw=2)  # , label ='y-nullcline')
        ax3.axvline(x=self.beta, color='b', lw=2, label='y-nullcline')

        """plot equilibrium points"""

        for point in self.equilibria:
            ax3.plot(point[0], point[1], "red", marker="o", markersize=10.0)
        ax3.set_title("Quiverplot with Nullclines")
        ax3.legend(loc='best')

        """define a grid and compute direction at each point"""
        # self.x = np.linspace(0, 2, 20)
        # self.y = np.linspace(0, 2, 20)

        X1, Y1 = np.meshgrid(self.x, self.y)  # create a grid
        # X1, Y1 = self.x, self.y
        DX1, DY1 = self.logistic_sys()  # compute growth rate on the grid
        M = (np.hypot(DX1, DY1))  # norm growth rate
        M[M == 0] = 1.  # avoid zero division errors
        DX1 /= M  # normalize each arrows
        DY1 /= M

        ax3.quiver(X1, Y1, DX1, DY1)
        ax3.legend()
        ax3.grid()
        fig2.savefig(filename, dpi=150)

    def eigenvalues(self):

        for x, y in self.equilibria:

            """Calculating Jacobian for each equilibrium point"""

            # alpha*x - x**2 - x*y
            a11 = self.alpha - 2 * x - y  # differentiated with respect to x
            a12 = - x  # differentiated with respect to y
            # - beta*y + x*y
            a21 = y  # differentiated with respect to x
            a22 = - self.beta + x  # differentiated with respect to y

            """Calculating and trace and determinant of Jacobian"""

            tr = a11 + a22
            det = a11 * a22 - a12 * a21

            """Calculating Eigen Values"""

            lambda1 = (tr - sqrt(tr ** 2 - 4 * det)) / 2
            lambda2 = (tr + sqrt(tr ** 2 - 4 * det)) / 2
            print('Check the equilibrium point  (%s, %s)' % (x, y))
            print('The real part of the first eigenvalue is %s' % lambda1.real)
            print('The real part of the second eigenvalue is %s' % lambda2.real)

            """Checking the stability of each equilibrium point with respect to the sign of their eigen values"""

            if lambda1.real < 0 and lambda2.real < 0:
                print('The equilibrium in (%s, %s) is a sink. It is stable' % (x, y))
            if lambda1.real > 0 and lambda2.real > 0:
                print('The equilibrium in (%s, %s) is a source. It is unstable' % (x, y))
            if lambda1.real > 0 and lambda2.real < 0:
                print('The equilibrium in (%s, %s) is a saddle. It is unstable' % (x, y))
            if lambda1.real < 0 and lambda2.real > 0:
                print('The equilibrium in (%s, %s) is unstable' % (x, y))
            print('----------------------------')


if __name__ == "__main__":
    iv_x = 10
    iv_y = 2
    alpha = 2
    beta = 1
    dt = 0.01
    time = 1000
    L = Lotka_Volterra(iv_x, iv_y, alpha, beta, dt, time)
    L.initial_value(iv_x, iv_y)
    L.logistic_sys()
    L.plot_system()

    equilibria = L.find_equilibrium(10)
    L.eigenvalues()
