import networkx as nx
import random as rnd
from fractions import Fraction

class Graph:
    def __init__(self,ini=False,di=True):
        if ini is True:
            self.di=di
            if di is False:
                self.G=nx.Graph()
            else:
                self.G=nx.DiGraph()
        self.n=len(self.G.nodes())
        self.m=len(self.G.edges())
        self.sorted_edges={}
        self.sorted_nodes={}

    # set_type: 0 edges, 1 nodes
    # get the attribute of an element e
    def e_attr(self, e, attr='weight', set_type=0):
        val=-1
        if attr=='name':
            # textify the element
            if set_type==0:
                val = '_'.join(map(str, e))
            elif set_type==1:
                val = str(e)
        else:
            # get the attr value
            if set_type==0:
                val = self.G[e[0]][e[1]][attr]
            elif set_type==1:
                val = self.G.node[e][attr]
        return val

    def e_attr_sum(self,e_lst,attr='weight', set_type=0):
        attr_lst=[self.e_attr(e,attr,set_type) for e in e_lst]
        return sum(attr_lst)

    def edges_sorted(self,attr='weight',reverse=False):
        if (attr,reverse) not in self.sorted_edges:
            tmp_edges=self.G.edges(data=True)
            if self.di:
                self.sorted_edges[(attr,reverse)]=[(a,b) for a,b,c in sorted(tmp_edges,key=lambda x: x[2][attr],reverse=reverse)]
            else:
                self.sorted_edges[(attr,reverse)]=[tuple(sorted((a,b))) for a,b,c in sorted(tmp_edges,key=lambda x: x[2][attr],reverse=reverse)]

        return self.sorted_edges[(attr,reverse)]

    
    def nodes_sorted(self,attr='weight',reverse=False):
        if (attr,reverse) not in self.sorted_nodes:
            tmp_nodes=self.G.nodes(data=True)
            self.sorted_nodes[(attr,reverse)]=[a for a,b in sorted(tmp_nodes,key=lambda x: x[1][attr],reverse=reverse)]

        return self.sorted_nodes[(attr,reverse)]

    def label_st(self,s=0,t=-1):
        if t==-1:
            t=self.n-1
            print(t)
            print(self.G.nodes())
        mapping={s:'s',t:'t'}
        print(mapping)
        self.G=nx.relabel_nodes(self.G,mapping,copy=False)

    def getAttr(self,attLst):
        attrs=[]
        for attr in attLst:
            att_mp={}
            for e in self.G.edges():
                att_mp[e]=self.G[e[0]][e[1]][attr]
            attrs.append(att_mp.copy())
        return attrs

    def to_directed(self):
        if self.di is False:
            self.G=self.G.to_directed()
            self.di=True

    def SP(self,src,tgt,attr='weight'):
        sp=nx.shortest_path(self.G,src,tgt,attr)
        sol=[(sp[i],sp[i+1]) for i in range(len(sp)-1)]
        val=self.e_attr_sum(sol,attr='cost')

        ### test if sol is correctly constructed
        #spLen=nx.shortest_path_length(self.G,src,tgt,attr)
        #print(spLen==val)
        ### end test

        return val,sol

    def STMinCut(self,src,tgt,inf_val,attr='weight'):
        val,set_part=nx.minimum_cut(self.G,src,tgt,capacity=attr)
        if val>=inf_val:
            val=-1
            sol=-1
        else:
            #if self.di is True:
            sol=[e for e in self.edges_sorted() if e[0] in set_part[0] and 
                e[1] in set_part[1]]
            #else:
            #    sol=[e for e in self.edges_sorted() if (e[0] in set_part[0] and 
            #        e[1] in set_part[1]) or (e[0] in set_part[1] and 
            #        e[1] in set_part[0])]
            #print(val)
            #print(sol)
            ### test if sol is correctly constructed
            #val1=self.e_attr_sum(sol)
            #print(val==val1)
            ### test end
            
        return val, sol

    def MST(self, edges=True):
        if edges is True:
            return nx.minimum_spanning_edges(self.G)
        else:
            return nx.minimum_spanning_tree(self.G)

    def print_edgelist(self, wname='out_graph.dat'):
        nx.write_edgelist(self.G, wname, data=True)
        
    def MF(self,src,snk):
        return nx.maximum_flow_value(self.G,src,snk,'weight')

    def delta(self,v, out=True):
        if self.di is False:
            return self.G.edges(v)
        else:
            if out is True:
                return self.G.out_edges(v)
            else:
                return self.G.in_edges(v)

    def adjList(self, v,out=True):
        if self.di is False:
            return nx.all_neighbors(self.G, v)
        else:
            if out is True:
                return self.G.neighbors(v)
            else:
                return self.G.predecessors(v)

    def totalW(self, MST):
        w = 0.0
        for e in MST:
            w += e[2]['weight']
        return w

    def residualG(self,f):
        resG=Graph(ini=True,di=True)
        resG.G.add_nodes_from(self.G)
        for e in self.G.edges():
            c_f=self.G[e[0]][e[1]]['weight']-f[e]
            if c_f>0:
                resG.G.add_edge(e[0],e[1])
                resG.G[e[0]][e[1]]['cap']=c_f
                resG.G[e[0]][e[1]]['weight'] = 1
                resG.G[e[0]][e[1]]['dir'] = 'f'
            if f[e]>0:
                resG.G.add_edge(e[1],e[0])
                resG.G[e[1]][e[0]]['cap'] = f[e]
                resG.G[e[1]][e[0]]['weight'] = 1
                resG.G[e[1]][e[0]]['dir'] = 'r'
        return resG



