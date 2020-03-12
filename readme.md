# Getting started


# Assumptions - Route Finding
1. Shuttle routes are not included. These include the Alewife-Harvard shuttle that is included in the "shape" api request that is associated with the redline during construction. 
2. Despite variations within a route, all stops are combined and associated with a route. For example, there are both Braintree-Alewife and Ashmont-Alewife trains on the red line routes. This solution associates all of those stops with the red route despite the Braintree/Ashmont variations. 
3. Optimization: For finding the route, optmization is based on the number of route switches instead of number of stops for the choosen route. I recognize that there are sceanrios where is may be significantly faster to switch routes additional times rather than ride further on a single route. 
