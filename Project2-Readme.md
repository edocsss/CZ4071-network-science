1. Ssh to graph02
  ssh to grpNT06s@distgraph.scse.ntu.edu.sg, password is (see in WA)  
  `ssh grpNT06s@distgraph.scse.ntu.edu.sg`  
  ssh to graph02  
  `ssh graph02`  
  
2. Setting up environment variables for both single node and distributed.
There are two folders under graph02: single_node and distributed. We need to check if our code works in both modes.
For distributed, source the setup.sh under distributed directory, while for single node mode source the setup.sh under the single_node directory  
  `cd [single_node or distributed dir]`  
  `source setup.sh`  
  
This will set up the appropriate hadoop, java, and giraph environment variables according to the mode that is being used.   
  
3. Copying Java files
You need to copy your code into the giraph/custom-code directory under both single_node and distributed directory.   
  copy your .java files into [single_node or distributed]/giraph/custom-code  
  
4. Running custom code
  a. Ensuring environment variable  
  Be careful about which mode you are using because the environment variables affect how the jar is generated. So when you're using distributed make sure that the setup.sh for distributed is sourced, and vice versa for single_node.  
    
  b. Generating Jar  
  cd to the [single_node or distributed]/giraph/custom-code , then run generate-jar.sh using the .java file that you want to run.  
  `cd [single_node or distributed]/giraph/custom-code`  
  `./generate-jar.sh [JAVA_FILENAME].java`  
  This will generate the java class, a jar file that contains this class and its dependencies `custom-code.jar` in this directory, and copy the jar dependencies to the shared hadoop folder.  
    
  c. Running code  
  Under the custom-code directory. Just edit, copy and run the following code. Note that the JAVA_FILENAME, is the generated java class name, without the .class extension. So if you have PageRankComputation.class, just use PageRankComputation without the .class extension  
  
  `$HADOOP_HOME/bin/hadoop jar custom-code.jar org.apache.giraph.GiraphRunner [JAVA_FILENAME] --yarnjars custom-code.jar -w 1 -vif org.apache.giraph.io.formats.JsonLongDoubleFloatDoubleVertexInputFormat -vip /input/[txt_input] -vof org.apache.giraph.io.formats.IdWithValueTextOutputFormat  -op /output/[directory_output]`  
  
  Note for input and output, please read the relevant documentation of how to upload input to Hadoop File system  
  Basically just run:  
  `$HADOOP_HOME/bin/hadoop dfs -put [input_file] [hadoop input directory]`  
