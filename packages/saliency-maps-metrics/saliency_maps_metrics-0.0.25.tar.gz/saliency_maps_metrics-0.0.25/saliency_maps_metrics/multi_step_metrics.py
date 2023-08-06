from re import A
import sys
import numpy as np
import torch

from .data_replace import select_data_replace_method

def compute_correlation(score_var, all_sal_score_list):
    corr_list = []
    for i in range(len(score_var)):
        var_class_score = score_var[i][:,np.newaxis]
        sal_score = all_sal_score_list[i][:,np.newaxis]

        points = np.concatenate((var_class_score,sal_score),axis=-1)
        corr_list.append(np.corrcoef(points,rowvar=False)[0,1])

    corr_mean = np.array(corr_list)
    return corr_mean

def compute_auc_metric(all_score_list,cumulative=True):

    if not cumulative:
        all_score_list = all_score_list[:,1:]

    auc_list = []
    for i in range(len(all_score_list)):
        scores = all_score_list[i]
        auc = np.trapz(scores,np.arange(len(scores))/(len(scores)-1))
        auc_list.append(auc)

    auc_mean = np.array(auc_list)
    return auc_mean

class MultiStepMetric():

    def __init__(self,data_replace_method,bound_max_step=True,batch_size=20,max_step_nb=14*14,cumulative=True):

        #Set this to true to limit the maximum number of inferences computed by the metric
        #The DAUC/IAUC protocol requires one inference per pixel of the explanation map.
        #This can be prohibitive for high resolution maps like Smooth-Grad.
        #In the case of a high-resolution map (>14x14), setting this arg to True results 
        #in one inference for every few pixels removed, instead of one inference per pixel.
        self.bound_max_step = bound_max_step 
        self.max_step_nb = max_step_nb

        self.cumulative = cumulative

        self.data_replace_method = data_replace_method
        self.data_replace_func = select_data_replace_method(data_replace_method)
        self.batch_size = batch_size

    def get_masking_data(self,data):
        return self.data_replace_func(data)

    def choose_data_order(self,data,masking_data):
        raise NotImplementedError

    def compute_mask(self,explanation,data_shape,k,pixel_removed_per_step):
        mask_flat = torch.ones(explanation.shape[2]*explanation.shape[3]).to(explanation.device)
        saliency_scores,inds = torch.topk(explanation.view(-1),k,0,sorted=True)

        saliency_scores = saliency_scores[-pixel_removed_per_step:]

        if not self.cumulative:
            inds = inds[-pixel_removed_per_step:]

        mask_flat[inds] = 0
        mask = mask_flat.reshape(1,1,explanation.shape[2],explanation.shape[3])
        mask = torch.nn.functional.interpolate(mask,data_shape[2:],mode="nearest")
        return mask,saliency_scores

    def apply_mask(self,data1,data2,mask):
        data_masked = data1*mask + data2*(1-mask)
        return data_masked

    def update_data(self,data, i, y1, y2, x1, x2,masking_data):
        data[i:i+1,:,y1:y2,x1:x2] = masking_data[i:i+1,:,y1:y2,x1:x2]
        return data

    def compute_calibration_metric(self,all_score_list, all_sal_score_list):
        raise NotImplementedError

    def make_result_dic(self,auc_metric,calibration_metric):
        raise NotImplementedError

    def inference(self,model,data,save_all_class_scores,class_to_explain=None):
        output = model(data)
        if not save_all_class_scores:
            output = output[:,class_to_explain]
        return output

    def compute_scores(self,model,data,explanations,class_to_explain_list=None,masking_data=None,save_all_class_scores=False,return_data=False):

        with torch.no_grad():

            total_pixel_nb = explanations.shape[2]*explanations.shape[3]
            step_nb = min(self.max_step_nb,total_pixel_nb) if self.bound_max_step else total_pixel_nb
            pixel_removed_per_step = total_pixel_nb//step_nb

            if masking_data is None:
                masking_data = self.get_masking_data(data)

            dic = self.choose_data_order(data,masking_data)
            data1,data2 = dic["data1"],dic["data2"]

            all_score_list = []
            all_sal_score_list = []

            if return_data:
                all_data = []
            else:
                all_data = None

            for i in range(len(data1)):
                
                expl = explanations[i:i+1]
                left_pixel_nb = total_pixel_nb

                #Inference on initial image
                output = self.inference(model,data1[i:i+1],save_all_class_scores=False)

                if class_to_explain_list is None:
                    class_to_explain = torch.argmax(output,axis=1)[0]
                else:
                    class_to_explain = class_to_explain_list[i]
            
                if not save_all_class_scores:
                    output = output[:,class_to_explain]

                score_list = [output]
                saliency_score_list = []            
                iter_nb = 0

                #Computing perturbed images
                data_masked_list = []
                while left_pixel_nb > 0:

                    mask,saliency_scores = self.compute_mask(expl,data1.shape,pixel_removed_per_step*(iter_nb+1),pixel_removed_per_step)
                    mask = mask.to(data1.device)
                    data_masked = self.apply_mask(data1[i:i+1],data2[i:i+1],mask)
                    data_masked_list.append(data_masked)
                    saliency_score_list.append(saliency_scores.mean().item())
            
                    iter_nb += 1
                    left_pixel_nb -= pixel_removed_per_step

                data_masked_list = torch.cat(data_masked_list,dim=0)
                data_masked_chunks = torch.split(data_masked_list,self.batch_size)

                #Inference on perturbed images
                for data_masked in data_masked_chunks:
                    output = self.inference(model,data_masked,save_all_class_scores,class_to_explain)
                    score_list.append(output)        

                    if return_data and i %10==0:
                        all_data.append(data_masked.cpu())

                score_list = torch.cat(score_list,dim=0)

                all_score_list.append(score_list.cpu())
                all_sal_score_list.append(saliency_score_list)
            
            all_score_list = torch.stack(all_score_list).numpy()
            all_sal_score_list = np.array(all_sal_score_list)

        if return_data:
            all_data = torch.cat(all_data,dim=0)
            return all_score_list,all_sal_score_list,all_data
        else:
            return all_score_list,all_sal_score_list

    def __call__(self,model,data,explanations,class_to_explain_list=None,masking_data=None):
        all_score_list,all_sal_score_list = self.compute_scores(model,data,explanations,class_to_explain_list,masking_data)
        auc_metric = compute_auc_metric(all_score_list,self.cumulative)
        calibration_metric = self.compute_calibration_metric(all_score_list, all_sal_score_list)
        mean_auc_metric = auc_metric.mean()
        mean_calibration_metric = calibration_metric.mean()
        return self.make_result_dic(mean_auc_metric,mean_calibration_metric)

