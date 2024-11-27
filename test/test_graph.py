from code import graphing
import numpy as np

dummy_total_text_none = ""
dummy_total_text_data = """Food $10.0
Transport $50.0
Shopping $148.0
Miscellaneous $47.93
Utilities $200.0
Groceries $55.21\n"""

dummy_x = ["Food", "Transport", "Shopping", "Miscellaneous", "Utilities", "Groceries"]
dummy_y = [10.0, 50.0, 148.0, 47.93, 200.0, 55.21]
dummy_categ_val = {
    "Food": 10.0,
    "Transport": 50.0,
    "Shopping": 148.0,
    "Miscellaneous": 47.93,
    "Miscellaneous": 47.93,
    "Utilities": 200.0,
    "Groceries": 55.21,
}
dummy_color = [
    (1.00, 0, 0, 0.6),
    (0.2, 0.4, 0.6, 0.6),
    (0, 1.00, 0, 0.6),
    (1.00, 1.00, 0, 1.00),
]
dummy_edgecolor = "blue"
dummy_monthly_budget = {
    "Food": 100.0,
    "Transport": 150.0,
    "Shopping": 150.0,
    "Miscellaneous": 50,
    "Utilities": 200.0,
    "Groceries": 100,
}

dummy_pie_chart = {
    "food": 10.0,
    "transport": 50.0,
    "shopping": 148.0,
    "miscellaneous": 47.93,
    "utilities": 200.0,
    "groceries": 55.21,
}
dummy_budget_dict = {
    "food": 100.0,
    "transport": 150.0,
    "shopping": 150.0,
    "miscellaneous": 50,
    "utilities": 200.0,
    "groceries": 100,
}

dummy_months = ["January", "February", "March", "April", "May", "June"]
dummy_spendings = [100, 200, 300, 400, 500, 600]

n2 = len(dummy_x)
r2 = np.arange(n2)
width = 0.45


def test_visualize(mocker):
    mocker.patch.object(graphing, "plt")
    graphing.plt.bar.return_value = True
    graphing.visualize(dummy_total_text_data, dummy_monthly_budget)
    # graphing.plt.bar.assert_called_with(r2,
    # ANY, width=width, label='your spendings')


def test_visualize_pie_chart(pc):
    pc.patch.object(graphing, "plt")
    graphing.plt.pie.return_value = True
    graphing.visualize_pie_chart(dummy_pie_chart)
    graphing.plt.pie.assert_called_with(
        dummy_y,
        labels=dummy_x,
        colors=dummy_color,
        autopct="%1.1f%%",
        startangle=140,
        wedgeprops={"edgecolor": dummy_edgecolor, "linewidth": 1.5},
    )
    graphing.plt.show.assert_called_once()
    graphing.plt.close.assert_called_once()
    graphing.plt.savefig.assert_called_once_with(
        "expenditure_pie_chart.png", bbox_inches="tight"
    )


def test_visualize_bar_with_budget(mocker):
    mocker.patch.object(graphing, "plt")
    graphing.plt.bar.return_value = True
    graphing.visualize_bar_with_budget(dummy_pie_chart, dummy_budget_dict)
    graphing.plt.bar.assert_called_with(
        r2, dummy_categ_val.values(), width=width, label="your spendings"
    )
    graphing.plt.bar.assert_called_with(
        r2 + width, dummy_monthly_budget.values(), width=width, label="your budget"
    )
    graphing.plt.xticks.assert_called_with(
        r2 + width / 2, dummy_monthly_budget.keys(), rotation=90
    )
    graphing.plt.legend.assert_called_once()
    graphing.plt.savefig.assert_called_once_with("expenditure.png", bbox_inches="tight")
    graphing.plt.close.assert_called_once()


def test_visualize_bar_without_budget(mocker):
    mocker.patch.object(graphing, "plt")
    graphing.plt.bar.return_value = True
    graphing.visualize_bar_without_budget(dummy_pie_chart)
    graphing.plt.bar.assert_called_with(
        r2, dummy_categ_val.values(), width=width, label="your spendings"
    )
    graphing.plt.xticks.assert_called_with(r2, dummy_categ_val.keys(), rotation=90)
    graphing.plt.legend.assert_called_once()
    graphing.plt.savefig.assert_called_once_with("expenditure.png", bbox_inches="tight")
    graphing.plt.close.assert_called_once()


def test_visualize_bar_graph(mocker):
    mocker.patch.object(graphing, "plt")
    graphing.plt.bar.return_value = True
    graphing.visualize_bar_graph(dummy_months, dummy_spendings)
    graphing.plt.bar.assert_called_with(
        r2, dummy_categ_val.values(), width=width, label="your spendings"
    )
    graphing.plt.xticks.assert_called_with(r2, dummy_categ_val.keys(), rotation=90)
    graphing.plt.legend.assert_called_once()
    graphing.plt.savefig.assert_called_once_with("expenditure.png", bbox_inches="tight")
    graphing.plt.close.assert_called_once()


def test_visualize_line_chart(mocker):
    mocker.patch.object(graphing, "plt")
    graphing.plt.plot.return_value = True
    graphing.visualize_line_chart(dummy_months, dummy_spendings)
    graphing.plt.plot.assert_called_with(
        dummy_months, dummy_spendings, marker="o", color="b"
    )
    graphing.plt.xticks.assert_called_with(r2, dummy_categ_val.keys(), rotation=90)
    graphing.plt.legend.assert_called_once()
    graphing.plt.savefig.assert_called_once_with("expenditure.png", bbox_inches="tight")
    graphing.plt.close.assert_called_once()
