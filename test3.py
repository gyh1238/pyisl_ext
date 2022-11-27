import pickle as pkl
import pandas as pd

# with open("./data/STARLINK_CenterSat_temp", "rb") as f1:
#     object1 = pkl.load(f1)
# df = pd.DataFrame(object1)
# df.to_csv(r'./data/STARLINK_CenterSat_temp.csv')
#
# with open("./data/STARLINK_POS_temp", "rb") as f2:
#     object2 = pkl.load(f2)
# df = pd.DataFrame(object2)
# df.to_csv(r'./data/STARLINK_POS_temp.csv')
#
# with open("./data/STARLINK_Center_temp", "rb") as f3:
#     object3 = pkl.load(f3)
# df = pd.DataFrame(object3)
# df.to_csv(r'./data/STARLINK_Center_temp.csv')
#
# with open("./data/STARLINK_Cluster_temp", "rb") as f4:
#     object4 = pkl.load(f4)
# df = pd.DataFrame(object4)
# df.to_csv(r'./data/STARLINK_Cluster_temp.csv')

with open("./data/STARLINK_CenterSat_POS_temp", "rb") as f5:
    object5 = pkl.load(f5)
df = pd.DataFrame(object5)
df.to_csv(r'./data/STARLINK_CenterSat_POS_temp.csv')