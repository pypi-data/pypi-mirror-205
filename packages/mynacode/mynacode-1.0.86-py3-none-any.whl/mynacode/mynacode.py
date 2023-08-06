import numpy as np
import os, sys
import json, requests, ast
import pkg_resources
import GPUtil, platform, psutil
from datetime import datetime
from sklearn import metrics
from sklearn.metrics import confusion_matrix

#protocol = 'https'
protocol = 'http'


IP = '127.0.0.1:8000'
#IP = 'mynacode.com'
#prev_func_list = ['a1zqw_9_', 'b1zqw_9_']
prev_func_list = []
prev_node = -999
username = ""
key = ""
  

def login(uname, ky):
  global username
  global key
  
  print("Logging in...")
  credentials = {'username':uname, 'key':ky, 'task':'login'}
  response = requests.post(protocol+'://'+IP+'/api/python_login', data=credentials)
  
  if response.text == '1':
    username = uname
    key = ky
    print("Successfully connected to mynacode!")
  else:
    print("Credentials could not be verified.")


def metadata(run_id = -999):

  installed_packages = pkg_resources.working_set #Save all installed packages for that project
  installed_packages_list = sorted(["%s = %s" % (i.key, i.version) for i in installed_packages])

  system_info_list = ['Codebase Python ' + platform.python_version()]
  
  system_info_list.append("    GPU    ")
  try:
      gpus = GPUtil.getGPUs()
      if len(gpus) == 0:
          system_info_list.append("No NVIDIA GPU found")
      else:
          for gpu in gpus:
            gpu_id = gpu.id
            gpu_name = gpu.name
            gpu_memory = gpu.memoryTotal
            system_info_list.append("GPU ID " + str(gpu_id))
            system_info_list.append(gpu_name)
            system_info_list.append(str(gpu_memory) + " MB")
  except:
      system_info_list.append("No NVIDIA Driver found")

  system_info_list.append("    CPU    ")
  system_info_list.append(platform.processor())
  system_info_list.append(platform.platform())
  system_info_list.append(platform.machine())
  system_info_list.append("    MEMORY    ")
  system_info_list.append("RAM " + str(round(psutil.virtual_memory().total / (1024.0 **3))) + " GB")

  data = {'run_id' : run_id, 'installed_packages': str(installed_packages_list), 'username': username, 'key': key, 'system_information': str(system_info_list)}
  
  response = requests.post(protocol+'://'+IP+'/api/add_metadata', data=data)
  
  if response.text == '0':
    print("Authentication failed")
  else:
    print("Metadata saved")
   



def datasets(train, test, val, run_id = -999):

  train = np.array(train)
  test = np.array(test)
  val = np.array(val)

  train_shape = train.shape
  test_shape = test.shape
  val_shape = val.shape


  data = {'run_id': run_id, 'train_shape' : train_shape, 'test_shape': test_shape, 'val_shape': val_shape,
          'username': username, 'key': key}
  
  response = requests.post(protocol+'://'+IP+'/api/add_datasets', data=data)
  
  if response.text == '0':
    print("Authentication failed")
  else:
    print("Datasets Information saved.")

def csv_data(dataframe, run_id = -999):
    columns_list = dataframe.columns.values.tolist()
    isnull_list = dataframe.isnull().sum().values.tolist()
    isunique_list = dataframe.nunique().values.tolist()
    dtypes_list = dataframe.dtypes.tolist()

    data = {'run_id': run_id, 'columns_list': columns_list, 'isnull_list': isnull_list, 'isunique_list': isunique_list, 'dtypes_list': dtypes_list}

    response = requests.post(protocol+'://'+IP+'/api/add_csv', data=data)

    if response.text == '0':
      print("Authentication failed")
    else:
      print("CSV Information saved.")

    

def specificity(y_true, y_pred):
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_truth = np.count_nonzero(y_true == 0)
   
    return float(y_correct/y_truth)

def npv(y_true, y_pred): #Negative Predicted Value
    y_correct = np.isnan(np.divide(y_pred, y_true)) #0/0 -> nan, 1/0 -> inf
    y_correct = np.sum(y_correct)
    y_predicted = np.count_nonzero(y_pred == 0)
   
    return float(y_correct/y_predicted)

def get_roc_auc(y_true, y_pred):
    fpr, tpr, threshold = roc_curve(y_true, y_pred)
    roc_auc = auc(fpr, tpr)
    gmeans = np.sqrt(tpr * (1 - fpr))
    index = np.argmax(gmeans) #Returns index of max value
    best_threshold = threshold[index]
   
    return fpr, tpr, roc_auc, gmeans, best_threshold, index

def get_metrics(y_true, y_pred, threshold):
    y_pred_binary = (y_pred > threshold).astype('float')
   
    prec = metrics.precision_score(y_true, y_pred_binary)
    rec = metrics.recall_score(y_true, y_pred_binary)
    spec = specificity(y_true, y_pred_binary)
    f1 = metrics.f1_score(y_true, y_pred_binary)
    acc = metrics.accuracy_score(y_true, y_pred_binary)
    npv_val = npv(y_true, y_pred_binary)
   
    c_matrix = confusion_matrix(y_true, y_pred_binary, labels=[0,1])
   
    return prec, rec, spec, f1, acc, npv_val, c_matrix



def results(y_predicted, y_true, run_id, threshold = 0.5, problem_type = 'binary classification'):
    prec, rec, spec, f1, acc, npv_val, c_matrix = get_metrics(y_true, y_predicted, threshold)
    fpr, tpr, roc_auc, gmeans, best_threshold, index = get_roc_auc(y_true, y_predicted)
    #t_cmatrix = PrettyTable(['', 'No Disease', 'Disease'])
    #t_cmatrix.add_row(["No Disease", c_matrix[0][0], c_matrix[0][1]])
    #t_cmatrix.add_row(["Disease", c_matrix[1][0], c_matrix[1][1]])                
    #print(t_cmatrix)

    data = {'run_id' : run_id, 'precision': prec, 'recall': recall, 'specificity': spec, 'f1': f1, 'accuracy': acc, 'npv': npv, 'c_matrix': c_matrix,
            'username': username, 'key': key, 'test_auc': roc_auc}

    response = requests.post(protocol+'://'+IP+'/api/add_results', data=data)
  
    if response.text == '0':
      print("Authentication failed")
    else:
      print("Results saved")
 



