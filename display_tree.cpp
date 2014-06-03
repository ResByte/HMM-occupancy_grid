#include <octomap/octomap.h>
#include <octomap/OcTree.h>
#include <octomap/OccupancyOcTreeBase.h>
#include <octomap/OcTreeDataNode.h>
#include <octomap/Pointcloud.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include<pcl/filters/passthrough.h>
#include<pcl/filters/statistical_outlier_removal.h>
#include<pcl/visualization/cloud_viewer.h>
#include<pcl/io/pcd_io.h>
#include<stdio.h>
using namespace std;
using namespace octomap;


void print_query_info(point3d query, OcTreeNode* node) {
  if (node != NULL) {
    cout << "occupancy probability at " << query << ":\t " << node->getOccupancy() << endl;
  }
  else 
    cout << "occupancy probability at " << query << ":\t is unknown" << endl;    
}

int main(int argc, char** argv) {

  cout << endl;
  cout << "generating example map" << endl;
  pcl::PointCloud<pcl::PointXYZRGB>::Ptr static_cld(new pcl::PointCloud<pcl::PointXYZRGB>);
  pcl::PointCloud<pcl::PointXYZRGB>::Ptr dynamic_cld(new pcl::PointCloud<pcl::PointXYZRGB>);
 
  if (pcl::io::loadPCDFile<pcl::PointXYZRGB>("static.pcd",*static_cld)==-1){
     std::cout<<"ERror"<<std::endl;
}
  if (pcl::io::loadPCDFile<pcl::PointXYZRGB>("chair.pcd",*dynamic_cld)==-1){
         std::cout<<"ERror"<<std::endl;
  }

	
  OcTree st_tree (0.01);  // create empty tree with resolution 0.1
  OcTree dy_tree (0.01);
  octomap::Pointcloud st_cld,dy_cld;
  //OccupancyOcTreeBase<OcTreeDataNode<float> >  st_occ(0.01);

  // insert some measurements of occupied cells
/*
  for (int x=-40; x<80; x++) {
    for (int y=-10; y<20; y++) {
      for (int z=-30; z<20; z++) {
        point3d endpoint ((float) x*0.05f, (float) y*0.05f, (float) z*0.05f);
        tree.updateNode(endpoint, true); // integrate 'occupied' measurement
      }
    }
  }

  // insert some measurements of free cells

  for (int x=-30; x<30; x++) {
    for (int y=-30; y<30; y++) {
      for (int z=-30; z<30; z++) {
        point3d endpoint ((float) x*0.02f-1.0f, (float) y*0.02f-1.0f, (float) z*0.02f-1.0f);
        tree.updateNode(endpoint, false);  // integrate 'free' measurement
      }
    }
  }
*/
  for(int i = 0;i<static_cld->size();i++){
//	cout<<static_cld->points[i]<<endl;
	point3d endpoint((float) static_cld->points[i].x,(float) static_cld->points[i].y,(float) static_cld->points[i].z);
	st_cld.push_back(endpoint);
	//st_tree.updateNode(endpoint,true);
  }
for(int i = 0;i<dynamic_cld->size();i++){
//	cout<<static_cld->points[i]<<endl;
	point3d endpoint((float) dynamic_cld->points[i].x,(float) dynamic_cld->points[i].y,(float) dynamic_cld->points[i].z);
	dy_cld.push_back(endpoint);
	//dy_tree.updateNode(endpoint,true);
  }

point3d origin(0.0,0.0,0.0);
st_tree.insertPointCloud(st_cld,origin);
st_tree.updateInnerOccupancy();

//st_occ.insertPointCloud(st_cld,origin);


for(OcTree::leaf_iterator it = st_tree.begin_leafs(),
       end=st_tree.end_leafs(); it!= end; ++it)
{
  //manipulate node, e.g.:
  std::cout << "Node center: " << it.getCoordinate() << std::endl;
  std::cout << "Node size: " << it.getSize() << std::endl;
  std::cout << "Node value: " << it->getValue() << std::endl;
  //v=v+(pow(it.getSize(),3));
}
//st_tree.computeUpdate(dy_cld,origin);

//dy_tree.insertPointCloud(dy_cld,origin);

/*
for(leaf_iterator it = st_tree->begin_leafs(),end = st_tree->end_leafs();it!=end;++it ){
	 std::cout << "Node center: " << it.getCoordinate() << std::endl;
	std::cout << "Node size: " << it.getSize() << std::endl;
	std::cout << "Node value: " << it->getValue() << std::endl;

}
*/

/*    
  point3d origin(0.0,0.0,0.0);	
  //tree.insertPointCloud(static_cld,origin); 
  cout << endl;
  cout << "performing some queries:" << endl;
  
  point3d query (0., 0., 0.);
  OcTreeNode* result = tree.search (query);
  print_query_info(query, result);

  query = point3d(-1.,-1.,-1.);
  result = tree.search (query);
  print_query_info(query, result);

  query = point3d(1.,1.,1.);
  result = tree.search (query);
  print_query_info(query, result);


  cout << endl;
*/
  st_tree.writeBinary("static_occ.bt");
  
//  dy_tree.writeBinary("dynamic_tree.bt");
  
  cout << "wrote example file simple_tree.bt" << endl << endl;
  cout << "now you can use octovis to visualize: octovis simple_tree.bt"  << endl;
  cout << "Hint: hit 'F'-key in viewer to see the freespace" << endl  << endl;  

}
