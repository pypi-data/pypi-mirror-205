import requests
import pandas as pd
from rtichoke.rtichoke_curves.exported_functions import create_plotly_curve
from rtichoke.rtichoke_curves.send_post_request_to_r_rtichoke import create_rtichoke_curve


def create_precision_recall_curve(probs, reals, by = 0.01, stratified_by = "probability_threshold", size= None, color_values = ["#1b9e77", "#d95f02", "#7570b3", "#e7298a", "#07004D", "#E6AB02",
                "#FE5F55", "#54494B", "#006E90", "#BC96E6", "#52050A", "#1F271B", "#BE7C4D",
                "#63768D", "#08A045", "#320A28", "#82FF9E", "#2176FF", "#D1603D", "#585123"] ,url_api = "http://localhost:4242/"):
        fig = create_rtichoke_curve(
            probs, 
            reals, 
            stratified_by = stratified_by,
            url_api = url_api,
            curve = "precision_recall")
        return fig