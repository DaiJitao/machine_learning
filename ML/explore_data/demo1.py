import pandas as pd
import pandas_profiling


def explore(output_file, data_file=None, ):
    if data_file == None:
        data_file = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
    data = pd.read_csv(data_file)
    print(data.describe())
    profile = data.profile_report()
    print(profile)

    profile.to_file(output_file)
    print("saved in "+ output_file)


if __name__ == '__main__':
    output_file_html = './result/titanic_report.html'
    data_file = r'F:\pycharm_workspce\dai_github\myproject\machine_learning\ML\data\titanic.csv'

    app_output_file_html = "./result/app_report.html",
    app_data_file = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\ML\data\app.csv"

    test_output_file_html = "./result/test_report.html",
    test_data_file = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\ML\data\test.csv"

    train_output_file_html = "./result/train_report.html",
    train_data_file = r"F:\pycharm_workspce\dai_github\myproject\machine_learning\ML\data\train.csv"
    explore(test_output_file_html, test_data_file)
    explore(train_output_file_html, train_data_file)
