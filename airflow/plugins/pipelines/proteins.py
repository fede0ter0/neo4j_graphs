from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import xmltodict, json, logging

URI = "bolt://host.docker.internal:7687"
AUTH = ("neo4j", "neo4j")

class Neo4jApp:
    def __init__(self,uri,auth):
        self.driver = GraphDatabase.driver(uri, auth=(auth[0], auth[1]))

    def close(self):
        self.driver.close()

    def insert_node(self,query):
        with self.driver.session(database="neo4j") as session:
            try:
                result = session.run(query)
            except ServiceUnavailable as exception:
                logging.error("{query} raised an error: \n {exception}".format(query=query, exception=exception))
                raise

def get_piece_json(json_content,object_loc):
    all_keys = object_loc.split(".")
    it = json_content
    for k in all_keys:
        it = it[k]
    return it

def make_query_node(node_type,node_instances_json,properties_loc_json,ind=None):
    node_type = node_type.capitalize()
    query_node = "{"
    for p in properties_loc_json:
        property_label = p['label']
        prop_loc = p['property_location']
        property_value = get_piece_json(node_instances_json,prop_loc)
        if ind != None:
            name_att = p['property_sub_location']
            property_value = property_value[ind][name_att]
        if property_label == 'name':
            node_name = property_value.lower()
        query_node = query_node + f"{property_label}: \'{property_value}\',"
    query_node = query_node[:-1] + "}"
    query_node = f"CREATE ({node_name}:{node_type} " + query_node + ")" 
    return query_node

def create_nodes(json_schema,json_content):
    nodes = json_schema['nodes']
    query_nodes = ""
    for n in nodes:
        for name,attributes in n.items():
            node_loc = attributes.get('node_location')
            properties_loc = attributes.get('properties')
            node_instances = get_piece_json(json_content,node_loc)
            if isinstance(node_instances,list):
                query_node_instance = ""
                for i,inst in enumerate(node_instances,start=0):
                    query_node_instance = make_query_node(name,json_content,properties_loc,i)
                    query_nodes = query_nodes + query_node_instance + "\n"
            elif isinstance(node_instances,dict):
                query_node_instance = make_query_node(name,json_content,properties_loc)
                query_nodes = query_nodes + query_node_instance + "\n"
    query_nodes = query_nodes[:-1]

    return query_nodes

def run_pipeline():
    protfile_xml = open("data/Q9Y261.xml","r")
    protfile_content = protfile_xml.read()
    protdict=xmltodict.parse(protfile_content)
    
    protfile_schema = open("schemas/uniprot.json")
    protfile_schema_dict = json.load(protfile_schema)

    nodes = protfile_schema_dict['nodes']
    query = create_nodes(protfile_schema_dict,protdict)
    print('lets see the query')
    print(query)

    app = Neo4jApp(URI,AUTH)
    app.insert_node(query)
    app.close()