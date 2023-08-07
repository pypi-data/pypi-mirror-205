The following report describes the test and evaluation of multiple
algorithms, with links to their individual more detailed reports.

Algorithm             AUC     Time (m)
--------------------  ------  --------
{% for algorithm in algorithm_results -%}
{{"%-20s" | format(algorithm)}}  {{"%4s" | format(algorithm_results[algorithm]['test_auc'])}}  {{"%4s" | format(algorithm_results[algorithm]['tande_time'])}}
{% endfor %}

# Detailed Algorithm Reports
{% for algorithm in algorithm_results -%}
## {{algorithm}}
- Report: [{{algorithm}}]({{algorithm}}/index.html)

![{{algorithm}} ROC curve]({{algorithm}}/results-ROC.png)

{% endfor %}
