import numpy as np
class Node:
    def __init__(self,parent,rank=0,size=1):
        self.parent=parent
        self.rank=rank
        self.size=size

    def __repr__(self):
        return 'Node parent {} | rank {} | size {}'.format(self.parent,self.rank,self.size)

class Forest:
    def __init__(self,num_size):
        self.nodes=[Node(i) for i in range(num_size)]
        self.num_size=num_size

    def find(self,n):
        while n!=self.nodes[n].parent:
            n=self.nodes[n].parent
        return n
        # temp=n
        # while temp!=self.nodes[temp].parent:
        #     temp=self.nodes[temp].parent
        # self.nodes[n].parent=temp
        # return temp
    def merge(self,a,b):
        if self.nodes[a].rank>self.nodes[b].rank:
            self.nodes[b].parent=a
            self.nodes[a].size=self.nodes[a].size+self.nodes[b].size
        else:
            self.nodes[a].parent=b
            self.nodes[b].size=self.nodes[a].size+self.nodes[b].size
            if self.nodes[a].rank==self.nodes[b].rank:
                self.nodes[b].rank=self.nodes[b].rank+1
        self.num_size-=1

def diff(image,a,b,a1,b1):
    value=np.sum((image[b,a]-image[b1,a1])**2)
    return np.sqrt(value)

def create_edge(image,x,y,x1,y1,width):
    vertex_id=lambda x,y: y*width+x
    return (vertex_id(x,y),vertex_id(x1,y1),diff(image,x,y,x1,y1))

def create_graph(image,height,width,neighbor_8=True):
    edges=[]
    for i in range(height):
        for j in range(width):
            if j>0:
                edges.append(create_edge(image,j,i,j-1,i,width))
            if i>0:
                edges.append(create_edge(image,j,i,j,i-1,width))
            if neighbor_8:
                if j>0 and i>0:
                    edges.append(create_edge(image,j,i,j-1,i-1,width))
                if j>0 and i+1<=height-1:
                    edges.append(create_edge(image,j,i,j-1,i+1,width))
    return edges

def threshold_func(size,const):
    return const*1.0/size

def remove_small_segmentation(forest,edges,min_size):
    for edge in edges:
        temp_a=forest.find(edge[0])
        temp_b=forest.find(edge[1])
        if temp_a!=temp_b and (forest.nodes[temp_a].size<min_size or forest.nodes[temp_b].size<min_size):
            forest.merge(temp_a,temp_b)
    return forest

def segmentation_graph(image,height,width,const_value,min_size):
    forest=Forest(height*width)
    edges=create_graph(image,height,width)
    weight=lambda x:x[2]
    edges=sorted(edges,key=weight)
    threshold=[threshold_func(1,const_value) for i in range(height*width)]#max_diff
    for edge in edges:
        a,b,diff_value=edge[0],edge[1],edge[2]
        a_parent=forest.find(a)
        b_parent=forest.find(b)
        a_condition=diff_value<=threshold[a_parent]
        b_condition=diff_value<=threshold[b_parent]
        if a_parent!=b_parent and a_condition and b_condition:
            forest.merge(a_parent,b_parent)
            temp_parent=forest.find(a_parent)
            threshold[temp_parent]=diff_value+threshold_func(forest.nodes[temp_parent].size,const_value)

    return remove_small_segmentation(forest,edges,min_size)
