#include<iostream>
#include<pcl/io/pcd_io.h>
#include<pcl/point_types.h>
#include<pcl/filters/passthrough.h>
#include<pcl/visualization/pcl_visualizer.h>
#include<pcl/visualization/cloud_viewer.h>
#include<pcl/filters/voxel_grid.h>
#include<pcl/octree/octree.h>
using namespace std;

int main(int argc, char** argv){
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_ptr (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::PointCloud<pcl::PointXYZ>& cloud = *cloud_ptr;
 if (pcl::io::loadPCDFile("test_pcd.pcd",cloud) ==-1){
	std::cout<<"Error"<<std::endl;
   	return(-1);
 } 

 // Apply filter over initial point cloud
 pcl::PassThrough<pcl::PointXYZ> pass(true);
 //pass.setInputCloud(cloud);
 pass.setFilterFieldName("z");
 pass.setFilterLimits(0.0,1.0);
 pass.filter(cloud);
 
 //vector<pcl::PointXYZ> data = cloud.points;
 for (int i = 0;i<cloud.points.size();i++)
   {
     cout<<cloud.points[i]<<endl;
   }

 // apply octree based search method
 
 
return(0);
}
