import matplotlib.pyplot as plt
import matplotlib
import pickle as pkl
import pandas as pd

f = open("./input/ra_fit_info.pkl","rb")
data = pkl.load(f)
f.close()

fit_info = {"fit_bias":[],"uncertainty":[],"mean_gamma_e":[],"source":[]}
for key in data.keys():
    fit_info["source"].append(key)
    for s_key in fit_info.keys():
        if s_key in data[key].keys():
            fit_info[s_key].append(data[key][s_key])
fit_info = pd.DataFrame(fit_info)
fit_info = fit_info.sort_values(by="mean_gamma_e",ascending=True).reset_index(drop=True)
print(fit_info)

fig,ax = plt.subplots()
plt.errorbar(fit_info["mean_gamma_e"].to_numpy(),
        fit_info["fit_bias"].to_numpy(),
        fit_info["uncertainty"],
        fmt="o",color="black",linewidth=1.5)

# plot text
texts = {
        "Ge68":{"name":"$^{68}Ge$","delta_x":0,"delta_y":-2*fit_info["uncertainty"][0],"v_align":"top"},
        "Cs137":{"name":"$^{137}Cs$","delta_x":0,"delta_y":2*fit_info["uncertainty"][1],"v_align":"bottom"},
        "Mn54":{"name":"$^{54}Mn$","delta_x":0,"delta_y":-5*fit_info["uncertainty"][2],"v_align":"top"},
        "Co60":{"name":"$^{60}Co$","delta_x":0,"delta_y":-5*fit_info["uncertainty"][3],"v_align":"top"},
        "K40":{"name":"$^{40}K$","delta_x":0,"delta_y":2*fit_info["uncertainty"][4],"v_align":"bottom"},
        "n_delay":{"name":"n-H","delta_x":0.0,"delta_y":-1.1*fit_info["uncertainty"][5],"v_align":"top"},
        "n_prompt":{"name":"$^{16}O^{*}$","delta_x":0,"delta_y":fit_info["uncertainty"][6],"v_align":"bottom"}
}
for index in range(len(fit_info["source"])):
    source = fit_info["source"][index]
    plt.text(
            fit_info["mean_gamma_e"][index] + texts[source]["delta_x"],
            fit_info["fit_bias"][index] + texts[source]["delta_y"],
            texts[source]["name"],
            fontsize=12,
            horizontalalignment = "center",
            verticalalignment = texts[source]["v_align"]
            )
plt.grid(axis="y")
plt.xlabel("$E^{\gamma}$ [MeV]",fontsize=16)
plt.ylabel("Bias [%]",fontsize=16)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14)
ax.set_xscale("log")
ax.set_xticks([0.5,1,5])
ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
plt.tight_layout()
fig_path = "../result/nonlinearity/fig/fitting_bias.eps"
plt.savefig(fig_path)
print("Fig save to %s"%(fig_path))
plt.show()
