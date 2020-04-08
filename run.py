import sys
import json
import math
import pandas as pd
from sklearn.externals import joblib


def load_data(filepath="input.json"):
    """
    load data from file
    :param filepath:(str)
    :return:(dict)x
    """
    # load portfolio data
    portfolio = pd.read_json('data/portfolio.json', orient='records', lines=True)
    # load input
    with open(filepath, "rb") as f:
        x_input = json.load(f)
    x_portfolio = portfolio[portfolio['id'] == x_input['portfolio_id']]
    # initialize x
    x = {
        "difficulty": int(x_portfolio['difficulty']),
        "duration": int(x_portfolio['duration']),
        "reward": int(x_portfolio['reward']),
        "email": 0,
        "social": 0,
        "web": 0,
        "mobile": 0,
        "offer_type_bogo": 0,
        "offer_type_discount": 0,
        "offer_type_informational": 0,
        "age_1.0": 0,
        "age_2.0": 0,
        "age_3.0": 0,
        "age_4.0": 0,
        "age_5.0": 0,
        "age_6.0": 0,
        "age_7.0": 0,
        "age_8.0": 0,
        "age_9.0": 0,
        "age_10.0": 0,
        "became_member_year_2013": 0,
        "became_member_year_2014": 0,
        "became_member_year_2015": 0,
        "became_member_year_2016": 0,
        "became_member_year_2017": 0,
        "became_member_year_2018": 0,
        "gender_F": 0,
        "gender_M": 0,
        "gender_O": 0,
        "income_3.0": 0,
        "income_4.0": 0,
        "income_5.0": 0,
        "income_6.0": 0,
        "income_7.0": 0,
        "income_8.0": 0,
        "income_9.0": 0,
        "income_10.0": 0,
        "income_11.0": 0,
        "income_12.0": 0
    }
    # update channel values
    for channel in ['email', 'mobile', 'social', 'web']:
        if channel in x_portfolio['channels'][0]:
            x[channel] = 1
    # update offer_type values
    for offer_type in portfolio['offer_type']:
        if offer_type == x_portfolio['offer_type'][0]:
            x["offer_type_" + offer_type] = 1
    # update age values
    if 0 < x_input['age'] < 110 :
        age = str(int(math.floor(x_input['age'] / 10)))
        x['age_' + age + '.0'] = 1
    # update gender values
    if x_input['gender'] in ['F', 'M', 'O']:
        x['gender_' + x_input['gender']] = 1
    # update income values
    if 30000 <= x_input['income'] < 130000:
        income = str(int(math.floor(x_input['income'] / 10000)))
        x['income_' + income + '.0'] = 1

    return x


def predict_results(model_filepath, x):
    """
    Load model and predict
    :param model_filepath: (str)
    :param x: (dict)input
    :return: (dict)output
    """
    x = pd.DataFrame(x, index=[0])
    # load model
    model = joblib.load("model.pickle")
    # predict
    pred = model.predict(x)
    # output results
    results = dict(zip(["offer_completed", "viewed_before_completed"], pred[0]))
    return results


def main():
    if len(sys.argv) == 4:
        model_filepath, input_filepath, result_filepath = sys.argv[1:]

    else:
        print('Using the default model (model.pickle). '\
              'You can provide the model filepath as the first argument, '\
              'the filepath of the input json file to '\
              'and the filepath of the txt file to '\
              'save the resualt to as the second argument.\n\nExample: python '\
              'run.py model.pickle input.json result.txt')
        model_filepath = 'model.pickle'
        input_filepath = 'input.json'
        result_filepath = 'result.txt'

    x = load_data(input_filepath)
    results = predict_results(model_filepath, x)
    print("predict results: \n {}".format(results))
    with open(result_filepath, 'w', encoding='utf-8') as file:
        file.write(str(results))


if __name__ == '__main__':
    main()