class Deletion(MultiStepMetric):
    def __init__(self,data_replace_method="black",bound_max_step=True,batch_size=20,max_step_nb=14*14,cumulative=True):
        super().__init__(data_replace_method,bound_max_step,batch_size,max_step_nb,cumulative)

    def choose_data_order(self,data,masking_data):
        return {"data1":data,"data2":masking_data}

    def compute_calibration_metric(self, all_score_list, all_sal_score_list):
        if self.cumulative:
            score_var = all_score_list[:,:-1] - all_score_list[:,1:] 
        else:
            score_var = all_score_list[:,0:1] - all_score_list[:,1:] 
        return compute_correlation(score_var, all_sal_score_list)

    def make_result_dic(self,auc_metric,calibration_metric):
        return {"dauc":auc_metric,"dc":calibration_metric}
         
class Insertion(MultiStepMetric):
    def __init__(self,data_replace_method="blur",bound_max_step=True,batch_size=20,max_step_nb=14*14,cumulative=True):
        super().__init__(data_replace_method,bound_max_step,batch_size,max_step_nb,cumulative)

    def choose_data_order(self,data,masking_data):
        return {"data1":masking_data,"data2":data}

    def compute_calibration_metric(self, all_score_list, all_sal_score_list):
        if self.cumulative:
            score_var = all_score_list[:,1:] - all_score_list[:,:-1]
        else:
            score_var = all_score_list[:,1:] - all_score_list[:,0:1]
        return compute_correlation(score_var, all_sal_score_list)

    def make_result_dic(self,auc_metric,calibration_metric):
        return {"iauc":auc_metric,"ic":calibration_metric}