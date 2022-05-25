#### Parking-recommendation-system-Autonmous-Vehicle
##OverView:
- Movapkg is a backage can set the goal with respect to map for a vehicle for the best parking should park or stop based on some features ,the setting the goal is based on prediction come from Machine Learning Model that have an ability to cluster the data to  3 parking spots with respect to the data which is traind on. 
- The idea of detrmining the parking of the vehicle or the pose that should be in it,it will save time and power ;thenfor, make the reponse of arriving the vehcile better on next request ,in other word "prediction the parking that near of next request will provide time for vehicle response "
  
**Sample of the Data-Set**  
![sss](https://user-images.githubusercontent.com/28098904/170249835-b28614e5-211e-4644-a013-682d5168ab81.PNG)

- you can check more about the creation of the model and preprocessing of the data from **ML_model_Recommender_last.ipynb** file 
**Ros-Nodes Side**
- By downloading the model and loaded it on Ros-node ,by getting the data that what we need from API and pass it to model to predict parking spots so,based on  prediction the Actionlib access the Movebase package and pass the cordinates and there are different cordinates for each spot that predicted 
## How to run it**
1- after cloning the package on [working-space](http://wiki.ros.org/catkin/Tutorials/create_a_workspace),run gazebo with your World or empty
2- run the navigation package that has move_base pkg like rtabmap  or amcl with rtabmap
3-run the node that load the model and produce the prediction to the map topic 
**HINT** in case you runned the gazebo with empty world just load your map.yaml by rosrun map_server map_server [filename.yaml]
![Screencast-from-05-25-2022-03_39_56-PM](https://user-images.githubusercontent.com/28098904/170280075-0171219c-5269-4c5a-a54a-3bf21029e1d3.gif)
