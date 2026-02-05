
import matplotlib

# matplotlib.use("Agg")

import matplotlib.pyplot as plt
from io import BytesIO
from datetime import date, timedelta
today = date.today()

week_last_7 = []
for i in range(7):
    start = today - timedelta(weeks=i)
    week_last_7.append(start)






weeks = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
def transalanlysis(y):

    fig, ax = plt.subplots(figsize=(10, 4.5), dpi=150)


    fig.patch.set_facecolor("#020617")
    ax.set_facecolor("#020617")


    ax.bar(weeks, y, color="#22c55e", alpha=0.85, edgecolor="#0f172a")


    ax.set_title("Weekly Spend Analysis", pad=12, color="white", fontsize=14, fontweight="bold")
    ax.set_xlabel("Week Days", color="#cbd5e1")
    ax.set_ylabel("Amount", color="#cbd5e1")


    ax.tick_params(axis="x", colors="#cbd5e1")
    ax.tick_params(axis="y", colors="#cbd5e1")


    ax.grid(True, axis="y", linestyle="--", alpha=0.25)


    for spine in ax.spines.values():
        spine.set_color("#1f2937")

    buf = BytesIO()
    plt.tight_layout()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf



###################





def trans_analysis(y, a, b):
    fig2, ax2 = plt.subplots(1, 2, figsize=(16, 5), dpi=150)


    fig2.patch.set_facecolor("#020617")

    for axis in ax2:
        axis.set_facecolor("#0f172a")
        axis.grid(True, linestyle="--", alpha=0.25)
        axis.tick_params(axis="x", colors="#cbd5e1")
        axis.tick_params(axis="y", colors="#cbd5e1")

        # clean borders
        axis.spines["top"].set_visible(False)
        axis.spines["right"].set_visible(False)
        axis.spines["left"].set_color("#334155")
        axis.spines["bottom"].set_color("#334155")

 
    months = list(range(1, len(y)+1))

    max_val = max(y)
    max_index = y.index(max_val)

    colors = ["#ef4444" if v == max_val else "#38bdf8" for v in y]  # red max, blue others

    ax2[0].bar(months, y, color=colors, alpha=0.9, edgecolor="#0f172a")
    ax2[0].plot(months, y, color="#facc15", marker="o", linewidth=2, alpha=0.9)

    ax2[0].set_title("📊 Monthly Spend Analysis", color="white", fontsize=14, fontweight="bold", pad=12)
    ax2[0].set_xlabel("Days", color="#cbd5e1")
    ax2[0].set_ylabel("Spend (₹)", color="#cbd5e1")

  
    ax2[0].text(
        months[max_index],
        y[max_index] + 200,
        f"MAX ₹{y[max_index]}",
        ha="center",
        color="white",
        fontsize=9,
        fontweight="bold"
    )

 
    ax2[1].plot(week_last_7, a, color="#22c55e", marker="o", linewidth=2.5, label="Deposit")
    ax2[1].plot(week_last_7, b, color="#ef4444", marker="o", linewidth=2.5, label="Spend")

    ax2[1].fill_between(week_last_7, a, b, alpha=0.18)

    ax2[1].set_title("💰 Spend vs Deposit (Last 7 Weeks)", color="white", fontsize=14, fontweight="bold", pad=12)
    ax2[1].set_xlabel("Weeks", color="#cbd5e1")
    ax2[1].set_ylabel("Money (₹)", color="#cbd5e1")
    ax2[1].legend(facecolor="#0f172a", edgecolor="#334155", labelcolor="white")


    buf2 = BytesIO()
    plt.tight_layout()
    fig2.savefig(buf2, format="png", bbox_inches="tight", facecolor=fig2.get_facecolor())
    plt.close(fig2)
    buf2.seek(0)

    return buf2
# y=[]
# a=[]
# b=[]
# for i in range(1,8):
#     a.append(i*1000)
#     b.append(i*500)
# for i in range(1,31):
#     y.append(i*200)

# trans_analysis(y, a, b)






#############333


# def trans_analysis(y,a,b):
#     fig2,ax2 = plt.subplots(1, 2,figsize = (15,4.5))
#     max_val = max(y)
#     colors = ["red" if v == max_val else "#7768A3" for v in y]
#     ax2[0].bar(months,y,color = colors, alpha=0.85)
#     ax2[0].plot(months,y,color="#C38BA8", alpha=0.65,marker = "^")
#     ax2[0].set_title("Monthlt Spend Analysis", color = "white")
#     ax2[0].set_xlabel("DATE",color = "white")
#     ax2[0].set_ylabel("SPENDS",color = "white")
    
#     ax2[0].tick_params(axis="x", colors="#000000", labelsize=10)
#     ax2[0].tick_params(axis="y", colors="#000304", labelsize=10)

#     ax2[0].grid(True,axis = "y", linestyle = ":", alpha = 0.6,color = "white")
#     fig2.patch.set_facecolor("#A1A6BD")
    

#     #2
    
#     ax2[1].plot(week_last_7,a,color = "green",marker = "o", label = "Deposit")
#     ax2[1].plot(week_last_7,b,color = "red",marker = "o", label = "Spend")
#     ax2[1].set_xlabel("last 7 weeks")
#     ax2[1].set_ylabel("money")
#     ax2[1].set_title("SPEND VS DEPOSIT")
#     ax2[1].legend()
#     ax2[0].tick_params(axis="x", colors="#000000", labelsize=10)
#     ax2[0].tick_params(axis="y", colors="#000304", labelsize=10)
#     plt.grid(True)
    


    
   




   

    
#     buf2 = BytesIO()
#     plt.tight_layout()
 
#     fig2.savefig(buf2, format="png", bbox_inches="tight", facecolor=fig2.get_facecolor())
#     plt.close(fig2)
#     buf2.seek(0)
#     return buf2 
    



    
 

    

    



