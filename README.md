# AzAppServiceFirewallAudit_python3

This script is **Pending Verification**. The Azure environment it's currently running in executes properly but there are very few App Services deployed. I would like to know how well this works at scale (100-1000 App Services).

# Intro

This script will create two CSV files for Azure App Services: One list App Services and their firewall rules, and the other covering the SCM rules (Part of the management kudu service)

Originally created to help address the problems with querying multiple App Service's SiteConfig values at once as Azure does not return this data all at once (at least at original time of creation). See: https://github.com/Azure/azure-cli/issues/21548#issuecomment-1064633848

# Requirements

* Make sure you have an authenticated session to Az CLI. If you do not have the Az CLI installed, visit the following page: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli and run "az login".
* Install the modules listed in "requirements.txt" before executing the script with the following:

```
pip install -r requirements.txt
```



