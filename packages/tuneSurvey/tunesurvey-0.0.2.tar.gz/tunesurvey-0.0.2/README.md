# tuneSurvey

Survey on combination of preprocesses/ features/ model types and hyperparameters on their performances and implications on the data.

Inspired by the question "can we automate what is done by statisticians". Answering only one part of the question: "how to automate predictive model selection?"
The purpose overlaps with various AutoMLs online. But I wish this "modelzoo" cares about tuning and selecting simpler models to:
 - avoid overfitting
 - save time on computing (with default high or low level parallelization)
 - give inferences and interpretations of the data just like [1].
 - compare and visualize if the model selection(AutoML) process is repeatable, stable without data-leaking.

You may use this package for model building/ selection and dataset evaluation by choosing from the lists of models and procedures to compromise computing time.

Therefore I included many basic(almost naive) models from statsmodels. For regular tabular datasets, there are variations of GLM, ANOVA. For time series, AR, MA and ARMA models and some other traditional models like GARCH is considered.
For machine learning, the default tunegrid considers models list in an analogy to the history of the models, including Lasso, ElasticNet, SVM, Trees, Bagged predictors and boosting predictors (tuning are easily parallelable by joblib). To address the big data problem I also plan to include  SGD version of traditional ML, and models like lightgbm to address big data, and within-model parallelization. 
For deep learning, the module deals with Pytorch to call LSTM, transformers and variations of which (conformers, informers) for time series data. NNs can be searched on GPU using within-model parallelization and will be  considerably slow, but thanks to the property of SGD we can use pruner methods with Optuna to truncate a lot of the trails when the model clearly overfit or has no sign of convergence after some number of trails, the  tunegrid will not be a gridsearch, but we can still load the results and make multi-variable visualization. Other NNs are considered but will not be stressed.
Specifically, for interpretability in physics and dynamics, the package is designed to call PySR for symbolic regression, so that we can find elementary function solutions to the problem. However, this is an experimental feature.


The progress of model building (typically for a hackathon) involves:

 - data pre-proc, grouping, encoding and reshaping
 - data cleaning
 - feature building and selection
 - inference tests for model/feature validification
 - data transformations (for symmerty, stable models)
 - model selection between different types of assumptions
 - model hyper-parameter tune
 - model evaluations (in the outer validation set)

The package aim to collect data on different options for each designated procedure.

Considering the complexity to collect on all permutations, some procedural reduce, e.x. RFE for features and reduce GridSearch by inner CV can be done, and lists of models can be saved with a name linked to its tunegrid row to be extracted later.

Considering some models are generalization of others, the list of model is built to roughly resembles the history of the evolvement of models, so that we can see whether a small generalization increases accuracy on a test set.

Considering that some dataframes need multiple models to predict a serial, single term, and others might need transforming from single observation to counts within time frames, there are functions predefined.

For handiness for Datathon and Hackathon purpose (and also for safety) some visualization functions are added.

Some useful references on how to use machine learnings **safely and systematically** that I recommend reading:

(1) Applied Predictive Modeling. Kuhn an Johnson
Much of the "historical order of models" loosely follows this book.
(2) Deep Learning. Goodfellow
On regularizations and kernelizations, and how to tune models
(3) This lecture by Prof. Hulten(and the prerequisites for NFL theorem) https://www.youtube.com/watch?v=ZXWv3aA8JsI
(4) This video by Optuna https://www.youtube.com/watch?v=P6NwZVl8ttc
(5) This website by Prof. Miles Cranmer https://astroautomata.com/PySR/


Let's reduce overfit, find interpretability and safety in the modelfitting process!

For the list of relevant Hackathon project I participated that inspired and inspired by this package project:
[1]UCI 2022 ML Hackathon https://www.informatics.uci.edu/uci-ml-repository-highlights-four-impactful-projects-at-2022-ml-hackathon/
[2]Embark Datathon Data@UCI 2023 https://devpost.com/software/montreal-crime-space-time-analysis
