# import libraries
import sys
import pickle
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import  AdaBoostClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report


def load_data(data_filepath='./data/clean_data.pickle'):
    """
    load data from file
    :param data_filepath: (str)
    :return: (pd.Series)features, (pd.DataFrame)labels, (pd.columns)category names
    """
    with open(data_filepath, 'rb') as f:
        df = pickle.load(f)
    X = df.drop(['person', 'offer_received_time', 'offerId', 'time_btw_rec_view',
                 'time_btw_rec_cmpt', 'offer_viewed', 'offer_completed',
                 'time_btw_rec_cmpt_valid', 'time_btw_rec_view_valid',
                 'viewed_before_completed', 'age', 'became_member_on', 'income'], axis=1)
    # Scale X to 0-1
    min_max_scaler = MinMaxScaler()
    X = min_max_scaler.fit_transform(X)
    Y = df.loc[:, ['offer_completed', 'viewed_before_completed']]
    category_names = Y.columns
    return X, Y, category_names


def build_model():
    """
    Build pipeline and use grid search to find better parameters.
    :return: (GridSearchCV)
    """
    pipeline = Pipeline([
        ('scaler', MinMaxScaler()),
        ('clf', MultiOutputClassifier(AdaBoostClassifier()))
    ])

    parameters = {
        'clf__estimator__n_estimators': [100, 200, 300],
        'clf__estimator__learning_rate': [0.8, 0.9, 1.0]
    }

    cv = GridSearchCV(pipeline, param_grid=parameters)
    return cv


def evaluate_model(model, X_test, Y_test, category_names):
    """
    Show the accuracy, precision, and recall of the tuned model.
    :param model:(sklearn.pipeline.Pipeline)
    :param X_test: (pd.Series)test features
    :param Y_test:(pd.DataFrame)test labels
    :param category_names:(pd.columns)category names
    :return:None
    """
    Y_pred = model.predict(X_test)
    overall_accuracy = (Y_pred == Y_test).mean().mean()
    print('Average overall accuracy {0:.2f}% \n'.format(overall_accuracy * 100))
    y_pred_pd = pd.DataFrame(Y_pred, columns=category_names)
    for column in category_names:
        print('------------------------------------------------------\n')
        print('category: {}\n'.format(column))
        print(classification_report(Y_test[column], y_pred_pd[column]))
    return


def save_model(model, model_filepath='model.pickle'):
    """
    Export the model as a pickle file
    :param model:(sklearn.pipeline.Pipeline)
    :param model_filepath:(str)
    :return:None
    """
    with open(model_filepath, "wb") as file:
        pickle.dump(model, file)
    return


def main():
    if len(sys.argv) == 3:
        data_filepath, model_filepath = sys.argv[1:]

    else:
        print('Using the default data (./data/clean_data.pickle). '\
              'You can provide the data filepath as the first argument '\
              'and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ./data/clean_data.pickle model.pickle')
        data_filepath = './data/clean_data.pickle'
        model_filepath = 'model.pickle'

    print('Loading data...\n    DATA: {}'.format(data_filepath))
    try:
        X, Y, category_names = load_data(data_filepath)
    except Exception as e:
        print("Loading data failed. Please check the data filepath.")

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

    print('Building model...')
    model = build_model()

    print('Training model...')
    model.fit(X_train, Y_train)

    print('Evaluating model...')
    evaluate_model(model, X_test, Y_test, category_names)

    print('Saving model...\n    MODEL: {}'.format(model_filepath))
    save_model(model, model_filepath)

    print('Trained model saved!')


if __name__ == '__main__':
    main()
