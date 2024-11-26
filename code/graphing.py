import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.use("Agg")

# === Documentation of graphing.py ===


def viewBudget(data):
    sorted_data = {}
    sorted_data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1])}
    values = []
    labels = []
    for k, v in sorted_data.items():
        values.append(v)
        labels.append(k)
    plt.pie(values, labels=values, counterclock=False, shadow=True)
    plt.title("Category Wise Budget")
    plt.legend(labels, loc="center")
    plt.savefig("budget.png", bbox_inches="tight")
    plt.close()


def addlabels(x, y):
    """
    addlabels(x, y): This function is used to add the labels to the graph.
    It takes the expense values and adds the values inside the bar graph for each expense type
    """
    for i in range(len(x)):
        plt.text(i, y[i] // 2, y[i], ha="center")


def visualize(total_text, monthly_budget):
    """
    visualize(total_text): This is the main function used to implement the graphing
    part of display feature. This file is called from display.py, and takes the user
    expense as a string and creates a dictionary which in turn is fed as input matplotlib to create the graph
    """
    n1 = len(monthly_budget)
    r1 = np.arange(n1)
    width = 0.45
    total_text_split = [line for line in total_text.split("\n") if line.strip() != ""]
    monthly_budget_str = ""
    for key, value in monthly_budget.items():
        monthly_budget_str += str(key) + " $" + str(value) + "\n"
    monthly_budget_split = [
        line for line in monthly_budget_str.split("\n") if line.strip() != ""
    ]

    monthly_budget_categ_val = {}
    for j in monthly_budget_split:
        x = j.split(" ")
        x[1] = x[1].replace("$", "")
        monthly_budget_categ_val[x[0]] = float(x[1])

    categ_val = {key: 0 for key in monthly_budget_categ_val}
    for i in total_text_split:
        a = i.split(" ")
        a[1] = a[1].replace("$", "")
        categ_val[a[0]] = float(a[1])

    x = list(categ_val.keys())
    y = list(categ_val.values())
    n2 = len(x)
    r2 = np.arange(n2)
    plt.bar(r2, categ_val.values(), width=width, label="your spendings")
    plt.bar(
        r1 + width, monthly_budget_categ_val.values(), width=width, label="your budget"
    )
    addlabels(x, y)

    plt.ylabel("Expenditure")
    plt.xlabel("Categories")
    plt.xticks(r1 + width / 2, monthly_budget_categ_val.keys(), rotation=90)
    plt.legend()
    plt.savefig("expenditure.png", bbox_inches="tight")
    plt.close()

def visualize_pie_chart(total_dict):
    """
    Generate a pie chart for the spending data from a dictionary input.
    total_dict: A dictionary where keys are categories and values are spending amounts.
    """
    categories = list(total_dict.keys())
    amounts = list(total_dict.values())

    # Check if there's any data to plot
    if not categories or not amounts:
        raise ValueError("No data available to visualize.")

    plt.figure(figsize=(8, 8))
    plt.pie(
        amounts,
        labels=categories,
        autopct="%1.1f%%",
        startangle=140,
        colors=plt.cm.Paired.colors,
    )
    plt.title("Spending Distribution")
    plt.savefig("expenditure.png", bbox_inches="tight")
    plt.close()


def visualize_bar_with_budget(total_dict, budget_dict):
    """
    Generate a bar graph for the spending data alongside the budget data.
    total_dict: A dictionary where keys are categories and values are spending amounts (floats).
    budget_dict: A dictionary where keys are categories and values are budget amounts (floats).
    """
    # Ensure the values are numeric (float)
    categories = list(budget_dict.keys())
    spending_values = [float(total_dict.get(category, 0)) for category in categories]  # Make sure values are float
    budget_values = [float(budget_dict.get(category, 0)) for category in categories]  # Make sure values are float

    # Check if there's any data to plot
    if not categories or not spending_values or not budget_values:
        raise ValueError("No data available to visualize.")

    width = 0.35  # width of the bars
    x = np.arange(len(categories))

    plt.figure(figsize=(10, 6))
    plt.bar(x - width / 2, spending_values, width, label="Your Spendings", color="skyblue")
    plt.bar(x + width / 2, budget_values, width, label="Your Budget", color="orange")
    plt.ylabel("Amount ($)")
    plt.xlabel("Categories")
    plt.title("Spending vs Budget by Category")
    plt.xticks(x, categories, rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig("expenditure.png", bbox_inches="tight")
    plt.close()


def visualize_bar_without_budget(total_dict):
    """
    Generate a bar graph for the spending data without considering the budget.
    total_dict: A dictionary where keys are categories and values are spending amounts.
    """
    categories = list(total_dict.keys())
    amounts = list(total_dict.values())

    # Check if there's any data to plot
    if not categories or not amounts:
        raise ValueError("No data available to visualize.")

    plt.figure(figsize=(10, 6))
    plt.bar(categories, amounts, color="skyblue", alpha=0.7)
    plt.ylabel("Expenditure ($)")
    plt.xlabel("Categories")
    plt.title("Spending by Category (Without Budget)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("expenditure.png", bbox_inches="tight")
    plt.close()

def visualize_bar_graph(months, spending_values):
    """
    Visualize monthly expenses comparison using a bar chart.
    months: List of month labels (e.g., 'Nov-2024', 'Dec-2024')
    spending_values: List of total spending amounts for each month
    """
    plt.figure(figsize=(10, 6))
    x = np.arange(len(months))  # Position of the bars

    plt.bar(x, spending_values, width=0.6, color="skyblue", label="Monthly Expenses")
    plt.ylabel("Amount ($)")
    plt.xlabel("Month")
    plt.title("Monthly Expenses Comparison")
    plt.xticks(x, months, rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("expenditure.png", bbox_inches="tight")
    plt.close()
    
def visualize_line_chart(months, spending_values):
    """
    Visualize monthly expenses trend using a line chart.
    months: List of month labels (e.g., 'Nov-2024', 'Dec-2024')
    spending_values: List of total spending amounts for each month
    """
    plt.figure(figsize=(10, 6))
    plt.plot(months, spending_values, marker='o', color='skyblue', label="Monthly Expenses")
    
    plt.ylabel("Amount ($)")
    plt.xlabel("Month")
    plt.title("Monthly Expenses Trend")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("expenditure.png", bbox_inches="tight")
    plt.close()
