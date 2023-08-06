# main runner
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

from amendment_forecast import utils
from amendment_forecast.models import DATE_COLUMN_NAME, VALUE_COLUMN_NAME, initialize_model
# import utils
# from models import DATE_COLUMN_NAME, VALUE_COLUMN_NAME, initialize_model

FREQUENCY_MAPPING = {
    "week": "W-MON",
    "month": "MS"
}


def get_train_end_date(time_series_df, training_holdout):
    """ Determines the start date for the test data and throws a warning if less than 1 year of training data is included
    """
    training_rows = int(len(time_series_df) * training_holdout)
    train_end_date = time_series_df.iloc[training_rows][DATE_COLUMN_NAME]

    if (train_end_date - time_series_df[DATE_COLUMN_NAME].min()).days < 365:
        print("Warning: Less than 1 year of data provided for training")

    return train_end_date


def get_forecast_periods(last_day, horizon_years, frequency) -> list:
    # Get start and end dates
    max_week = last_day.strftime("%Y %W")
    last_week_start = datetime.strptime(f"{max_week} w1", "%Y %W w%w")
    start_date = last_week_start + relativedelta(days=7)
    end_date = start_date + relativedelta(years=horizon_years)
    period_list = pd.date_range(start=start_date, end=end_date, freq=frequency)
    if frequency == "W-MON":
        # Truncate if the last week is the same as the first
        first_week_number = pd.Timestamp(period_list[0]).isocalendar()[1]
        final_week_number = pd.Timestamp(period_list[-1]).isocalendar()[1]
        drop_final_week = False
        if first_week_number not in [52, 53]:
            if final_week_number == first_week_number:
                drop_final_week = True
        else:
            # Handle forecasts that start on the last day of the year
            first_year = pd.Timestamp(period_list[0]).isocalendar()[0]
            first_year_weeks = datetime(first_year, 12, 28).isocalendar()[1]
            final_year = pd.Timestamp(period_list[-1]).isocalendar()[0]
            final_year_weeks = datetime(final_year, 12, 28).isocalendar()[1]
            if first_week_number == 52:
                if final_week_number == first_week_number:
                    # Only drop if final year doesn't have 53 weeks
                    if final_year_weeks != 53:
                        drop_final_week = True
                elif final_week_number == 53:
                    # Drop if first year doesn't have 53 weeks
                    if first_year_weeks != 53:
                        drop_final_week = True
            elif first_week_number == 53:
                if final_week_number == first_week_number:
                    # Always drop if weeks are the same
                    period_list = period_list[:-1]
                elif final_week_number == 52:
                    # Drop if final year doesn't have 53 weeks
                    if final_year_weeks != 53:
                        drop_final_week = True
        if drop_final_week:
            period_list = period_list[:-1]

    return period_list


