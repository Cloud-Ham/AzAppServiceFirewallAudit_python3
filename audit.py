from os import system
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.subscription import SubscriptionClient
from azure.mgmt.web import WebSiteManagementClient
import csv

def main():
    # Delete the next line and line 1 if you don't care to have the terminal clear at script execution.
    system('clear')

    # AzAppServiceFilewallRules.csv will contain the App Service's Primary (Public site) firewall rules
    with open('AzAppServiceFirewallRules.csv', 'w') as fwfile:
        AzFirewallRules = csv.writer(fwfile)
        # Create the csv headers for AzAppServiceFirewallRules
        AzFirewallRules.writerow(['AppServiceName', 'ResourceGroup', 'AppKind', 'SCM_UseMain', 'Rulename', 'Description', 'IPAddress', 'Action', 'Priority', 'SubnetMask', 'VnetTrafficTag', 'SubnetTrafficTag', 'Tag', 'Headers'])

    # AzAppServiceScmRules.csv will contain the App Service's config/kudu service firewall rules.
    with open('AzAppServiceScmRules.csv', 'w') as scmfile:
        ScmFirewallRules = csv.writer(scmfile)
        # Create the csv headers for AzAppServiceScmRules
        ScmFirewallRules.writerow(['AppServiceName', 'ResourceGroup', 'AppKind', 'SCM_UserMain', 'Rulename', 'Description', 'IPAddress', 'Action', 'Priority', 'SubnetMask', 'VnetTrafficTag', 'SubnetTrafficTag', 'Tag', 'Headers'])

    # Use credentials from Az CLI. If you haven't already, login at the terminal using "az login"
    credential = AzureCliCredential()

    # Create the Subscription manager object
    sublist = SubscriptionClient(credential, base_url="https://management.azure.com")

    # Begin first loop, For Each Subscription that the authenticated session returns...
    for sub in sublist.subscriptions.list():

        # Begin 2nd loop, For Each Resource Group in each Subscription
        rg_client = ResourceManagementClient(credential, sub.subscription_id)
        for rg in rg_client.resource_groups.list():
            #
            # This establishes the client management for Azure App Services
            app_client = WebSiteManagementClient(credential, sub.subscription_id)
            #
            # This next loop associates the App Service to the Resource Group for the following loop
            # The "ip_security_restrictions" field always returns as "None" when querying more than one App Service
            # See the following Github post on this functionality: https://github.com/Azure/azure-cli/issues/21548#issuecomment-1064633848
            for app_rg in app_client.web_apps.list_by_resource_group(rg.name):
                
                # For each App Service in the current Resource Group
                for app_config in app_client.web_apps.list_configurations(app_rg.resource_group, app_rg.name):
                    
                    # Assign the type of app service (functionapp, app) to a variable for use in writing to the files.
                    app_kind = str(app_client.web_apps.get(app_rg.resource_group, app_rg.name).kind).split(",")[0]
                    
                    # Open file, then for each IP security Rule in the App, write details to a row in the AzAppServiceFirewallRules.csv
                    with open('AzAppServiceFirewallRules.csv', 'a') as fwfile:
                        AzFirewallRules = csv.writer(fwfile)
                        for ip_sec_res in app_config.ip_security_restrictions:
                            AzFirewallRules.writerow([app_rg.name, app_rg.resource_group, app_kind, app_config.scm_ip_security_restrictions_use_main ,ip_sec_res.name, ip_sec_res.description, ip_sec_res.ip_address, ip_sec_res.action, ip_sec_res.priority, ip_sec_res.subnet_mask, ip_sec_res.vnet_traffic_tag, ip_sec_res.subnet_traffic_tag, ip_sec_res.tag, ip_sec_res.headers])
                    
                    # Open file, then for each SCM security Rule in the App, write details to a row in the AzAppServiceSCMRules.csv
                    with open('AzAppServiceScmRules.csv', 'w') as scmfile:
                        ScmFirewallRules = csv.writer(scmfile)
                        for scm_sec_res in app_config.scm_ip_security_restrictions:
                            ScmFirewallRules.writerow([app_rg.name, app_rg.resource_group, app_kind, app_config.scm_ip_security_restrictions_use_main, scm_sec_res.name, scm_sec_res.description, scm_sec_res.ip_address, scm_sec_res.action, scm_sec_res.priority, scm_sec_res.subnet_mask, scm_sec_res.vnet_traffic_tag, scm_sec_res.subnet_traffic_tag, scm_sec_res.tag, scm_sec_res.headers])

if __name__ == "__main__":
    main()