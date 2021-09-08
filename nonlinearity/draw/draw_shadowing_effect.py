import matplotlib.pyplot as plt
import pickle as pkl
import pandas as pd

f = open("./input/shadowing_info.pkl","rb")
data = pkl.load(f)
f.close()

shadowing_info = {"shadowing":[],"uncertainty":[],"mean_gamma_e":[],"source":[]}
for key in data.keys():
    shadowing_info["source"].append(key)
    for s_key in shadowing_info.keys():
        if s_key in data[key].keys():
            shadowing_info[s_key].append(data[key][s_key])
shadowing_info = pd.DataFrame(shadowing_info)
shadowing_info = shadowing_info.sort_values(by="mean_gamma_e",ascending=True).reset_index(drop=True)
print(shadowing_info)

plt.errorbar(shadowing_info["mean_gamma_e"].to_numpy(),
        shadowing_info["shadowing"].to_numpy(),
        shadowing_info["uncertainty"],
        fmt="o",color="black",linewidth=1.5)

# plot text
texts = {
        "Ge68":{"name":"$^{68}Ge$","delta_x":0,"delta_y":shadowing_info["uncertainty"][0],"v_align":"bottom"},
        "Cs137":{"name":"$^{137}Cs$","delta_x":0,"delta_y":-2*shadowing_info["uncertainty"][1],"v_align":"top"},
        "Mn54":{"name":"$^{54}Mn$","delta_x":0,"delta_y":shadowing_info["uncertainty"][2],"v_align":"bottom"},
        "Co60":{"name":"$^{60}Co$","delta_x":0,"delta_y":shadowing_info["uncertainty"][3],"v_align":"bottom"},
        "K40":{"name":"$^{40}K$","delta_x":0,"delta_y":-1.5*shadowing_info["uncertainty"][4],"v_align":"top"},
        "n_delay":{"name":"n-H","delta_x":0.3,"delta_y":0,"v_align":"bottom"},
        "n_prompt":{"name":"$^{16}O^{*}$","delta_x":-0.3,"delta_y":0,"v_align":"bottom"}
}
for index in range(len(shadowing_info["source"])):
    source = shadowing_info["source"][index]
    plt.text(
            shadowing_info["mean_gamma_e"][index] + texts[source]["delta_x"],
            shadowing_info["shadowing"][index] + texts[source]["delta_y"],
            texts[source]["name"],
            fontsize=12,
            horizontalalignment = "center",
            verticalalignment = texts[source]["v_align"]
            )
plt.grid(axis="y")
plt.xlabel("$E^{\gamma}$ [MeV]",fontsize=16)
plt.ylabel("Shadowing bias [%]",fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.ylim(-0.12,0.04)
plt.tight_layout()
fig_path = "../result/nonlinearity/fig/Shadowing_bias.eps"
plt.savefig(fig_path)
print("Fig save to %s"%(fig_path))
plt.show()
