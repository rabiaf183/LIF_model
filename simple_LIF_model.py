# Imports
import numpy as np
import matplotlib.pyplot as plt
# @markdown Execute this code to initialize the default parameters

def default_pars(**kwargs):
  pars = {}

  # typical neuron parameters#
  pars['V_th'] = -55.     # spike threshold [mV]
  pars['V_reset'] = -75.  # reset potential [mV]
  pars['tau_m'] = 10.     # membrane time constant [ms]
  pars['g_L'] = 10.       # leak conductance [nS]
  pars['V_init'] = -75.   # initial potential [mV]
  pars['E_L'] = -75.      # leak reversal potential [mV]
  pars['tref'] = 2.       # refractory time (ms)

  # simulation parameters #
  pars['T'] = 400.  # Total duration of simulation [ms]
  pars['dt'] = .1   # Simulation time step [ms]

  # external parameters if any #
  for k in kwargs:
    pars[k] = kwargs[k]

  pars['range_t'] = np.arange(0, pars['T'], pars['dt'])  # Vector of discretized time points [ms]

  return pars


pars = default_pars()
print(pars)

def plot_volt_trace(pars, v, sp):
    t = pars['range_t']                      # Time axis (0 → T ms)
    plt.figure()
    plt.plot(t, v, lw=1)                     # Plot voltage vs time

    # Optional: mark spike times as dashed vertical lines
    if len(sp):
        ymin, ymax = v.min() - 5, v.max() + 5
        plt.vlines(sp, ymin, ymax, linestyles='dashed', linewidth=0.8)

    plt.xlabel('Time [ms]')
    plt.ylabel('Membrane potential [mV]')
    plt.title('LIF voltage trace')
    plt.tight_layout()
    plt.show()

def run_LIF(pars, Iinj, stop=False):
  """
  Simulate the LIF dynamics with external input current

  Args:
    pars       : parameter dictionary
    Iinj       : input current [pA]. The injected current here can be a value
                 or an array
    stop       : boolean. If True, use a current pulse

  Returns:
    rec_v      : membrane potential
    rec_sp     : spike times
  """

  # Set parameters
  V_th, V_reset = pars['V_th'], pars['V_reset']
  tau_m, g_L = pars['tau_m'], pars['g_L']
  V_init, E_L = pars['V_init'], pars['E_L']
  dt, range_t = pars['dt'], pars['range_t']
  Lt = range_t.size
  tref = pars['tref']

  # Initialize voltage
  v = np.zeros(Lt) #400-0/0.1=4000
  v[0] = V_init # initalize first value with V_init

  # Set current time course
  Iinj = Iinj * np.ones(Lt) # range is 4000 so if Iinj=200 then it becomes array of 200s of size 4000

  # If current pulse, set beginning and end to 0
  if stop:
    Iinj[:int(len(Iinj) / 2) - 1000] = 0 # first half -1000 values are 0
    Iinj[int(len(Iinj) / 2) + 1000:] = 0# last half -1000 values are 0


    # Loop over time
  rec_spikes = []  # record spike times
  tr = 0.  # the count for refractory duration

  for it in range(Lt - 1):

    if tr > 0:  # check if in refractory period
      v[it] = V_reset  # set voltage to reset
      tr = tr - 1 # reduce running counter of refractory period

    elif v[it] >= V_th:  # if voltage over threshold
      rec_spikes.append(it)  # record spike event
      v[it] = V_reset  # reset voltage
      tr = tref / dt  # set refractory counter

    dv_dt = (-(v[it] - E_L) + Iinj[it] / g_L) / tau_m
    dv    = dt * dv_dt
    dv = dt * dv_dt
    v[it + 1] = v[it] + dv
    # Get spike times in ms
  rec_spikes = np.array(rec_spikes) * dt

  return v, rec_spikes


# Get parameters
pars = default_pars(T=500)

# Simulate LIF model
v, sp = run_LIF(pars, Iinj=100, stop=True)

# Visualize
plot_volt_trace(pars, v, sp)



