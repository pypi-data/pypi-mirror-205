# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:43:58 2023

@author: qq102
"""
import shap
import logging
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class SHAPValueConduct:
    def __init__(self, explainer,X_input,y_input):
        self.explainer = explainer
        self.X_input=X_input
        self.y_input=y_input
    def shap_value_conduct(self):  
        self.shap_values = self.explainer.shap_values(self.X_input)
        return self.shap_values
    
    def save_shap_values(self, X_predict_input,shap_value_input,X_input,y_input, type_class,save_path,file_name,gene_ID):
        
        
        X_shap_save = pd.DataFrame(shap_value_input, columns=X_input.columns, index=X_input.index)
        X_shap_save = X_shap_save.join(y_input, how="inner")
        X_shap_save = X_shap_save.join(X_predict_input, how="inner")
        file_path = f"{save_path}/{file_name}_{type_class}_shap_value.csv"
        X_shap_save.to_csv(file_path, index_label=gene_ID)
        return X_shap_save
        

    def Shapley_value_save(self,X_predict_input,type_class,save_path,file_name="train",gene_ID='ID'):
        logging.warning('Please ensure that the type entered for the type_class parameter matches the type of the model default classification,\
                        otherwise the results may be inaccurate!')
        X_shap_save=list(map(lambda x,y:self.save_shap_values(X_predict_input,\
                                    self.shap_values[y],self.X_input,self.y_input,x,save_path,file_name,gene_ID),type_class,range(len(type_class))))
        X_shap_save=dict(zip(type_class,X_shap_save))
        return X_shap_save


class ShapInteractionIndexConduct:
    
    def __init__(self, frac_num, tree_limit_num, explainer, shap_plot_figure_size):
        self.frac_num = frac_num
        self.tree_limit_num = tree_limit_num
        self.explainer = explainer
        self.shap_plot_figure_size = shap_plot_figure_size
    
    def plot_shap_interaction_index_values(self, shap_interaction_values, X_input, class_names, file_name, save_path):
        
        
        shap.summary_plot(shap_interaction_values, X_input, 
                           plot_size=self.shap_plot_figure_size, show=False, max_display=10)
        
        
        plt.savefig(save_path + file_name + "_" + class_names  + "_shap_interaction.png",
                    dpi=1000, bbox_inches="tight")
        plt.savefig(save_path + file_name + "_" + class_names  + "_shap_interaction.pdf",
                    dpi=1000, bbox_inches="tight")
        plt.close()

    def save_shap_interaction_index(self, shap_interaction_values, X_random, file_name, save_path,type_class):
        for i, value in enumerate(type_class):
            self.plot_shap_interaction_index_values(shap_interaction_values[i], X_random, value,  file_name, save_path)

            shap_interaction_data = pd.DataFrame(shap_interaction_values[i][0,:,:],
                                                       index=X_random.columns, columns=X_random.columns)
            shap_interaction_data['feature_max'] = shap_interaction_data.apply(lambda x: sorted(abs(x))[-2], axis='columns')
            shap_interaction_data.to_csv(save_path + file_name + "_" + value + "_dim0_shap_interaction.csv", index_label='feature_name')

            shap_interaction_abs = pd.DataFrame(np.abs(shap_interaction_values[i]).sum(0),
                                                      index=X_random.columns, columns=X_random.columns)
            shap_interaction_abs.to_csv(save_path  + file_name + "_" + value + "_shap_interaction_abs.csv", index_label='feature_name')

        shap_interaction_values_all = dict(zip(type_class, shap_interaction_values))
        X_random.to_csv(save_path + file_name + "_feature_random.csv", index_label='ID')
        np.save(save_path + file_name + "_shap_interaction_all.npy", shap_interaction_values_all)

    def conduct(self, X_input, file_name, save_path, type_class):
        logging.warning('Please ensure that the type entered for the type_class parameter matches the type of the model default classification,\
                        otherwise the results may be inaccurate!')

        X_random = X_input.sample(frac=self.frac_num, replace=False, random_state=0, axis=0)
        shap_interaction_values = self.explainer.shap_interaction_values(X_random, tree_limit=self.tree_limit_num)

        self.save_shap_interaction_index(shap_interaction_values, X_random, file_name, save_path,type_class)