class CompleteGraph(Graph):
    def __init__(self,n=4,lb=1.0,ub=10.0, int_weight=True, st=False,name=''):
        if name=='':
            self.name='Complete_'+ str(n)
        else:
            self.name=name
        self.G=nx.complete_graph(n)
        self.di=False
        for e in self.G.edges():
            #self.G[e[0]][e[1]]['weight'] = rnd.randint(int(lb),int(ub))
            tmpVal=rnd.random()*(ub-lb)+lb
            if int_weight is True:
                tmpVal=int(tmpVal)
            self.G[e[0]][e[1]]['weight']=tmpVal

        Graph.__init__(self)
        if st is True:
            self.label_st()

class GraphFromCopy(Graph):
    def __init__(self,myg):
        self.name=myg.name+'_copy'
        self.G=myg.G.copy()
        self.di=myg.di
        super().__init__()

class GraphFromFile(Graph):
    def __init__(self,fpath,gname, keyParseFun=None, mysep='\t',pofix='.dat'):
        self.name=gname
        fname=fpath+gname+pofix

        f = open(fname, 'r')
        header=splitby(' \t,', f.readline().strip('\n\t\r'))
        
        # update digrap
        if header[0]=='T':
            digraph=True
        elif header[0]=='i':
            digraph=False
        else:
            print('Input has wrong header:', header)
            exit()

        if digraph is False:
            self.G=nx.Graph()
            self.di=False
        else:
            self.G=nx.DiGraph()
            self.di=True

        # check if needs to add nodes first
        if (header[0]=='T' and header[1]!='H') or (header[0]=='i' and header[1]!='j'):
            add_nodes=True
        else:
            add_nodes=False
        
        # add nodes
        if add_nodes is True:
            header=self.read_elements(f, mysep, header, ele_name=1, parseFun=keyParseFun)

        self.read_elements(f, mysep, header, parseFun=keyParseFun)

        Graph.__init__(self)

    # ele_name: 0, edges; 1, nodes
    def read_elements(self, f, mysep, header, ele_name=0, parseFun=None):
        if ele_name==0:
            col_offset=2
        else:
            col_offset=1
        
        gInfo=[]
        attrInfo={}
        attrs=header[col_offset:]

        ret_header=None

        for line in f:
            row=splitby(' \t,', line.rstrip('\n\t\r'))
            if len(row)==0 or row[0]=='':
                continue
            elif row[0]=='i' or row[0]=='T':
                ret_header=row
                break

            tmp=[]
            for i in range(col_offset):
                if parseFun is None:
                    tmp.append(row[i])
                else:
                    tmp.append(parseFun(row[i]))
            
            for i,attr in enumerate(attrs,col_offset):
                attrInfo[tuple(tmp),attr]=row[i]
            
            if ele_name==0:
                gInfo.append(tuple(tmp.copy()))
            else:
                gInfo.append(tmp[0])

        
        if ele_name==0:
            self.G.add_edges_from(gInfo)
            for u,v in gInfo:
                for attr in attrs:
                    try:
                        self.G[u][v][attr]=float(attrInfo[(u,v),attr])
                    except:
                        pass
                    try:
                        self.G[u][v][attr]=Fraction(attrInfo[(u,v),attr])
                    except:
                        self.G[u][v][attr]=attrInfo[(u,v),attr]
        else:
            self.G.add_nodes_from(gInfo)
            for v in gInfo:
                for attr in attrs:
                    try:
                        self.G.node[v][attr]=float(attrInfo[(v,),attr])
                    except:
                        pass
                    try:
                        self.G[u][v][attr]=Fraction(attrInfo[(u,v),attr])
                    except:
                        self.G.node[v][attr]=attrInfo[(v,),attr]

        return ret_header

def splitby(seps, text):
    for c in seps:
        text = text.replace(c, ' ')
    return text.split()



if __name__ == '__main__':
    fpath = './'
    gname = 'g3'
    g = GraphFromFile(fpath, gname)
    print(g.G.edges(data=True))
