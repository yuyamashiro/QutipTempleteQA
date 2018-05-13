import numpy as np
from qutip import *
import matplotlib.pyplot as plt

from QutipTempQA.utils.utils import *
from .dynamics import dynamics_result

def draw_observables(observables, N, Tlist, system, params, variable):


    # dictionary( values type is 2d array ) of result of observables that is specified
    result_obs = {}
    for key,_ in observables.items():
        result_obs[key] = []

    # result_obs have 2d-array(matrix) 1-axis : each T, 2-axis : each variable
    # follow two for statement is doing stuck result to result_obs
    for i,var in enumerate(variable[1]):
        obs_eachT = {}
        for key,_ in observables.items():
            obs_eachT[key] = []

        for T in Tlist:
            allparams = params
            allparams[variable[0]] = var
            sys = system(T, N, allparams)
            final_state = dynamics_result(sys, N, T, allparams)

            correct_energy, correct_state = sys.H(T).eigenstates(eigvals=1)

            # calculate observables
            for obs, path in observables.items():
                if obs == "Residual energy":
                    Eres = 1.0 / sys.N * np.abs(expect(sys.H(T), final_state) - correct_energy[0])
                    obs_eachT[obs].append(Eres)
                elif obs == "Probability of mistaking":
                    miss_prob = 1.0 - np.abs((correct_state[0].dag() * final_state).full()[0][0]) ** 2
                    obs_eachT[obs].append(miss_prob)
                else:
                    raise ValueError("Observable {} is not exist".format(obs))

        for key, value in obs_eachT.items():
            result_obs[key].append(value)

    # draw figure of result vs T
    for obs, path in observables.items():
        draw_to_figure(obs, path, result_obs[obs], Tlist, N, params, variable)


def draw_to_figure(observable, path, result_mat, Tlist, N, params, variable):
    T = max(Tlist)
    figure_path = path + filename_from(N, T, params) + '.pdf'

    plt.figure()
    plot_setting()
    plt.xlabel("$T_{Q}$ : Annealing time")
    plt.ylabel(observable)
    plt.xscale('log')
    plt.yscale('log')

    for value, result in zip(variable[1], result_mat):
        plt.plot(Tlist, result, label=variable[0]+"="+str(value))

    plt.legend()
    plt.savefig(figure_path)


