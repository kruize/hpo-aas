# hpo-aas

## Goal:
- Provide Hyperparameter Optimization(HPO) as a service to choose the optimal hyperparameters provided by the user for any model. 
- Primary use case is to optimize the performance of an environment by tuning below layers independently or together.
  * Container : resource usage like cpu and memory requests /limits.
  * Runtime: Ex : hotspot, openj9, nodeJS , etc.
  * Application stack:  Ex: Quarkus , Liberty, postgres etc.
  * OS layer.
 
## Intended Users: 
To improve the performance of the runtime / application server we would have lots of tunables to tune and those vary with the application and hardware we are running on. Manual tuning the multiple parameters with a large range is so cumbersome, and is hard to come up with an optimal configuration.
HPO as a service helps the user find the optimal parameter values for any model. As a use case, this service provides a list of all tunables along with their ranges that helps tune hotspot and Quarkus based on the application. 
*In the process of adding other tunables for different runtimes and application stacks.

# About HPO:
## What is HPO:
Hyperparameter optimization(HPO) is choosing a set of optimal hyperparameters that yields an optimal performance based on the predefined objective function. 

## Supporting Tools & Algorithms :
Optuna
TPE:  Tree-structured Parzen Estimator sampler.
TPE with multivariate
Scikit-Optimize
Hyperopt

The above tools mentioned supports Bayesian optimization which is part of a class of sequential model-based optimization(SMBO) algorithms for using results from a previous trial to improve the next.


## Definitions:
Search space : List of tunables with the ranges to optimize.
Study (an experiment in Autotune): It is to find the optimal set of tunable values through multiple trials.
Trials: Each trial is an execution of an objective function by running a benchmark/ application with the configuration generated by Bayesian.
Objective function: Decides where to sample in upcoming trials and returns the value which represents the performance of tunables (hyper parameters).

## What HPO as a Service provides you ?

Machine learning is a process of teaching a system to make accurate predictions based on the data fed. Hyperparamter optimization (/ tuning) in machine learning has different methods like Manual, Random search, Grid search, Bayesian optimization for increased efficiency. This HPO uses Bayesian optimization because of its multiple advantages. 
To tune any OS / application stack, there would be multiple tunables available for different layers and it is difficult to tune each of them based on the ranges available for the tunable and  requirement we have. Based on the objective function defined, bayesian helps in finding the optimal values for those tunables considering the past results. It explores the tunable ranges for the first few trials and exploits them in the next trials in a narrow range. 
HPO as a service provides you to
select any tool / framework to use. Currently, it supports optuna.
Select any algorithms of the framework. Currently, it uses TPE from optuna.
Tune one or multiple stacks. Supports both kubernetes and bare models.
Add your own layer of tunables which need to be tuned.
Configure how many trials you need for an experiment to get the optimal set. 
Run an experiment without any previous data available.
Append the existing data of an application/ benchmark to optuna study to generate the next configuration. This helps in re-using the available data to come up with an optimal set of values in lesser time.
Supports multiple optuna study for multiple experiments.

## Use Cases:
Tune resource usage of a container in a cluster.
Improve the response time of an application on an openshift cluster run on hotspot + Quarkus.
Few experiments are done for this use case with TechEmpower Quarkus benchmark on openshift cluster and the results are updated in kruize/autotune-results repo. In this case, a total of 31 tunables are used to optimize the performance and with multiple experiments, objective function was also improved to reflect the improvements of Performance which are defined in the repo.
Tune the RHEL OS environment variables to improve the performance.
Use the existing application data (from Horreum) to generate the next optimal configuration set.
        


## How to Access the Service:


With Autotune: https://github.com/kruize/autotune/blob/master/docs/autotune_install.md

Containerised HPO:

With Scripts: https://github.com/kruize/em-hpo-scripts/blob/main/README.md


## Workflow for HPO as a Service


Wrapper scripts to take input as Application autotune yaml & layer yamls (this will be copied by the user from autotune configs into a separate folder) and generate the search space json
Start the HPO service (start_hpo_servers.sh in autotune/tests)
Post the searchspace json with tunables to HPO
Get the config from HPO, (add objective function variables / queries from application autotune yaml?) & provide it to the user to run the experiment. 
User has to post experiment result in the specified format 
Wrapper scripts should compute objective function value (using Algebraic parser) and post it to HPO
Get the next config from HPO


Input: 
    -    layer tunables yaml
    
    -    slo yaml  ( Validate if obj function is based on function variables defined)
    
    -    no.of trials ; no.of parallel jobs
