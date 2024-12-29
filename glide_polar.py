import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class GlidePolar:
    velocity_kmh = []
    sink_rate= []
    velocity_ms = []
    glide_ratio= []

    def __init__(self, velocity_kmh: list, sink_rate: list):
        '''
        Five values required in each list: min sink, trim, 1/3 speedbar, 2/3 speedbar, and full bar
        '''
        assert(len(velocity_kmh) == 5)
        assert(len(sink_rate) == 5)

        self.velocity_kmh = velocity_kmh
        self.sink_rate = sink_rate
        self.velocity_ms = [vel/3.6 for vel in self.velocity_kmh]
        self.glide_ratio = [abs(v/s) for v, s in zip(self.velocity_ms, self.sink_rate)]

    def velocity_idx_to_speedbar(index):
        '''
        Convert an index in a 
        '''
        if index == 0:
            return "Min Sink"
        elif index == 1:
            return "Trim"
        elif index == 2:
            return "1/3 Bar"
        elif index == 3:
            return "2/3 Bar"
        elif index == 4:
            return "Full Bar"
        else:
            return "Invalid Index"
        
    def plot_curves(self):
        fig = plt.figure()
        gs = fig.add_gridspec(2, hspace=0)
        ax_top, ax_bottom = gs.subplots(sharex=True)

        ax_top.plot(self.velocity_kmh, self.sink_rate)
        ax_top.set_ylabel("Sink Rate")
        ax_bottom.plot(self.velocity_kmh, self.glide_ratio)
        ax_bottom.set_ylabel("Glide Ratio")
        ax_bottom.set_xlabel("Velocity Km/h")
        ax_top.grid(True, linestyle='-.')
        ax_bottom.grid(True, linestyle='-.')

        ax_top.set_title("Polar Curves")

    def plot_polar(self, ax, color = None, label = None):
        ax.plot(self.velocity_kmh, self.sink_rate, "o-", color = color, label = label)
        ax.set_ylabel("Sink Rate")
        ax.set_xlabel("Velocity Km/h")
        ax.grid(True, linestyle='-.')


    def plot_glide(self, ax, color = None, label = None):
        ax.plot(self.velocity_kmh, self.glide_ratio, "o-", color = color, label = label)
        ax.set_ylabel("Glide Ratio")
        ax.set_xlabel("Velocity Km/h")
        ax.grid(True, linestyle='-.')