def run_forecast_ensemble(
        dataframe,
        date_column,
        target_column,
        forecast_horizon_years,
        aggregate_operation="sum",
        training_holdout_pct=0.3,
        frequency="week",
        period_format=None,
        model_list=None,
        prediction_lag=0.0):
    # Initialize with copy of input date
    dataframe[DATE_COLUMN_NAME] = pd.to_datetime(dataframe[date_column])
    df = dataframe.copy()

    # Creates time series and ensures proper naming and frequency
    frequency = FREQUENCY_MAPPING.get(frequency)
    df = utils.create_time_series_from_records(
        df,
        target_column,
        aggregate_operation,
        period_format)
    df = df[[DATE_COLUMN_NAME, VALUE_COLUMN_NAME]]

    # Create Future Forecast Periods
    last_date = pd.to_datetime(dataframe[DATE_COLUMN_NAME]).max()
    period_list = get_forecast_periods(last_date, forecast_horizon_years, frequency)

    # Add additional period if lag is requested
    if prediction_lag != 0:
        if frequency == "W-MON":
            delta = relativedelta(days=7)
        elif frequency == "MS":
            delta = relativedelta(months=1)
        end_date = period_list[-1] + delta
        period_list = period_list.append(pd.DatetimeIndex([end_date]))

    # Mark dataframe with training/testing split
    train_end_date = get_train_end_date(df, training_holdout_pct)

    # Assemble ensemble of models
    if model_list:
        named_model_list = model_list
    else:
        named_model_list = [
            "GreyKite",
            "FBProphet",
            "Naive",
            "XGBoost",
            "RandomForest",
            "SARIMA"
        ]

    # For each model, run a full evaluation and add to the ensemble results
    ensemble = []
    for model_name in named_model_list:
        print(f"    Running --{model_name}")
        model = initialize_model(model_name)
        model_dict = model.evaluate(
            dataframe=df,
            train_end_date=train_end_date,
            frequency=frequency,
            forecast_period_list=period_list)
        weight = model_dict["performance_metrics"]["r2"] ** 2
        if weight < 0.5:
            weight = 0
        elif model_name == "Naive":
            weight = 0
            estimate_df = model_dict["forecast_dataframe"]
        model_dict["weight"] = weight
        ensemble.append(model_dict)

    # Combine outputs to calculate ensemble effectiveness
    print("Creating Ensemble")
    return_dataframe = df.copy().set_index(DATE_COLUMN_NAME)
    total_weight = sum([model["weight"] for model in ensemble])
    # If no model satisfies the threshhold, Naive is the only one used
    if total_weight == 0:
        naive_model = next((model for model in ensemble if model['name'] == "Naive"), None)

        forecast_df = naive_model["forecast_dataframe"]
        forecast_df[f"weighted_forecast_values_Naive"] = forecast_df["forecast_values_Naive"].copy()
        return_dataframe = pd.merge(
            left=return_dataframe,
            right=forecast_df,
            how="outer",
            left_index=True,
            right_index=True)

        train_df = naive_model["train_dataframe"]
        train_df["weighted_predicted_values_Naive"] = train_df["predicted_values_Naive"].copy()
        return_dataframe = pd.merge(
            left=return_dataframe,
            right=train_df,
            how="outer",
            left_index=True,
            right_index=True
        )
    else:
        for model in ensemble:
            # Replace negative values with the Naive value
            forecast_df = model["forecast_dataframe"]

            return_dataframe = pd.merge(
                left=return_dataframe,
                right=model["forecast_dataframe"],
                how="outer",
                left_index=True,
                right_index=True)
            if model["weight"] > 0:
                train_df = model["train_dataframe"]
                train_df[f"weighted_predicted_values_{model['name']}"] = train_df[f"predicted_values_{model['name']}"] * model["weight"]
                return_dataframe = pd.merge(
                    left=return_dataframe,
                    right=train_df,
                    how="outer",
                    left_index=True,
                    right_index=True)
                forecast_df[f"weighted_forecast_values_{model['name']}"] = forecast_df[f"forecast_values_{model['name']}"] * model["weight"]
                return_dataframe = pd.merge(
                    left=return_dataframe,
                    right=forecast_df[[f"weighted_forecast_values_{model['name']}"]],
                    how="outer",
                    left_index=True,
                    right_index=True)
    # Create Ensemble Predictions
    ensemble_prediction_columns = [column for column in return_dataframe.columns if column.startswith("weighted_predicted_values")]
    return_dataframe["predicted_values_Ensemble"] = return_dataframe[ensemble_prediction_columns].sum(axis=1, min_count=1) / total_weight

    # Create ensemble weighted forecast
    ensemble_forecast_columns = [column for column in return_dataframe.columns if column.startswith("weighted_forecast_values")]
    return_dataframe["forecast_values_Ensemble"] = return_dataframe[ensemble_forecast_columns].sum(axis=1, min_count=1) / total_weight
    forecast_columns = [column for column in return_dataframe.columns if column.startswith("forecast_values")]
    if prediction_lag != 0:
        return_dataframe = utils.apply_lag(return_dataframe, forecast_columns, prediction_lag)

    # Calculate ensemble metrics
    required_columns = ensemble_prediction_columns + ["y"]
    ensemble_train_df = return_dataframe.dropna(subset=required_columns)
    performance_metrics = utils.get_model_statistics(ensemble_train_df["y"], ensemble_train_df["predicted_values_Ensemble"])
    consolidated_metrics = utils.consolidate_scores(performance_metrics, ensemble_train_df["y"].mean())

    # Filter to only the required columns
    return_columns = ["y"] + forecast_columns
    return_dataframe = return_dataframe[return_columns]

    # Add ensemble to list
    ensemble.append({
        "name": "ensemble",
        "ensemble_dataframe": return_dataframe,
        "performance_metrics": performance_metrics,
        "consolidated_metrics": consolidated_metrics
    })

    # Add horizon column
    return_dataframe["prediction_date"] = return_dataframe.index.copy()
    first_prediction_date = return_dataframe["prediction_date"].min()
    return_dataframe["horizon"] = return_dataframe["prediction_date"].apply(
        lambda x: relativedelta(x, first_prediction_date).years + 1
    )

    # Create degraded accuracies for all models
    training_years = round((df[DATE_COLUMN_NAME].max() - df[DATE_COLUMN_NAME].min()).days / 365)
    for model in ensemble:
        degraded_accuracies = {}
        degraded_fit = {}
        for year in range(1, forecast_horizon_years + 1):
            multiplier = 1.0
            if year > 1:
                for yy in range(1, int(year)):
                    if yy > ((2 * training_years) + 1):
                        multiplier *= 0.5
                    else:
                        multiplier *= 0.95
            degraded_accuracies[year] = multiplier * model["consolidated_metrics"]["accuracy"]
            degraded_fit[year] = multiplier * model["consolidated_metrics"]["fit"]
        model["degraded_accuracies"] = degraded_accuracies
        model["degraded_fit"] = degraded_fit

    return ensemble
